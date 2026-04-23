from __future__ import annotations

import importlib.util
from pathlib import Path

import joblib
import polars as pl
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA


BASE_DIR = Path(__file__).resolve().parents[2]
ARIMA_MODULE_PATH = BASE_DIR / "src" / "models" / "arima_model.py"
EVAL_MODULE_PATH = BASE_DIR / "src" / "model_evaluation.py"

ARIMA_SPEC = importlib.util.spec_from_file_location("arima_model", ARIMA_MODULE_PATH)
arima_model = importlib.util.module_from_spec(ARIMA_SPEC)
assert ARIMA_SPEC.loader is not None
ARIMA_SPEC.loader.exec_module(arima_model)

EVAL_SPEC = importlib.util.spec_from_file_location("model_evaluation", EVAL_MODULE_PATH)
model_evaluation = importlib.util.module_from_spec(EVAL_SPEC)
assert EVAL_SPEC.loader is not None
EVAL_SPEC.loader.exec_module(model_evaluation)


def _build_features() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "profession": ["doctors"] * 8 + ["nurses"] * 8,
            "year": [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019] * 2,
            "count": [100, 108, 117, 127, 138, 150, 163, 177, 300, 312, 324, 337, 351, 366, 382, 399],
            "year_index": [0, 1, 2, 3, 4, 5, 6, 7] * 2,
            "lag_1": [None, 100, 108, 117, 127, 138, 150, 163, None, 300, 312, 324, 337, 351, 366, 382],
            "lag_2": [None, None, 100, 108, 117, 127, 138, 150, None, None, 300, 312, 324, 337, 351, 366],
        }
    )


def test_train_arima_models_trains_and_returns_profession_models(tmp_path: Path) -> None:
    arima_model.MODELS_DIR = tmp_path
    arima_model.LOGS_DIR = tmp_path / "logs"

    features = _build_features()
    series_dict = {
        profession: features.filter(pl.col("profession") == profession).select(["year", "count"])
        for profession in ["doctors", "nurses"]
    }

    trained = arima_model.train_arima_models(series_dict, holdout_years=3)

    assert set(trained) == {"doctors", "nurses"}
    assert (tmp_path / "doctors_arima_20260423.pkl").exists() or any(
        path.name.startswith("doctors_arima_") for path in tmp_path.glob("*.pkl")
    )


def test_select_champions_prefers_linear_when_mape_is_within_threshold() -> None:
    eval_df = pl.DataFrame(
        {
            "profession": ["doctors", "doctors"],
            "model_type": ["linear", "arima"],
            "mape": [4.10, 4.00],
            "mae": [10.0, 9.8],
            "rmse": [11.0, 10.5],
        }
    )

    champions = model_evaluation.select_champions(eval_df)

    assert champions.item(0, "model_type") == "linear"


def test_generate_forecasts_for_linear_champion_returns_contract_columns(tmp_path: Path) -> None:
    model_evaluation.MODELS_DIR = tmp_path / "models"
    model_evaluation.LOGS_DIR = tmp_path / "logs"
    model_evaluation.MODELS_DIR.mkdir(parents=True, exist_ok=True)

    features = _build_features().filter(pl.col("profession") == "doctors")
    train_df = features.slice(0, features.height - model_evaluation.HOLDOUT_YEARS)
    linear_model = LinearRegression().fit(
        train_df.select("year_index").to_numpy(),
        train_df.get_column("count").to_numpy(),
    )
    joblib.dump(linear_model, model_evaluation.MODELS_DIR / "doctors_linear_20260423.pkl")

    champions = pl.DataFrame(
        {
            "profession": ["doctors"],
            "model_type": ["linear"],
            "mape": [5.0],
            "mae": [8.0],
            "rmse": [9.0],
        }
    )

    forecast_df = model_evaluation.generate_forecasts(champions, features, horizon=2)

    assert forecast_df.columns == [
        "profession",
        "year",
        "forecast_count",
        "model_type",
        "lower_95",
        "upper_95",
    ]
    assert forecast_df.get_column("year").to_list() == [2020, 2021]
    assert forecast_df.get_column("model_type").to_list() == ["linear", "linear"]
    assert all(
        lower <= upper
        for lower, upper in zip(
            forecast_df.get_column("lower_95").to_list(),
            forecast_df.get_column("upper_95").to_list(),
        )
    )