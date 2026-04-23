"""Growth analysis helpers for workforce trend calculations."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import polars as pl
from loguru import logger


REQUIRED_COLUMNS: Final[set[str]] = {"profession", "sector", "year", "count"}
GROUP_COLUMNS: Final[list[str]] = ["profession", "sector"]
OUTPUT_SCHEMA: Final[dict[str, pl.DataType]] = {
    "profession": pl.Categorical,
    "sector": pl.Categorical,
    "year": pl.Int32,
    "yoy_pct": pl.Float64,
    "cagr": pl.Float64,
}


def _empty_growth_frame() -> pl.DataFrame:
    return pl.DataFrame(schema=OUTPUT_SCHEMA)


def _validate_input(df: pl.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")


def _aggregate_input(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.select(["profession", "sector", "year", "count"])
        .with_columns(
            [
                pl.col("profession").cast(pl.String),
                pl.col("sector").cast(pl.String),
                pl.col("year").cast(pl.Int32),
                pl.col("count").cast(pl.Int64),
            ]
        )
        .group_by(["profession", "sector", "year"])
        .agg(pl.col("count").sum().alias("count"))
        .sort(["profession", "sector", "year"])
    )


def _build_profession_totals(aggregated_df: pl.DataFrame) -> pl.DataFrame:
    return (
        aggregated_df.group_by(["profession", "year"])
        .agg(pl.col("count").sum().alias("count"))
        .with_columns(pl.lit("All").alias("sector"))
        .select(["profession", "sector", "year", "count"])
        .sort(["profession", "sector", "year"])
    )


def _compute_cagr_values(sorted_df: pl.DataFrame) -> pl.DataFrame:
    summaries = (
        sorted_df.group_by(GROUP_COLUMNS)
        .agg(
            [
                pl.len().alias("points"),
                pl.col("year").first().alias("first_year"),
                pl.col("year").last().alias("last_year"),
                pl.col("count").first().alias("first_count"),
                pl.col("count").last().alias("last_count"),
            ]
        )
        .with_columns((pl.col("last_year") - pl.col("first_year")).alias("year_span"))
    )

    insufficient_groups = summaries.filter(pl.col("points") < 2)
    for row in insufficient_groups.iter_rows(named=True):
        logger.warning(
            "Skipping CAGR for profession={} sector={} because only {} data point is available",
            row["profession"],
            row["sector"],
            row["points"],
        )

    zero_initial_groups = summaries.filter((pl.col("points") >= 2) & (pl.col("first_count") <= 0))
    for row in zero_initial_groups.iter_rows(named=True):
        logger.warning(
            "Skipping CAGR for profession={} sector={} because initial count is {}",
            row["profession"],
            row["sector"],
            row["first_count"],
        )

    return summaries.select(
        [
            "profession",
            "sector",
            pl.when(
                (pl.col("points") < 2)
                | (pl.col("year_span") <= 0)
                | (pl.col("first_count") <= 0)
            )
            .then(pl.lit(None, dtype=pl.Float64))
            .otherwise(
                (pl.col("last_count").cast(pl.Float64) / pl.col("first_count").cast(pl.Float64))
                .pow(1.0 / pl.col("year_span").cast(pl.Float64))
                - 1.0
            )
            .alias("cagr"),
        ]
    )


def _compute_growth_slice(base_df: pl.DataFrame) -> pl.DataFrame:
    if base_df.is_empty():
        return _empty_growth_frame()

    sorted_df = base_df.sort(["profession", "sector", "year"])
    cagr_df = _compute_cagr_values(sorted_df)

    return (
        sorted_df.with_columns(pl.col("count").shift(1).over(GROUP_COLUMNS).alias("previous_count"))
        .with_columns(
            pl.when(pl.col("previous_count").is_null() | (pl.col("previous_count") == 0))
            .then(pl.lit(None, dtype=pl.Float64))
            .otherwise(
                ((pl.col("count") - pl.col("previous_count")) / pl.col("previous_count"))
                * 100.0
            )
            .alias("yoy_pct")
        )
        .drop("previous_count")
        .join(cagr_df, on=GROUP_COLUMNS, how="left")
        .select(["profession", "sector", "year", "yoy_pct", "cagr"])
        .with_columns(
            [
                pl.col("profession").cast(pl.Categorical),
                pl.col("sector").cast(pl.Categorical),
                pl.col("year").cast(pl.Int32),
                pl.col("yoy_pct").cast(pl.Float64),
                pl.col("cagr").cast(pl.Float64),
            ]
        )
        .sort(["profession", "sector", "year"])
    )


def compute_growth_rates(df: pl.DataFrame) -> pl.DataFrame:
    """Compute YoY growth and CAGR by profession and profession-sector."""
    _validate_input(df)

    aggregated_df = _aggregate_input(df)
    if aggregated_df.is_empty():
        return _empty_growth_frame()

    profession_totals = _build_profession_totals(aggregated_df)
    combined_df = pl.concat([profession_totals, aggregated_df], how="vertical")
    return _compute_growth_slice(combined_df)


def default_input_path(project_root: Path) -> Path:
    return project_root / "shared" / "data" / "4_processed" / "workforce_clean.parquet"


def default_output_path(project_root: Path) -> Path:
    return (
        project_root
        / "artifacts"
        / "ps-003-workforce-growth-analysis"
        / "results"
        / "tables"
        / "growth_rates.parquet"
    )