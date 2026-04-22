# PS-005 — Forecast Dashboard Integration

## Status
Defined

## Description
Add a "5-Year Forecast" tab to the existing PS-002 Dash app by reading the PS-004 model registry and forecast table from disk — no model retraining, no data re-processing. This PS is executed live during Demo 2: the agent wires the tab while the client watches.

## Primary Stakeholder
MOH Workforce Planners (self-service); Team Lead (sign-off)

## Business Question
What does the five-year workforce supply forecast show, and which model drove each profession's projection?

## Success Criteria
1. A new `dcc.Tab` labelled "5-Year Forecast" is appended to the PS-002 app's tab list and the app hot-reloads to show it
2. Tab contains: (a) a line chart per profession showing historical actuals + the five-year forecast horizon present in `forecast_table.csv` with 95% confidence band, (b) a summary table showing champion model type, MAPE, and MAPE target status per profession
3. All data read exclusively from `forecast_table.csv` and `model_registry.csv` — no model objects loaded, no retraining
4. Tab appears within 60 seconds of the agent being invoked (demo latency requirement)
5. Confidence bands displayed where available; graceful fallback label "N/A" where not

## Inputs
- `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv` (from PS-004)
- `artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv` (from PS-004)
- `shared/data/4_processed/workforce_clean.parquet` (for historical actuals overlay)
- `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` (tab list to append to)

## Outputs
- `artifacts/ps-005-forecast-dashboard-integration/src/forecast_tab.py` — tab layout and callbacks
- Modified PS-002 dashboard with 5-Year Forecast tab appended

## Dependencies
- PS-001 (clean Parquet for historical actuals)
- PS-002 (dashboard must be running; tab list must be appendable)
- PS-004 (forecast outputs must exist at documented paths)

## Demo Role
**Demo 2 live story** — called in front of the client to demonstrate on-demand AI-generated forecast integration.

## Technical Notes
- Read CSVs with `pl.read_csv`; convert to pandas only at Plotly boundary
- Tab injection must not require restarting the Dash server — use the same appendable tabs pattern from PS-002/PS-003
- Historical + forecast combined chart: plot actuals as solid line, forecast as dashed line, confidence band as shaded area
- Display annual forecast output exactly as exported by PS-004; do not infer extra periods or demand-side shortage metrics in the dashboard layer
- Module must expose a reusable `build_forecast_tab` function for standalone execution and dashboard integration tests
- No credentials or network calls — all inputs are local files
