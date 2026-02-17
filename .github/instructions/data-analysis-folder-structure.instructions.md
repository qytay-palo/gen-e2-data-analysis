---
name: 'Data Analysis Folder Structure'
description: 'Data Analysis folder structure for organizing project files and documentation.'
applyTo: 'src/problem-statement-*/**'
---

# Instructions

When starting a new data analysis project or organizing an existing one, **CREATE** the following folder structure. Use the phase indicators to guide which folders/files to create based on project maturity:

1. **Create all directories** using the structure below
2. **Initialize key files** in each phase as indicated
3. **Add README.md files** in major directories to explain their purpose
4. **Create .gitkeep files** in empty directories to preserve structure in version control

Below is the base folder structure to create:
```
.
├── .env.example      # [PHASE 0] Template for environment variables (DB credentials, API keys)
├── .gitignore        # [PHASE 0] Files to exclude from version control
├── README.md         # [PHASE 0] Project overview and setup instructions
├── requirements.txt  # [PHASE 0] Python dependencies
├── environment.yml   # [PHASE 0] Conda environment (optional)
├── .github/          # [PHASE 0] GitHub Actions & CI/CD
│   └── workflows/
│       ├── data_quality_checks.yml  # → Automated data validation
│       └── scheduled_extraction.yml # → Scheduled ETL jobs
├── docs/             # [PHASE 1] Context & Understanding
│   ├── index.md         # → 1: Central documentation hub (navigation)
│   ├── objectives/      # → 2: PROJECT GOALS: What to achieve
│   ├── data_dictionary/ # → 3: Understand data: schemas, fields, definitions
│   └── methodology/     # → 4: Understand approach: statistical methods, frameworks
|   └── problem_statements.md #→ Analytics opportunities and use cases
├── config/           # [PHASE 2] Project Configuration
│   └── *.yml, *.json       # → Parameters, settings, environment configs
├── sql/              # [PHASE 2] SQL Queries & Database Scripts
│   ├── views/         # → SQL views for common queries
│   ├── procedures/    # → Stored procedures
│   └── extractions/   # → Data extraction queries
├── data/             # [PHASE 3] Data Acquisition & Preparation
│   ├── 1_raw/         # → 1: Original immutable source data
│   ├── 2_external/    # → 2: External reference data (demographics, benchmarks)
│   ├── 3_interim/     # → 3: Intermediate transformation outputs
│   ├── 4_processed/   # → 4: Final cleaned datasets (analysis-ready)
│   └── schemas/       # → Data schemas, contracts, and lineage documentation
├── notebooks/        # [PHASE 4] Interactive Exploration & Analysis
│   ├── 1_exploratory/   # → 1: Initial EDA, data profiling, hypothesis generation
│   └── 2_analysis/      # → 2: Deep-dive analysis, final insights, documentation
│   └── 3_feature_engineering/ # → 3: Feature creation, variable transformations 
├── src/              # [PHASE 5] Production Code Development
│   ├── utils/           # → Foundation: Helper functions, common utilities
│   ├── data_processing/ # → Pipeline 1: ETL, cleaning, validation
│   ├── features/        # → Pipeline 2: Feature engineering, variable transformations
│   ├── analysis/        # → Pipeline 3: Statistical analysis, algorithms
│   ├── visualization/   # → Pipeline 4: Chart generation, plotting utilities
│   └── models/          # → Pipeline 5: Model training, hyperparameter tuning
├── tests/            # [PHASE 6] Quality Assurance
│   ├── unit/          # → Unit tests for individual functions
│   ├── integration/   # → Integration tests for pipelines
│   └── data/          # → Data validation tests
├── models/           # [PHASE 7] Model Development & Storage
│   └── *.pkl, *.h5, *.joblib # → Trained models, model artifacts, serialized objects
├── results/          # [PHASE 8] Analysis Outputs
│   ├── tables/        # → Output 1: Summary statistics, analytical tables (CSV/Excel)
│   ├── metrics/       # → Output 2: Performance KPIs, evaluation metrics (JSON/CSV)
│   └── exports/       # → Output 3: Stakeholder-ready data exports
├── reports/          # [PHASE 9] Stakeholder Communication
│   ├── figures/       # → Component 1: Static visualizations (PNG/PDF)
│   ├── dashboards/    # → Component 2: Interactive dashboards (HTML/Streamlit)
│   └── presentations/ # → Component 3: Executive summaries (PPTX/PDF)
├── logs/             # [PHASE 10] Execution Logs & Audit Trails
│   ├── etl/           # → ETL pipeline execution logs
│   ├── errors/        # → Error logs and stack traces
│   └── audit/         # → Audit trails for data access and changes
└── scripts/          # [PHASE 10] Automation & Deployment
    └── *.py, *.R, *.sh  # → End-to-end pipelines, deployment scripts, automation
```

## Implementation Steps

When creating this structure for a new project:

1. **Initialize Python environment**:
   - Create virtual environment using `uv`: `uv venv .venv`
   - Activate environment: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
   - Create `requirements.txt` with essential packages:
     ```
     polars>=0.20.0
     numpy>=1.24.0
     matplotlib>=3.7.0
     seaborn>=0.12.0
     plotly>=5.14.0
     pyyaml>=6.0
     loguru>=0.7.0
     pytest>=7.3.0
     jupyter>=1.0.0
     ```
   - Install dependencies: `uv pip install -r requirements.txt`

2. **Create the directory structure** using the appropriate command for your OS:
   - macOS/Linux: Use `mkdir -p` to create nested directories
   - Windows: Use `mkdir` or PowerShell equivalent

3. **Initialize essential files**:
   - Create `.gitkeep` files in empty directories
   - Add `__init__.py` files in all Python package directories under `src/` and `tests/`
   - Generate starter `README.md` files with directory purpose descriptions
   - Create `.env.example` template for environment variables
   - Set up `.gitignore` with appropriate patterns (`.venv/`, `data/1_raw/`, `*.pyc`, `__pycache__/`, `.env`, `logs/`, `.DS_Store`)

4. **Set up configuration files** in `config/`:
   - Create YAML/JSON files for project parameters
   - Document database connections, API settings, environment variables
   - Add `analysis.yml` for analysis parameters
   - Add `databricks.yml` if using Databricks

5. **Update project documentation**:
   - Populate `README.md` with project overview and setup instructions
   - Create `docs/index.md` as the central documentation hub
   - Add data dictionaries and methodology documentation as needed
   - Create `TODO.md` for task tracking

6. **Initialize logging configuration**:
   - Set up loguru logger in `src/utils/logger.py`
   - Configure log rotation and retention policies
   - Create log directory structure

7. **Maintain structure integrity**:
   - Never modify files in `data/1_raw/` (immutable source data)
   - Log all ETL activities to `logs/etl/`
   - Version control all code in `src/` with proper tests in `tests/`

## Usage Guidelines

- **For new projects**: Create the entire structure at project initialization
- **For existing projects**: Gradually migrate to this structure, starting with critical phases
- **Phase-based approach**: Focus on creating folders relevant to your current project phase
- **Flexibility**: Adapt the structure to project needs while maintaining core organization principles