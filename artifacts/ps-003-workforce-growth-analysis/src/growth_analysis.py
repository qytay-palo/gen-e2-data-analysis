from __future__ import annotations

from pathlib import Path

import polars as pl
from loguru import logger


ROOT = Path(__file__).resolve().parents[3]
INPUT_PATH = ROOT / "shared/data/4_processed/workforce_clean.parquet"
OUTPUT_PATH = (
    ROOT
    / "artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet"
)
GROUP_KEYS = ["profession", "sector"]
REQUIRED_COLUMNS = {"year", "sector", "count", "profession"}


def _prepare_aggregate(df: pl.DataFrame) -> pl.DataFrame:
    by_profession_and_sector = (
        df.group_by(["profession", "sector", "year"])
        .agg(pl.col("count").sum().alias("count"))
        .sort(["profession", "sector", "year"])
    )

    by_profession = (
        df.group_by(["profession", "year"])
        .agg(pl.col("count").sum().alias("count"))
        .with_columns(pl.lit("All").alias("sector"))
        .select(["profession", "sector", "year", "count"])
        .sort(["profession", "sector", "year"])
    )

    return pl.concat([by_profession, by_profession_and_sector], how="vertical")


def _log_groups_without_cagr(aggregated: pl.DataFrame) -> None:
    insufficient_groups = (
        aggregated.group_by(GROUP_KEYS)
        .agg(pl.len().alias("n_points"))
        .filter(pl.col("n_points") < 2)
        .sort(GROUP_KEYS)
    )

    for row in insufficient_groups.iter_rows(named=True):
        logger.warning(
            "Skipping CAGR for profession='{profession}', sector='{sector}' due to only {n_points} data point(s)",
            profession=row["profession"],
            sector=row["sector"],
            n_points=row["n_points"],
        )


def compute_growth_rates(df: pl.DataFrame) -> pl.DataFrame:
    """Compute YoY growth percent and CAGR by profession and profession-sector."""
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input data is missing required columns: {missing}")

    aggregated = _prepare_aggregate(
        df.select(["profession", "sector", "year", "count"]).with_columns(
            [
                pl.col("profession").cast(pl.Utf8),
                pl.col("sector").cast(pl.Utf8),
                pl.col("year").cast(pl.Int32),
                pl.col("count").cast(pl.Float64),
            ]
        )
    )
    _log_groups_without_cagr(aggregated)

    growth_with_yoy = (
        aggregated.with_columns(
            pl.col("count").shift(1).over(GROUP_KEYS).alias("previous_count")
        )
        .with_columns(
            pl.when(pl.col("previous_count").is_null() | (pl.col("previous_count") == 0))
            .then(None)
            .otherwise(
                ((pl.col("count") - pl.col("previous_count")) / pl.col("previous_count"))
                * 100.0
            )
            .alias("yoy_pct")
        )
    )

    cagr_by_group = (
        aggregated.group_by(GROUP_KEYS)
        .agg(
            [
                pl.len().alias("n_points"),
                pl.col("year").min().alias("year_start"),
                pl.col("year").max().alias("year_end"),
                pl.col("count").sort_by("year").first().alias("count_start"),
                pl.col("count").sort_by("year").last().alias("count_end"),
            ]
        )
        .with_columns((pl.col("year_end") - pl.col("year_start")).alias("n_years"))
        .with_columns(
            pl.when(
                (pl.col("n_points") < 2)
                | (pl.col("n_years") <= 0)
                | (pl.col("count_start") <= 0)
                | (pl.col("count_end") < 0)
            )
            .then(None)
            .otherwise(
                (
                    (pl.col("count_end") / pl.col("count_start"))
                    ** (1.0 / pl.col("n_years"))
                )
                - 1.0
            )
            .alias("cagr")
        )
        .select(GROUP_KEYS + ["cagr"])
    )

    return (
        growth_with_yoy.join(cagr_by_group, on=GROUP_KEYS, how="left")
        .select(["profession", "sector", "year", "yoy_pct", "cagr"])
        .sort(["profession", "sector", "year"])
    )


def write_growth_rates(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
) -> Path:
    """Load the clean workforce parquet, compute growth metrics, and persist them."""
    df = pl.read_parquet(input_path)
    growth_rates = compute_growth_rates(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    growth_rates.write_parquet(output_path)
    logger.info("Wrote growth rates to {path}", path=output_path)
    return output_path


if __name__ == "__main__":
    write_growth_rates()