# Package Management & Environment

- **Always use `uv` for package management** (NOT pip/conda)
  ```bash
  uv pip install <package>           # Install new package
  uv pip install -r requirements.txt # Install from file
  uv pip freeze > requirements.txt   # Update after adding packages
  ```
- **Python 3.9+** is required (Databricks runtime compatibility)
- Virtual environment activation: `source .venv/bin/activate` (macOS/Linux)

## Data Processing Stack

### Primary: Polars (MANDATORY)
```python
import polars as pl

# Lazy loading for large files
df = pl.scan_csv("data/1_raw/disease_data.csv").collect()

# Method chaining for transformations
df_clean = (
    df.clone()
    .drop_nulls(subset=['date', 'case_count'])
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('disease').cast(pl.Categorical)
    ])
    .filter(pl.col('year') >= 2012)
)
```
- Use pandas ONLY if Polars lacks functionality (document why in comments)
- Optimize dtypes: `Int32` over `Int64`, `Categorical` for disease names
- Use lazy evaluation (`scan_csv`, `scan_parquet`) for files > 100MB

## Development Workflow

### 1. Problem-Driven Approach
- Each analysis task starts with a problem statement in `docs/objectives/problem_statements/`
- Reference existing problem statements: `ps-001-seasonal-pattern-forecasting.md`, `ps-002-disease-burden-prioritization.md`, `ps-003-executive-surveillance-dashboard.md`
- Define success criteria and stakeholder requirements upfront

### 2. Data Quality First
- ALWAYS validate data upon loading (check columns, dtypes, ranges)
- Handle missing values explicitly - never ignore them silently
- Generate data quality reports after cleaning steps
- Save validation results to `logs/etl/`

### 3. Modular Code Organization
- Place reusable functions in appropriate `src/` subdirectories:
  - `src/data_processing/`: ETL, cleaning, validation
  - `src/analysis/`: Statistical algorithms, trend detection
  - `src/models/`: Forecasting models, model evaluation
  - `src/visualization/`: Chart generation utilities
  - `src/utils/`: Helpers, config loaders
- Use type hints and docstrings for all functions
- Write unit tests in `tests/unit/` for critical logic

### 4. Logging & Monitoring
- Use `loguru` for logging (NOT `print()` in production code)
- Log to appropriate subdirectories: `logs/etl/`, `logs/errors/`, `logs/audit/`
- Include timestamps and severity levels

### 5. Results Documentation
- Save analysis outputs to `results/` subdirectories:
  - `results/tables/`: Summary statistics, analytical tables
  - `results/metrics/`: KPIs, performance metrics
  - `results/exports/`: Stakeholder-ready CSV/Excel exports
- Generate figures to `reports/figures/` in PNG/PDF for presentations

## Databricks Integration

- Cluster config in `config/databricks.yml` specifies runtime 13.3.x (Python 3.9)
- Workspace paths: `/Workspace/Users/moh-analytics/`
- Data storage: `/dbfs/mnt/moh-data/`
- Use `databricks-connect` for local development with remote Spark clusters
- Enable Spark adaptive query execution in configs

## Common Patterns & Anti-Patterns

### ✅ DO
```python
# Load config-driven parameters
import yaml
with open('config/analysis.yml') as f:
    config = yaml.safe_load(f)
target_diseases = config['data']['target_diseases']

# Save intermediate checkpoints with timestamps
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
df_clean.write_csv(f'data/3_interim/cleaned_disease_data_{timestamp}.csv')

# Use type hints and validation
def calculate_seasonal_strength(df: pl.DataFrame, disease: str) -> float:
    """Calculate seasonal strength metric for a disease time series."""
    if 'case_count' not in df.columns:
        raise ValueError("DataFrame must contain 'case_count' column")
    # ... implementation
```

### ❌ DON'T
```python
# Hardcoded parameters
diseases = ['Dengue', 'HFMD']  # Use config/analysis.yml instead

# Modifying raw data
df = pl.read_csv('data/1_raw/source.csv')
df.write_csv('data/1_raw/source.csv')  # NEVER overwrite raw data

# Silent failures
df = df.drop_nulls()  # Should log how many rows were dropped

# Print statements in production
print("Processing complete")  # Use logger.info() instead
```

## Testing Strategy

- Unit tests in `tests/unit/` for functions in `src/`
- Integration tests in `tests/integration/` for end-to-end pipelines
- Data validation tests in `tests/data/` for schema compliance
- Run tests with `pytest` before committing code
- Target: >80% code coverage for critical modules

## Quick Reference: Key Files

- [TODO.md](TODO.md): Project task breakdown with ownership and status
- [docs/project_context/](docs/project_context/): Project objectives and data source details
- [.github/instructions/](.github/instructions/): Coding standards (refer to these for detailed conventions) and best practices
