# PS-001 — Workforce Data Foundation

## Status
Defined

## Description
Extract the four profession CSV files (doctors, nurses, pharmacists, physiotherapists) from the MOH SharePoint workforce folder, validate schema and data quality, clean and standardise all four files into a single combined analysis-ready Parquet file. This PS creates the local landing zone under `shared/data/1_raw/workforce/` if it does not yet exist and establishes the data contract that every downstream problem statement depends on.

## Primary Stakeholder
Team Lead

## Business Question
Do we have a single trusted, auditable dataset of historical healthcare workforce headcount that can be safely used for trend analysis and forecasting?

## Success Criteria
1. All four profession CSV files downloaded to `shared/data/1_raw/workforce/` with timestamps logged
2. Schema validation passes for all four files (required columns: `year`, `sector`, `count`)
3. Cleaning audit written to `artifacts/ps-001-workforce-data-foundation/results/tables/workforce_cleaning_audit.yml` documenting every row dropped or imputed
4. Combined clean dataset written to `shared/data/4_processed/workforce_clean.parquet` with `profession` column and consistent dtypes (`year: Int32`, `count: Int32`, `sector: Categorical`, `profession: Categorical`)
5. Unit tests pass for cleaning logic; pipeline completes in under 5 minutes locally

## Inputs
- SharePoint workforce folder: `/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/`
- `shared/data/1_raw/workforce/doctors.csv`
- `shared/data/1_raw/workforce/nurses.csv`
- `shared/data/1_raw/workforce/pharmacists.csv`
- `shared/data/1_raw/workforce/physiotherapists.csv`

## Outputs
- `shared/data/4_processed/workforce_clean.parquet` ← **shared contract for all downstream PSes**
- `artifacts/ps-001-workforce-data-foundation/results/tables/workforce_cleaning_audit.yml`
- `artifacts/ps-001-workforce-data-foundation/logs/etl/` — extraction and cleaning run logs

## Dependencies
None — this is the root PS.

## Demo Role
Prerequisite. Must be executed before any demo.

## Technical Notes
- Use `shared/src/data_processing/sharepoint_connector.py` for extraction
- Use Polars for all transformations; no pandas
- This PS is the only problem statement that requires SharePoint credentials; all downstream PSes run from local files written by this PS
- Null `year` or `count` rows must be dropped (not imputed); null `sector` filled with `"Unknown"`
- Exact duplicate rows removed and logged
- Raw files in `shared/data/1_raw/` are immutable — never modified in place
