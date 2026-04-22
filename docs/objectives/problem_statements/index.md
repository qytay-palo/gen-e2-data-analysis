# Problem Statements Index

## Overview

This index tracks the active problem statements for the Gen-E2 workforce analysis project. The five PSes are designed to support two demo scenarios — see the demo map below.

**Validation status as of 22 April 2026:** All five PSes have been checked against the documented SharePoint workforce source, the workforce data dictionary, and the local-first Python/Polars/Dash/statsmodels toolchain. The set is end-to-end solvable because PS-001 creates the local canonical dataset from the four documented SharePoint CSVs, and every downstream PS consumes only documented local outputs.

## STEP 1.5 Data Reality Check

**Available data domains**
- Healthcare workforce headcount by profession and sector from four SharePoint CSV files: doctors, nurses, pharmacists, physiotherapists

**Temporal scope**
- Analytical grain validated for delivery: annual headcount using the documented `year` field
- Source refresh cadence: monthly file refreshes, but the cross-file analytical contract is annual rather than daily or monthly time series

**Geographic and organizational scope**
- Confirmed comparison dimensions in documented data: profession and sector
- No facility-level, district-level, or patient-level fields are documented for this delivery

**Feasible analyses**
- Build a canonical combined workforce dataset from the four SharePoint CSV files
- Annual profession-level and sector-level trend analysis
- Annual YoY growth and CAGR comparisons across professions and sectors
- Profession-level five-year supply forecasting from historical headcount trends
- Dashboard delivery that reads local processed outputs without re-querying SharePoint

**Infeasible analyses within current scope**
- Real-time or monthly operational monitoring based only on the documented shared contract
- Facility-level or regional workforce comparisons
- Demand forecasting, shortage-gap estimation, or training-pipeline adequacy analysis without additional demand-side data
- Individual-level or patient-level causal analysis

## Problem Statements

| PS | Validation | Description | Demo Role |
|----|------------|-------------|-----------|
| [ps-001-workforce-data-foundation](ps-001-workforce-data-foundation.md) | Validated | Extract, validate, and clean workforce data from SharePoint into a trusted analysis-ready Parquet file. | Prerequisite |
| [ps-002-workforce-trends-dashboard](ps-002-workforce-trends-dashboard.md) | Validated | Build a Plotly Dash app with two pre-built tabs: Headcount Over Time and Sector Breakdown. | Demo 1 + Demo 2 opening state |
| [ps-003-workforce-growth-analysis](ps-003-workforce-growth-analysis.md) | Validated | Compute YoY growth rates and CAGR; append a Growth Trends tab to the dashboard live during the demo. | Demo 1 live story |
| [ps-004-headcount-forecasting](ps-004-headcount-forecasting.md) | Validated with scope clarification | Train linear baseline + ARIMA per profession; export champion registry and rolling 5-year forecast table. | Demo 2 pre-executed |
| [ps-005-forecast-dashboard-integration](ps-005-forecast-dashboard-integration.md) | Validated with horizon clarification | Add a 5-Year Forecast tab to the dashboard by reading PS-004 outputs — no retraining. | Demo 2 live story |

## User Story Backlogs

| PS | User Story Index | Coverage | Reusable Components | Status |
|----|------------------|----------|---------------------|--------|
| PS-001 | [problem-statement-001-workforce-data-foundation](../user_stories/problem-statement-001-workforce-data-foundation/index.md) | SharePoint extraction, schema validation, profiling, cleaning, Parquet export | Shared SharePoint connector, canonical Parquet contract, cleaning audit | Generated |
| PS-002 | [problem-statement-002-workforce-trends-dashboard](../user_stories/problem-statement-002-workforce-trends-dashboard/index.md) | Dash scaffold, Headcount Over Time tab, Sector Breakdown tab, smoke validation | Dashboard entrypoint, modular tab directory, canonical Parquet contract | Generated |
| PS-003 | [problem-statement-003-workforce-growth-analysis](../user_stories/problem-statement-003-workforce-growth-analysis/index.md) | YoY growth computation, CAGR computation, Parquet export, Growth Trends tab, runtime injection | Growth-rate Parquet contract, Growth Trends tab module, PS-002 appendable tab host | Generated |
| PS-004 | [problem-statement-004-headcount-forecasting](../user_stories/problem-statement-004-headcount-forecasting/index.md) | Annual feature engineering, linear baseline, ARIMA, held-out evaluation, registry publication, five-year forecast export | Model comparison table, model registry CSV, forecast table CSV | Generated |
| PS-005 | [problem-statement-005-forecast-dashboard-integration](../user_stories/problem-statement-005-forecast-dashboard-integration/index.md) | Forecast contract loading, forecast tab module, runtime injection | Forecast tab module, PS-004 CSV contracts, PS-002 appendable tab host | Generated |

## Demo Map

| Demo | Pre-executed before demo | Called live during demo |
|------|--------------------------|------------------------|
| **Demo 1 — Live Analysis** | PS-001, PS-002 | PS-003 |
| **Demo 2 — Forecast** | PS-001, PS-002, PS-004 | PS-005 |

## Progress Notes

- PS-001 is the prerequisite for all other PSes — do not skip it.
- PS-002 must be designed with an appendable tab list so PS-003 and PS-005 can inject tabs without restarting the server.
- PS-003 user stories assume growth metrics are exported once and consumed by the dashboard rather than recomputed inside callbacks.
- PS-004 outputs (`model_registry.csv`, `forecast_table.csv`) are the stable file contract that PS-005 reads — do not rename or move them.
- PS-004 user stories preserve a file-based interface so PS-005 never loads model objects or retrains at dashboard runtime.
- PS-004 and PS-005 are constrained to annual workforce supply forecasting from documented headcount history; they do not answer demand-side shortage questions without additional data.
- Target pipeline runtime: under 5 minutes per PS locally.