from __future__ import annotations

import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html


PROFESSION_COLOURS = {
    "doctors": "#1f77b4",
    "nurses": "#2ca02c",
    "pharmacists": "#ff7f0e",
    "physiotherapists": "#9467bd",
}


def make_tab(year_min: int, year_max: int, professions: list[str]) -> dcc.Tab:
    return dcc.Tab(
        label="Headcount Over Time",
        children=[
            html.Div(
                [
                    dcc.Graph(id="headcount-chart"),
                    html.Label("Year range", className="mt-3"),
                    dcc.RangeSlider(
                        id="headcount-year-slider",
                        min=year_min,
                        max=year_max,
                        step=1,
                        value=[year_min, year_max],
                        marks={
                            year: str(year) for year in range(year_min, year_max + 1)
                        },
                    ),
                    html.Label("Profession filter", className="mt-4"),
                    dcc.Dropdown(
                        id="headcount-profession-filter",
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
        Output("headcount-chart", "figure"),
        [
            Input("headcount-year-slider", "value"),
            Input("headcount-profession-filter", "value"),
        ],
    )
    def update_headcount(year_range: list[int], selected_professions: list[str]):
        filtered = df_pandas.copy()
        if year_range:
            filtered = filtered[
                (filtered["year"] >= year_range[0])
                & (filtered["year"] <= year_range[1])
            ]
        if selected_professions:
            filtered = filtered[filtered["profession"].isin(selected_professions)]

        agg = filtered.groupby(["year", "profession"], as_index=False)["count"].sum()
        fig = px.line(
            agg,
            x="year",
            y="count",
            color="profession",
            color_discrete_map=PROFESSION_COLOURS,
            title="Healthcare Workforce Headcount Over Time",
            labels={"count": "Headcount", "year": "Year", "profession": "Profession"},
        )
        fig.update_layout(legend_title_text="Profession")
        return fig

    return None
