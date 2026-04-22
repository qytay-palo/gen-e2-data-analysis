"""Run schema validation and quality profiling for raw workforce CSV files."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import yaml
from loguru import logger


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.src.data_processing.workforce_validation import validate_workforce_files


def configure_logger(log_dir: Path) -> Path:
    """Configure loguru to write validation logs for this run."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_path, level="INFO", enqueue=False)
    return log_path


def build_report(results: dict[str, dict[str, object]], log_path: Path) -> dict[str, object]:
    """Build the YAML report payload for all validated workforce files."""
    return {
        "agent": "data-validation",
        "ps": "ps-001-workforce-data-foundation",
        "timestamp": datetime.now().date().isoformat(),
        "log_path": str(log_path.relative_to(ROOT_DIR)),
        "files": results,
    }


def main() -> int:
    """Validate the four workforce CSV files and persist a YAML quality report."""
    raw_dir = ROOT_DIR / "shared" / "data" / "1_raw" / "workforce"
    file_paths = [
        raw_dir / "doctors.csv",
        raw_dir / "nurses.csv",
        raw_dir / "pharmacists.csv",
        raw_dir / "physiotherapists.csv",
    ]
    output_path = (
        ROOT_DIR
        / "artifacts"
        / "ps-001-workforce-data-foundation"
        / "results"
        / "tables"
        / "data_quality_report.yml"
    )
    log_dir = (
        ROOT_DIR
        / "artifacts"
        / "ps-001-workforce-data-foundation"
        / "logs"
        / "etl"
    )

    log_path = configure_logger(log_dir)
    logger.info("Starting workforce validation run for {} files", len(file_paths))

    results = validate_workforce_files(file_paths)
    report = build_report(results, log_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file_handle:
        yaml.safe_dump(report, file_handle, sort_keys=False, allow_unicode=False)

    logger.info("Wrote workforce quality report to {}", output_path)

    has_missing_required_columns = any(
        file_result["missing_required_columns"] for file_result in results.values()
    )
    if has_missing_required_columns:
        logger.error("Schema validation failed because one or more required columns are missing")
        return 1

    logger.info("Schema validation passed for all workforce files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())