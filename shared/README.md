# Shared Infrastructure

Reusable code, raw data landing zones, schemas, SQL assets, tests, and configuration that can be shared across multiple problem statements.

## Folder Structure

| Folder | Purpose |
|---|---|
| `src/` | Reusable Python modules for ingestion, validation, analysis, and visualization |
| `data/1_raw/` | Immutable source extracts copied from approved systems |
| `data/2_external/` | Reference datasets and benchmarks |
| `data/schemas/` | Schema notes and contracts for landed datasets |
| `sql/` | Reusable SQL views, extractions, and procedures |
| `tests/` | Unit tests for shared code |
| `config/` | Shared YAML configuration for local and platform execution |

## How to Use

1. Put reusable ingestion code under `shared/src/data_processing/`.
2. Keep raw source files under `shared/data/1_raw/` and never edit them in place.
3. Save shared schema notes under `shared/data/schemas/`.
4. Import shared helpers from problem-specific code rather than copying logic.

## Current Shared Assets

- SharePoint workforce connector in `shared/src/data_processing/sharepoint_connector.py`
- YAML config loader in `shared/src/utils/config.py`
- Base platform configs in `shared/config/`
