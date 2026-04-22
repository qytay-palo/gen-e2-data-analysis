"""SharePoint extraction utilities for workforce datasets."""

from __future__ import annotations

import fnmatch
import io
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import polars as pl
from loguru import logger
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File


@dataclass
class SharePointSettings:
    """Settings required to access SharePoint-hosted workforce files."""

    site_url: str
    workforce_folder: str
    client_id: str | None = None
    client_secret: str | None = None
    tenant_id: str | None = None
    username: str | None = None
    password: str | None = None

    @classmethod
    def from_env(cls) -> "SharePointSettings":
        """Build settings from environment variables."""
        return cls(
            site_url=os.getenv("SHAREPOINT_SITE_URL", ""),
            workforce_folder=os.getenv("SHAREPOINT_WORKFORCE_FOLDER", ""),
            client_id=os.getenv("SHAREPOINT_CLIENT_ID") or None,
            client_secret=os.getenv("SHAREPOINT_CLIENT_SECRET") or None,
            tenant_id=os.getenv("SHAREPOINT_TENANT_ID") or None,
            username=os.getenv("SHAREPOINT_USERNAME") or None,
            password=os.getenv("SHAREPOINT_PASSWORD") or None,
        )

    def validate(self) -> None:
        """Validate that enough credentials exist to authenticate."""
        if not self.site_url:
            raise ValueError("SHAREPOINT_SITE_URL is required")
        if not self.workforce_folder:
            raise ValueError("SHAREPOINT_WORKFORCE_FOLDER is required")

        has_user_credentials = bool(self.username and self.password)
        has_app_credentials = bool(self.client_id and self.client_secret)

        if not (has_user_credentials or has_app_credentials):
            raise ValueError(
                "Provide either username/password or client_id/"
                "client_secret credentials"
            )


class SharePointConnector:
    """Download CSV files from SharePoint and load them into Polars."""

    def __init__(self, settings: SharePointSettings | None = None) -> None:
        self.settings = settings or SharePointSettings.from_env()
        self.settings.validate()
        self._context = self._build_context()

    def _build_context(self) -> ClientContext:
        if self.settings.client_id and self.settings.client_secret:
            logger.info("Using client credential SharePoint authentication")
            return ClientContext(self.settings.site_url).with_credentials(
                ClientCredential(
                    self.settings.client_id,
                    self.settings.client_secret,
                )
            )

        logger.info("Using username/password SharePoint authentication")
        return ClientContext(self.settings.site_url).with_credentials(
            UserCredential(self.settings.username or "", self.settings.password or "")
        )

    @staticmethod
    def _normalize_server_relative_url(path: str) -> str:
        return path if path.startswith("/") else f"/{path}"

    def list_files(self, folder_path: str | None = None) -> List[Dict[str, Any]]:
        """List files available in a SharePoint folder."""
        target_folder = self._normalize_server_relative_url(
            folder_path or self.settings.workforce_folder
        )
        folder = self._context.web.get_folder_by_server_relative_url(target_folder)
        files = folder.files.get().execute_query()
        return [
            {
                "name": file.properties.get("Name", ""),
                "server_relative_url": file.properties.get("ServerRelativeUrl", ""),
            }
            for file in files
        ]

    def extract_file(self, file_path: str) -> pl.DataFrame:
        """Download a CSV file from SharePoint into a Polars DataFrame."""
        target_path = self._normalize_server_relative_url(file_path)
        file_bytes = self._download_file_bytes(target_path)
        dataframe = pl.read_csv(io.BytesIO(file_bytes))
        logger.info(
            f"Loaded {Path(target_path).name} with {dataframe.height} rows "
            f"and {dataframe.width} columns"
        )
        return dataframe

    def _download_file_bytes(self, file_path: str) -> bytes:
        """Download raw file bytes from SharePoint without rewriting the content."""
        target_path = self._normalize_server_relative_url(file_path)
        response = File.open_binary(self._context, target_path)
        return response.content

    def extract_folder(
        self,
        folder_path: str | None = None,
        file_pattern: str = "*.csv",
        output_dir: Path | None = None,
        allowed_filenames: List[str] | None = None,
    ) -> Dict[str, Any]:
        """Download all matching files from a SharePoint folder.

        When ``output_dir`` is provided, raw file bytes are written unchanged to disk and
        the return value maps file stems to saved paths. Otherwise, files are returned as
        in-memory Polars DataFrames.
        """
        files = self.list_files(folder_path)
        extracted: Dict[str, Any] = {}
        allowed = set(allowed_filenames or [])

        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)

        for file_info in files:
            filename = file_info["name"]
            if not fnmatch.fnmatch(filename, file_pattern):
                continue
            if allowed and filename not in allowed:
                continue
            key = Path(filename).stem
            file_path = file_info["server_relative_url"]

            if output_dir is None:
                extracted[key] = self.extract_file(file_path)
                continue

            destination = output_dir / filename
            if destination.exists():
                logger.info(
                    f"Raw file already exists at {destination}; skipping overwrite"
                )
                extracted[key] = destination
                continue

            destination.write_bytes(self._download_file_bytes(file_path))
            logger.info(f"Saved raw SharePoint file to {destination}")
            extracted[key] = destination

        return extracted

    def test_connection(self) -> bool:
        """Return True when the workforce folder can be listed."""
        try:
            files = self.list_files()
            logger.info(f"SharePoint connection test succeeded with {len(files)} files")
            return True
        except Exception as exc:  # pragma: no cover - network/auth dependent
            logger.error(f"SharePoint connection test failed: {exc}")
            return False
