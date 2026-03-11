# Implementation Plan Reference Guide

> Supporting documentation for `3-generate-data-analysis-implementation-plan.prompt.md`

## Table of Contents
1. [Code Executability Standards](#code-executability-standards)
2. [Code Examples by Section](#code-examples-by-section)
3. [Testing Patterns](#testing-patterns)
4. [Security Patterns](#security-patterns)
5. [Common Anti-Patterns](#common-anti-patterns)

---

## Code Executability Standards

### Complete Function Implementation Example

```python
import polars as pl
from pathlib import Path
from loguru import logger
import yaml

def extract_disease_data(
    start_date: str,
    end_date: str,
    diseases: list[str],
    config_path: str = "config/analysis.yml"
) -> pl.DataFrame:
    """Extract disease surveillance data for specified period and diseases.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        diseases: List of disease names to extract
        config_path: Path to configuration file
        
    Returns:
        DataFrame with columns: [date, disease, case_count, region, age_group]
        
    Raises:
        ValueError: If date range invalid or diseases not found
        FileNotFoundError: If config file not found
    """
    # Load configuration
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Validate date range
    try:
        start = pl.datetime.strptime(start_date, '%Y-%m-%d')
        end = pl.datetime.strptime(end_date, '%Y-%m-%d')
        if start > end:
            raise ValueError(f"start_date {start_date} must be before end_date {end_date}")
    except Exception as e:
        logger.error(f"Invalid date format: {e}")
        raise ValueError(f"Dates must be in YYYY-MM-DD format: {e}")
    
    # Extract data
    data_path = config['data']['source_path']
    try:
        df = (
            pl.scan_csv(data_path)
            .filter(pl.col('disease').is_in(diseases))
            .filter(
                (pl.col('date') >= start_date) & 
                (pl.col('date') <= end_date)
            )
            .collect()
        )
        logger.info(f"Extracted {len(df)} records for {len(diseases)} diseases")
        return df
    except Exception as e:
        logger.error(f"Data extraction failed: {e}")
        raise
```

### Validation Before Including Code Checklist

- [ ] **Syntax**: Run through linter or mentally parse for errors
- [ ] **Imports**: All dependencies listed at top
- [ ] **Paths**: Reference actual project locations or config-driven paths
- [ ] **Error handling**: Try/except for all external operations
- [ ] **Logging**: Use loguru, never print()
- [ ] **Type hints**: Parameters and return types specified
- [ ] **Docstring**: NumPy style with Args/Returns/Raises
- [ ] **No stubs**: Full implementation, no TODO or pass

---

## Code Examples by Section

### Section 6.2: Data Schemas

**Pydantic Model Example:**
```python
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Literal

class DiseaseRecordSchema(BaseModel):
    """Schema for disease surveillance records."""
    epi_week: int = Field(ge=1, le=53, description="Epidemiological week")
    disease_name: str = Field(min_length=1, description="Disease name")
    case_count: int = Field(ge=0, description="Number of cases")
    date_reported: date
    region: Literal['North', 'South', 'East', 'West', 'Central']
    
    @validator('disease_name')
    def validate_disease(cls, v):
        allowed = ['Dengue', 'HFMD', 'Chickenpox', 'TB']
        if v not in allowed:
            raise ValueError(f"Disease must be one of {allowed}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "epi_week": 23,
                "disease_name": "Dengue",
                "case_count": 145,
                "date_reported": "2026-06-07",
                "region": "Central"
            }
        }
```

**Dataclass Example:**
```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class WorkforceRecord:
    """Record for healthcare workforce data."""
    year: int
    profession: str
    total_count: int
    region: str
    per_10k_population: float
    data_date: date = field(default_factory=date.today)
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.year < 2000 or self.year > 2030:
            raise ValueError(f"Invalid year: {self.year}")
        if self.total_count < 0:
            raise ValueError(f"Count cannot be negative: {self.total_count}")
```

### Section 6.3: Data Validation Rules

**Comprehensive Validation Example:**
```python
import polars as pl
from loguru import logger
from typing import Dict, List, Tuple

# Schema definition
REQUIRED_COLUMNS = ['date', 'disease', 'case_count', 'region']

EXPECTED_DTYPES = {
    'date': pl.Date,
    'disease': pl.Categorical,
    'case_count': pl.Int32,
    'region': pl.Categorical,
    'age_group': pl.Categorical
}

VALUE_CONSTRAINTS = {
    'case_count': {'min': 0, 'max': 100000},
    'year': {'min': 2012, 'max': 2026},
    'disease': {'allowed': ['Dengue', 'HFMD', 'Chickenpox', 'TB']},
    'region': {'allowed': ['North', 'South', 'East', 'West', 'Central']}
}

def validate_dataframe(df: pl.DataFrame, schema_name: str = "disease_data") -> Dict[str, any]:
    """Validate DataFrame against schema and constraints.
    
    Returns:
        dict with validation results and issues found
    """
    issues = []
    
    # Check required columns
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")
    
    # Check data types
    for col, expected_dtype in EXPECTED_DTYPES.items():
        if col in df.columns and df[col].dtype != expected_dtype:
            issues.append(f"Column '{col}' has type {df[col].dtype}, expected {expected_dtype}")
    
    # Check value constraints
    for col, constraints in VALUE_CONSTRAINTS.items():
        if col not in df.columns:
            continue
        
        if 'min' in constraints:
            violations = df.filter(pl.col(col) < constraints['min'])
            if len(violations) > 0:
                issues.append(f"Column '{col}' has {len(violations)} values < {constraints['min']}")
        
        if 'max' in constraints:
            violations = df.filter(pl.col(col) > constraints['max'])
            if len(violations) > 0:
                issues.append(f"Column '{col}' has {len(violations)} values > {constraints['max']}")
        
        if 'allowed' in constraints:
            violations = df.filter(~pl.col(col).is_in(constraints['allowed']))
            if len(violations) > 0:
                issues.append(f"Column '{col}' has {len(violations)} invalid values")
    
    # Check for nulls in required columns
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            null_count = df[col].null_count()
            if null_count > 0:
                issues.append(f"Column '{col}' has {null_count} null values")
    
    result = {
        'valid': len(issues) == 0,
        'issues': issues,
        'row_count': len(df),
        'schema_name': schema_name
    }
    
    if not result['valid']:
        logger.warning(f"Validation failed for {schema_name}: {issues}")
    else:
        logger.info(f"Validation passed for {schema_name}")
    
    return result
```

### Section 6.4: Library-Specific Patterns

**Polars Optimization Patterns:**
```python
# Pattern 1: Lazy evaluation for large files
df = (
    pl.scan_csv("data/1_raw/large_file.csv")
    .filter(pl.col('year') >= 2020)
    .select(['date', 'disease', 'case_count'])
    .collect()  # Execute only once
)

# Pattern 2: Method chaining for readability
df_clean = (
    df.clone()
    .drop_nulls(subset=['date', 'case_count'])
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('disease').cast(pl.Categorical),
        pl.col('case_count').cast(pl.Int32)
    ])
    .filter(pl.col('case_count') > 0)
    .sort('date')
)

# Pattern 3: Window functions for time series
df_with_moving_avg = df.with_columns([
    pl.col('case_count')
      .rolling_mean(window_size=4, center=True)
      .over('disease')
      .alias('moving_avg_4wk')
])

# Pattern 4: Efficient aggregations
summary = (
    df.group_by(['disease', 'region', 'year'])
    .agg([
        pl.sum('case_count').alias('total_cases'),
        pl.mean('case_count').alias('avg_weekly_cases'),
        pl.max('case_count').alias('peak_week')
    ])
)

# Pattern 5: Memory-efficient dtypes
df = df.with_columns([
    pl.col('case_count').cast(pl.Int32),  # not Int64
    pl.col('disease').cast(pl.Categorical),  # for low-cardinality
    pl.col('year').cast(pl.Int16)  # if range is small
])
```

**Logging Patterns:**
```python
from loguru import logger
from datetime import datetime

# Configure logger with rotation
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
logger.add(
    f"logs/etl/extraction_{timestamp}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

# Structured logging
logger.info(f"Starting extraction | diseases={len(diseases)} | date_range={start_date} to {end_date}")
logger.info(f"Extracted data | rows={len(df)} | columns={df.columns}")
logger.warning(f"Data quality issue | null_count={null_count} | column={col_name}")
logger.error(f"Extraction failed | error={str(e)} | source={data_source}")
```

**Configuration Loading:**
```python
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = "config/analysis.yml") -> Dict[str, Any]:
    """Load configuration with validation."""
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Validate required keys
    required_keys = ['data', 'analysis', 'output']
    missing = set(required_keys) - set(config.keys())
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")
    
    return config

# Usage
config = load_config()
target_diseases = config['data']['target_diseases']
output_dir = Path(config['output']['results_dir'])
```

---

## Testing Patterns

### Unit Test Examples

```python
# tests/unit/test_data_processing.py
import polars as pl
import pytest
from src.data_processing.cleaning import remove_duplicates, validate_date_range

class TestDataCleaning:
    """Test suite for data cleaning functions."""
    
    def test_remove_duplicates_success(self):
        """Should remove duplicate rows based on subset columns."""
        # Arrange
        df = pl.DataFrame({
            'id': [1, 1, 2, 3],
            'value': [10, 10, 20, 30],
            'other': ['a', 'b', 'c', 'd']
        })
        
        # Act
        result = remove_duplicates(df, subset=['id', 'value'])
        
        # Assert
        assert len(result) == 3
        assert result['id'].to_list() == [1, 2, 3]
    
    def test_validate_date_range_valid(self):
        """Should accept valid date range."""
        start = "2023-01-01"
        end = "2023-12-31"
        
        result = validate_date_range(start, end)
        
        assert result == True
    
    def test_validate_date_range_invalid_order(self):
        """Should raise ValueError when start > end."""
        start = "2023-12-31"
        end = "2023-01-01"
        
        with pytest.raises(ValueError, match="start_date must be before end_date"):
            validate_date_range(start, end)
    
    def test_validate_date_range_invalid_format(self):
        """Should raise ValueError for invalid date format."""
        start = "2023/01/01"  # Wrong format
        end = "2023-12-31"
        
        with pytest.raises(ValueError, match="must be in YYYY-MM-DD format"):
            validate_date_range(start, end)
```

### Data Quality Test Examples

```python
# tests/data/test_disease_data_quality.py
import polars as pl
import pytest
from pathlib import Path

class TestDiseaseDataQuality:
    """Data quality tests for disease surveillance data."""
    
    @pytest.fixture
    def disease_data(self):
        """Load disease data for testing."""
        return pl.read_csv('data/1_raw/disease_data.csv')
    
    def test_schema_completeness(self, disease_data):
        """All required columns must be present."""
        required = ['date', 'disease', 'case_count', 'region']
        missing = set(required) - set(disease_data.columns)
        assert len(missing) == 0, f"Missing columns: {missing}"
    
    def test_data_types(self, disease_data):
        """Columns must have correct data types."""
        assert disease_data['case_count'].dtype == pl.Int32
        assert disease_data['disease'].dtype == pl.Categorical
    
    def test_no_nulls_in_required_fields(self, disease_data):
        """Required fields cannot have null values."""
        required = ['date', 'disease', 'case_count']
        for col in required:
            null_count = disease_data[col].null_count()
            assert null_count == 0, f"Column '{col}' has {null_count} nulls"
    
    def test_case_count_range(self, disease_data):
        """Case counts must be non-negative and reasonable."""
        assert disease_data['case_count'].min() >= 0
        assert disease_data['case_count'].max() <= 100000
    
    def test_disease_values(self, disease_data):
        """Disease names must be from allowed list."""
        allowed = {'Dengue', 'HFMD', 'Chickenpox', 'TB'}
        actual = set(disease_data['disease'].unique())
        invalid = actual - allowed
        assert len(invalid) == 0, f"Invalid diseases: {invalid}"
    
    def test_date_range(self, disease_data):
        """Dates must be within expected range."""
        df_parsed = disease_data.with_columns(
            pl.col('date').str.strptime(pl.Date, '%Y-%m-%d')
        )
        min_date = df_parsed['date'].min()
        max_date = df_parsed['date'].max()
        
        assert min_date >= pl.date(2012, 1, 1)
        assert max_date <= pl.date(2026, 12, 31)
```

### Integration Test Example

```python
# tests/integration/test_etl_pipeline.py
import polars as pl
import pytest
from pathlib import Path
from scripts.run_etl import run_complete_pipeline

class TestETLPipeline:
    """End-to-end tests for ETL pipeline."""
    
    def test_complete_pipeline_execution(self, tmp_path):
        """Pipeline should execute successfully end-to-end."""
        # Arrange
        config = {
            'input_dir': 'data/1_raw',
            'output_dir': str(tmp_path),
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }
        
        # Act
        result = run_complete_pipeline(config)
        
        # Assert
        assert result['status'] == 'success'
        assert result['rows_processed'] > 0
        assert (tmp_path / 'cleaned_data.parquet').exists()
    
    def test_pipeline_output_quality(self, tmp_path):
        """Pipeline output should meet quality standards."""
        config = {'output_dir': str(tmp_path)}
        run_complete_pipeline(config)
        
        # Load output
        df = pl.read_parquet(tmp_path / 'cleaned_data.parquet')
        
        # Quality checks
        assert len(df) > 0
        assert df['case_count'].null_count() == 0
        assert df['case_count'].min() >= 0
```

---

## Security Patterns

### PII/PHI Anonymization

```python
import hashlib
import polars as pl
from typing import Literal

def anonymize_pii(
    df: pl.DataFrame,
    pii_columns: list[str],
    method: Literal['hash', 'mask', 'remove'] = 'hash'
) -> pl.DataFrame:
    """Anonymize PII fields in DataFrame.
    
    Args:
        df: Input DataFrame
        pii_columns: List of columns containing PII
        method: Anonymization method ('hash', 'mask', 'remove')
    
    Returns:
        DataFrame with anonymized PII
    """
    df_anon = df.clone()
    
    for col in pii_columns:
        if col not in df.columns:
            continue
        
        if method == 'hash':
            df_anon = df_anon.with_columns(
                pl.col(col)
                .apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16])
                .alias(col)
            )
        elif method == 'mask':
            df_anon = df_anon.with_columns(
                pl.lit('***REDACTED***').alias(col)
            )
        elif method == 'remove':
            df_anon = df_anon.drop(col)
    
    return df_anon

# Usage
SENSITIVE_FIELDS = ['nric', 'name', 'date_of_birth', 'address']
df_safe = anonymize_pii(df_raw, SENSITIVE_FIELDS, method='hash')
```

### Credential Management

```python
import os
from pathlib import Path
from dotenv import load_dotenv

def load_credentials() -> dict:
    """Load credentials from environment variables."""
    # Load from .env file (not committed to git)
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
    
    # Retrieve credentials
    credentials = {
        'db_host': os.getenv('DB_HOST'),
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'api_key': os.getenv('API_KEY')
    }
    
    # Validate all required credentials present
    missing = [k for k, v in credentials.items() if v is None]
    if missing:
        raise ValueError(f"Missing required credentials: {missing}")
    
    return credentials

# Example .env file (NEVER commit this):
# DB_HOST=localhost
# DB_USER=analytics_user
# DB_PASSWORD=secure_password_here
# API_KEY=your_api_key_here
```

---

## Common Anti-Patterns

### ❌ DON'T: Incomplete Code

```python
# BAD - Stub function
def process_data(df):
    # TODO: implement cleaning logic
    pass

# BAD - Missing imports
def load_data(file_path):
    df = pl.read_csv(file_path)  # Where is 'pl' imported from?
    return df

# BAD - No error handling
def extract_data(source):
    df = database.query(source)  # What if connection fails?
    return df
```

### ✅ DO: Complete, Executable Code

```python
# GOOD - Fully implemented
import polars as pl
from loguru import logger
from typing import Optional

def process_data(df: pl.DataFrame) -> pl.DataFrame:
    """Clean and validate disease surveillance data."""
    try:
        df_clean = (
            df.drop_nulls(subset=['date', 'case_count'])
            .with_columns([
                pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
                pl.col('disease').cast(pl.Categorical)
            ])
            .filter(pl.col('case_count') >= 0)
        )
        logger.info(f"Processed {len(df_clean)} records")
        return df_clean
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
```

### ❌ DON'T: Hardcoded Values

```python
# BAD - Hardcoded configuration
diseases = ['Dengue', 'HFMD']
start_date = '2023-01-01'
output_path = '/Users/john/project/output.csv'
```

### ✅ DO: Config-Driven

```python
# GOOD - Configuration-driven
import yaml

with open('config/analysis.yml') as f:
    config = yaml.safe_load(f)

diseases = config['data']['target_diseases']
start_date = config['analysis']['start_date']
output_path = Path(config['output']['results_dir']) / 'output.csv'
```

### ❌ DON'T: Silent Failures

```python
# BAD - No logging of data quality issues
df = df.drop_nulls()  # How many rows were dropped?
df = df.filter(pl.col('value') > 0)  # How many filtered out?
```

### ✅ DO: Explicit Logging

```python
# GOOD - Log all transformations
from loguru import logger

initial_count = len(df)
df = df.drop_nulls()
null_dropped = initial_count - len(df)
logger.info(f"Dropped {null_dropped} rows with nulls ({null_dropped/initial_count:.1%})")

before_filter = len(df)
df = df.filter(pl.col('value') > 0)
filtered = before_filter - len(df)
logger.info(f"Filtered {filtered} rows with value <= 0")
```

---

## Package Management

### Using uv (MANDATORY)

```bash
# Install packages (NOT pip install)
uv pip install polars>=0.20.0
uv pip install loguru>=0.7.0
uv pip install pydantic>=2.0.0
uv pip install pytest>=7.0.0

# Install from requirements
uv pip install -r requirements.txt

# Update requirements after adding packages
uv pip freeze > requirements.txt

# Install in editable mode (for local development)
uv pip install -e .
```

### Requirements.txt Structure

```txt
# Data processing
polars>=0.20.0
pyarrow>=12.0.0

# Configuration and logging
pyyaml>=6.0
loguru>=0.7.0

# Validation
pydantic>=2.0.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0

# Analysis (optional, install as needed)
scipy>=1.11.0
scikit-learn>=1.3.0
```

---

## Performance Optimization

### Memory Management

```python
# Monitor memory usage
import polars as pl
from loguru import logger

# Use lazy evaluation for large files
df = pl.scan_csv("large_file.csv")  # Doesn't load into memory immediately
result = (
    df.filter(pl.col('year') >= 2020)
    .select(['date', 'value'])
    .collect()  # Execute query optimally
)

# Use optimized dtypes
df = df.with_columns([
    pl.col('small_int').cast(pl.Int16),  # Instead of Int64
    pl.col('category').cast(pl.Categorical),  # For low-cardinality
])

# Log memory usage
memory_mb = df.estimated_size() / 1024 / 1024
logger.info(f"DataFrame size: {memory_mb:.2f} MB")
```

### Execution Time Optimization

```python
import time
from loguru import logger

def timed_operation(func):
    """Decorator to time function execution."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper

@timed_operation
def process_large_dataset(df: pl.DataFrame) -> pl.DataFrame:
    """Process dataset with timing."""
    return df.with_columns([
        pl.col('value').rolling_mean(window_size=7).alias('ma_7d')
    ])
```

---

This reference guide should be used alongside the main prompt to provide detailed examples and patterns for implementation plan creation.
