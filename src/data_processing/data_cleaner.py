"""
Data Cleaning Functions for Workforce and Capacity Data
User Story 2: Data Cleaning and Standardization

This module provides core data cleaning and standardization functions:
- Column name standardization
- Data type conversions
- Sector name standardization
- Table unification (workforce/capacity)
- Missing value handling
- Duplicate detection and removal
- Outlier detection and flagging

All functions are designed to be defensive, logging all transformations
and preserving data lineage.
"""

import polars as pl
from loguru import logger
from typing import Dict, List, Optional, Tuple
from datetime import datetime


def standardize_column_names(
    df: pl.DataFrame,
    column_mapping: Dict[str, str]
) -> pl.DataFrame:
    """
    Rename columns according to mapping dictionary.
    
    Args:
        df: Input DataFrame
        column_mapping: Dictionary mapping old column names to new names
        
    Returns:
        DataFrame with renamed columns
        
    Raises:
        ValueError: If columns in mapping don't exist in DataFrame
        
    Example:
        >>> mapping = {'Year': 'year', 'Sector Name': 'sector'}
        >>> df_renamed = standardize_column_names(df, mapping)
    """
    logger.info(f"Standardizing {len(column_mapping)} column names")
    
    # Validate all columns in mapping exist
    missing_cols = set(column_mapping.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
    
    df_renamed = df.rename(column_mapping)
    logger.success(f"Renamed columns: {list(column_mapping.values())}")
    
    return df_renamed


def unify_workforce_tables(
    doctors_df: pl.DataFrame,
    nurses_df: pl.DataFrame,
    pharmacists_df: pl.DataFrame
) -> pl.DataFrame:
    """
    Consolidate workforce tables into single unified DataFrame.
    
    Adds 'profession' column to identify source. Handles profession-specific 
    columns by creating nullable columns for all variations.
    
    Args:
        doctors_df: Doctors workforce data (with 'specialist_category')
        nurses_df: Nurses workforce data (with 'nurse_type')
        pharmacists_df: Pharmacists workforce data
        
    Returns:
        Unified DataFrame with profession column and all fields
        
    Example:
        >>> unified = unify_workforce_tables(doctors_df, nurses_df, pharmacists_df)
        >>> assert set(unified['profession'].unique()) == {'Doctor', 'Nurse', 'Pharmacist'}
    """
    logger.info("Unifying workforce tables (doctors, nurses, pharmacists)")
    
    # Count input records
    doctor_count = len(doctors_df)
    nurse_count = len(nurses_df)
    pharmacist_count = len(pharmacists_df)
    total_input = doctor_count + nurse_count + pharmacist_count
    
    logger.debug(f"Input counts: Doctors={doctor_count}, Nurses={nurse_count}, Pharmacists={pharmacist_count}")
    
    # Add profession column to each table
    doctors_df = doctors_df.with_columns([
        pl.lit('Doctor').alias('profession'),
        pl.lit('workforce_doctors').alias('source_table')
    ])
    
    nurses_df = nurses_df.with_columns([
        pl.lit('Nurse').alias('profession'),
        pl.lit('workforce_nurses').alias('source_table')
    ])
    
    pharmacists_df = pharmacists_df.with_columns([
        pl.lit('Pharmacist').alias('profession'),
        pl.lit('workforce_pharmacists').alias('source_table')
    ])
    
    # Add profession-specific columns as nulls to tables that don't have them
    if 'specialist_category' not in nurses_df.columns:
        nurses_df = nurses_df.with_columns(pl.lit(None).cast(pl.String).alias('specialist_category'))
    if 'specialist_category' not in pharmacists_df.columns:
        pharmacists_df = pharmacists_df.with_columns(pl.lit(None).cast(pl.String).alias('specialist_category'))
    
    if 'nurse_type' not in doctors_df.columns:
        doctors_df = doctors_df.with_columns(pl.lit(None).cast(pl.String).alias('nurse_type'))
    if 'nurse_type' not in pharmacists_df.columns:
        pharmacists_df = pharmacists_df.with_columns(pl.lit(None).cast(pl.String).alias('nurse_type'))
    
    # Concatenate all tables
    unified_df = pl.concat([doctors_df, nurses_df, pharmacists_df], how='diagonal')
    
    # Verify row count
    total_output = len(unified_df)
    if total_output != total_input:
        logger.warning(f"Row count mismatch: input={total_input}, output={total_output}")
    else:
        logger.success(f"Unified workforce data: {total_output} records from 3 tables")
    
    # Verify profession distribution
    profession_counts = unified_df.group_by('profession').agg(pl.count().alias('count'))
    logger.info(f"Profession distribution:\n{profession_counts}")
    
    return unified_df


def unify_capacity_tables(
    hospital_beds_df: pl.DataFrame,
    primary_care_df: pl.DataFrame
) -> pl.DataFrame:
    """
    Consolidate capacity tables into single unified DataFrame.
    
    Adds 'institution_category' to distinguish hospital vs primary care facilities.
    
    Args:
        hospital_beds_df: Hospital beds capacity data
        primary_care_df: Primary care facilities data
        
    Returns:
        Unified DataFrame with institution_category column
    """
    logger.info("Unifying capacity tables (hospital beds, primary care)")
    
    # Count input records
    hospital_count = len(hospital_beds_df)
    primary_count = len(primary_care_df)
    total_input = hospital_count + primary_count
    
    logger.debug(f"Input counts: Hospital beds={hospital_count}, Primary care={primary_count}")
    
    # Add category and source columns
    hospital_beds_df = hospital_beds_df.with_columns([
        pl.lit('Hospital').alias('institution_category'),
        pl.lit('capacity_hospital_beds').alias('source_table')
    ])
    
    primary_care_df = primary_care_df.with_columns([
        pl.lit('Primary Care').alias('institution_category'),
        pl.lit('capacity_primary_care').alias('source_table')
    ])
    
    # Handle schema differences - add missing columns as nulls
    # Hospital beds has: num_beds
    # Primary care doesn't have: num_beds
    if 'num_beds' not in primary_care_df.columns:
        primary_care_df = primary_care_df.with_columns(
            pl.lit(None).cast(pl.Int64).alias('num_beds')
        )
    
    # Concatenate tables
    unified_df = pl.concat([hospital_beds_df, primary_care_df], how='diagonal')
    
    # Verify row count
    total_output = len(unified_df)
    if total_output != total_input:
        logger.warning(f"Row count mismatch: input={total_input}, output={total_output}")
    else:
        logger.success(f"Unified capacity data: {total_output} records from 2 tables")
    
    return unified_df


def convert_data_types(
    df: pl.DataFrame,
    type_mapping: Dict[str, pl.DataType]
) -> pl.DataFrame:
    """
    Convert DataFrame columns to specified data types.
    
    Uses non-strict casting by default to handle conversion failures gracefully.
    Logs any conversion warnings.
    
    Args:
        df: Input DataFrame
        type_mapping: Dictionary mapping column names to Polars data types
        
    Returns:
        DataFrame with converted data types
        
    Raises:
        ValueError: If required columns for type conversion are missing
        
    Example:
        >>> type_map = {'year': pl.Int32, 'sector': pl.Categorical}
        >>> df_typed = convert_data_types(df, type_map)
    """
    logger.info(f"Converting data types for {len(type_mapping)} columns")
    
    # Validate columns exist
    missing_cols = set(type_mapping.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Columns not found for type conversion: {missing_cols}")
    
    df_converted = df.clone()
    
    for col, target_dtype in type_mapping.items():
        try:
            original_dtype = df[col].dtype
            df_converted = df_converted.with_columns(
                pl.col(col).cast(target_dtype, strict=False).alias(col)
            )
            logger.debug(f"Converted '{col}': {original_dtype} → {target_dtype}")
        except Exception as e:
            logger.error(f"Failed to convert '{col}' to {target_dtype}: {e}")
            raise
    
    logger.success(f"Data type conversions complete")
    
    return df_converted


def standardize_sector_names(
    df: pl.DataFrame,
    sector_column: str,
    standardization_map: Dict[str, str]
) -> pl.DataFrame:
    """
    Standardize sector name variations to canonical values.
    
    Maps variations like 'Public Sector' → 'Public', 'Not in Active Practice' → 'Inactive'.
    Converts sector column to Categorical type.
    
    Args:
        df: Input DataFrame
        sector_column: Name of the sector column to standardize
        standardization_map: Dictionary mapping original values to standard values
        
    Returns:
        DataFrame with standardized sector names as Categorical
        
    Raises:
        ValueError: If sector column not found in DataFrame
        
    Example:
        >>> mapping = {'Public Sector': 'Public', 'Private Sector': 'Private'}
        >>> df_std = standardize_sector_names(df, 'sector', mapping)
    """
    logger.info(f"Standardizing sector names in column '{sector_column}'")
    
    if sector_column not in df.columns:
        raise ValueError(f"Sector column '{sector_column}' not found in DataFrame")
    
    # Log unique values before standardization
    unique_before = df[sector_column].unique().to_list()
    logger.debug(f"Unique sector values before standardization: {unique_before}")
    
    # Apply mapping
    df_standardized = df.with_columns(
        pl.col(sector_column).replace(standardization_map).alias(sector_column)
    )
    
    # Convert to Categorical
    df_standardized = df_standardized.with_columns(
        pl.col(sector_column).cast(pl.Categorical).alias(sector_column)
    )
    
    # Log unique values after standardization
    unique_after = df_standardized[sector_column].unique().to_list()
    logger.success(f"Standardized to {len(unique_after)} sector categories: {unique_after}")
    
    # Count standardizations
    changes = sum(1 for v in unique_before if v in standardization_map and standardization_map[v] != v)
    logger.info(f"Standardized {changes} sector name variations")
    
    return df_standardized


def analyze_missing_values(df: pl.DataFrame) -> Dict[str, Dict[str, any]]:
    """
    Analyze missing value patterns in DataFrame.
    
    Returns comprehensive statistics about null values for each column.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with column-level missing value statistics
        
    Example:
        >>> analysis = analyze_missing_values(df)
        >>> print(analysis['age']['null_count'])
    """
    logger.info("Analyzing missing value patterns")
    
    total_rows = len(df)
    analysis = {}
    
    for col in df.columns:
        null_count = df[col].null_count()
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0
        
        analysis[col] = {
            'null_count': null_count,
            'null_percentage': null_pct,
            'non_null_count': total_rows - null_count,
            'data_type': str(df[col].dtype)
        }
        
        if null_count > 0:
            logger.warning(f"Column '{col}': {null_count} nulls ({null_pct:.2f}%)")
        else:
            logger.debug(f"Column '{col}': No missing values")
    
    # Summary statistics
    total_nulls = sum(v['null_count'] for v in analysis.values())
    total_cells = total_rows * len(df.columns)
    overall_completeness = ((total_cells - total_nulls) / total_cells * 100) if total_cells > 0 else 0
    
    logger.info(f"Overall completeness: {overall_completeness:.2f}% ({total_cells - total_nulls}/{total_cells} cells)")
    
    return analysis


def handle_missing_values(
    df: pl.DataFrame,
    strategy: str = 'flag',
    drop_threshold: float = 50.0
) -> pl.DataFrame:
    """
    Handle missing values according to specified strategy.
    
    Strategies:
    - 'flag': Add has_missing_values boolean column (default)
    - 'drop_rows': Remove rows with any null values
    - 'drop_cols': Remove columns with >drop_threshold% nulls
    
    Args:
        df: Input DataFrame
        strategy: Handling strategy ('flag', 'drop_rows', 'drop_cols')
        drop_threshold: Percentage threshold for dropping columns
        
    Returns:
        DataFrame with missing values handled
        
    Raises:
        ValueError: If invalid strategy specified
    """
    logger.info(f"Handling missing values using strategy: {strategy}")
    
    if strategy not in ['flag', 'drop_rows', 'drop_cols']:
        raise ValueError(f"Invalid strategy '{strategy}'. Use: flag, drop_rows, or drop_cols")
    
    df_handled = df.clone()
    total_rows_before = len(df)
    total_cols_before = len(df.columns)
    
    if strategy == 'flag':
        # Add boolean column indicating if row has any missing values
        df_handled = df_handled.with_columns(
            pl.any_horizontal([pl.col(c).is_null() for c in df.columns]).alias('has_missing_values')
        )
        rows_with_nulls = df_handled['has_missing_values'].sum()
        logger.info(f"Flagged {rows_with_nulls} rows with missing values")
    
    elif strategy == 'drop_rows':
        # Drop rows with any null values
        df_handled = df_handled.drop_nulls()
        rows_dropped = total_rows_before - len(df_handled)
        drop_pct = (rows_dropped / total_rows_before * 100) if total_rows_before > 0 else 0
        logger.warning(f"Dropped {rows_dropped} rows ({drop_pct:.2f}%) with null values")
    
    elif strategy == 'drop_cols':
        # Drop columns with >threshold% null values
        cols_to_drop = []
        for col in df.columns:
            null_pct = (df[col].null_count() / total_rows_before * 100) if total_rows_before > 0 else 0
            if null_pct > drop_threshold:
                cols_to_drop.append(col)
                logger.warning(f"Dropping column '{col}' ({null_pct:.2f}% nulls > {drop_threshold}% threshold)")
        
        if cols_to_drop:
            df_handled = df_handled.drop(cols_to_drop)
            logger.warning(f"Dropped {len(cols_to_drop)} columns")
        else:
            logger.info(f"No columns exceed {drop_threshold}% null threshold")
    
    logger.success(f"Missing value handling complete: {len(df_handled)} rows, {len(df_handled.columns)} columns")
    
    return df_handled


def detect_duplicates(
    df: pl.DataFrame,
    subset: Optional[List[str]] = None,
    keep: str = 'first'
) -> Tuple[int, pl.DataFrame]:
    """
    Detect and remove exact duplicate records.
    
    Args:
        df: Input DataFrame
        subset: Columns to use for duplicate detection (None = all columns)
        keep: Which duplicates to keep ('first', 'last', or 'none')
        
    Returns:
        Tuple of (duplicate_count, deduplicated_dataframe)
        
    Example:
        >>> dup_count, df_clean = detect_duplicates(df, subset=['year', 'sector', 'profession'])
    """
    logger.info(f"Detecting duplicates (subset={subset}, keep={keep})")
    
    total_rows = len(df)
    
    # Detect duplicates
    if subset:
        df_deduped = df.unique(subset=subset, keep=keep)
    else:
        df_deduped = df.unique(keep=keep)
    
    duplicate_count = total_rows - len(df_deduped)
    dup_pct = (duplicate_count / total_rows * 100) if total_rows > 0 else 0
    
    if duplicate_count > 0:
        logger.warning(f"Found and removed {duplicate_count} duplicates ({dup_pct:.2f}%)")
    else:
        logger.success("No duplicate records found")
    
    return duplicate_count, df_deduped


def detect_and_flag_outliers(
    df: pl.DataFrame,
    numeric_columns: List[str],
    threshold: float = 3.0,
    method: str = 'zscore'
) -> pl.DataFrame:
    """
    Detect and flag outliers in numeric columns.
    
    Methods:
    - 'zscore': Values >threshold standard deviations from mean
    - 'iqr': Values beyond threshold * IQR from Q1/Q3
    
    Adds boolean columns: {col}_outlier for each numeric column, plus overall outlier_flag.
    
    Args:
        df: Input DataFrame
        numeric_columns: List of numeric column names to check
        threshold: Threshold value (stdev for zscore, IQR multiplier for iqr)
        method: Detection method ('zscore' or 'iqr')
        
    Returns:
        DataFrame with outlier flag columns added
        
    Raises:
        ValueError: If invalid method specified
        
    Example:
        >>> df_flagged = detect_and_flag_outliers(df, ['count'], threshold=3.0, method='zscore')
    """
    logger.info(f"Detecting outliers in {len(numeric_columns)} columns using {method} method (threshold={threshold})")
    
    if method not in ['zscore', 'iqr']:
        raise ValueError(f"Invalid method '{method}'. Use 'zscore' or 'iqr'")
    
    df_flagged = df.clone()
    
    for col in numeric_columns:
        if col not in df.columns:
            logger.warning(f"Column '{col}' not found, skipping outlier detection")
            continue
        
        if method == 'zscore':
            mean = df[col].mean()
            std = df[col].std()
            if std == 0:
                logger.warning(f"Column '{col}' has zero std dev, marking no outliers")
                outlier_condition = pl.lit(False)
            else:
                outlier_condition = (pl.col(col) - mean).abs() > threshold * std
        
        elif method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            if IQR == 0:
                logger.warning(f"Column '{col}' has zero IQR, marking no outliers")
                outlier_condition = pl.lit(False)
            else:
                outlier_condition = (pl.col(col) < Q1 - threshold * IQR) | (pl.col(col) > Q3 + threshold * IQR)
        
        df_flagged = df_flagged.with_columns(
            outlier_condition.alias(f'{col}_outlier')
        )
        
        outlier_count = df_flagged[f'{col}_outlier'].sum()
        outlier_pct = (outlier_count / len(df) * 100) if len(df) > 0 else 0
        
        if outlier_count > 0:
            logger.info(f"Column '{col}': {outlier_count} outliers ({outlier_pct:.1f}%)")
    
    # Add overall outlier flag (any column flagged)
    outlier_cols = [f'{col}_outlier' for col in numeric_columns if f'{col}_outlier' in df_flagged.columns]
    if outlier_cols:
        df_flagged = df_flagged.with_columns(
            pl.any_horizontal(outlier_cols).alias('outlier_flag')
        )
        
        total_outliers = df_flagged['outlier_flag'].sum()
        total_pct = (total_outliers / len(df) * 100) if len(df) > 0 else 0
        logger.info(f"Overall: {total_outliers} records flagged as outliers ({total_pct:.1f}%)")
    
    return df_flagged


def log_transformation_summary(
    df_before: pl.DataFrame,
    df_after: pl.DataFrame,
    operation: str
):
    """
    Log before/after statistics for a transformation operation.
    
    Args:
        df_before: DataFrame before transformation
        df_after: DataFrame after transformation
        operation: Description of the operation performed
    """
    rows_before = len(df_before)
    rows_after = len(df_after)
    cols_before = len(df_before.columns)
    cols_after = len(df_after.columns)
    
    logger.info(f"=== Transformation Summary: {operation} ===")
    logger.info(f"Rows: {rows_before} → {rows_after} (Δ {rows_after - rows_before})")
    logger.info(f"Columns: {cols_before} → {cols_after} (Δ {cols_after - cols_before})")
    
    # Null count changes
    nulls_before = sum([df_before[col].null_count() for col in df_before.columns])
    nulls_after = sum([df_after[col].null_count() for col in df_after.columns])
    logger.info(f"Total nulls: {nulls_before} → {nulls_after} (Δ {nulls_after - nulls_before})")
    
    logger.info("=" * 50)
