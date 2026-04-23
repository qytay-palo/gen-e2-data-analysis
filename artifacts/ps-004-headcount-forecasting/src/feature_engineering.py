from __future__ import annotations

from pathlib import Path

import polars as pl
from loguru import logger


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = (
    ROOT
    / "artifacts/ps-004-headcount-forecasting/data/3_interim/features.parquet"
)
REQUIRED_COLUMNS = {"year", "sector", "count", "profession"}


def build_feature_table(df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate annual profession totals and create linear baseline features."""
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input data is missing required columns: {missing}")

    feature_df = (
        df.select(["profession", "year", "count"])
        .with_columns(
            [
                pl.col("profession").cast(pl.Utf8),
                pl.col("year").cast(pl.Int32),
                pl.col("count").cast(pl.Int32),
            ]
        )
        .group_by(["profession", "year"])
        .agg(pl.col("count").sum().cast(pl.Int32).alias("count"))
        .sort(["profession", "year"])
        .with_columns(
            [
                (pl.col("year").cum_count().over("profession") - 1)
                .cast(pl.Int32)
                .alias("year_index"),
                pl.col("count").shift(1).over("profession").cast(pl.Int32).alias("lag_1"),
                pl.col("count").shift(2).over("profession").cast(pl.Int32).alias("lag_2"),
            ]
        )
        .select(["profession", "year", "count", "year_index", "lag_1", "lag_2"])
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    feature_df.write_parquet(OUTPUT_PATH)
    logger.info("Wrote feature table to {path}", path=OUTPUT_PATH)
    return feature_df


if __name__ == "__main__":
    input_path = ROOT / "shared/data/4_processed/workforce_clean.parquet"
    build_feature_table(pl.read_parquet(input_path))