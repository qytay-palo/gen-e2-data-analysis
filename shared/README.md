# Shared Infrastructure

Reusable code, raw data landing zones, schemas, SQL assets, tests, and configuration that can be shared across multiple problem statements.

## Folder Structure

| Folder | Purpose |
|---|---|
| `src/` | Reusable Python modules for ingestion, validation, analysis, and visualization |
| `data/1_raw/` | Immutable source extracts copied from approved systems |
| `data/4_processed/` | Canonical processed datasets shared across downstream problem statements |
| `data/2_external/` | Reference datasets and benchmarks |
| `data/schemas/` | Schema notes and contracts for landed datasets |
| `sql/` | Reusable SQL views, extractions, and procedures |
| `tests/` | Unit tests for shared code |
| `config/` | Shared YAML configuration for local and platform execution |

## How to Run

1. Activate the virtual environment: `source .venv/bin/activate`
2. Keep raw source files under `shared/data/1_raw/` and never edit them in place.
3. Run problem-specific scripts that import shared helpers, such as `python artifacts/ps-001-workforce-data-foundation/scripts/clean_workforce_data.py`
4. Run shared unit tests with `pytest shared/tests/unit/` or the narrower target you are changing.
5. Add reusable ingestion, validation, and cleaning modules under `shared/src/data_processing/`
6. For PS-001 downstream validation and reporting, run `artifacts/ps-001-workforce-data-foundation/notebooks/04_exploratory_analysis.ipynb` against `shared/data/4_processed/workforce_clean.parquet`

## Current Shared Assets

- SharePoint workforce connector in `shared/src/data_processing/sharepoint_connector.py`
- Workforce schema validator in `shared/src/data_processing/workforce_validation.py`
- Workforce cleaning module in `shared/src/data_processing/workforce_cleaning.py`
- Raw workforce landing zone in `shared/data/1_raw/workforce/`
- Canonical workforce Parquet in `shared/data/4_processed/workforce_clean.parquet`
- PS-001 exploratory notebook consuming the canonical workforce Parquet in `artifacts/ps-001-workforce-data-foundation/notebooks/04_exploratory_analysis.ipynb`
- YAML config loader in `shared/src/utils/config.py`
- Base platform configs in `shared/config/`
