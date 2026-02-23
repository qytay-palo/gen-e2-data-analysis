"""Statistical analysis functions for workforce and capacity data.

This module provides functions for calculating growth rates, composition metrics,
ratios, and performing statistical hypothesis tests on healthcare workforce and
capacity data.

Author: Generated from User Story 3 Implementation Plan
Date: 2026-02-23
"""

import polars as pl
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Any
from loguru import logger


def calculate_growth_rates(
    df: pl.DataFrame,
    group_cols: List[str],
    value_col: str = 'count',
    time_col: str = 'year'
) -> pl.DataFrame:
    """
    Calculate year-over-year growth rates for grouped data.
    
    Args:
        df: Input DataFrame with time series data
        group_cols: Columns to group by (e.g., ['sector', 'profession'])
        value_col: Column containing values to calculate growth on
        time_col: Column containing time dimension (year)
        
    Returns:
        DataFrame with original columns plus 'growth_rate' column (percentage)
        
    Raises:
        ValueError: If required columns not in DataFrame
        
    Example:
        >>> growth_df = calculate_growth_rates(
        ...     workforce_df,
        ...     group_cols=['sector', 'profession']
        ... )
        >>> growth_df.filter(pl.col('sector') == 'Public').head()
    """
    # Validate required columns
    required_cols = set(group_cols + [value_col, time_col])
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info(f"Calculating growth rates grouped by {group_cols}")
    
    # Sort by group and time
    df_sorted = df.sort(group_cols + [time_col])
    
    # Calculate growth rate using shift within groups
    result = (
        df_sorted
        .with_columns([
            pl.col(value_col).shift(1).over(group_cols).alias('prev_value')
        ])
        .with_columns([
            ((pl.col(value_col) - pl.col('prev_value')) / pl.col('prev_value') * 100.0)
            .alias('growth_rate')
        ])
        .drop('prev_value')
    )
    
    logger.success(f"Growth rates calculated for {result.height} rows")
    return result


def calculate_indexed_growth(
    df: pl.DataFrame,
    group_cols: List[str],
    value_col: str = 'count',
    time_col: str = 'year',
    base_year: int = 2006
) -> pl.DataFrame:
    """
    Calculate growth indexed to a baseline year (base_year = 100).
    
    Args:
        df: Input DataFrame with time series data
        group_cols: Columns to group by
        value_col: Column containing values to index
        time_col: Column containing year
        base_year: Year to use as baseline (index = 100)
        
    Returns:
        DataFrame with original columns plus 'indexed_value' column
        
    Raises:
        ValueError: If base_year not in data
        
    Example:
        >>> indexed_df = calculate_indexed_growth(
        ...     workforce_df,
        ...     group_cols=['sector'],
        ...     base_year=2006
        ... )
    """
    if base_year not in df[time_col].unique().to_list():
        raise ValueError(f"Base year {base_year} not found in data")
    
    logger.info(f"Calculating indexed growth (base year: {base_year})")
    
    # Get baseline values
    baseline = (
        df
        .filter(pl.col(time_col) == base_year)
        .select(group_cols + [pl.col(value_col).alias('base_value')])
    )
    
    # Join and calculate index
    result = (
        df
        .join(baseline, on=group_cols, how='left')
        .with_columns([
            (pl.col(value_col) / pl.col('base_value') * 100.0).alias('indexed_value')
        ])
        .drop('base_value')
    )
    
    logger.success(f"Indexed values calculated for {result.height} rows")
    return result


def calculate_composition_metrics(
    df: pl.DataFrame,
    group_cols: List[str],
    category_col: str,
    value_col: str = 'count'
) -> pl.DataFrame:
    """
    Calculate percentage composition by category within groups.
    
    Args:
        df: Input DataFrame
        group_cols: Columns defining groups (e.g., ['year', 'sector'])
        category_col: Column containing categories (e.g., 'profession')
        value_col: Column containing counts
        
    Returns:
        DataFrame with composition percentages
        
    Example:
        >>> composition = calculate_composition_metrics(
        ...     workforce_df,
        ...     group_cols=['year', 'sector'],
        ...     category_col='profession'
        ... )
    """
    logger.info(f"Calculating composition by {category_col} within {group_cols}")
    
    # Calculate total by group
    result = (
        df
        .with_columns([
            pl.col(value_col).sum().over(group_cols).alias('total')
        ])
        .with_columns([
            (pl.col(value_col) / pl.col('total') * 100.0).alias('percentage')
        ])
    )
    
    logger.success(f"Composition calculated for {result.height} rows")
    return result


def calculate_workforce_to_bed_ratio(
    workforce_df: pl.DataFrame,
    capacity_df: pl.DataFrame,
    by: List[str] = ['year', 'sector']
) -> pl.DataFrame:
    """
    Calculate workforce-to-bed ratio by joining workforce and capacity data.
    
    SCHEMA CORRECTION APPLIED: Uses institution_type and num_beds instead of
    category and count for capacity data.
    
    Args:
        workforce_df: DataFrame with workforce counts
        capacity_df: DataFrame with bed counts (must have institution_type, num_beds columns)
        by: Columns to join on (e.g., ['year', 'sector'])
        
    Returns:
        DataFrame with workforce_total, beds_total, and ratio columns
        
    Raises:
        ValueError: If join columns missing or no matching records
        
    Example:
        >>> ratio_df = calculate_workforce_to_bed_ratio(
        ...     workforce_df,
        ...     capacity_df,
        ...     by=['year', 'sector']
        ... )
    """
    logger.info(f"Calculating workforce-to-bed ratio joined on {by}")
    
    # Aggregate workforce by join columns
    workforce_agg = (
        workforce_df
        .group_by(by)
        .agg([
            pl.col('count').sum().alias('total_workforce')
        ])
    )
    
    # Aggregate capacity by join columns (filter to hospitals only)
    # SCHEMA CORRECTION: Use institution_type == 'Hospital' and num_beds
    capacity_agg = (
        capacity_df
        .filter(pl.col('institution_type') == 'Hospital')
        .group_by(by)
        .agg([
            pl.col('num_beds').sum().alias('total_beds')
        ])
    )
    
    # Join and calculate ratio
    result = (
        workforce_agg
        .join(capacity_agg, on=by, how='inner')
        .with_columns([
            (pl.col('total_workforce') / pl.col('total_beds')).alias('workforce_to_bed_ratio')
        ])
    )
    
    if result.height == 0:
        raise ValueError("No matching records found between workforce and capacity data")
    
    logger.success(f"Workforce-to-bed ratio calculated for {result.height} rows")
    return result


def test_sector_growth_differences(
    growth_df: pl.DataFrame,
    sector_col: str = 'sector',
    growth_col: str = 'growth_rate',
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Test if growth rates differ significantly across sectors using ANOVA or Kruskal-Wallis.
    
    Args:
        growth_df: DataFrame with growth rates by sector
        sector_col: Column containing sector categories
        growth_col: Column containing growth rate values
        alpha: Significance level for hypothesis test
        
    Returns:
        Dictionary with test results:
            - 'test_used': 'ANOVA' or 'Kruskal-Wallis'
            - 'statistic': Test statistic value
            - 'p_value': P-value
            - 'significant': Boolean (True if p < alpha)
            - 'conclusion': Interpretation string
            
    Example:
        >>> test_result = test_sector_growth_differences(growth_df)
        >>> print(test_result['conclusion'])
    """
    logger.info(f"Testing growth rate differences across {sector_col}")
    
    # Drop null growth rates (first year has no prior year)
    growth_clean = growth_df.filter(pl.col(growth_col).is_not_null())
    
    # Group data by sector
    sectors = growth_clean[sector_col].unique().to_list()
    sector_groups = [
        growth_clean.filter(pl.col(sector_col) == sector)[growth_col].to_numpy()
        for sector in sectors
    ]
    
    # Check normality assumption (Shapiro-Wilk test)
    normality_pvalues = [stats.shapiro(group)[1] for group in sector_groups if len(group) > 3]
    all_normal = all(p > alpha for p in normality_pvalues)
    
    # Choose appropriate test
    if all_normal and len(sectors) >= 2:
        # Use ANOVA (parametric)
        statistic, p_value = stats.f_oneway(*sector_groups)
        test_used = 'ANOVA'
        logger.info(f"Using ANOVA (data approximately normal)")
    else:
        # Use Kruskal-Wallis (non-parametric)
        statistic, p_value = stats.kruskal(*sector_groups)
        test_used = 'Kruskal-Wallis'
        logger.info(f"Using Kruskal-Wallis (data not normal or small sample)")
    
    # Interpret result
    significant = p_value < alpha
    if significant:
        conclusion = f"Growth rates differ significantly across sectors (p={p_value:.4f} < {alpha})"
    else:
        conclusion = f"No significant difference in growth rates across sectors (p={p_value:.4f} >= {alpha})"
    
    result = {
        'test_used': test_used,
        'statistic': statistic,
        'p_value': p_value,
        'significant': significant,
        'conclusion': conclusion,
        'sectors_compared': sectors,
        'sample_sizes': [len(g) for g in sector_groups]
    }
    
    logger.success(f"Hypothesis test complete: {conclusion}")
    return result


def test_workforce_capacity_correlation(
    ratio_df: pl.DataFrame,
    workforce_col: str = 'total_workforce',
    capacity_col: str = 'total_beds',
    method: str = 'pearson',
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Test correlation between workforce and capacity growth.
    
    Args:
        ratio_df: DataFrame with workforce and capacity values
        workforce_col: Column containing workforce values
        capacity_col: Column containing capacity values
        method: 'pearson' or 'spearman'
        alpha: Significance level
        
    Returns:
        Dictionary with correlation test results
        
    Example:
        >>> corr_result = test_workforce_capacity_correlation(ratio_df)
        >>> print(f"Correlation: {corr_result['correlation']:.3f}")
    """
    logger.info(f"Testing {method} correlation between {workforce_col} and {capacity_col}")
    
    # Extract values as numpy arrays
    workforce_values = ratio_df[workforce_col].to_numpy()
    capacity_values = ratio_df[capacity_col].to_numpy()
    
    # Calculate correlation
    if method == 'pearson':
        correlation, p_value = stats.pearsonr(workforce_values, capacity_values)
    elif method == 'spearman':
        correlation, p_value = stats.spearmanr(workforce_values, capacity_values)
    else:
        raise ValueError(f"Unknown correlation method: {method}")
    
    # Interpret strength
    abs_corr = abs(correlation)
    if abs_corr >= 0.7:
        strength = 'strong'
    elif abs_corr >= 0.4:
        strength = 'moderate'
    else:
        strength = 'weak'
    
    direction = 'positive' if correlation > 0 else 'negative'
    significant = p_value < alpha
    
    conclusion = (
        f"{strength.capitalize()} {direction} correlation "
        f"(r={correlation:.3f}, p={p_value:.4f})"
    )
    
    if significant:
        conclusion += f" - statistically significant at α={alpha}"
    else:
        conclusion += f" - not statistically significant at α={alpha}"
    
    result = {
        'method': method,
        'correlation': correlation,
        'p_value': p_value,
        'significant': significant,
        'strength': strength,
        'direction': direction,
        'conclusion': conclusion,
        'sample_size': len(workforce_values)
    }
    
    logger.success(f"Correlation test complete: {conclusion}")
    return result
