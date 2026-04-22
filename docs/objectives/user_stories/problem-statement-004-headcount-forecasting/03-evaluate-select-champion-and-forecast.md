# Story 03: Evaluate Models, Select Champions, and Generate Forecast Table

## User Story
As a Team Lead, I want a single evaluation run that compares linear and ARIMA models, selects the best per profession, and exports a 5-year forecast table and model registry, so that Demo 2 has all pre-computed outputs ready to wire into the dashboard.

## Acceptance Criteria
1. Evaluation table with MAPE, MAE, RMSE for every profession × model combination on the held-out validation years written to `artifacts/ps-004-headcount-forecasting/results/metrics/model_comparison.csv`
2. Champion selected per profession: lowest MAPE; tie-break by RMSE; prefer simpler model (linear) if MAPE difference < 0.25 percentage points
3. `model_registry.csv` written to `artifacts/ps-004-headcount-forecasting/results/metrics/` with schema: `profession, model_type, mape, mae, rmse, mape_target_met` — this is the **PS-005 contract**
4. 5-year forecast table written to `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv` with schema: `profession, year, forecast_count, model_type, lower_95, upper_95` — this is the **PS-005 contract**
5. MAPE < 10% flagged as `true`/`false` in `mape_target_met` column
6. Professions where no model meets 10% MAPE target are logged with a warning but still included

## Technical Notes
- Load serialised models with `joblib.load` — no retraining in this story
- Forecast horizon: 5 years after the last observed year in the dataset
- Confidence intervals: use `statsmodels` `get_forecast().conf_int()` for ARIMA; for linear baseline use ±1.96 × residual std dev
- Evaluation in `artifacts/ps-004-headcount-forecasting/src/model_evaluation.py`

## Definition of Done
- `model_comparison.csv`, `model_registry.csv`, `forecast_table.csv` all written
- Both PS-005 contract files exist at documented paths
- Logged summary of champion models and MAPE target status per profession

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-004 Stories 01 and 02 complete — model `.pkl` files must exist
