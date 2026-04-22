# PS-002 — Workforce Trends Dashboard

## Status
Defined

## Description
Build an interactive Plotly Dash web application with two pre-built tabs that let MOH workforce planners explore historical headcount trends without any manual steps. The app reads from the canonical clean Parquet produced by PS-001. This is the opening state shown to the client at the start of Demo 1 and Demo 2.

## Primary Stakeholder
MOH Workforce Planners (self-service); Team Lead (sign-off)

## Business Question
How has healthcare workforce headcount changed over time across professions and sectors?

## Success Criteria
1. Dash app starts with `python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` and serves on `http://localhost:8050`
2. Tab 1 "Headcount Over Time" — line chart with one line per profession, year-range slider, profession multi-select filter
3. Tab 2 "Sector Breakdown" — stacked bar chart by sector and profession, year-range slider, profession multi-select filter
4. All charts update instantly on filter change (no page reload)
5. App tab list is designed to accept additional tabs appended at runtime (required for PS-003 and PS-005)
6. App loads and renders in under 3 seconds on local machine

## Inputs
- `shared/data/4_processed/workforce_clean.parquet` (from PS-001)

## Outputs
- `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` — runnable Dash app
- `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/tabs/` — one module per tab for clean separation

## Dependencies
- PS-001 must be complete and `workforce_clean.parquet` must exist

## Demo Role
**Demo 1 opening state** — shown to client before any live generation.
**Demo 2 opening state** — also the base app that PS-005 extends.

## Technical Notes
- Tabs must be stored in a list so PS-003 and PS-005 can `append()` a new `dcc.Tab` without modifying core app logic
- Use `pl.scan_parquet` to read data; convert to pandas only if Dash callback requires it
- Plotly Express for charts; consistent MOH colour palette across tabs
- No hardcoded file paths — read path from `config/config.yml`
