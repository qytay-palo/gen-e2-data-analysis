"""Feature engineering helpers for PS-004 headcount forecasting."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import polars as pl


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
RAW_INPUT_PATH: Final[Path] = (
    PROJECT_ROOT / "shared" / "data" / "4_processed" / "workforce_clean.parquet"
)
OUTPUT_PATH: Final[Path] = (
    PROJECT_ROOT
    / "artifacts"
    / "ps-004-headcount-forecasting"
    / "data"
    / "3_interim"
    / "features.parquet"
)
RAW_REQUIRED_COLUMNS: Final[set[str]] = {"year", "sector", "count", "profession"}
FEATURE_REQUIRED_COLUMNS: Final[set[str]] = {"profession", "year", "count"}


def load_workforce_data(input_path: Path = RAW_INPUT_PATH) -> pl.DataFrame:
    """Load the canonical cleaned workforce dataset."""
    return pl.read_parquet(input_path)


def aggregate_profession_totals(raw_df: pl.DataFrame) -> pl.DataFrame:
    """Prepare one annual count per profession for feature engineering.

    The requested contract expects `sector == "All"` rows to already represent the
    annual total. The current parquet in this workspace does not include those rows,
    so the function falls back to summing the available sectors to keep PS-004 runnable.
    """
    missing_columns = RAW_REQUIRED_COLUMNS.difference(raw_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    base_df = raw_df.select(["profession", "year", "count", "sector"]).with_columns(
        [
            pl.col("profession").cast(pl.String),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
            pl.col("sector").cast(pl.String),
        ]
    )

    totals_df = base_df.filter(pl.col("sector") == "All").select(
        ["profession", "year", "count"]
    )
    if totals_df.is_empty():
        print(
            "No sector='All' rows found in workforce_clean.parquet; "
            "falling back to profession-year sums across sectors."
        )
        totals_df = (
            base_df.group_by(["profession", "year"])
            .agg(pl.col("count").sum().alias("count"))
            .select(["profession", "year", "count"])
        )

    return totals_df.with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    ).sort(["profession", "year"])


def build_features(df: pl.DataFrame) -> pl.DataFrame:
    """Build linear-baseline features for annual profession headcount series."""
    missing_columns = FEATURE_REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    features = (
        df.select(["profession", "year", "count"])
        .with_columns(
            [
                pl.col("profession").cast(pl.String),
                pl.col("year").cast(pl.Int32),
                pl.col("count").cast(pl.Int32),
            ]
        )
        .sort(["profession", "year"])
        .with_columns(
            [
                (pl.col("year").rank("ordinal").over("profession") - 1)
                .cast(pl.Int32)
                .alias("year_index"),
                pl.col("count").shift(1).over("profession").cast(pl.Int32).alias("lag_1"),
                pl.col("count").shift(2).over("profession").cast(pl.Int32).alias("lag_2"),
            ]
        )
        .with_columns(pl.col("profession").cast(pl.Categorical))
        .select(["profession", "year", "count", "year_index", "lag_1", "lag_2"])
        .sort(["profession", "year"])
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    features.write_parquet(OUTPUT_PATH)
    return features
