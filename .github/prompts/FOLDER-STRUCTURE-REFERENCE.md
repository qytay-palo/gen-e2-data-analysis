# Hybrid Folder Structure Quick Reference

**Last Updated:** 2026-03-11  
**Purpose:** Quick reference for folder paths when using Gen-E2 prompts

---

## 🏗️ Hybrid Structure Overview

This project uses a **hybrid approach** combining:
- **Shared resources** (`shared/`) - Reusable code, raw data, SQL queries
- **Problem statements** (`problem-statement/ps-{num}/`) - Self-contained analysis packages

---

## 📁 Path Reference Guide

### Shared Resources (Write Once, Use Everywhere)

| What | Path | Purpose |
|------|------|---------|
| **Reusable Code** | `shared/src/` | Library functions (data processing, analysis, models, visualization, utils) |
| **Raw Data** | `shared/data/1_raw/` | Original source data (READ-ONLY, single source of truth) |
| **External Data** | `shared/data/2_external/` | Reference data (demographics, benchmarks) |
| **Agent Handoffs** | `shared/data/3_interim/agent_handoffs/` | Multi-agent communication files |
| **SQL Queries** | `shared/sql/` | Common SQL views, procedures, extractions |
| **Base Config** | `shared/config/base.yml` | Shared configuration parameters |
| **Platform Config** | `shared/config/databricks.yml` | Platform-specific settings |
| **Unit Tests** | `shared/tests/unit/` | Tests for shared code |

### Problem-Specific Resources (Self-Contained)

| What | Path | Purpose |
|------|------|---------|
| **Notebooks** | `problem-statement/ps-{num}/notebooks/` | Interactive analysis |
| ├─ Exploratory | `problem-statement/ps-{num}/notebooks/1_exploratory/` | Data profiling, exploration |
| ├─ Analysis | `problem-statement/ps-{num}/notebooks/2_analysis/` | Deep-dive analysis, modeling |
| └─ Feature Eng | `problem-statement/ps-{num}/notebooks/3_feature_engineering/` | Feature creation |
| **Custom Code** | `problem-statement/ps-{num}/src/` | Problem-specific utilities |
| **Interim Data** | `problem-statement/ps-{num}/data/3_interim/` | Intermediate processing results |
| **Processed Data** | `problem-statement/ps-{num}/data/4_processed/` | Final analysis-ready datasets |
| **Tables** | `problem-statement/ps-{num}/results/tables/` | Summary statistics, analytical tables |
| **Metrics** | `problem-statement/ps-{num}/results/metrics/` | KPIs, performance metrics |
| **Exports** | `problem-statement/ps-{num}/results/exports/` | Stakeholder-ready exports |
| **Figures** | `problem-statement/ps-{num}/reports/figures/` | Publication-quality visualizations |
| **Dashboards** | `problem-statement/ps-{num}/reports/dashboards/` | Interactive dashboards |
| **Presentations** | `problem-statement/ps-{num}/reports/presentations/` | Executive summaries |
| **Models** | `problem-statement/ps-{num}/models/` | Trained model artifacts |
| **Config** | `problem-statement/ps-{num}/config/config.yml` | Problem-specific configuration |
| **Scripts** | `problem-statement/ps-{num}/scripts/` | Pipeline orchestration scripts |
| **Tests** | `problem-statement/ps-{num}/tests/integration/` | Integration tests |
| **Logs** | `problem-statement/ps-{num}/logs/` | Execution logs (pipeline/, errors/) |
| **README** | `problem-statement/ps-{num}/README.md` | Problem overview and instructions |

### Project Documentation (Shared)

| What | Path | Purpose |
|------|------|---------|
| **Problem Statements** | `docs/objectives/problem_statements/ps-{num}-{slug}.md` | Problem definition documents |
| **User Stories** | `docs/objectives/user_stories/ps-{num}-{name}/` | User stories grouped by problem |
| **Data Dictionary** | `docs/data_dictionary/` | Data schemas and field definitions |
| **Methodology** | `docs/methodology/` | Statistical methods, frameworks |
| **Project Context** | `docs/project_context/` | Business objectives, tech stack, guides |

---

## 🔄 Import Pattern (CRITICAL)

**In all problem-specific notebooks and scripts:**

```python
import sys
from pathlib import Path

# Add shared library to Python path
shared_path = Path(__file__).parent.parent.parent.parent / 'shared'  # For scripts
# OR for notebooks:
shared_path = Path('../../../../shared').resolve()

sys.path.append(str(shared_path))

# Now import shared utilities
from src.data_processing.loaders import load_disease_data
from src.analysis.time_series import detect_seasonality
from src.visualization.plots import create_time_series_plot
from src.utils.logger import setup_logger

# Also import problem-specific utilities
from src.custom_utils import custom_function  # From problem-statement/ps-{num}/src/
```

---

## 🎯 Decision Tree: Where to Put Code?

```
Is this code reusable across multiple problem statements?
├─ YES → shared/src/{module}/
│         Examples: data loaders, cleaning functions, 
│                   statistical algorithms, plotting utilities
│
└─ NO → problem-statement/ps-{num}/src/
         Examples: problem-specific transformations,
                   custom business logic, one-off calculations
```

---

## 📊 Decision Tree: Where to Put Data?

```
What type of data is this?
├─ Raw source data → shared/data/1_raw/
│   (Original, immutable, single source of truth)
│
├─ External reference data → shared/data/2_external/
│   (Demographics, benchmarks, lookup tables)
│
├─ Intermediate processing → problem-statement/ps-{num}/data/3_interim/
│   (Temporary, problem-specific transformations)
│
└─ Final analysis-ready → problem-statement/ps-{num}/data/4_processed/
    (Clean, validated, ready for analysis)
```

---

## ⚙️ Decision Tree: Where to Put Config?

```
What type of configuration?
├─ Shared base settings → shared/config/base.yml
│   (Database connections, default parameters)
│
├─ Platform settings → shared/config/databricks.yml
│   (Cluster config, workspace paths)
│
└─ Problem-specific → problem-statement/ps-{num}/config/config.yml
    (Analysis parameters, target diseases, date ranges)
```

---

## 📝 Naming Conventions

### Problem Statement Identifiers
- **Format:** `ps-{num}` or `ps-{num}-{slug}`
- **Examples:**
  - `ps-001` (short form)
  - `ps-001-seasonal-forecasting` (full form with slug)
  - `ps-002-disease-burden-analysis`

### File Naming
- **Notebooks:** `{step}_{description}.ipynb` → `01_data_profiling.ipynb`
- **Scripts:** `run_{purpose}_pipeline.py` → `run_forecasting_pipeline.py`
- **Outputs:** `{metric}_{date}.{ext}` → `weekly_forecasts_20260311.csv`
- **Config:** `config.yml` (in problem folder) or `base.yml` (in shared/config/)

---

## 🚀 Quick Start: Creating New Problem Statement

```bash
# Use the hybrid scaffold script
./scripts/shared/create_problem_statement_hybrid.sh 003 "outbreak-prediction" "Real-time outbreak prediction"

# This creates:
# - docs/objectives/problem_statements/ps-003-outbreak-prediction.md
# - problem-statement/ps-003-outbreak-prediction/ (complete structure)
# - docs/objectives/user_stories/ps-003/ (user stories folder)
```

---

## 📚 Reference Documents

- **Detailed Guide:** [docs/project_context/folder-structure-guide.md](../../docs/project_context/folder-structure-guide.md)
- **Comparison:** [docs/project_context/folder-structure-comparison.md](../../docs/project_context/folder-structure-comparison.md)
- **Scripts README:** [scripts/shared/README.md](../../scripts/shared/README.md)
- **Notebooks README:** [notebooks/README.md](../../notebooks/README.md)

---

## ✅ Checklist for Prompt Users

When creating implementation plans or executing code:

- [ ] Identified if code is **shared** (reusable) or **problem-specific** (one-time)
- [ ] Placed shared code in `shared/src/{appropriate_module}/`
- [ ] Placed problem-specific code in `problem-statement/ps-{num}/src/`
- [ ] Used correct import pattern in notebooks/scripts
- [ ] Saved raw data to `shared/data/1_raw/` (if new source)
- [ ] Saved outputs to `problem-statement/ps-{num}/{results|reports}/`
- [ ] Created configuration in appropriate location (shared vs problem-specific)
- [ ] Followed naming conventions for files and directories
- [ ] Updated documentation and README files

---

**Remember:** The hybrid structure balances **code reusability** (shared resources) with **clear organization** (self-contained problem statements). When in doubt, ask: "Will other problem statements use this?" If yes → `shared/`. If no → `problem-statement/ps-{num}/`.
