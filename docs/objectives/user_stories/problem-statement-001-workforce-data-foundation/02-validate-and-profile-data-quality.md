# Story 02: Validate Schema and Profile Data Quality

## User Story
As a Data Analyst, I want each raw profession file validated for required columns and profiled for data quality issues, so that cleaning decisions in Story 03 are grounded in observed problems rather than assumptions.

## Acceptance Criteria
1. Schema validation confirms all four files contain `year`, `sector`, and `count` (or mappable equivalents); any missing required column raises a logged error and halts the pipeline
2. Quality profile reports null rates, duplicate row counts, negative `count` values, and unique `year` and `sector` values per file
3. Profile written to `artifacts/ps-001-workforce-data-foundation/results/tables/data_quality_report.yml`
4. No file is modified during validation or profiling
5. Validation passes even if column names differ slightly (e.g. `Count`, `Year`) — case-insensitive match attempted before failing

## Technical Notes
- Use Polars for all reads — `pl.read_csv` with `infer_schema_length=0` for initial column inspection
- Quality report is YAML, not CSV — human-readable for audit purposes
- Log all findings to `artifacts/ps-001-workforce-data-foundation/logs/etl/`

## Definition of Done
- `data_quality_report.yml` written with per-file findings
- Schema validation result logged (pass/fail per file)
- No source file modified

## Story Points
3

## Priority
Must Have

## Dependencies
- Story 01 complete — raw files must exist in `shared/data/1_raw/workforce/`
