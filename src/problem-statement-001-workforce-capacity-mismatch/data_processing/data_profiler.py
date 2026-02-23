"""Data quality profiling module for healthcare workforce and capacity data.

This module provides comprehensive data profiling utilities including null analysis,
duplicate detection, outlier identification, and quality report generation.
"""

import polars as pl
from pathlib import Path
from loguru import logger
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


def profile_dataframe(df: pl.DataFrame, table_name: str) -> Dict[str, Any]:
    """
    Generate comprehensive data quality profile for a DataFrame.
    
    Args:
        df: Polars DataFrame to profile
        table_name: Name of the table for reporting
        
    Returns:
        Dictionary containing profile metrics:
        - row_count: Total number of rows
        - column_count: Total number of columns
        - columns: List of column names
        - dtypes: Data types for each column
        - null_counts: Null counts per column
        - null_percentages: Null percentage per column
        - numeric_summary: Summary statistics for numeric columns
        - unique_counts: Unique value counts per column
    """
    profile = {
        'table_name': table_name,
        'row_count': df.shape[0],
        'column_count': df.shape[1],
        'columns': df.columns,
        'dtypes': {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    }
    
    # Null analysis
    null_counts = df.null_count()
    profile['null_counts'] = {col: null_counts[col][0] for col in df.columns}
    profile['null_percentages'] = {
        col: (null_counts[col][0] / df.shape[0] * 100) if df.shape[0] > 0 else 0
        for col in df.columns
    }
    
    # Numeric summary statistics
    numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]]
    if numeric_cols:
        profile['numeric_summary'] = df.select(numeric_cols).describe().to_dicts()
    else:
        profile['numeric_summary'] = []
    
    # Unique value counts
    profile['unique_counts'] = {col: df[col].n_unique() for col in df.columns}
    
    logger.info(f"Profiled {table_name}: {profile['row_count']} rows, {profile['column_count']} columns")
    
    return profile


def detect_duplicates(df: pl.DataFrame, subset: Optional[List[str]] = None) -> Tuple[int, pl.DataFrame]:
    """
    Detect duplicate records in DataFrame.
    
    Args:
        df: Polars DataFrame to check
        subset: List of columns to check for duplicates (None = all columns)
        
    Returns:
        Tuple of (duplicate_count, duplicate_rows)
    """
    if subset is None:
        subset = df.columns
    
    duplicates = df.filter(pl.struct(subset).is_duplicated())
    duplicate_count = duplicates.shape[0]
    
    logger.info(f"Found {duplicate_count} duplicate records")
    
    return duplicate_count, duplicates


def identify_outliers(
    df: pl.DataFrame,
    column: str,
    threshold: float = 3.0
) -> Tuple[pl.DataFrame, Dict[str, float]]:
    """
    Identify outliers using z-score method (±threshold standard deviations).
    
    Args:
        df: Polars DataFrame containing data
        column: Column name to check for outliers
        threshold: Number of standard deviations for outlier threshold (default: 3.0)
        
    Returns:
        Tuple of (outlier_rows, statistics_dict)
        statistics_dict contains: mean, std, min, max, outlier_count
        
    Raises:
        ValueError: If column is not numeric
    """
    if df[column].dtype not in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
        raise ValueError(f"Column {column} must be numeric for outlier detection")
    
    mean = df[column].mean()
    std = df[column].std()
    
    if std == 0 or std is None:
        logger.warning(f"Column {column} has zero standard deviation, no outliers detected")
        return pl.DataFrame(), {'mean': mean, 'std': 0, 'outlier_count': 0}
    
    # Calculate z-scores and identify outliers
    outliers = df.filter(
        ((pl.col(column) - mean) / std).abs() > threshold
    )
    
    stats = {
        'mean': mean,
        'std': std,
        'min': df[column].min(),
        'max': df[column].max(),
        'outlier_count': outliers.shape[0]
    }
    
    logger.info(f"Found {stats['outlier_count']} outliers in {column} (threshold: ±{threshold} std)")
    
    return outliers, stats


def generate_quality_report(
    profiles: Dict[str, Dict],
    output_path: Path
) -> None:
    """
    Generate markdown data quality report from table profiles.
    
    Args:
        profiles: Dictionary mapping table names to profile dictionaries
        output_path: Path to save markdown report
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report_lines = [
        "# Data Quality Assessment Report",
        f"\n**Generated:** {timestamp}",
        f"\n**Tables Analyzed:** {len(profiles)}",
        "\n---\n"
    ]
    
    # Summary table
    report_lines.append("## Summary\n")
    report_lines.append("| Table | Rows | Columns | Null % (Max) | Completeness |")
    report_lines.append("|-------|------|---------|--------------|--------------|")
    
    for table_name, profile in profiles.items():
        max_null_pct = max(profile['null_percentages'].values()) if profile['null_percentages'] else 0
        completeness = 100 - max_null_pct
        report_lines.append(
            f"| {table_name} | {profile['row_count']} | {profile['column_count']} | "
            f"{max_null_pct:.2f}% | {completeness:.2f}% |"
        )
    
    # Detailed profiles
    report_lines.append("\n---\n## Detailed Profiles\n")
    
    for table_name, profile in profiles.items():
        report_lines.append(f"\n### {table_name}\n")
        report_lines.append(f"**Rows:** {profile['row_count']}  ")
        report_lines.append(f"**Columns:** {profile['column_count']}\n")
        
        # Column details
        report_lines.append("\n**Column Details:**\n")
        report_lines.append("| Column | Type | Nulls | Null % | Unique Values |")
        report_lines.append("|--------|------|-------|--------|---------------|")
        
        for col in profile['columns']:
            null_count = profile['null_counts'][col]
            null_pct = profile['null_percentages'][col]
            unique_count = profile['unique_counts'][col]
            dtype = profile['dtypes'][col]
            
            report_lines.append(
                f"| {col} | {dtype} | {null_count} | {null_pct:.2f}% | {unique_count} |"
            )
        
        report_lines.append("")
    
    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    logger.info(f"Data quality report saved to: {output_path}")
