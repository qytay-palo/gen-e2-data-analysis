from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import polars as pl
import yaml
from dash import dcc, html

from tabs.headcount_over_time import make_tab as make_headcount_tab
from tabs.headcount_over_time import register_callbacks as reg_headcount
from tabs.sector_breakdown import make_tab as make_sector_tab
from tabs.sector_breakdown import register_callbacks as reg_sector


ROOT = Path(__file__).resolve().parents[4]
CFG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yml"
cfg = yaml.safe_load(CFG_PATH.read_text())
PARQUET_PATH = ROOT / cfg["data"]["parquet_path"]


df_polars = pl.scan_parquet(PARQUET_PATH).collect()
df: pd.DataFrame = df_polars.to_pandas()
YEAR_MIN = int(df["year"].min())
YEAR_MAX = int(df["year"].max())
PROFESSIONS = sorted(df["profession"].unique().tolist())


TABS = [
    make_headcount_tab(YEAR_MIN, YEAR_MAX, PROFESSIONS),
    make_sector_tab(YEAR_MIN, YEAR_MAX, PROFESSIONS),
]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = cfg["app"]["title"]


app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2(cfg["app"]["title"], className="text-primary my-3"))),
        dcc.Tabs(id="main-tabs", children=TABS),
    ],
    fluid=True,
    className="p-3",
)


reg_headcount(app, df)
reg_sector(app, df)


if __name__ == "__main__":
    app.run(debug=cfg["app"]["debug"], port=cfg["app"]["port"])
