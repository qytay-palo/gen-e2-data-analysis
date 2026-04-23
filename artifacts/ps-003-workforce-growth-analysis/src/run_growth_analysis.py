"""Run workforce growth analysis and export a parquet result."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import polars as pl
from loguru import logger

from growth_analysis import compute_growth_rates, default_input_path, default_output_path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "ps-003-workforce-growth-analysis"
    / "logs"
    / "analysis"
)


def configure_logger() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"growth_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_path, level="INFO", enqueue=False)
    return log_path


def main() -> int:
    log_path = configure_logger()
    input_path = default_input_path(PROJECT_ROOT)
    output_path = default_output_path(PROJECT_ROOT)

    logger.info("Loading workforce parquet from {}", input_path)
    df = pl.read_parquet(input_path)

    growth_df = compute_growth_rates(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    growth_df.write_parquet(output_path, compression="snappy")

    professions = growth_df.select(pl.col("profession").unique().sort()).to_series().to_list()
    year_range = growth_df.select(
        pl.col("year").min().alias("min_year"),
        pl.col("year").max().alias("max_year"),
    ).to_dicts()[0]
    logger.info(
        "Wrote {} growth rows to {} | professions={} | year_range={}..{} | log={}",
        growth_df.height,
        output_path,
        professions,
        year_range["min_year"],
        year_range["max_year"],
        log_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())