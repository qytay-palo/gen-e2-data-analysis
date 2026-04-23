from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import json

import joblib
import numpy as np
import polars as pl
from loguru import logger


ROOT = Path(__file__).resolve().parents[3]
FEATURES_PATH = (
    ROOT / "artifacts/ps-004-headcount-forecasting/data/3_interim/features.parquet"
)
SOURCE_DATA_PATH = ROOT / "shared/data/4_processed/workforce_clean.parquet"
MODELS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/models"
LOGS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/logs"
METRICS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/results/metrics"
EXPORTS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/results/exports"
HANDOFF_DIR = (
    ROOT / "docs/agent-handoffs/model-forecasting/ps-004-headcount-forecasting"
)
HOLDOUT_YEARS = 3
MAPE_TARGET = 10.0
REQUIRED_COLUMNS = {"profession", "year", "year_index", "count"}
_LOGGER_CONFIGURED = False


def _configure_logger() -> None:
    global _LOGGER_CONFIGURED

    if _LOGGER_CONFIGURED:
        return

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"model_evaluation_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log"
    logger.add(log_path, level="INFO", enqueue=False)
    _LOGGER_CONFIGURED = True


def _validate_features(features_df: pl.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(features_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Features data is missing required columns: {missing}")


def _resolve_model(model_or_path: Any) -> Any:
    if isinstance(model_or_path, (str, Path)):
        return joblib.load(model_or_path)
    return model_or_path


def _metric_row(
    profession: str,
    model_type: str,
    actual: np.ndarray,
    predicted: np.ndarray,
) -> dict[str, float | str]:
    actual = actual.astype(float)
    predicted = predicted.astype(float)
    abs_error = np.abs(actual - predicted)
    mape = float(np.mean(abs_error / actual) * 100.0)
    mae = float(np.mean(abs_error))
    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
    return {
        "profession": profession,
        "model_type": model_type,
        "mape": mape,
        "mae": mae,
        "rmse": rmse,
    }


def _profession_frame(features_df: pl.DataFrame, profession: str) -> pl.DataFrame:
    return (
        features_df.filter(pl.col("profession") == profession)
        .sort("year")
        .select(["profession", "year", "year_index", "count"])
    )


def _train_validation_split(profession_df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    if profession_df.height <= HOLDOUT_YEARS:
        raise ValueError(
            f"Profession '{profession_df.item(0, 'profession')}' has insufficient rows for a {HOLDOUT_YEARS}-year holdout"
        )
    return (
        profession_df.slice(0, profession_df.height - HOLDOUT_YEARS),
        profession_df.slice(profession_df.height - HOLDOUT_YEARS, HOLDOUT_YEARS),
    )


def evaluate_models(
    features_df: pl.DataFrame,
    linear_models: dict,
    arima_models: dict,
) -> pl.DataFrame:
    """Compute validation metrics for each profession-model pair."""
    _configure_logger()
    _validate_features(features_df)
    rows: list[dict[str, float | str]] = []

    for profession in sorted(features_df.get_column("profession").unique().to_list()):
        profession_df = _profession_frame(features_df, profession)
        _, validation_df = _train_validation_split(profession_df)
        actual = validation_df.get_column("count").to_numpy()

        linear_model = linear_models.get(profession)
        if linear_model is not None:
            linear_model = _resolve_model(linear_model)
            linear_pred = np.asarray(
                linear_model.predict(validation_df.select("year_index").to_numpy()),
                dtype=float,
            )
            rows.append(_metric_row(profession, "linear", actual, linear_pred))

        arima_model = arima_models.get(profession)
        if arima_model is not None:
            arima_model = _resolve_model(arima_model)
            arima_pred = np.asarray(
                arima_model.get_forecast(steps=validation_df.height).predicted_mean,
                dtype=float,
            )
            rows.append(_metric_row(profession, "arima", actual, arima_pred))
        else:
            logger.warning(
                "No ARIMA model available for {profession}; evaluation will rely on the linear baseline only",
                profession=profession,
            )

    return pl.DataFrame(rows).sort(["profession", "model_type"])


def select_champions(eval_df: pl.DataFrame) -> pl.DataFrame:
    """Select the champion model per profession with a simplicity preference for near-ties."""
    if eval_df.is_empty():
        return pl.DataFrame(
            schema={
                "profession": pl.Utf8,
                "model_type": pl.Utf8,
                "mape": pl.Float64,
                "mae": pl.Float64,
                "rmse": pl.Float64,
            }
        )

    rows: list[dict[str, float | str]] = []
    for profession in sorted(eval_df.get_column("profession").unique().to_list()):
        profession_eval = eval_df.filter(pl.col("profession") == profession).sort(
            ["mape", "rmse", "model_type"]
        )
        best_row = profession_eval.row(0, named=True)
        linear_row = profession_eval.filter(pl.col("model_type") == "linear")

        if linear_row.height:
            linear_candidate = linear_row.row(0, named=True)
            if linear_candidate["model_type"] != best_row["model_type"]:
                mape_gap = float(linear_candidate["mape"]) - float(best_row["mape"])
                if mape_gap < 0.25:
                    best_row = linear_candidate

        rows.append(best_row)

    return pl.DataFrame(rows).sort("profession")


def _latest_model_path(profession: str, model_type: str) -> Path:
    candidates = sorted(MODELS_DIR.glob(f"{profession}_{model_type}_*.pkl"))
    if not candidates:
        raise FileNotFoundError(
            f"No serialized {model_type} model found for profession '{profession}' in {MODELS_DIR}"
        )
    return candidates[-1]


def _linear_residual_std(profession_df: pl.DataFrame, linear_model: Any) -> float:
    train_df, _ = _train_validation_split(profession_df)
    train_actual = train_df.get_column("count").to_numpy().astype(float)
    train_pred = np.asarray(
        linear_model.predict(train_df.select("year_index").to_numpy()),
        dtype=float,
    )
    residuals = train_actual - train_pred
    if residuals.size <= 1:
        return 0.0
    return float(np.std(residuals, ddof=1))


def _forecast_intervals_from_conf_int(conf_int: Any) -> tuple[np.ndarray, np.ndarray]:
    if hasattr(conf_int, "iloc"):
        lower = np.asarray(conf_int.iloc[:, 0], dtype=float)
        upper = np.asarray(conf_int.iloc[:, 1], dtype=float)
        return lower, upper

    conf_array = np.asarray(conf_int, dtype=float)
    return conf_array[:, 0], conf_array[:, 1]


def generate_forecasts(
    champions: pl.DataFrame,
    features_df: pl.DataFrame,
    horizon: int = 5,
) -> pl.DataFrame:
    """Generate horizon-year forecasts and confidence intervals using the champion model per profession."""
    _configure_logger()
    _validate_features(features_df)
    if horizon < 1:
        raise ValueError("horizon must be at least 1")

    rows: list[dict[str, float | int | str]] = []
    for champion in champions.iter_rows(named=True):
        profession = str(champion["profession"])
        model_type = str(champion["model_type"])
        profession_df = _profession_frame(features_df, profession)
        last_year = int(profession_df.get_column("year").max())

        if model_type == "linear":
            model = _resolve_model(_latest_model_path(profession, "linear"))
            next_index = int(profession_df.get_column("year_index").max()) + 1
            future_index = np.arange(next_index, next_index + horizon, dtype=float).reshape(-1, 1)
            forecast = np.asarray(model.predict(future_index), dtype=float)
            residual_std = _linear_residual_std(profession_df, model)
            margin = 1.96 * residual_std
            lower = forecast - margin
            upper = forecast + margin
        elif model_type == "arima":
            model = _resolve_model(_latest_model_path(profession, "arima"))
            forecast_result = model.get_forecast(steps=horizon)
            forecast = np.asarray(forecast_result.predicted_mean, dtype=float)
            lower, upper = _forecast_intervals_from_conf_int(forecast_result.conf_int(alpha=0.05))
        else:
            raise ValueError(f"Unsupported model_type '{model_type}' for profession '{profession}'")

        lower = np.maximum(lower, 0.0)
        upper = np.maximum(upper, lower)
        for offset in range(horizon):
            rows.append(
                {
                    "profession": profession,
                    "year": last_year + offset + 1,
                    "forecast_count": float(forecast[offset]),
                    "model_type": model_type,
                    "lower_95": float(lower[offset]),
                    "upper_95": float(upper[offset]),
                }
            )

    return pl.DataFrame(rows).sort(["profession", "year"])


def load_serialized_models(model_type: str) -> dict[str, Any]:
    models: dict[str, Any] = {}
    for model_path in sorted(MODELS_DIR.glob(f"*_{model_type}_*.pkl")):
        profession = model_path.name.split(f"_{model_type}_", maxsplit=1)[0]
        models[profession] = joblib.load(model_path)
    return models


def export_results(
    eval_df: pl.DataFrame,
    champions: pl.DataFrame,
    forecast_df: pl.DataFrame,
) -> tuple[Path, Path, Path]:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    model_comparison_path = METRICS_DIR / "model_comparison.csv"
    model_registry_path = METRICS_DIR / "model_registry.csv"
    forecast_table_path = EXPORTS_DIR / "forecast_table.csv"

    eval_df.write_csv(model_comparison_path)

    forecast_years = forecast_df.group_by("profession").agg(
        [
            pl.col("year").min().alias("forecast_start_year"),
            pl.col("year").max().alias("forecast_end_year"),
        ]
    )
    model_registry = (
        champions.join(forecast_years, on="profession", how="left")
        .with_columns((pl.col("mape") < MAPE_TARGET).alias("mape_target_met"))
        .select(
            [
                "profession",
                "model_type",
                "mape",
                "mae",
                "rmse",
                "mape_target_met",
                "forecast_start_year",
                "forecast_end_year",
            ]
        )
        .sort("profession")
    )
    model_registry.write_csv(model_registry_path)

    forecast_df.select(
        ["profession", "year", "forecast_count", "model_type", "lower_95", "upper_95"]
    ).write_csv(forecast_table_path)

    for row in model_registry.iter_rows(named=True):
        if not row["mape_target_met"]:
            logger.warning(
                "MAPE target not met for {profession}: champion={model_type}, MAPE={mape:.2f}%",
                profession=row["profession"],
                model_type=row["model_type"],
                mape=row["mape"],
            )

    return model_comparison_path, model_registry_path, forecast_table_path


def write_handoff(champions: pl.DataFrame) -> Path:
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_date = datetime.now().strftime("%Y%m%d")
    notes = "; ".join(
        f"{row['profession']}: champion={row['model_type']}, MAPE={row['mape']:.2f}%, target_met={'yes' if row['mape'] < MAPE_TARGET else 'no'}"
        for row in champions.iter_rows(named=True)
    )
    payload = {
        "status": "success",
        "problem_statement": "PS-004 Headcount Forecasting",
        "handoff_metadata": {
            "agent": "model-forecasting",
            "problem_statement_id": "ps-004",
            "timestamp": timestamp,
        },
        "artifacts": [
            "artifacts/ps-004-headcount-forecasting/src/models/arima_model.py",
            "artifacts/ps-004-headcount-forecasting/src/model_evaluation.py",
            "artifacts/ps-004-headcount-forecasting/results/metrics/model_comparison.csv",
            "artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv",
            "artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv",
        ],
        "outputs": [
            "artifacts/ps-004-headcount-forecasting/results/metrics/model_comparison.csv",
            "artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv",
            "artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv",
            f"artifacts/ps-004-headcount-forecasting/models/doctors_arima_{run_date}.pkl",
            f"artifacts/ps-004-headcount-forecasting/models/nurses_arima_{run_date}.pkl",
            f"artifacts/ps-004-headcount-forecasting/models/pharmacists_arima_{run_date}.pkl",
            f"artifacts/ps-004-headcount-forecasting/models/physiotherapists_arima_{run_date}.pkl",
        ],
        "notes": notes,
    }
    handoff_path = HANDOFF_DIR / f"forecasting_to_verify_{timestamp}.json"
    handoff_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return handoff_path


def main() -> tuple[Path, Path, Path, Path]:
    _configure_logger()
    features_df = pl.read_parquet(FEATURES_PATH)
    source_df = pl.read_parquet(SOURCE_DATA_PATH)
    logger.info(
        "Loaded feature data with {feature_rows} rows and source data through year {last_year}",
        feature_rows=features_df.height,
        last_year=int(source_df.get_column("year").max()),
    )

    linear_models = load_serialized_models("linear")
    arima_models = load_serialized_models("arima")
    eval_df = evaluate_models(features_df, linear_models, arima_models)
    champions = select_champions(eval_df)
    forecast_df = generate_forecasts(champions, features_df, horizon=5)
    model_comparison_path, model_registry_path, forecast_table_path = export_results(
        eval_df,
        champions,
        forecast_df,
    )

    for row in champions.iter_rows(named=True):
        logger.info(
            "Champion for {profession}: {model_type} (MAPE={mape:.2f}%, RMSE={rmse:.2f})",
            profession=row["profession"],
            model_type=row["model_type"],
            mape=row["mape"],
            rmse=row["rmse"],
        )

    handoff_path = write_handoff(champions)
    return model_comparison_path, model_registry_path, forecast_table_path, handoff_path


if __name__ == "__main__":
    main()