"""Evaluation and forecasting helpers for PS-004 headcount forecasting."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import math

import matplotlib.pyplot as plt
import numpy as np
import polars as pl


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PS004_ROOT = PROJECT_ROOT / "artifacts" / "ps-004-headcount-forecasting"
METRICS_DIR = PS004_ROOT / "results" / "metrics"
EXPORTS_DIR = PS004_ROOT / "results" / "exports"
FIGURES_DIR = PS004_ROOT / "reports" / "figures"
MODEL_COMPARISON_PATH = METRICS_DIR / "model_comparison.csv"
MODEL_REGISTRY_PATH = METRICS_DIR / "model_registry.csv"
FORECAST_TABLE_PATH = EXPORTS_DIR / "forecast_table.csv"
FORECAST_FIGURE_PATH = FIGURES_DIR / "forecast_by_profession.png"
REQUIRED_COLUMNS = {"profession", "year", "count", "year_index", "lag_1", "lag_2"}


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


def _split_train_validation(
    profession_features: pl.DataFrame, holdout_years: int
) -> tuple[pl.DataFrame, pl.DataFrame]:
    if profession_features.height <= holdout_years:
        raise ValueError(
            f"Profession '{profession_features.get_column('profession')[0]}' does not have enough rows "
            f"for holdout_years={holdout_years}"
        )
    return (
        profession_features.head(profession_features.height - holdout_years),
        profession_features.tail(holdout_years),
    )


def _calculate_metrics(
    profession: str, model_type: str, actual: np.ndarray, predicted: np.ndarray
) -> dict[str, Any]:
    actual = actual.astype(float)
    predicted = predicted.astype(float)
    absolute_error = np.abs(actual - predicted)
    mape = float(np.mean(absolute_error / np.clip(actual, 1e-9, None)) * 100)
    mae = float(np.mean(absolute_error))
    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
    return {
        "profession": profession,
        "model_type": model_type,
        "mape": round(mape, 4),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
    }


def _linear_predict(model: Any, year_index: np.ndarray) -> np.ndarray:
    return np.asarray(model.predict(year_index.reshape(-1, 1)), dtype=float)


def evaluate_models(
    features: pl.DataFrame,
    linear_models: dict[str, Any],
    arima_models: dict[str, tuple[Any, tuple[int, int, int] | None]],
    holdout_years: int = 3,
) -> pl.DataFrame:
    """Evaluate linear and ARIMA candidates on the held-out validation window."""
    _validate_features(features)
    metric_rows: list[dict[str, Any]] = []

    professions = (
        features.select(pl.col("profession").cast(pl.String).unique().sort())
        .to_series()
        .to_list()
    )

    for profession in professions:
        profession_features = _profession_frame(features, profession)
        _, validation_features = _split_train_validation(profession_features, holdout_years)
        actual = validation_features.get_column("count").to_numpy()

        linear_model = linear_models[profession]
        linear_prediction = _linear_predict(
            linear_model,
            validation_features.get_column("year_index").to_numpy(),
        )
        metric_rows.append(_calculate_metrics(profession, "linear", actual, linear_prediction))

        arima_model, arima_order = arima_models[profession]
        if hasattr(arima_model, "forecast"):
            arima_prediction = np.asarray(arima_model.forecast(steps=holdout_years), dtype=float)
        else:
            arima_prediction = _linear_predict(
                arima_model,
                validation_features.get_column("year_index").to_numpy(),
            )

        arima_metrics = _calculate_metrics(profession, "arima", actual, arima_prediction)
        arima_metrics["arima_order"] = None if arima_order is None else str(arima_order)
        arima_metrics["arima_is_fallback"] = arima_order is None
        metric_rows.append(arima_metrics)

    return pl.DataFrame(metric_rows).sort(["profession", "model_type"])


def select_champions(eval_df: pl.DataFrame) -> pl.DataFrame:
    """Select one champion model per profession using the PS-004 tie-break rules."""
    required_columns = {"profession", "model_type", "mape", "mae", "rmse"}
    missing_columns = required_columns.difference(eval_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required evaluation columns: {missing}")

    champion_rows: list[dict[str, Any]] = []
    professions = eval_df.get_column("profession").unique().sort().to_list()

    for profession in professions:
        profession_metrics = eval_df.filter(pl.col("profession") == profession)
        linear_row = profession_metrics.filter(pl.col("model_type") == "linear").to_dicts()[0]
        arima_row = profession_metrics.filter(pl.col("model_type") == "arima").to_dicts()[0]

        mape_gap = abs(float(linear_row["mape"]) - float(arima_row["mape"]))
        if mape_gap < 0.25:
            selected_row = linear_row
        elif float(arima_row["mape"]) < float(linear_row["mape"]):
            selected_row = arima_row
        elif float(arima_row["mape"]) > float(linear_row["mape"]):
            selected_row = linear_row
        else:
            selected_row = (
                arima_row if float(arima_row["rmse"]) < float(linear_row["rmse"]) else linear_row
            )

        champion_rows.append(
            {
                "profession": profession,
                "model_type": selected_row["model_type"],
                "mape": round(float(selected_row["mape"]), 4),
                "mae": round(float(selected_row["mae"]), 4),
                "rmse": round(float(selected_row["rmse"]), 4),
                "mape_target_met": float(selected_row["mape"]) < 10.0,
            }
        )

    return pl.DataFrame(champion_rows).sort("profession")


def _linear_residual_std(model: Any, train_features: pl.DataFrame) -> float:
    fitted = _linear_predict(model, train_features.get_column("year_index").to_numpy())
    residuals = train_features.get_column("count").to_numpy() - fitted
    residual_std = float(np.std(residuals, ddof=1)) if residuals.size > 1 else 0.0
    return residual_std if math.isfinite(residual_std) else 0.0


def generate_forecast(
    features: pl.DataFrame, champion_models: dict[str, dict[str, Any]], horizon: int = 5
) -> pl.DataFrame:
    """Generate 5-year profession forecasts with 95% confidence intervals."""
    _validate_features(features)
    forecast_rows: list[dict[str, Any]] = []

    for profession, champion in champion_models.items():
        profession_features = _profession_frame(features, profession)
        train_features, _ = _split_train_validation(profession_features, holdout_years=3)
        last_observed_year = int(profession_features.select(pl.col("year").max()).item())
        forecast_years = list(range(last_observed_year + 1, last_observed_year + horizon + 1))
        model = champion["model"]
        model_type = champion["model_type"]

        if model_type == "arima" and hasattr(model, "get_forecast"):
            summary_frame = model.get_forecast(steps=horizon).summary_frame(alpha=0.05)
            point_forecast = np.asarray(summary_frame["mean"], dtype=float)
            lower_95 = np.asarray(summary_frame["mean_ci_lower"], dtype=float)
            upper_95 = np.asarray(summary_frame["mean_ci_upper"], dtype=float)
        else:
            future_year_index = np.arange(
                int(profession_features.select(pl.col("year_index").max()).item()) + 1,
                int(profession_features.select(pl.col("year_index").max()).item()) + horizon + 1,
                dtype=float,
            )
            point_forecast = _linear_predict(model, future_year_index)
            residual_std = _linear_residual_std(model, train_features)
            interval = 1.96 * residual_std
            lower_95 = point_forecast - interval
            upper_95 = point_forecast + interval

        for year, forecast_count, lower_bound, upper_bound in zip(
            forecast_years, point_forecast, lower_95, upper_95
        ):
            forecast_rows.append(
                {
                    "profession": profession,
                    "year": int(year),
                    "forecast_count": round(float(forecast_count), 4),
                    "model_type": model_type,
                    "lower_95": round(float(lower_bound), 4),
                    "upper_95": round(float(upper_bound), 4),
                }
            )

    return pl.DataFrame(forecast_rows).sort(["profession", "year"])


def build_model_registry(champion_df: pl.DataFrame, forecast_df: pl.DataFrame) -> pl.DataFrame:
    registry_rows: list[dict[str, Any]] = []
    for row in champion_df.to_dicts():
        profession_forecast = forecast_df.filter(pl.col("profession") == row["profession"])
        registry_rows.append(
            {
                "profession": row["profession"],
                "model_type": row["model_type"],
                "mape": row["mape"],
                "mae": row["mae"],
                "rmse": row["rmse"],
                "mape_target_met": row["mape_target_met"],
                "forecast_start_year": int(profession_forecast.select(pl.col("year").min()).item()),
                "forecast_end_year": int(profession_forecast.select(pl.col("year").max()).item()),
            }
        )
    return pl.DataFrame(registry_rows).sort("profession")


def write_contract_outputs(
    eval_df: pl.DataFrame, champion_df: pl.DataFrame, forecast_df: pl.DataFrame
) -> tuple[Path, Path, Path]:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    eval_df.select(["profession", "model_type", "mape", "mae", "rmse"]).write_csv(
        MODEL_COMPARISON_PATH
    )
    build_model_registry(champion_df, forecast_df).write_csv(MODEL_REGISTRY_PATH)
    forecast_df.select(
        ["profession", "year", "forecast_count", "model_type", "lower_95", "upper_95"]
    ).write_csv(FORECAST_TABLE_PATH)

    return MODEL_COMPARISON_PATH, MODEL_REGISTRY_PATH, FORECAST_TABLE_PATH


def plot_forecast_by_profession(
    features: pl.DataFrame, forecast_df: pl.DataFrame, output_path: Path = FORECAST_FIGURE_PATH
) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    professions = forecast_df.get_column("profession").unique().sort().to_list()
    fig, axes = plt.subplots(len(professions), 1, figsize=(10, 3.5 * len(professions)), sharex=True)

    if len(professions) == 1:
        axes = [axes]

    for axis, profession in zip(axes, professions):
        history = _profession_frame(features, profession)
        projection = forecast_df.filter(pl.col("profession") == profession).sort("year")

        history_years = history.get_column("year").to_list()
        history_counts = history.get_column("count").to_list()
        forecast_years = projection.get_column("year").to_list()
        forecast_counts = projection.get_column("forecast_count").to_list()
        lower_95 = projection.get_column("lower_95").to_list()
        upper_95 = projection.get_column("upper_95").to_list()

        axis.plot(history_years, history_counts, marker="o", linewidth=2, color="#1f4e79", label="historical")
        axis.plot(forecast_years, forecast_counts, marker="o", linewidth=2, color="#c44e52", label="forecast")
        axis.fill_between(forecast_years, lower_95, upper_95, color="#c44e52", alpha=0.2, label="95% CI")
        axis.set_title(profession.title())
        axis.set_ylabel("Headcount")
        axis.grid(alpha=0.3)

    axes[-1].set_xlabel("Year")
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path