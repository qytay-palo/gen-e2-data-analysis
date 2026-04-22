# Story 01: Extract SharePoint Workforce Files

## User Story
As a Data Engineer, I want to download all four profession CSV files from MOH SharePoint to the local raw landing zone, so that downstream cleaning and validation steps have an immutable local copy to work from.

## Acceptance Criteria
1. All four files (`doctors.csv`, `nurses.csv`, `pharmacists.csv`, `physiotherapists.csv`) are downloaded to `shared/data/1_raw/workforce/`
2. Each file has row count > 0 logged on download
3. Download timestamp is logged per file
4. If a file fails to download, the error is logged and the script exits non-zero — no silent failures
5. Raw files are never modified after download

## Technical Notes
- Use the existing `shared/src/data_processing/sharepoint_connector.py` (`SharePointConnector.extract_folder`)
- Credentials loaded from `.env` via `SharePointSettings.from_env()`
- Log to `artifacts/ps-001-workforce-data-foundation/logs/etl/`
- Use `loguru` — no `print()` statements

## Definition of Done
- All 4 files present in `shared/data/1_raw/workforce/`
- Extraction log written with timestamps and row counts
- Script exits 0 on success, non-zero on any file failure

## Story Points
2

## Priority
Must Have

## Dependencies
None — first story in the pipeline
