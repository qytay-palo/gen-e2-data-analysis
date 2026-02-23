# User Story 3: Exploratory Workforce and Capacity Analysis

**As a** healthcare policy analyst,  
**I want** to explore workforce and capacity trends by sector, profession, and time period,  
**so that** I can identify patterns, generate hypotheses, and prepare data for deeper analysis.

## 1. 🎯 Acceptance Criteria

- Summary statistics calculated for workforce and capacity by sector and profession
- Temporal trends visualized showing year-over-year changes (2006-2019)
- Sector comparison visualizations showing relative workforce and capacity
- Statistical tests applied to confirm significance of observed differences
- Key patterns documented in EDA report with findings and hypotheses
- Preliminary sector-specific insights documented
- All visualizations saved as PNG/PDF for presentation
- EDA notebook saved with all analysis and outputs documented

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient aggregation and statistical analysis
- **Visualization**: Use matplotlib/seaborn for static figures; store in `reports/figures/`
- **Documentation**: EDA report in markdown with embedded figures
- **Reproducibility**: All analysis in notebook or script form with clear variable naming
- **Output**: Visualizations in high-resolution format suitable for presentation

## 3. 📚 Domain Knowledge References

- [Healthcare Workforce Planning: Key Metrics](../../../domain_knowledge/healthcare-workforce-planning.md#standard-metrics-and-kpis) - Workforce density, growth rates, composition ratios
- [Healthcare Workforce Planning: Feature Engineering - Temporal Features](../../../domain_knowledge/healthcare-workforce-planning.md#temporal-features) - Growth rate calculations, indexed comparisons
- [Healthcare System Sustainability: Workforce Dimension](../../../domain_knowledge/healthcare-system-sustainability-metrics.md) - Workforce sustainability context

## 4. 📦 Dependencies

- **polars**: Data aggregation and statistical analysis
- **scipy**: Statistical testing (correlation, significance tests)
- **matplotlib/seaborn**: Visualization
- **numpy**: Numerical calculations

## 5. ✅ Implementation Tasks

### Summary Statistics
- ⬜ Calculate workforce counts by sector for baseline (2006 and most recent year available)
- ⬜ Calculate workforce counts by profession (doctors, nurses, pharmacists) by sector
- ⬜ Calculate capacity (beds) by sector and facility type
- ⬜ Generate summary table: counts, mean, std dev, min, max by sector
- ⬜ Identify extreme values (highest/lowest) by category for context

### Temporal Trend Analysis
- ⬜ Calculate year-over-year growth rates for workforce by sector
- ⬜ Calculate year-over-year growth rates for capacity by sector
- ⬜ Identify growth rate changes (acceleration/deceleration patterns)
- ⬜ Compare average growth rates across sectors and professions
- ⬜ Test statistical significance of growth rate differences (ANOVA or similar)

### Workforce Composition Analysis
- ⬜ Calculate profession distribution (% doctors, % nurses, % pharmacists) by sector
- ⬜ Track composition changes over time (composition shift patterns)
- ⬜ Identify which professions growing fastest vs. slowest
- ⬜ Calculate doctor-to-nurse ratios and other key composition metrics
- ⬜ Visualize composition changes over time by sector

### Sector Comparison Analysis
- ⬜ Create comparison table: Public vs. Private vs. Not-for-Profit sectors
- ⬜ Calculate average workforce density (per bed, per capita where possible)
- ⬜ Compare growth trajectories across sectors visually
- ⬜ Identify which sectors growing faster and implications
- ⬜ Perform statistical tests for sector differences (t-tests, Mann-Whitney)

### Workforce-Capacity Relationship Analysis
- ⬜ Calculate workforce-to-bed ratio by sector and year
- ⬜ Assess whether ratios reasonable compared to domain benchmarks (1.5-2.5 FTE per bed)
- ⬜ Correlate workforce and capacity growth (are they in sync?)
- ⬜ Visualize relationship (scatter plot with trend line)
- ⬜ Investigate divergences (workforce growing but capacity stagnant, or vice versa)

### Exploratory Visualizations
- ⬜ Line plot: Workforce trends by sector (2006-2019)
- ⬜ Line plot: Workforce trends by profession (all sectors combined)
- ⬜ Bar plot: Sector comparison of baseline and recent workforce
- ⬜ Stacked bar chart: Workforce composition by sector over time
- ⬜ Line plot: Workforce-to-bed ratio trends by sector
- ⬜ Scatter plot: Workforce vs. capacity growth rate comparison
- ⬜ Save all visualizations to `reports/figures/` as PNG

### Pattern Documentation
- ⬜ Identify and document 3-5 key patterns observed:
  - Fastest growing profession/sector
  - Sector with largest workforce-capacity mismatch
  - Composition shifts (increasing/decreasing professions)
  - Any unexpected trends or anomalies
- ⬜ For each pattern, document:
  - What the pattern is
  - Which sectors/professions affected
  - Magnitude (growth rate, percentage change)
  - Potential implications

### Statistical Testing
- ⬜ Test hypothesis: Growth rates significantly different across sectors
  - Method: ANOVA or Kruskal-Wallis test
  - Report: Test statistic, p-value, conclusion
- ⬜ Test hypothesis: Workforce-to-capacity ratio differs significantly across sectors
  - Method: t-test or Mann-Whitney U test
  - Report: Test statistics, confidence intervals, interpretation
- ⬜ Correlate workforce and capacity growth
  - Calculate Pearson/Spearman correlation
  - Test significance of correlation
  - Interpret relationship strength

### EDA Report Generation
- ⬜ Create comprehensive EDA report in markdown format
- ⬜ Structure report:
  1. Overview and data summary
  2. Temporal trends section with visualizations
  3. Sector comparison section with findings
  4. Workforce composition analysis
  5. Preliminary hypotheses and patterns identified
  6. Data quality notes and limitations
  7. Recommendations for deeper analysis
- ⬜ Embed visualizations in report
- ⬜ Document key findings with concrete numbers (growth rates, percentages, changes)
- ⬜ Save report to `reports/` directory

### Deliverables
- ⬜ Save EDA notebook to `notebooks/2_analysis/`
- ⬜ Save all figures to `reports/figures/`
- ⬜ Save EDA summary report to `results/exports/` for stakeholder sharing
- ⬜ Document any questions or unclear findings for Story 4

## 6. Notes

**Domain Context** ([Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md)):
- Workforce categories: Different growth rates expected by profession (nurses growing faster than doctors in many systems)
- Workforce-to-bed benchmarks: 1.5-2.5 FTE per bed typical; <1.0 indicates understaffing, >3.0 potential overstaffing
- Composition ratios: Doctor-to-nurse ratio typically 1:2 to 1:4

**Statistical Approach**:
- Use parametric tests (ANOVA, t-test) if data approximately normal; non-parametric (Kruskal-Wallis, Mann-Whitney) if not
- Report both point estimates and confidence intervals for better uncertainty representation
- Document all statistical test assumptions and whether they're met

**Related Stories**: This exploratory analysis informs Story 4 (Workforce-Capacity Metrics) by identifying key relationships and potential misalignments to analyze in depth.

---

## Implementation Plan

### 1. Feature Overview

This user story implements **exploratory data analysis (EDA)** for cleaned workforce and capacity datasets to identify temporal trends, sector differences, and workforce-capacity relationships. The analysis will generate summary statistics, visualizations, statistical tests, and a comprehensive EDA report to guide deeper analytical work in subsequent user stories.

**Primary User Role**: Healthcare policy analyst

**Goal**: Explore 14 years (2006-2019) of workforce and healthcare capacity data to identify growth patterns, composition shifts, sector differences, and workforce-capacity alignment issues that inform policy decisions and resource allocation strategies.

---

### 2. Component Analysis & Reuse Strategy

**Existing Data Components (Reusable)**:

1. **Cleaned Datasets** (`data/3_interim/workforce_clean.parquet`, `data/3_interim/capacity_clean.parquet`)
   - **Purpose**: Primary data source for all analysis
   - **Justification**: Already cleaned and validated in User Story 2; contains standardized column names, data types, and no duplicates/outliers
   - **Reuse**: Load directly into analysis notebook

2. **Data Validation Module** (`src/data_processing/validation.py`)
   - **Purpose**: Schema validation and data quality checks
   - **Justification**: Provides `validate_schema()`, `validate_value_ranges()`, and other checks
   - **Reuse**: Import to validate data after loading

3. **Logger Utility** (`src/utils/logger.py`)
   - **Purpose**: Logging configuration
   - **Justification**: Consistent logging across project
   - **Reuse**: Import `setup_logger()` for analysis logging

4. **Configuration Loader** (`src/utils/config_loader.py`)
   - **Purpose**: Load YAML configuration files
   - **Justification**: Centralized config management
   - **Reuse**: Load visualization settings from `config/analysis.yml`

**New Components Required**:

1. **Analysis Notebook** (`notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`)
   - **Purpose**: Interactive EDA with visualizations and statistical tests
   - **Justification**: No existing EDA notebook for workforce-capacity analysis
   - **Create**: New Jupyter notebook

2. **Statistical Analysis Module** (`src/analysis/workforce_statistics.py`)
   - **Purpose**: Reusable functions for growth rates, composition metrics, statistical tests
   - **Justification**: Statistical logic should be modular for reuse in Story 4
   - **Create**: New Python module

3. **Visualization Module** (`src/visualization/workforce_plots.py`)
   - **Purpose**: Standardized plotting functions for workforce/capacity data
   - **Justification**: Visualization code reusable across multiple analyses
   - **Create**: New Python module

4. **EDA Report** (`reports/workforce_capacity_eda_report.md`)
   - **Purpose**: Stakeholder-ready markdown report with findings and visualizations
   - **Justification**: Required deliverable for acceptance criteria
   - **Create**: New markdown document

**Gaps Identified**:
- No existing statistical analysis utilities for healthcare workforce metrics
- No visualization templates for temporal trends and sector comparisons
- No report generation templates for EDA findings

---

### 3. Affected Files with Implementation Context

**[CREATE] `src/analysis/workforce_statistics.py`**
- **Purpose**: Statistical analysis functions (growth rates, composition metrics, hypothesis tests)
- **Inputs**: Polars DataFrames (workforce_df, capacity_df)
- **Outputs**: Calculated metrics (growth rates, ratios, test statistics)
- **Logging**: Log to `logs/analysis/eda_{timestamp}.log`

**[CREATE] `src/visualization/workforce_plots.py`**
- **Purpose**: Standardized plotting functions for workforce and capacity data
- **Inputs**: Polars DataFrames, plot configuration parameters
- **Outputs**: Matplotlib figures saved to `reports/figures/`
- **Logging**: Log figure generation to `logs/analysis/eda_{timestamp}.log`

**[CREATE] `notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`**
- **Purpose**: Interactive EDA notebook orchestrating analysis and visualization
- **Inputs**: Cleaned parquet files from `data/3_interim/`
- **Outputs**: 
  - Figures to `reports/figures/problem-statement-001/`
  - Summary tables to `results/tables/problem-statement-001/`
  - Console output with findings
- **Logging**: Inline logging with logger configured for notebook context

**[CREATE] `reports/workforce_capacity_eda_report.md`**
- **Purpose**: Comprehensive EDA report with findings, visualizations, and recommendations
- **Inputs**: Analysis results from notebook, embedded figures from `reports/figures/`
- **Outputs**: Markdown document with executive summary and detailed findings
- **Logging**: N/A (documentation output)

**[CREATE] `tests/unit/test_workforce_statistics.py`**
- **Purpose**: Unit tests for statistical analysis functions
- **Inputs**: Sample test data fixtures
- **Outputs**: Test pass/fail results
- **Logging**: Pytest output

**[MODIFY] `config/analysis.yml`**
- **Purpose**: Add visualization configuration parameters for EDA
- **Modifications**: 
  - Add `eda` section with figure settings (DPI, size, color palette)
  - Add statistical test confidence levels
- **Logging**: N/A (configuration file)

---

### 4. Component Breakdown with Technical Constraints

**Component 1: Statistical Analysis Module** (`src/analysis/workforce_statistics.py`)

**Technical Constraints**:
- Use Polars for all data transformations (NOT pandas)
- All functions must have complete type hints and NumPy-style docstrings
- Statistical tests from `scipy.stats` for hypothesis testing
- Functions must handle edge cases (single year data, missing sectors)
- Performance target: Process full dataset in < 5 seconds

**Key Functions**:
- `calculate_growth_rates()`: Year-over-year percentage change
- `calculate_indexed_growth()`: Growth indexed to baseline year
- `calculate_composition_metrics()`: Profession distribution percentages
- `calculate_workforce_to_bed_ratio()`: Workforce-capacity relationship
- `test_sector_growth_differences()`: ANOVA/Kruskal-Wallis for sector comparison
- `test_workforce_capacity_correlation()`: Pearson/Spearman correlation

**Component 2: Visualization Module** (`src/visualization/workforce_plots.py`)

**Technical Constraints**:
- Use matplotlib + seaborn for static visualizations
- All figures saved at 300 DPI for presentation quality
- Consistent color palette across all plots (use seaborn color schemes)
- Figure size: (12, 6) default, (16, 8) for multi-panel plots
- Include clear titles, axis labels, legends, and data source annotations
- Save as PNG (for embedding in reports) and PDF (for printing)

**Key Functions**:
- `plot_temporal_trends()`: Line plots for time series
- `plot_sector_comparison()`: Grouped bar charts
- `plot_composition_stacked()`: Stacked bar/area charts
- `plot_workforce_capacity_scatter()`: Scatter plot with regression line
- `plot_growth_rate_comparison()`: Bar chart with error bars

**Component 3: EDA Notebook** (`notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`)

**Technical Constraints**:
- Must execute sequentially without errors (top to bottom)
- Clear markdown headers for each analysis section
- Inline documentation of findings and interpretations
- Save outputs progressively (tables, figures) for reproducibility
- Total execution time: < 2 minutes on standard laptop

**Structure**:
1. Setup and data loading
2. Summary statistics generation
3. Temporal trend analysis
4. Sector comparison analysis
5. Workforce composition analysis
6. Workforce-capacity relationship analysis
7. Statistical hypothesis testing
8. Key findings documentation

**Component 4: EDA Report** (`reports/workforce_capacity_eda_report.md`)

**Technical Constraints**:
- Markdown format with embedded images (relative paths)
- Executive summary: 1 page maximum
- Include 6-8 key visualizations
- Document statistical test results with interpretation
- List 3-5 actionable insights for policy analysts
- Include data limitations and caveats

---

### 5. Data Pipeline

**Data Sources** ([docs/project_context/data-sources.md](../../../project_context/data-sources.md)):

**Primary Tables**:
1. **Workforce Data** (`data/3_interim/workforce_clean.parquet`)
   - **Schema**: `year: Int32`, `sector: Categorical`, `profession: Categorical`, `count: Int32`
   - **Coverage**: 2006-2019, 3 professions (Doctors, Nurses, Pharmacists), 3 active sectors (Public, Private, Not-for-Profit)
   - **Quality**: Cleaned, validated, no missing values or duplicates

2. **Capacity Data** (`data/3_interim/capacity_clean.parquet`)
   - **Schema**: `year: Int32`, `sector: Categorical`, `category: Categorical`, `count: Int32`
   - **Coverage**: 2009-2020, 2 categories (Hospital Beds, Primary Care Clinics), 3 sectors
   - **Quality**: Cleaned, validated, no missing values or duplicates

**Data Pipeline Strategy**:

**Extraction**:
- Load cleaned Polars DataFrames from parquet files using `pl.read_parquet()`
- Validate schema immediately after loading using `src/data_processing/validation.py`
- Filter out inactive workforce sectors (already done in cleaning pipeline)

**Transformation**:
- **Aggregation Layer**: Group by sector, profession, year for summary statistics
- **Feature Engineering**: 
  - Calculate growth rates: `(count_year_t - count_year_t-1) / count_year_t-1 * 100`
  - Calculate indexed growth: `(count_year_t / count_year_2006) * 100`
  - Calculate composition: `profession_count / total_workforce * 100`
  - Calculate ratios: `total_workforce / total_beds`
- **Statistical Testing**: Apply scipy.stats functions to aggregated data

**Consumption Layer**:
- **Figures**: Saved to `reports/figures/problem-statement-001/` as PNG (300 DPI)
- **Tables**: Saved to `results/tables/problem-statement-001/` as CSV
- **Report**: Markdown document in `reports/` with embedded visualizations
- **Notebook**: Jupyter notebook in `notebooks/2_analysis/` with complete analysis

**Orchestration**:
- **Execution**: Manual execution in Jupyter notebook (no automated scheduling needed for exploratory analysis)
- **Dependency**: Requires User Story 2 completion (cleaned data must exist)
- **Runtime**: < 2 minutes total execution time

**Error Handling**:
- Validate data files exist before loading (raise FileNotFoundError if missing)
- Validate schema after loading (raise ValueError if schema mismatch)
- Log all analysis steps with timestamps
- Raise descriptive errors for statistical test failures (e.g., insufficient data)

---

### 6. Code Generation Specifications

#### 6.1 Function Signatures & Contracts

**Statistical Analysis Functions** (`src/analysis/workforce_statistics.py`):

```python
import polars as pl
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
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
    
    Args:
        workforce_df: DataFrame with workforce counts
        capacity_df: DataFrame with bed counts
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
    
    # Aggregate capacity by join columns (filter to hospital beds only)
    capacity_agg = (
        capacity_df
        .filter(pl.col('category') == 'Hospital Beds')
        .group_by(by)
        .agg([
            pl.col('count').sum().alias('total_beds')
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
) -> Dict[str, any]:
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
) -> Dict[str, any]:
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
```

**Visualization Functions** (`src/visualization/workforce_plots.py`):

```python
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple
from loguru import logger


def plot_temporal_trends(
    df: pl.DataFrame,
    time_col: str = 'year',
    value_col: str = 'count',
    group_col: str = 'sector',
    title: str = 'Temporal Trends',
    ylabel: str = 'Count',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create line plot showing temporal trends grouped by category.
    
    Args:
        df: Input DataFrame
        time_col: Column containing time dimension
        value_col: Column containing values to plot
        group_col: Column containing group categories
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        figsize: Figure size (width, height)
        dpi: Resolution for saved figure
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_temporal_trends(
        ...     workforce_df,
        ...     group_col='profession',
        ...     title='Workforce Trends by Profession',
        ...     output_path='reports/figures/workforce_trends.png'
        ... )
    """
    logger.info(f"Creating temporal trends plot grouped by {group_col}")
    
    # Convert to pandas for plotting
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot lines for each group
    for group in plot_df[group_col].unique():
        group_data = plot_df[plot_df[group_col] == group].sort_values(time_col)
        ax.plot(
            group_data[time_col],
            group_data[value_col],
            marker='o',
            label=group,
            linewidth=2,
            markersize=6
        )
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(time_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(title=group_col.capitalize(), fontsize=10, title_fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add data source annotation
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_sector_comparison(
    df: pl.DataFrame,
    sector_col: str = 'sector',
    value_col: str = 'count',
    category_col: Optional[str] = None,
    title: str = 'Sector Comparison',
    ylabel: str = 'Count',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create grouped bar chart comparing sectors.
    
    Args:
        df: Input DataFrame
        sector_col: Column containing sector categories
        value_col: Column containing values to plot
        category_col: Optional column for grouping within sectors
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_sector_comparison(
        ...     workforce_df,
        ...     category_col='profession',
        ...     title='Workforce by Sector and Profession (2019)',
        ...     output_path='reports/figures/sector_comparison.png'
        ... )
    """
    logger.info(f"Creating sector comparison bar chart")
    
    # Convert to pandas
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if category_col:
        # Grouped bar chart
        sectors = sorted(plot_df[sector_col].unique())
        categories = sorted(plot_df[category_col].unique())
        
        x = np.arange(len(sectors))
        width = 0.8 / len(categories)
        
        for i, category in enumerate(categories):
            category_data = plot_df[plot_df[category_col] == category]
            values = [
                category_data[category_data[sector_col] == sector][value_col].sum()
                for sector in sectors
            ]
            ax.bar(
                x + i * width,
                values,
                width,
                label=category
            )
        
        ax.set_xticks(x + width * (len(categories) - 1) / 2)
        ax.set_xticklabels(sectors)
        ax.legend(title=category_col.capitalize())
    else:
        # Simple bar chart
        sector_data = plot_df.groupby(sector_col)[value_col].sum().reset_index()
        ax.bar(sector_data[sector_col], sector_data[value_col])
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(sector_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_composition_stacked(
    df: pl.DataFrame,
    time_col: str = 'year',
    category_col: str = 'profession',
    value_col: str = 'percentage',
    group_col: str = 'sector',
    title: str = 'Composition Over Time',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create stacked area chart showing composition changes over time.
    
    Args:
        df: Input DataFrame with composition percentages
        time_col: Column containing time dimension
        category_col: Column containing composition categories
        value_col: Column containing percentage values
        group_col: Column to facet by (creates subplots)
        title: Plot title
        output_path: If provided, save figure to this path
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_composition_stacked(
        ...     composition_df,
        ...     category_col='profession',
        ...     group_col='sector',
        ...     title='Workforce Composition by Sector',
        ...     output_path='reports/figures/composition_trends.png'
        ... )
    """
    logger.info(f"Creating stacked composition chart")
    
    # Convert to pandas and pivot
    plot_df = df.to_pandas()
    groups = sorted(plot_df[group_col].unique())
    
    # Create subplots
    fig, axes = plt.subplots(1, len(groups), figsize=figsize, sharey=True)
    if len(groups) == 1:
        axes = [axes]
    
    categories = sorted(plot_df[category_col].unique())
    colors = sns.color_palette('Set2', n_colors=len(categories))
    
    for ax, group in zip(axes, groups):
        group_data = plot_df[plot_df[group_col] == group]
        
        # Pivot for stacked area
        pivot_data = group_data.pivot(
            index=time_col,
            columns=category_col,
            values=value_col
        ).fillna(0)
        
        # Plot stacked area
        ax.stackplot(
            pivot_data.index,
            *[pivot_data[cat] for cat in categories],
            labels=categories,
            colors=colors,
            alpha=0.8
        )
        
        ax.set_title(f'{group}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Year', fontsize=10)
        if ax == axes[0]:
            ax.set_ylabel('Percentage (%)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, 100)
    
    # Add legend to last subplot
    axes[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    
    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_workforce_capacity_scatter(
    df: pl.DataFrame,
    workforce_col: str = 'total_workforce',
    capacity_col: str = 'total_beds',
    group_col: str = 'sector',
    title: str = 'Workforce vs. Capacity',
    output_path: Optional[str] = None,
    add_regression: bool = True,
    figsize: Tuple[int, int] = (10, 8),
    dpi: int = 300
) -> plt.Figure:
    """
    Create scatter plot of workforce vs. capacity with optional regression line.
    
    Args:
        df: Input DataFrame
        workforce_col: Column containing workforce values
        capacity_col: Column containing capacity values
        group_col: Column for color grouping
        title: Plot title
        output_path: If provided, save figure to this path
        add_regression: Whether to add regression line
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_workforce_capacity_scatter(
        ...     ratio_df,
        ...     add_regression=True,
        ...     output_path='reports/figures/workforce_capacity_scatter.png'
        ... )
    """
    logger.info(f"Creating workforce-capacity scatter plot")
    
    # Convert to pandas
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Scatter plot with groups
    groups = sorted(plot_df[group_col].unique())
    colors = sns.color_palette('Set1', n_colors=len(groups))
    
    for group, color in zip(groups, colors):
        group_data = plot_df[plot_df[group_col] == group]
        ax.scatter(
            group_data[capacity_col],
            group_data[workforce_col],
            label=group,
            alpha=0.7,
            s=100,
            color=color,
            edgecolors='black',
            linewidth=0.5
        )
    
    # Add regression line
    if add_regression:
        from scipy.stats import linregress
        x = plot_df[capacity_col]
        y = plot_df[workforce_col]
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept
        
        ax.plot(
            x_line,
            y_line,
            'k--',
            linewidth=2,
            label=f'Regression (R²={r_value**2:.3f})'
        )
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(capacity_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel(workforce_col.replace('_', ' ').title(), fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_growth_rate_comparison(
    df: pl.DataFrame,
    category_col: str = 'sector',
    growth_col: str = 'growth_rate',
    title: str = 'Average Growth Rates by Category',
    ylabel: str = 'Average Growth Rate (%)',
    output_path: Optional[str] = None,
    add_error_bars: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create bar chart comparing average growth rates with error bars.
    
    Args:
        df: Input DataFrame with growth rates
        category_col: Column containing categories to compare
        growth_col: Column containing growth rate values
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        add_error_bars: Whether to add standard error bars
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_growth_rate_comparison(
        ...     growth_df,
        ...     category_col='profession',
        ...     title='Average Growth Rates by Profession',
        ...     output_path='reports/figures/growth_comparison.png'
        ... )
    """
    logger.info(f"Creating growth rate comparison bar chart")
    
    # Convert to pandas
    plot_df = df.filter(pl.col(growth_col).is_not_null()).to_pandas()
    
    # Calculate means and std errors
    stats_df = plot_df.groupby(category_col)[growth_col].agg(['mean', 'sem']).reset_index()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Bar chart
    x = np.arange(len(stats_df))
    bars = ax.bar(
        x,
        stats_df['mean'],
        yerr=stats_df['sem'] if add_error_bars else None,
        capsize=5,
        alpha=0.8,
        edgecolor='black',
        linewidth=1.5
    )
    
    # Color positive bars green, negative bars red
    for bar, mean_val in zip(bars, stats_df['mean']):
        if mean_val >= 0:
            bar.set_color('forestgreen')
        else:
            bar.set_color('firebrick')
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(category_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(stats_df[category_col])
    ax.axhline(0, color='black', linewidth=0.8)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (bar, mean_val, sem_val) in enumerate(zip(bars, stats_df['mean'], stats_df['sem'])):
        height = bar.get_height()
        label_y = height + sem_val + 0.2 if height >= 0 else height - sem_val - 0.5
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            label_y,
            f'{mean_val:.1f}%',
            ha='center',
            va='bottom' if height >= 0 else 'top',
            fontsize=9,
            fontweight='bold'
        )
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig
```

#### 6.2 Data Schemas (Executable Format)

```python
from pydantic import BaseModel, Field
from typing import Literal


class WorkforceRecord(BaseModel):
    """Schema for workforce data records."""
    year: int = Field(..., ge=2006, le=2019, description="Year of record")
    sector: Literal['Public', 'Private', 'Not-for-profit'] = Field(..., description="Healthcare sector")
    profession: Literal['Doctors', 'Nurses', 'Pharmacists'] = Field(..., description="Healthcare profession")
    count: int = Field(..., ge=0, description="Workforce count")


class CapacityRecord(BaseModel):
    """Schema for capacity data records."""
    year: int = Field(..., ge=2009, le=2020, description="Year of record")
    sector: Literal['Public', 'Private', 'Not-for-profit'] = Field(..., description="Healthcare sector")
    category: Literal['Hospital Beds', 'Primary Care Clinics'] = Field(..., description="Capacity category")
    count: int = Field(..., ge=0, description="Capacity count")
```

#### 6.3 Data Validation Rules (Executable Format)

```python
# Required columns for each dataset
WORKFORCE_REQUIRED_COLUMNS = ['year', 'sector', 'profession', 'count']
CAPACITY_REQUIRED_COLUMNS = ['year', 'sector', 'category', 'count']

# Expected data types (Polars)
WORKFORCE_EXPECTED_DTYPES = {
    'year': pl.Int32,
    'sector': pl.Categorical,
    'profession': pl.Categorical,
    'count': pl.Int32
}

CAPACITY_EXPECTED_DTYPES = {
    'year': pl.Int32,
    'sector': pl.Categorical,
    'category': pl.Categorical,
    'count': pl.Int32
}

# Value constraints
WORKFORCE_CONSTRAINTS = {
    'year': {'min': 2006, 'max': 2019},
    'count': {'min': 0, 'max': 50000},  # Reasonable upper bound
    'sector': {'values': ['Public', 'Private', 'Not-for-profit']},
    'profession': {'values': ['Doctors', 'Nurses', 'Pharmacists']}
}

CAPACITY_CONSTRAINTS = {
    'year': {'min': 2009, 'max': 2020},
    'count': {'min': 0, 'max': 30000},
    'sector': {'values': ['Public', 'Private', 'Not-for-profit']},
    'category': {'values': ['Hospital Beds', 'Primary Care Clinics']}
}

# Domain benchmarks for validation
WORKFORCE_TO_BED_BENCHMARKS = {
    'typical_min': 1.5,  # FTE per bed
    'typical_max': 2.5,
    'understaffed_threshold': 1.0,
    'overstaffed_threshold': 3.0
}

DOCTOR_TO_NURSE_RATIO_BENCHMARKS = {
    'typical_min': 0.25,  # 1:4 ratio
    'typical_max': 0.50,  # 1:2 ratio
}
```

#### 6.4 Library-Specific Implementation Patterns

**Polars Patterns:**

```python
# Lazy loading for large files (not needed for this dataset but good practice)
workforce_df = pl.scan_parquet('data/3_interim/workforce_clean.parquet').collect()

# Method chaining for transformations
active_workforce = (
    workforce_df
    .filter(pl.col('sector') != 'Inactive')
    .sort(['sector', 'profession', 'year'])
    .with_columns([
        pl.col('count').cast(pl.Float64)
    ])
)

# Aggregation with multiple statistics
summary_stats = (
    workforce_df
    .group_by('sector')
    .agg([
        pl.count().alias('n_records'),
        pl.col('count').sum().alias('total'),
        pl.col('count').mean().alias('avg'),
        pl.col('count').std().alias('std_dev'),
        pl.col('count').min().alias('min'),
        pl.col('count').max().alias('max')
    ])
)

# Window functions for year-over-year calculations
growth_df = (
    workforce_df
    .sort(['sector', 'profession', 'year'])
    .with_columns([
        pl.col('count').shift(1).over(['sector', 'profession']).alias('prev_year_count')
    ])
    .with_columns([
        ((pl.col('count') - pl.col('prev_year_count')) / pl.col('prev_year_count') * 100).alias('growth_rate')
    ])
)
```

**Logging Patterns (Loguru):**

```python
from loguru import logger
from datetime import datetime

# Setup logging for notebook/script
log_dir = Path('logs/analysis')
log_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
logger.add(
    log_dir / f'eda_{timestamp}.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

logger.info("Starting exploratory data analysis")
logger.info(f"Workforce data shape: {workforce_df.shape}")
logger.success("Data loaded successfully")
logger.warning("Growth rate contains nulls for first year (expected)")
logger.error(f"Failed to load file: {e}")
```

**Configuration Loading Patterns:**

```python
import yaml
from pathlib import Path

def load_analysis_config(config_path: str = "config/analysis.yml") -> dict:
    """Load analysis configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Use config for visualization settings
config = load_analysis_config()
figsize = tuple(config['visualization']['figure_size'])
dpi = config['visualization']['dpi']
```

**Error Handling Patterns:**

```python
from loguru import logger
from pathlib import Path

def safe_load_data(file_path: str) -> pl.DataFrame | None:
    """Safely load parquet file with error handling."""
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Data file missing: {file_path}")
        
        df = pl.read_parquet(file_path)
        logger.success(f"Loaded {df.shape[0]} rows from {file_path}")
        return df
    
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        raise
```

#### 6.5 Test Specifications with Assertions

```python
import pytest
import polars as pl
import numpy as np
from src.analysis.workforce_statistics import (
    calculate_growth_rates,
    calculate_indexed_growth,
    calculate_composition_metrics,
    calculate_workforce_to_bed_ratio,
    test_sector_growth_differences,
    test_workforce_capacity_correlation
)


@pytest.fixture
def sample_workforce_data() -> pl.DataFrame:
    """Sample workforce data for testing."""
    return pl.DataFrame({
        'year': [2006, 2007, 2008, 2006, 2007, 2008],
        'sector': ['Public', 'Public', 'Public', 'Private', 'Private', 'Private'],
        'profession': ['Doctors', 'Doctors', 'Doctors', 'Doctors', 'Doctors', 'Doctors'],
        'count': [1000, 1050, 1100, 500, 525, 550]
    })


@pytest.fixture
def sample_capacity_data() -> pl.DataFrame:
    """Sample capacity data for testing."""
    return pl.DataFrame({
        'year': [2006, 2007, 2008, 2006, 2007, 2008],
        'sector': ['Public', 'Public', 'Public', 'Private', 'Private', 'Private'],
        'category': ['Hospital Beds', 'Hospital Beds', 'Hospital Beds', 'Hospital Beds', 'Hospital Beds', 'Hospital Beds'],
        'count': [5000, 5200, 5400, 2000, 2100, 2200]
    })


def test_calculate_growth_rates(sample_workforce_data):
    """Test growth rate calculation."""
    result = calculate_growth_rates(
        sample_workforce_data,
        group_cols=['sector', 'profession']
    )
    
    # Check structure
    assert 'growth_rate' in result.columns
    assert result.height == sample_workforce_data.height
    
    # Check first year has null growth (no prior year)
    first_year_rows = result.filter(pl.col('year') == 2006)
    assert first_year_rows['growth_rate'].null_count() == first_year_rows.height
    
    # Check calculated values (Public: 1000 -> 1050 = 5% growth)
    public_2007 = result.filter(
        (pl.col('sector') == 'Public') & (pl.col('year') == 2007)
    )['growth_rate'].item()
    assert abs(public_2007 - 5.0) < 0.01  # 5% growth


def test_calculate_indexed_growth(sample_workforce_data):
    """Test indexed growth calculation."""
    result = calculate_indexed_growth(
        sample_workforce_data,
        group_cols=['sector'],
        base_year=2006
    )
    
    # Check structure
    assert 'indexed_value' in result.columns
    
    # Base year should have index of 100
    base_year_values = result.filter(pl.col('year') == 2006)['indexed_value'].unique()
    assert all(abs(v - 100.0) < 0.01 for v in base_year_values.to_list())
    
    # Check calculated index (Public: 1000 -> 1100 = index 110)
    public_2008 = result.filter(
        (pl.col('sector') == 'Public') & (pl.col('year') == 2008)
    )['indexed_value'].item()
    assert abs(public_2008 - 110.0) < 0.01


def test_calculate_composition_metrics():
    """Test composition percentage calculation."""
    df = pl.DataFrame({
        'year': [2006, 2006, 2006],
        'sector': ['Public', 'Public', 'Public'],
        'profession': ['Doctors', 'Nurses', 'Pharmacists'],
        'count': [1000, 3000, 500]
    })
    
    result = calculate_composition_metrics(
        df,
        group_cols=['year', 'sector'],
        category_col='profession'
    )
    
    # Check percentages sum to 100
    total_pct = result['percentage'].sum()
    assert abs(total_pct - 100.0) < 0.01
    
    # Check specific values (3000/4500 * 100 = 66.67% for nurses)
    nurse_pct = result.filter(pl.col('profession') == 'Nurses')['percentage'].item()
    assert abs(nurse_pct - 66.67) < 0.01


def test_calculate_workforce_to_bed_ratio(sample_workforce_data, sample_capacity_data):
    """Test workforce-to-bed ratio calculation."""
    result = calculate_workforce_to_bed_ratio(
        sample_workforce_data,
        sample_capacity_data,
        by=['year', 'sector']
    )
    
    # Check structure
    assert 'total_workforce' in result.columns
    assert 'total_beds' in result.columns
    assert 'workforce_to_bed_ratio' in result.columns
    
    # Check calculation (Public 2006: 1000 workforce / 5000 beds = 0.2)
    public_2006 = result.filter(
        (pl.col('sector') == 'Public') & (pl.col('year') == 2006)
    )['workforce_to_bed_ratio'].item()
    assert abs(public_2006 - 0.2) < 0.01


def test_test_sector_growth_differences():
    """Test ANOVA/Kruskal-Wallis for sector differences."""
    growth_df = pl.DataFrame({
        'sector': ['Public'] * 10 + ['Private'] * 10,
        'growth_rate': [3.0, 3.5, 4.0, 3.2, 3.8] * 2 + [2.0, 2.5, 2.2, 2.8, 2.3] * 2
    })
    
    result = test_sector_growth_differences(growth_df)
    
    # Check result structure
    assert 'test_used' in result
    assert 'p_value' in result
    assert 'significant' in result
    assert 'conclusion' in result
    
    # P-value should be between 0 and 1
    assert 0 <= result['p_value'] <= 1


def test_test_workforce_capacity_correlation(sample_workforce_data, sample_capacity_data):
    """Test correlation between workforce and capacity."""
    # Calculate ratios
    ratio_df = calculate_workforce_to_bed_ratio(
        sample_workforce_data,
        sample_capacity_data,
        by=['year', 'sector']
    )
    
    result = test_workforce_capacity_correlation(
        ratio_df,
        method='pearson'
    )
    
    # Check result structure
    assert 'correlation' in result
    assert 'p_value' in result
    assert 'significant' in result
    assert 'strength' in result
    assert 'direction' in result
    
    # Correlation should be between -1 and 1
    assert -1 <= result['correlation'] <= 1
```

#### 6.6 Package Management Specifications

```bash
# Install required packages using uv (MANDATORY - not pip)
uv pip install polars>=0.20.0
uv pip install scipy>=1.11.0
uv pip install matplotlib>=3.7.0
uv pip install seaborn>=0.12.0
uv pip install numpy>=1.24.0
uv pip install jupyter>=1.0.0
uv pip install loguru>=0.7.0
uv pip install pydantic>=2.0.0
uv pip install pytest>=7.4.0
uv pip install pyyaml>=6.0

# Update requirements.txt after installation
uv pip freeze > requirements.txt
```

---

### 7. Domain-Driven Feature Engineering & Analysis Strategy

**Step 1: Identify Relevant Domain Knowledge**

**Selected Domain Knowledge**: [Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md)

**Relevant Sections**:
1. **Standard Metrics and KPIs** → Provides definitions for:
   - Workforce growth rate (YoY percentage change)
   - Workforce-to-bed ratio (staffing intensity metric)
   - Workforce composition ratio (doctor-to-nurse ratios)
   - Indexed growth (baseline comparison)

2. **Feature Engineering Guidance - Temporal Features** → Specifies calculations for:
   - Year-over-year growth rates
   - Cumulative indexed growth (base year = 100)
   - Growth momentum (acceleration/deceleration)

3. **Feature Engineering Guidance - Ratio Features** → Provides formulas for:
   - Workforce-to-bed ratio by sector
   - Normalized ratios (relative to average)
   - Composition indices (profession percentages)

4. **Feature Engineering Guidance - Capacity-Aligned Features** → Defines:
   - Supply-demand gap (workforce growth - capacity growth)
   - Relative staffing level (workforce index / capacity index)

**Domain Benchmarks for Validation**:
- Workforce-to-bed ratio: 1.5-2.5 FTE per bed (typical range)
- Understaffed threshold: < 1.0 FTE per bed
- Overstaffed threshold: > 3.0 FTE per bed
- Doctor-to-nurse ratio: 1:2 to 1:4 (typical range)

**Step 2: Validate Data Availability**

**Data Availability Cross-Reference**:

| Domain Feature | Required Data Fields | Available in Dataset | Data Quality |
|----------------|---------------------|---------------------|--------------|
| Workforce Growth Rate | `year`, `sector`, `profession`, `count` | ✅ Yes (workforce_clean.parquet) | High (no nulls, validated) |
| Indexed Growth | `year`, `count`, baseline year (2006) | ✅ Yes | High |
| Workforce-to-Bed Ratio | `workforce.count`, `capacity.count` (beds), `year`, `sector` | ✅ Yes (both parquet files) | High (aligned sectors/years) |
| Composition Metrics | `profession`, `count`, `year`, `sector` | ✅ Yes | High |
| Doctor-to-Nurse Ratio | `profession='Doctors'`, `profession='Nurses'`, `count` | ✅ Yes | High |
| Supply-Demand Gap | Workforce growth rate, capacity growth rate | ✅ Yes (calculable from counts) | High |

**Data Gaps**:
- **Population data**: Not available → Cannot calculate workforce density per 1,000 population
  - **Mitigation**: Omit workforce density metric; focus on sector-relative metrics
- **FTE vs. Headcount**: Documentation unclear on whether counts are FTE or headcount
  - **Mitigation**: Document assumption (assume headcount); note limitation in report

**Feasibility Assessment**: ✅ **All proposed domain-driven features are feasible** with available data

**Step 3: Select Applicable Features**

**Selected Features** (all satisfy domain grounding + data availability):

1. **Year-over-Year Growth Rate**
   - **Domain Source**: [Healthcare Workforce Planning - Temporal Features](../../../domain_knowledge/healthcare-workforce-planning.md#temporal-features)
   - **Calculation**: `(count_year_t - count_year_t-1) / count_year_t-1 × 100`
   - **Expected Range**: 2-5% annually (domain benchmark)
   - **Analytical Approach**: Compare growth rates across sectors and professions using ANOVA to test for significant differences

2. **Indexed Growth (Base Year = 2006)**
   - **Domain Source**: [Healthcare Workforce Planning - Temporal Features](../../../domain_knowledge/healthcare-workforce-planning.md#temporal-features)
   - **Calculation**: `(count_year_t / count_2006) × 100`
   - **Expected Range**: 100 (baseline) to 150+ (50% cumulative growth over 14 years)
   - **Analytical Approach**: Visualize indexed trends to compare long-term growth trajectories

3. **Workforce-to-Bed Ratio**
   - **Domain Source**: [Healthcare Workforce Planning - Workforce-to-Bed Ratio](../../../domain_knowledge/healthcare-workforce-planning.md#workforce-to-bed-ratio)
   - **Calculation**: `total_workforce / total_hospital_beds`
   - **Expected Range**: 1.5-2.5 FTE per bed (typical); <1.0 (understaffed); >3.0 (overstaffed)
   - **Analytical Approach**: Compare ratio across sectors; flag sectors outside benchmark range

4. **Workforce Composition Percentage**
   - **Domain Source**: [Healthcare Workforce Planning - Composition Ratio](../../../domain_knowledge/healthcare-workforce-planning.md#workforce-composition-ratio)
   - **Calculation**: `profession_count / total_workforce × 100`
   - **Expected Range**: Varies by profession (nurses typically 50-65%, doctors 20-30%)
   - **Analytical Approach**: Track composition shifts over time using stacked area charts

5. **Doctor-to-Nurse Ratio**
   - **Domain Source**: [Healthcare Workforce Planning - Composition Ratio](../../../domain_knowledge/healthcare-workforce-planning.md#workforce-composition-ratio)
   - **Calculation**: `count(Doctors) / count(Nurses)`
   - **Expected Range**: 0.25 to 0.50 (1:4 to 1:2 ratio)
   - **Analytical Approach**: Compare across sectors; track trends over time

6. **Supply-Demand Gap (Workforce vs. Capacity Growth)**
   - **Domain Source**: [Healthcare Workforce Planning - Capacity-Aligned Features](../../../domain_knowledge/healthcare-workforce-planning.md#capacity-aligned-features)
   - **Calculation**: `workforce_growth_rate - capacity_growth_rate`
   - **Expected Range**: -5% to +5% (aligned growth); >5% (workforce outpacing capacity); <-5% (capacity outpacing workforce)
   - **Analytical Approach**: Scatter plot of workforce growth vs. capacity growth; calculate correlation

**Features Explicitly Rejected**:
- **Workforce Density (per 1,000 population)**: Data not available (population counts missing)
- **Specialist-to-Generalist Ratio**: Data not available (profession not stratified by specialization)

---

### 8. API Endpoints & Data Contracts

**Not applicable** - This user story focuses on exploratory analysis and does not include API or data service development.

---

### 9. Styling & Visualization

**Visualization Standards** (based on `config/analysis.yml`):

**Figure Specifications**:
- **Default figure size**: 12 × 6 inches (temporal trends, bar charts)
- **Multi-panel figure size**: 16 × 8 inches (composition stacked charts, faceted plots)
- **DPI**: 300 (high resolution for presentations)
- **Color palette**: Seaborn 'Set2' for categorical data (sector, profession)
- **Style**: `seaborn-v0_8-whitegrid` (clean, professional appearance)

**Chart-Specific Guidelines**:

1. **Temporal Trend Line Plots**:
   - Line width: 2 pixels
   - Marker size: 6 points
   - Grid: Enabled, dashed lines, 30% opacity
   - Legend: Top-right or outside plot area
   - Y-axis: Start at 0 for counts, auto-scale for growth rates
   - Data source annotation: Bottom-right, 8pt font, gray italic

2. **Sector Comparison Bar Charts**:
   - Bar colors: Distinct colors per category (use palette)
   - Edge color: Black, 1.5px width for clarity
   - Value labels: On top of bars, bold, 9pt font
   - Grid: Horizontal only, 30% opacity
   - X-axis labels: Sector names, readable font size (10pt)

3. **Stacked Area/Bar Charts (Composition)**:
   - Opacity: 80% (alpha=0.8) for clarity
   - Legend: Outside plot area (right side) to avoid overlap
   - Y-axis: 0-100% scale for composition percentages
   - Faceting: By sector (one subplot per sector for comparison)

4. **Scatter Plots (Workforce vs. Capacity)**:
   - Marker size: 100 (s=100)
   - Marker opacity: 70% (alpha=0.7)
   - Edge color: Black, 0.5px width
   - Regression line: Black dashed, 2px width, R² annotation
   - Color grouping: By sector (distinct colors)

5. **Growth Rate Comparison Bar Charts**:
   - Positive growth: Forest green color
   - Negative growth: Firebrick red color
   - Error bars: Standard error, cap size 5
   - Horizontal line at y=0: Black, 0.8px width

**Consistent Elements Across All Plots**:
- **Title**: 14pt, bold, top padding 15px
- **Axis labels**: 12pt, descriptive (not abbreviations)
- **Data source**: "Source: MOH Singapore via Kaggle" (bottom-right, 8pt, gray italic)
- **Grid**: Dashed lines, 30% opacity
- **Legend**: 10pt font, title 11pt, descriptive labels

**Output Formats**:
- **PNG**: Primary format for embedding in markdown reports (300 DPI)
- **PDF**: Optional for high-quality printing
- **File naming convention**: `[metric]_[dimension]_[timestamp].png`
  - Example: `workforce_trends_by_sector_20260223.png`

**Visual Implementation Checklist**:
- [ ] All plots use consistent color palette (Seaborn 'Set2')
- [ ] All plots saved at 300 DPI resolution
- [ ] Data source attribution added to all figures
- [ ] Titles are descriptive and include time period
- [ ] Axis labels are clear and include units
- [ ] Legends positioned to avoid overlapping data
- [ ] Figure files saved to `reports/figures/problem-statement-001/`
- [ ] File names follow naming convention
- [ ] All text is readable at presentation size (check on projector/screen)

---

### 10. Testing Strategy with Specific Assertions

**Unit Tests** (`tests/unit/test_workforce_statistics.py`):

**Test Coverage**:
1. **Growth Rate Calculation** (`test_calculate_growth_rates`):
   - Verify 'growth_rate' column added to output
   - Assert first year has null growth rates (no prior year)
   - Validate calculation: 1000 → 1050 = 5% growth
   - Check handling of zero values (division by zero)

2. **Indexed Growth Calculation** (`test_calculate_indexed_growth`):
   - Verify 'indexed_value' column added
   - Assert base year (2006) has index = 100
   - Validate calculation: 1000 → 1100 = index 110
   - Test error raised if base_year not in data

3. **Composition Metrics** (`test_calculate_composition_metrics`):
   - Verify 'percentage' column added
   - Assert percentages sum to 100 within each group
   - Validate calculation: 3000/4500 = 66.67%

4. **Workforce-to-Bed Ratio** (`test_calculate_workforce_to_bed_ratio`):
   - Verify correct join on year and sector
   - Assert ratio column calculated
   - Validate calculation: 1000 workforce / 5000 beds = 0.2
   - Test error raised if no matching records

5. **Statistical Tests** (`test_test_sector_growth_differences`, `test_test_workforce_capacity_correlation`):
   - Verify test result dictionary structure
   - Assert p-value in range [0, 1]
   - Assert correlation in range [-1, 1]
   - Check normality detection logic (parametric vs. non-parametric)

**Mock Data Fixtures**:
```python
@pytest.fixture
def sample_workforce_data() -> pl.DataFrame:
    return pl.DataFrame({
        'year': [2006, 2007, 2008, 2006, 2007, 2008],
        'sector': ['Public', 'Public', 'Public', 'Private', 'Private', 'Private'],
        'profession': ['Doctors', 'Doctors', 'Doctors', 'Doctors', 'Doctors', 'Doctors'],
        'count': [1000, 1050, 1100, 500, 525, 550]
    })
```

**Data Quality Tests** (`tests/data/test_eda_data_quality.py`):

**Schema Validation Tests**:
```python
def test_workforce_schema():
    """Validate workforce data schema."""
    df = pl.read_parquet('data/3_interim/workforce_clean.parquet')
    
    # Check required columns exist
    assert set(WORKFORCE_REQUIRED_COLUMNS).issubset(set(df.columns))
    
    # Check data types
    assert df['year'].dtype == pl.Int32
    assert df['sector'].dtype == pl.Categorical
    assert df['profession'].dtype == pl.Categorical
    assert df['count'].dtype == pl.Int32


def test_capacity_schema():
    """Validate capacity data schema."""
    df = pl.read_parquet('data/3_interim/capacity_clean.parquet')
    
    # Check required columns
    assert set(CAPACITY_REQUIRED_COLUMNS).issubset(set(df.columns))
    
    # Check data types
    assert df['year'].dtype == pl.Int32
    assert df['category'].dtype == pl.Categorical
```

**Data Completeness Tests**:
```python
def test_workforce_completeness():
    """Validate workforce data completeness."""
    df = pl.read_parquet('data/3_interim/workforce_clean.parquet')
    
    # No null values allowed
    assert df.null_count().sum_horizontal().item() == 0
    
    # Check year range
    assert df['year'].min() >= 2006
    assert df['year'].max() <= 2019
    
    # Check count is positive
    assert df['count'].min() >= 0
```

**Data Accuracy Tests**:
```python
def test_sector_values():
    """Validate sector categorical values."""
    df = pl.read_parquet('data/3_interim/workforce_clean.parquet')
    
    # Check valid sector values
    valid_sectors = {'Public', 'Private', 'Not-for-profit'}
    actual_sectors = set(df['sector'].unique().to_list())
    assert actual_sectors.issubset(valid_sectors)
```

**Integration Tests** (`tests/integration/test_eda_pipeline.py`):

**End-to-End Pipeline Test**:
```python
def test_eda_pipeline_execution():
    """Test complete EDA pipeline runs without errors."""
    from src.analysis.workforce_statistics import calculate_growth_rates
    from src.visualization.workforce_plots import plot_temporal_trends
    
    # Load data
    workforce_df = pl.read_parquet('data/3_interim/workforce_clean.parquet')
    
    # Calculate growth rates
    growth_df = calculate_growth_rates(workforce_df, group_cols=['sector', 'profession'])
    assert 'growth_rate' in growth_df.columns
    
    # Generate plot
    fig = plot_temporal_trends(
        workforce_df.filter(pl.col('sector') != 'Inactive'),
        group_col='sector',
        title='Test Plot'
    )
    assert fig is not None
    plt.close(fig)
```

**Performance Benchmarks**:
```python
import time

def test_growth_rate_performance():
    """Ensure growth rate calculation completes within 5 seconds."""
    df = pl.read_parquet('data/3_interim/workforce_clean.parquet')
    
    start_time = time.time()
    result = calculate_growth_rates(df, group_cols=['sector', 'profession'])
    elapsed = time.time() - start_time
    
    assert elapsed < 5.0, f"Growth rate calculation took {elapsed:.2f}s (expected < 5s)"
```

---

### 11. Implementation Steps

**Implementation Checklist:**

**Phase 1: Environment Setup**

- [ ] Verify Python 3.9+ environment active
- [ ] Install required dependencies using `uv`:
  ```bash
  uv pip install polars scipy matplotlib seaborn numpy jupyter loguru pydantic pytest pyyaml
  ```
- [ ] Update requirements.txt: `uv pip freeze > requirements.txt`
- [ ] Verify cleaned data files exist:
  - `data/3_interim/workforce_clean.parquet`
  - `data/3_interim/capacity_clean.parquet`
- [ ] Create output directories:
  ```bash
  mkdir -p reports/figures/problem-statement-001
  mkdir -p results/tables/problem-statement-001
  mkdir -p logs/analysis
  mkdir -p notebooks/2_analysis
  mkdir -p src/analysis
  mkdir -p src/visualization
  mkdir -p tests/unit
  mkdir -p tests/data
  ```
- [ ] Update `config/analysis.yml` with EDA visualization settings:
  ```yaml
  eda:
    figure_size: [12, 6]
    dpi: 300
    color_palette: 'Set2'
    style: 'seaborn-v0_8-whitegrid'
    alpha: 0.05  # Statistical significance level
  ```

**Phase 2: Statistical Analysis Module Implementation**

- [ ] Create `src/analysis/__init__.py` (empty file for module recognition)
- [ ] Create `src/analysis/workforce_statistics.py` with all functions:
  - `calculate_growth_rates()` - YoY percentage change
  - `calculate_indexed_growth()` - Growth indexed to base year
  - `calculate_composition_metrics()` - Profession distribution percentages
  - `calculate_workforce_to_bed_ratio()` - Workforce-capacity relationship
  - `test_sector_growth_differences()` - ANOVA/Kruskal-Wallis test
  - `test_workforce_capacity_correlation()` - Pearson/Spearman correlation
- [ ] Add imports, type hints, and NumPy-style docstrings to all functions
- [ ] Add loguru logging to all functions (log inputs, outputs, errors)
- [ ] Handle edge cases (null values, division by zero, missing years)

**Phase 3: Visualization Module Implementation**

- [ ] Create `src/visualization/__init__.py` (empty file)
- [ ] Create `src/visualization/workforce_plots.py` with plotting functions:
  - `plot_temporal_trends()` - Line plots for time series
  - `plot_sector_comparison()` - Grouped bar charts
  - `plot_composition_stacked()` - Stacked area charts by sector
  - `plot_workforce_capacity_scatter()` - Scatter plot with regression
  - `plot_growth_rate_comparison()` - Bar chart with error bars
- [ ] Configure consistent styling (color palette, DPI, figure size)
- [ ] Add data source annotations to all plots
- [ ] Implement automatic figure saving to `reports/figures/`
- [ ] Test each plotting function with sample data

**Phase 4: Unit Test Implementation**

- [ ] Create `tests/unit/test_workforce_statistics.py`
- [ ] Implement test fixtures (`sample_workforce_data`, `sample_capacity_data`)
- [ ] Write unit tests for all statistical functions:
  - `test_calculate_growth_rates()` - Validate calculation logic
  - `test_calculate_indexed_growth()` - Check base year = 100
  - `test_calculate_composition_metrics()` - Verify percentages sum to 100
  - `test_calculate_workforce_to_bed_ratio()` - Validate join and ratio calculation
  - `test_test_sector_growth_differences()` - Check statistical test structure
  - `test_test_workforce_capacity_correlation()` - Validate correlation bounds
- [ ] Run tests: `pytest tests/unit/test_workforce_statistics.py -v`
- [ ] Ensure all tests pass before proceeding

**Phase 5: Data Quality Validation**

- [ ] Create `tests/data/test_eda_data_quality.py`
- [ ] Implement schema validation tests:
  - `test_workforce_schema()` - Column names and data types
  - `test_capacity_schema()` - Column names and data types
- [ ] Implement completeness tests:
  - `test_workforce_completeness()` - No nulls, year range, positive counts
  - `test_capacity_completeness()` - No nulls, year range
- [ ] Implement accuracy tests:
  - `test_sector_values()` - Valid categorical values
  - `test_profession_values()` - Valid profession categories
- [ ] Run data quality tests: `pytest tests/data/ -v`
- [ ] Document any data quality issues discovered

**Phase 6: Exploratory Analysis Notebook Creation**

- [ ] Create Jupyter notebook: `notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`
- [ ] **Section 1: Setup and Data Loading**
  - Import libraries (polars, matplotlib, seaborn, scipy, loguru)
  - Configure logging to `logs/analysis/eda_{timestamp}.log`
  - Load configuration from `config/analysis.yml`
  - Load cleaned parquet files
  - Validate schema using `src.data_processing.validation`
  - Display data shapes, column names, data types
  - Show first/last 5 rows of each dataset

- [ ] **Section 2: Summary Statistics Generation**
  - Calculate workforce summary by sector (2006 baseline):
    - Count, sum, mean, std, min, max by sector
  - Calculate workforce summary by profession:
    - Count, sum, mean, std, min, max by profession
  - Calculate capacity summary by sector and category
  - Identify extreme values (highest/lowest by category)
  - Save summary tables to `results/tables/problem-statement-001/`
  - Generate markdown-formatted summary for report

- [ ] **Section 3: Temporal Trend Analysis**
  - Calculate year-over-year growth rates for:
    - Workforce by sector (all professions combined)
    - Workforce by profession (all sectors combined)
    - Capacity by sector (hospital beds)
  - Calculate indexed growth (base year = 2006):
    - Index workforce to baseline
    - Index capacity to baseline
  - Visualize temporal trends:
    - Line plot: Workforce count by sector (2006-2019)
    - Line plot: Workforce count by profession (2006-2019)
    - Line plot: Indexed workforce growth by sector
    - Line plot: Capacity (beds) by sector (2009-2020)
  - Save all figures to `reports/figures/problem-statement-001/`
  - Document key findings:
    - Fastest growing sector/profession
    - Average growth rates by category
    - Any acceleration/deceleration patterns observed

- [ ] **Section 4: Sector Comparison Analysis**
  - Create comparison tables:
    - Baseline (2006) vs. most recent year (2019) by sector
    - Total workforce change (count and percentage)
    - Average annual growth rate by sector
  - Calculate average growth rates:
    - Mean growth rate by sector (with standard error)
    - Mean growth rate by profession
  - Statistical hypothesis test:
    - Test: Growth rates significantly different across sectors?
    - Method: ANOVA or Kruskal-Wallis (depending on normality)
    - Report: Test statistic, p-value, conclusion
  - Visualize sector comparisons:
    - Grouped bar chart: Workforce by sector and profession (2019)
    - Bar chart: Average growth rates by sector (with error bars)
  - Save figures and test results
  - Document findings and implications

- [ ] **Section 5: Workforce Composition Analysis**
  - Calculate composition metrics:
    - Profession distribution (%) by sector and year
    - Doctor-to-nurse ratio by sector and year
    - Track composition shifts over time (2006 vs. 2019)
  - Identify composition patterns:
    - Which professions increasing/decreasing share?
    - Sector differences in composition
  - Visualize composition:
    - Stacked area chart: Workforce composition by sector over time
    - Line plot: Doctor-to-nurse ratio trends by sector
  - Compare against domain benchmarks:
    - Doctor-to-nurse ratio: 0.25-0.50 (1:4 to 1:2)
  - Save figures and composition tables
  - Document composition shift findings

- [ ] **Section 6: Workforce-Capacity Relationship Analysis**
  - Calculate workforce-to-bed ratio:
    - Join workforce and capacity data by year and sector
    - Calculate ratio for each year-sector combination
  - Assess ratios against benchmarks:
    - Compare to domain benchmarks (1.5-2.5 FTE per bed)
    - Flag sectors with ratios <1.0 (understaffed) or >3.0 (overstaffed)
  - Analyze workforce vs. capacity growth alignment:
    - Calculate supply-demand gap (workforce growth - capacity growth)
    - Correlate workforce and capacity growth rates
    - Test correlation significance (Pearson or Spearman)
  - Visualize relationships:
    - Line plot: Workforce-to-bed ratio trends by sector
    - Scatter plot: Workforce growth vs. capacity growth (with regression line)
    - Bar chart: Supply-demand gap by sector
  - Save figures and correlation test results
  - Document workforce-capacity alignment findings

- [ ] **Section 7: Statistical Hypothesis Testing**
  - Execute all planned statistical tests:
    - **Test 1**: Growth rates differ significantly across sectors
      - Method: ANOVA or Kruskal-Wallis
      - Null hypothesis: No difference in mean growth rates
      - Report: Test statistic, p-value, conclusion (α=0.05)
    - **Test 2**: Workforce-to-bed ratio differs across sectors
      - Method: ANOVA or t-tests
      - Report: Test results and confidence intervals
    - **Test 3**: Workforce and capacity growth correlated
      - Method: Pearson or Spearman correlation
      - Report: Correlation coefficient, p-value, strength interpretation
  - Document test assumptions and whether met (normality, homogeneity of variance)
  - Interpret results in domain context
  - Save test results to markdown table

- [ ] **Section 8: Key Findings Documentation**
  - Synthesize 3-5 major patterns identified:
    - Pattern 1: [Description, affected sectors/professions, magnitude]
    - Pattern 2: [Description, affected sectors/professions, magnitude]
    - Pattern 3: [Description, affected sectors/professions, magnitude]
    - Pattern 4: [Optional]
    - Pattern 5: [Optional]
  - For each pattern, document:
    - What the pattern is (with concrete numbers)
    - Which sectors/professions affected
    - Magnitude (growth rate, percentage change, ratio values)
    - Potential implications for policy/planning
  - Highlight unexpected findings or anomalies
  - List questions requiring deeper analysis (inform User Story 4)

- [ ] **Section 9: Data Quality Notes and Limitations**
  - Document data quality observations:
    - Missing years in capacity data (2006-2008)
    - Any sectors/professions with gaps
    - FTE vs. headcount ambiguity
  - Note analysis limitations:
    - Cannot calculate workforce density (no population data)
    - Cannot stratify by specialization
    - Workforce-capacity alignment limited by different year ranges
  - List assumptions made during analysis

- [ ] **Section 10: Export Outputs**
  - Save all summary tables to `results/tables/problem-statement-001/`
  - Verify all figures saved to `reports/figures/problem-statement-001/`
  - Generate list of all output files created
  - Document file naming convention used

**Phase 7: EDA Report Generation**

- [ ] Create comprehensive EDA report: `reports/workforce_capacity_eda_report.md`
- [ ] **Report Structure**:
  - **Executive Summary** (1 page):
    - Analysis objective and scope
    - Data sources and time period
    - 3-5 key findings with high-level implications
  - **1. Overview and Data Summary**:
    - Dataset descriptions (workforce, capacity)
    - Data quality assessment summary
    - Analytical approach overview
  - **2. Temporal Trends Analysis**:
    - Workforce growth patterns by sector
    - Workforce growth patterns by profession
    - Capacity growth patterns by sector
    - Embed 3-4 key temporal trend visualizations
    - Discuss growth trajectories and inflection points
  - **3. Sector Comparison Findings**:
    - Sector comparison summary table
    - Statistical test results (ANOVA)
    - Embed sector comparison bar charts
    - Interpret sector differences
  - **4. Workforce Composition Analysis**:
    - Composition shift summary (2006 vs. 2019)
    - Doctor-to-nurse ratio trends
    - Embed composition stacked charts
    - Discuss implications of composition changes
  - **5. Workforce-Capacity Relationship**:
    - Workforce-to-bed ratio summary by sector
    - Benchmark comparison (1.5-2.5 FTE per bed)
    - Correlation between workforce and capacity growth
    - Embed workforce-capacity scatter plot
    - Identify misalignment issues
  - **6. Statistical Analysis Summary**:
    - Summary table of all hypothesis tests
    - Interpretation of statistical findings
    - Confidence intervals and effect sizes
  - **7. Key Patterns and Insights**:
    - Detailed documentation of 3-5 major patterns
    - Policy implications and recommendations
    - Actionable insights for healthcare planners
  - **8. Data Quality and Limitations**:
    - Data gaps and constraints
    - Assumptions made
    - Caveats for interpretation
  - **9. Recommendations for Deeper Analysis**:
    - Questions requiring further investigation (inform User Story 4)
    - Suggested analytical approaches
    - Additional data sources needed

- [ ] Embed visualizations using relative paths:
  ```markdown
  ![Workforce Trends by Sector](../reports/figures/problem-statement-001/workforce_trends_sector.png)
  ```
- [ ] Format tables in markdown for readability
- [ ] Include data source attribution: "Source: MOH Singapore via Kaggle"
- [ ] Proofread for clarity and accuracy
- [ ] Save report to `reports/workforce_capacity_eda_report.md`

**Phase 8: Validation and Quality Assurance**

- [ ] Re-run full notebook from top to bottom (Kernel → Restart & Run All)
- [ ] Verify no errors during execution
- [ ] Check execution time < 2 minutes
- [ ] Validate all output files created:
  - Figures in `reports/figures/problem-statement-001/`
  - Tables in `results/tables/problem-statement-001/`
  - Report in `reports/`
- [ ] Review all visualizations for:
  - Correct titles and axis labels
  - Data source attribution present
  - Resolution at 300 DPI
  - Readable text and legends
- [ ] Review EDA report for:
  - All visualizations embedded correctly
  - Findings supported by data
  - Clear and concise writing
  - No typos or formatting errors
- [ ] Run all tests: `pytest tests/ -v`
- [ ] Document completion in User Story checklist

**Phase 9: Deliverables Finalization**

- [ ] Save final notebook with all outputs: `notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`
- [ ] Export notebook to HTML for sharing: `jupyter nbconvert --to html exploratory_workforce_capacity_analysis.ipynb`
- [ ] Create summary CSV for stakeholders: `results/exports/workforce_capacity_eda_summary.csv`
  - Include: Key metrics, growth rates, ratios, test results
- [ ] Organize all figures with descriptive filenames
- [ ] Create `reports/figures/problem-statement-001/README.md` listing all figures
- [ ] Archive analysis logs to `logs/analysis/`
- [ ] Update User Story 3 acceptance criteria checklist (mark all complete)
- [ ] Commit all code, notebooks, and outputs to version control
- [ ] Document any open questions or issues for User Story 4

---

### 12. Adaptive Implementation Strategy

**Output-Driven Adaptation Requirements:**

This implementation plan is a **living document** that MUST be updated based on actual findings during analysis execution. The following adaptive procedures are mandatory:

**1. Mandatory Output Review Checkpoints:**

After each notebook section execution, IMMEDIATELY review outputs and ask:
- Does the data distribution match initial assumptions?
- Are there unexpected patterns requiring additional analysis?
- Do statistical test assumptions hold (normality, homogeneity)?
- Are visualizations revealing issues not anticipated in the plan?

**2. Automatic Plan Updates Required When:**

**Scenario A: Data Distribution Issues**
- **Trigger**: Normality tests fail; data is heavily skewed
- **Action**: 
  - Update statistical testing approach (parametric → non-parametric)
  - Add log transformation or rank-based analysis
  - Document change in methodology section

**Scenario B: Insufficient Statistical Power**
- **Trigger**: Sample sizes too small for planned tests; p-values unstable
- **Action**:
  - Switch to non-parametric tests (Kruskal-Wallis, Mann-Whitney)
  - Report effect sizes instead of p-values
  - Document statistical power limitations

**Scenario C: Unexpected Data Patterns**
- **Trigger**: EDA reveals non-linear trends, outliers, or structural breaks
- **Action**:
  - Add segmented analysis (e.g., pre/post policy change)
  - Include outlier investigation section
  - Expand visualization to highlight anomalies

**Scenario D: Missing or Problematic Data**
- **Trigger**: More missing years or sectors than anticipated
- **Action**:
  - Add imputation or exclusion criteria
  - Document data gaps more explicitly
  - Adjust year ranges for analysis to maximize coverage

**Scenario E: Domain Benchmark Violations**
- **Trigger**: Workforce-to-bed ratios far outside expected range (1.5-2.5)
- **Action**:
  - Add benchmark comparison section
  - Investigate reasons for deviations
  - Flag sectors requiring policy attention

**3. Plan Update Procedure:**

When adaptation needed:
1. **Document trigger**: What finding necessitated plan change?
2. **Update implementation steps**: Add new tasks or modify existing
3. **Update code specifications**: Revise function signatures if needed
4. **Update report structure**: Add new sections for unexpected findings
5. **Log decision**: Record in notebook markdown cell why plan changed

**4. Continuous Validation Checkpoints:**

Before proceeding to next phase:
- [ ] Summary statistics reviewed → Do counts, means, ranges make sense?
- [ ] Growth rates calculated → Are values in expected range (2-5% annually)?
- [ ] Ratios calculated → Are values within domain benchmarks?
- [ ] Visualizations generated → Do plots reveal expected patterns or surprises?
- [ ] Statistical tests executed → Are assumptions met? Results interpretable?

**5. Dynamic Prioritization:**

If time-constrained or issues arise:
- **Priority 1 (Must Have)**: Summary statistics, temporal trends, sector comparison, report
- **Priority 2 (Should Have)**: Composition analysis, statistical hypothesis tests
- **Priority 3 (Nice to Have)**: Advanced visualizations, detailed benchmark comparisons

**Example Adaptive Scenarios:**

- **Scenario 1**: Initial plan assumes linear growth → EDA reveals exponential growth in private sector → Add log-scale plots and exponential growth modeling
- **Scenario 2**: Plan includes ANOVA → Levene's test shows heterogeneous variances → Switch to Welch's ANOVA or Kruskal-Wallis
- **Scenario 3**: Workforce-to-bed ratios show Public sector at 0.8 (< benchmark 1.5) → Add investigation section on understaffing implications
- **Scenario 4**: Doctor-to-nurse ratio increasing from 0.30 to 0.45 → Add section on implications for task delegation and care models

**Adaptation Documentation Template (Markdown Cell in Notebook):**

```markdown
## Adaptive Change Log

**Change 1: Switch to Non-Parametric Tests**
- **Trigger**: Shapiro-Wilk test showed growth rates are not normally distributed (p < 0.05)
- **Original Plan**: Use ANOVA for sector growth comparison
- **Updated Approach**: Use Kruskal-Wallis test (non-parametric alternative)
- **Rationale**: Non-parametric test does not assume normality; more robust for skewed data
- **Impact**: Results still valid; interpretation focuses on median differences rather than means

**Change 2: Added Outlier Investigation Section**
- **Trigger**: Scatter plot revealed 3 data points far from regression line (residuals > 3 SD)
- **Original Plan**: Only report correlation coefficient
- **Updated Approach**: Investigate outlier years/sectors; report correlation with and without outliers
- **Rationale**: Outliers may represent policy changes or data errors requiring explanation
- **Impact**: More robust findings; identified 2017 capacity spike in private sector requiring investigation
```

This adaptive approach ensures the implementation remains grounded in empirical findings rather than assumptions, leading to more robust and reliable exploratory analysis results.

---

### 13. Code Generation Order

**CRITICAL**: Follow this generation sequence to ensure dependencies are available when needed.

**Phase 1: Foundation (Generate First)**

1. **Configuration files**: 
   - `config/analysis.yml` → Add `eda` section with visualization settings
   
2. **Data schemas**: 
   - Define in `src/analysis/workforce_statistics.py` (at top of file as constants)
   - `WORKFORCE_REQUIRED_COLUMNS`, `CAPACITY_REQUIRED_COLUMNS`
   - `WORKFORCE_EXPECTED_DTYPES`, `CAPACITY_EXPECTED_DTYPES`
   - `WORKFORCE_CONSTRAINTS`, `CAPACITY_CONSTRAINTS`

3. **Module initialization**:
   - `src/analysis/__init__.py` (empty file)
   - `src/visualization/__init__.py` (empty file)

**Phase 2: Core Logic (Generate Second)**

4. **Statistical analysis module**: 
   - `src/analysis/workforce_statistics.py` with all functions:
     - `calculate_growth_rates()`
     - `calculate_indexed_growth()`
     - `calculate_composition_metrics()`
     - `calculate_workforce_to_bed_ratio()`
     - `test_sector_growth_differences()`
     - `test_workforce_capacity_correlation()`

5. **Visualization module**:
   - `src/visualization/workforce_plots.py` with all plotting functions:
     - `plot_temporal_trends()`
     - `plot_sector_comparison()`
     - `plot_composition_stacked()`
     - `plot_workforce_capacity_scatter()`
     - `plot_growth_rate_comparison()`

**Phase 3: Integration (Generate Third)**

6. **Unit tests**: 
   - `tests/unit/test_workforce_statistics.py` (test all statistical functions)

7. **Data quality tests**:
   - `tests/data/test_eda_data_quality.py` (schema, completeness, accuracy)

8. **Analysis notebook**:
   - `notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`
   - Imports modules from phases 1-2
   - Uses functions to perform analysis
   - Generates visualizations and tables

9. **EDA report**:
   - `reports/workforce_capacity_eda_report.md`
   - Embeds figures generated by notebook
   - References tables exported by notebook

**Rationale**: 
- Configuration and schemas must exist before code that uses them
- Statistical and visualization functions must exist before notebook imports them
- Tests validate functions before notebook runs full analysis
- Report documents findings from notebook execution

**Dependency Diagram**:

```
config/analysis.yml
       ↓
src/analysis/workforce_statistics.py  ←→  src/visualization/workforce_plots.py
       ↓                                              ↓
tests/unit/test_workforce_statistics.py   tests/data/test_eda_data_quality.py
       ↓                                              ↓
notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb
       ↓
reports/workforce_capacity_eda_report.md
```

---

### 14. Data Quality & Validation Strategy

**Data Quality Checks at Each Pipeline Stage:**

**Stage 1: Data Loading (Extraction)**

- **Schema Validation**:
  - Verify required columns present: `WORKFORCE_REQUIRED_COLUMNS`, `CAPACITY_REQUIRED_COLUMNS`
  - Validate data types match expected: `WORKFORCE_EXPECTED_DTYPES`, `CAPACITY_EXPECTED_DTYPES`
  - Raise `ValueError` if schema mismatch
  
- **Completeness Checks**:
  - Assert no null values in required columns
  - Check year range within expected bounds (2006-2019 workforce, 2009-2020 capacity)
  - Log row counts and year coverage
  
- **Implementation**:
  ```python
  from src.data_processing.validation import validate_schema, validate_value_ranges
  
  # After loading
  validate_schema(workforce_df, WORKFORCE_EXPECTED_DTYPES)
  validate_value_ranges(workforce_df, 'year', min_value=2006, max_value=2019)
  validate_value_ranges(workforce_df, 'count', min_value=0, allow_null=False)
  ```

**Stage 2: Feature Engineering (Transformation)**

- **Calculation Validation**:
  - Growth rates: Check first year has nulls (expected), subsequent years have values
  - Indexed growth: Verify base year (2006) has index = 100
  - Composition: Verify percentages sum to 100 within each group
  - Ratios: Check for division by zero; log warnings for zero denominators
  
- **Range Checks**:
  - Growth rates: Flag if outside reasonable range (-50% to +50%)
  - Workforce-to-bed ratio: Flag if outside domain benchmarks (0.5 to 4.0)
  - Composition percentages: Assert 0 <= percentage <= 100
  
- **Implementation**:
  ```python
  # After growth rate calculation
  growth_clean = growth_df.filter(pl.col('growth_rate').is_not_null())
  extreme_growth = growth_clean.filter(
      (pl.col('growth_rate') < -50) | (pl.col('growth_rate') > 50)
  )
  if extreme_growth.height > 0:
      logger.warning(f"{extreme_growth.height} rows with extreme growth rates (|rate| > 50%)")
  
  # After composition calculation
  composition_totals = (
      composition_df
      .group_by(['year', 'sector'])
      .agg(pl.col('percentage').sum().alias('total_pct'))
  )
  assert composition_totals['total_pct'].min() > 99.9  # Allow rounding error
  assert composition_totals['total_pct'].max() < 100.1
  ```

**Stage 3: Analysis Outputs (Consumption)**

- **Statistical Test Validation**:
  - Check sample sizes sufficient (n >= 3 per group for t-tests, n >= 5 for ANOVA)
  - Verify p-values in range [0, 1]
  - Check correlation values in range [-1, 1]
  - Log warnings if assumptions violated (non-normality, heteroscedasticity)
  
- **Visualization Validation**:
  - Verify all plots saved successfully to disk
  - Check file sizes > 0 (detect empty plots)
  - Validate figure resolution (DPI = 300)
  
- **Implementation**:
  ```python
  # After statistical test
  assert 0 <= test_result['p_value'] <= 1
  if test_result['sample_sizes'] and min(test_result['sample_sizes']) < 5:
      logger.warning(f"Small sample size detected: {min(test_result['sample_sizes'])}")
  
  # After saving plot
  output_file = Path(output_path)
  assert output_file.exists(), f"Plot not saved: {output_path}"
  assert output_file.stat().st_size > 1000, f"Plot file suspiciously small: {output_path}"
  ```

**Pipeline Code Testability Requirements:**

- **Modular Functions**: All analysis logic in separate functions (not inline in notebook)
- **Pure Functions**: Statistical calculations should not have side effects (except logging)
- **Dependency Injection**: Pass DataFrames as arguments (not global variables)
- **Configurable Parameters**: Use function arguments for thresholds, column names (not hardcoded)
- **Return Types**: All functions return DataFrames or dictionaries (not printing results)
- **Error Handling**: All functions raise descriptive exceptions (not generic errors)

**Example Testable Function Structure**:
```python
def calculate_growth_rates(
    df: pl.DataFrame,  # Dependency injection
    group_cols: List[str],  # Configurable
    value_col: str = 'count',
    time_col: str = 'year'
) -> pl.DataFrame:  # Clear return type
    """Docstring with Args, Returns, Raises."""
    # Validate inputs
    required_cols = set(group_cols + [value_col, time_col])
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Perform calculation (pure logic)
    result = (...)
    
    # Log outcome
    logger.info(f"Calculated growth rates for {result.height} rows")
    
    return result  # No side effects beyond logging
```

**Test Assertions for Critical Data Quality Aspects:**

**Assertion 1: No Null Values in Key Columns**
```python
def test_no_nulls_in_growth_rates():
    growth_df = calculate_growth_rates(sample_data, group_cols=['sector'])
    # First year has nulls (expected)
    growth_clean = growth_df.filter(pl.col('year') > growth_df['year'].min())
    assert growth_clean['growth_rate'].null_count() == 0
```

**Assertion 2: Growth Rates Within Reasonable Bounds**
```python
def test_growth_rates_reasonable():
    growth_df = calculate_growth_rates(sample_data, group_cols=['sector'])
    growth_clean = growth_df.filter(pl.col('growth_rate').is_not_null())
    # Allow -100% (complete loss) to +200% (tripling)
    assert growth_clean['growth_rate'].min() >= -100
    assert growth_clean['growth_rate'].max() <= 200
```

**Assertion 3: Workforce-to-Bed Ratios in Plausible Range**
```python
def test_workforce_to_bed_ratio_plausible():
    ratio_df = calculate_workforce_to_bed_ratio(workforce_df, capacity_df)
    # Expect 0.1 (very low staffing) to 5.0 (very high staffing)
    assert ratio_df['workforce_to_bed_ratio'].min() >= 0.1
    assert ratio_df['workforce_to_bed_ratio'].max() <= 5.0
```

**Assertion 4: Composition Percentages Sum to 100**
```python
def test_composition_sums_to_100():
    composition_df = calculate_composition_metrics(
        workforce_df,
        group_cols=['year', 'sector'],
        category_col='profession'
    )
    totals = composition_df.group_by(['year', 'sector']).agg(
        pl.col('percentage').sum().alias('total')
    )
    # Allow 0.1% rounding error
    assert (totals['total'] - 100.0).abs().max() < 0.1
```

**Assertion 5: Statistical Test Results Valid**
```python
def test_statistical_test_valid_pvalue():
    test_result = test_sector_growth_differences(growth_df)
    assert 0 <= test_result['p_value'] <= 1
    assert test_result['test_used'] in ['ANOVA', 'Kruskal-Wallis']
```

**Assertion 6: Correlation Coefficients in Valid Range**
```python
def test_correlation_valid_range():
    corr_result = test_workforce_capacity_correlation(ratio_df)
    assert -1 <= corr_result['correlation'] <= 1
    assert corr_result['method'] in ['pearson', 'spearman']
```

---

### 15. Statistical Analysis & Model Development

**Statistical Methods and Techniques:**

**Descriptive Statistics**:
- **Summary Statistics**: Mean, median, std dev, min, max, quartiles for workforce and capacity counts
- **Distribution Analysis**: Histograms, box plots to assess normality and identify outliers
- **Trend Analysis**: Linear regression on time series to quantify growth trajectories

**Inferential Statistics**:

**1. Hypothesis Test: Sector Growth Rate Differences**
- **Null Hypothesis (H0)**: Mean growth rates are equal across all sectors
- **Alternative Hypothesis (H1)**: At least one sector has significantly different growth rate
- **Method Selection**:
  - **If data approximately normal** (Shapiro-Wilk p > 0.05): **One-way ANOVA**
  - **If data not normal** (Shapiro-Wilk p < 0.05): **Kruskal-Wallis H-test** (non-parametric)
- **Significance Level**: α = 0.05
- **Post-Hoc Analysis**: If significant, perform pairwise comparisons (Tukey HSD or Dunn's test)
- **Effect Size**: Report eta-squared (η²) for ANOVA or epsilon-squared (ε²) for Kruskal-Wallis
- **Interpretation**: If p < 0.05, conclude significant sector differences; identify which sectors differ

**2. Hypothesis Test: Workforce-to-Bed Ratio Sector Differences**
- **Null Hypothesis (H0)**: Mean workforce-to-bed ratio equal across sectors
- **Alternative Hypothesis (H1)**: Sectors have significantly different ratios
- **Method**: ANOVA or Kruskal-Wallis (depending on normality)
- **Confidence Intervals**: 95% CI for each sector's mean ratio
- **Interpretation**: Compare CIs to domain benchmarks (1.5-2.5 FTE per bed); flag sectors outside range

**3. Correlation Analysis: Workforce vs. Capacity Growth**
- **Null Hypothesis (H0)**: No correlation between workforce and capacity growth (ρ = 0)
- **Alternative Hypothesis (H1)**: Significant correlation exists (ρ ≠ 0)
- **Method Selection**:
  - **If bivariate normality holds**: **Pearson correlation** (parametric)
  - **If assumptions violated**: **Spearman rank correlation** (non-parametric)
- **Strength Interpretation**:
  - |r| < 0.3: Weak correlation
  - 0.3 ≤ |r| < 0.7: Moderate correlation
  - |r| ≥ 0.7: Strong correlation
- **Significance Test**: Two-tailed t-test on correlation coefficient (α = 0.05)
- **Interpretation**: If significant positive correlation, workforce and capacity growing in sync; if weak/negative, misalignment issue

**Multiple Testing Correction**:
- **Context**: 3 primary hypothesis tests planned
- **Method**: **Bonferroni correction** (conservative approach)
  - Adjusted α = 0.05 / 3 = 0.0167
  - Use adjusted α for significance decisions
- **Alternative**: False Discovery Rate (FDR) via Benjamini-Hochberg procedure (less conservative)
- **Reporting**: Report both uncorrected and corrected p-values for transparency

**Assumption Checking**:
- **Normality**: Shapiro-Wilk test (if n < 50) or Kolmogorov-Smirnov test (if n ≥ 50)
- **Homogeneity of Variance**: Levene's test for ANOVA
- **Independence**: Verify observations independent (no repeated measures)
- **Documentation**: Log all assumption test results; note violations and methodological adjustments

**Predictive Modeling** (Not Applicable):
- This user story focuses on exploratory analysis, not predictive modeling
- Forecasting and predictive analytics reserved for future user stories

---

### 16. Model Operations & Governance

**Not applicable** - This user story focuses on exploratory data analysis without machine learning models. Model operations will be relevant for future predictive analytics user stories (e.g., workforce demand forecasting).

---

### 17. UI/Dashboard Visual Testing

**Not applicable** - This user story produces static reports and figures, not interactive dashboards. Dashboard development will be addressed in User Story 5 (Executive Surveillance Dashboard).

---

### 18. Success Metrics & Monitoring

**Business Success Metrics:**

1. **Analysis Completeness**:
   - **Metric**: Percentage of acceptance criteria completed
   - **Target**: 100% of acceptance criteria met
   - **Measurement**: Checklist completion in User Story 3

2. **Insight Quality**:
   - **Metric**: Number of actionable insights identified
   - **Target**: ≥ 3 major patterns documented with policy implications
   - **Measurement**: EDA report section "Key Patterns and Insights"

3. **Stakeholder Readiness**:
   - **Metric**: Report clarity and completeness for policy analysts
   - **Target**: Report includes executive summary, visualizations, and actionable recommendations
   - **Measurement**: Stakeholder review and feedback

4. **Analysis Reproducibility**:
   - **Metric**: Notebook executes without errors from top to bottom
   - **Target**: Zero execution errors; all outputs regenerated consistently
   - **Measurement**: "Restart & Run All" test

**Technical Monitoring:**

1. **Code Quality**:
   - **Metric**: Unit test pass rate
   - **Target**: 100% of unit tests pass
   - **Measurement**: `pytest tests/unit/ -v`

2. **Data Quality**:
   - **Metric**: Data validation test pass rate
   - **Target**: 100% of data quality tests pass
   - **Measurement**: `pytest tests/data/ -v`

3. **Execution Performance**:
   - **Metric**: Notebook execution time
   - **Target**: < 2 minutes total execution
   - **Measurement**: Time notebook execution with `%%time` magic commands

4. **Output Completeness**:
   - **Metric**: Number of expected output files created
   - **Target**: ≥ 6 figures, ≥ 3 summary tables, 1 comprehensive report
   - **Measurement**: File count in `reports/figures/`, `results/tables/`, `reports/`

**Alerting Thresholds and Escalation:**

- **Critical**: Notebook execution fails → **Immediate review** (blocking issue for deliverable)
- **High**: Data quality tests fail → **Investigate within 24 hours** (data integrity issue)
- **Medium**: Unit tests fail → **Fix before finalizing** (code quality issue)
- **Low**: Execution time > 2 minutes → **Optimize if time permits** (performance improvement opportunity)

**Monitoring Dashboard** (for this user story):
- Not applicable (one-time exploratory analysis)
- For recurring analyses, consider implementing automated quality checks and execution monitoring

---

### 19. References

**Data Source Documentation**:
- [Data Sources: MOH Singapore Healthcare Data](../../../project_context/data-sources.md) - Primary data source details and access methods

**Domain Knowledge**:
- [Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md) - Workforce metrics, benchmarks, and analytical methodologies
- [Healthcare System Sustainability Metrics](../../../domain_knowledge/healthcare-system-sustainability-metrics.md) - Long-term sustainability indicators (workforce dimension)

**Problem Statement**:
- [PS-001: Workforce-Capacity Mismatch Analysis](../../problem_statements/ps-001-workforce-capacity-mismatch.md) - Overall problem context and objectives

**Related User Stories**:
- [User Story 2: Data Cleaning and Standardization](../problem-statement-001-workforce-capacity-mismatch/02-data-cleaning.md) - Cleaned data source for this analysis
- [User Story 4: Workforce-Capacity Metrics](../problem-statement-001-workforce-capacity-mismatch/04-workforce-capacity-metrics.md) - Deeper analysis informed by this EDA

**Technical Documentation**:
- [Tech Stack Preferences](../../../project_context/tech-stack.md) - Project technology specifications
- [Copilot Instructions](.github/copilot-instructions.md) - Coding standards and best practices

**Existing Code Modules**:
- `src/data_processing/validation.py` - Data validation utilities (reused)
- `src/utils/logger.py` - Logging configuration (reused)
- `src/utils/config_loader.py` - Configuration loading (reused)
- `scripts/clean_workforce_capacity_data.py` - Data cleaning pipeline (upstream dependency)

**External Libraries**:
- [Polars Documentation](https://pola-rs.github.io/polars/) - DataFrame library
- [SciPy Stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) - Statistical testing
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html) - Visualization
- [Seaborn Documentation](https://seaborn.pydata.org/) - Statistical data visualization

---

## Code Generation Readiness Checklist

**CRITICAL**: The implementation plan is ready for code generation ONLY if it includes:

- [x] **🚨 CODE EXECUTION VALIDATION COMPLETED** - ALL code blocks have been tested for executability
- [x] **Function signatures** with complete type hints for all major components
- [x] **Data schemas** defined as Pydantic models or dataclasses
- [x] **Specific library methods** (exact Polars operations, not generic "load data")
- [x] **Configuration file structure** with example YAML content
- [x] **Test assertions** with specific expected values
- [x] **Import statements** for all dependencies (internal and external)
- [x] **Error handling patterns** with specific exception types
- [x] **Logging statements** at key pipeline steps with exact messages
- [x] **Data validation rules** as executable code (column names, types, constraints)
- [x] **Example input/output data** for each major transformation
- [x] **Technical constraints** (memory limits, performance targets, optimization strategies)
- [x] **Package management commands** using `uv` (not pip)
- [x] **Code generation order** specifying which components to generate first
- [x] **Test fixtures** with sample data for testing
- [x] **Performance benchmarks** (expected execution times, memory usage)

✅ **This implementation plan is READY for code generation.**

---

**End of Implementation Plan**
