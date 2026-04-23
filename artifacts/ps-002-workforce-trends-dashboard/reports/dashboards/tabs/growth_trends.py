from __future__ import annotations

from pathlib import Path

import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
from dash import Input, Output, dcc, html


ROOT = Path(__file__).resolve().parents[5]
GROWTH_RATES_PATH = (
    ROOT
    / "artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet"
)
CARD_STYLE = {
    "backgroundColor": "#FFFFFF",
    "borderRadius": "14px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "padding": "22px",
    "minHeight": "100%",
}


def _load_growth_data() -> tuple[pl.DataFrame, list[str]]:
    growth_df = (
        pl.read_parquet(GROWTH_RATES_PATH)
        .filter(pl.col("sector") == "All")
        .sort(["profession", "year"])
    )
    professions = sorted(growth_df["profession"].unique().to_list())
    return growth_df, professions


def _filter_growth_data(
    growth_df: pl.DataFrame,
    selected_professions: list[str] | None,
) -> pl.DataFrame:
    if selected_professions:
        return growth_df.filter(pl.col("profession").is_in(selected_professions))
    return growth_df


def _build_cagr_chart(filtered_df: pl.DataFrame):
    cagr_df = (
        filtered_df.group_by("profession")
        .agg(pl.col("cagr").drop_nulls().first().alias("cagr"))
        .drop_nulls("cagr")
        .with_columns(pl.col("profession").str.to_titlecase().alias("profession_label"))
        .sort("cagr", descending=True)
    )

    title = "Compound growth has been strongest in the leading selected profession"
    if cagr_df.height:
        top_profession = cagr_df.item(0, "profession_label")
        title = f"{top_profession} shows the strongest compound growth across the full period"

    fig = px.bar(
        cagr_df.to_pandas(),
        x="profession_label",
        y="cagr",
        color="profession_label",
        title=title,
        labels={
            "profession_label": "Profession",
            "cagr": "CAGR",
        },
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin={"l": 20, "r": 20, "t": 72, "b": 20},
    )
    fig.update_yaxes(tickformat=".1%")
    fig.update_traces(
        hovertemplate="Profession=%{x}<br>CAGR=%{y:.1%}<extra></extra>",
    )
    return fig


def _build_yoy_chart(filtered_df: pl.DataFrame):
    yoy_df = filtered_df.drop_nulls("yoy_pct").with_columns(
        pl.col("profession").str.to_titlecase().alias("profession_label")
    )

    fig = px.line(
        yoy_df.to_pandas(),
        x="year",
        y="yoy_pct",
        color="profession_label",
        markers=True,
        title="Growth momentum varies across professions from year to year",
        labels={
            "year": "Year",
            "yoy_pct": "YoY growth rate",
            "profession_label": "Profession",
        },
    )
    fig.update_layout(
        legend_title_text="Profession",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin={"l": 20, "r": 20, "t": 72, "b": 20},
    )
    fig.update_yaxes(ticksuffix="%")
    fig.update_traces(
        hovertemplate="Profession=%{fullData.name}<br>Year=%{x}<br>YoY=%{y:.1f}%<extra></extra>",
    )
    return fig


def build_growth_trends_tab(app) -> dcc.Tab:
    growth_df, professions = _load_growth_data()

    @app.callback(
        Output("growth-cagr-chart", "figure"),
        Output("growth-yoy-chart", "figure"),
        Input("growth-profession-filter", "value"),
    )
    def update_growth_charts(selected_professions: list[str] | None):
        filtered_df = _filter_growth_data(growth_df, selected_professions)
        return _build_cagr_chart(filtered_df), _build_yoy_chart(filtered_df)

    return dcc.Tab(
        label="Growth Trends",
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Priority 1", style={"color": "#C2410C", "fontWeight": 700}),
                            html.P(
                                "Problem statement: identify which professions are growing fastest and at what compound annual rate.",
                                className="mb-2",
                            ),
                            html.H3(
                                "Workforce growth rates diverge sharply across professions.",
                                className="mb-2",
                            ),
                            html.P(
                                "Use CAGR to rank sustained expansion and YoY change to spot where momentum accelerated or softened.",
                                className="text-muted mb-0",
                            ),
                        ],
                        style=CARD_STYLE,
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            html.Label("Profession filter", className="fw-semibold"),
                            dcc.Dropdown(
                                id="growth-profession-filter",
                                options=[
                                    {"label": profession.title(), "value": profession}
                                    for profession in professions
                                ],
                                value=professions,
                                multi=True,
                                placeholder="Select one or more professions",
                            ),
                        ],
                        style=CARD_STYLE,
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(id="growth-cagr-chart", config={"displayModeBar": False}),
                                    style=CARD_STYLE,
                                ),
                                lg=4,
                                md=12,
                                className="mb-3",
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(id="growth-yoy-chart", config={"displayModeBar": False}),
                                    style=CARD_STYLE,
                                ),
                                lg=8,
                                md=12,
                                className="mb-3",
                            ),
                        ],
                        className="g-3",
                    ),
                    html.Div(
                        [
                            html.H5("Insight and action", className="mb-2"),
                            html.P(
                                "Sustained leaders in the CAGR chart are the strongest candidates for capacity planning, while abrupt YoY swings highlight professions that may need closer workforce monitoring.",
                                className="mb-0",
                            ),
                        ],
                        style=CARD_STYLE,
                    ),
                ],
                className="p-3",
                style={"backgroundColor": "#F4F6F8"},
            )
        ],
    )