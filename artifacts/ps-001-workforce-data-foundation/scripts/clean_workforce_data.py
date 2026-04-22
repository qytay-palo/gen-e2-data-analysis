"""Clean raw workforce CSV files and export a canonical Parquet dataset."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import polars as pl
import yaml
from loguru import logger


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.src.data_processing.workforce_cleaning import (
    clean_workforce_frame,
    combine_cleaned_frames,
)


def configure_logger(log_dir: Path) -> Path:
    """Configure loguru to write cleaning logs for this run."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"cleaning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_path, level="INFO", enqueue=False)
    return log_path


def build_audit(audits: list[dict[str, object]], combined_df: pl.DataFrame, log_path: Path) -> dict[str, object]:
    """Build the YAML audit payload for the cleaning run."""
    return {
        "agent": "data-cleaning",
        "ps": "ps-001-workforce-data-foundation",
        "timestamp": datetime.now().date().isoformat(),
        "log_path": str(log_path.relative_to(ROOT_DIR)),
        "professions": audits,
        "combined": {
            "rows_out": combined_df.height,
            "columns": combined_df.columns,
            "schema": {column_name: str(dtype) for column_name, dtype in combined_df.schema.items()},
        },
    }


def main() -> int:
    """Run workforce cleaning for all raw profession CSVs."""
    raw_dir = ROOT_DIR / "shared" / "data" / "1_raw" / "workforce"
    processed_path = ROOT_DIR / "shared" / "data" / "4_processed" / "workforce_clean.parquet"
    audit_path = (
        ROOT_DIR
        / "artifacts"
        / "ps-001-workforce-data-foundation"
        / "results"
        / "tables"
        / "workforce_cleaning_audit.yml"
    )
    log_dir = (
        ROOT_DIR
        / "artifacts"
        / "ps-001-workforce-data-foundation"
        / "logs"
        / "etl"
    )

    log_path = configure_logger(log_dir)
    frames: dict[str, pl.DataFrame] = {}
    audits: list[dict[str, object]] = []

    for csv_path in sorted(raw_dir.glob("*.csv")):
        profession = csv_path.stem
        logger.info("Cleaning workforce file: {}", csv_path)
        raw_df = pl.read_csv(csv_path)
        cleaned_df, audit = clean_workforce_frame(raw_df, profession)
        frames[profession] = cleaned_df.select(["year", "sector", "count", "profession"])
        audits.append(audit)

    combined_df = combine_cleaned_frames(frames).select(["year", "sector", "count", "profession"])

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    combined_df.write_parquet(processed_path, compression="snappy")
    logger.info("Wrote clean workforce parquet to {}", processed_path)

    audit_payload = build_audit(audits, combined_df, log_path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("w", encoding="utf-8") as file_handle:
        yaml.safe_dump(audit_payload, file_handle, sort_keys=False, allow_unicode=False)

    logger.info("Wrote cleaning audit to {}", audit_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())