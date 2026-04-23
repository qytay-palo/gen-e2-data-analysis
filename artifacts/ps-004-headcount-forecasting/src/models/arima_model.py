"""ARIMA training helpers for PS-004 headcount forecasting."""

from __future__ import annotations

from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Any
import math
import warnings

import joblib
import polars as pl
from sklearn.base import RegressorMixin
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.arima.model import ARIMA


PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODELS_DIR = PROJECT_ROOT / "artifacts" / "ps-004-headcount-forecasting" / "models"
DATE_STAMP = datetime.now().strftime("%Y%m%d")
REQUIRED_COLUMNS = {"profession", "year", "count", "year_index", "lag_1", "lag_2"}
ARIMA_ORDERS = list(product((0, 1, 2), (0, 1), (0, 1, 2)))


def _validate_features(features: pl.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(features.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")


def _profession_frame(features: pl.DataFrame, profession: str) -> pl.DataFrame:
    return (
        features.filter(pl.col("profession").cast(pl.String) == profession)
        .sort("year")
        .with_columns(
            [
                pl.col("profession").cast(pl.String),
                pl.col("year").cast(pl.Int32),
                pl.col("count").cast(pl.Float64),
                pl.col("year_index").cast(pl.Int32),
            ]
        )
    )


def _safe_profession_name(profession: str) -> str:
    if not profession or profession in {".", ".."} or "/" in profession or "\\" in profession:
        raise ValueError(f"Unsafe profession name for model path: {profession!r}")
    return profession


def _load_linear_fallback(profession: str) -> RegressorMixin:
    safe_profession = _safe_profession_name(profession)
    linear_path = MODELS_DIR / f"{safe_profession}_linear_{DATE_STAMP}.pkl"
    if not linear_path.exists():
        raise FileNotFoundError(f"Missing linear fallback model: {linear_path}")
    return joblib.load(linear_path)


def train_arima_models(
    features: pl.DataFrame, holdout_years: int = 3
) -> dict[str, tuple[Any, tuple[int, int, int] | None]]:
    """Train one ARIMA model per profession using AIC-based grid search."""
    _validate_features(features)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    trained_models: dict[str, tuple[Any, tuple[int, int, int] | None]] = {}
    professions = (
        features.select(pl.col("profession").cast(pl.String).unique().sort())
        .to_series()
        .to_list()
    )

    for profession in professions:
        safe_profession = _safe_profession_name(profession)
        profession_features = _profession_frame(features, profession)
        if profession_features.height <= holdout_years:
            print(
                f"WARNING [{profession}] insufficient rows for holdout_years={holdout_years}; "
                "using linear fallback."
            )
            fallback_model = _load_linear_fallback(profession)
            fallback_path = MODELS_DIR / f"{safe_profession}_arima_{DATE_STAMP}.pkl"
            joblib.dump(fallback_model, fallback_path)
            trained_models[profession] = (fallback_model, None)
            continue

        train_features = profession_features.head(profession_features.height - holdout_years)
        train_series = train_features.get_column("count").to_list()

        best_model: Any | None = None
        best_order: tuple[int, int, int] | None = None
        best_aic = math.inf

        for order in ARIMA_ORDERS:
            try:
                with warnings.catch_warnings(record=True) as caught_warnings:
                    warnings.filterwarnings("always", category=ConvergenceWarning)
                    warnings.filterwarnings("always", category=UserWarning)
                    candidate_model = ARIMA(train_series, order=order)
                    fitted_model = candidate_model.fit()

                for caught_warning in caught_warnings:
                    if issubclass(caught_warning.category, ConvergenceWarning):
                        print(
                            f"WARNING [{profession}] ARIMA{order} convergence warning: "
                            f"{caught_warning.message}"
                        )

                candidate_aic = float(fitted_model.aic)
                if math.isfinite(candidate_aic) and candidate_aic < best_aic:
                    best_model = fitted_model
                    best_order = order
                    best_aic = candidate_aic
            except Exception as exc:
                print(f"WARNING [{profession}] ARIMA{order} failed: {exc}")

        model_path = MODELS_DIR / f"{safe_profession}_arima_{DATE_STAMP}.pkl"
        if best_model is None or best_order is None:
            print(
                f"WARNING [{profession}] grid search failed for all ARIMA orders; "
                "using linear fallback."
            )
            fallback_model = _load_linear_fallback(profession)
            joblib.dump(fallback_model, model_path)
            trained_models[profession] = (fallback_model, None)
            continue

        print(f"INFO [{profession}] selected ARIMA{best_order} with AIC={best_aic:.3f}")
        joblib.dump(best_model, model_path)
        trained_models[profession] = (best_model, best_order)

    return trained_models