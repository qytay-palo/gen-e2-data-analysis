from __future__ import annotations

import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html


def make_tab(year_min: int, year_max: int, professions: list[str]) -> dcc.Tab:
    return dcc.Tab(
        label="Sector Breakdown",
        children=[
            html.Div(
                [
                    dcc.Graph(id="sector-chart"),
                    html.Label("Year range", className="mt-3"),
                    dcc.RangeSlider(
                        id="sector-year-slider",
                        min=year_min,
                        max=year_max,
                        step=1,
                        value=[year_min, year_max],
                        marks={year: str(year) for year in range(year_min, year_max + 1)},
                    ),
                    html.Label("Profession filter", className="mt-4"),
                    dcc.Dropdown(
                        id="sector-profession-filter",
                        options=[
                            {"label": profession.title(), "value": profession}
                            for profession in professions
                        ],
                        value=professions,
                        multi=True,
                    ),
                ],
                className="p-3",
            )
        ],
    )


def register_callbacks(app, df_pandas: pd.DataFrame) -> None:
    @app.callback(
        Output("sector-chart", "figure"),
        [
            Input("sector-year-slider", "value"),
            Input("sector-profession-filter", "value"),
        ],
    )
    def update_sector(year_range: list[int], selected_professions: list[str]):
        filtered = df_pandas.copy()
        if year_range:
            filtered = filtered[
                (filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])
            ]
        if selected_professions:
            filtered = filtered[filtered["profession"].isin(selected_professions)]

        agg = filtered.groupby(["profession", "sector"], as_index=False)["count"].sum()
        fig = px.bar(
            agg,
            x="profession",
            y="count",
            color="sector",
            barmode="stack",
            title="Workforce Headcount by Profession and Sector",
            labels={"count": "Headcount", "profession": "Profession", "sector": "Sector"},
        )
        fig.update_layout(legend_title_text="Sector")
        return fig

    return None