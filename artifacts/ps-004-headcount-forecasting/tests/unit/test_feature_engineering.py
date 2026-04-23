from __future__ import annotations

import importlib.util
from pathlib import Path

import polars as pl


MODULE_PATH = (
    Path(__file__).resolve().parents[2] / "src" / "feature_engineering.py"
)
SPEC = importlib.util.spec_from_file_location("feature_engineering", MODULE_PATH)
feature_engineering = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(feature_engineering)


def _build_source_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "year": [2020, 2020, 2021, 2021, 2022, 2022, 2021, 2022],
            "sector": [
                "Public",
                "Private",
                "Public",
                "Private",
                "Public",
                "Private",
                "Public",
                "Public",
            ],
            "count": [10, 5, 20, 10, 25, 5, 7, 8],
            "profession": [
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "nurses",
                "nurses",
            ],
        }
    )


def test_year_index_starts_at_zero_and_increments_per_profession(tmp_path: Path) -> None:
    feature_engineering.OUTPUT_PATH = tmp_path / "features.parquet"

    result = feature_engineering.build_feature_table(_build_source_df())

    doctors_indices = (
        result.filter(pl.col("profession") == "doctors")
        .sort("year")
        .get_column("year_index")
        .to_list()
    )
    nurses_indices = (
        result.filter(pl.col("profession") == "nurses")
        .sort("year")
        .get_column("year_index")
        .to_list()
    )

    assert doctors_indices == [0, 1, 2]
    assert nurses_indices == [0, 1]


def test_lag_1_matches_previous_year_count(tmp_path: Path) -> None:
    feature_engineering.OUTPUT_PATH = tmp_path / "features.parquet"

    result = feature_engineering.build_feature_table(_build_source_df())
    doctors_2021 = result.filter(
        (pl.col("profession") == "doctors") & (pl.col("year") == 2021)
    )
    doctors_2022 = result.filter(
        (pl.col("profession") == "doctors") & (pl.col("year") == 2022)
    )

    assert doctors_2021.item(0, "lag_1") == 15
    assert doctors_2022.item(0, "lag_1") == 30


def test_lag_2_matches_two_years_prior_count(tmp_path: Path) -> None:
    feature_engineering.OUTPUT_PATH = tmp_path / "features.parquet"

    result = feature_engineering.build_feature_table(_build_source_df())
    doctors_2022 = result.filter(
        (pl.col("profession") == "doctors") & (pl.col("year") == 2022)
    )

    assert doctors_2022.item(0, "lag_2") == 15