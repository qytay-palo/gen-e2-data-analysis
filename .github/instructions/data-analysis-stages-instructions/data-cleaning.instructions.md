---
name: 'Data Cleaning and Preprocessing'
description: 'Standards for data cleaning, transformation, and preprocessing operations'
applyTo: 'src/data_processing/*clean*.py, src/data_processing/*preprocess*.py, data/3_interim/**, notebooks/1_exploratory/*clean*.ipynb, src/problem-statement-**/notebooks/**clean**.ipynb, scripts/clean_*.py'
---

## Purpose
This document defines **mandatory data cleaning standards** for preprocessing raw data. Apply these practices to ensure consistent, high-quality data for analysis.

## Core Principles

### 1. Never Modify Raw Data
- **NEVER overwrite files** in `data/1_raw/`
- Always save cleaned data to `data/3_interim/` or `data/4_processed/`
- Maintain full audit trail of cleaning operations

### 2. Explicit Transformations
- Log every cleaning operation with counts affected
- Document the reasoning behind cleaning decisions
- Make transformations reversible when possible

### 3. Preserve Data Lineage
- Track which raw files produced which cleaned files
- Include timestamps in output filenames
- Save cleaning parameters in configuration files

## Required Cleaning Operations

### 1. Categorical Data Standardization (MANDATORY)

**Case Normalization**
```python
import polars as pl
from loguru import logger

def standardize_categorical_columns(
    df: pl.DataFrame,
    columns: list[str],
    case_method: str = "title"  # Options: 'upper', 'lower', 'title'
) -> pl.DataFrame:
    """
    Standardize categorical data by normalizing case and whitespace.
    
    Args:
        df: Input dataframe
        columns: List of categorical columns to standardize
        case_method: Case normalization method ('upper', 'lower', 'title')
    
    Returns:
        DataFrame with standardized categorical columns
    """
    df_clean = df.clone()
    
    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column '{col}' not found in dataframe")
            continue
        
        # Count unique values before cleaning
        unique_before = df[col].n_unique()
        
        # Apply standardization pipeline
        if case_method == "upper":
            df_clean = df_clean.with_columns(
                pl.col(col).str.strip_chars().str.to_uppercase().alias(col)
            )
        elif case_method == "lower":
            df_clean = df_clean.with_columns(
                pl.col(col).str.strip_chars().str.to_lowercase().alias(col)
            )
        elif case_method == "title":
            df_clean = df_clean.with_columns(
                pl.col(col).str.strip_chars().str.to_titlecase().alias(col)
            )
        
        # Count after cleaning
        unique_after = df_clean[col].n_unique()
        
        logger.info(
            f"Standardized '{col}': {unique_before} → {unique_after} unique values "
            f"({unique_before - unique_after} duplicates merged)"
        )
    
    return df_clean


# Example usage for disease names
df_clean = standardize_categorical_columns(
    df_raw,
    columns=['disease', 'region', 'age_group'],
    case_method='title'
)
```

**Custom Value Mapping**
```python
def apply_value_mappings(
    df: pl.DataFrame,
    column: str,
    mapping: dict[str, str]
) -> pl.DataFrame:
    """
    Apply custom mappings to standardize categorical values.
    
    Example:
        mappings = {
            'dengue': 'Dengue Fever',
            'DENGUE': 'Dengue Fever',
            'Dengue fever': 'Dengue Fever',
            'DF': 'Dengue Fever'
        }
    """
    # Create case-insensitive mapping
    normalized_mapping = {
        k.lower().strip(): v for k, v in mapping.items()
    }
    
    df_clean = df.with_columns(
        pl.col(column)
        .str.to_lowercase()
        .str.strip_chars()
        .replace(normalized_mapping)
        .alias(column)
    )
    
    # Log changes
    changed = df.filter(pl.col(column) != df_clean[column]).height
    logger.info(f"Applied {len(mapping)} mappings to '{column}': {changed} rows affected")
    
    return df_clean
```

### 2. Missing Value Handling

**Null Detection and Reporting**
```python
def report_missing_values(df: pl.DataFrame, output_path: str = None) -> pl.DataFrame:
    """Generate missing value report for all columns."""
    missing_report = pl.DataFrame({
        'column': df.columns,
        'missing_count': [df[col].null_count() for col in df.columns],
        'missing_pct': [
            round(100 * df[col].null_count() / df.height, 2) 
            for col in df.columns
        ],
        'dtype': [str(df[col].dtype) for col in df.columns]
    }).filter(pl.col('missing_count') > 0).sort('missing_pct', descending=True)
    
    logger.info(f"Missing values found in {missing_report.height} columns")
    
    if output_path:
        missing_report.write_csv(output_path)
        logger.info(f"Missing value report saved to {output_path}")
    
    return missing_report


# Example: Selective null handling
df_clean = (
    df.clone()
    # Drop rows where critical columns are null
    .drop_nulls(subset=['date', 'disease', 'case_count'])
    # Fill numeric nulls with 0 (document why)
    .with_columns([
        pl.col('death_count').fill_null(0),  # Assume no deaths if not reported
        pl.col('hospitalized').fill_null(0)
    ])
    # Keep nulls in optional fields
    .with_columns([
        pl.col('notes').fill_null('N/A')
    ])
)

logger.info(f"Rows after null handling: {df.height} → {df_clean.height}")
```

### 3. Duplicate Removal

```python
def remove_duplicates(
    df: pl.DataFrame,
    subset: list[str] = None,
    keep: str = 'first'
) -> pl.DataFrame:
    """
    Remove duplicate rows with logging.
    
    Args:
        df: Input dataframe
        subset: Columns to consider for duplicate detection
        keep: Which duplicate to keep ('first', 'last', 'none')
    """
    initial_rows = df.height
    
    if keep == 'none':
        # Remove all duplicates (keep unique only)
        df_clean = df.unique(subset=subset, maintain_order=True)
        duplicates_mask = df.select(subset).is_duplicated()
        df_clean = df.filter(~duplicates_mask)
    else:
        df_clean = df.unique(subset=subset, keep=keep, maintain_order=True)
    
    rows_removed = initial_rows - df_clean.height
    logger.warning(
        f"Removed {rows_removed} duplicate rows "
        f"({100 * rows_removed / initial_rows:.2f}%) - kept '{keep}'"
    )
    
    return df_clean
```

### 4. Data Type Validation and Conversion

```python
def enforce_data_types(
    df: pl.DataFrame,
    schema: dict[str, pl.DataType]
) -> pl.DataFrame:
    """
    Enforce data types with error handling.
    
    Example schema:
        {
            'date': pl.Date,
            'disease': pl.Categorical,
            'case_count': pl.Int32,
            'region_code': pl.Utf8
        }
    """
    df_clean = df.clone()
    
    for col, dtype in schema.items():
        if col not in df.columns:
            logger.warning(f"Schema column '{col}' not found in dataframe")
            continue
        
        try:
            if dtype == pl.Date:
                # Handle date parsing
                df_clean = df_clean.with_columns(
                    pl.col(col).str.strptime(pl.Date, '%Y-%m-%d', strict=False)
                )
            elif dtype == pl.Categorical:
                # Convert to categorical for memory efficiency
                df_clean = df_clean.with_columns(
                    pl.col(col).cast(pl.Categorical)
                )
            else:
                df_clean = df_clean.with_columns(
                    pl.col(col).cast(dtype, strict=False)
                )
            
            logger.info(f"Converted '{col}' to {dtype}")
        
        except Exception as e:
            logger.error(f"Failed to convert '{col}' to {dtype}: {e}")
            raise
    
    return df_clean
```

### 5. Outlier Detection and Handling

```python
def detect_outliers_iqr(
    df: pl.DataFrame,
    column: str,
    multiplier: float = 1.5
) -> pl.DataFrame:
    """
    Detect outliers using Interquartile Range (IQR) method.
    
    Args:
        df: Input dataframe
        column: Numeric column to check
        multiplier: IQR multiplier (1.5 = standard, 3.0 = extreme)
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    
    outliers = df.filter(
        (pl.col(column) < lower_bound) | (pl.col(column) > upper_bound)
    )
    
    logger.warning(
        f"Found {outliers.height} outliers in '{column}' "
        f"(range: {lower_bound:.2f} - {upper_bound:.2f})"
    )
    
    return outliers


# Example: Cap outliers instead of removing
def cap_outliers(df: pl.DataFrame, column: str, multiplier: float = 1.5) -> pl.DataFrame:
    """Cap outliers at IQR boundaries."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    
    df_clean = df.with_columns(
        pl.col(column).clip(lower_bound, upper_bound).alias(column)
    )
    
    capped = df.filter(
        (pl.col(column) < lower_bound) | (pl.col(column) > upper_bound)
    ).height
    
    logger.info(f"Capped {capped} outliers in '{column}'")
    return df_clean
```

### 6. Date and Time Standardization

```python
def standardize_dates(
    df: pl.DataFrame,
    date_columns: list[str],
    date_format: str = '%Y-%m-%d'
) -> pl.DataFrame:
    """
    Parse and standardize date columns.
    
    Handles multiple input formats and converts to consistent output.
    """
    df_clean = df.clone()
    
    for col in date_columns:
        # Try common date formats
        formats_to_try = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y%m%d',
            '%d-%b-%Y'
        ]
        
        parsed = False
        for fmt in formats_to_try:
            try:
                df_clean = df_clean.with_columns(
                    pl.col(col).str.strptime(pl.Date, fmt, strict=False)
                )
                parsed = True
                logger.info(f"Parsed '{col}' using format '{fmt}'")
                break
            except:
                continue
        
        if not parsed:
            logger.error(f"Could not parse dates in column '{col}'")
            raise ValueError(f"Date parsing failed for '{col}'")
    
    return df_clean
```

## Cleaning Pipeline Template

```python
# src/data_processing/cleaner.py
import polars as pl
from pathlib import Path
from datetime import datetime
from loguru import logger
import yaml

class DataCleaner:
    """Template for standardized data cleaning pipelines."""
    
    def __init__(self, config_path: str):
        """Load cleaning configuration from YAML."""
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        logger.info(f"Loaded cleaning config: {config_path}")
    
    def clean(self, df_raw: pl.DataFrame) -> pl.DataFrame:
        """Execute full cleaning pipeline."""
        logger.info(f"Starting cleaning pipeline: {df_raw.height} rows")
        
        df = df_raw.clone()
        
        # 1. Standardize categorical columns
        if 'categorical_columns' in self.config:
            df = standardize_categorical_columns(
                df,
                columns=self.config['categorical_columns'],
                case_method=self.config.get('case_method', 'title')
            )
        
        # 2. Apply value mappings
        if 'value_mappings' in self.config:
            for col, mappings in self.config['value_mappings'].items():
                df = apply_value_mappings(df, col, mappings)
        
        # 3. Handle missing values
        if 'drop_nulls' in self.config:
            df = df.drop_nulls(subset=self.config['drop_nulls'])
        
        if 'fill_nulls' in self.config:
            for col, fill_value in self.config['fill_nulls'].items():
                df = df.with_columns(pl.col(col).fill_null(fill_value))
        
        # 4. Remove duplicates
        if 'deduplicate' in self.config:
            df = remove_duplicates(
                df,
                subset=self.config['deduplicate'].get('subset'),
                keep=self.config['deduplicate'].get('keep', 'first')
            )
        
        # 5. Enforce data types
        if 'schema' in self.config:
            df = enforce_data_types(df, self.config['schema'])
        
        # 6. Validate ranges
        if 'range_validation' in self.config:
            for col, bounds in self.config['range_validation'].items():
                invalid = df.filter(
                    (pl.col(col) < bounds['min']) | (pl.col(col) > bounds['max'])
                ).height
                
                if invalid > 0:
                    logger.warning(
                        f"{invalid} rows in '{col}' outside "
                        f"range [{bounds['min']}, {bounds['max']}]"
                    )
        
        logger.info(f"Cleaning complete: {df.height} rows ({df_raw.height - df.height} removed)")
        return df
    
    def save_cleaned_data(
        self,
        df: pl.DataFrame,
        output_dir: Path,
        filename_prefix: str
    ) -> Path:
        """Save cleaned data with timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"{filename_prefix}_cleaned_{timestamp}.csv"
        
        df.write_csv(output_path)
        logger.info(f"Saved cleaned data: {output_path}")
        
        return output_path


# Example usage
if __name__ == '__main__':
    from pathlib import Path
    
    # Load raw data
    df_raw = pl.read_csv('data/1_raw/disease_surveillance.csv')
    
    # Initialize cleaner with config
    cleaner = DataCleaner('config/cleaning_rules.yml')
    
    # Execute cleaning pipeline
    df_clean = cleaner.clean(df_raw)
    
    # Save results
    output_path = cleaner.save_cleaned_data(
        df_clean,
        Path('data/3_interim'),
        'disease_surveillance'
    )
```

## Example Cleaning Configuration

```yaml
# config/cleaning_rules.yml
categorical_columns:
  - disease
  - region
  - age_group
  - sex

case_method: title  # Options: upper, lower, title

value_mappings:
  disease:
    'dengue': 'Dengue Fever'
    'DENGUE': 'Dengue Fever'
    'Dengue fever': 'Dengue Fever'
    'DF': 'Dengue Fever'
    'HFMD': 'Hand Foot Mouth Disease'
    'hand, foot and mouth disease': 'Hand Foot Mouth Disease'
  
  region:
    'central': 'Central'
    'CENTRAL': 'Central'
    'north': 'North'
    'NORTH': 'North'

drop_nulls:
  - date
  - disease
  - case_count

fill_nulls:
  death_count: 0
  hospitalized_count: 0
  notes: 'N/A'

deduplicate:
  subset:
    - date
    - disease
    - region
  keep: first

schema:
  date: Date
  disease: Categorical
  region: Categorical
  case_count: Int32
  death_count: Int32

range_validation:
  case_count:
    min: 0
    max: 100000
  year:
    min: 2000
    max: 2030

### ✅ DO
```python
# Log all transformations
initial_rows = df.height
df_clean = df.drop_nulls(subset=['date', 'case_count'])
logger.info(f"Removed {initial_rows - df_clean.height} rows with null critical fields")

# Standardize categorical data systematically
df_clean = standardize_categorical_columns(
    df,
    columns=['disease', 'region'],
    case_method='title'
)

# Save to interim/processed directories
df_clean.write_csv('data/3_interim/cleaned_data_20260309.csv')

# Document outlier handling decisions
# Comment: Remove case counts > 10,000 after consulting epidemiologist
# These are likely data entry errors (max historical outbreak = 8,500 cases)
df_clean = df.filter(pl.col('case_count') <= 10000)

# Use configuration-driven mappings
with open('config/cleaning_rules.yml') as f:
    mappings = yaml.safe_load(f)['value_mappings']
df_clean = apply_value_mappings(df, 'disease', mappings['disease'])
```

## Quality Checks After Cleaning

```python
def validate_cleaned_data(df: pl.DataFrame) -> dict:
    """Run post-cleaning validation checks."""
    checks = {
        'total_rows': df.height,
        'total_columns': df.width,
        'null_counts': {col: df[col].null_count() for col in df.columns},
        'duplicate_rows': df.height - df.unique().height,
        'categorical_consistency': {}
    }
    
    # Check categorical columns have consistent casing
    categorical_cols = [col for col in df.columns if df[col].dtype == pl.Categorical]
    for col in categorical_cols:
        values = df[col].unique().to_list()
        # Check if any values differ only by case
        normalized = {v.lower() for v in values if v is not None}
        checks['categorical_consistency'][col] = {
            'unique_values': len(values),
            'case_variants': len(values) - len(normalized)
        }
    
    logger.info(f"Validation complete: {checks}")
    return checks
```

## Logging Standards

```python
# Configure logging for cleaning operations
from loguru import logger
from pathlib import Path

# Setup log file
log_dir = Path('logs/etl')
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    log_dir / 'data_cleaning_{time:YYYY-MM-DD}.log',
    rotation='1 day',
    retention='30 days',
    level='INFO'
)

# Always log:
# 1. Initial data dimensions
logger.info(f"Loaded raw data: {df.shape}")

# 2. Each transformation with counts
logger.info(f"Standardized 'disease' column: {before} → {after} unique values")

# 3. Final data dimensions
logger.info(f"Cleaning complete: {df_clean.shape}")

# 4. Output file paths
logger.info(f"Saved to: {output_path}")
```

## Summary Checklist

Before moving cleaned data to `data/4_processed/`:

- [ ] Categorical columns standardized (consistent casing and whitespace)
- [ ] Value mappings applied from configuration files
- [ ] Missing values handled explicitly with logging
- [ ] Duplicates removed or documented why kept
- [ ] Data types validated and enforced
- [ ] Outliers detected and handled appropriately
- [ ] Date formats standardized
- [ ] Validation report generated
- [ ] All transformations logged with counts
- [ ] Configuration file saved with cleaning parameters
- [ ] Output saved to `data/3_interim/` with timestamp
