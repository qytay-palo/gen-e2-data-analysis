# Gen-E2 Workforce Trends Analysis

MOH workforce planners need to know whether current training and recruitment pipelines will produce enough doctors, nurses, pharmacists, and physiotherapists to meet projected demand over the next five years. This repository delivers a reproducible data foundation, interactive trend dashboards, and profession-level 5-year forecasts.

## Project overview

**Business decision supported:** Headcount planning for MOH doctors, nurses, pharmacists, and physiotherapists across public and private sectors through 2030.

**What happens without this:** Hiring and training decisions are made on intuition and spreadsheets, risking either over-supply (budget waste) or under-supply (patient care gaps).

**Success criteria:**
1. Trusted, reproducible cleaned dataset from all four profession files with a documented audit trail
2. Interactive self-service dashboard — historical trends by profession and sector with no manual steps
3. Profession-level 5-year forecasts with MAPE < 10% on held-out validation period
4. Full pipeline re-runs from scratch in under 30 minutes on source file refresh

## Technical environment

- Platform: Local-first (Python 3.11 + `.venv`); production target HEALIX/Databricks
- Fallback: MCDR/CDSW
- Package manager: `uv`
- Data processing: Polars (mandatory)
- Dashboard: Plotly Dash
- Primary source: MOH SharePoint / DataDojo workforce folder

## Problem statements

| PS | Name | Purpose | Demo role |
|----|------|---------|-----------|
| PS-001 | Workforce Data Foundation | Extract, validate, clean → `shared/data/4_processed/workforce_clean.parquet` | Prerequisite |
| PS-002 | Workforce Trends Dashboard | Dash app with Headcount Over Time + Sector Breakdown tabs | Demo 1 opening state |
| PS-003 | Workforce Growth Rate Analysis | Computes YoY growth + CAGR; adds Growth Trends tab live during demo | Demo 1 live story |
| PS-004 | Headcount Forecasting Models | Linear baseline + ARIMA per profession; champion registry + 5-year forecast table | Demo 2 pre-executed |
| PS-005 | Forecast Dashboard Integration | Adds 5-Year Forecast tab by reading PS-004 outputs — no retraining | Demo 2 live story |

## Repository structure

```text
.
├── artifacts/
│   ├── ps-001-workforce-data-foundation/
│   ├── ps-002-workforce-trends-dashboard/
│   ├── ps-003-workforce-growth-analysis/
│   ├── ps-004-headcount-forecasting/
│   └── ps-005-forecast-dashboard-integration/
│       ├── notebooks/
│       ├── src/
│       ├── data/
│       │   ├── 3_interim/
│       │   └── 4_processed/
│       ├── results/
│       ├── reports/
│       ├── models/
│       ├── config/
│       ├── scripts/
│       ├── tests/
│       └── logs/
├── docs/
│   ├── index.md
│   ├── project-context/
│   └── data_dictionary/
├── shared/
│   ├── src/           ← reusable connectors, ETL, models, viz
│   ├── data/
│   │   ├── 1_raw/     ← immutable source downloads
│   │   ├── 2_external/
│   │   ├── 4_processed/ ← shared clean outputs (e.g. workforce_clean.parquet)
│   │   └── schemas/
│   ├── sql/
│   ├── tests/
│   └── config/
├── scripts/
├── requirements.txt
└── TODO.md
```

## Shared vs problem-specific layout

- `shared/` contains reusable connectors, config, tests, schemas, and immutable raw data.
- Each `artifacts/ps-*/` folder is a self-contained analysis package — notebooks, src, data, results, reports, models, config, scripts, tests, logs.
- Raw source data is written to `shared/data/1_raw/` and never modified in place.
- The canonical clean dataset lives at `shared/data/4_processed/workforce_clean.parquet`.
- Processed outputs and stakeholder-ready results live inside the relevant problem package.

## Stakeholders

- **Primary:** Team Lead — reviews outputs, approves forecasts for planning use
- **End consumers:** MOH workforce planners — self-service dashboard users

## Environment setup

```bash
uv venv .venv
source .venv/bin/activate    # macOS/Linux
uv pip install -r requirements.txt
```

## Data access

Copy `.env.example` to `.env` and fill in SharePoint credentials.

```
SHAREPOINT_SITE_URL=https://<tenant>.sharepoint.com/sites/DataDojo
SHAREPOINT_WORKFORCE_FOLDER=/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce
SHAREPOINT_USERNAME=...
SHAREPOINT_PASSWORD=...
```

## Demo runbook

### Demo 1 — "Live Growth Analysis"

Pre-built state (this branch): PS-001 + PS-002 (Headcount Over Time + Sector Breakdown tabs).
Live story: agent plans PS-003, then executes it — computing growth rates and injecting the Growth Trends tab with no server restart.

```bash
# 1. Start the dashboard (keep this terminal open)
source .venv/bin/activate
python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py

# 2. Open browser → http://localhost:8050  (shows 2 tabs)

# 3. Plan PS-003 — open GitHub Copilot Chat and run:
#
#   #file:.github/prompts/1-planning-stage.md PS-003
#
#   This generates user stories + implementation plan under
#   docs/objectives/user_stories/problem-statement-003-workforce-growth-analysis/

# 4. Execute PS-003 — open GitHub Copilot Chat and run:
#
#   #file:.github/prompts/2-execution-stage.md PS-003
#
#   Or run the output script directly:
python artifacts/ps-003-workforce-growth-analysis/src/run_growth_analysis.py

# 5. Dash hot-reloads (~3 s). Refresh browser → Growth Trends tab now visible.
```

> Demo 2 ("Live Forecast Integration") is on the `demo-add-forecast` branch.

### Demo 2 — "Live Forecast Integration"

Pre-built state: PS-001 + PS-002 + PS-003 + PS-004 outputs (forecast CSVs pre-computed).
Live story: agent plans PS-005, then executes it — reading PS-004 outputs and injecting the 5-Year Forecast tab with no server restart.

```bash
# 1. Start the dashboard (keep this terminal open)
source .venv/bin/activate
python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py

# 2. Open browser → http://localhost:8050  (shows 3 tabs: Headcount Over Time, Sector Breakdown, Growth Trends)

# 3. Plan PS-005 — open GitHub Copilot Chat and run:
#
#   #file:.github/prompts/1-planning-stage.md PS-005
#
#   This generates user stories + implementation plan under
#   docs/objectives/user_stories/problem-statement-005-forecast-dashboard-integration/

# 4. Execute PS-005 — open GitHub Copilot Chat and run:
#
#   #file:.github/prompts/2-execution-stage.md PS-005
#
#   Or run the output script directly:
python artifacts/ps-005-forecast-dashboard-integration/src/forecast_tab.py

# 5. Dash hot-reloads (~3 s). Refresh browser → 5-Year Forecast tab now visible.
```

## Code quality

- Formatting / linting: Ruff
- Testing: Pytest (`>80%` coverage target for critical modules)
- Logging: Loguru (never `print()` in production code)
- Configuration: YAML + `.env` environment variables

## Notes

- SharePoint extraction requires valid credentials and network access.
- No transcript files were found, so transcript analysis was skipped during initialization.
