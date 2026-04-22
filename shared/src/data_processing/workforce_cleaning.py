"""Cleaning helpers for raw workforce CSV files."""

from __future__ import annotations

import re
from typing import Any

import polars as pl
from loguru import logger


HEADCOUNT_ALIASES = {
    "count",
    "headcount",
    "head_count",
    "head count",
}


def _normalize_column_name(column_name: str) -> str:
    cleaned_name = re.sub(r"[^0-9a-zA-Z]+", "_", column_name.strip())
    return re.sub(r"_+", "_", cleaned_name).strip("_").lower()


def _canonicalize_columns(dataframe: pl.DataFrame) -> pl.DataFrame:
    rename_map: dict[str, str] = {}

    for column_name in dataframe.columns:
        normalized_name = _normalize_column_name(column_name)
        if normalized_name in HEADCOUNT_ALIASES:
            rename_map[column_name] = "count"
        else:
            rename_map[column_name] = normalized_name

    return dataframe.rename(rename_map)


def _title_case_sector(value: str | None) -> str | None:
    if value is None:
        return None

    return value.strip().title()


def clean_workforce_frame(df: pl.DataFrame, profession: str) -> tuple[pl.DataFrame, dict[str, Any]]:
    """Clean one workforce frame and return the cleaned result plus audit counts."""
    rows_in = df.height
    cleaned_df = _canonicalize_columns(df)

    if "year" not in cleaned_df.columns:
        raise ValueError("Missing required column after normalization: year")
    if "count" not in cleaned_df.columns:
        raise ValueError("Missing required column after normalization: count")
    if "sector" not in cleaned_df.columns:
        raise ValueError("Missing required column after normalization: sector")

    cleaned_df = cleaned_df.with_columns(
        [
            pl.col("year").cast(pl.Int32, strict=False),
            pl.col("count").cast(pl.Int32, strict=False),
            pl.col("sector").cast(pl.Utf8, strict=False),
        ]
    )

    nulls_dropped = cleaned_df.filter(
        pl.col("year").is_null() | pl.col("count").is_null()
    ).height
    if nulls_dropped:
        logger.info("Dropping {} rows with null year/count for {}", nulls_dropped, profession)

    cleaned_df = cleaned_df.filter(pl.col("year").is_not_null() & pl.col("count").is_not_null())

    cleaned_df = cleaned_df.with_columns(
        [
            pl.col("sector").fill_null("Unknown").map_elements(_title_case_sector, return_dtype=pl.String),
            pl.lit(profession).alias("profession"),
        ]
    )

    dupes_dropped = cleaned_df.height - cleaned_df.unique(maintain_order=True).height
    if dupes_dropped:
        logger.info("Dropping {} duplicate rows for {}", dupes_dropped, profession)

    cleaned_df = (
        cleaned_df.unique(keep="first", maintain_order=True)
        .with_columns(
            [
                pl.col("sector").cast(pl.Categorical),
                pl.col("profession").cast(pl.Categorical),
            ]
        )
    )

    audit = {
        "profession": profession,
        "rows_in": rows_in,
        "rows_out": cleaned_df.height,
        "nulls_dropped": nulls_dropped,
        "dupes_dropped": dupes_dropped,
    }

    return cleaned_df, audit


def combine_cleaned_frames(frames: dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Concatenate cleaned profession frames into one canonical dataset."""
    if not frames:
        return pl.DataFrame(schema={"year": pl.Int32, "sector": pl.Categorical, "count": pl.Int32, "profession": pl.Categorical})

    return pl.concat(list(frames.values()), how="vertical")