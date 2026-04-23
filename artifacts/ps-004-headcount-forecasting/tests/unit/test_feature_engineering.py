from __future__ import annotations

import sys
from pathlib import Path

import polars as pl


PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODULE_DIR = PROJECT_ROOT / "artifacts" / "ps-004-headcount-forecasting" / "src"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from feature_engineering import aggregate_profession_totals, build_features


def _sample_aggregated_frame() -> pl.DataFrame:
    professions = [
        "doctors",
        "nurses",
        "pharmacists",
        "physiotherapists",
    ]
    years = [2017, 2018, 2019]
    rows: list[dict[str, int | str]] = []

    for profession_index, profession in enumerate(professions):
        for year_offset, year in enumerate(years):
            rows.append(
                {
                    "profession": profession,
                    "year": year,
                    "count": 100 + (profession_index * 10) + year_offset,
                }
            )

    return pl.DataFrame(rows).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )


def test_aggregate_profession_totals_falls_back_when_all_sector_is_absent() -> None:
    raw_df = pl.DataFrame(
        {
            "profession": ["doctors", "doctors", "doctors", "doctors"],
            "year": [2018, 2018, 2019, 2019],
            "sector": ["Public", "Private", "Public", "Private"],
            "count": [10, 15, 12, 18],
        }
    )

    result = aggregate_profession_totals(raw_df)

    assert result.sort("year").to_dicts() == [
        {"profession": "doctors", "year": 2018, "count": 25},
        {"profession": "doctors", "year": 2019, "count": 30},
    ]


def test_year_index_starts_at_zero_and_increments_per_profession() -> None:
    result = build_features(_sample_aggregated_frame())

    for profession in ["doctors", "nurses", "pharmacists", "physiotherapists"]:
        indices = (
            result.filter(pl.col("profession") == profession)
            .sort("year")
            .get_column("year_index")
            .to_list()
        )
        assert indices == [0, 1, 2]


def test_lag_1_is_null_for_first_year_of_each_profession() -> None:
    result = build_features(_sample_aggregated_frame())

    first_year_rows = result.sort(["profession", "year"]).group_by("profession").first()
    assert first_year_rows.sort("profession").get_column("lag_1").to_list() == [
        None,
        None,
        None,
        None,
    ]


def test_lag_2_is_null_for_first_two_years_of_each_profession() -> None:
    result = build_features(_sample_aggregated_frame())

    first_two_rows = (
        result.sort(["profession", "year"])
        .with_columns(
            (pl.col("year").rank("ordinal").over("profession")).alias("row_number")
        )
        .filter(pl.col("row_number") <= 2)
        .sort(["profession", "year"])
    )
    assert first_two_rows.get_column("lag_2").to_list() == [None] * 8


def test_feature_frame_keeps_one_row_per_input_profession_year() -> None:
    aggregated = _sample_aggregated_frame()
    result = build_features(aggregated)

    assert result.height == aggregated.height
