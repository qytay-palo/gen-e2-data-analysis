# Story 01: Build Dashboard App with Headcount Over Time Tab

## User Story
As a Workforce Planner, I want a running Dash app with a Headcount Over Time tab, so that I can interactively explore how total headcount has changed per profession across years.

## Acceptance Criteria
1. App starts with `python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` and serves on `http://localhost:8050`
2. App reads data from `shared/data/4_processed/workforce_clean.parquet` — path configured in `artifacts/ps-002-workforce-trends-dashboard/config/config.yml`
3. Tab 1 "Headcount Over Time" displays a line chart with one line per profession
4. Year-range slider and profession multi-select filter both update the chart immediately on change
5. Tab list is a Python `list` that additional tabs (PS-003, PS-005) can `append()` to without modifying core app bootstrap logic
6. App loads and first render completes in under 3 seconds locally

## Technical Notes
- Dash 4.1.0 + Plotly 6.7.0 — use current APIs
- Data loaded once at startup; convert Polars → pandas only at the Plotly boundary
- Tab modules live in `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/tabs/`; imported and appended to the tab list in the main app file
- `config.yml` holds: `data.parquet_path`, `app.port`, `app.debug`

## Definition of Done
- App starts without errors
- Headcount Over Time tab renders with correct data
- `curl http://localhost:8050` returns HTTP 200
- Tab list is externally appendable

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-001 Story 03 complete — `workforce_clean.parquet` must exist
