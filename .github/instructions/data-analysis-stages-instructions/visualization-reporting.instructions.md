---
name: 'Visualization and Reporting Standards'
description: 'Best practices for creating effective visualizations, dashboards, and stakeholder reports'
applyTo: 'src/visualization/**, reports/figures/**, reports/dashboards/**, reports/presentations/**, notebooks/**/*, results/exports/**, docs/objectives/user_stories/**/*visual*.md'
---

## Purpose
This document defines **mandatory standards** for data visualization and reporting. Apply these practices to create clear, accurate, and actionable visualizations for technical and non-technical audiences.

## Core Principles

### 1. Clarity Over Complexity
- **ALWAYS prioritize readability** over visual sophistication
- Use simple chart types when they convey the message effectively
- Avoid 3D charts, excessive colors, and unnecessary decorations
- Include clear titles, axis labels, and legends

### 2. Audience-Appropriate Design
- **Technical reports**: Include details, methodology, statistical measures
- **Executive dashboards**: Focus on KPIs, trends, and actionable insights
- **Public communication**: Simple visualizations with minimal jargon
- Document assumptions and limitations

### 3. Reproducible Visualizations
- Use code-based visualization (not manual editing)
- Save plotting functions for reuse
- Version control visualization code
- Document data sources and calculation methods

## Visualization Standards

### Chart Type Selection Guide

```python
# src/visualization/chart_selection.py
"""
Chart Type Selection Guide
===========================

Time Series Data:
- Line chart: Trends over time
- Area chart: Cumulative or stacked trends
- Seasonal plot: Patterns by season/month

Comparisons:
- Bar chart: Comparing categories
- Grouped bar: Comparing multiple series across categories
- Horizontal bar: Long category names or rankings

Distributions:
- Histogram: Frequency distribution
- Box plot: Summary statistics and outliers
- Violin plot: Distribution shape and density

Relationships:
- Scatter plot: Correlation between variables
- Heatmap: Correlation matrix or intensity patterns

Proportions:
- Pie chart: AVOID (use bar chart instead)
- Stacked bar: Part-to-whole relationships
- Tree map: Hierarchical proportions

Geospatial:
- Choropleth map: Regional comparisons
- Point map: Location-based data
"""
```

### Standard Plotting Functions

```python
# src/visualization/plotting.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import numpy as np
from typing import Optional, List, Tuple, Dict, Any
from pathlib import Path
from loguru import logger

# Set consistent style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Standard figure size
DEFAULT_FIGSIZE = (12, 6)

# Color palette for diseases (consistent across all visualizations)
DISEASE_COLORS = {
    'Dengue Fever': '#e74c3c',
    'Hand, Foot and Mouth Disease': '#3498db',
    'Influenza': '#2ecc71',
    'COVID-19': '#9b59b6',
    'Tuberculosis': '#f39c12',
    'Chickenpox': '#1abc9c',
}


def setup_plot_style(
    style: str = 'seaborn-v0_8-darkgrid',
    context: str = 'notebook',
    font_scale: float = 1.0
) -> None:
    """Configure consistent plotting style.
    
    Args:
        style: Matplotlib style
        context: Seaborn context ('paper', 'notebook', 'talk', 'poster')
        font_scale: Font size scaling factor
    """
    plt.style.use(style)
    sns.set_context(context, font_scale=font_scale)
    
    # Set default figure parameters
    plt.rcParams['figure.figsize'] = DEFAULT_FIGSIZE
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9


def plot_time_series(
    df: pl.DataFrame,
    x_col: str,
    y_col: str,
    group_by: Optional[str] = None,
    title: str = 'Time Series Plot',
    xlabel: str = 'Date',
    ylabel: str = 'Value',
    figsize: Tuple[int, int] = DEFAULT_FIGSIZE,
    save_path: Optional[str] = None,
    show_legend: bool = True
) -> plt.Figure:
    """Create a time series line plot.
    
    Args:
        df: DataFrame with time series data
        x_col: Column name for x-axis (time)
        y_col: Column name for y-axis (values)
        group_by: Column name for grouping (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height)
        save_path: Path to save figure (optional)
        show_legend: Whether to show legend
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> plot_time_series(
        ...     df,
        ...     x_col='date',
        ...     y_col='case_count',
        ...     group_by='disease',
        ...     title='Weekly Disease Cases',
        ...     save_path='reports/figures/time_series.png'
        ... )
    """
    logger.info(f"Creating time series plot: {title}")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if group_by:
        # Plot multiple series
        groups = df[group_by].unique().to_list()
        for group in groups:
            group_df = df.filter(pl.col(group_by) == group)
            color = DISEASE_COLORS.get(group, None)
            
            ax.plot(
                group_df[x_col].to_numpy(),
                group_df[y_col].to_numpy(),
                label=group,
                linewidth=2,
                marker='o',
                markersize=3,
                alpha=0.7,
                color=color
            )
    else:
        # Single series
        ax.plot(
            df[x_col].to_numpy(),
            df[y_col].to_numpy(),
            linewidth=2,
            marker='o',
            markersize=3,
            alpha=0.7,
            color='steelblue'
        )
    
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, linestyle='--')
    
    if show_legend and group_by:
        ax.legend(loc='best', frameon=True, shadow=True)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig


def plot_seasonal_pattern(
    df: pl.DataFrame,
    time_col: str,
    value_col: str,
    group_by: str,
    period: str = 'month',
    title: str = 'Seasonal Pattern',
    figsize: Tuple[int, int] = (14, 8),
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create seasonal pattern visualization.
    
    Args:
        df: DataFrame with time series data
        time_col: Date/time column name
        value_col: Value column name
        group_by: Grouping column (e.g., 'disease')
        period: 'month' or 'week' for seasonal period
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
        
    Returns:
        Matplotlib Figure object
    """
    logger.info(f"Creating seasonal pattern plot for {period}")
    
    # Extract period
    if period == 'month':
        df = df.with_columns(
            pl.col(time_col).dt.month().alias('period')
        )
        period_label = 'Month'
        period_range = range(1, 13)
    elif period == 'week':
        df = df.with_columns(
            pl.col(time_col).dt.week().alias('period')
        )
        period_label = 'Week'
        period_range = range(1, 54)
    
    # Calculate average by period and group
    seasonal_data = df.group_by(['period', group_by]).agg([
        pl.col(value_col).mean().alias('avg_value'),
        pl.col(value_col).std().alias('std_value')
    ]).sort(['period', group_by])
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each group
    groups = df[group_by].unique().to_list()
    for group in groups[:8]:  # Limit to top 8 for clarity
        group_data = seasonal_data.filter(pl.col(group_by) == group)
        periods = group_data['period'].to_numpy()
        values = group_data['avg_value'].to_numpy()
        
        color = DISEASE_COLORS.get(group, None)
        ax.plot(
            periods,
            values,
            label=group,
            linewidth=2.5,
            marker='o',
            markersize=5,
            alpha=0.7,
            color=color
        )
    
    ax.set_xlabel(period_label, fontsize=12)
    ax.set_ylabel(f'Average {value_col}', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True, ncol=2)
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_xlim(min(period_range), max(period_range))
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig


def plot_forecast_comparison(
    actual: np.ndarray,
    forecasts: Dict[str, np.ndarray],
    dates: Optional[np.ndarray] = None,
    title: str = 'Forecast Comparison',
    ylabel: str = 'Cases',
    figsize: Tuple[int, int] = (14, 8),
    save_path: Optional[str] = None
) -> plt.Figure:
    """Compare multiple forecast methods against actuals.
    
    Args:
        actual: Actual values
        forecasts: Dictionary of {method_name: forecast_array}
        dates: Date indices (optional)
        title: Plot title
        ylabel: Y-axis label
        figsize: Figure size
        save_path: Path to save figure
        
    Returns:
        Matplotlib Figure object
    """
    logger.info(f"Creating forecast comparison plot with {len(forecasts)} methods")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    x = dates if dates is not None else np.arange(len(actual))
    
    # Plot actual
    ax.plot(x, actual, label='Actual', linewidth=3, color='black', alpha=0.8, zorder=10)
    
    # Plot forecasts
    colors = plt.cm.tab10(np.linspace(0, 1, len(forecasts)))
    for (method, forecast), color in zip(forecasts.items(), colors):
        ax.plot(
            x,
            forecast,
            label=method,
            linewidth=2,
            alpha=0.7,
            linestyle='--',
            color=color
        )
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True)
    ax.grid(alpha=0.3, linestyle='--')
    
    if dates is not None:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {save_path}")
    
    return fig


def create_interactive_dashboard(
    df: pl.DataFrame,
    title: str = 'Disease Surveillance Dashboard',
    output_path: str = 'reports/dashboards/surveillance_dashboard.html'
) -> None:
    """Create interactive Plotly dashboard.
    
    Args:
        df: DataFrame with disease surveillance data
        title: Dashboard title
        output_path: Path to save HTML dashboard
    """
    logger.info(f"Creating interactive dashboard: {title}")
    
    from plotly.subplots import make_subplots
    
    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            'Weekly Cases by Disease',
            'Total Cases by Disease',
            'Seasonal Pattern',
            'Growth Rate'
        ),
        specs=[
            [{"type": "scatter"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "scatter"}]
        ]
    )
    
    # Subplot 1: Time series
    diseases = df['disease'].unique().to_list()
    for disease in diseases[:5]:  # Top 5
        disease_df = df.filter(pl.col('disease') == disease)
        fig.add_trace(
            go.Scatter(
                x=disease_df['reporting_date'].to_list(),
                y=disease_df['case_count'].to_list(),
                name=disease,
                mode='lines',
                line=dict(width=2)
            ),
            row=1,
            col=1
        )
    
    # Subplot 2: Total cases bar chart
    totals = df.group_by('disease').agg([
        pl.col('case_count').sum().alias('total_cases')
    ]).sort('total_cases', descending=True).head(10)
    
    fig.add_trace(
        go.Bar(
            x=totals['disease'].to_list(),
            y=totals['total_cases'].to_list(),
            marker_color='steelblue'
        ),
        row=1,
        col=2
    )
    
    # Subplot 3: Seasonal pattern (month)
    df = df.with_columns(
        pl.col('reporting_date').dt.month().alias('month')
    )
    
    seasonal = df.group_by(['month', 'disease']).agg([
        pl.col('case_count').mean().alias('avg_cases')
    ])
    
    for disease in diseases[:5]:
        disease_seasonal = seasonal.filter(pl.col('disease') == disease)
        fig.add_trace(
            go.Scatter(
                x=disease_seasonal['month'].to_list(),
                y=disease_seasonal['avg_cases'].to_list(),
                name=disease,
                mode='lines+markers',
                showlegend=False
            ),
            row=2,
            col=1
        )
    
    # Update layout
    fig.update_layout(
        height=800,
        title_text=title,
        title_font_size=18,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Save to HTML
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path)
    logger.info(f"Dashboard saved to {output_path}")
```

### Publication-Quality Figures

```python
# src/visualization/publication_figures.py
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple
from pathlib import Path
from loguru import logger

def create_publication_figure(
    plot_function: callable,
    title: str,
    output_prefix: str,
    formats: List[str] = ['png', 'pdf', 'svg'],
    dpi: int = 300,
    **plot_kwargs
) -> None:
    """Create publication-quality figure in multiple formats.
    
    Args:
        plot_function: Function that creates the plot
        title: Figure title
        output_prefix: Path prefix for saved files (without extension)
        formats: List of output formats
        dpi: Resolution for raster formats
        **plot_kwargs: Additional arguments for plot_function
    """
    logger.info(f"Creating publication figure: {title}")
    
    # Set publication style
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    
    # Create figure
    fig = plot_function(**plot_kwargs)
    
    # Save in multiple formats
    for fmt in formats:
        output_path = f"{output_prefix}.{fmt}"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if fmt in ['png', 'jpg']:
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight', format=fmt)
        else:
            plt.savefig(output_path, bbox_inches='tight', format=fmt)
        
        logger.info(f"Saved {fmt.upper()} to {output_path}")
    
    plt.close(fig)
```

## Report Templates

### Executive Summary Template

```markdown
# Disease Surveillance Analysis Report

**Report Date**: [DATE]  
**Reporting Period**: [START DATE] to [END DATE]  
**Prepared by**: [ANALYST NAME]

---

## Executive Summary

[2-3 sentence overview of key findings]

### Key Findings

1. **[Finding 1 Title]**: [Brief description with key metric]
2. **[Finding 2 Title]**: [Brief description with key metric]
3. **[Finding 3 Title]**: [Brief description with key metric]

### Recommendations

- **Immediate Actions**: [List urgent recommendations]
- **Medium-term Priorities**: [Strategic recommendations]

---

## 1. Surveillance Overview

### 1.1 Data Summary
- Total cases reported: [NUMBER]
- Diseases monitored: [NUMBER]
- Reporting facilities: [NUMBER]
- Data completeness: [PERCENTAGE]%

### 1.2 Temporal Coverage
![Time Series Overview](figures/time_series_overview.png)

---

## 2. Disease Burden Analysis

### 2.1 Top Diseases by Case Count

| Rank | Disease | Total Cases | % of Total | Change vs Previous Period |
|------|---------|-------------|------------|---------------------------|
| 1 | [Disease] | [Number] | [%] | [±%] |
| 2 | ... | ... | ... | ... |

### 2.2 Trend Analysis
![Disease Trends](figures/disease_trends.png)

**Interpretation**: [Describe trends and their significance]

---

## 3. Seasonal Patterns

### 3.1 Monthly Variation
![Seasonal Patterns](figures/seasonal_patterns.png)

**Key Observations**:
- [Disease X] shows peak in [months]
- [Disease Y] exhibits bimodal pattern
- [Other notable patterns]

---

## 4. Outbreak Detection

### 4.1 Alert Summary
- Active outbreaks: [NUMBER]
- Diseases on watch list: [LIST]
- Geographic hotspots: [LOCATIONS]

### 4.2 Outbreak Timeline
![Outbreak Events](figures/outbreak_timeline.png)

---

## 5. Forecasts and Predictions

### 5.1 4-Week Forecast
![Forecast Chart](figures/forecast_4week.png)

| Disease | Current Week | Forecast Week +4 | Confidence Interval |
|---------|--------------|------------------|---------------------|
| [Disease] | [Number] | [Number] | [Lower - Upper] |

### 5.2 Model Performance
- Forecast accuracy (MAPE): [%]
- Model: [Model type and version]
- Last updated: [Date]

---

## 6. Data Quality Notes

- **Completeness**: [Percentage] of expected reports received
- **Timeliness**: [Percentage] reported within deadline
- **Known Issues**: [List any data quality concerns]

---

## 7. Methodology

### Data Sources
- Primary: [Source name and description]
- External: [List external data sources]

### Analysis Methods
- Statistical tests: [List tests used]
- Forecasting model: [Model description]
- Thresholds: [Outbreak thresholds and rationale]

---

## Appendices

### A. Technical Details
[Link to technical documentation]

### B. Data Dictionary
[Link to data dictionary]

### C. Change Log
- [Date]: [Description of changes]
```

## Dashboard Design Principles

### 1. Information Hierarchy
```
┌─────────────────────────────────────────────────┐
│  HEADER: Title, Date, Key Metrics Summary       │
├─────────────────────────────────────────────────┤
│  PRIMARY VISUALIZATION                          │
│  (Main insight, largest chart)                  │
├──────────────────┬──────────────────────────────┤
│  SUPPORTING VIZ  │  SUPPORTING VIZ              │
│  (Details)       │  (Comparisons)               │
├──────────────────┴──────────────────────────────┤
│  FILTERS AND CONTROLS                           │
└─────────────────────────────────────────────────┘
```

### 2. Color Usage
- **Limit palette**: Use 3-5 colors maximum
- **Consistent mapping**: Same disease = same color across all charts
- **Accessibility**: Ensure color-blind safe palettes
- **Emphasis**: Use color to highlight key data, not decoration

### 3. Interactivity
- Tooltips for detailed information
- Filters for time period, disease, region
- Drill-down capabilities
- Export functionality

## Anti-Patterns (AVOID)

```python
# ❌ DON'T: Poor labeling and formatting
plt.plot(x, y)
plt.show()  # No title, labels, or save

# ✅ DO: Complete, professional visualization
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(x, y, linewidth=2, color='steelblue', label='Case Count')
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Number of Cases', fontsize=11)
ax.set_title('Weekly Disease Cases Over Time', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('reports/figures/weekly_cases.png', dpi=300, bbox_inches='tight')

# ❌ DON'T: 3D pie chart (hard to read, misleading)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.pie3d(...)  # Never do this

# ✅ DO: Simple bar chart (clear, accurate)
fig, ax = plt.subplots()
ax.barh(categories, values)
ax.set_xlabel('Case Count')
ax.set_title('Cases by Disease')

# ❌ DON'T: Too many colors, no legend
for i, disease in enumerate(diseases):
    plt.plot(data[disease], color=np.random.rand(3,))

# ✅ DO: Consistent colors with clear legend
for disease in diseases:
    color = DISEASE_COLORS.get(disease, None)
    plt.plot(data[disease], label=disease, color=color, linewidth=2)
plt.legend()
```

## Checklist

Before sharing visualizations or reports:

- [ ] **Clear title**: Describes what is being shown
- [ ] **Axis labels**: Both axes labeled with units
- [ ] **Legend**: Included when multiple series shown
- [ ] **Appropriate chart type**: Best visualization for data type
- [ ] **Color scheme**: Consistent and accessible
- [ ] **High resolution**: Saved at 300 DPI minimum
- [ ] **Data source noted**: Source and date documented
- [ ] **Assumptions stated**: Any caveats or limitations mentioned
- [ ] **Reproducible**: Code saved and version controlled
- [ ] **Audience-appropriate**: Complexity matches audience expertise
- [ ] **Actionable insights**: Clear takeaways highlighted

## Summary

Effective visualization requires:
1. **Choose the right chart** for your data and message
2. **Design for your audience** - technical vs executive vs public
3. **Maintain consistency** in colors, styles, and formatting
4. **Prioritize clarity** over visual complexity
5. **Document everything** - sources, methods, assumptions
6. **Make it reproducible** - code-based, version controlled
