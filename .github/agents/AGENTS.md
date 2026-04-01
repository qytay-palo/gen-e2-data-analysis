# Multi-Agent Data Analysis System

**Last Updated**: 2 March 2026  
**Version**: 2.0.0

## Overview

This project implements a **multi-agent orchestration system** for data analysis workflows. Specialized agents handle different stages of the data pipeline, from extraction to visualization, with built-in quality gates and handoff protocols.

### Key Benefits
- 🎯 **Specialization**: Each agent focuses on a specific domain expertise
- 🔄 **Reproducibility**: Standardized templates ensure consistency
- ✅ **Quality Gates**: Validation between stages prevents error propagation
- 📊 **Traceability**: Handoff files create audit trail of transformations
- 🚀 **Scalability**: Agents can run sequentially or in parallel

---

## Agent Architecture

### Agent Types

#### 1. Core Pipeline Agents
Execute the main data analysis workflow in sequence:

| Agent | Stages | Purpose | Key Outputs |
|-------|--------|---------|-------------|
| **ExtractionAgent** | 0-2 | Data extraction from Kaggle, CSV, APIs | `shared/data/3_interim/extracted_*.csv` |
| **ProfilingAgent** | 3 | Data quality assessment & profiling | `results/tables/*/data_quality_report.md` |
| **CleaningAgent** | 4 | Data cleaning & preprocessing | `problem-statements/ps-{num}-{name}/data/4_processed/cleaned_*.csv` |
| **EDAAgent** | 5 | Exploratory data analysis | `problem-statements/ps-{num}-{name}/reports/figures/*/`, `problem-statements/ps-{num}-{name}/notebooks/1_exploratory/` |
| **ModelingAgent** | 7 | Statistical modeling & forecasting | `problem-statements/ps-{num}-{name}/models/*/`, `problem-statements/ps-{num}-{name}/results/metrics/*/model_performance.json` |
| **VisualizationAgent** | 9 | Publication-quality visualizations | `problem-statements/ps-{num}-{name}/reports/figures/*/final/`, `problem-statements/ps-{num}-{name}/reports/*/final_report.md` |
| **DashboardAgent** | 9 | Interactive HTML dashboards with narrative storytelling | `problem-statements/ps-{num}-{name}/reports/dashboards/*.html`, `problem-statements/ps-{num}-{name}/notebooks/3_dashboards/` |

#### 2. Code Quality Agents
Ensure code quality and maintainability:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **CodeReviewerAgent** | Comprehensive code review (error handling, type safety, security, testing) | After new implementations, before PR |
| **DuplicateDetectionAgent** | Identify duplicate code patterns & refactoring opportunities | During refactoring sprints |
| **DeadCodeEliminationAgent** | Remove unused imports, functions, obsolete files | Before releases, cleanup sprints |
| **CodeReviewerAgent** | In-depth correctness & best practices review | Post-implementation validation |

#### 3. Supporting Agents
Plan and document the workflow:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **PlanningAgent** | Generate detailed implementation plans from user stories | Before starting new problem statements |
| **DocumentationAgent** | Create technical documentation | After implementation completion |

---