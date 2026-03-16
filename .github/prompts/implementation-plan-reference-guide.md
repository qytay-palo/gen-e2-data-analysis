# Implementation Plan Reference Guide

> Supporting documentation for `3-generate-data-analysis-implementation-plan.prompt.md`

## Table of Contents
1. [Code Executability Standards](#code-executability-standards)
2. [Code Examples by Section](#code-examples-by-section)
   - [Section 6.2: Data Schemas](#section-62-data-schemas)
   - [Section 6.3: Data Validation Rules](#section-63-data-validation-rules)
   - [Section 6.3.5: String Normalization Patterns](#section-635-string-normalization-patterns)
   - [Section 6.4: Library-Specific Patterns](#section-64-library-specific-patterns)
3. [Testing Patterns](#testing-patterns)
4. [Security Patterns](#security-patterns)
5. [Common Anti-Patterns](#common-anti-patterns)
6. [Package Management](#package-management)
7. [Performance Optimization](#performance-optimization)

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

### Section 6.3.5: String Normalization Patterns

**Comprehensive String Cleaning:**
```python
import polars as pl
from loguru import logger
from typing import Dict, List
import unicodedata

def normalize_string_column(
    df: pl.DataFrame,
    column: str,
    operations: List[str] = ['strip', 'lower', 'remove_extra_spaces']
) -> pl.DataFrame:
    """Normalize string column with specified operations.
    
    Args:
        df: Input DataFrame
        column: Column name to normalize
        operations: List of operations to apply in order
            Options: 'strip', 'lower', 'upper', 'title', 'remove_extra_spaces',
                    'remove_special_chars', 'remove_numbers'
    
    Returns:
        DataFrame with normalized string column
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    df_norm = df.clone()
    
    for op in operations:
        if op == 'strip':
            df_norm = df_norm.with_columns(
                pl.col(column).str.strip_chars().alias(column)
            )
        elif op == 'lower':
            df_norm = df_norm.with_columns(
                pl.col(column).str.to_lowercase().alias(column)
            )
        elif op == 'upper':
            df_norm = df_norm.with_columns(
                pl.col(column).str.to_uppercase().alias(column)
            )
        elif op == 'title':
            df_norm = df_norm.with_columns(
                pl.col(column).str.to_titlecase().alias(column)
            )
        elif op == 'remove_extra_spaces':
            # Replace multiple spaces with single space
            df_norm = df_norm.with_columns(
                pl.col(column).str.replace_all(r'\s+', ' ').alias(column)
            )
        elif op == 'remove_special_chars':
            # Keep only alphanumeric and spaces
            df_norm = df_norm.with_columns(
                pl.col(column).str.replace_all(r'[^a-zA-Z0-9\s]', '').alias(column)
            )
        elif op == 'remove_numbers':
            df_norm = df_norm.with_columns(
                pl.col(column).str.replace_all(r'\d+', '').alias(column)
            )
    
    logger.info(f"Normalized column '{column}' with operations: {operations}")
    return df_norm


def standardize_similar_values(
    df: pl.DataFrame,
    column: str,
    similarity_threshold: float = 0.8,
    min_frequency: int = 2,
    case_sensitive: bool = False
) -> pl.DataFrame:
    """Automatically detect and standardize similar values in a column.
    
    Analyzes unique values and groups similar strings together, standardizing
    to the most common variant in each group.
    
    Args:
        df: Input DataFrame
        column: Column name to analyze and standardize
        similarity_threshold: Similarity score threshold (0-1) for grouping values
                            Higher = more strict matching
        min_frequency: Minimum frequency for a value to be kept as standard
        case_sensitive: Whether to consider case when comparing strings
    
    Returns:
        DataFrame with standardized column values
        
    Example:
        # Will group: "Registered Nurse", "Registered  Nurse", "registered nurse"
        # Into: "Registered Nurse" (most common variant)
        df = standardize_similar_values(df, 'profession', similarity_threshold=0.85)
    """
    from difflib import SequenceMatcher
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Get value counts
    value_counts = df[column].value_counts().to_pandas()
    unique_values = value_counts[column].tolist()
    
    # Normalize for comparison if not case sensitive
    if not case_sensitive:
        comparison_values = [str(v).lower().strip() for v in unique_values]
    else:
        comparison_values = [str(v).strip() for v in unique_values]
    
    # Group similar values
    groups = []
    processed = set()
    
    for i, val in enumerate(comparison_values):
        if i in processed:
            continue
        
        # Start a new group with this value
        group = {
            'indices': [i],
            'values': [unique_values[i]],
            'counts': [value_counts.iloc[i]['count']]
        }
        
        # Find similar values
        for j in range(i + 1, len(comparison_values)):
            if j in processed:
                continue
            
            # Calculate similarity
            similarity = SequenceMatcher(None, val, comparison_values[j]).ratio()
            
            if similarity >= similarity_threshold:
                group['indices'].append(j)
                group['values'].append(unique_values[j])
                group['counts'].append(value_counts.iloc[j]['count'])
                processed.add(j)
        
        processed.add(i)
        groups.append(group)
    
    # Build mapping: choose most frequent variant as standard
    value_mapping = {}
    standardization_log = []
    
    for group in groups:
        if len(group['values']) > 1:
            # Find most common variant
            max_count_idx = group['counts'].index(max(group['counts']))
            standard_value = group['values'][max_count_idx]
            
            # Map all variants to standard
            for idx, variant in enumerate(group['values']):
                if variant != standard_value:
                    value_mapping[variant] = standard_value
                    standardization_log.append({
                        'from': variant,
                        'to': standard_value,
                        'count': group['counts'][idx]
                    })
    
    # Log standardization actions
    if standardization_log:
        logger.info(f"Auto-standardizing {len(standardization_log)} variants in '{column}':")
        for item in standardization_log[:10]:  # Show first 10
            logger.info(f"  '{item['from']}' -> '{item['to']}' ({item['count']} rows)")
        if len(standardization_log) > 10:
            logger.info(f"  ... and {len(standardization_log) - 10} more")
    else:
        logger.info(f"No similar values detected in '{column}' (threshold={similarity_threshold})")
    
    # Apply mapping
    if value_mapping:
        df_std = df.with_columns([
            pl.col(column).replace(value_mapping, default=pl.col(column)).alias(column)
        ])
        
        unique_before = len(unique_values)
        unique_after = df_std[column].n_unique()
        logger.info(f"Reduced unique values: {unique_before} -> {unique_after}")
        
        return df_std
    else:
        return df.clone()


def standardize_column_values(
    df: pl.DataFrame,
    column: str,
    value_mapping: Dict[str, str],
    normalize_first: bool = True,
    unmapped_case: str = 'title'
) -> pl.DataFrame:
    """Standardize column values using a mapping dictionary.
    
    Generic function for standardizing any string column to consistent values.
    
    Args:
        df: Input DataFrame
        column: Column name to standardize
        value_mapping: Dictionary mapping variations to standard values
        normalize_first: If True, normalize strings before mapping (lowercase, strip, etc.)
        unmapped_case: Case transformation for unmapped values ('title', 'upper', 'lower', 'keep')
    
    Returns:
        DataFrame with standardized column values
        
    Example:
        profession_mapping = {
            'registered nurse': 'Nurse',
            'rn': 'Nurse',
            'staff nurse': 'Nurse',
            'medical doctor': 'Doctor',
            'physician': 'Doctor',
            'md': 'Doctor'
        }
        df = standardize_column_values(df, 'profession', profession_mapping)
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    df_std = df.clone()
    
    # Track unique values before standardization
    unique_before = df[column].n_unique()
    
    if normalize_first:
        # Step 1: Basic normalization
        df_std = df_std.with_columns([
            pl.col(column)
              .str.strip_chars()
              .str.to_lowercase()
              .str.replace_all(r'\s+', ' ')  # Remove extra spaces
              .alias(f'{column}_normalized')
        ])
        
        # Step 2: Apply mapping
        df_std = df_std.with_columns([
            pl.col(f'{column}_normalized')
              .replace(value_mapping, default=pl.col(f'{column}_normalized'))
              .alias(column)
        ])
        
        # Step 3: Apply case transformation to unmapped values
        if unmapped_case == 'title':
            df_std = df_std.with_columns([
                pl.when(pl.col(column).is_in(list(value_mapping.values())))
                  .then(pl.col(column))
                  .otherwise(pl.col(column).str.to_titlecase())
                  .alias(column)
            ])
        elif unmapped_case == 'upper':
            df_std = df_std.with_columns([
                pl.when(pl.col(column).is_in(list(value_mapping.values())))
                  .then(pl.col(column))
                  .otherwise(pl.col(column).str.to_uppercase())
                  .alias(column)
            ])
        elif unmapped_case == 'lower':
            df_std = df_std.with_columns([
                pl.when(pl.col(column).is_in(list(value_mapping.values())))
                  .then(pl.col(column))
                  .otherwise(pl.col(column).str.to_lowercase())
                  .alias(column)
            ])
        # 'keep' - no transformation
        
        df_std = df_std.drop(f'{column}_normalized')
    else:
        # Direct mapping without normalization
        df_std = df_std.with_columns([
            pl.col(column)
              .replace(value_mapping, default=pl.col(column))
              .alias(column)
        ])
    
    # Log the mapping results
    unique_after = df_std[column].n_unique()
    logger.info(f"Standardized '{column}': {unique_before} unique values -> {unique_after}")
    
    return df_std


def standardize_disease_names(df: pl.DataFrame) -> pl.DataFrame:
    """Standardize disease names to consistent format.
    
    Example implementation using standardize_column_values for disease surveillance data.
    """
    # Define mapping for known variations
    disease_mapping = {
        'hand foot and mouth disease': 'HFMD',
        'hand, foot and mouth disease': 'HFMD',
        'hfmd': 'HFMD',
        'dengue fever': 'Dengue',
        'dengue': 'Dengue',
        'df': 'Dengue',
        'tuberculosis': 'TB',
        'tb': 'TB',
        'chicken pox': 'Chickenpox',
        'chickenpox': 'Chickenpox',
        'varicella': 'Chickenpox'
    }
    
    return standardize_column_values(
        df, 
        column='disease',
        value_mapping=disease_mapping,
        normalize_first=True,
        unmapped_case='title'
    )


def standardize_profession_names(df: pl.DataFrame) -> pl.DataFrame:
    """Standardize healthcare profession names.
    
    Example for workforce data.
    """
    profession_mapping = {
        'registered nurse': 'Nurse',
        'rn': 'Nurse',
        'staff nurse': 'Nurse',
        'enrolled nurse': 'Enrolled Nurse',
        'en': 'Enrolled Nurse',
        'medical doctor': 'Doctor',
        'physician': 'Doctor',
        'md': 'Doctor',
        'general practitioner': 'General Practitioner',
        'gp': 'General Practitioner',
        'pharmacist': 'Pharmacist',
        'pharmacy': 'Pharmacist',
        'allied health': 'Allied Health Professional',
        'ahp': 'Allied Health Professional'
    }
    
    return standardize_column_values(
        df,
        column='profession',
        value_mapping=profession_mapping,
        normalize_first=True,
        unmapped_case='title'
    )


def clean_region_names(df: pl.DataFrame, region_col: str = 'region') -> pl.DataFrame:
    """Clean and standardize region/location names."""
    valid_regions = {'North', 'South', 'East', 'West', 'Central'}
    
    df_clean = (
        df.clone()
        # Normalize to title case
        .with_columns([
            pl.col(region_col)
              .str.strip_chars()
              .str.to_titlecase()
              .alias(region_col)
        ])
        # Validate against allowed values
        .with_columns([
            pl.when(pl.col(region_col).is_in(valid_regions))
              .then(pl.col(region_col))
              .otherwise(pl.lit(None))  # Set invalid to null for investigation
              .alias(region_col)
        ])
    )
    
    # Log invalid regions
    invalid_count = df_clean[region_col].null_count()
    if invalid_count > 0:
        logger.warning(f"Found {invalid_count} invalid region values, set to null")
    
    return df_clean


# Pattern: Intelligent standardization workflow
def smart_standardize_column(
    df: pl.DataFrame,
    column: str,
    known_mappings: Dict[str, str] = None,
    auto_detect: bool = True,
    similarity_threshold: float = 0.85
) -> pl.DataFrame:
    """Two-stage standardization: manual mappings + auto-detection.
    
    Best practice pattern combining explicit rules with intelligent detection.
    
    Args:
        df: Input DataFrame
        column: Column to standardize
        known_mappings: Dictionary of known value mappings (applied first)
        auto_detect: Whether to auto-detect similar values after manual mapping
        similarity_threshold: Threshold for auto-detection
        
    Returns:
        DataFrame with fully standardized column
        
    Example:
        # Stage 1: Apply known standardizations
        # Stage 2: Auto-detect remaining similar values
        known = {'rn': 'Nurse', 'md': 'Doctor'}
        df = smart_standardize_column(df, 'profession', known, auto_detect=True)
    """
    df_result = df.clone()
    
    # Stage 1: Apply known mappings
    if known_mappings:
        logger.info(f"Applying {len(known_mappings)} known mappings to '{column}'")
        df_result = standardize_column_values(
            df_result,
            column=column,
            value_mapping=known_mappings,
            normalize_first=True,
            unmapped_case='title'
        )
    
    # Stage 2: Auto-detect similar values
    if auto_detect:
        logger.info(f"Auto-detecting similar values in '{column}'")
        df_result = standardize_similar_values(
            df_result,
            column=column,
            similarity_threshold=similarity_threshold,
            case_sensitive=False
        )
    
    return df_result


# Pattern: Batch normalize multiple columns
def normalize_multiple_columns(
    df: pl.DataFrame,
    column_operations: Dict[str, List[str]]
) -> pl.DataFrame:
    """Apply different normalization operations to multiple columns.
    
    Args:
        df: Input DataFrame
        column_operations: Dict mapping column names to lists of operations
        
    Example:
        column_operations = {
            'disease': ['strip', 'lower'],
            'region': ['strip', 'title'],
            'notes': ['strip', 'remove_extra_spaces']
        }
    """
    df_result = df.clone()
    
    for col, ops in column_operations.items():
        df_result = normalize_string_column(df_result, col, ops)
    
    return df_result


# Pattern: Remove unicode and special characters
def remove_unicode_artifacts(df: pl.DataFrame, column: str) -> pl.DataFrame:
    """Remove common unicode artifacts from text data."""
    df_clean = df.with_columns([
        pl.col(column)
          .str.replace_all(r'[^\x00-\x7F]+', '')  # Remove non-ASCII
          .str.replace_all(r'[\u200b-\u200d\ufeff]', '')  # Remove zero-width chars
          .str.replace_all(r'[\r\n\t]+', ' ')  # Replace newlines/tabs with space
          .str.strip_chars()
          .alias(column)
    ])
    
    return df_clean


# Pattern: Standardize date strings before parsing
def standardize_date_strings(df: pl.DataFrame, date_col: str) -> pl.DataFrame:
    """Standardize various date string formats to YYYY-MM-DD."""
    df_std = (
        df.clone()
        .with_columns([
            pl.col(date_col)
              .str.strip_chars()
              # Replace common separators with hyphen
              .str.replace_all(r'[/.]', '-')
              .alias(date_col)
        ])
    )
    
    return df_std
```

**Complete Example: Disease Data Cleaning Pipeline:**
```python
import polars as pl
from loguru import logger
from pathlib import Path

def clean_disease_surveillance_data(
    input_path: str,
    output_path: str,
    use_auto_standardization: bool = True
) -> pl.DataFrame:
    """Complete cleaning pipeline for disease surveillance data.
    
    Demonstrates comprehensive string normalization with both manual and
    intelligent auto-detection approaches.
    
    Args:
        input_path: Path to raw data file
        output_path: Path to save cleaned data
        use_auto_standardization: Enable intelligent similarity detection
    """
    logger.info(f"Loading data from {input_path}")
    df_raw = pl.read_csv(input_path)
    
    initial_rows = len(df_raw)
    logger.info(f"Loaded {initial_rows} rows")
    
    # Step 1: Normalize string columns (whitespace, case, etc.)
    df_clean = normalize_multiple_columns(df_raw, {
        'disease': ['strip', 'lower'],
        'region': ['strip', 'title'],
        'notes': ['strip', 'remove_extra_spaces']
    })
    
    # Step 2: Standardize disease names using known mappings
    disease_mapping = {
        'hfmd': 'HFMD',
        'dengue fever': 'Dengue',
        'tb': 'TB'
    }
    df_clean = standardize_column_values(
        df_clean,
        column='disease',
        value_mapping=disease_mapping,
        normalize_first=True
    )
    
    # Step 3: Auto-detect and fix similar disease name variants
    if use_auto_standardization:
        df_clean = standardize_similar_values(
            df_clean,
            column='disease',
            similarity_threshold=0.85,
            case_sensitive=False
        )
    
    # Step 4: Clean region names
    df_clean = clean_region_names(df_clean, region_col='region')
    
    # Step 5: Remove rows with invalid regions (if any)
    before_filter = len(df_clean)
    df_clean = df_clean.drop_nulls(subset=['region'])
    filtered = before_filter - len(df_clean)
    if filtered > 0:
        logger.warning(f"Removed {filtered} rows with invalid regions")
    
    # Step 6: Standardize date format
    df_clean = standardize_date_strings(df_clean, date_col='date')
    
    # Step 7: Convert to categorical for memory efficiency
    df_clean = df_clean.with_columns([
        pl.col('disease').cast(pl.Categorical),
        pl.col('region').cast(pl.Categorical)
    ])
    
    # Save cleaned data
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    df_clean.write_csv(output_path)
    
    logger.info(f"Cleaned data saved to {output_path}")
    logger.info(f"Final row count: {len(df_clean)} ({len(df_clean)/initial_rows:.1%} retained)")
    
    return df_clean
```

**Standardization Strategy Decision Guide:**

| Approach | When to Use | Advantages | Limitations |
|----------|------------|------------|-------------|
| **Manual Mapping** (`standardize_column_values`) | - Known value variations<br>- Business rules required<br>- Domain-specific abbreviations | - Full control<br>- Explicit logic<br>- Predictable output | - Requires upfront knowledge<br>- Maintenance overhead |
| **Auto-Detection** (`standardize_similar_values`) | - Unknown variations<br>- Messy data sources<br>- Exploratory cleaning | - Discovers patterns automatically<br>- No mapping needed<br>- Adapts to data | - May group incorrectly<br>- Requires threshold tuning |
| **Hybrid** (`smart_standardize_column`) | - Most real-world scenarios | - Best of both worlds<br>- Catches edge cases | - Slightly more complex |

**Usage Examples:**

```python
# Approach 1: Manual only (full control)
df = standardize_column_values(df, 'profession', known_mappings)

# Approach 2: Auto-detection only (exploratory)
df = standardize_similar_values(df, 'profession', similarity_threshold=0.85)

# Approach 3: Hybrid (recommended for production)
df = smart_standardize_column(
    df, 
    column='profession',
    known_mappings={'rn': 'Nurse', 'md': 'Doctor'},
    auto_detect=True,
    similarity_threshold=0.85
)

# Approach 4: Inspect before applying
# First, check what auto-detection would find
unique_vals = df['profession'].value_counts()
print(unique_vals)  # Review the variations

# Then apply with appropriate threshold
df = standardize_similar_values(df, 'profession', similarity_threshold=0.90)
```

**Tuning Similarity Threshold:**

The `similarity_threshold` parameter controls how strict the matching is:

- **0.95 - 1.0** (Very strict): Only catches typos, extra spaces
  - Example: "Registered Nurse" ≈ "Registered  Nurse" (extra space)
  
- **0.85 - 0.95** (Recommended): Catches missing words, minor variations
  - Example: "Registered Nurse" ≈ "Nurse Registered" ≈ "Regd Nurse"
  
- **0.70 - 0.85** (Moderate): More fuzzy matching
  - Example: "Medical Doctor" ≈ "Doctor" ≈ "Med Doctor"
  
- **0.50 - 0.70** (Loose): Aggressive grouping, may over-match
  - Risk: "Nurse" might match "Nurse Practitioner" incorrectly

**Best Practice Workflow:**
```python
# 1. Start strict and inspect results
df_test = standardize_similar_values(df, 'column', similarity_threshold=0.95)
print(df_test['column'].value_counts())

# 2. Gradually lower threshold if needed
df_test = standardize_similar_values(df, 'column', similarity_threshold=0.85)
print(df_test['column'].value_counts())

# 3. Apply final threshold
df_clean = standardize_similar_values(df, 'column', similarity_threshold=0.88)
```

**Quick Reference: Common String Operations in Polars:**
```python
import polars as pl

# Remove leading/trailing whitespace
df = df.with_columns(pl.col('text').str.strip_chars())

# Case conversion
df = df.with_columns(pl.col('text').str.to_lowercase())
df = df.with_columns(pl.col('text').str.to_uppercase())
df = df.with_columns(pl.col('text').str.to_titlecase())

# Replace operations
df = df.with_columns(
    pl.col('text').str.replace('old', 'new')  # First occurrence
)
df = df.with_columns(
    pl.col('text').str.replace_all('pattern', 'replacement')  # All occurrences
)

# Regex operations
df = df.with_columns(
    pl.col('text').str.replace_all(r'\d+', '')  # Remove all digits
)
df = df.with_columns(
    pl.col('text').str.replace_all(r'\s+', ' ')  # Collapse whitespace
)

# Extract patterns
df = df.with_columns(
    pl.col('text').str.extract(r'(\d{4})', 1).alias('year')  # Extract year
)

# Contains and filtering
df = df.filter(pl.col('text').str.contains('keyword'))
df = df.filter(~pl.col('text').str.contains(r'\d'))  # No digits

# Length operations
df = df.with_columns(pl.col('text').str.len_chars().alias('text_length'))

# Padding
df = df.with_columns(
    pl.col('id').str.pad_start(5, '0')  # Zero-pad to 5 chars
)

# Splitting
df = df.with_columns(
    pl.col('text').str.split(',').alias('text_list')  # Returns list
)
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
