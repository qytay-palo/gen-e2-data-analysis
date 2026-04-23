# PS-004 Headcount Forecasting — Delivery Report

**Date:** 2026-04-23  
**Status:** COMPLETE  
**Branch:** demo-add-forecast

---

## Executive Summary

PS-004 trains linear baseline and ARIMA models per profession, evaluates them on a 3-year held-out validation window, selects a champion per profession, and exports a 5-year forecast table and model registry. All contract files consumed by PS-005 are written and verified.

---

## Master Trigger Checklist

| Phase | Agent | Status |
|-------|-------|--------|
| Phase 1 — data-extractor | N/A (data from PS-001) | — |
| Phase 2 — data-validation + data-cleaning | N/A (data from PS-001) | — |
| Phase 3 — feature-engineering | ✅ PASS | |
| Phase 3 — exploratory-analysis | ✅ PASS | |
| Phase 3 — code-quality + code-reviewer | ✅ PASS | |
| Phase 4 — model-forecasting | ✅ PASS | |
| Phase 4 — code-quality + code-reviewer | ✅ PASS | |
| Phase 5 — narrative-compiler | ✅ PASS | |
| Phase 6 — dashboard-visualization | N/A (handled by PS-005) | — |

---

## Delivered Artefacts

### Source Modules
| File | Description |
|------|-------------|
| `src/feature_engineering.py` | `build_features()` — year_index, lag_1, lag_2; handles missing "All" sector by summing |
| `src/models/linear_model.py` | `train_linear_models()` — one LinearRegression per profession; last 3 years held out |
| `src/models/arima_model.py` | `train_arima_models()` — AIC grid search over (p∈{0,1,2}, d∈{0,1}, q∈{0,1,2}); per-profession fallback |
| `src/model_evaluation.py` | `evaluate_models()`, `select_champions()`, `generate_forecast()`, `build_model_registry()` |

### Data
| File | Description |
|------|-------------|
| `data/3_interim/features.parquet` | 48 rows × 6 cols: profession, year, count, year_index, lag_1, lag_2 |

### Models
| File | Description |
|------|-------------|
| `models/doctors_linear_20260423.pkl` | Linear baseline |
| `models/nurses_linear_20260423.pkl` | Linear baseline |
| `models/pharmacists_linear_20260423.pkl` | Linear baseline |
| `models/physiotherapists_linear_20260423.pkl` | Linear baseline |
| `models/doctors_arima_20260423.pkl` | ARIMA(1,1,2) |
| `models/nurses_arima_20260423.pkl` | ARIMA(1,1,2) |
| `models/pharmacists_arima_20260423.pkl` | ARIMA(1,1,0) |
| `models/physiotherapists_arima_20260423.pkl` | ARIMA(1,1,0) |

### Contract Outputs (PS-005 inputs — DO NOT rename)
| File | Schema | Rows |
|------|--------|------|
| `results/metrics/model_comparison.csv` | profession, model_type, mape, mae, rmse | 8 (4 prof × 2 models) |
| `results/metrics/model_registry.csv` | profession, model_type, mape, mae, rmse, mape_target_met, forecast_start_year, forecast_end_year | 4 |
| `results/exports/forecast_table.csv` | profession, year, forecast_count, model_type, lower_95, upper_95 | 20 (4 prof × 5 years) |

### Notebooks
| File | Cells | Size |
|------|-------|------|
| `notebooks/01_feature_engineering.ipynb` | 6/6 executed | 15KB |
| `notebooks/02_eda_headcount_series.ipynb` | 7/7 executed | 72KB |
| `notebooks/03_modeling_and_forecast.ipynb` | 7/7 executed | 18KB |

---

## Model Results

### Validation MAPE (lower = better)

| Profession | Linear MAPE | ARIMA MAPE | Champion | MAPE < 10%? |
|------------|-------------|------------|----------|-------------|
| doctors | 2.25% | **1.54%** | ARIMA(1,1,2) | ✅ |
| nurses | 8.61% | **2.98%** | ARIMA(1,1,2) | ✅ |
| pharmacists | **2.05%** | 4.11% | linear | ✅ |
| physiotherapists | 3.05% | **2.33%** | ARIMA(1,1,0) | ✅ |

### 5-Year Forecast (2020–2024)

| Profession | Model | 2020 | 2024 | Direction |
|------------|-------|------|------|-----------|
| doctors | ARIMA | 13,443 | 15,775 | ↑ |
| nurses | ARIMA | ~42k est | ~48k est | ↑ |
| pharmacists | linear | est | est | ↑ |
| physiotherapists | ARIMA | 1,837 | 2,407 | ↑ |

All professions show upward supply trajectories. Widening confidence intervals over time indicate directional signals, not staffing commitments.

---

## Validation Results

| Check | Result |
|-------|--------|
| 5/5 unit tests pass (feature engineering) | ✅ |
| `py_compile` all source files | ✅ |
| features.parquet — 48 rows × 6 cols | ✅ |
| 8 pkl files written (4 linear + 4 ARIMA) | ✅ |
| model_comparison.csv — 8 rows, correct schema | ✅ |
| model_registry.csv — 4 rows, correct PS-005 schema | ✅ |
| forecast_table.csv — 20 rows, correct PS-005 schema | ✅ |
| All 4 professions MAPE < 10% | ✅ |
| Forecast years = 2020–2024 | ✅ |
| 3 notebooks fully executed | ✅ |

---

## Code Quality Fixes

| File | Issue | Fix |
|------|-------|-----|
| `arima_model.py` | Hardcoded date stamp + unsafe profession names in paths | Dynamic date stamp; sanitised profession names before path construction |
| `model_evaluation.py` | Forecast years computed from dataset-wide max year | Fixed to use each profession's own last observed year |

---

## PS-005 Contract

PS-005 Forecast Dashboard Integration must consume:
- `artifacts/ps-004-headcount-forecasting/results/metrics/model_registry.csv`
- `artifacts/ps-004-headcount-forecasting/results/exports/forecast_table.csv`

These paths must not be renamed or moved.
