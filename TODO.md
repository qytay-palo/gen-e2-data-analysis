# TODO — Singapore Infectious Disease Analysis (MOH)

## Phase 0 — Project Setup
- [x] Create project folder structure (hybrid shared + problem-statements)
- [x] Create `requirements.txt` with Polars, Prophet, scikit-learn, Kaggle API
- [x] Create `.env.example` with Kaggle and Databricks credentials template
- [x] Create `shared/config/base.yml` and `shared/config/databricks.yml`
- [x] Create `shared/src/data_processing/kaggle_connector.py`
- [x] Create data dictionary skeleton in `docs/data_dictionary/`
- [ ] Copy `.env.example` → `.env` and fill in real credentials (developer)
- [ ] Create and activate Python virtual environment: `uv venv .venv`
- [ ] Install dependencies: `uv pip install -r requirements.txt`
- [ ] Verify Kaggle connection: `connector.test_connection()`

## Phase 1 — Problem Statement Identification
- [ ] Run `/1-identify-problem-statement` to generate `docs/objectives/problem_statements/` files
- [ ] Review and approve generated problem statements (MOH Internal Committee)
- [ ] Prioritise problem statements for sprint planning

## Phase 2 — Data Extraction & Validation
- [ ] Identify correct Kaggle dataset slug for Singapore infectious disease data
- [ ] Run data-extractor agent to download raw data to `shared/data/1_raw/`
- [ ] Run data-validation agent — validate schema, nulls, date formats, value ranges
- [ ] Update `docs/data_dictionary/01-infectious-diseases-kaggle.md` with actual schema
- [ ] Verify raw data immutability (no modifications to `1_raw/`)

## Phase 3 — Data Cleaning & EDA
- [ ] Run data-cleaning agent — handle missing values, duplicates, type coercion
- [ ] Run exploratory-analysis agent — univariate + multivariate, seasonality patterns
- [ ] Review EDA outputs with MOH Epidemiology stakeholders
- [ ] Document COVID-19 anomaly period (2020–2022) for exclusion from baselines

## Phase 4 — Feature Engineering & Modelling
- [ ] Run feature-engineer agent — seasonal features, lag features, rolling averages
- [ ] Select forecasting models: Prophet (seasonality), ARIMA/SARIMA (statsmodels), ensemble
- [ ] Run model-forecasting agent — train, evaluate, compare models per disease
- [ ] Validate forecast accuracy (MAE, MAPE) against holdout set (last 12 months)

## Phase 5 — Visualisation & Dashboards
- [ ] Run dashboard-visualization agent — build interactive HTML dashboard
- [ ] Dashboard must answer:
  - [ ] Which diseases show strong seasonality?
  - [ ] Predicted high-risk periods for Dengue, HFMD, influenza-like illnesses
  - [ ] Top disease burden contributors (case volume, growth rate, outbreak frequency)
  - [ ] Resource allocation recommendations
- [ ] Review dashboard with MOH stakeholders (Minister of Health + Internal Committee)

## Phase 6 — Code Quality Gate
- [ ] Run code-simplifier agent on all notebooks and scripts
- [ ] Run jupyter-notebook-reviewer agent — execute all notebooks, fix errors
- [ ] Run code-reviewer agent — review for bugs, security issues, logic errors
- [ ] Achieve >80% pytest coverage on `shared/src/` critical modules

## Documentation & Governance
- [ ] Update `README.md` with final project outcomes and usage instructions
- [ ] Update `docs/data_dictionary/` with final validated schemas
- [ ] Review `.gitignore` — ensure `.env`, `1_raw/`, model artifacts, logs are excluded
- [ ] Ensure no secrets committed to version control
- [ ] Archive final problem-statement folders as shareable packages

## DevOps / Infrastructure
- [ ] Set up Databricks workspace paths (`/Workspace/Users/moh-analytics/`)
- [ ] Configure DBFS mount `/dbfs/mnt/moh-data/` for raw and processed data
- [ ] Enable Spark adaptive query execution (`spark.sql.adaptive.enabled=true`)
- [ ] Set up cluster autoscaling (min: 1, max: 4 workers, Standard_DS3_v2)
- [ ] Configure loguru log rotation (10 MB, 30-day retention)

## Security & Compliance
- [ ] Ensure health data handling complies with MOH data governance policies
- [ ] Confirm Kaggle datasets are public and cleared for government use
- [ ] Review outputs for any PII before sharing with stakeholders
