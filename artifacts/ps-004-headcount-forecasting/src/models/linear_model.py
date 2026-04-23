"""Linear baseline training for PS-004 headcount forecasting."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Final

import joblib
import polars as pl
from sklearn.linear_model import LinearRegression


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[4]
MODELS_DIR: Final[Path] = (
    PROJECT_ROOT / "artifacts" / "ps-004-headcount-forecasting" / "models"
)
DATE_STAMP: Final[str] = datetime.now().strftime("%Y%m%d")
REQUIRED_COLUMNS: Final[set[str]] = {"profession", "year", "count", "year_index"}


def train_linear_models(
    features: pl.DataFrame, holdout_years: int = 3
) -> dict[str, LinearRegression]:
    """Train one linear regression baseline per profession."""
    missing_columns = REQUIRED_COLUMNS.difference(features.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    trained_models: dict[str, LinearRegression] = {}
    professions = features.select(pl.col("profession").cast(pl.String).unique().sort()).to_series()

    for profession in professions.to_list():
        if (
            not profession
            or profession in {".", ".."}
            or "/" in profession
            or "\\" in profession
        ):
            raise ValueError(f"Unsafe profession name for model path: {profession!r}")

        profession_features = (
            features.filter(pl.col("profession").cast(pl.String) == profession)
            .sort("year")
            .with_columns(
                [
                    pl.col("year").cast(pl.Int32),
                    pl.col("count").cast(pl.Int32),
                    pl.col("year_index").cast(pl.Int32),
                ]
            )
        )
        if profession_features.height <= holdout_years:
            raise ValueError(
                f"Profession '{profession}' does not have enough rows for holdout_years={holdout_years}"
            )

        train_features = profession_features.head(profession_features.height - holdout_years)
        start_year = train_features.select(pl.col("year").min()).item()
        end_year = train_features.select(pl.col("year").max()).item()
        print(
            f"Training {profession}: rows={train_features.height}, "
            f"years={start_year}-{end_year}"
        )

        model = LinearRegression()
        model.fit(
            train_features.select("year_index").to_numpy(),
            train_features.get_column("count").to_numpy(),
        )

        model_path = MODELS_DIR / f"{profession}_linear_{DATE_STAMP}.pkl"
        joblib.dump(model, model_path)
        trained_models[profession] = model

    return trained_models
