from __future__ import annotations

import importlib.util
from pathlib import Path

import polars as pl

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "workforce_trends_utils.py"
)
SPEC = importlib.util.spec_from_file_location("workforce_trends_utils", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_schema_snapshot_returns_expected_columns() -> None:
    dataframe = pl.DataFrame({"year": [2024], "count": [100]})
    snapshot = MODULE.build_schema_snapshot(dataframe)

    assert snapshot.columns == ["column_name", "dtype", "null_count"]
    assert snapshot.height == 2
