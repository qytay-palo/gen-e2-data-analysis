---
name: 'Python Standards for Data Analysis'
description: 'Coding conventions for Python files'
applyTo: '**/*.py, **/*.ipynb'
---
## 1. Code Organization and Structure

### Project Structure
- Follow a consistent directory structure separating raw data, processed data, notebooks, scripts, and source code
- Use `src/` for reusable modules, `scripts/` for one-off tasks, `notebooks/` for exploratory analysis
- Store parameter files (JSON, YAML) in relevant data folders (e.g., `data/schemas/`, `data/parameters/`)
- Store all outputs (figures, tables, models) in a `results/` or `outputs/` directory

### Module Design
- **Single Responsibility Principle**: Each function/class should do one thing well
- **DRY (Don't Repeat Yourself)**: Extract repeated code into reusable functions
- Use meaningful, descriptive names: `calculate_disease_burden()` not `calc_db()`
- Keep functions short (< 50 lines) and focused on a single task
- Group related functions into modules with clear purposes

### Package Structure
```python
# Good: Clear imports and structure
from src.data_processing.validation import validate_date_range
from src.analysis.trend_analysis import detect_seasonal_patterns

# Avoid: Unclear star imports
from src.data_processing import *
```

## 2. Data Handling Best Practices

### Data Loading and Validation
- **Always validate input data** upon loading
- Check for expected columns, data types, and ranges
- Handle missing values explicitly - never ignore them silently
- Document data assumptions and constraints

```python
def load_disease_data(filepath: str) -> pl.DataFrame:
    """Load and validate disease surveillance data.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Validated DataFrame
        
    Raises:
        ValueError: If required columns are missing or data is invalid
    """
    df = pl.read_csv(filepath)
    
    # Validate required columns
    required_cols = ['disease', 'date', 'case_count']
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Validate data types and ranges
    df = df.with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d', strict=False),
        pl.col('case_count').cast(pl.Int64, strict=False)
    ])
    
    if df['case_count'].null_count() > 0:
        raise ValueError("Invalid case_count values found")
    
    return df
```

### Data Processing Pipeline
- **Immutability**: Avoid modifying DataFrames in-place when possible
- Use method chaining for readability
- Create intermediate checkpoints for complex transformations
- Save processed data with clear versioning

```python
# Good: Clear pipeline with intermediate results
df_processed = (
    df_raw
    .clone()
    .drop_nulls(subset=['critical_column'])
    .with_columns([
        pl.col('date').dt.year().alias('year'),
        pl.col('date').dt.month().alias('month')
    ])
    .filter(pl.col('year') >= 2020)
    .sort(['disease', 'date'])
)

# Save intermediate results
df_processed.write_csv('data/3_interim/cleaned_data.csv')
```

### Memory Management
- Use appropriate data types: `Int32` instead of `Int64`, `Categorical` for categorical data
- Process large datasets in chunks or use lazy evaluation (`pl.scan_csv()`) when memory is constrained
- Delete unnecessary DataFrames explicitly with `del` when done
- Use `pl.read_csv(..., columns=[...])` to load only needed columns
- Leverage Polars' lazy evaluation for efficient query optimization

### Advanced Polars Patterns

#### Window Functions for Time Series
```python
# Calculate rolling metrics by disease
df_with_trends = df.with_columns([
    pl.col('cases').rolling_mean(window_size=4).over('disease').alias('cases_4wk_avg'),
    pl.col('cases').rolling_std(window_size=4).over('disease').alias('cases_4wk_std'),
    (pl.col('cases') - pl.col('cases').shift(1)).over('disease').alias('cases_change')
])

# Rank diseases by burden within each year
df_ranked = df.group_by(['year', 'disease']).agg(
    pl.col('cases').sum().alias('total_cases')
).with_columns(
    pl.col('total_cases').rank(descending=True).over('year').alias('burden_rank')
)
```

#### Efficient Joins and Merging
```python
# Left join with validation
df_merged = (
    disease_data
    .join(population_data, on=['region', 'year'], how='left')
    .with_columns([
        # Check for missing population data
        pl.col('population').is_null().alias('missing_population')
    ])
)

if df_merged['missing_population'].any():
    logger.warning(f"Found {df_merged['missing_population'].sum()} regions with missing population")

# Anti-join to find unmatched records
unmatched = disease_data.join(
    population_data, on=['region', 'year'], how='anti'
)
```

#### Streaming for Large Datasets
```python
# Use streaming for datasets larger than RAM
result = (
    pl.scan_csv('very_large_file.csv')
    .filter(pl.col('year') >= 2020)
    .group_by(['disease', 'year']).agg([
        pl.col('cases').sum().alias('total_cases'),
        pl.col('cases').mean().alias('mean_cases')
    ])
    .collect(streaming=True)  # Process in batches
)
```

## 3. Data Validation with Polars

### Schema Validation with Polars
- Use Polars expressions for data validation in production pipelines
- Catch data quality issues early with explicit validation functions
- Document expected data structure in code
- Generate detailed validation reports

```python
import polars as pl
from typing import List, Dict
from datetime import date

class SchemaValidationError(Exception):
    """Raised when data fails schema validation."""
    pass

def validate_disease_schema(df: pl.DataFrame) -> pl.DataFrame:
    """Validate disease surveillance data schema.
    
    Args:
        df: Input DataFrame to validate
        
    Returns:
        Validated DataFrame with correct types
        
    Raises:
        SchemaValidationError: If validation fails
    """
    errors = []
    
    # Define expected schema
    expected_columns = ['disease', 'date', 'cases', 'region']
    allowed_diseases = ['COVID-19', 'Dengue', 'Tuberculosis', 'Influenza']
    min_date = date(2020, 1, 1)
    max_date = date.today()
    
    # Check required columns exist
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise SchemaValidationError(f"Missing required columns: {missing_cols}")
    
    # Validate data types and constraints
    try:
        df = df.with_columns([
            pl.col('disease').cast(pl.Utf8),
            pl.col('date').str.strptime(pl.Date, format='%Y-%m-%d', strict=False),
            pl.col('cases').cast(pl.Int64, strict=False),
            pl.col('region').cast(pl.Utf8)
        ])
    except Exception as e:
        raise SchemaValidationError(f"Type casting failed: {e}")
    
    # Validate disease values
    invalid_diseases = df.filter(
        ~pl.col('disease').is_in(allowed_diseases)
    )
    if invalid_diseases.height > 0:
        errors.append(
            f"Found {invalid_diseases.height} rows with invalid diseases. "
            f"Allowed: {allowed_diseases}"
        )
    
    # Validate date ranges
    invalid_dates = df.filter(
        (pl.col('date') < min_date) | (pl.col('date') > max_date)
    )
    if invalid_dates.height > 0:
        errors.append(
            f"Found {invalid_dates.height} rows with dates outside "
            f"valid range [{min_date}, {max_date}]"
        )
    
    # Validate null values
    null_checks = {
        'disease': df['disease'].null_count(),
        'date': df['date'].null_count(),
        'cases': df['cases'].null_count(),
        'region': df['region'].null_count()
    }
    null_cols = {col: count for col, count in null_checks.items() if count > 0}
    if null_cols:
        errors.append(f"Found null values: {null_cols}")
    
    # Validate cases range
    invalid_cases = df.filter(
        (pl.col('cases') < 0) | (pl.col('cases') >= 100000)
    )
    if invalid_cases.height > 0:
        errors.append(
            f"Found {invalid_cases.height} rows with cases outside valid range [0, 100000)"
        )
    
    if errors:
        raise SchemaValidationError(f"Validation failed: {'; '.join(errors)}")
    
    logger.info(f"Schema validation passed for {df.height} rows")
    return df

def load_and_validate(filepath: str) -> pl.DataFrame:
    """Load data with automatic schema validation.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Validated DataFrame
        
    Raises:
        SchemaValidationError: If validation fails
    """
    df = pl.read_csv(filepath)
    
    try:
        validated_df = validate_disease_schema(df)
        logger.info(f"Data validation passed for {filepath}")
        return validated_df
    except SchemaValidationError as e:
        logger.error(f"Schema validation failed for {filepath}: {e}")
        raise
```

### Custom Data Quality Checks
```python
class DataQualityError(Exception):
    """Raised when data fails quality checks."""
    pass

def validate_disease_data_quality(df: pl.DataFrame) -> None:
    """Run comprehensive data quality checks.
    
    Raises:
        DataQualityError: If data fails quality thresholds
    """
    issues = []
    
    # Check for duplicates
    duplicate_count = df.is_duplicated().sum()
    if duplicate_count > 0:
        issues.append(f"Found {duplicate_count} duplicate rows")
    
    # Check for temporal gaps
    df_sorted = df.sort('date')
    date_gaps = df_sorted['date'].diff().dt.days()
    large_gaps = (date_gaps > 14).sum()  # More than 2 weeks
    if large_gaps > 0:
        issues.append(f"Found {large_gaps} time gaps exceeding 2 weeks")
    
    # Check for outliers using IQR
    q1 = df['cases'].quantile(0.25)
    q3 = df['cases'].quantile(0.75)
    iqr = q3 - q1
    outliers = ((df['cases'] < (q1 - 3 * iqr)) | (df['cases'] > (q3 + 3 * iqr))).sum()
    if outliers > df.height * 0.01:  # More than 1% outliers
        issues.append(f"Found {outliers} extreme outliers ({outliers/df.height*100:.1f}%)")
    
    if issues:
        raise DataQualityError(f"Data quality issues: {'; '.join(issues)}")
    
    logger.info("All data quality checks passed")
```

## 4. Type Hints and Documentation

### Type Annotations
- **Always use type hints** for function parameters and return values
- Use `typing` module for complex types
- Helps catch bugs early and improves code readability

```python
from typing import List, Dict, Optional, Tuple
import polars as pl
import numpy as np

def calculate_incidence_rate(
    cases: pl.Series,
    population: int,
    multiplier: int = 100_000
) -> np.ndarray:
    """Calculate incidence rate per population."""
    return (cases / population) * multiplier

def aggregate_by_disease(
    df: pl.DataFrame,
    groupby_cols: List[str]
) -> Dict[str, pl.DataFrame]:
    """Aggregate data by disease categories."""
    return {name: group for name, group in df.groupby(groupby_cols)}
```

### Docstrings
- Use **Google or NumPy style docstrings** consistently
- Document parameters, return values, and exceptions
- Include example usage for complex functions
- Explain the "why" not just the "what"

```python
def detect_outbreak(
    time_series: pl.Series,
    threshold_std: float = 2.0,
    window: int = 4
) -> pl.Series:
    """Detect potential disease outbreaks using moving statistics.
    
    Identifies weeks where case counts exceed the moving average by
    more than threshold_std standard deviations, indicating potential
    outbreak conditions.
    
    Args:
        time_series: Weekly case counts indexed by date
        threshold_std: Number of standard deviations above mean to flag
        window: Size of rolling window in weeks for calculating baseline
        
    Returns:
        Boolean series where True indicates potential outbreak week
        
    Raises:
        ValueError: If time_series contains negative values
        
    Example:
        >>> cases = pl.Series([10, 12, 11, 45, 50, 15, 12])
        >>> outbreaks = detect_outbreak(cases, threshold_std=2.0)
        >>> print(outbreaks.sum())  # Count of outbreak weeks
        2
    """
    if (time_series < 0).any():
        raise ValueError("Case counts cannot be negative")
    
    rolling_mean = time_series.rolling(window=window).mean()
    rolling_std = time_series.rolling(window=window).std()
    
    threshold = rolling_mean + (threshold_std * rolling_std)
    return time_series > threshold
```

## 5. Error Handling and Logging

### Exception Handling
- Use specific exception types, not bare `except:`
- Provide informative error messages with context
- Fail fast - validate inputs early
- Use custom exceptions for domain-specific errors

```python
# Domain-specific exception hierarchy
class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass

class OutbreakDetectionError(Exception):
    """Raised when outbreak detection algorithm fails."""
    pass

class DataQualityError(Exception):
    """Raised when data fails quality checks."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass

def process_disease_data(df: pl.DataFrame) -> pl.DataFrame:
    """Process disease surveillance data with validation."""
    try:
        # Validate data structure
        if df.empty:
            raise DataValidationError("Input DataFrame is empty")
        
        if 'date' not in df.columns:
            raise DataValidationError("Missing required 'date' column")
        
        # Process data
        df['date'] = pl.to_datetime(df['date'], errors='coerce')
        
        # Check for conversion failures
        invalid_dates = df['date'].null_count()
        if invalid_dates > 0:
            raise DataValidationError(
                f"Found {invalid_dates} invalid date values"
            )
        
        return df
        
    except pl.exceptions.ComputeError as e:
        raise DataValidationError(f"Failed to parse data: {e}") from e
    except Exception as e:
        # Log unexpected errors for debugging
        logger.error(f"Unexpected error processing data: {e}")
        raise
```

### Logging
- Use Python's `logging` module, not `print()` statements
- Set appropriate log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include context in log messages (function name, relevant IDs)
- Configure logging from a central location

```python
import logging

# Configure at module level
logger = logging.getLogger(__name__)

def calculate_metrics(disease: str, df: pl.DataFrame) -> Dict:
    """Calculate disease burden metrics."""
    logger.info(f"Calculating metrics for {disease}")
    logger.debug(f"Input data shape: {df.shape}")
    
    try:
        metrics = {
            'total_cases': df['cases'].sum(),
            'mean_weekly': df['cases'].mean()
        }
        logger.info(f"Successfully calculated {len(metrics)} metrics")
        return metrics
        
    except KeyError as e:
        logger.error(f"Missing required column for {disease}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error calculating metrics: {e}")
        raise
```

## 5. Testing and Quality Assurance

### Unit Testing
- Write tests for all business logic and data transformations
- Use `pytest` for testing framework
- Aim for >80% code coverage
- Test edge cases, not just happy paths

```python
import pytest
import polars as pl
from src.analysis.trend_analysis import detect_outbreak

def test_detect_outbreak_with_spike():
    """Test outbreak detection identifies clear spike."""
    cases = pl.Series('cases', [10, 10, 10, 50, 10, 10])
    result = detect_outbreak(cases, threshold_std=2.0, window=3)
    assert result[3] == True  # Spike should be detected

def test_detect_outbreak_with_negative_values():
    """Test that negative values raise ValueError."""
    cases = pl.Series('cases', [10, -5, 10])
    with pytest.raises(ValueError, match="cannot be negative"):
        detect_outbreak(cases)

def test_detect_outbreak_empty_series():
    """Test handling of empty input."""
    cases = pl.Series('cases', [], dtype=pl.Float64)
    result = detect_outbreak(cases)
    assert len(result) == 0
```

### Data Quality Checks
- Implement automated data quality checks in pipelines
- Check for duplicates, nulls, outliers, and inconsistencies
- Document data quality issues and handling strategies
- Create data quality reports

```python
def run_data_quality_checks(df: pl.DataFrame) -> Dict[str, any]:
    """Run comprehensive data quality checks."""
    quality_report = {
        'total_rows': len(df),
        'duplicate_rows': df.is_duplicated().sum(),
        'missing_values': {col: df[col].null_count() for col in df.columns},
        'negative_values': {col: (df[col] < 0).sum() for col in df.select(pl.col(pl.NUMERIC_DTYPES)).columns},
        'date_range': {
            'min': df['date'].min() if 'date' in df.columns else None,
            'max': df['date'].max() if 'date' in df.columns else None
        }
    }
    
    logger.info(f"Data quality report: {quality_report}")
    return quality_report
```

## 6. Performance Optimization

### Performance Profiling
- Profile before optimizing - measure, don't guess
- Use appropriate profiling tools for different bottlenecks
- Focus on the 20% of code that takes 80% of time

```python
import time
from functools import wraps
from line_profiler import profile
import memory_profiler

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed:.3f} seconds")
        return result
    return wrapper

@timing_decorator
def process_large_dataset(df: pl.DataFrame) -> pl.DataFrame:
    """Process dataset with timing."""
    return df.with_columns([
        (pl.col('cases') / pl.col('population') * 100000).alias('rate')
    ])

# Line-by-line profiling for CPU bottlenecks
@profile
def analyze_disease_burden(df: pl.DataFrame) -> pl.DataFrame:
    """Detailed line-by-line profiling."""
    # Each line's execution time will be measured
    filtered = df.filter(pl.col('cases') > 0)
    grouped = filtered.group_by('disease').agg(pl.col('cases').sum())
    sorted_df = grouped.sort('cases', descending=True)
    return sorted_df

# Memory profiling
@memory_profiler.profile
def memory_intensive_operation(filepath: str) -> pl.DataFrame:
    """Profile memory usage line by line."""
    df = pl.read_csv(filepath)
    df_processed = df.with_columns([
        pl.col('cases').rolling_mean(window_size=52)
    ])
    return df_processed

# Context manager for timing blocks
from contextlib import contextmanager

@contextmanager
def timer(operation_name: str):
    """Time a block of code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    logger.info(f"{operation_name} completed in {elapsed:.3f} seconds")

# Usage
with timer("Data loading and processing"):
    df = pl.read_csv('large_file.csv')
    df_processed = process_data(df)
```

### Vectorization
- Use vectorized Polars expressions instead of loops
- Leverage Polars' expression API for efficient transformations
- Use `@njit` from numba for computationally intensive custom operations

```python
# Bad: Slow loop
for row in df.iter_rows(named=True):
    # Don't iterate and mutate!
    pass

# Good: Vectorized operation using Polars expressions
df = df.with_columns(
    ((pl.col('cases') / pl.col('population')) * 100000).alias('rate')
)

# Also good: Using lazy evaluation for large datasets
df_lazy = pl.scan_csv('data.csv')
df_result = df_lazy.with_columns(
    ((pl.col('cases') / pl.col('population')) * 100000).alias('rate')
).collect()
```

### Efficient Data Operations
- Use Categorical data types for repeated string values
- Leverage Polars expressions for efficient filtering and transformations
- Use lazy evaluation (`scan_csv`, `scan_parquet`) for large datasets
- Consider Polars' streaming engine for datasets that don't fit in memory

```python
# Optimize data types
df = df.with_columns([
    pl.col('disease').cast(pl.Categorical),
    pl.col('year').cast(pl.Int16)
])

# Fast filtering with expressions
high_burden = df.filter(
    (pl.col('case_count') > threshold) & (pl.col('year') >= 2020)
)

# Fast arithmetic with expressions
df = df.with_columns(
    ((pl.col('cases') / pl.col('population')) * 100000).alias('incidence_rate')
)

# Lazy evaluation for large files
df = pl.scan_csv('large_file.csv').filter(
    pl.col('year') >= 2020
).collect()
```

### Parallel Processing
- Use parallel processing for independent operations across diseases/regions
- Balance overhead vs. speedup - not worth it for small datasets
- Consider memory implications of multiple processes

```python
from joblib import Parallel, delayed
import multiprocessing as mp
from typing import List

def analyze_single_disease(
    disease: str,
    df: pl.DataFrame,
    config: AnalysisConfig
) -> dict:
    """Analyze a single disease - can be parallelized."""
    disease_df = df.filter(pl.col('disease') == disease)
    
    return {
        'disease': disease,
        'total_cases': disease_df['cases'].sum(),
        'mean_cases': disease_df['cases'].mean(),
        'peak_week': disease_df.sort('cases', descending=True)[0, 'date']
    }

# Parallel processing of multiple diseases
def analyze_all_diseases_parallel(
    df: pl.DataFrame,
    diseases: List[str],
    config: AnalysisConfig,
    n_jobs: int = -1
) -> List[dict]:
    """Analyze multiple diseases in parallel.
    
    Args:
        df: Disease surveillance data
        diseases: List of diseases to analyze
        config: Analysis configuration
        n_jobs: Number of parallel jobs (-1 = all cores)
        
    Returns:
        List of analysis results for each disease
    """
    logger.info(f"Analyzing {len(diseases)} diseases in parallel")
    
    results = Parallel(n_jobs=n_jobs, verbose=1)(
        delayed(analyze_single_disease)(disease, df, config)
        for disease in diseases
    )
    
    logger.info(f"Completed parallel analysis of {len(results)} diseases")
    return results

# For CPU-intensive operations with shared memory
def parallel_regions_analysis(df: pl.DataFrame) -> pl.DataFrame:
    """Analyze regions in parallel using multiprocessing."""
    regions = df['region'].unique().to_list()
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            analyze_single_disease,
            [(region, df.filter(pl.col('region') == region)) for region in regions]
        )
    
    return pl.DataFrame(results)
```

## 7. Configuration Management

### Type-Safe Configuration with Pydantic
- Use Pydantic for validated, type-safe configuration
- Prevent configuration errors at startup
- Document all configuration options
- Support multiple configuration sources (files, environment variables)

```python
from pydantic import BaseModel, Field, validator
from pathlib import Path
from typing import List, Optional
import yaml

class AnalysisConfig(BaseModel):
    """Configuration for disease burden analysis."""
    
    # Analysis parameters
    outbreak_threshold_std: float = Field(
        default=2.0,
        gt=0,
        description="Standard deviations above baseline for outbreak detection"
    )
    rolling_window_weeks: int = Field(
        default=4,
        gt=0,
        le=52,
        description="Window size for rolling statistics"
    )
    min_cases_for_analysis: int = Field(
        default=10,
        ge=0,
        description="Minimum cases required to perform analysis"
    )
    
    # Data paths
    data_path: Path = Field(default=Path('data/1_raw'))
    output_path: Path = Field(default=Path('results'))
    
    # Disease list
    diseases: List[str] = Field(
        default=['COVID-19', 'Dengue', 'Tuberculosis', 'Influenza']
    )
    
    class Config:
        frozen = True  # Immutable after creation
        extra = 'forbid'  # Reject unknown parameters
    
    @validator('data_path', 'output_path')
    def validate_paths_exist(cls, v):
        """Ensure paths exist."""
        if not v.exists():
            raise ValueError(f"Path does not exist: {v}")
        return v

def load_config(config_path: str = 'config/analysis.yml') -> AnalysisConfig:
    """Load and validate configuration from YAML file.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Validated configuration object
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    try:
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        config = AnalysisConfig(**config_dict)
        logger.info(f"Loaded configuration from {config_path}")
        return config
        
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return AnalysisConfig()
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e

# Usage
config = load_config()
threshold = config.outbreak_threshold_std
window = config.rolling_window_weeks
```

## 8. Parameters and Constants Management

### Define Parameters as Constants or Load from Data Folders
- Store reusable parameters as module-level constants in your code
- For complex parameters, store in JSON/YAML files within data folders (e.g., `data/parameters/`, `data/schemas/`)
- Never hardcode magic numbers without clear naming
- Use environment variables for secrets only
- Document parameter choices and rationale

```python
import json
from pathlib import Path
from typing import Dict

# Module-level constants
BASE_DATA_PATH = Path('data')
OUTBREAK_THRESHOLD_STD = 2.0  # Number of std deviations above baseline
ROLLING_WINDOW_WEEKS = 4  # Window for moving averages
HIGH_INCIDENCE_CUTOFF = 100  # Cases per 100k population (WHO definition)

def load_disease_parameters(disease: str) -> Dict:
    """Load disease-specific parameters from data folder."""
    param_file = BASE_DATA_PATH / 'parameters' / f'{disease.lower()}_params.json'
    
    if not param_file.exists():
        raise FileNotFoundError(f"Parameters not found: {param_file}")
    
    with open(param_file, 'r') as f:
        params = json.load(f)
    
    # Validate required keys
    required_keys = ['incubation_period', 'infectious_period']
    missing = set(required_keys) - set(params.keys())
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")
    
    return params

# Usage
disease_params = load_disease_parameters('COVID-19')
incubation_days = disease_params['incubation_period']
```

## 9. Data Lineage and Provenance

### Track Data Transformations
- Document all data transformations for audit trails
- Log inputs, outputs, and parameters for each processing step
- Enable reproducibility and debugging

```python
from datetime import datetime
from typing import Any, Callable
import json

class DataLineage:
    """Track data transformation lineage."""
    
    def __init__(self, lineage_file: str = 'logs/audit/data_lineage.jsonl'):
        self.lineage_file = Path(lineage_file)
        self.lineage_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_transformation(
        self,
        step_name: str,
        input_data: pl.DataFrame,
        output_data: pl.DataFrame,
        parameters: dict,
        user: str = 'automated'
    ) -> None:
        """Log a data transformation step."""
        lineage_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step_name,
            'user': user,
            'input_shape': input_data.shape,
            'output_shape': output_data.shape,
            'rows_added': output_data.height - input_data.height,
            'columns_added': output_data.width - input_data.width,
            'parameters': parameters
        }
        
        with open(self.lineage_file, 'a') as f:
            f.write(json.dumps(lineage_entry) + '\n')
        
        logger.info(f"Lineage logged: {step_name}")

def transform_with_lineage(
    df: pl.DataFrame,
    transform_func: Callable,
    step_name: str,
    **kwargs
) -> pl.DataFrame:
    """Apply transformation with automatic lineage tracking."""
    logger.info(f"Starting: {step_name} | Input shape: {df.shape}")
    
    result = transform_func(df, **kwargs)
    
    logger.info(f"Completed: {step_name} | Output shape: {result.shape}")
    
    # Log lineage
    lineage = DataLineage()
    lineage.log_transformation(
        step_name=step_name,
        input_data=df,
        output_data=result,
        parameters=kwargs
    )
    
    return result

# Usage
df_cleaned = transform_with_lineage(
    df_raw,
    clean_disease_data,
    step_name="initial_cleaning",
    remove_duplicates=True,
    fill_missing='forward'
)
```

## 10. SQL Integration and Database Operations

### Parameterized Queries
- Always use parameterized queries to prevent SQL injection
- Use connection pooling for better performance
- Handle database errors gracefully

```python
import polars as pl
from sqlalchemy import create_engine, text
from contextlib import contextmanager
from typing import Optional

@contextmanager
def get_db_connection(connection_string: str):
    """Context manager for database connections."""
    engine = create_engine(connection_string, pool_pre_ping=True)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()

def load_from_database(
    query: str,
    params: Optional[dict] = None,
    connection_string: str = None
) -> pl.DataFrame:
    """Load data from database with parameterized query.
    
    Args:
        query: SQL query with named parameters (:param_name)
        params: Dictionary of parameter values
        connection_string: Database connection string
        
    Returns:
        DataFrame with query results
    """
    with get_db_connection(connection_string) as conn:
        # Use parameterized query to prevent SQL injection
        result = conn.execute(text(query), params or {})
        
        # Convert to Polars DataFrame
        df = pl.DataFrame(result.fetchall(), schema=result.keys())
        
    logger.info(f"Loaded {len(df)} rows from database")
    return df

# Safe query with parameters
query = """
    SELECT disease, date, case_count, region
    FROM surveillance_data
    WHERE date >= :start_date
      AND date <= :end_date
      AND disease = :disease_name
"""

df = load_from_database(
    query=query,
    params={
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'disease_name': 'COVID-19'
    },
    connection_string='postgresql://user:pass@localhost/disease_db'
)

def write_to_database(
    df: pl.DataFrame,
    table_name: str,
    connection_string: str,
    if_exists: str = 'append'
) -> None:
    """Write DataFrame to database table.
    
    Args:
        df: Data to write
        table_name: Target table name
        connection_string: Database connection string
        if_exists: 'fail', 'replace', or 'append'
    """
    # Convert to pandas for SQLAlchemy compatibility
    df_pandas = df.to_pandas()
    
    engine = create_engine(connection_string)
    try:
        df_pandas.to_sql(
            table_name,
            engine,
            if_exists=if_exists,
            index=False,
            method='multi',  # Faster bulk inserts
            chunksize=1000
        )
        logger.info(f"Wrote {len(df)} rows to {table_name}")
    except Exception as e:
        logger.error(f"Failed to write to database: {e}")
        raise
    finally:
        engine.dispose()
```

## 11. Version Control and Reproducibility

### Git Best Practices
- **Never commit data files** - use `.gitignore`
- Never commit credentials or API keys
- Write clear, descriptive commit messages
- Commit often with logical, atomic changes
- Use branches for new features

### Reproducibility
- Pin all dependencies in `requirements.txt` with exact versions
- Use virtual environments (`venv`, `uv`)
- Document Python version requirements
- Set random seeds for reproducible results
- Log environment details for audit trails

```python
# Set seeds for reproducibility
import random
import numpy as np
import platform
import sys
from datetime import datetime

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def log_environment_info(output_file: str = 'logs/environment_info.json'):
    """Log environment details for reproducibility."""
    import json
    
    env_info = {
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'platform': platform.platform(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_implementation': platform.python_implementation(),
        'packages': {
            'polars': pl.__version__,
            'numpy': np.__version__,
        },
        'random_seed': RANDOM_SEED
    }
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(env_info, f, indent=2)
    
    logger.info(f"Environment info logged to {output_file}")
    logger.info(f"Python {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Polars: {pl.__version__}")

# Call at the start of analysis
log_environment_info()

# requirements.txt format (use uv for management)
"""
# Generated by: uv pip freeze
polars==0.20.0
numpy==1.24.3
pyyaml==6.0.1
pydantic==2.5.0
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
joblib==1.3.2
sqlalchemy==2.0.23
"""
```

## 12. Visualization Best Practices

### Clear and Informative Plots
- Always label axes with units
- Include titles and legends
- Use appropriate color schemes (consider colorblind-friendly palettes)
- Save figures in high resolution for publications

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_disease_trend(
    df: pl.DataFrame,
    disease: str,
    save_path: Optional[str] = None
) -> None:
    """Create publication-quality disease trend plot."""
    plt.figure(figsize=(12, 6))
    
    # Use clear styling
    sns.set_style('whitegrid')
    
    # Create plot
    plt.plot(df['date'], df['cases'], linewidth=2, label=disease)
    
    # Add labels and title
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Weekly Case Count', fontsize=12)
    plt.title(f'{disease} Cases Over Time', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    
    # Format dates
    plt.gcf().autofmt_xdate()
    
    # Save with high DPI
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
```

## 13. Code Style and Formatting

### PEP 8 Compliance
- Follow PEP 8 style guide
- Use tools: `black` (formatter), `flake8` (linter), `isort` (import sorting)
- Maximum line length: 88 (black default) or 100 characters
- Use 4 spaces for indentation (never tabs)

### Naming Conventions
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`
- Be descriptive: `disease_burden_metrics` not `dbm`

```python
# Good naming
MAX_RETRY_ATTEMPTS = 3
DEFAULT_ANALYSIS_WINDOW = 52  # weeks

class DiseaseAnalyzer:
    """Analyzer for infectious disease surveillance data."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self._cache = {}  # Private attribute
    
    def calculate_burden_metrics(self, disease: str) -> Dict:
        """Calculate disease burden metrics."""
        pass
    
    def _validate_input(self, data: pl.DataFrame) -> bool:
        """Private method for input validation."""
        pass
```

## 14. Data Privacy and Security

### Protected Health Information (PHI)
- Never log or print sensitive data
- Anonymize/aggregate data before sharing
- Use secure file permissions
- Document data handling procedures

```python
def export_aggregated_data(df: pl.DataFrame, output_path: str) -> None:
    """Export aggregated data with no PHI."""
    # Aggregate to prevent re-identification
    aggregated = df.groupby(['disease', 'year', 'week']).agg({
        'case_count': 'sum',
        'population': 'first'
    }).reset_index()
    
    # Remove any potentially identifiable information
    safe_columns = ['disease', 'year', 'week', 'case_count']
    aggregated[safe_columns].to_csv(output_path, index=False)
    
    logger.info(f"Exported aggregated data to {output_path}")
```

## 15. Notebook Best Practices

### Jupyter Notebooks
- Use notebooks for exploration, not production code
- Keep notebooks under 100 cells
- Extract reusable code into modules
- Clear outputs before committing to version control
- Use markdown cells to document analysis workflow

```python
# Cell 1: Imports and setup
import polars as pl
import numpy as np
from src.data_processing.validation import load_disease_data

# Cell 2: Document objective
"""
## Objective
Analyze seasonal patterns in respiratory diseases for 2020-2023

## Data Source
Weekly surveillance data from MOH infectious disease bulletin
"""

# Cell 3: Load and validate data
df = load_disease_data('data/1_raw/disease_data.csv')
print(f"Loaded {len(df):,} records")

# Cell 4: Basic exploration
df.info()
df.describe()
```

## 16. Dependencies Management

### Requirements Management with UV
- **Use `uv` for fast, reliable package management** (project standard)
- Separate development and production dependencies
- Pin exact versions for reproducibility
- Keep dependencies up to date but test updates thoroughly

```bash
# Install packages with uv
uv pip install polars numpy pyyaml

# Generate requirements.txt
uv pip freeze > requirements.txt

# Install from requirements.txt
uv pip sync requirements.txt

# Create virtual environment
uv venv
source .venv/bin/activate  # On Unix
# or
.venv\\Scripts\\activate  # On Windows
```

```txt
# requirements.txt (production) - exact versions
polars==0.20.0
numpy==1.24.3
pyyaml==6.0.1
pydantic==2.5.0
sqlalchemy==2.0.23

# requirements-dev.txt (development)
-r requirements.txt
pytest==7.4.3
black==23.12.0
flake8==6.1.0
jupyter==1.0.0
line-profiler==4.1.1
memory-profiler==0.61.0
```

## 17. Documentation

### Project Documentation
- Maintain README.md with project overview and setup instructions
- Document data sources, methodologies, and assumptions
- Create data dictionaries for all datasets
- Keep a CHANGELOG.md for tracking uplates

### Code Comments
- Comment the "why" not the "what"
- Avoid redundant comments
- Uplate comments when code changes
- Use TODO comments for future improvements

```python
# Good: Explains reasoning
# Use 4-week window to smooth out weekly reporting variations
# while still capturing monthly trends
rolling_avg = df['cases'].rolling(window=4).mean()

# Bad: States the obvious
# Calculate rolling average
rolling_avg = df['cases'].rolling(window=4).mean()

# TODO: Implement automated anomaly detection for data quality
# See issue #45 for algorithm selection discussion
```

## 18. Anti-Patterns: What Should NOT Exist

#### ❌ Hardcoded Values
```python
# BAD: Magic numbers and hardcoded paths
df = pl.read_csv('/Users/john/Desktop/data.csv')
threshold = 42  # What does 42 mean?
if cases > 100:  # Why 100?
    flag_outbreak()

# GOOD: Named constants with clear meaning
BASE_DATA_PATH = Path('data/1_raw')
RAW_DATA_FILE = BASE_DATA_PATH / 'surveillance_data.csv'
OUTBREAK_THRESHOLD_CASES = 50  # Historical 95th percentile for this region
HIGH_BURDEN_CUTOFF = 100  # Cases per 100k population (WHO definition)

df = pl.read_csv(RAW_DATA_FILE)
if cases > HIGH_BURDEN_CUTOFF:
    flag_outbreak()
```

#### ❌ Print Statements for Debugging
```python
# BAD: Print debugging left in code
def calculate_metrics(df):
    print("Starting calculation...")
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns}")
    result = df.groupby('disease').sum()
    print(result)  # Debugging print
    return result

# GOOD: Use proper logging
def calculate_metrics(df: pl.DataFrame) -> pl.DataFrame:
    logger.debug(f"Calculating metrics for DataFrame with shape {df.shape}")
    result = df.groupby('disease').sum()
    logger.info(f"Calculated metrics for {len(result)} diseases")
    return result
```

#### ❌ Silencing Errors
```python
# BAD: Bare except that hides problems
try:
    df['date'] = pl.to_datetime(df['date'])
except:
    pass  # What went wrong? We'll never know!

# BAD: Catching all exceptions without action
try:
    process_data()
except Exception:
    pass

# GOOD: Specific error handling with logging
try:
    df['date'] = pl.to_datetime(df['date'])
except (ValueError, TypeError) as e:
    logger.error(f"Failed to parse dates: {e}")
    logger.info("Attempting alternative date format...")
    df['date'] = pl.to_datetime(df['date'], format='%d/%m/%Y')
```

#### ❌ God Functions and God Classes
```python
# BAD: 500-line function that does everything
def analyze_everything(file1, file2, file3, config):
    # Load data
    df1 = pl.read_csv(file1)
    df2 = pl.read_csv(file2)
    # Clean data
    # Validate data
    # Calculate metrics
    # Create visualizations
    # Generate report
    # Send email
    # ... 450 more lines
    return result

# GOOD: Break into focused, testable functions
def load_and_validate_data(filepath: str) -> pl.DataFrame:
    """Load and validate single data file."""
    pass

def calculate_disease_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """Calculate burden metrics for diseases."""
    pass

def generate_visualizations(metrics: pl.DataFrame, output_dir: str) -> List[str]:
    """Create standard visualization suite."""
    pass
```

#### ❌ Mutable Default Arguments
```python
# BAD: Mutable default arguments
def add_disease(disease: str, disease_list=[]):
    disease_list.append(disease)
    return disease_list

# This causes unexpected behavior:
# list1 = add_disease("COVID-19")
# list2 = add_disease("Dengue")  # list2 contains both!

# GOOD: Use None and create new instance
def add_disease(disease: str, disease_list: Optional[List[str]] = None) -> List[str]:
    if disease_list is None:
        disease_list = []
    disease_list.append(disease)
    return disease_list
```

#### ❌ Nested Loops for Data Operations
```python
# BAD: Nested loops on DataFrames
for i in range(len(df)):
    for col in df.columns:
        if df.iloc[i][col] < 0:
            df.iloc[i][col] = 0

# GOOD: Vectorized operations
df[df < 0] = 0
# Or for specific columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].clip(lower=0)
```

#### ❌ Ignoring Data Types
```python
# BAD: Everything is object type, wasting memory
df = pl.read_csv('large_file.csv')  # All columns are 'object' type

# BAD: Mixing types in analysis
year = "2023"  # String
cases = "150"   # String
rate = cases / year  # Will fail!

# GOOD: Explicit type specification and conversion
df = pl.read_csv('large_file.csv', dtype={
    'disease': 'category',
    'year': 'int16',
    'week': 'int8',
    'cases': 'int32'
})

year = 2023  # Integer
cases = 150  # Integer
rate = cases / year
```

### Files and Directories That Should NOT Exist

#### ❌ Data Files in Version Control
```bash
# These should be in .gitignore:
data/1_raw/*.csv
data/1_raw/*.xlsx
data/2_external/*.json
data/3_interim/*.parquet
data/4_processed/*.csv
*.db
*.sqlite
```

#### ❌ Credentials and Secrets
```bash
# NEVER commit these:
.env
credentials.json
*.pem
*.key
.aws/credentials
database_passwords.txt
api_keys.txt
secrets/
```

#### ❌ IDE and System Files
```bash
# Should be in .gitignore:
.DS_Store
.vscode/settings.json  # Personal settings
.idea/
*.pyc
__pycache__/
.ipynb_checkpoints/
Thumbs.db
```

#### ❌ Output Files from Runs
```bash
# Should be in .gitignore:
results/figures/*.png
results/tables/*.csv
models/*.pkl
logs/*.log
*.tmp
.cache/
```

#### ❌ Redundant or Deprecated Files
```python
# BAD: Multiple versions cluttering the repo
analysis_v1.py
analysis_v2.py
analysis_final.py
analysis_final_FINAL.py
analysis_final_really_final.py

# GOOD: Use version control properly
# Keep only: analysis.py
# Git history preserves all versions
```

### Code Patterns to Avoid

#### ❌ Copy-Paste Programming
```python
# BAD: Repeated code for each disease
covid_metrics = df[df['disease'] == 'COVID-19'].agg({
    'cases': ['sum', 'mean', 'std']
})

dengue_metrics = df[df['disease'] == 'Dengue'].agg({
    'cases': ['sum', 'mean', 'std']
})

tb_metrics = df[df['disease'] == 'Tuberculosis'].agg({
    'cases': ['sum', 'mean', 'std']
})

# GOOD: Reusable function
def calculate_disease_metrics(df: pl.DataFrame, disease: str) -> pl.DataFrame:
    """Calculate standard metrics for a specific disease."""
    return df[df['disease'] == disease].agg({
        'cases': ['sum', 'mean', 'std']
    })

# Use for all diseases
diseases = ['COVID-19', 'Dengue', 'Tuberculosis']
metrics = {d: calculate_disease_metrics(df, d) for d in diseases}
```

#### ❌ Premature Optimization
```python
# BAD: Over-engineering before understanding requirements
import numba
from multiprocessing import Pool

@numba.jit
def ultra_optimized_mean(arr):
    # Complex optimization for simple operation
    pass

# GOOD: Start simple, optimize if needed
def calculate_mean(df: pl.DataFrame, column: str) -> float:
    """Calculate mean of column."""
    return df[column].mean()

# Profile first, then optimize bottlenecks if necessary
```

#### ❌ Unclear Variable Names
```python
# BAD: Cryptic abbreviations
df1 = pl.read_csv('data.csv')
tmp = df1[df1['x'] > 5]
res = tmp.groupby('y').agg({'z': 'sum'})

# GOOD: Descriptive names
disease_data = pl.read_csv('weekly_surveillance.csv')
high_incidence_cases = disease_data[disease_data['incidence_rate'] > 5]
cases_by_region = high_incidence_cases.groupby('region').agg({
    'case_count': 'sum'
})
```

#### ❌ Modifying DataFrames In-Place Without Intent
```python
# BAD: Unintended side effects
def process_data(df):
    df.drop(columns=['temp_col'], inplace=True)  # Modifies original!
    df['new_col'] = df['old_col'] * 2
    return df

original_df = load_data()
processed_df = process_data(original_df)
# original_df is now modified unexpectedly!

# GOOD: Explicit about mutations
def process_data(df: pl.DataFrame) -> pl.DataFrame:
    """Process data, returns new DataFrame without modifying input."""
    return (
        df.copy()
        .drop(columns=['temp_col'])
        .assign(new_col=lambda x: x['old_col'] * 2)
    )
```

#### ❌ Not Handling Edge Cases
```python
# BAD: Assumes perfect data
def calculate_rate(cases: int, population: int) -> float:
    return (cases / population) * 100000

# What if population is 0? What if cases is negative?

# GOOD: Validate inputs and handle edge cases
def calculate_incidence_rate(
    cases: int,
    population: int
) -> Optional[float]:
    """Calculate incidence rate per 100,000 population.
    
    Returns:
        Incidence rate or None if calculation not possible
    """
    if population <= 0:
        logger.warning(f"Invalid population: {population}")
        return None
    
    if cases < 0:
        raise ValueError(f"Cases cannot be negative: {cases}")
    
    return (cases / population) * 100_000
```

#### ❌ Mixing Analysis and Presentation
```python
# BAD: Analysis code mixed with plotting
df = pl.read_csv('data.csv')
result = df.groupby('disease').sum()
plt.plot(result)  # Visualization in middle of analysis
more_results = result.apply(some_function)
plt.bar(more_results)
final = more_results.merge(other_data)

# GOOD: Separate concerns
# 1. Data loading and preparation
df = load_and_validate_data('data.csv')

# 2. Analysis
disease_totals = calculate_disease_totals(df)
burden_metrics = calculate_burden_metrics(disease_totals)

# 3. Visualization (separate function or notebook)
create_disease_trend_plot(disease_totals, save_path='results/figures/')
create_burden_heatmap(burden_metrics, save_path='results/figures/')
```

#### ❌ Not Using Context Managers
```python
# BAD: File not properly closed if error occurs
f = open('data.csv', 'r')
data = f.read()
process(data)
f.close()  # Might not execute if process() raises error

# GOOD: Context manager ensures cleanup
with open('data.csv', 'r') as f:
    data = f.read()
    process(data)
# File automatically closed even if error occurs
```

#### ❌ Overly Complex Comprehensions
```python
# BAD: Unreadable one-liner
result = [item for sublist in [[x*y for y in range(10) if y%2==0] for x in data if x>5] for item in sublist if item<100]

# GOOD: Break into readable steps
filtered_data = [x for x in data if x > 5]
even_products = []
for x in filtered_data:
    products = [x * y for y in range(10) if y % 2 == 0]
    even_products.extend(products)
result = [item for item in even_products if item < 100]

# Or use functions for clarity
def calculate_products(x: int) -> List[int]:
    return [x * y for y in range(0, 10, 2)]

result = [
    product 
    for x in data if x > 5
    for product in calculate_products(x) if product < 100
]
```

### Documentation Anti-Patterns

#### ❌ No Documentation
```python
# BAD: No docstring, unclear purpose
def proc(d, t=2):
    return d[d.x > t].groupby('y').sum()
```

#### ❌ Outdated Documentation
```python
# BAD: Documentation doesn't match implementation
def calculate_rate(cases, population):
    """Calculate mortality rate per 1000."""  # Says mortality
    return (cases / population) * 100000  # Actually incidence per 100k
```

#### ❌ Redundant Comments
```python
# BAD: Comments that just restate the code
# Loop through each row
for row in df.iterrows():
    # Get the disease name
    disease = row['disease']
    # Add to list
    disease_list.append(disease)
```

### Testing Anti-Patterns

#### ❌ No Tests At All
```python
# If your src/ directory has no corresponding tests/ directory,
# you're accumulating technical debt
```

#### ❌ Tests That Don't Actually Test
```python
# BAD: Test that can never fail
def test_calculate_metrics():
    result = calculate_metrics(df)
    assert result is not None  # Meaningless assertion
    assert True  # Always passes
```

#### ❌ Tests That Depend on External State
```python
# BAD: Test depends on specific file existing
def test_load_data():
    df = load_data('/Users/john/data.csv')  # Fails on other machines
    assert len(df) > 0

# GOOD: Use fixtures or test data
import pytest

@pytest.fixture
def sample_data(tmp_path):
    """Create temporary test data."""
    data_file = tmp_path / "test_data.csv"
    data_file.write_text("disease,cases\nCOVID-19,100\n")
    return str(data_file)

def test_load_data(sample_data):
    df = load_data(sample_data)
    assert len(df) == 1
```

## Summary Checklist

### ✅ Should Exist
- [ ] Project structure follows standard conventions
- [ ] All functions have type hints and docstrings
- [ ] Input validation and error handling implemented
- [ ] Logging configured and used appropriately
- [ ] Unit tests cover key functionality
- [ ] Code follows PEP 8 style guidelines
- [ ] Constants clearly named, no magic numbers
- [ ] Dependencies pinned in requirements.txt
- [ ] .gitignore excludes data files and credentials
- [ ] Documentation up to date
- [ ] Sensitive data handled appropriately
- [ ] Notebook outputs cleared before commit
- [ ] Code reviewed and tested before merging

### ❌ Should NOT Exist
- [ ] Print statements for debugging (use logging instead)
- [ ] Hardcoded absolute file paths or credentials
- [ ] Magic numbers without explanation
- [ ] Bare except clauses that hide errors
- [ ] Functions longer than 100 lines
- [ ] God classes that do too many things
- [ ] Data files committed to version control
- [ ] API keys or passwords in code
- [ ] Commented-out code blocks (use git history)
- [ ] Multiple "final" versions of files
- [ ] Nested loops for DataFrame operations
- [ ] Copy-pasted code repeated across files
- [ ] IDE-specific settings files
- [ ] Generated output files (figures, models)
- [ ] Temporary or debug files
- [ ] Tests that don't actually assert anything

---

**Remember**: Write code that your future self (and colleagues) will thank you for. Prioritize clarity, maintainability, and reproducibility over clever tricks.