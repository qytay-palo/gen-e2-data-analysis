from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import warnings

import joblib
import polars as pl
from loguru import logger
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.arima.model import ARIMA, ARIMAResultsWrapper


ROOT = Path(__file__).resolve().parents[4]
FEATURES_PATH = (
    ROOT / "artifacts/ps-004-headcount-forecasting/data/3_interim/features.parquet"
)
MODELS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/models"
LOGS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/logs"
REQUIRED_COLUMNS = {"count"}
SEARCH_ORDERS = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 2),
    (0, 1, 0),
    (0, 1, 1),
    (0, 1, 2),
    (1, 0, 0),
    (1, 0, 1),
    (1, 0, 2),
    (1, 1, 0),
    (1, 1, 1),
    (1, 1, 2),
    (2, 0, 0),
    (2, 0, 1),
    (2, 0, 2),
    (2, 1, 0),
    (2, 1, 1),
    (2, 1, 2),
)
_LOGGER_CONFIGURED = False

warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", module="statsmodels")


def _configure_logger() -> None:
    global _LOGGER_CONFIGURED

    if _LOGGER_CONFIGURED:
        return

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"arima_model_training_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log"
    logger.add(log_path, level="INFO", enqueue=False)
    _LOGGER_CONFIGURED = True


def _coerce_series_frame(series_like: Any) -> pl.DataFrame:
    if isinstance(series_like, pl.DataFrame):
        frame = series_like.clone()
    elif isinstance(series_like, dict):
        frame = pl.DataFrame(series_like)
    else:
        frame = pl.DataFrame({"count": list(series_like)})

    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Series data is missing required columns: {missing}")

    if "year" in frame.columns:
        sort_col = "year"
    elif "year_index" in frame.columns:
        sort_col = "year_index"
    else:
        frame = frame.with_row_index(name="year_index")
        sort_col = "year_index"

    selected_columns = [column for column in ["year", "year_index", "count"] if column in frame.columns]
    return (
        frame.select(selected_columns)
        .sort(sort_col)
        .with_columns(pl.col("count").cast(pl.Float64))
    )


def _fit_best_arima(counts: list[float]) -> tuple[ARIMAResultsWrapper, tuple[int, int, int], float]:
    best_model: ARIMAResultsWrapper | None = None
    best_order: tuple[int, int, int] | None = None
    best_aic: float | None = None
    failures: list[str] = []

    for order in SEARCH_ORDERS:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ConvergenceWarning)
                warnings.filterwarnings("ignore", module="statsmodels")
                candidate = ARIMA(
                    counts,
                    order=order,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                ).fit()
            candidate_aic = float(candidate.aic)
            if best_aic is None or candidate_aic < best_aic:
                best_model = candidate
                best_order = order
                best_aic = candidate_aic
        except Exception as exc:
            failures.append(f"{order}: {exc}")

    if best_model is None or best_order is None or best_aic is None:
        detail = "; ".join(failures[:5])
        raise RuntimeError(f"ARIMA grid search failed for all candidate orders. {detail}")

    return best_model, best_order, best_aic


def train_arima_models(
    series_dict: dict,
    holdout_years: int = 3,
) -> dict[str, ARIMAResultsWrapper]:
    """Train one AIC-selected ARIMA model per profession on the training split."""
    if holdout_years < 1:
        raise ValueError("holdout_years must be at least 1")

    _configure_logger()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    run_date = datetime.now().strftime("%Y%m%d")
    trained_models: dict[str, ARIMAResultsWrapper] = {}

    for profession, series_like in sorted(series_dict.items()):
        profession_df = _coerce_series_frame(series_like)
        if profession_df.height <= holdout_years:
            logger.error(
                "Skipping ARIMA for {profession}: {n_rows} rows is not enough for a {holdout_years}-year holdout",
                profession=profession,
                n_rows=profession_df.height,
                holdout_years=holdout_years,
            )
            continue

        train_df = profession_df.slice(0, profession_df.height - holdout_years)
        train_counts = train_df.get_column("count").to_list()

        try:
            model, order, aic = _fit_best_arima(train_counts)
            model_path = MODELS_DIR / f"{profession}_arima_{run_date}.pkl"
            joblib.dump(model, model_path)
            logger.info(
                "Selected ARIMA{order} for {profession} with AIC={aic:.3f}; saved to {path}",
                order=order,
                profession=profession,
                aic=aic,
                path=model_path,
            )
            trained_models[profession] = model
        except Exception as exc:
            logger.error(
                "ARIMA grid search failed for {profession}; falling back to linear baseline. Error: {error}",
                profession=profession,
                error=exc,
            )

    return trained_models


def _build_series_dict(features_df: pl.DataFrame) -> dict[str, pl.DataFrame]:
    return {
        profession: (
            features_df.filter(pl.col("profession") == profession)
            .sort("year")
            .select(["year", "year_index", "count"])
        )
        for profession in sorted(features_df.get_column("profession").unique().to_list())
    }


def main() -> dict[str, ARIMAResultsWrapper]:
    features_df = pl.read_parquet(FEATURES_PATH)
    return train_arima_models(_build_series_dict(features_df))


if __name__ == "__main__":
    main()