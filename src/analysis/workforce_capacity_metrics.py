"""
Workforce-Capacity Metrics Calculation Module

This module provides functions for calculating workforce-capacity alignment metrics,
detecting misalignments, and comparing Singapore healthcare metrics against international benchmarks.

Functions include:
- Workforce-to-bed ratio calculations
- Doctor-to-nurse ratio calculations
- Growth rate mismatch detection
- Benchmark comparisons
- Cumulative mismatch analysis

Author: Data Analytics Team
Date: 2026-02-23
"""

import polars as pl
import numpy as np
from typing import Dict, List, Tuple, Optional
from loguru import logger
from dataclasses import dataclass

from .benchmarks import (
    WORKFORCE_TO_BED_BENCHMARKS,
    DOCTOR_TO_NURSE_BENCHMARKS,
    MISMATCH_THRESHOLDS
)


@dataclass
class MismatchResult:
    """Container for mismatch detection results."""
    sector: str
    years_affected: List[int]
    avg_mismatch: float
    max_mismatch: float
    cumulative_mismatch: float
    severity: str  # 'Low', 'Medium', 'High'


def calculate_all_workforce_capacity_ratios(
    workforce_df: pl.DataFrame,
    capacity_df: pl.DataFrame,
    by_profession: bool = False
) -> pl.DataFrame:
    """
    Calculate comprehensive workforce-to-capacity ratios by sector and year.
    
    Merges workforce and capacity datasets on year and sector, then calculates:
    - FTE per bed ratio
    - Total workforce counts
    - Total bed counts
    - Optionally, profession-specific ratios
    
    Parameters
    ----------
    workforce_df : pl.DataFrame
        Workforce data with columns: year, sector, profession, count
    capacity_df : pl.DataFrame
        Capacity data with columns: year, sector, institution_type, num_beds
    by_profession : bool, default False
        If True, calculate ratios separately for each profession
        
    Returns
    -------
    pl.DataFrame
        DataFrame with columns:
        - year: Year of observation
        - sector: Sector (Public, Private, Inactive)
        - total_workforce: Total FTE workforce
        - total_beds: Total hospital beds
        - workforce_to_bed_ratio: FTE per bed
        - [profession columns if by_profession=True]
        
    Example
    -------
    >>> ratios = calculate_all_workforce_capacity_ratios(workforce_df, capacity_df)
    >>> ratios.filter(pl.col('sector') == 'Public').select(['year', 'workforce_to_bed_ratio'])
    """
    logger.info("Calculating workforce-to-capacity ratios")
    
    # Aggregate workforce by year and sector
    if by_profession:
        workforce_agg = (
            workforce_df
            .group_by(['year', 'sector', 'profession'])
            .agg([pl.col('count').sum().alias('workforce_count')])
        )
        # Pivot to get professions as columns
        workforce_agg = workforce_agg.pivot(
            index=['year', 'sector'],
            columns='profession',
            values='workforce_count'
        ).fill_null(0)
        
        # Calculate total
        profession_cols = [col for col in workforce_agg.columns if col not in ['year', 'sector']]
        workforce_agg = workforce_agg.with_columns([
            pl.sum_horizontal(profession_cols).alias('total_workforce')
        ])
    else:
        workforce_agg = (
            workforce_df
            .group_by(['year', 'sector'])
            .agg([pl.col('count').sum().alias('total_workforce')])
        )
    
    # Aggregate capacity (hospital beds only)
    capacity_agg = (
        capacity_df
        .filter(pl.col('institution_type') == 'Hospital')
        .group_by(['year', 'sector'])
        .agg([pl.col('num_beds').sum().alias('total_beds')])
    )
    
    # Join workforce and capacity
    ratios_df = workforce_agg.join(
        capacity_agg,
        on=['year', 'sector'],
        how='inner'
    )
    
    # Calculate workforce-to-bed ratio
    ratios_df = ratios_df.with_columns([
        (pl.col('total_workforce') / pl.col('total_beds')).alias('workforce_to_bed_ratio')
    ])
    
    logger.success(f"Calculated ratios for {len(ratios_df)} year-sector combinations")
    
    return ratios_df


def calculate_mismatch_index(
    workforce_df: pl.DataFrame,
    capacity_df: pl.DataFrame,
    by: List[str] = ['sector']
) -> pl.DataFrame:
    """
    Calculate Mismatch Index: growth rate differential between workforce and capacity.
    
    Mismatch Index = Workforce Growth Rate - Capacity Growth Rate
    
    Positive values indicate workforce growing faster than capacity.
    Negative values indicate capacity growing faster than workforce.
    
    Parameters
    ----------
    workforce_df : pl.DataFrame
        Workforce data with columns: year, sector, count
    capacity_df : pl.DataFrame
        Capacity data with columns: year, sector, institution_type, num_beds
    by : List[str], default ['sector']
        Group by columns for calculating growth rates
        
    Returns
    -------
    pl.DataFrame
        DataFrame with columns:
        - year: Year of observation
        - sector: Sector
        - total_workforce: Total FTE
        - total_beds: Total beds
        - workforce_growth_rate: Year-over-year workforce growth (%)
        - capacity_growth_rate: Year-over-year capacity growth (%)
        - mismatch_index: workforce_growth_rate - capacity_growth_rate (percentage points)
        
    Example
    -------
    >>> mismatch = calculate_mismatch_index(workforce_df, capacity_df)
    >>> mismatch.filter(pl.col('mismatch_index').abs() > 1.0)  # Significant mismatches
    """
    logger.info(f"Calculating mismatch index by {by}")
    
    # Aggregate workforce
    workforce_agg = (
        workforce_df
        .group_by(['year'] + by)
        .agg([pl.col('count').sum().alias('total_workforce')])
        .sort(['year'] + by)
    )
    
    # Aggregate capacity (hospital beds only)
    capacity_agg = (
        capacity_df
        .filter(pl.col('institution_type') == 'Hospital')
        .group_by(['year'] + by)
        .agg([pl.col('num_beds').sum().alias('total_beds')])
        .sort(['year'] + by)
    )
    
    # Calculate growth rates using window functions
    workforce_agg = workforce_agg.with_columns([
        pl.col('total_workforce').shift(1).over(by).alias('prev_workforce')
    ]).with_columns([
        ((pl.col('total_workforce') - pl.col('prev_workforce')) / pl.col('prev_workforce') * 100)
        .alias('workforce_growth_rate')
    ])
    
    capacity_agg = capacity_agg.with_columns([
        pl.col('total_beds').shift(1).over(by).alias('prev_beds')
    ]).with_columns([
        ((pl.col('total_beds') - pl.col('prev_beds')) / pl.col('prev_beds') * 100)
        .alias('capacity_growth_rate')
    ])
    
    # Join and calculate mismatch index
    mismatch_df = workforce_agg.join(
        capacity_agg.select(['year'] + by + ['total_beds', 'capacity_growth_rate']),
        on=['year'] + by,
        how='inner'
    )
    
    mismatch_df = mismatch_df.with_columns([
        (pl.col('workforce_growth_rate') - pl.col('capacity_growth_rate'))
        .alias('mismatch_index')
    ])
    
    # Drop temporary columns
    mismatch_df = mismatch_df.drop(['prev_workforce'])
    
    logger.success(f"Calculated mismatch index for {len(mismatch_df)} observations")
    
    # Log significant mismatches
    significant_count = len(mismatch_df.filter(pl.col('mismatch_index').abs() > MISMATCH_THRESHOLDS['significant_divergence']))
    if significant_count > 0:
        logger.warning(f"Found {significant_count} observations with significant mismatch (>±{MISMATCH_THRESHOLDS['significant_divergence']}%)")
    
    return mismatch_df


def detect_significant_misalignments(
    mismatch_df: pl.DataFrame,
    threshold: float = None,
    min_years: int = 3
) -> List[MismatchResult]:
    """
    Detect sectors with sustained workforce-capacity misalignments.
    
    Identifies sectors where the mismatch index exceeds the threshold
    for at least min_years consecutive years.
    
    Parameters
    ----------
    mismatch_df : pl.DataFrame
        Output from calculate_mismatch_index()
    threshold : float, optional
        Mismatch threshold in percentage points. If None, uses MISMATCH_THRESHOLDS['significant_divergence']
    min_years : int, default 3
        Minimum consecutive years of sustained mismatch to flag
        
    Returns
    -------
    List[MismatchResult]
        List of misalignment results for sectors exceeding threshold
        
    Example
    -------
    >>> misalignments = detect_significant_misalignments(mismatch_df, threshold=1.0, min_years=3)
    >>> for result in misalignments:
    ...     print(f"{result.sector}: {result.severity} severity, {len(result.years_affected)} years affected")
    """
    if threshold is None:
        threshold = MISMATCH_THRESHOLDS['significant_divergence']
    
    logger.info(f"Detecting significant misalignments (threshold=±{threshold}%, min_years={min_years})")
    
    results = []
    
    # Filter to non-null mismatch values
    mismatch_df = mismatch_df.filter(pl.col('mismatch_index').is_not_null())
    
    sectors = mismatch_df['sector'].unique().to_list()
    
    for sector in sectors:
        sector_data = (
            mismatch_df
            .filter(pl.col('sector') == sector)
            .sort('year')
        )
        
        # Identify years exceeding threshold
        years_exceeded = (
            sector_data
            .filter(pl.col('mismatch_index').abs() > threshold)
            ['year'].to_list()
        )
        
        if len(years_exceeded) >= min_years:
            # Calculate statistics
            mismatch_values = (
                sector_data
                .filter(pl.col('year').is_in(years_exceeded))
                ['mismatch_index'].to_list()
            )
            
            avg_mismatch = np.mean(mismatch_values)
            max_mismatch = max(mismatch_values, key=abs)
            
            # Calculate cumulative mismatch
            cumulative_mismatch = sector_data['mismatch_index'].sum()
            
            # Determine severity
            if abs(avg_mismatch) > MISMATCH_THRESHOLDS['severe_divergence']:
                severity = 'High'
            elif abs(avg_mismatch) > MISMATCH_THRESHOLDS['significant_divergence']:
                severity = 'Medium'
            else:
                severity = 'Low'
            
            result = MismatchResult(
                sector=sector,
                years_affected=years_exceeded,
                avg_mismatch=avg_mismatch,
                max_mismatch=max_mismatch,
                cumulative_mismatch=cumulative_mismatch,
                severity=severity
            )
            
            results.append(result)
            logger.warning(f"Sector '{sector}': {severity} severity mismatch detected ({len(years_exceeded)} years)")
    
    if not results:
        logger.info("No significant sustained misalignments detected")
    else:
        logger.success(f"Detected {len(results)} sector(s) with significant misalignments")
    
    return results


def compare_to_benchmarks(
    ratios_df: pl.DataFrame,
    benchmark_type: str = 'workforce_to_bed',
    ratio_col: str = 'workforce_to_bed_ratio'
) -> pl.DataFrame:
    """
    Compare calculated ratios to international benchmarks.
    
    Adds columns indicating whether ratios fall within benchmark ranges
    and calculates distance from benchmark midpoints.
    
    Parameters
    ----------
    ratios_df : pl.DataFrame
        DataFrame with calculated ratios
    benchmark_type : str, default 'workforce_to_bed'
        Type of benchmark to use ('workforce_to_bed', 'doctor_to_nurse')
    ratio_col : str, default 'workforce_to_bed_ratio'
        Column name containing the ratio values to compare
        
    Returns
    -------
    pl.DataFrame
        Original DataFrame with added columns:
        - within_benchmark: Boolean indicating if ratio is within typical range
        - deviation_from_midpoint: Distance from benchmark midpoint
        - benchmark_status: 'Within Range', 'Below Range', or 'Above Range'
        
    Example
    -------
    >>> ratios_with_benchmark = compare_to_benchmarks(ratios_df)
    >>> ratios_with_benchmark.filter(~pl.col('within_benchmark'))  # Outside benchmark
    """
    logger.info(f"Comparing {ratio_col} to {benchmark_type} benchmarks")
    
    # Get appropriate benchmarks
    if benchmark_type == 'workforce_to_bed':
        benchmarks = WORKFORCE_TO_BED_BENCHMARKS
        min_val = benchmarks['typical_min']
        max_val = benchmarks['typical_max']
    elif benchmark_type == 'doctor_to_nurse':
        benchmarks = DOCTOR_TO_NURSE_BENCHMARKS
        min_val = benchmarks['typical_min']
        max_val = benchmarks['typical_max']
    else:
        raise ValueError(f"Unknown benchmark_type: {benchmark_type}")
    
    midpoint = (min_val + max_val) / 2
    
    # Add benchmark comparison columns
    result = ratios_df.with_columns([
        (
            (pl.col(ratio_col) >= min_val) & (pl.col(ratio_col) <= max_val)
        ).alias('within_benchmark'),
        (pl.col(ratio_col) - midpoint).alias('deviation_from_midpoint'),
        pl.when(pl.col(ratio_col) < min_val)
        .then(pl.lit('Below Range'))
        .when(pl.col(ratio_col) > max_val)
        .then(pl.lit('Above Range'))
        .otherwise(pl.lit('Within Range'))
        .alias('benchmark_status')
    ])
    
    # Log summary statistics
    within_count = len(result.filter(pl.col('within_benchmark')))
    total_count = len(result)
    within_pct = (within_count / total_count * 100) if total_count > 0 else 0
    
    logger.info(f"Benchmark range: {min_val} - {max_val}")
    logger.info(f"Within benchmark: {within_count}/{total_count} ({within_pct:.1f}%)")
    
    return result


def calculate_doctor_to_nurse_ratio(
    workforce_df: pl.DataFrame,
    by: List[str] = ['year', 'sector']
) -> pl.DataFrame:
    """
    Calculate doctor-to-nurse ratios by specified grouping variables.
    
    Ratio = Number of Doctors / Number of Nurses
    
    Typical range: 0.25 - 0.50 (1 doctor per 2-4 nurses)
    
    Parameters
    ----------
    workforce_df : pl.DataFrame
        Workforce data with columns: year, sector, profession, count
    by : List[str], default ['year', 'sector']
        Grouping columns for ratio calculation
        
    Returns
    -------
    pl.DataFrame
        DataFrame with columns:
        - [by columns]: Grouping variables
        - doctors: Number of doctors
        - nurses: Number of nurses
        - doctor_to_nurse_ratio: Doctors / Nurses
        - within_benchmark: Boolean indicating if ratio is within typical range
        
    Example
    -------
    >>> dn_ratios = calculate_doctor_to_nurse_ratio(workforce_df)
    >>> dn_ratios.filter(pl.col('sector') == 'Public').select(['year', 'doctor_to_nurse_ratio'])
    """
    logger.info(f"Calculating doctor-to-nurse ratios by {by}")
    
    # Filter to doctors and nurses only
    doctors = (
        workforce_df
        .filter(pl.col('profession') == 'Doctor')
        .group_by(by)
        .agg([pl.col('count').sum().alias('doctors')])
    )
    
    nurses = (
        workforce_df
        .filter(pl.col('profession') == 'Nurse')
        .group_by(by)
        .agg([pl.col('count').sum().alias('nurses')])
    )
    
    # Join and calculate ratio
    ratio_df = doctors.join(nurses, on=by, how='inner')
    
    ratio_df = ratio_df.with_columns([
        (pl.col('doctors') / pl.col('nurses')).alias('doctor_to_nurse_ratio')
    ])
    
    # Add benchmark comparison
    ratio_df = ratio_df.with_columns([
        (
            (pl.col('doctor_to_nurse_ratio') >= DOCTOR_TO_NURSE_BENCHMARKS['typical_min']) &
            (pl.col('doctor_to_nurse_ratio') <= DOCTOR_TO_NURSE_BENCHMARKS['typical_max'])
        ).alias('within_benchmark')
    ])
    
    logger.success(f"Calculated doctor-to-nurse ratios for {len(ratio_df)} observations")
    
    # Log summary
    within_count = len(ratio_df.filter(pl.col('within_benchmark')))
    within_pct = (within_count / len(ratio_df) * 100) if len(ratio_df) > 0 else 0
    logger.info(f"Within benchmark range: {within_count}/{len(ratio_df)} ({within_pct:.1f}%)")
    
    return ratio_df


def calculate_cumulative_mismatch(
    mismatch_df: pl.DataFrame,
    start_year: int = 2009,
    end_year: int = 2019,
    by: List[str] = ['sector']
) -> pl.DataFrame:
    """
    Calculate cumulative mismatch over a multi-year period.
    
    Cumulative Mismatch = Sum of annual mismatch indices over the period
    
    A large positive cumulative mismatch indicates workforce has grown substantially
    faster than capacity over time. A large negative value indicates the opposite.
    
    Parameters
    ----------
    mismatch_df : pl.DataFrame
        Output from calculate_mismatch_index()
    start_year : int, default 2009
        Start year for cumulative calculation
    end_year : int, default 2019
        End year for cumulative calculation
    by : List[str], default ['sector']
        Grouping columns
        
    Returns
    -------
    pl.DataFrame
        DataFrame with columns:
        - [by columns]: Grouping variables
        - cumulative_mismatch: Sum of mismatch indices
        - years_analyzed: Number of years included
        - avg_annual_mismatch: Average mismatch per year
        
    Example
    -------
    >>> cumulative = calculate_cumulative_mismatch(mismatch_df, start_year=2009, end_year=2019)
    >>> cumulative.sort('cumulative_mismatch', descending=True)  # Most overextended workforce
    """
    logger.info(f"Calculating cumulative mismatch ({start_year}-{end_year}) by {by}")
    
    # Filter to specified year range and non-null values
    filtered = mismatch_df.filter(
        (pl.col('year') >= start_year) &
        (pl.col('year') <= end_year) &
        pl.col('mismatch_index').is_not_null()
    )
    
    # Calculate cumulative statistics
    cumulative_df = (
        filtered
        .group_by(by)
        .agg([
            pl.col('mismatch_index').sum().alias('cumulative_mismatch'),
            pl.col('year').count().alias('years_analyzed'),
            pl.col('mismatch_index').mean().alias('avg_annual_mismatch')
        ])
    )
    
    logger.success(f"Calculated cumulative mismatch for {len(cumulative_df)} groups")
    
    return cumulative_df
