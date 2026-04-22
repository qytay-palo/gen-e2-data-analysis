# Story 02: Train ARIMA Models

## User Story
As a Data Scientist, I want an ARIMA model trained per profession with order selected by AIC, so that the forecast has a model capable of capturing autocorrelation beyond a linear trend.

## Acceptance Criteria
1. AIC-based grid search over (p, d, q) where p ∈ {0,1,2}, d ∈ {0,1}, q ∈ {0,1,2} — 18 combinations per profession
2. Best-AIC model fitted per profession and serialised to `artifacts/ps-004-headcount-forecasting/models/{profession}_arima_{YYYYMMDD}.pkl`
3. Selected (p,d,q) and AIC score logged per profession
4. Training uses same held-out split as Story 01 (last 3 years excluded)
5. If grid search fails for a profession (e.g. convergence issues), the error is logged and that profession falls back to the linear baseline — pipeline does not halt

## Technical Notes
- `statsmodels.tsa.arima.model.ARIMA` — suppress convergence warnings in logs, not silently
- Aggregate to annual total per profession before fitting (same series as Story 01)
- Training in `artifacts/ps-004-headcount-forecasting/src/models/arima_model.py`
- Runtime target: < 3 minutes for all 4 professions

## Definition of Done
- Up to 4 ARIMA `.pkl` files written (fallback to linear if convergence fails)
- Selected orders and AIC scores logged
- Pipeline completes without unhandled exceptions

## Story Points
5

## Priority
Must Have

## Dependencies
- PS-004 Story 01 complete — features and train/val split established
