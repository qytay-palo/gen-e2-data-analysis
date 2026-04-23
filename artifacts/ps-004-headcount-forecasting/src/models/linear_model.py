from __future__ import annotations

from datetime import datetime
from pathlib import Path

import joblib
import polars as pl
from loguru import logger
from sklearn.linear_model import LinearRegression


ROOT = Path(__file__).resolve().parents[4]
MODELS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/models"
LOGS_DIR = ROOT / "artifacts/ps-004-headcount-forecasting/logs"
REQUIRED_COLUMNS = {"profession", "year", "year_index", "count"}
_LOGGER_CONFIGURED = False


def _configure_logger() -> None:
    global _LOGGER_CONFIGURED

    if _LOGGER_CONFIGURED:
        return

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"linear_model_training_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log"
    logger.add(log_path, level="INFO", enqueue=False)
    _LOGGER_CONFIGURED = True


def train_linear_models(
    features_df: pl.DataFrame,
    holdout_years: int = 3,
) -> dict[str, LinearRegression]:
    """Train one linear regression baseline per profession using year_index only."""
    missing_columns = REQUIRED_COLUMNS.difference(features_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Features data is missing required columns: {missing}")
    if holdout_years < 1:
        raise ValueError("holdout_years must be at least 1")

    _configure_logger()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    run_date = datetime.now().strftime("%Y%m%d")
    models: dict[str, LinearRegression] = {}

    profession_names = sorted(features_df["profession"].cast(pl.Utf8).unique().to_list())
    for profession in profession_names:
        profession_df = (
            features_df.filter(pl.col("profession").cast(pl.Utf8) == profession)
            .sort("year")
            .select(["profession", "year", "year_index", "count"])
        )

        if profession_df.height <= holdout_years:
            raise ValueError(
                f"Profession '{profession}' has {profession_df.height} rows, which is not enough for a {holdout_years}-year holdout"
            )

        train_df = profession_df.slice(0, profession_df.height - holdout_years)
        logger.info(
            "Training linear model for {profession}: {n_rows} rows, years {year_start}-{year_end}",
            profession=profession,
            n_rows=train_df.height,
            year_start=train_df.item(0, "year"),
            year_end=train_df.item(train_df.height - 1, "year"),
        )

        model = LinearRegression()
        model.fit(
            train_df.select("year_index").to_numpy(),
            train_df.get_column("count").to_numpy(),
        )

        model_path = MODELS_DIR / f"{profession}_linear_{run_date}.pkl"
        joblib.dump(model, model_path)
        logger.info("Saved linear model for {profession} to {path}", profession=profession, path=model_path)
        models[profession] = model

    return models