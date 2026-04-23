# PS-003 Workforce Growth Rate Analysis — Delivery Report

**Date:** 2026-04-23  
**Status:** COMPLETE

---

## Executive Summary

PS-003 computes year-on-year growth rates and CAGR per profession and sector, then automatically injects a live "Growth Trends" tab into the running PS-002 dashboard. A single executor invocation produces the analysis and patches the dashboard — browser refresh reveals the new tab with no server restart required.

---

## Master Trigger Checklist

| Phase | Agent | Status |
|-------|-------|--------|
| Phase 1 — data-extractor | N/A (data from PS-001) | — |
| Phase 2 — data-validation + data-cleaning | N/A (data from PS-001) | — |
| Phase 3 — exploratory-analysis | ✅ PASS | |
| Phase 3 — code-quality + code-reviewer | ✅ PASS | |
| Phase 4 — model-forecasting | N/A | — |
| Phase 5 — narrative-compiler | ✅ PASS | |
| Phase 6 — dashboard-visualization | ✅ PASS | |
| Phase 6 — code-quality + code-reviewer | ✅ PASS | |

---

## Delivered Artefacts

### PS-003 Analysis
| File | Description |
|------|-------------|
| `src/growth_analysis.py` | `compute_growth_rates()` — YoY + CAGR in Polars |
| `src/run_growth_analysis.py` | Pipeline entry point — writes growth_rates.parquet |
| `tests/unit/test_growth_analysis.py` | 5 unit tests (all pass) |
| `notebooks/01_growth_analysis.ipynb` | Executed EDA notebook (17 KB) |
| `results/tables/growth_rates.parquet` | 192 rows: profession × sector × year × yoy_pct × cagr |
| `reports/figures/cagr_by_profession.png` | CAGR bar chart |
| `reports/figures/yoy_growth_by_profession.png` | YoY line chart |
| `results/narrative.md` | Stakeholder narrative (236 words) |

### PS-002 Dashboard (modified)
| File | Description |
|------|-------------|
| `tabs/growth_trends.py` | New Growth Trends tab module (CAGR bar + YoY line + profession filter) |
| `workforce_trends_dashboard.py` | Patched to import + append growth tab (idempotent) |

---

## Key Findings

| Metric | Value |
|--------|-------|
| CAGR #1 (overall) | Physiotherapists 7.70% |
| CAGR #2 (overall) | Pharmacists 6.96% |
| CAGR #3 (overall) | Doctors 5.72% |
| CAGR #4 (overall) | Nurses 5.65% |
| Peak YoY (overall) | Physiotherapists 2015: +11.1% |
| Fastest sector (Public) | Pharmacists 10.35% CAGR |

---

## Dashboard State After Injection

The running app at `http://localhost:8050` now shows **3 tabs**:
1. Headcount Over Time
2. Sector Breakdown  
3. **Growth Trends** ← injected by PS-003

---

## Demo Flow (Demo 1)

| Step | Who | Action |
|------|-----|--------|
| Pre-demo | You | `python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py` |
| Live | You | Invoke executor-stage PS-003 |
| Automated | Agents | Growth rates computed → tab module written → app patched |
| Auto | Dash hot-reload | App reloads in ~3 sec |
| You | — | Browser refresh → Growth Trends tab visible |

---

## Validation Results

| Check | Result |
|-------|--------|
| 5/5 unit tests pass | ✅ |
| `py_compile` all 5 files | ✅ |
| `growth_rates.parquet` readable (192 rows) | ✅ |
| Tab module exports `make_tab` + `register_callbacks` | ✅ |
| Patch contains `growth_trends` string | ✅ |
| Patch is idempotent | ✅ |
| HTTP 200 on localhost:8050 | ✅ |

---

## Code Quality Fixes

| File | Issue | Fix |
|------|-------|-----|
| `growth_trends.py` | Polars→pandas conversion at module import (violated data-flow rule) | Kept `DF_GROWTH` as Polars at module level; converts to pandas only inside callbacks at Plotly boundary |
| `workforce_trends_dashboard.py` | Growth tab wiring as trailing appended block | Moved to single canonical import path at top of file |

---

## Acceptance Criteria — All Met

- [x] `growth_analysis.py` computes YoY % and CAGR with no hardcoded values
- [x] `growth_rates.parquet` written (192 rows)
- [x] Growth Trends tab injected automatically by executor — no separate command
- [x] Tab contains CAGR bar chart + YoY line chart with profession filter
- [x] Patch is idempotent (safe to run twice)
- [x] HTTP 200 confirmed after injection
- [x] 5 unit tests pass
