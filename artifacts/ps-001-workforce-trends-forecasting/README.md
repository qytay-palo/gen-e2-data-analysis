# PS-001 Workforce Trends Forecasting

Self-contained analysis package for the first Gen-E2 delivery. This package focuses on historical workforce trend extraction and a practical five-year baseline forecast that supports team-lead decision discussions.

## Objectives

- Consolidate in-scope workforce profession files into a common analytical structure.
- Produce reusable interim and processed datasets inside this package.
- Generate trend tables and metrics that can feed later dashboards and narrative outputs.

## Folder Structure

| Folder | Purpose |
|---|---|
| `notebooks/` | Exploratory notebooks for PS-001 |
| `src/` | Problem-specific helpers built on shared modules |
| `data/3_interim/` | Standardized intermediate workforce outputs |
| `data/4_processed/` | Final packaged analysis-ready datasets |
| `results/` | Tables, metrics, and stakeholder exports |
| `reports/` | Figures, dashboard assets, and presentations |
| `models/` | Saved model artifacts when forecasting matures |
| `config/` | Problem-specific configuration |
| `scripts/` | End-to-end orchestration scripts |
| `tests/` | Integration tests for PS-001 |
| `logs/` | PS-specific ETL and error logs |

## How to Run

1. Land raw SharePoint files into `shared/data/1_raw/workforce/`.
2. Run `scripts/load_workforce_data.py` to extract the latest workforce CSV files when credentials are available.
3. Run `artifacts/ps-001-workforce-trends-forecasting/scripts/run_pipeline.py` to standardize the raw files and write interim and processed outputs.
4. Review generated tables under `results/tables/` and `results/metrics/`.
