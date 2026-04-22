"""Download workforce CSV files from SharePoint into the raw landing zone."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
from dotenv import load_dotenv
from loguru import logger

REQUIRED_FILES = [
    "doctors.csv",
    "nurses.csv",
    "pharmacists.csv",
    "physiotherapists.csv",
]

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
PS001_ARTIFACT_DIR = Path("artifacts") / "ps-001-workforce-data-foundation"
DEFAULT_RAW_OUTPUT_DIR = Path("shared") / "data" / "1_raw" / "workforce"
DEFAULT_LOG_DIR = PS001_ARTIFACT_DIR / "logs" / "etl"


def resolve_project_root() -> Path:
    """Return the configured project root for PS-001 execution."""
    configured_root = os.getenv("GEN_E2_PROJECT_ROOT")
    if configured_root:
        return Path(configured_root).expanduser().resolve()
    return DEFAULT_PROJECT_ROOT


PROJECT_ROOT = resolve_project_root()

sys.path.insert(0, str(PROJECT_ROOT))

from shared.src.data_processing.sharepoint_connector import (  # noqa: E402
    SharePointConnector,
    SharePointSettings,
)


def resolve_runtime_path(env_var_name: str, default_relative_path: Path) -> Path:
    """Resolve a runtime path from an environment variable or project-relative default."""
    configured_path = os.getenv(env_var_name)
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return PROJECT_ROOT / default_relative_path


def get_raw_output_dir() -> Path:
    """Return the configured raw workforce landing directory."""
    return resolve_runtime_path("PS001_WORKFORCE_RAW_DIR", DEFAULT_RAW_OUTPUT_DIR)


def get_log_dir() -> Path:
    """Return the configured PS-001 extraction log directory."""
    return resolve_runtime_path("PS001_LOG_DIR", DEFAULT_LOG_DIR)


def configure_logging() -> Path:
    """Configure loguru sinks for the extraction run."""
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = (
        log_dir
        / f"extract_workforce_data_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}.log"
    )

    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_path, level="INFO", enqueue=True)

    return log_path


def count_rows(csv_path: Path) -> int:
    """Return the row count for a downloaded CSV using Polars."""
    return pl.scan_csv(csv_path).select(pl.len().alias("row_count")).collect().item()


def extract_workforce_files() -> dict[str, dict[str, str | int]]:
    """Download all required workforce files and return file metadata."""
    load_dotenv(PROJECT_ROOT / ".env")
    settings = SharePointSettings.from_env()
    settings.validate()

    raw_output_dir = get_raw_output_dir()
    raw_output_dir.mkdir(parents=True, exist_ok=True)
    connector = SharePointConnector(settings=settings)

    downloaded = connector.extract_folder(
        folder_path=settings.workforce_folder,
        file_pattern="*.csv",
        output_dir=raw_output_dir,
        allowed_filenames=REQUIRED_FILES,
    )

    expected_keys = {Path(filename).stem for filename in REQUIRED_FILES}
    missing = sorted(expected_keys.difference(downloaded.keys()))
    if missing:
        raise RuntimeError(f"Missing required SharePoint files: {', '.join(missing)}")

    metadata: dict[str, dict[str, str | int]] = {}
    for filename in REQUIRED_FILES:
        file_path = raw_output_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Downloaded file not found: {file_path}")

        row_count = count_rows(file_path)
        if row_count <= 0:
            raise ValueError(f"Downloaded file is empty: {file_path}")

        downloaded_at = datetime.fromtimestamp(
            file_path.stat().st_mtime,
            tz=timezone.utc,
        ).isoformat()
        logger.info(f"Downloaded {filename} at {downloaded_at} with {row_count} rows")
        metadata[filename] = {
            "path": str(file_path),
            "row_count": row_count,
            "downloaded_at": downloaded_at,
        }

    return metadata


def main() -> int:
    """Run the workforce extraction and return a process exit code."""
    log_path = configure_logging()
    logger.info("Starting PS-001 SharePoint workforce extraction")

    try:
        extract_workforce_files()
    except Exception:
        logger.exception("Workforce extraction failed")
        logger.error(f"Extraction log written to {log_path}")
        return 1

    logger.info("Workforce extraction completed successfully")
    logger.info(f"Extraction log written to {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
