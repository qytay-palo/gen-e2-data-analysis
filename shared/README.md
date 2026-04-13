# Shared Infrastructure

Reusable code, raw data, SQL queries, and configuration used across all problem statements.

## Structure

| Folder | Purpose |
|--------|---------|
| `src/` | Reusable Python library code (ETL, analysis, visualization, orchestration) |
| `data/1_raw/` | **Immutable** raw source data — never modify in place |
| `data/2_external/` | External reference data (demographics, benchmarks) |
| `data/schemas/` | Data schemas and contracts |
| `sql/` | SQL views, procedures, and extraction queries |
| `tests/` | Unit tests for shared functions |
| `config/` | `base.yml` (project-wide) and `databricks.yml` (platform-specific) |

## Data Connector

```python
from shared.src.data_processing.kaggle_connector import KaggleConnector

connector = KaggleConnector()          # Reads KAGGLE_USERNAME / KAGGLE_KEY from env
connector.test_connection()
connector.download_dataset(
    "owner/dataset-slug",
    "shared/data/1_raw/dataset-name/"
)
```

## Import Pattern (from problem-specific code)

```python
# In problem-statements/ps-001-*/src/
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))  # repo root
from shared.src.utils import ...
from shared.src.data_processing import ...
```
