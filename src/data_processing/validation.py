"""
Data Validation Functions for Cleaned Workforce and Capacity Data
User Story 2: Data Cleaning and Standardization

This module provides validation functions to ensure cleaned data meets quality standards:
- Schema validation (column presence, data types)
- Value range validation (years, counts, categorical values)
- Referential integrity checks
- Data quality thresholds verification

All validation functions raise descriptive errors on failure for clear debugging.
"""

import polars as pl
from loguru import logger
from typing import Dict, List, Optional
from datetime import datetime


def validate_schema(df: pl.DataFrame, expected_schema: Dict[str, pl.DataType]) -> bool:
    """
    Validate DataFrame schema against expected column names and data types.
    
    Args:
        df: DataFrame to validate
        expected_schema: Dictionary mapping column names to expected Polars data types
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If required columns are missing
        TypeError: If column data types don't match expected types
        
    Example:
        >>> schema = {'year': pl.Int32, 'sector': pl.Categorical}
        >>> validate_schema(df, schema)
    """
    logger.info(f"Validating schema ({len(expected_schema)} columns)")
    
    # Check all expected columns present
    missing_cols = set(expected_schema.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check data types
    type_mismatches = []
    for col, expected_dtype in expected_schema.items():
        actual_dtype = df[col].dtype
        if actual_dtype != expected_dtype:
            type_mismatches.append(f"Column '{col}': expected {expected_dtype}, got {actual_dtype}")
    
    if type_mismatches:
        raise TypeError(f"Data type mismatches:\n" + "\n".join(type_mismatches))
    
    logger.success("Schema validation passed")
    return True


def validate_value_ranges(
    df: pl.DataFrame,
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allow_null: bool = False
) -> bool:
    """
    Validate that values in a column fall within specified range.
    
    Args:
        df: DataFrame to validate
        column: Column name to check
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        allow_null: Whether null values are permitted
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If column not found or values outside range or nulls present when not allowed
        
    Example:
        >>> validate_value_ranges(df, 'year', min_value=2006, max_value=2019)
    """
    logger.info(f"Validating value ranges for column '{column}'")
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Check for nulls
    null_count = df[column].null_count()
    if null_count > 0 and not allow_null:
        raise ValueError(f"Column '{column}' contains {null_count} null values (not allowed)")
    
    # Check min value
    if min_value is not None:
        actual_min = df[column].min()
        if actual_min is not None and actual_min < min_value:
            raise ValueError(f"Column '{column}' has value {actual_min} < minimum {min_value}")
    
    # Check max value
    if max_value is not None:
        actual_max = df[column].max()
        if actual_max is not None and actual_max > max_value:
            raise ValueError(f"Column '{column}' has value {actual_max} > maximum {max_value}")
    
    logger.success(f"Value range validation passed for '{column}'")
    return True


def validate_categorical_values(
    df: pl.DataFrame,
    column: str,
    valid_values: List[str],
    allow_null: bool = False
) -> bool:
    """
    Validate that all values in a categorical column are in the allowed set.
    
    Args:
        df: DataFrame to validate
        column: Column name to check
        valid_values: List of allowed categorical values
        allow_null: Whether null values are permitted
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If column not found or invalid values present
        
    Example:
        >>> validate_categorical_values(df, 'sector', ['Public', 'Private', 'Not-for-Profit'])
    """
    logger.info(f"Validating categorical values for column '{column}'")
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Check for nulls
    null_count = df[column].null_count()
    if null_count > 0 and not allow_null:
        raise ValueError(f"Column '{column}' contains {null_count} null values (not allowed)")
    
    # Get unique values (excluding nulls)
    unique_values = df[column].drop_nulls().unique().to_list()
    
    # Check for invalid values
    invalid_values = set(unique_values) - set(valid_values)
    if invalid_values:
        raise ValueError(f"Column '{column}' contains invalid values: {invalid_values}. Allowed: {valid_values}")
    
    logger.success(f"Categorical validation passed for '{column}' ({len(unique_values)} unique values)")
    return True


def validate_no_duplicates(
    df: pl.DataFrame,
    subset: List[str]
) -> bool:
    """
    Validate that DataFrame has no duplicate records on specified columns.
    
    Args:
        df: DataFrame to validate
        subset: List of column names that define uniqueness
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If duplicate records found
        
    Example:
        >>> validate_no_duplicates(df, ['year', 'sector', 'profession'])
    """
    logger.info(f"Validating no duplicates on columns: {subset}")
    
    # Check all subset columns exist
    missing_cols = set(subset) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Subset columns not found: {missing_cols}")
    
    # Count duplicates
    total_rows = len(df)
    df_unique = df.unique(subset=subset)
    unique_rows = len(df_unique)
    duplicate_count = total_rows - unique_rows
    
    if duplicate_count > 0:
        dup_pct = (duplicate_count / total_rows * 100) if total_rows > 0 else 0
        raise ValueError(f"Found {duplicate_count} duplicate records ({dup_pct:.2f}%) on columns {subset}")
    
    logger.success(f"No duplicates found on specified columns")
    return True


def validate_completeness(
    df: pl.DataFrame,
    critical_columns: List[str],
    target_completeness: float = 100.0
) -> bool:
    """
    Validate data completeness meets target threshold.
    
    Args:
        df: DataFrame to validate
        critical_columns: Columns that must meet completeness threshold
        target_completeness: Target completeness percentage (default 100%)
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If completeness below target for any critical column
        
    Example:
        >>> validate_completeness(df, ['year', 'sector', 'count'], target_completeness=100.0)
    """
    logger.info(f"Validating completeness for {len(critical_columns)} critical columns (target: {target_completeness}%)")
    
    failures = []
    
    for col in critical_columns:
        if col not in df.columns:
            failures.append(f"Column '{col}' not found in DataFrame")
            continue
        
        total_rows = len(df)
        null_count = df[col].null_count()
        completeness = ((total_rows - null_count) / total_rows * 100) if total_rows > 0 else 0
        
        if completeness < target_completeness:
            failures.append(
                f"Column '{col}': {completeness:.2f}% completeness < target {target_completeness}% "
                f"({null_count}/{total_rows} nulls)"
            )
    
    if failures:
        raise ValueError(f"Completeness validation failed:\n" + "\n".join(failures))
    
    logger.success(f"Completeness validation passed for all critical columns")
    return True


def validate_workforce_data(df: pl.DataFrame, config: Dict) -> bool:
    """
    Comprehensive validation for cleaned workforce data.
    
    Validates schema, year ranges, sectors, professions, counts, and completeness.
    
    Args:
        df: Cleaned workforce DataFrame
        config: Configuration dictionary with validation rules
        
    Returns:
        True if all validations pass
        
    Raises:
        ValueError/TypeError: If any validation fails
    """
    logger.info("=== Validating Cleaned Workforce Data ===")
    
    # Define expected schema
    expected_schema = {
        'year': pl.Int32,
        'sector': pl.Categorical,
        'profession': pl.Categorical,
        'count': pl.Int32,
        'source_table': pl.String,
        'outlier_flag': pl.Boolean,
        'has_missing_values': pl.Boolean
    }
    
    # Schema validation
    validate_schema(df, expected_schema)
    
    # Year range validation
    validate_value_ranges(
        df, 'year',
        min_value=config['value_constraints']['workforce']['year_min'],
        max_value=config['value_constraints']['workforce']['year_max'],
        allow_null=False
    )
    
    # Count validation (must be non-negative)
    validate_value_ranges(
        df, 'count',
        min_value=config['value_constraints']['workforce']['min_count'],
        allow_null=False
    )
    
    # Sector validation
    validate_categorical_values(
        df, 'sector',
        valid_values=config['valid_values']['sectors'],
        allow_null=False
    )
    
    # Profession validation
    validate_categorical_values(
        df, 'profession',
        valid_values=config['valid_values']['professions'],
        allow_null=False
    )
    
    # Completeness validation
    critical_cols = ['year', 'sector', 'profession', 'count']
    validate_completeness(
        df, critical_cols,
        target_completeness=config['quality_thresholds']['completeness_target']
    )
    
    # No duplicates on key columns
    validate_no_duplicates(df, ['year', 'sector', 'profession', 'specialist_category', 'nurse_type', 'source_table'])
    
    logger.success("=== Workforce Data Validation PASSED ===")
    return True


def validate_capacity_data(df: pl.DataFrame, config: Dict) -> bool:
    """
    Comprehensive validation for cleaned capacity data.
    
    Validates schema, year ranges, sectors, facility types, counts, and completeness.
    
    Args:
        df: Cleaned capacity DataFrame
        config: Configuration dictionary with validation rules
        
    Returns:
        True if all validations pass
        
    Raises:
        ValueError/TypeError: If any validation fails
    """
    logger.info("=== Validating Cleaned Capacity Data ===")
    
    # Define expected schema (flexible for capacity data variations)
    expected_columns = ['year', 'sector', 'num_facilities', 'source_table']
    
    # Check critical columns exist
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns in capacity data: {missing_cols}")
    
    # Year range validation
    validate_value_ranges(
        df, 'year',
        min_value=config['value_constraints']['capacity']['year_min'],
        max_value=config['value_constraints']['capacity']['year_max'],
        allow_null=False
    )
    
    # Facility count validation
    validate_value_ranges(
        df, 'num_facilities',
        min_value=config['value_constraints']['capacity']['min_count'],
        allow_null=False
    )
    
    # Sector validation (allow nulls for primary care which doesn't have sector in original data)
    validate_categorical_values(
        df, 'sector',
        valid_values=config['valid_values']['sectors'],
        allow_null=True  # Some capacity data may not have sector
    )
    
    # Completeness validation
    critical_cols = ['year', 'num_facilities']
    validate_completeness(
        df, critical_cols,
        target_completeness=config['quality_thresholds']['completeness_target']
    )
    
    logger.success("=== Capacity Data Validation PASSED ===")
    return True


def generate_validation_report(
    df: pl.DataFrame,
    dataset_name: str,
    validation_results: Dict[str, bool]
) -> str:
    """
    Generate a markdown validation report.
    
    Args:
        df: Validated DataFrame
        dataset_name: Name of the dataset
        validation_results: Dictionary of validation check names and pass/fail status
        
    Returns:
        Markdown-formatted validation report
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""# Data Validation Report: {dataset_name}

**Generated**: {timestamp}  
**Total Records**: {len(df):,}  
**Total Columns**: {len(df.columns)}

## Validation Results

| Check | Status |
|-------|--------|
"""
    
    for check_name, passed in validation_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        report += f"| {check_name} | {status} |\n"
    
    # Add schema summary
    report += f"\n## Schema Summary\n\n"
    report += "| Column | Data Type | Null Count | Null % |\n"
    report += "|--------|-----------|------------|--------|\n"
    
    total_rows = len(df)
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = df[col].null_count()
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0
        report += f"| {col} | {dtype} | {null_count:,} | {null_pct:.2f}% |\n"
    
    # Add value summaries for key columns
    report += f"\n## Key Column Statistics\n\n"
    
    if 'year' in df.columns:
        report += f"**Year Range**: {df['year'].min()} - {df['year'].max()}\n\n"
    
    if 'sector' in df.columns:
        sector_counts = df.group_by('sector').agg(pl.count().alias('count')).sort('count', descending=True)
        report += "**Sector Distribution**:\n\n"
        for row in sector_counts.iter_rows(named=True):
            report += f"- {row['sector']}: {row['count']:,}\n"
        report += "\n"
    
    if 'profession' in df.columns:
        prof_counts = df.group_by('profession').agg(pl.count().alias('count')).sort('count', descending=True)
        report += "**Profession Distribution**:\n\n"
        for row in prof_counts.iter_rows(named=True):
            report += f"- {row['profession']}: {row['count']:,}\n"
        report += "\n"
    
    report += f"\n---\n*Validation completed successfully*\n"
    
    return report
