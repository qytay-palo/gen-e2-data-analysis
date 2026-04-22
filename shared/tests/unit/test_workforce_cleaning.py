from __future__ import annotations

import sys
from pathlib import Path

import polars as pl
import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.src.data_processing.workforce_cleaning import clean_workforce_frame


def test_clean_workforce_frame_normalizes_headcount_and_profession() -> None:
    dataframe = pl.DataFrame(
        {
            "Year": [2020],
            " Sector ": ["public"],
            "Head Count": [42],
        }
    )

    result, audit = clean_workforce_frame(dataframe, "doctors")

    assert result.columns == ["year", "sector", "count", "profession"]
    assert result["count"].to_list() == [42]
    assert result["profession"].to_list() == ["doctors"]
    assert audit == {
        "profession": "doctors",
        "rows_in": 1,
        "rows_out": 1,
        "nulls_dropped": 0,
        "dupes_dropped": 0,
    }


def test_clean_workforce_frame_drops_null_year_or_count_rows() -> None:
    dataframe = pl.DataFrame(
        {
            "year": [2020, None, 2022],
            "sector": ["public", "private", "public"],
            "headcount": [100, 200, None],
        },
        strict=False,
    )

    result, audit = clean_workforce_frame(dataframe, "nurses")

    assert result.height == 1
    assert result["year"].to_list() == [2020]
    assert result["count"].to_list() == [100]
    assert audit["nulls_dropped"] == 2


def test_clean_workforce_frame_removes_exact_duplicates() -> None:
    dataframe = pl.DataFrame(
        {
            "year": [2020, 2020],
            "sector": ["public", "public"],
            "headcount": [100, 100],
        }
    )

    result, audit = clean_workforce_frame(dataframe, "pharmacists")

    assert result.height == 1
    assert audit["dupes_dropped"] == 1


def test_clean_workforce_frame_standardizes_sector_values() -> None:
    dataframe = pl.DataFrame(
        {
            "year": [2020, 2021],
            "sector": [" public ", None],
            "headcount": [100, 120],
        },
        strict=False,
    )

    result, _ = clean_workforce_frame(dataframe, "physiotherapists")

    assert result["sector"].cast(pl.String).to_list() == ["Public", "Unknown"]


def test_clean_workforce_frame_enforces_expected_dtypes() -> None:
    dataframe = pl.DataFrame(
        {
            "year": ["2020"],
            "sector": ["private"],
            "headcount": ["15"],
        }
    )

    result, _ = clean_workforce_frame(dataframe, "doctors")

    assert result.schema["year"] == pl.Int32
    assert result.schema["count"] == pl.Int32
    assert result.schema["sector"] == pl.Categorical
    assert result.schema["profession"] == pl.Categorical


def test_clean_workforce_frame_handles_empty_input_with_expected_schema() -> None:
    dataframe = pl.DataFrame(
        schema={
            "year": pl.Int64,
            "sector": pl.String,
            "headcount": pl.Int64,
        }
    )

    result, audit = clean_workforce_frame(dataframe, "doctors")

    assert result.is_empty()
    assert result.schema["year"] == pl.Int32
    assert result.schema["count"] == pl.Int32
    assert result.schema["sector"] == pl.Categorical
    assert result.schema["profession"] == pl.Categorical
    assert audit == {
        "profession": "doctors",
        "rows_in": 0,
        "rows_out": 0,
        "nulls_dropped": 0,
        "dupes_dropped": 0,
    }


def test_clean_workforce_frame_raises_for_missing_required_column() -> None:
    dataframe = pl.DataFrame(
        {
            "year": [2020],
            "headcount": [10],
        }
    )

    with pytest.raises(ValueError, match="sector"):
        clean_workforce_frame(dataframe, "doctors")


def test_clean_workforce_frame_replaces_all_null_sector_values() -> None:
    dataframe = pl.DataFrame(
        {
            "year": [2020, 2021],
            "sector": [None, None],
            "headcount": [10, 12],
        },
        strict=False,
    )

    result, _ = clean_workforce_frame(dataframe, "doctors")

    assert result["sector"].cast(pl.String).to_list() == ["Unknown", "Unknown"]