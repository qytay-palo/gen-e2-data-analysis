---
name: 'Data Analysis Best Practices'
description: 'Analysis best practices for data analysis projects, covering the entire life cycle from problem definition to deployment.'
applyTo: 'docs/objectives/problem_statements/*, docs/objectives/user_stories/*'
---

## Purpose
This document provides **mandatory guidelines** for all data analysis work. When generating, reviewing, or modifying data analysis code, **ALWAYS follow these practices**.

## Rules

When assisting with data analysis tasks:

1. **NEVER modify files in `data/1_raw/`** - treat as read-only
2. **ALWAYS validate input data** before processing
3. **ALWAYS use type hints** in function definitions
4. **ALWAYS log using `logging` module**, never `print()` for production code
5. **ALWAYS save intermediate results** to `data/3_interim/` during processing
6. **ALWAYS save final results** to `data/4_processed/` with documentation
7. **ALWAYS save ALL outputs to local directories**:
   - Figures → `reports/figures/problem-statement-{num}/`
   - Tables → `results/tables/problem-statement-{num}/`
   - Metrics → `results/metrics/problem-statement-{num}/`
   - Include timestamps in filenames
   - Print confirmation messages
8. **ALWAYS use descriptive variable names** (`disease_burden_metrics` not `dbm`)
9. **ALWAYS handle exceptions** explicitly with informative error messages
10. **ALWAYS document data transformations** with clear comments
11. **ALWAYS generate data quality reports** after cleaning steps

## 🗂️ Required Folder Structure

```
data/
├── 1_raw/           # ❌ READ-ONLY: Original source data, never modify
├── 2_external/      # Third-party/reference data with documented sources  
├── 3_interim/       # ✅ WRITE: Intermediate processing checkpoints
├── 4_processed/     # ✅ WRITE: Final analysis-ready data with README
└── schemas/         # Data schemas and metadata definitions
results/
├── tables/          # ✅ WRITE: Summary tables and data exports
│   └── problem-statement-{num}/  # Organized by problem statement
├── metrics/         # ✅ WRITE: KPIs and calculated metrics
│   └── problem-statement-{num}/
└── exports/         # ✅ WRITE: Stakeholder-ready outputs
reports/
├── figures/         # ✅ WRITE: Visualizations and charts
│   └── problem-statement-{num}/  # Organized by problem statement
├── dashboards/      # Interactive dashboards
└── presentations/   # Presentation materials
logs/
├── etl/            # ETL and data processing logs
├── errors/         # Error logs
└── audit/          # Audit trail and lineage logs
```

## 📝 Logger Setup (Required)

**ALWAYS configure logging at the start of any analysis script or notebook.**

```python
import logging
from pathlib import Path
from datetime import datetime

def setup_logger(
    name: str = __name__,
    log_dir: str = 'logs/analysis',
    level: int = logging.INFO
) -> logging.Logger:
    """Configure logger for analysis workflows.
    
    Args:
        name: Logger name (use __name__ for module-level)
        log_dir: Directory to store log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # File handler with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_path / f'analysis_{timestamp}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usage at top of any script or notebook
logger = setup_logger(__name__)
logger.info("Analysis started")
```

## Overview

This document outlines best practices for the complete data analysis life cycle, from problem definition through deployment and monitoring. These practices ensure reproducibility, quality, and actionable insights from data analysis projects.

## Data Analysis Life Cycle Stages

```
1. Problem Definition & Planning
   ↓
2. Data Collection & Acquisition  
   ↓
3. Data Exploration & Understanding
   ↓
4. Data Preparation & Cleaning
   ↓
5. Feature Engineering & Transformation
   ↓
6. Analysis & Modeling
   ↓
7. Validation & Testing
   ↓
8. Interpretation & Visualization
   ↓
9. Documentation & Communication
   ↓
10. Deployment & Monitoring
```

---

## 1. Problem Definition & Planning

### Define Clear Objectives
- **Write specific, measurable questions** the analysis should answer
- Identify key stakeholders and their requirements
- Define success criteria and metrics upfront
- Document assumptions and constraints

### Create Problem Statement Document
```markdown
## Problem Statement
**Question**: What are the seasonal patterns in respiratory disease outbreaks?

**Stakeholders**: Public Health Epidemiologists, Healthcare Administrators

**Success Criteria**:
- Identify peak outbreak months with >80% accuracy
- Quantify disease burden by season
- Generate actionable early warning indicators

**Constraints**:
- Historical data available from 2015-2023
- Weekly aggregated case counts (no patient-level data)
- Analysis must complete within 2 weeks
```

### Plan Data Requirements
- List required data sources and availability
- Identify data quality concerns upfront
- Define minimum viable dataset criteria
- Plan data access and permissions

**Location**: Store in `docs/problem_statements/` or `docs/objectives/`

---

## 2. Data Collection & Acquisition

### Organize by Data Provenance
Use the standardized folder structure:

```
data/
├── 1_raw/           # Original, immutable source data
├── 2_external/      # Third-party or reference data
├── 3_interim/       # Intermediate processing steps
├── 4_processed/     # Final analysis-ready data
└── schemas/         # Data schemas and metadata
```

### Raw Data Management (`data/1_raw/`)
- **Never modify raw data files** - treat as read-only
- Preserve original file formats and structure
- Document data source, collection date, and methodology
- Include `.gitkeep` files to preserve directory structure
- Use descriptive filenames with dates: `disease_surveillance_2023-01-15.csv`

```python
# Good practice: Load raw data with metadata
import polars as pl
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path('data/1_raw')

def load_raw_surveillance_data(filename: str) -> pl.DataFrame:
    """Load raw surveillance data with provenance tracking.
    
    Args:
        filename: Name of raw data file
        
    Returns:
        Polars DataFrame
    """
    filepath = RAW_DATA_PATH / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Raw data not found: {filepath}")
    
    # Use lazy loading for large files
    df = pl.read_csv(filepath)
    
    # Log metadata
    metadata = {
        'source_file': filename,
        'load_timestamp': datetime.now().isoformat(),
        'row_count': df.height,
        'column_count': df.width,
        'memory_mb': df.estimated_size() / (1024**2)
    }
    
    logger.info(f"Loaded {df.height:,} rows x {df.width} columns from {filename}")
    logger.debug(f"Metadata: {metadata}")
    return df
```

### External Reference Data (`data/2_external/`)
- Store third-party datasets (e.g., population data, disease taxonomies)
- Document source, version, and update frequency
- Include license information if applicable
- Create README.md listing all external sources

```markdown
# External Data Sources

## population_singapore_2023.csv
- **Source**: Singapore Department of Statistics
- **URL**: https://www.singstat.gov.sg/...
- **Date Retrieved**: 2024-01-15
- **Update Frequency**: Annual
- **License**: Public Domain

## who_disease_classification.json
- **Source**: WHO International Classification of Diseases (ICD-11)
- **Version**: 2023 Release
- **Date Retrieved**: 2024-01-10
```

### Data Acquisition Automation
```python
def download_external_data(
    url: str,
    destination: Path,
    force_update: bool = False
) -> Path:
    """Download external data with caching.
    
    Args:
        url: Source URL
        destination: Local file path in data/2_external/
        force_update: Re-download even if file exists
        
    Returns:
        Path to downloaded file
    """
    if destination.exists() and not force_update:
        logger.info(f"Using cached data: {destination}")
        return destination
    
    logger.info(f"Downloading from {url}")
    
    # Download logic here
    # ... 
    
    # Log metadata
    metadata = {
        'source_url': url,
        'download_date': datetime.now().isoformat(),
        'file_size_bytes': destination.stat().st_size
    }
    
    metadata_file = destination.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return destination
```

---

## 3. Data Exploration & Understanding

### Initial Data Profiling
Conduct systematic exploration before any transformations:

```python
import polars as pl
from typing import Dict
from datetime import datetime
import json
from pathlib import Path

def profile_dataset(df: pl.DataFrame, dataset_name: str) -> Dict:
    """Generate comprehensive data profile using pure Polars.
    
    Returns:
        Dictionary with profiling statistics
    """
    profile = {
        'dataset': dataset_name,
        'timestamp': datetime.now().isoformat(),
        'shape': {'rows': df.height, 'columns': df.width},
        'memory_usage_mb': df.estimated_size() / (1024**2),
        'columns': {},
        'missing_data': {col: df[col].null_count() for col in df.columns},
        'duplicate_rows': df.is_duplicated().sum(),
        'data_types': {col: str(df[col].dtype) for col in df.columns}
    }
    
    # Per-column statistics using Polars expressions
    numeric_types = [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64]
    
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'missing_count': df[col].null_count(),
            'missing_pct': (df[col].null_count() / df.height) * 100,
            'unique_count': df[col].n_unique()
        }
        
        # Add numeric statistics if applicable
        if df[col].dtype in numeric_types:
            stats = df.select([
                pl.col(col).min().alias('min'),
                pl.col(col).max().alias('max'),
                pl.col(col).mean().alias('mean'),
                pl.col(col).median().alias('median'),
                pl.col(col).std().alias('std')
            ]).to_dicts()[0]
            
            col_profile.update({k: float(v) if v is not None else None for k, v in stats.items()})
        
        profile['columns'][col] = col_profile
    
    return profile

# Usage in notebook or script
profile = profile_dataset(df_raw, 'disease_surveillance_raw')

# Save profile report with timestamp
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save to problem-statement-specific directory
profile_dir = Path('results/tables/problem-statement-001')  # Adjust number as needed
profile_dir.mkdir(parents=True, exist_ok=True)
profile_path = profile_dir / f'data_profile_report_{timestamp}.json'

with open(profile_path, 'w') as f:
    json.dump(profile, f, indent=2)

logger.info(f"✅ Data profile saved: {profile_path}")
```

### Schema Validation
For production pipelines, use schema validation from Python best practices:

```python
# See python-best-practices.instructions.md Section 3 for full implementation
from src.data_processing.validation import validate_disease_schema

try:
    df_validated = validate_disease_schema(df_raw)
    logger.info("Schema validation passed")
except SchemaValidationError as e:
    logger.error(f"Schema validation failed: {e}")
    raise
```

### Exploratory Data Analysis (EDA) Checklist
- [ ] Check data dimensions (rows, columns)
- [ ] Examine data types for each column
- [ ] Identify missing values and patterns
- [ ] Detect duplicates
- [ ] Analyze distributions (histograms, box plots)
- [ ] Check for outliers and anomalies
- [ ] Explore relationships between variables (correlation matrix)
- [ ] Identify temporal patterns if time-series data
- [ ] Document unexpected findings
- [ ] **Save all EDA outputs to local directories** (see Output Persistence Requirements below)

### Use Notebooks for Exploration
- Keep exploratory notebooks in `notebooks/1_exploratory/`
- Name with sequence numbers: `01_initial_data_profiling.ipynb`
- Use markdown cells to document findings
- Clear outputs before committing to version control
- **CRITICAL**: Include output directory setup in first code cell
- **CRITICAL**: Save all visualizations and summaries to local directories

```python
# Notebook cell 1: Setup
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

%matplotlib inline
sns.set_style('whitegrid')

# Setup output directories (REQUIRED)
PROBLEM_STATEMENT_NUM = '001'  # Adjust as needed
FIGURES_DIR = Path(f'reports/figures/problem-statement-{PROBLEM_STATEMENT_NUM}')
RESULTS_DIR = Path(f'results/tables/problem-statement-{PROBLEM_STATEMENT_NUM}')

for dir_path in [FIGURES_DIR, RESULTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
print(f"✅ Output directories configured | Timestamp: {timestamp}")

# Notebook cell 2: Document objective
"""
## Objective
Initial exploration of weekly disease surveillance data

## Data Source
data/1_raw/weekly_disease_bulletin_2020-2023.csv

## Key Questions
1. What is the completeness of the data?
2. Are there any temporal gaps?
3. What is the distribution of case counts?

## Outputs
All results saved to:
- Figures: reports/figures/problem-statement-001/
- Tables: results/tables/problem-statement-001/
"""

# Notebook cell 3: Example - Always save visualizations
plt.figure(figsize=(12, 6))
# ... create plot ...
fig_path = FIGURES_DIR / f'descriptive_name_{timestamp}.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {fig_path}")
plt.show()
```

---

## 4. Data Preparation & Cleaning

### Store Interim Results (`data/3_interim/`)
- Save intermediate processing steps for debugging and auditing
- Use clear, descriptive filenames with processing step indicators
- Document what processing was applied

```python
import polars as pl
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def clean_disease_data(df_raw: pl.DataFrame) -> pl.DataFrame:
    """Clean and standardize disease surveillance data.
    
    Cleaning steps:
    1. Remove duplicate records
    2. Standardize date formats
    3. Handle missing values
    4. Validate case counts (non-negative)
    5. Standardize disease names
    6. Optimize data types
    
    Args:
        df_raw: Raw disease surveillance data
        
    Returns:
        Cleaned DataFrame
    """
    logger.info(f"Starting data cleaning: {df_raw.height} rows")
    
    df_clean = df_raw.clone()
    
    # Remove exact duplicates
    initial_rows = df_clean.height
    df_clean = df_clean.unique()
    duplicates_removed = initial_rows - df_clean.height
    logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Standardize dates using Polars date parsing
    df_clean = df_clean.with_columns(
        pl.col('date').str.strptime(pl.Date, format='%Y-%m-%d', strict=False)
    )
    invalid_dates = df_clean['date'].null_count()
    if invalid_dates > 0:
        logger.warning(f"Found {invalid_dates} invalid dates, removing rows")
        df_clean = df_clean.drop_nulls(subset=['date'])
    
    # Handle missing case counts
    if 'case_count' in df_clean.columns:
        missing_counts = df_clean['case_count'].null_count()
        if missing_counts > 0:
            logger.warning(f"Dropping {missing_counts} rows with missing case counts")
            df_clean = df_clean.drop_nulls(subset=['case_count'])
    
    # Validate case counts are non-negative
    if 'case_count' in df_clean.columns:
        negative_counts = df_clean.filter(pl.col('case_count') < 0).height
        if negative_counts > 0:
            logger.error(f"Found {negative_counts} negative case counts, removing")
            df_clean = df_clean.filter(pl.col('case_count') >= 0)
    
    # Standardize disease names (trim whitespace, title case)
    if 'disease' in df_clean.columns:
        df_clean = df_clean.with_columns(
            pl.col('disease').str.strip_chars().str.to_titlecase().cast(pl.Categorical)
        )
    
    # Optimize data types for memory efficiency
    if 'case_count' in df_clean.columns:
        max_cases = df_clean['case_count'].max()
        if max_cases < 32767:  # Fits in Int16
            df_clean = df_clean.with_columns(pl.col('case_count').cast(pl.Int32))
    
    # Save interim cleaned data
    interim_path = Path('data/3_interim/disease_data_cleaned.csv')
    interim_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.write_csv(interim_path)
    logger.info(f"Saved cleaned data: {interim_path}")
    
    logger.info(f"Cleaning complete: {df_clean.height} rows retained ({df_clean.height/initial_rows*100:.1f}%)")
    return df_clean
```

### Data Quality Report
Generate and save quality reports after cleaning:

```python
import polars as pl
from typing import Dict
from datetime import datetime
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def generate_quality_report(
    df_raw: pl.DataFrame,
    df_cleaned: pl.DataFrame,
    output_path: str = 'results/tables/data_quality_report.json'
) -> Dict:
    """Generate data quality report comparing raw and cleaned data."""
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'raw_data': {
            'rows': df_raw.height,
            'columns': df_raw.width,
            'missing_values': sum(df_raw[col].null_count() for col in df_raw.columns),
            'duplicates': df_raw.is_duplicated().sum(),
            'memory_mb': df_raw.estimated_size() / (1024**2)
        },
        'cleaned_data': {
            'rows': df_cleaned.height,
            'columns': df_cleaned.width,
            'missing_values': sum(df_cleaned[col].null_count() for col in df_cleaned.columns),
            'duplicates': df_cleaned.is_duplicated().sum(),
            'memory_mb': df_cleaned.estimated_size() / (1024**2)
        },
        'changes': {
            'rows_removed': df_raw.height - df_cleaned.height,
            'removal_rate': ((df_raw.height - df_cleaned.height) / df_raw.height) * 100,
            'memory_saved_mb': (df_raw.estimated_size() - df_cleaned.estimated_size()) / (1024**2)
        }
    }
    
    # Save report
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Quality report saved: {output_path}")
    logger.info(f"Data cleaned: {report['cleaned_data']['rows']:,} rows ({report['changes']['removal_rate']:.1f}% removed)")
    return report
```

---

## 5. Feature Engineering & Transformation

### Create Analysis-Ready Data (`data/4_processed/`)
- Final datasets ready for analysis/modeling
- Well-documented with data dictionaries
- Optimized data types for performance
- Include README.md explaining each file

```python
import polars as pl
import logging

logger = logging.getLogger(__name__)

def engineer_temporal_features(df: pl.DataFrame) -> pl.DataFrame:
    """Add time-based features for temporal analysis using Polars.
    
    Features added:
    - year, month, week, quarter
    - day_of_week, is_weekend
    - season (meteorological - Singapore monsoons)
    
    Args:
        df: DataFrame with 'date' column
        
    Returns:
        DataFrame with temporal features
    """
    logger.info("Engineering temporal features")
    
    df_featured = df.clone()
    
    # Ensure date column is proper Date type
    df_featured = df_featured.with_columns(
        pl.col('date').cast(pl.Date)
    )
    
    # Extract temporal components with optimized dtypes
    df_featured = df_featured.with_columns([
        pl.col('date').dt.year().cast(pl.Int16).alias('year'),
        pl.col('date').dt.month().cast(pl.UInt8).alias('month'),
        pl.col('date').dt.week().cast(pl.UInt8).alias('week'),
        pl.col('date').dt.quarter().cast(pl.UInt8).alias('quarter'),
        pl.col('date').dt.weekday().cast(pl.UInt8).alias('day_of_week'),
        (pl.col('date').dt.weekday() >= 5).alias('is_weekend')
    ])
    
    # Add season (Singapore context - monsoon seasons)
    df_featured = df_featured.with_columns(
        pl.when(pl.col('month').is_in([12, 1, 2]))
        .then(pl.lit('Northeast Monsoon'))
        .when(pl.col('month').is_in([3, 4, 5]))
        .then(pl.lit('Inter-monsoon'))
        .when(pl.col('month').is_in([6, 7, 8, 9]))
        .then(pl.lit('Southwest Monsoon'))
        .otherwise(pl.lit('Inter-monsoon'))
        .cast(pl.Categorical)
        .alias('season')
    )
    
    logger.info(f"Added temporal features: {df_featured.width - df.width} new columns")
    return df_featured

def create_processed_dataset(df: pl.DataFrame, output_name: str) -> Path:
    """Create final processed dataset with memory optimizations.
    
    Args:
        df: Cleaned and featured DataFrame
        output_name: Name for processed file (e.g., 'disease_metrics.csv')
        
    Returns:
        Path to saved file
    """
    logger.info("Creating processed dataset with optimizations")
    
    df_optimized = df.clone()
    
    # Optimize data types - convert low cardinality string columns to Categorical
    string_cols = [col for col in df_optimized.columns if df_optimized[col].dtype == pl.Utf8]
    for col in string_cols:
        unique_count = df_optimized[col].n_unique()
        if unique_count < 50:  # Low cardinality threshold
            df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.Categorical))
            logger.debug(f"Converted '{col}' to Categorical ({unique_count} unique values)")
    
    # Save to processed folder
    output_path = Path('data/4_processed') / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use Parquet for better compression and performance
    if output_name.endswith('.csv'):
        df_optimized.write_csv(output_path)
    elif output_name.endswith('.parquet'):
        df_optimized.write_parquet(output_path, compression='zstd')
    else:
        # Default to CSV
        df_optimized.write_csv(output_path)
    
    memory_mb = df_optimized.estimated_size() / (1024**2)
    logger.info(f"Processed data saved: {output_path}")
    logger.info(f"Final shape: {df_optimized.height} rows x {df_optimized.width} columns")
    logger.info(f"Memory usage: {memory_mb:.2f} MB")
    
    return output_path
```

### Document Processed Datasets
Create `data/4_processed/README.md`:

```markdown
# Processed Datasets

## disease_burden_metrics.csv
**Description**: Disease burden metrics calculated from weekly surveillance data

**Source**: Derived from data/1_raw/weekly_disease_bulletin_2020-2023.csv

**Processing Steps**:
1. Data cleaning and validation (scripts/clean_data.py)
2. Temporal feature engineering
3. Burden metric calculations (incidence rate, YLL, etc.)

**Columns**:
- `disease` (str): Standardized disease name
- `year` (int): Year of observation
- `week` (int): ISO week number
- `case_count` (int): Number of reported cases
- `incidence_rate` (float): Cases per 100,000 population
- `burden_score` (float): Composite burden metric (0-100)

**Rows**: 12,458
**Date Range**: 2020-W01 to 2023-W52
**Last Updated**: 2024-02-11
```

---

## 5.5 Configuration Management (Best Practice)

### Use Type-Safe Configuration with Pydantic
Store analysis parameters in configuration files and load them with validation.

```python
# config/analysis.yml
outbreak_detection:
  threshold_std: 2.0
  rolling_window_weeks: 4
  min_cases_for_analysis: 10

data_sources:
  singapore_population: 5686000
  analysis_start_year: 2020
  
target_diseases:
  - COVID-19
  - Dengue
  - Tuberculosis
  - Influenza
```

```python
# src/utils/config.py
from pydantic import BaseModel, Field, validator
from pathlib import Path
from typing import List
import yaml
import logging

logger = logging.getLogger(__name__)

class OutbreakDetectionConfig(BaseModel):
    \"\"\"Outbreak detection parameters.\"\"\"
    threshold_std: float = Field(gt=0, description=\"Standard deviations above baseline\")
    rolling_window_weeks: int = Field(gt=0, le=52)
    min_cases_for_analysis: int = Field(ge=0)

class AnalysisConfig(BaseModel):
    \"\"\"Main analysis configuration.\"\"\"
    
    outbreak_detection: OutbreakDetectionConfig
    singapore_population: int = Field(gt=0)
    analysis_start_year: int = Field(ge=2000, le=2030)
    target_diseases: List[str]
    
    class Config:
        frozen = True  # Immutable after creation
        extra = 'forbid'  # Reject unknown parameters

def load_config(config_path: str = 'config/analysis.yml') -> AnalysisConfig:
    \"\"\"Load and validate configuration.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Validated configuration object
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If configuration is invalid
    \"\"\"
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f\"Config file not found: {config_path}\")
    
    with open(config_file, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    try:
        config = AnalysisConfig(**config_dict)
        logger.info(f\"Loaded configuration from {config_path}\")
        return config
    except Exception as e:
        raise ValueError(f\"Invalid configuration: {e}\") from e

# Usage in analysis
config = load_config()
threshold = config.outbreak_detection.threshold_std
window = config.outbreak_detection.rolling_window_weeks
population = config.singapore_population
```

---

## 6. Analysis & Modeling

### Separate Analysis Notebooks
Keep analysis notebooks in `notebooks/2_analysis/`:

```
notebooks/
├── 1_exploratory/
│   ├── 01_disease_data_profiling.ipynb
│   └── 02_temporal_patterns_exploration.ipynb
└── 2_analysis/
    ├── 01_burden_metrics_calculation.ipynb
    ├── 02_seasonal_trend_analysis.ipynb
    └── 03_outbreak_detection_model.ipynb
```

### Modular Analysis Functions
Extract reusable analysis code to `src/analysis/`:

```python
# src/analysis/burden_metrics.py

def calculate_incidence_rate(
    cases: pl.Series,
    population: int,
    per_population: int = 100_000
) -> pl.Series:
    """Calculate incidence rate per specified population.
    
    Args:
        cases: Series of case counts
        population: Total population at risk
        per_population: Rate per this many people (default: 100,000)
        
    Returns:
        Series of incidence rates
    """
    return (cases / population) * per_population

def calculate_disease_burden_score(
    incidence_rate: float,
    severity_weight: float,
    hospitalization_rate: float
) -> float:
    """Calculate composite disease burden score.
    
    Score combines incidence, severity, and healthcare utilization.
    
    Args:
        incidence_rate: Cases per 100k population
        severity_weight: Disease severity factor (0-1)
        hospitalization_rate: Proportion requiring hospitalization
        
    Returns:
        Burden score (0-100 scale)
    """
    raw_score = incidence_rate * severity_weight * (1 + hospitalization_rate)
    # Normalize to 0-100 scale
    normalized_score = min(100, raw_score / 10)
    return normalized_score
```

### Analysis Workflow Pattern

```python
# notebooks/2_analysis/01_burden_metrics_calculation.ipynb

# Cell 1: Imports
from pathlib import Path
import polars as pl
from src.analysis.burden_metrics import (
    calculate_incidence_rate,
    calculate_disease_burden_score
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Cell 2: Load processed data
PROCESSED_DATA = Path('data/4_processed')
df = pl.read_csv(PROCESSED_DATA / 'disease_data_featured.csv')
logger.info(f"Loaded {len(df):,} records")

# Cell 3: Load parameters
with open(Path('data/parameters/disease_parameters.json'), 'r') as f:
    disease_params = json.load(f)

# Cell 4: Calculate metrics
SINGAPORE_POPULATION = 5_686_000  # 2023 estimate

df = df.with_columns(
    calculate_incidence_rate(
        df['case_count'],
        SINGAPORE_POPULATION
    ).alias('incidence_rate')
)

# Cell 5: Save results
results_path = Path('data/4_processed/disease_burden_metrics.csv')
df.write_csv(results_path)
logger.info(f"Results saved: {results_path}")
```

---

## 7. Validation & Testing

### Statistical Validation
```python
import polars as pl
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

def validate_analysis_results(
    results: pl.DataFrame,
    expected_columns: List[str],
    value_ranges: Dict[str, Tuple[float, float]]
) -> bool:
    """Validate analysis results meet expectations.
    
    Args:
        results: DataFrame with analysis results
        expected_columns: Required column names
        value_ranges: Dict of {column: (min, max)} acceptable ranges
        
    Returns:
        True if all validations pass
        
    Raises:
        ValueError: If validation fails
    """
    # Check required columns
    missing_cols = set(expected_columns) - set(results.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check value ranges using Polars expressions
    for col, (min_val, max_val) in value_ranges.items():
        if col not in results.columns:
            continue
        
        out_of_range = results.filter(
            (pl.col(col) < min_val) | (pl.col(col) > max_val)
        ).height
        
        if out_of_range > 0:
            logger.warning(
                f"{out_of_range} values in '{col}' outside range "
                f"[{min_val}, {max_val}]"
            )
    
    # Check for unexpected nulls using Polars null_count
    null_checks = {col: results[col].null_count() for col in results.columns}
    nulls_found = {col: count for col, count in null_checks.items() if count > 0}
    if nulls_found:
        logger.warning(f"Null values found: {nulls_found}")
    
    logger.info("Analysis results validation completed")
    return True

# Usage
validate_analysis_results(
    df_metrics,
    expected_columns=['disease', 'incidence_rate', 'burden_score'],
    value_ranges={
        'incidence_rate': (0, 10000),
        'burden_score': (0, 100)
    }
)
```

### Sensitivity Analysis
Test robustness of results to parameter changes:

```python
import polars as pl
from typing import List, Callable
import logging

logger = logging.getLogger(__name__)

def run_sensitivity_analysis(
    data: pl.DataFrame,
    analysis_func: Callable,
    param_name: str,
    param_values: List[float]
) -> pl.DataFrame:
    """Run sensitivity analysis on analysis function.
    
    Args:
        data: Input data
        analysis_func: Function to test (must return DataFrame)
        param_name: Name of parameter to vary
        param_values: List of parameter values to test
        
    Returns:
        DataFrame with results for each parameter value
    """
    results = []
    
    for value in param_values:
        logger.info(f"Testing {param_name}={value}")
        
        result = analysis_func(data, **{param_name: value})
        
        # Add sensitivity tracking columns
        result = result.with_columns([
            pl.lit(param_name).alias('sensitivity_param'),
            pl.lit(value).alias('sensitivity_value')
        ])
        
        results.append(result)
    
    # Concatenate all results vertically
    combined_results = pl.concat(results, how='vertical')
    logger.info(f"Sensitivity analysis complete: tested {len(param_values)} values")
    
    return combined_results
```

---

## 8. Interpretation & Visualization

### Create Publication-Quality Figures

**CRITICAL**: ALL visualizations MUST be saved to local directories with timestamps.

Save all figures to `reports/figures/problem-statement-{num}/`:

```python
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_disease_burden_heatmap(
    df: pl.DataFrame,
    problem_statement_num: str = '001',
    save_name: str = 'disease_burden_heatmap'
) -> None:
    """Create heatmap of disease burden over time using pure Polars.
    
    Args:
        df: DataFrame with disease, time period, and burden metrics
        problem_statement_num: Problem statement number for directory organization
        save_name: Base name for saved file (timestamp added automatically)
    """
    from datetime import datetime
    logger.info("Creating disease burden heatmap")
    
    # Aggregate and pivot using Polars native pivot
    pivot_df = df.group_by(['disease', 'year']).agg(
        pl.col('burden_score').mean().alias('burden_score')
    )
    
    # Use Polars pivot (no pandas conversion needed!)
    pivot = pivot_df.pivot(
        values='burden_score',
        index='disease',
        columns='year',
        aggregate_function='first'  # Already aggregated above
    )
    
    # Convert to numpy for seaborn heatmap
    # Extract disease names and years for labels
    diseases = pivot['disease'].to_list()
    years = [col for col in pivot.columns if col != 'disease']
    
    # Get the numeric data matrix
    data_matrix = pivot.select(years).to_numpy()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.heatmap(
        data_matrix,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Burden Score'},
        xticklabels=years,
        yticklabels=diseases,
        ax=ax
    )
    
    ax.set_title(
        'Disease Burden Score by Year',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Disease', fontsize=12)
    
    plt.tight_layout()
    
    # Save with high DPI and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    figures_dir = Path(f'reports/figures/problem-statement-{problem_statement_num}')
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = figures_dir / f'{save_name}_{timestamp}.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    logger.info(f"✅ Figure saved: {save_path}")
    
    plt.show()
```

### Save Summary Tables

**CRITICAL**: ALL summary tables MUST be saved to local directories with timestamps.

Store summary tables in `results/tables/problem-statement-{num}/`:

```python
import polars as pl
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_summary_table(
    df: pl.DataFrame,
    problem_statement_num: str = '001',
    save_name: str = 'burden_metrics_summary'
) -> pl.DataFrame:
    """Create summary statistics table using Polars.
    
    Args:
        df: DataFrame with metrics
        problem_statement_num: Problem statement number for directory organization
        save_name: Base name for saved file (timestamp added automatically)
        
    Returns:
        Summary DataFrame
    """
    from datetime import datetime
    logger.info("Creating summary statistics table")
    
    # Modern Polars aggregation syntax
    summary = df.group_by('disease').agg([
        pl.col('case_count').sum().alias('total_cases'),
        pl.col('case_count').mean().alias('mean_cases'),
        pl.col('case_count').std().alias('std_cases'),
        pl.col('incidence_rate').mean().alias('avg_incidence_rate'),
        pl.col('incidence_rate').max().alias('max_incidence_rate'),
        pl.col('burden_score').mean().alias('avg_burden_score'),
        pl.col('burden_score').max().alias('max_burden_score')
    ]).sort('total_cases', descending=True)
    
    # Save with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tables_dir = Path(f'results/tables/problem-statement-{problem_statement_num}')
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = tables_dir / f'{save_name}_{timestamp}.csv'
    summary.write_csv(save_path)
    logger.info(f"✅ Summary table saved: {save_path} ({summary.height} diseases)")
    
    return summary
```

---

## 8.5 Data Lineage and Memory Optimization

### Track Data Transformations
Document all transformations for audit trails and reproducibility.

```python
import polars as pl
from datetime import datetime
from pathlib import Path
import json
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class DataLineage:
    \"\"\"Track data transformation lineage for audit trails.\"\"\"
    
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
        \"\"\"Log a data transformation step.
        
        Args:
            step_name: Name of transformation
            input_data: Input DataFrame
            output_data: Output DataFrame
            parameters: Transformation parameters
            user: User or process performing transformation
        \"\"\"
        lineage_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step_name,
            'user': user,
            'input_shape': {'rows': input_data.height, 'cols': input_data.width},
            'output_shape': {'rows': output_data.height, 'cols': output_data.width},
            'rows_added': output_data.height - input_data.height,
            'columns_added': output_data.width - input_data.width,
            'memory_before_mb': input_data.estimated_size() / (1024**2),
            'memory_after_mb': output_data.estimated_size() / (1024**2),
            'parameters': parameters
        }
        
        with open(self.lineage_file, 'a') as f:
            f.write(json.dumps(lineage_entry) + '\\n')
        
        logger.info(f\"Lineage logged: {step_name}\")\n\ndef transform_with_lineage(\n    df: pl.DataFrame,\n    transform_func: Callable,\n    step_name: str,\n    **kwargs\n) -> pl.DataFrame:\n    \"\"\"Apply transformation with automatic lineage tracking.\n    \n    Args:\n        df: Input DataFrame\n        transform_func: Transformation function\n        step_name: Name of transformation step\n        **kwargs: Parameters passed to transform_func\n        \n    Returns:\n        Transformed DataFrame\n    \"\"\"
    logger.info(f\"Starting: {step_name} | Input: {df.height} rows x {df.width} cols\")\n    \n    result = transform_func(df, **kwargs)\n    \n    logger.info(f\"Completed: {step_name} | Output: {result.height} rows x {result.width} cols\")\n    \n    # Log lineage\n    lineage = DataLineage()\n    lineage.log_transformation(\n        step_name=step_name,\n        input_data=df,\n        output_data=result,\n        parameters=kwargs\n    )\n    \n    return result\n\n# Usage\ndf_cleaned = transform_with_lineage(\n    df_raw,\n    clean_disease_data,\n    step_name=\"initial_cleaning\",\n    remove_duplicates=True\n)\n```

### Memory Optimization Techniques

```python\nimport polars as pl\nimport logging\n\nlogger = logging.getLogger(__name__)\n\ndef optimize_dataframe_memory(df: pl.DataFrame) -> pl.DataFrame:\n    \"\"\"Optimize DataFrame memory usage.\n    \n    Techniques:\n    - Downcast numeric types where possible\n    - Convert low-cardinality strings to Categorical\n    - Use appropriate date/time types\n    \n    Args:\n        df: Input DataFrame\n        \n    Returns:\n        Memory-optimized DataFrame\n    \"\"\"
    initial_memory = df.estimated_size() / (1024**2)\n    logger.info(f\"Initial memory usage: {initial_memory:.2f} MB\")\n    \n    df_optimized = df.clone()\n    \n    # Downcast integers\n    for col in df_optimized.columns:\n        dtype = df_optimized[col].dtype\n        \n        # Optimize integers\n        if dtype == pl.Int64:\n            max_val = df_optimized[col].max()\n            min_val = df_optimized[col].min()\n            \n            if max_val is not None and min_val is not None:\n                if min_val >= 0 and max_val < 255:\n                    df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.UInt8))\n                    logger.debug(f\"Optimized '{col}': Int64 -> UInt8\")\n                elif min_val >= 0 and max_val < 65535:\n                    df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.UInt16))\n                    logger.debug(f\"Optimized '{col}': Int64 -> UInt16\")\n                elif min_val >= -32768 and max_val < 32767:\n                    df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.Int16))\n                    logger.debug(f\"Optimized '{col}': Int64 -> Int16\")\n                elif min_val >= -2147483648 and max_val < 2147483647:\n                    df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.Int32))\n                    logger.debug(f\"Optimized '{col}': Int64 -> Int32\")\n        \n        # Convert low-cardinality strings to Categorical\n        elif dtype == pl.Utf8:\n            unique_count = df_optimized[col].n_unique()\n            total_count = df_optimized.height\n            \n            # If less than 50% unique values, consider categorical\n            if unique_count < total_count * 0.5 and unique_count < 1000:\n                df_optimized = df_optimized.with_columns(pl.col(col).cast(pl.Categorical))\n                logger.debug(f\"Optimized '{col}': Utf8 -> Categorical ({unique_count} unique)\")\n    \n    final_memory = df_optimized.estimated_size() / (1024**2)\n    saved_memory = initial_memory - final_memory\n    \n    logger.info(f\"Final memory usage: {final_memory:.2f} MB\")\n    logger.info(f\"Memory saved: {saved_memory:.2f} MB ({saved_memory/initial_memory*100:.1f}%)\")\n    \n    return df_optimized\n\n# Usage\ndf_optimized = optimize_dataframe_memory(df)\n```

### Lazy Evaluation for Large Datasets

```python\nimport polars as pl\nimport logging\n\nlogger = logging.getLogger(__name__)\n\ndef process_large_dataset_lazy(filepath: str) -> pl.DataFrame:\n    \"\"\"Process large dataset using lazy evaluation.\n    \n    Benefits:\n    - Query optimization\n    - Reduced memory footprint\n    - Faster execution\n    \n    Args:\n        filepath: Path to large CSV file\n        \n    Returns:\n        Processed DataFrame\n    \"\"\"
    logger.info(f\"Processing large dataset with lazy evaluation: {filepath}\")\n    \n    # Use scan_csv for lazy loading\n    result = (\n        pl.scan_csv(filepath)\n        .filter(pl.col('year') >= 2020)  # Filter early\n        .with_columns([\n            pl.col('date').str.strptime(pl.Date, format='%Y-%m-%d'),\n            pl.col('disease').cast(pl.Categorical)\n        ])\n        .group_by(['disease', 'year']).agg([\n            pl.col('cases').sum().alias('total_cases'),\n            pl.col('cases').mean().alias('mean_cases')\n        ])\n        .sort('total_cases', descending=True)\n        .collect()  # Execute query\n    )\n    \n    logger.info(f\"Query executed: {result.height} rows\")\n    return result\n\n# For very large datasets, use streaming\ndef process_huge_dataset_streaming(filepath: str) -> pl.DataFrame:\n    \"\"\"Process dataset that doesn't fit in memory using streaming.\"\"\"\n    logger.info(f\"Processing huge dataset with streaming: {filepath}\")\n    \n    result = (\n        pl.scan_csv(filepath)\n        .filter(pl.col('year') >= 2020)\n        .collect(streaming=True)  # Process in batches\n    )\n    \n    logger.info(f\"Streaming complete: {result.height} rows\")\n    return result\n```

---

## 9. Documentation & Communication

### Analysis Documentation Structure
```
docs/
├── objectives/              # Problem statements and goals
├── methodology/            # Analysis methods and approaches
├── data_dictionary/        # Data field definitions
├── domain_knowledge/       # Subject matter context
└── results/                # Analysis findings and reports
```

### Document Key Decisions
Create decision log for important analytical choices:

```markdown
# Analysis Decision Log

## Decision 001: Missing Value Handling
**Date**: 2024-02-10
**Context**: 3.2% of case_count values are missing in raw data
**Decision**: Drop rows with missing case_counts
**Rationale**: 
- Missing values are random (MCAR confirmed by Little's test)
- Small percentage won't bias results
- Imputation would introduce uncertainty in public health metrics
**Alternatives Considered**:
- Mean imputation: Rejected - artificial inflation of case counts
- Zero-fill: Rejected - misrepresents actual missing data
**Impact**: Dataset reduced from 12,845 to 12,433 rows

## Decision 002: Outbreak Threshold Selection
**Date**: 2024-02-11
**Context**: Need to define outbreak alert threshold
**Decision**: Use 2 standard deviations above 4-week rolling mean
**Rationale**:
- Balances sensitivity (95% confidence) with specificity
- 4-week window smooths weekly reporting variations
- Aligns with WHO outbreak detection guidelines
**Parameters**: threshold_std=2.0, window=4 weeks
```

### Create Analysis Reports
```python
def generate_analysis_report(
    summary_stats: Dict,
    figures: List[str],
    output_path: str = 'docs/results/analysis_report.md'
) -> None:
    """Generate markdown analysis report.
    
    Args:
        summary_stats: Dictionary of key statistics
        figures: List of figure paths to include
        output_path: Where to save report
    """
    report = f"""# Disease Burden Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Analysis Period**: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}

## Executive Summary

This analysis examined disease burden patterns across {summary_stats['n_diseases']} 
infectious diseases over {summary_stats['n_years']} years.

### Key Findings

1. **Highest Burden Disease**: {summary_stats['top_disease']} 
   - Total cases: {summary_stats['top_disease_cases']:,}
   - Peak incidence: {summary_stats['peak_incidence']:.1f} per 100k

2. **Seasonal Patterns**: Clear seasonality detected in {summary_stats['n_seasonal']} diseases

3. **Trend Analysis**: {summary_stats['increasing_diseases']} diseases show 
   increasing trends over study period

## Visualizations

"""
    
    for fig_path in figures:
        report += f"![{Path(fig_path).stem}]({fig_path})\n\n"
    
    report += f"""
## Methodology

- **Data Source**: Weekly disease surveillance bulletins
- **Analysis Period**: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}
- **Metrics Calculated**: Incidence rate, disease burden score
- **Statistical Methods**: Time series decomposition, trend analysis

## Data Quality

- **Completeness**: {summary_stats['completeness']:.1f}%
- **Records Analyzed**: {summary_stats['n_records']:,}
- **Data Quality Score**: {summary_stats['quality_score']:.1f}/100

## Recommendations

Based on this analysis, we recommend:

1. Enhanced surveillance for high-burden diseases
2. Seasonal preparedness planning for diseases with clear seasonal patterns
3. Further investigation into increasing disease trends

---
*Full analysis code available in notebooks/2_analysis/*
"""
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    logger.info(f"Analysis report saved: {output_path}")
```

---

## 10. Deployment & Monitoring

### Automate Reproducible Workflows
Create scripts in `scripts/` for end-to-end pipeline:

```python
# scripts/run_full_analysis_pipeline.py

"""
Complete analysis pipeline automation.
Run: python scripts/run_full_analysis_pipeline.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing.validation import load_disease_data
from src.data_processing.profiling import profile_dataset
from src.analysis.burden_metrics import calculate_all_metrics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Run complete analysis pipeline."""
    
    logger.info("="*60)
    logger.info("Starting Disease Burden Analysis Pipeline")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("="*60)
    
    try:
        # Stage 1: Load raw data
        logger.info("\n[1/5] Loading raw data...")
        df_raw = load_disease_data('data/1_raw/disease_surveillance.csv')
        
        # Stage 2: Data profiling
        logger.info("\n[2/5] Profiling data...")
        profile = profile_dataset(df_raw, 'disease_surveillance')
        
        # Stage 3: Data cleaning
        logger.info("\n[3/5] Cleaning data...")
        from src.data_processing.cleaning import clean_disease_data
        df_clean = clean_disease_data(df_raw)
        
        # Save interim
        df_clean.to_csv('data/3_interim/disease_data_cleaned.csv', index=False)
        
        # Stage 4: Calculate metrics
        logger.info("\n[4/5] Calculating burden metrics...")
        df_metrics = calculate_all_metrics(df_clean)
        
        # Save processed
        df_metrics.to_csv('data/4_processed/disease_burden_metrics.csv', index=False)
        
        # Stage 5: Generate outputs
        logger.info("\n[5/5] Generating visualizations and reports...")
        from src.visualization.plots import create_all_figures
        from src.reporting.summary import generate_analysis_report
        
        create_all_figures(df_metrics)
        generate_analysis_report(df_metrics)
        
        logger.info("\n" + "="*60)
        logger.info("Pipeline completed successfully!")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Version Control for Analysis
Tag analysis versions in git:

```bash
# After completing major analysis milestone
git tag -a v1.0-burden-analysis -m "Initial disease burden analysis complete"
git push origin v1.0-burden-analysis
```

### Create Analysis Manifest
Document exact environment and data versions:

```json
{
  "analysis_id": "burden-analysis-v1.0",
  "timestamp": "2024-02-11T14:30:00Z",
  "analyst": "Public Health Team",
  "data_sources": [
    {
      "file": "data/1_raw/disease_surveillance_2020-2023.csv",
      "md5_hash": "a3f5e1b2c4d5e6f7a8b9c0d1e2f3a4b5",
      "row_count": 12845
    }
  ],
  "environment": {
    "python_version": "3.10.12",
    "key_packages": {
      "polars": "0.20.0",
      "numpy": "1.24.3",
      "scikit-learn": "1.3.0"
    }
  },
  "parameters": {
    "outbreak_threshold_std": 2.0,
    "rolling_window_weeks": 4,
    "singapore_population": 5686000
  },
  "outputs": [
    "data/4_processed/disease_burden_metrics.csv",
    "results/figures/disease_burden_heatmap.png",
    "results/tables/burden_metrics_summary.csv"
  ]
}
```

---

## Summary Checklist

### ✅ For Each Analysis Project

**Planning Phase**
- [ ] Problem statement documented
- [ ] Success criteria defined
- [ ] Data requirements identified
- [ ] Stakeholders consulted

**Data Collection**
- [ ] Raw data stored in `data/1_raw/` (read-only)
- [ ] External data documented in `data/2_external/`
- [ ] Data provenance tracked
- [ ] .gitignore configured

**Exploration**
- [ ] Data profiling report generated
- [ ] EDA notebook created
- [ ] Data quality issues documented
- [ ] Unexpected findings noted

**Preparation**
- [ ] Cleaning steps documented
- [ ] Interim data saved to `data/3_interim/`
- [ ] Data quality report generated
- [ ] Missing value strategy documented

**Feature Engineering**
- [ ] Features engineered and documented
- [ ] Final dataset saved to `data/4_processed/`
- [ ] README.md created for processed data
- [ ] Data types optimized

**Analysis**
- [ ] Analysis notebooks organized in `notebooks/2_analysis/`
- [ ] Reusable functions extracted to `src/`
- [ ] Results validated
- [ ] Sensitivity analysis conducted

**Visualization & Communication**
- [ ] Publication-quality figures created
- [ ] Summary tables generated
- [ ] Analysis report written
- [ ] Key decisions documented
- [ ] **ALL figures saved to `reports/figures/problem-statement-{num}/` with timestamps**
- [ ] **ALL tables saved to `results/tables/problem-statement-{num}/` with timestamps**
- [ ] **ALL metrics saved to `results/metrics/problem-statement-{num}/` with timestamps**
- [ ] **Confirmation messages printed for all saved outputs**
- [ ] **Output directories created with proper structure**

**Deployment**
- [ ] Pipeline script created
- [ ] Analysis reproducible
- [ ] Environment documented
- [ ] Version tagged in git

---

## Anti-Patterns to Avoid

### ❌ Don't Do This

1. **Modifying raw data in place**
   ```python
   # BAD - Never do this!
   df_raw = pl.read_csv('data/1_raw/original.csv')
   df_raw['new_column'] = calculation()
   df_raw.to_csv('data/1_raw/original.csv', index=False)  # Overwrites original!
   ```

2. **Analysis without exploration**
   - Jumping straight to modeling without understanding your data
   - Not checking distributions, missing values, or outliers first

3. **Undocumented transformations**
   ```python
   # BAD - What did this do?
   df2 = df1.copy()
   df2['x'] = df2['x'] * 2.5
   df2 = df2[df2['y'] > threshold]
   ```

4. **Hard-to-reproduce analysis**
   - Manual Excel manipulations not scripted
   - Point-and-click tools without audit trail
   - "Final_FINAL_v3" file naming

5. **Results without validation**
   - Not checking if results make domain sense
   - No sensitivity analysis
   - Ignoring data quality issues

6. **Missing documentation**
   - No README explaining what files are
   - No data dictionary
   - No methodology notes

---

## Tools and Libraries

### Recommended Python Stack
```python
# Core data manipulation - REQUIRED
polars>=0.20.0
numpy>=1.24.0

# Configuration and validation
pyyaml>=6.0.1
pydantic>=2.5.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0  # For interactive dashboards

# Statistical analysis
scipy>=1.10.0
statsmodels>=0.14.0
scikit-learn>=1.3.0

# Database and storage
sqlalchemy>=2.0.23
pyarrow>=14.0.0  # For Parquet support

# Parallel processing
joblib>=1.3.2

# Utilities
python-dotenv>=1.0.0  # Environment variables
```

### Development Tools
```python
# Testing and code quality
pytest>=7.4.3
black>=23.12.0
flake8>=6.1.0

# Performance profiling
line-profiler>=4.1.1
memory-profiler>=0.61.0

# Notebooks
jupyter>=1.0.0
```

### Package Management with UV (Project Standard)
**ALWAYS use `uv` for package management** - faster and more reliable than pip.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # Unix/macOS
# or
.venv\\Scripts\\activate  # Windows

# Install packages
uv pip install polars numpy pyyaml pydantic matplotlib

# Install from requirements.txt
uv pip install -r requirements.txt

# Sync exact versions (for reproducibility)
uv pip sync requirements.txt

# Generate requirements.txt with exact versions
uv pip freeze > requirements.txt

# Install dev dependencies
uv pip install -r requirements-dev.txt
```

### Useful Commands

```bash
# Package management with UV
uv pip install polars numpy pyyaml
uv pip freeze > requirements.txt
uv pip sync requirements.txt

# Run full analysis pipeline
python scripts/run_full_analysis_pipeline.py

# Run specific analysis notebook
jupyter nbconvert --to notebook --execute notebooks/2_analysis/01_burden_metrics.ipynb

# Clear notebook outputs before committing
jupyter nbconvert --clear-output --inplace notebooks/**/*.ipynb

# Check data file hash for versioning
md5 data/1_raw/disease_surveillance.csv  # macOS
# or
certutil -hashfile data/1_raw/disease_surveillance.csv MD5  # Windows

# Profile Python script performance
python -m line_profiler script.py.lprof  # After decorating with @profile

# Memory profiling
python -m memory_profiler script.py
```

---

## 🤖 LLM Instruction Summary

When writing or reviewing data analysis code:

### ✅ ALWAYS Do:
- Load raw data from `data/1_raw/` (read-only)
- Validate data immediately after loading
- Use type hints: `def func(df: pl.DataFrame, col: str) -> pl.Series:`
- Log with `logger.info()`, `logger.warning()`, `logger.error()`
- Save checkpoints to `data/3_interim/` with descriptive names
- Save final outputs to `data/4_processed/` with README.md
- Use constants: `SINGAPORE_POPULATION = 5_686_000`
- Handle exceptions: `try/except` with specific exception types
- Document transformations in docstrings
- Generate quality reports after cleaning
- **Create ALL visualizations in `reports/figures/problem-statement-{num}/` with timestamps**
- **Create ALL summary tables in `results/tables/problem-statement-{num}/` with timestamps**
- **Create ALL metrics in `results/metrics/problem-statement-{num}/` with timestamps**
- **Print confirmation messages showing saved file paths**

### ❌ NEVER Do:
- Modify files in `data/1_raw/`
- Use `print()` for logging in production code
- Use hardcoded paths: `/Users/john/Desktop/data.csv`
- Use magic numbers without explanation
- Silence exceptions with bare `except: pass`
- Leave undocumented transformations
- Create "final_v2_FINAL.py" files
- Skip data validation steps
- Ignore missing values without strategy
- Overwrite processed data without versioning
from datetime import datetime
import logging
from pathlib import Path
import json

# 0. Setup logger (REQUIRED)
logger = logging.getLogger(__name__)

# 0.1 Setup output directories (REQUIRED)
PROBLEM_STATEMENT_NUM = '001'  # Adjust as needed
FIGURES_DIR = Path(f'reports/figures/problem-statement-{PROBLEM_STATEMENT_NUM}')
RESULTS_DIR = Path(f'results/tables/problem-statement-{PROBLEM_STATEMENT_NUM}')
METRICS_DIR = Path(f'results/metrics/problem-statement-{PROBLEM_STATEMENT_NUM}')

for dir_path in [FIGURES_DIR, RESULTS_DIR, METRICS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. Load configuration (recommended)
from src.utils.config import load_config
config = load_config('config/analysis.yml')

# 2. Load and validate raw data
df_raw = load_disease_data('data/1_raw/surveillance.csv')

# 3. Clean and save interim
df_clean = clean_disease_data(df_raw)
df_clean.write_csv('data/3_interim/surveillance_cleaned.csv')

# 4. Feature engineering
df_featured = engineer_features(df_clean)

# 5. Calculate metrics with lineage tracking
df_metrics = transform_with_lineage(
    df_featured,
    calculate_burden_metrics,
    step_name=\"burden_calculation\",
    config=config
)

# 6. Optimize and save final dataset
df_optimized = optimize_dataframe_memory(df_metrics)
df_optimized.write_csv('data/4_processed/disease_burden_metrics.csv')

# 7. Generate and SAVE outputs (REQUIRED)
# Save visualizations
create_visualizations(df_optimized, figures_dir=FIGURES_DIR, timestamp=timestamp)

# Save summary tables
summary_df = create_summary_table(df_optimized)
summary_path = RESULTS_DIR / f'summary_statistics_{timestamp}.csv'
summary_df.write_csv(summary_path)
logger.info(f\"✅ Saved summary: {summary_path}\")

# Save metrics
metrics = calculate_quality_metrics(df_optimized)
metrics_path = METRICS_DIR / f'quality_metrics_{timestamp}.json'
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2)
logger.info(f\"✅ Saved metrics: {metrics_path}\")

logger.info(\"✅ Analysis pipeline completed successfully\")
logger.info(f\"All outputs saved with timestamp: {timestamp}\")

# 7. Generate outputs
create_visualizations(df_optimized, save_path='results/figures/')
create_summary_table(df_optimized, save_path='results/tables/')

logger.info(\"Analysis pipeline completed successfully\")\n```

### 🚀 Modern Polars Features to Use:
- **Lazy evaluation**: Use `pl.scan_csv()` for large files
- **Streaming**: Use `.collect(streaming=True)` for huge datasets
- **Memory optimization**: Categorical dtypes, proper Int sizes (UInt8, Int16, Int32)
- **Native pivot**: Use `df.pivot()` instead of pandas conversion
- **Expressions**: Use `pl.col()` expressions for transformations
- **Window functions**: Use `.over()` for grouped operations

---

**Remember**: Good data analysis is reproducible, well-documented, uses pure Polars, and tells a clear story from data to insights.