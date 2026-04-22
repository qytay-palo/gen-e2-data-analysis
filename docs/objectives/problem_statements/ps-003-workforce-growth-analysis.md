# PS-003 — Workforce Growth Rate Analysis

## Status
Defined

## Description
A self-contained analysis module that computes year-on-year (YoY) growth rates and compound annual growth rate (CAGR) by profession and sector from the clean Parquet. The module then appends a third tab "Growth Trends" to the running PS-002 Dash app. This PS is executed live during Demo 1 — the agent generates the analysis and the client watches a new tab appear on the dashboard.

## Primary Stakeholder
Team Lead

## Business Question
Which professions and sectors are growing fastest, and at what compound annual rate?

## Success Criteria
1. `artifacts/ps-003-workforce-growth-analysis/src/growth_analysis.py` computes YoY % change and CAGR per profession and per sector with no hardcoded values
2. Results exported to `artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet`
3. A new `dcc.Tab` labelled "Growth Trends" is appended to the PS-002 app's tab list and the app hot-reloads to show it
4. Growth Trends tab contains: (a) a bar chart of CAGR by profession, (b) a line chart of YoY growth rate over time per profession, both with profession filter
5. Analysis completes and tab appears within 60 seconds of the agent being invoked (demo latency requirement)

## Inputs
- `shared/data/4_processed/workforce_clean.parquet` (from PS-001)
- `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` (tab list to append to)

## Outputs
- `artifacts/ps-003-workforce-growth-analysis/src/growth_analysis.py`
- `artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet`
- Modified PS-002 dashboard with Growth Trends tab appended

## Dependencies
- PS-001 (clean Parquet must exist)
- PS-002 (dashboard must be running; tab list must be appendable)

## Demo Role
**Demo 1 live story** — called in front of the client to demonstrate on-demand AI-generated analysis.

## Technical Notes
- YoY growth = `(count_year_n - count_year_n_minus_1) / count_year_n_minus_1 * 100`
- CAGR = `(count_final / count_initial) ^ (1 / n_years) - 1`
- Growth calculations are annual because the validated cross-file analytical grain is `year`, not month or facility
- All computation in Polars; convert to pandas only at Plotly boundary
- Tab injection must not require restarting the Dash server — use the appendable tabs pattern from PS-002
- Module must expose a reusable `compute_growth_rates` function for standalone execution and dashboard integration tests
