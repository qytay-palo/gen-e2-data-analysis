from __future__ import annotations

import math
import sys
from pathlib import Path

import polars as pl


PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODULE_DIR = PROJECT_ROOT / "artifacts" / "ps-003-workforce-growth-analysis" / "src"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from growth_analysis import compute_growth_rates


def test_yoy_formula_correctness() -> None:
    df = pl.DataFrame(
        {
            "profession": ["nurses", "nurses"],
            "sector": ["Public", "Public"],
            "year": [2018, 2019],
            "count": [100, 120],
        }
    ).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("sector").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )

    result = compute_growth_rates(df)
    yoy_value = (
        result.filter(
            (pl.col("profession") == "nurses")
            & (pl.col("sector") == "Public")
            & (pl.col("year") == 2019)
        )
        .select("yoy_pct")
        .item()
    )

    assert math.isclose(yoy_value, 20.0, rel_tol=1e-9)


def test_cagr_formula_correctness() -> None:
    df = pl.DataFrame(
        {
            "profession": ["doctors", "doctors"],
            "sector": ["Private", "Private"],
            "year": [2016, 2019],
            "count": [100, 172],
        }
    ).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("sector").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )

    result = compute_growth_rates(df)
    cagr_value = (
        result.filter(
            (pl.col("profession") == "doctors")
            & (pl.col("sector") == "Private")
            & (pl.col("year") == 2019)
        )
        .select("cagr")
        .item()
    )

    assert math.isclose(cagr_value, 0.19814528297901846, rel_tol=1e-9)


def test_first_year_yoy_is_null_for_each_group() -> None:
    df = pl.DataFrame(
        {
            "profession": ["pharmacists", "pharmacists", "pharmacists", "pharmacists"],
            "sector": ["Public", "Public", "Private", "Private"],
            "year": [2018, 2019, 2018, 2019],
            "count": [80, 88, 20, 18],
        }
    ).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("sector").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )

    result = compute_growth_rates(df)
    first_years = result.filter(pl.col("year") == 2018).sort(["sector"])
    assert first_years["yoy_pct"].to_list() == [None, None, None]


def test_single_year_group_has_null_cagr() -> None:
    df = pl.DataFrame(
        {
            "profession": ["physiotherapists"],
            "sector": ["Public"],
            "year": [2019],
            "count": [42],
        }
    ).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("sector").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )

    result = compute_growth_rates(df)
    assert result.select(pl.col("cagr").is_null().all()).item() is True


def test_zero_initial_count_excludes_cagr() -> None:
    df = pl.DataFrame(
        {
            "profession": ["nurses", "nurses"],
            "sector": ["Private", "Private"],
            "year": [2018, 2019],
            "count": [0, 50],
        }
    ).with_columns(
        [
            pl.col("profession").cast(pl.Categorical),
            pl.col("sector").cast(pl.Categorical),
            pl.col("year").cast(pl.Int32),
            pl.col("count").cast(pl.Int32),
        ]
    )

    result = compute_growth_rates(df)
    cagr_value = (
        result.filter(
            (pl.col("profession") == "nurses")
            & (pl.col("sector") == "Private")
            & (pl.col("year") == 2019)
        )
        .select("cagr")
        .item()
    )

    assert cagr_value is None