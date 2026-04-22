# Navigation Index — Gen-E2 Workforce Trends Analysis

## Project Context

- [Business Objectives](project-context/business-objectives.md)
- [Data Sources](project-context/data-sources.md)
- [Tech Stack](project-context/tech-stack.md)

## Data Dictionary

- [Index](data_dictionary/index.md)
- [Workforce Data Dictionary](data_dictionary/01-workforce-sharepoint.md)

## Problem Statements

- [Index](objectives/problem_statements/index.md)
- [PS-001 — Workforce Data Foundation](objectives/problem_statements/ps-001-workforce-data-foundation.md)
- [PS-002 — Workforce Trends Dashboard](objectives/problem_statements/ps-002-workforce-trends-dashboard.md)
- [PS-003 — Workforce Growth Rate Analysis](objectives/problem_statements/ps-003-workforce-growth-analysis.md)
- [PS-004 — Headcount Forecasting Models](objectives/problem_statements/ps-004-headcount-forecasting.md)
- [PS-005 — Forecast Dashboard Integration](objectives/problem_statements/ps-005-forecast-dashboard-integration.md)

## Artifact Packages

- [PS-001 artifact](../artifacts/ps-001-workforce-data-foundation/)
- [PS-002 artifact](../artifacts/ps-002-workforce-trends-dashboard/)
- [PS-003 artifact](../artifacts/ps-003-workforce-growth-analysis/)
- [PS-004 artifact](../artifacts/ps-004-headcount-forecasting/)
- [PS-005 artifact](../artifacts/ps-005-forecast-dashboard-integration/)

## Shared Infrastructure

- [Shared README](../shared/README.md)
- [Base Config](../shared/config/base.yml)
- [Databricks Config](../shared/config/databricks.yml)
- [CDSW Config](../shared/config/cdsw.yml)

## Agent Handoffs

- Located in: `docs/agent-handoffs/`

## Domain Knowledge

- Located in: `docs/domain-knowledge/`

---

## Workflow

```text
/0-start-gen-e2-data-analysis-project   ← Completed ✅
/1-planning-stage                        ← Next: generate user stories per PS
/2-execution-stage <ps-id>               ← Execute each PS in order
```

## Demo map

| Demo | Pre-executed | Live story |
|------|-------------|------------|
| Demo 1 — Live Analysis | PS-001, PS-002 | PS-003 |
| Demo 2 — Forecast | PS-001 → PS-004 | PS-005 |
