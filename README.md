# Gen-E2 Workforce Trends Analysis

This repository is initialized for a Gen-E2 data analysis project focused on extracting workforce trends and producing a practical five-year forecasting baseline for the Ministry of Health team lead.

## Project overview

The current delivery focus is:

- analyze historical healthcare workforce trends
- build reusable shared ingestion and validation utilities
- prepare a self-contained problem package for workforce trend forecasting
- stay local-first while remaining compatible with HEALIX/Databricks and MCDR/CDSW

## Technical environment

- Current decision: hybrid / local-first
- Preferred scaled target: HEALIX/Databricks
- Secondary fallback target: MCDR/CDSW
- Local development: `uv` + `.venv`
- Primary data processing library: Polars
- Primary external source: MOH SharePoint / DataDojo workforce folder

## Repository structure

```text
.
├── artifacts/
│   └── ps-001-workforce-trends-forecasting/
│       ├── notebooks/
│       ├── src/
│       ├── data/
│       │   ├── 3_interim/
│       │   └── 4_processed/
│       ├── results/
│       ├── reports/
│       ├── models/
│       ├── config/
│       ├── scripts/
│       ├── tests/
│       └── logs/
├── docs/
│   ├── index.md
│   ├── project-context/
│   └── data_dictionary/
├── shared/
│   ├── src/
│   ├── data/
│   ├── sql/
│   ├── tests/
│   └── config/
├── scripts/
├── logs/
├── requirements.txt
├── pyproject.toml
└── TODO.md
```

## Shared vs problem-specific layout

- `shared/` contains reusable connectors, config, tests, schemas, and immutable raw data.
- `artifacts/ps-001-workforce-trends-forecasting/` contains the self-contained analysis package for the current problem statement.
- Raw source data should be written to `shared/data/1_raw/` and not modified in place.
- Processed outputs, forecasts, and stakeholder-ready results should live inside the relevant problem package.

## Stakeholders and success criteria

- Primary stakeholder: team lead
- Decision supported: interpretation of historical workforce trends
- Good-enough first delivery: a transparent five-year forecast baseline plus reusable outputs for later reporting

## Environment setup

1. Create the virtual environment:
   - `uv venv .venv`
2. Activate it:
   - `source .venv/bin/activate`
3. Install dependencies:
   - `uv pip install -r requirements.txt`
4. Optional dev tooling:
   - `uv pip install -e .`

## Data access

The project expects SharePoint credentials in `.env`.
Use `.env.example` as the template.

Primary source folder:

- `/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/`

## Main workflows

- Project navigation: see `docs/index.md`
- Shared extraction script: `scripts/load_workforce_data.py`
- Problem package orchestrator: `artifacts/ps-001-workforce-trends-forecasting/scripts/run_pipeline.py`

## Code quality

- formatting and linting: Ruff
- testing: Pytest
- logging: Loguru
- configuration: YAML + environment variables

## Notes

- SharePoint extraction requires valid credentials and network access.
- No transcript files were found, so transcript analysis was skipped during initialization.
