from __future__ import annotations

import importlib.util
from pathlib import Path

import polars as pl

MODULE_PATH = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ps-001-workforce-trends-forecasting"
    / "src"
    / "workforce_trends_utils.py"
)
SPEC = importlib.util.spec_from_file_location("workforce_trends_utils", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_standardize_workforce_frame_adds_profession() -> None:
    dataframe = pl.DataFrame({"Year Value": [2024], "Sector Name": ["Public"]})
    result = MODULE.standardize_workforce_frame(dataframe, "doctors")

    assert result.columns == ["year_value", "sector_name", "profession"]
    assert result["profession"].to_list() == ["doctors"]


def test_combine_workforce_frames_combines_multiple_professions() -> None:
    result = MODULE.combine_workforce_frames(
        {
            "doctors": pl.DataFrame({"year": [2023], "count": [10]}),
            "nurses": pl.DataFrame({"year": [2023], "count": [20]}),
        }
    )

    assert result.height == 2
    assert sorted(result["profession"].to_list()) == ["doctors", "nurses"]
