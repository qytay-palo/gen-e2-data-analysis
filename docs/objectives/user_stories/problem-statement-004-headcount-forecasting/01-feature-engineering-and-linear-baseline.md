# Story 01: Feature Engineering and Linear Baseline Models

## User Story
As a Data Scientist, I want time series features prepared and a linear baseline model trained per profession, so that there is a simple benchmark to compare ARIMA against in Story 02.

## Acceptance Criteria
1. Feature table produced with columns: `profession`, `year`, `count`, `year_index` (integer starting at 0), `lag_1` (prior year count), `lag_2`
2. One `LinearRegression` model trained per profession using `year_index` as the only feature (intentionally minimal baseline)
3. Each model serialised with `joblib.dump` to `artifacts/ps-004-headcount-forecasting/models/{profession}_linear_{YYYYMMDD}.pkl`
4. Training uses all years except the last 3 (held out for evaluation in Story 03)
5. Unit tests verify feature generation produces correct `year_index` and lag values

## Technical Notes
- Input: `shared/data/4_processed/workforce_clean.parquet` — aggregate to annual total per profession before feature engineering (sum across sectors)
- sklearn `LinearRegression` — no regularisation for the baseline
- Feature engineering in `artifacts/ps-004-headcount-forecasting/src/feature_engineering.py`
- Training in `artifacts/ps-004-headcount-forecasting/src/models/linear_model.py`
- Log training set size and date range per profession

## Definition of Done
- 4 `.pkl` files written (one per profession)
- Feature table written to `artifacts/ps-004-headcount-forecasting/data/3_interim/features.parquet`
- Unit tests pass

## Story Points
3

## Priority
Must Have

## Dependencies
- PS-001 Story 03 complete — `workforce_clean.parquet` must exist
