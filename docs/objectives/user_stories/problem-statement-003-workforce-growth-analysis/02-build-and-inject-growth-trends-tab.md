# Story 02: Build and Inject Growth Trends Tab

## User Story
As a Team Lead demonstrating to a client, I want a Growth Trends tab injected into the running dashboard within 60 seconds of invoking this story, so that the client sees a new analysis appear live without any server restart.

## Acceptance Criteria
1. Growth Trends tab contains: (a) a bar chart of CAGR by profession, (b) a line chart of YoY growth rate over time per profession — both with a profession multi-select filter
2. Tab is appended to the PS-002 dashboard tab list and visible immediately on browser refresh — no server restart required
3. All data read from `artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet` — no recomputation at render time
4. Tab module is importable standalone: `from tabs.growth_trends import build_growth_trends_tab`
5. End-to-end time from story invocation to tab visible on dashboard ≤ 60 seconds

## Technical Notes
- Tab module at `artifacts/ps-003-workforce-growth-analysis/reports/dashboards/tabs/growth_trends.py`
- Injection appends to the same tab list used by PS-002 — requires `workforce_trends_dashboard.py` to expose `app` and `tabs` at module level
- Dash hot-reload or manual browser refresh acceptable for demo
- Convert Polars → pandas only at Plotly boundary

## Definition of Done
- Growth Trends tab renders in the running app
- Profession filter updates both charts
- 60-second latency requirement met in a dry run

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-002 Story 02 complete — dashboard must be running with appendable tab list
- PS-003 Story 01 complete — `growth_rates.parquet` must exist
