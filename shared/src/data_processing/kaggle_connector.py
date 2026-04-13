"""
Kaggle data connector for shared infrastructure.
Downloads datasets to shared/data/1_raw/ — immutable after download.

Usage:
    from shared.src.data_processing.kaggle_connector import KaggleConnector
    connector = KaggleConnector()
    connector.download_dataset("dataset/slug", "shared/data/1_raw/")
"""

from __future__ import annotations

import os
import time
import zipfile
from pathlib import Path

from loguru import logger


class KaggleConnector:
    """Handles authenticated Kaggle dataset downloads with retry logic."""

    MAX_RETRIES = 3
    RETRY_DELAY_SEC = 5

    def __init__(self) -> None:
        self._api = self._authenticate()

    def _authenticate(self):
        """Authenticate using KAGGLE_USERNAME / KAGGLE_KEY env vars or ~/.kaggle/kaggle.json."""
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi  # type: ignore

            api = KaggleApi()
            api.authenticate()
            logger.info("Kaggle authentication successful.")
            return api
        except Exception as exc:
            logger.error(f"Kaggle authentication failed: {exc}")
            raise

    def download_dataset(
        self,
        dataset_slug: str,
        destination: str | Path,
        unzip: bool = True,
    ) -> Path:
        """
        Download a Kaggle dataset with retry logic.

        Args:
            dataset_slug: Kaggle dataset identifier, e.g. 'owner/dataset-name'.
            destination: Local directory to save raw files (must be inside 1_raw/).
            unzip: Whether to extract zip archives after download.

        Returns:
            Path to the destination directory containing downloaded files.
        """
        dest = Path(destination)
        dest.mkdir(parents=True, exist_ok=True)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.info(
                    f"Downloading '{dataset_slug}' → {dest}  (attempt {attempt}/{self.MAX_RETRIES})"
                )
                self._api.dataset_download_files(
                    dataset_slug, path=str(dest), unzip=unzip, quiet=False
                )
                self._log_download_summary(dest)
                return dest
            except Exception as exc:
                logger.warning(f"Download attempt {attempt} failed: {exc}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_DELAY_SEC * attempt)
                else:
                    logger.error(f"All {self.MAX_RETRIES} download attempts failed.")
                    raise

    def _log_download_summary(self, dest: Path) -> None:
        """Log file sizes and counts after download."""
        files = list(dest.iterdir())
        total_bytes = sum(f.stat().st_size for f in files if f.is_file())
        logger.info(
            f"Download complete: {len(files)} file(s), "
            f"{total_bytes / 1_048_576:.2f} MB total in {dest}"
        )

    def test_connection(self) -> bool:
        """Validate Kaggle credentials are working."""
        try:
            self._api.datasets_list(search="test", max_size=1)
            logger.info("Kaggle connection test passed.")
            return True
        except Exception as exc:
            logger.error(f"Kaggle connection test failed: {exc}")
            return False
