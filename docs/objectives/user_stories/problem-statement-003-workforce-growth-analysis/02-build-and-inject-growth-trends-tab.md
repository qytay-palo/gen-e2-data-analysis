# Story 02: Build and Inject Growth Trends Tab

## User Story
As a Team Lead demonstrating to a client, I want a Growth Trends tab to appear in the running dashboard automatically when the PS-003 executor pipeline completes — no further command required — so that the client sees AI-generated analysis materialise live without any manual step.

## Acceptance Criteria
1. Growth Trends tab contains: (a) a bar chart of CAGR by profession, (b) a line chart of YoY growth rate over time per profession — both with a profession multi-select filter
2. The PS-003 executor pipeline (single invocation) automatically writes the tab module AND patches `workforce_trends_dashboard.py` to import and append it — no separate injection step or command
3. Dash hot-reload detects the patched app file and reloads within ~3 seconds — tab appears on browser refresh with no server restart
4. All data read from `artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet` — no recomputation at render time
5. Tab module is importable standalone: `from tabs.growth_trends import build_growth_trends_tab`
6. End-to-end time from executor invocation to tab visible on dashboard ≤ 60 seconds

## Technical Notes
- Tab module written to `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/tabs/growth_trends.py`
- `workforce_trends_dashboard.py` is patched (appended) to add the import and `TABS.append(...)` call — the patch is idempotent (safe to run twice)
- PS-002 runs with `debug: true` (hot-reload enabled) — this is a hard prerequisite
- Convert Polars → pandas only at Plotly boundary

## Definition of Done
- Single executor invocation → tab visible in running app with no further steps
- Profession filter updates both charts
- 60-second latency requirement met in a dry run

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-002 Story 02 complete — dashboard must be running with appendable tab list
- PS-003 Story 01 complete — `growth_rates.parquet` must exist
