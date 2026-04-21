"""Utilities for PS-001 workforce trend packaging."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

import polars as pl


def normalize_column_name(name: str) -> str:
    """Convert source column names to lowercase snake case."""
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip()).strip("_")
    return normalized.lower()


def standardize_workforce_frame(
    dataframe: pl.DataFrame,
    profession: str,
) -> pl.DataFrame:
    """Standardize a single profession dataframe for downstream combination."""
    renamed = dataframe.rename(
        {column: normalize_column_name(column) for column in dataframe.columns}
    )
    if "profession" not in renamed.columns:
        renamed = renamed.with_columns(pl.lit(profession).alias("profession"))
    return renamed


def combine_workforce_frames(frames: Dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Combine profession-level dataframes using a diagonal concat."""
    standardized_frames = [
        standardize_workforce_frame(dataframe, profession)
        for profession, dataframe in frames.items()
    ]
    if not standardized_frames:
        return pl.DataFrame()
    return pl.concat(standardized_frames, how="diagonal")


def build_schema_snapshot(dataframe: pl.DataFrame) -> pl.DataFrame:
    """Create a lightweight schema summary for documentation and QA."""
    null_counts = [
        dataframe[column].null_count() for column in dataframe.columns
    ]
    return pl.DataFrame(
        {
            "column_name": dataframe.columns,
            "dtype": [str(dtype) for dtype in dataframe.dtypes],
            "null_count": null_counts,
        }
    )


def write_outputs(
    combined_dataframe: pl.DataFrame,
    output_root: Path,
) -> None:
    """Write interim and processed outputs for PS-001."""
    interim_path = (
        output_root / "data" / "3_interim" / "combined_workforce_interim.parquet"
    )
    processed_path = (
        output_root / "data" / "4_processed" / "combined_workforce_processed.parquet"
    )
    schema_path = output_root / "results" / "tables" / "combined_workforce_schema.csv"
    metrics_path = (
        output_root
        / "results"
        / "metrics"
        / "combined_workforce_record_count.csv"
    )

    interim_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    combined_dataframe.write_parquet(interim_path)
    combined_dataframe.write_parquet(processed_path)
    build_schema_snapshot(combined_dataframe).write_csv(schema_path)
    pl.DataFrame(
        {
            "metric": ["row_count", "column_count"],
            "value": [combined_dataframe.height, combined_dataframe.width],
        }
    ).write_csv(metrics_path)
