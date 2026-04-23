from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import polars as pl


MODULE_PATH = (
    Path(__file__).resolve().parents[2] / "src" / "growth_analysis.py"
)
SPEC = importlib.util.spec_from_file_location("growth_analysis", MODULE_PATH)
growth_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(growth_analysis)


def test_compute_growth_rates_returns_yoy_and_cagr_for_both_grains() -> None:
    source_df = pl.DataFrame(
        {
            "year": [2020, 2021, 2022, 2020, 2021, 2022, 2020],
            "sector": [
                "Public",
                "Public",
                "Public",
                "Private",
                "Private",
                "Private",
                "Public",
            ],
            "count": [100, 110, 121, 50, 75, 100, 80],
            "profession": [
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "doctors",
                "nurses",
            ],
        }
    )

    result = growth_analysis.compute_growth_rates(source_df)

    public_doctors = result.filter(
        (pl.col("profession") == "doctors")
        & (pl.col("sector") == "Public")
        & (pl.col("year") == 2021)
    )
    assert math.isclose(public_doctors.item(0, "yoy_pct"), 10.0)
    assert math.isclose(public_doctors.item(0, "cagr"), 0.1)

    aggregate_doctors = result.filter(
        (pl.col("profession") == "doctors")
        & (pl.col("sector") == "All")
        & (pl.col("year") == 2022)
    )
    assert math.isclose(aggregate_doctors.item(0, "yoy_pct"), 19.45945945945946)

    nurses = result.filter(
        (pl.col("profession") == "nurses")
        & (pl.col("sector") == "All")
        & (pl.col("year") == 2020)
    )
    assert nurses.item(0, "yoy_pct") is None
    assert nurses.item(0, "cagr") is None


def test_compute_growth_rates_handles_zero_previous_count_without_error() -> None:
    source_df = pl.DataFrame(
        {
            "year": [2020, 2021],
            "sector": ["Public", "Public"],
            "count": [0, 10],
            "profession": ["pharmacists", "pharmacists"],
        }
    )

    result = growth_analysis.compute_growth_rates(source_df)
    growth_row = result.filter(
        (pl.col("profession") == "pharmacists")
        & (pl.col("sector") == "Public")
        & (pl.col("year") == 2021)
    )

    assert growth_row.item(0, "yoy_pct") is None
    assert growth_row.item(0, "cagr") is None