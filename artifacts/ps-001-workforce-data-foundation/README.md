# PS-001 Workforce Data Foundation

## Folder Structure

| Folder | Purpose |
|---|---|
| `notebooks/` | Reproducible extraction, validation, and cleaning notebooks for the PS-001 workforce pipeline |
| `scripts/` | PS-001 extraction, validation, and cleaning entry points |
| `logs/etl/` | Extraction, validation, and cleaning logs written by the PS-001 scripts |
| `data/3_interim/` | Reserved for intermediate PS-001 artifacts and staged outputs |
| `data/4_processed/` | Reserved for PS-local processed data mirrors when needed |
| `results/tables/` | Validation reports, cleaning audit output, and exploratory-analysis summary tables |
| `reports/` | Figures, dashboards, and presentation-ready PS-001 outputs, including EDA trend charts |
| `tests/` | PS-specific integration tests for the workforce data foundation workflow |

## How to Run

1. Activate the virtual environment: `source .venv/bin/activate`
2. Run the extractor: `python artifacts/ps-001-workforce-data-foundation/scripts/extract_workforce_data.py`
3. Run the validator: `python artifacts/ps-001-workforce-data-foundation/scripts/validate_workforce_data.py`
4. Run the cleaner: `python artifacts/ps-001-workforce-data-foundation/scripts/clean_workforce_data.py`
5. Run the shared unit tests for cleaning logic: `pytest shared/tests/unit/test_workforce_cleaning.py`
6. Open and run `artifacts/ps-001-workforce-data-foundation/notebooks/01_extract_workforce_data.ipynb` to verify landed files and row counts
7. Open and run `artifacts/ps-001-workforce-data-foundation/notebooks/02_validate_workforce_data.ipynb` to review per-file schema and quality findings
8. Open and run `artifacts/ps-001-workforce-data-foundation/notebooks/03_clean_workforce_data.ipynb` to review the canonical Parquet export, audit, and handoff outputs
9. Open and run `artifacts/ps-001-workforce-data-foundation/notebooks/04_exploratory_analysis.ipynb` to generate the PS-001 EDA figures, summary statistics CSV, findings YAML, and narrative handoff JSON