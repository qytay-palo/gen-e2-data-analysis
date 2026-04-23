from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import polars as pl
from dash import Input, Output, dcc, html


PROFESSION_COLOURS = {
    "doctors": "#1f77b4",
    "nurses": "#2ca02c",
    "pharmacists": "#ff7f0e",
    "physiotherapists": "#9467bd",
}

GROWTH_PARQUET_PATH = (
    Path(__file__).resolve().parents[5]
    / "artifacts"
    / "ps-003-workforce-growth-analysis"
    / "results"
    / "tables"
    / "growth_rates.parquet"
)

DF_GROWTH = pl.read_parquet(GROWTH_PARQUET_PATH)


def make_tab(professions: list[str]) -> dcc.Tab:
    return dcc.Tab(
        label="Growth Trends",
        children=[
            html.Div(
                [
                    html.Label("Profession filter", className="mt-3"),
                    dcc.Dropdown(
                        id="growth-profession-filter",
                        options=[
                            {"label": profession.title(), "value": profession}
                            for profession in professions
                        ],
                        value=None,
                        multi=True,
                        placeholder="All professions",
                    ),
                    dcc.Graph(id="cagr-chart"),
                    dcc.Graph(id="yoy-chart"),
                ],
                className="p-3",
            )
        ],
    )


def register_callbacks(app, df_growth: pl.DataFrame) -> None:
    @app.callback(
        [Output("cagr-chart", "figure"), Output("yoy-chart", "figure")],
        [Input("growth-profession-filter", "value")],
    )
    def update_growth(selected_professions: list[str] | None):
        filtered = df_growth.filter(pl.col("sector") == "All")
        if selected_professions:
            filtered = filtered.filter(pl.col("profession").is_in(selected_professions))

        cagr_data = (
            filtered.select(["profession", "cagr"])
            .drop_nulls(subset=["cagr"])
            .unique(subset=["profession"], keep="first")
            .sort("cagr", descending=True)
            .to_pandas()
        )
        cagr_data["cagr_pct"] = cagr_data["cagr"] * 100.0

        cagr_fig = px.bar(
            cagr_data,
            x="profession",
            y="cagr_pct",
            color="profession",
            color_discrete_map=PROFESSION_COLOURS,
            title="Compound Annual Growth Rate by Profession",
            labels={
                "profession": "Profession",
                "cagr_pct": "CAGR (%)",
            },
        )
        cagr_fig.update_layout(showlegend=False)

        yoy_data = filtered.select(["profession", "year", "yoy_pct"]).sort(
            ["profession", "year"]
        )
        yoy_data = yoy_data.to_pandas()
        yoy_fig = px.line(
            yoy_data,
            x="year",
            y="yoy_pct",
            color="profession",
            color_discrete_map=PROFESSION_COLOURS,
            markers=True,
            title="Year-on-Year Workforce Growth by Profession",
            labels={
                "year": "Year",
                "yoy_pct": "YoY Growth (%)",
                "profession": "Profession",
            },
        )
        yoy_fig.update_layout(legend_title_text="Profession")

        return cagr_fig, yoy_fig

    return None