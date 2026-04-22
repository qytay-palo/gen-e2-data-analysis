"""Validation helpers for raw workforce CSV files."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import polars as pl
from loguru import logger


REQUIRED_COLUMNS = ("year", "sector", "count")
COLUMN_ALIASES = {
    "year": ("year",),
    "sector": ("sector",),
    "count": ("count", "headcount", "head_count", "head count"),
}


def _normalize_column_name(column_name: str) -> str:
    cleaned_name = re.sub(r"[^0-9a-zA-Z]+", "_", column_name.strip())
    return re.sub(r"_+", "_", cleaned_name).strip("_").lower()


def _match_required_columns(columns: list[str]) -> dict[str, str]:
    normalized_lookup = {
        _normalize_column_name(column_name): column_name for column_name in columns
    }
    matched_columns: dict[str, str] = {}

    for canonical_name, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized_lookup:
                matched_columns[canonical_name] = normalized_lookup[alias]
                break

    return matched_columns


def _coerce_required_columns(
    dataframe: pl.DataFrame,
    matched_columns: dict[str, str],
) -> pl.DataFrame:
    return dataframe.with_columns(
        [
            pl.col(matched_columns["year"]).cast(pl.Int64, strict=False).alias("year"),
            pl.col(matched_columns["sector"]).cast(pl.Utf8, strict=False).alias("sector"),
            pl.col(matched_columns["count"]).cast(pl.Int64, strict=False).alias("count"),
        ]
    )


def validate_workforce_file(file_path: str | Path) -> dict[str, Any]:
    """Validate a single raw workforce CSV and return a structured quality profile."""
    csv_path = Path(file_path)
    logger.info(f"Validating workforce file: {csv_path}")

    dataframe = pl.read_csv(csv_path, infer_schema_length=0)
    matched_columns = _match_required_columns(dataframe.columns)
    missing_columns = [
        column_name for column_name in REQUIRED_COLUMNS if column_name not in matched_columns
    ]

    file_findings: dict[str, Any] = {
        "file_name": csv_path.name,
        "file_path": str(csv_path),
        "row_count": dataframe.height,
        "column_count": dataframe.width,
        "source_columns": dataframe.columns,
        "matched_columns": matched_columns,
        "missing_required_columns": missing_columns,
        "schema_validation": "pass" if not missing_columns else "fail",
    }

    if missing_columns:
        logger.error(
            "Missing required columns for {}: {}",
            csv_path.name,
            ", ".join(missing_columns),
        )
        return file_findings

    profiled_dataframe = _coerce_required_columns(dataframe, matched_columns)

    null_counts = profiled_dataframe.select(
        [pl.col(column_name).null_count().alias(column_name) for column_name in REQUIRED_COLUMNS]
    ).to_dicts()[0]
    null_rates = {
        column_name: (
            null_counts[column_name] / profiled_dataframe.height if profiled_dataframe.height else 0.0
        )
        for column_name in REQUIRED_COLUMNS
    }

    duplicate_row_count = profiled_dataframe.height - profiled_dataframe.unique().height
    negative_count_rows = profiled_dataframe.filter(pl.col("count") < 0).height

    year_values = (
        profiled_dataframe
        .select(pl.col("year").drop_nulls().unique().sort())
        .to_series()
        .to_list()
    )
    sector_values = (
        profiled_dataframe
        .select(pl.col("sector").drop_nulls().unique().sort())
        .to_series()
        .to_list()
    )

    file_findings.update(
        {
            "schema_validation": "pass",
            "null_counts": null_counts,
            "null_rates": null_rates,
            "duplicate_row_count": duplicate_row_count,
            "negative_count_rows": negative_count_rows,
            "unique_year_values": year_values,
            "unique_sector_values": sector_values,
            "year_range": {
                "min": min(year_values) if year_values else None,
                "max": max(year_values) if year_values else None,
            },
        }
    )

    logger.info(
        "{} schema={} duplicates={} negative_count_rows={} year_range={}..{}",
        csv_path.name,
        file_findings["schema_validation"],
        duplicate_row_count,
        negative_count_rows,
        file_findings["year_range"]["min"],
        file_findings["year_range"]["max"],
    )

    return file_findings


def validate_workforce_files(file_paths: list[str | Path]) -> dict[str, dict[str, Any]]:
    """Validate multiple raw workforce CSV files and return findings keyed by file stem."""
    results: dict[str, dict[str, Any]] = {}

    for file_path in file_paths:
        csv_path = Path(file_path)
        results[csv_path.stem] = validate_workforce_file(csv_path)

    return results