# PS-004 — Headcount Forecasting Models

## Status
Defined

## Description
Train a linear baseline model and an ARIMA model per profession using the canonical clean Parquet. Evaluate both on a held-out validation window, select the champion model per profession using documented selection rules, and export a machine-readable model registry and a 5-year forecast table. This PS forecasts workforce supply only from historical headcount trends; it does not estimate demand, training throughput, or shortage gaps because those inputs are not in the documented SharePoint workforce data. This PS is fully pre-executed before Demo 2 — the client never waits for training.

## Primary Stakeholder
Team Lead

## Business Question
What does the documented workforce headcount history suggest about profession-level supply direction over the next five annual periods?

## Success Criteria
1. Linear baseline and ARIMA trained for all four professions (doctors, nurses, pharmacists, physiotherapists)
2. Held-out validation window: last 3 years of available data
3. Consolidated evaluation table with MAPE, MAE, RMSE per profession × model, saved to `artifacts/ps-004-headcount-forecasting/results/metrics/model_comparison.csv`
4. Champion selected per profession by lowest MAPE; ties broken by RMSE; preference for simpler model when MAPE difference < 0.25 pp
5. MAPE < 10% flagged as achieved/not-achieved per profession in registry
6. 5-year forecast table for the next five annual periods after the latest observed year is saved to `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv` (current demo target: 2026–2030 when the latest observed year is 2025)
7. Model registry saved to `artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv` — consumed by PS-005 without modification

## Inputs
- `shared/data/4_processed/workforce_clean.parquet` (from PS-001)

## Outputs
- `artifacts/ps-004-headcount-forecasting/results/metrics/model_comparison.csv`
- `artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv` ← **contract for PS-005**
- `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv` ← **contract for PS-005**
- `artifacts/ps-004-headcount-forecasting/models/` — serialised fitted model objects (`.pkl`)
- `artifacts/ps-004-headcount-forecasting/logs/` — training and evaluation run logs

## Dependencies
- PS-001 must be complete and `workforce_clean.parquet` must exist

## Demo Role
**Demo 2 pre-executed.** All outputs must exist and be stable before the demo starts.

## Technical Notes
- Linear baseline: `sklearn.linear_model.LinearRegression` with `year` as the only feature
- ARIMA: `statsmodels.tsa.arima.model.ARIMA`; use AIC to auto-select (p,d,q) within (0–2, 0–1, 0–2) grid per profession
- Train/validation split: chronological, no shuffling
- Modeling grain is annual profession-level headcount because the validated shared contract is `year, sector, count, profession`
- If a profession series is too short or sparse for stable ARIMA fitting after cleaning, the linear baseline remains the default feasible model and must still be evaluated and exported
- Store model objects with `joblib.dump`; filename convention `{profession}_{model_type}_{YYYYMMDD}.pkl`
- Model registry CSV schema: `profession, model_type, mape, mae, rmse, mape_target_met, forecast_start_year, forecast_end_year`
- Forecast table CSV schema: `profession, year, forecast_count, model_type, lower_95, upper_95`
