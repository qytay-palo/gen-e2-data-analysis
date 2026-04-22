# Story 01: Compute Growth Rates and Export

## User Story
As a Data Analyst, I want year-on-year growth rates and CAGR computed per profession and sector, so that the Growth Trends tab has analysis-ready data to visualise without recalculating on every render.

## Acceptance Criteria
1. Year-on-year growth rate computed per profession per year: `(count_n - count_n-1) / count_n-1 * 100`
2. CAGR computed per profession over the full available time range: `(count_final / count_initial) ^ (1 / n_years) - 1`
3. Both metrics also computed at profession × sector level
4. Results exported to `artifacts/ps-003-workforce-growth-analysis/results/tables/growth_rates.parquet`
5. Professions or sectors with fewer than 2 data points are excluded from CAGR with a logged warning
6. Unit tests cover the growth rate and CAGR formulas

## Technical Notes
- All computation in Polars — no pandas
- Input: `shared/data/4_processed/workforce_clean.parquet`
- Output schema: `profession, sector, year, yoy_pct, cagr` (nulls allowed in `yoy_pct` for first year)
- Functions in `artifacts/ps-003-workforce-growth-analysis/src/growth_analysis.py`

## Definition of Done
- `growth_rates.parquet` written and readable
- Unit tests pass for both metrics
- Edge cases (single year, zero count) handled without errors

## Story Points
3

## Priority
Must Have

## Dependencies
- PS-001 Story 03 complete — `workforce_clean.parquet` must exist
