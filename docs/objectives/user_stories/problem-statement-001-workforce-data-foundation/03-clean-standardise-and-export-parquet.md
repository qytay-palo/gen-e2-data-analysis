# Story 03: Clean, Standardise, and Export Canonical Parquet

## User Story
As a Data Analyst, I want all four profession files cleaned, standardised, and combined into a single Parquet file, so that every downstream problem statement reads from one trusted dataset with consistent schema.

## Acceptance Criteria
1. Column names normalised to snake_case with canonical names `year`, `sector`, `count`, `profession`
2. `year` and `count` cast to `Int32`; `sector` and `profession` cast to `Categorical`
3. Rows with null `year` or null `count` dropped and count logged; null `sector` filled with `"Unknown"`
4. Whitespace stripped and sector values title-cased
5. Exact duplicate rows removed and count logged
6. `profession` column derived from source filename (e.g. `"doctors"`)
7. Combined clean dataset written to `shared/data/4_processed/workforce_clean.parquet`
8. Cleaning audit written to `artifacts/ps-001-workforce-data-foundation/results/tables/workforce_cleaning_audit.yml` documenting row counts before/after each step per profession
9. Unit tests for cleaning logic pass

## Technical Notes
- All transformation in Polars — no pandas
- Raw files in `shared/data/1_raw/workforce/` remain unchanged
- Write with `pyarrow` engine: `df.write_parquet(..., compression="snappy")`
- Cleaning functions go in `shared/src/data_processing/workforce_cleaning.py`
- Unit tests in `shared/tests/unit/test_workforce_cleaning.py`

## Definition of Done
- `shared/data/4_processed/workforce_clean.parquet` exists and is readable
- `workforce_cleaning_audit.yml` written
- All unit tests pass
- Pipeline runtime < 5 minutes locally

## Story Points
5

## Priority
Must Have

## Dependencies
- Story 02 complete — quality profile informs cleaning rules
