# Story 01: Build and Inject Forecast Tab

## User Story
As a Team Lead demonstrating to a client, I want a 5-Year Forecast tab injected into the running dashboard within 60 seconds of invoking this story, so that the client sees forecast results appear live without any model retraining or server restart.

## Acceptance Criteria
1. Forecast tab reads exclusively from two files on disk — no model loading, no retraining, no network calls:
   - `artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv`
   - `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv`
   - Historical actuals from `shared/data/4_processed/workforce_clean.parquet`
2. Tab contains:
   - Line chart per profession: solid line for historical actuals, dashed line for forecast, shaded 95% confidence band where available
   - Summary table showing champion model type, MAPE, and MAPE target status per profession
3. Tab is appended to the PS-002 dashboard tab list — visible on browser refresh with no server restart
4. Tab module importable standalone: `from tabs.forecast import build_forecast_tab`
5. End-to-end time from story invocation to tab visible on dashboard ≤ 60 seconds

## Technical Notes
- Tab module at `artifacts/ps-005-forecast-dashboard-integration/src/tabs/forecast.py`
- Injection appends to the same tab list used by PS-002/PS-003
- If `lower_95`/`upper_95` are null for a profession, omit the confidence band gracefully — do not error
- Convert Polars/pandas → Plotly only at chart boundary
- Dash 4.1.0 + Plotly 6.7.0

## Definition of Done
- Forecast tab renders in the running app with actuals + forecast line
- Model registry summary table populated correctly
- 60-second latency requirement met in a dry run
- No model files loaded, no retraining triggered

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-002 Story 02 complete — dashboard running with appendable tab list
- PS-004 Story 03 complete — `model_registry.csv` and `forecast_table.csv` must exist at contract paths
