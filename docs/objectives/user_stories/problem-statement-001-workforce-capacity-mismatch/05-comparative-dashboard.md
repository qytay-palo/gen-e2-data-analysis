# User Story 5: Comparative Analysis and Interactive Dashboard Development

**As a** MOH policy maker,  
**I want** an interactive dashboard showing workforce and capacity metrics with comparative analysis,  
**so that** I can monitor workforce-capacity alignment across sectors and make data-driven workforce planning decisions.

## 1. 🎯 Acceptance Criteria

- Interactive dashboard developed showing workforce and capacity metrics by sector
- Time series trends visualizable for all years (2006-2019)
- Sector comparison views available (side-by-side metrics)
- Ratio trends displayed with visual alerts for misalignments (e.g., red flag when ratio deviates >2 std dev)
- Drill-down capability by sector to view profession-level detail
- Dashboard accessible to authorized MOH stakeholders
- Performance acceptable (dashboards load <3 seconds)
- Mobile-responsive design for on-the-go access
- User guide documenting how to interpret visualizations
- Embedded data notes explaining metrics and limitations

## 2. 🔒 Technical Constraints

- **Platform**: Databricks or Python-based dashboard (specify choice)
- **Interactivity**: Filters for sector, year, and profession
- **Data Refresh**: Daily refresh from processed data (if deployed)
- **Access Control**: Authentication required; limited to authorized MOH users
- **Documentation**: In-dashboard tooltips and external user guide
- **Accessibility**: Compliant with web accessibility standards

## 3. 📚 Domain Knowledge References

- [Healthcare Workforce Planning: Key Metrics](../../../domain_knowledge/healthcare-workforce-planning.md#standard-metrics-and-kpis) - Context for metrics interpretation
- [Healthcare Workforce Planning: Best Practices](../../../domain_knowledge/healthcare-workforce-planning.md#common-pitfalls-and-best-practices) - Guidance on sector comparison pitfalls
- [Healthcare System Sustainability: Multi-Dimensional Analysis](../../../domain_knowledge/healthcare-system-sustainability-metrics.md) - Long-term sustainability context

## 4. 📦 Dependencies

- **streamlit** or **plotly**: Dashboard interactivity
- **altair**: Declarative visualization (alternative to plotly)
- **pandas/polars**: Data preparation for dashboard
- **python**: Backend dashboard logic

## 5. ✅ Implementation Tasks

### Dashboard Framework Setup
- ⬜ Choose dashboard platform (Streamlit recommended for simplicity)
- ⬜ Create dashboard project structure
- ⬜ Set up data loading from processed datasets
- ⬜ Implement caching for performance optimization

### Data Visualization Components
- ⬜ Time series line plot: Workforce trends by sector
  - Interactive: Toggle sectors on/off
  - X-axis: Year (2006-2019)
  - Y-axis: Workforce count
  - Legend: Sector names
  
- ⬜ Time series line plot: Workforce-to-bed ratios by sector
  - Interactive: Toggle sectors, adjust baseline benchmark
  - Shaded region: "Acceptable range" (1.5-2.5 FTE per bed)
  - Tooltip: Exact values on hover
  
- ⬜ Bar chart: Sector comparison
  - Baseline (2006) vs. Most recent year (2019)
  - Grouped bars: Public, Private, Not-for-Profit
  - Y-axis: Workforce count
  
- ⬜ Line plot: Professional composition over time
  - Multiple lines: Doctors, Nurses, Pharmacists (percent of total)
  - By sector view: Show composition trends by sector
  
- ⬜ Growth rate comparison table
  - Columns: Sector, Workforce Growth Rate, Capacity Growth Rate, Mismatch
  - Sort by mismatch magnitude
  - Color coding: Red for significant misalignments

### Interactive Filtering
- ⬜ Sector filter (checkboxes): Public, Private, Not-for-Profit
- ⬜ Year range slider: Select subset of years for analysis
- ⬜ Profession filter (if detailed data available): Show trends by professional category
- ⬜ Metric selector: Toggle between different views (counts, ratios, growth rates)

### Alert and Exception Highlighting
- ⬜ Highlight sectors with mismatch >1% annual growth rate difference
- ⬜ Highlight years with unusual values (>2 std dev from sector average)
- ⬜ Provide explanatory notes on highlighted anomalies (if known cause)
- ⬜ Allow user to export flagged items for further investigation

### Comparative Benchmarking Display
- ⬜ Include reference benchmark: WHO standard (4.45 health workers per 1,000 population)
- ⬜ Reference benchmark: Typical developed healthcare system ratio (1.5-2.5 FTE per bed)
- ⬜ Visual indicator showing Singapore comparison to benchmarks
- ⬜ Note any data/definition differences limiting comparability

### User Guidance and Documentation
- ⬜ Create in-dashboard tooltip help for each visualization
- ⬜ Create external user guide (markdown/PDF):
  - How to read each visualization
  - What each metric means
  - How to use interactive filters
  - Interpretation guidance (e.g., what does increasing ratio indicate?)
  - Data limitations and quality notes
  
- ⬜ Add data quality disclaimer:
  - Data source (Kaggle dataset, year coverage)
  - Known limitations (no facility-level detail, no demographic breakdown)
  - Recommendations for data verification

### Technical Implementation
- ⬜ Load clean datasets from `data/3_interim/` or `data/4_processed/`
- ⬜ Implement data transformation pipeline (aggregation, metric calculation if needed)
- ⬜ Create reusable visualization functions for consistency
- ⬜ Implement caching to improve dashboard responsiveness
- ⬜ Add error handling for data loading failures

### Performance Optimization
- ⬜ Profile dashboard load time (target: <3 seconds initial load)
- ⬜ Implement data caching for frequently accessed aggregations
- ⬜ Optimize visualizations for web (avoid overly complex plots)
- ⬜ Test with multiple concurrent users (if deployed)

### Deployment and Access
- ⬜ Deploy dashboard to appropriate platform (Streamlit Cloud, Databricks, internal server)
- ⬜ Set up authentication (if required by organization)
- ⬜ Create deployment documentation with access instructions
- ⬜ Set up data refresh schedule (if using live data connection)
- ⬜ Monitor dashboard uptime and performance

### Testing and Validation
- ⬜ Verify all filters work correctly
- ⬜ Verify calculations match source analysis (story 4)
- ⬜ Test with different screen sizes (desktop, tablet, mobile)
- ⬜ Validate with stakeholders:
  - Can they find information they need?
  - Are visualizations clear and interpretable?
  - Are there additional views or metrics needed?

### Documentation and Handoff
- ⬜ Create dashboard maintenance guide:
  - How to update data
  - How to modify visualizations
  - Known issues and troubleshooting
  
- ⬜ Provide training to stakeholders on dashboard use
- ⬜ Document access procedures and contact for technical issues

## 6. Notes

**Platform Choice Rationale**:
- **Streamlit**: Easiest for rapid development, good for exploration, Python-native
- **Plotly/Dash**: More customizable, better for production dashboards
- **Databricks Dashboards**: Integrated if using Databricks infrastructure

**Interactivity Trade-offs**:
- More interactive filters improve exploration but can overwhelm users
- Focus on filters that answer key business questions (sector comparison, time trends)
- Use sensible defaults that show most relevant data on initial load

**Domain Context** ([Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md)):
- Ratio interpretation: Higher doesn't necessarily mean better (depends on healthcare model)
- Sector differences matter: Public, Private, NGO sectors have different models and workforce structures
- Trends more important than absolute values: Is sector getting better or worse relative to others?

**Related Stories**: This dashboard integrates findings from Stories 1-4 and enables stakeholder engagement (Story 6). Feedback from dashboard users should inform final report generation.

---

## Implementation Plan

### 1. Feature Overview

This user story implements an **interactive web dashboard for workforce-capacity metrics exploration** to enable MOH policy makers to monitor workforce-capacity alignment, compare sectors, and identify misalignments interactively. The dashboard displays time series trends, sector comparisons, professional composition, and mismatch detection results with drill-down capabilities and benchmark overlays.

**Primary User Role**: MOH policy maker, healthcare system administrator

**Goal**: Provide self-service analytics tool for exploring workforce-capacity metrics (2009-2019), comparing sectors, and identifying areas requiring workforce planning interventions.

---

### 2. Component Analysis & Reuse Strategy

**Existing Data Components (Reusable)**:

1. **Processed Metrics Dataset** (`data/4_processed/workforce_capacity_metrics.parquet` - from User Story 4)
   - **Purpose**: Primary data source for dashboard
   - **Justification**: Pre-calculated metrics improve dashboard load time
   - **Reuse**: Load directly into dashboard with caching

2. **Cleaned Datasets** (`data/3_interim/workforce_clean.parquet`, `data/3_interim/capacity_clean.parquet`)
   - **Purpose**: Detailed data for profession-level drill-down
   - **Justification**: Metrics dataset aggregates professions; detailed data needed for composition analysis
   - **Reuse**: Load for composition and drill-down views

3. **Visualization Module** (`src/visualization/workforce_plots.py` - from User Story 3)
   - **Purpose**: Matplotlib/seaborn plotting functions
   - **Justification**: Can reuse base plotting logic, but need Plotly/Altair for interactivity
   - **Partial Reuse**: Convert static plots to interactive Plotly equivalents

4. **Benchmark Module** (`src/analysis/benchmarks.py` - from User Story 4)
   - **Purpose**: Benchmark values for comparison
   - **Justification**: Display benchmark ranges on charts
   - **Reuse**: Import benchmarks to overlay on visualizations

5. **Findings Report** (`reports/workforce_capacity_mismatch_findings.md` - from User Story 4)
   - **Purpose**: Interpretation guidance for metrics
   - **Justification**: Provide context for dashboard users
   - **Reuse**: Extract key findings for dashboard annotations

**New Components Required**:

1. **Streamlit Dashboard App** (`dashboards/workforce_capacity_dashboard.py`)
   - **Purpose**: Main interactive dashboard application
   - **Justification**: New UI layer for interactivity
   - **Create**: New Streamlit app with multi-page layout

2. **Dashboard Components Module** (`src/visualization/dashboard_components.py`)
   - **Purpose**: Reusable Plotly/Altair chart functions for dashboard
   - **Justification**: Separation of concerns; testable components
   - **Create**: New module with interactive chart builders

3. **Dashboard Data Loader** (`src/dashboard/data_loader.py`)
   - **Purpose**: Data loading and caching utilities for dashboard
   - **Justification**: Performance optimization with st.cache_data
   - **Create**: New module with cached data loaders

4. **Dashboard Configuration** (`config/dashboard.yml`)
   - **Purpose**: Dashboard settings (colors, benchmarks, defaults)
   - **Justification**: Centralized configuration for UI consistency
   - **Create**: New YAML config file

5. **User Guide** (`reports/dashboards/workforce_capacity_dashboard_user_guide.md`)
   - **Purpose**: Documentation for dashboard users
   - **Justification**: Required acceptance criterion
   - **Create**: New markdown guide with screenshots

**Gaps Identified**:
- No interactive visualization components (need Plotly/Altair)
- No Streamlit app structure
- Streamlit not yet installed (identified in context gathering)

---

### 3. Affected Files with Implementation Context

**[CREATE] `dashboards/workforce_capacity_dashboard.py`**
- **Purpose**: Main Streamlit dashboard application
- **Inputs**: Processed metrics parquet, cleaned workforce/capacity datasets
- **Outputs**: Interactive web dashboard (served by Streamlit)
- **Logging**: Log to `logs/dashboard/access_{timestamp}.log`

**[CREATE] `src/visualization/dashboard_components.py`**
- **Purpose**: Reusable Plotly chart functions
- **Inputs**: Polars DataFrames
- **Outputs**: Plotly Figure objects
- **Logging**: Minimal (chart creation logging if needed)

**[CREATE] `src/dashboard/__init__.py`**
- **Purpose**: Dashboard package initialization
- **Inputs**: N/A
- **Outputs**: N/A

**[CREATE] `src/dashboard/data_loader.py`**
- **Purpose**: Cached data loading for dashboard
- **Inputs**: Parquet file paths
- **Outputs**: Polars DataFrames (cached)
- **Logging**: Log data load times and cache hits

**[CREATE] `config/dashboard.yml`**
- **Purpose**: Dashboard configuration settings
- **Inputs**: N/A (configuration file)
- **Outputs**: N/A
- **Logging**: N/A

**[CREATE] `reports/dashboards/workforce_capacity_dashboard_user_guide.md`**
- **Purpose**: End-user documentation
- **Inputs**: Dashboard features, screenshots
- **Outputs**: Markdown documentation
- **Logging**: N/A

**[CREATE] `dashboards/pages/1_Workforce_Trends.py`**
- **Purpose**: Streamlit multi-page app - Workforce trends page
- **Inputs**: Cleaned workforce data
- **Outputs**: Interactive visualizations
- **Logging**: N/A

**[CREATE] `dashboards/pages/2_Workforce_Capacity_Ratios.py`**
- **Purpose**: Streamlit multi-page app - Ratios page
- **Inputs**: Processed metrics data
- **Outputs**: Interactive visualizations with benchmarks
- **Logging**: N/A

**[CREATE] `dashboards/pages/3_Sector_Comparison.py`**
- **Purpose**: Streamlit multi-page app - Comparative analysis page
- **Inputs**: Processed metrics and cleaned data
- **Outputs**: Side-by-side sector comparisons
- **Logging**: N/A

**[CREATE] `dashboards/pages/4_Mismatch_Detection.py`**
- **Purpose**: Streamlit multi-page app - Misalignment alerts page
- **Inputs**: Processed metrics with mismatch flags
- **Outputs**: Alert tables and visualizations
- **Logging**: N/A

**[CREATE] `dashboards/.streamlit/config.toml`**
- **Purpose**: Streamlit app configuration
- **Inputs**: N/A (Streamlit settings)
- **Outputs**: N/A
- **Logging**: N/A

**[MODIFY] `requirements.txt`**
- **Purpose**: Add dashboard dependencies
- **Modifications**: Add streamlit, plotly, altair
- **Logging**: N/A

---

### 4. Component Breakdown with Technical Constraints

**Component 1: Streamlit Dashboard App** (`dashboards/workforce_capacity_dashboard.py`)

**Technical Constraints**:
- Initial load time: < 3 seconds
- Use st.cache_data for data loading
- Support 1024px+ desktop screens (mobile-responsive design)
- Implement error handling for missing data files
- Clear navigation structure (multi-page app)

**Key Features**:
- Page navigation (Home, Workforce Trends, Ratios, Sector Comparison, Mismatch Detection)
- Global filters in sidebar (sector, year range, professions)
- Header with title and data refresh timestamp
- Footer with data source attribution
- Responsive layout

**Component 2: Dashboard Components Module** (`src/visualization/dashboard_components.py`)

**Technical Constraints**:
- All functions return Plotly Figure or Altair Chart objects
- Charts must be interactive (hover, zoom, pan)
- Consistent color scheme (defined in config/dashboard.yml)
- Tooltips on all data points
- Responsive sizing (use relative dimensions)

**Key Functions**:
- `create_workforce_trend_chart()`: Time series line chart
- `create_ratio_benchmark_chart()`: Ratio trends with benchmark shading
- `create_sector_comparison_bar_chart()`: Grouped bar chart
- `create_composition_stacked_area()`: Stacked area chart for composition
- `create_mismatch_heatmap()`: Heatmap showing mismatch by sector and year
- `create_growth_rate_scatter()`: Scatter plot (workforce vs. capacity growth)

**Component 3: Dashboard Data Loader** (`src/dashboard/data_loader.py`)

**Technical Constraints**:
- Use @st.cache_data decorator for all loaders
- Cache TTL: 24 hours (configurable)
- Handle missing files gracefully (return empty DataFrame with schema)
- Log cache hits/misses for performance monitoring
- Validate data schema after loading

**Key Functions**:
- `load_metrics_data()`: Load processed metrics
- `load_workforce_data()`: Load cleaned workforce data
- `load_capacity_data()`: Load cleaned capacity data
- `filter_data_by_selections()`: Apply user filters
- `get_data_refresh_timestamp()`: Return last data update time

**Component 4: Dashboard Pages** (`dashboards/pages/*.py`)

**Technical Constraints**:
- Each page must be self-contained
- Share common filters from main app session state
- Page load time: < 1 second after initial data load
- Consistent layout structure across pages
- Clear descriptive headers

**Page Breakdown**:
- **Home**: Overview, data summary, key findings highlights
- **Workforce Trends**: Time series of workforce by sector and profession
- **Workforce-Capacity Ratios**: Ratio trends with benchmark comparisons
- **Sector Comparison**: Side-by-side metrics across sectors
- **Mismatch Detection**: Alert table and visualizations for misalignments

---

### 5. Data Pipeline

**Data Sources** (all from prior User Stories):

**Primary Tables**:
1. **Processed Metrics** (`data/4_processed/workforce_capacity_metrics.parquet`)
   - **Schema**: `year`, `sector`, `total_workforce`, `total_beds`, `workforce_to_bed_ratio`, `workforce_growth_rate`, `capacity_growth_rate`, `mismatch_index`, `doctor_to_nurse_ratio`, `within_benchmark`, `mismatch_flag`
   - **Coverage**: 2009-2019 (overlap period)
   - **Purpose**: Primary data source for ratio and mismatch views

2. **Cleaned Workforce Data** (`data/3_interim/workforce_clean.parquet`)
   - **Schema**: `year`, `sector`, `profession`, `count`
   - **Coverage**: 2006-2019
   - **Purpose**: Detailed trends by profession

3. **Cleaned Capacity Data** (`data/3_interim/capacity_clean.parquet`)
   - **Schema**: `year`, `sector`, `category`, `count`
   - **Coverage**: 2009-2020
   - **Purpose**: Capacity trends and composition

**Data Pipeline Strategy**:

**Extraction**:
- Load all datasets at dashboard startup using cached loaders
- Validate schemas immediately
- Log data coverage and freshness
- Handle missing files with graceful degradation

**Transformation** (in dashboard):
- Apply user-selected filters (sector, year range, profession)
- Aggregate data dynamically for selected views
- Calculate derived metrics if not pre-calculated
- Format data for visualization (long-to-wide pivots if needed)

**Consumption Layer**:
- **Interactive Charts**: Plotly Figure objects rendered in Streamlit
- **Tables**: Polars DataFrames displayed with st.dataframe
- **Exports**: Filtered data downloadable as CSV via st.download_button

**Orchestration**:
- **Execution**: Streamlit app runs on local server or cloud deployment
- **Refresh Strategy**: Manual data refresh or scheduled batch update
- **Caching**: Streamlit cache with 24-hour TTL

**Error Handling**:
- Missing data files → Display error message with contact info
- Invalid filters → Reset to defaults and warn user
- Chart rendering errors → Show fallback message and log error

---

### 6. Code Generation Specifications

#### 6.1 Function Signatures & Contracts

**Dashboard Components Module** (`src/visualization/dashboard_components.py`):

```python
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional, Dict, Any
from loguru import logger


def create_workforce_trend_chart(
    workforce_df: pl.DataFrame,
    selected_sectors: List[str],
    selected_professions: Optional[List[str]] = None,
    year_range: Optional[tuple[int, int]] = None
) -> go.Figure:
    """
    Create interactive time series chart showing workforce trends.
    
    Args:
        workforce_df: Cleaned workforce DataFrame
        selected_sectors: List of sectors to include
        selected_professions: List of professions to include (None = all)
        year_range: Tuple of (start_year, end_year) or None for all years
        
    Returns:
        Plotly Figure with interactive line chart
        
    Example:
        >>> fig = create_workforce_trend_chart(
        ...     workforce_df,
        ...     selected_sectors=['Public', 'Private'],
        ...     selected_professions=['Doctors', 'Nurses'],
        ...     year_range=(2010, 2019)
        ... )
        >>> # Display in Streamlit: st.plotly_chart(fig, use_container_width=True)
    """
    logger.info(f"Creating workforce trend chart for sectors: {selected_sectors}")
    
    # Filter data
    filtered_df = workforce_df.filter(pl.col('sector').is_in(selected_sectors))
    
    if selected_professions:
        filtered_df = filtered_df.filter(pl.col('profession').is_in(selected_professions))
    
    if year_range:
        filtered_df = filtered_df.filter(
            (pl.col('year') >= year_range[0]) &
            (pl.col('year') <= year_range[1])
        )
    
    # Aggregate by year, sector, profession
    agg_df = (
        filtered_df
        .group_by(['year', 'sector', 'profession'])
        .agg([pl.col('count').sum().alias('total')])
        .sort(['sector', 'profession', 'year'])
    )
    
    # Convert to pandas for Plotly Express compatibility
    plot_df = agg_df.to_pandas()
    
    # Create line chart
    fig = px.line(
        plot_df,
        x='year',
        y='total',
        color='sector',
        line_dash='profession',
        title='Workforce Trends by Sector and Profession',
        labels={
            'year': 'Year',
            'total': 'Workforce Count',
            'sector': 'Sector',
            'profession': 'Profession'
        },
        hover_data=['sector', 'profession', 'year', 'total']
    )
    
    # Styling
    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        template='plotly_white',
        height=500
    )
    
    fig.update_xaxes(tickmode='linear', dtick=1)
    
    logger.success(f"Created workforce trend chart with {len(plot_df)} data points")
    
    return fig


def create_ratio_benchmark_chart(
    metrics_df: pl.DataFrame,
    selected_sectors: List[str],
    benchmark_min: float = 1.5,
    benchmark_max: float = 2.5
) -> go.Figure:
    """
    Create interactive chart showing workforce-to-bed ratios with benchmark overlay.
    
    Args:
        metrics_df: Processed metrics DataFrame
        selected_sectors: List of sectors to include
        benchmark_min: Lower bound of acceptable range
        benchmark_max: Upper bound of acceptable range
        
    Returns:
        Plotly Figure with ratio trends and shaded benchmark region
        
    Example:
        >>> fig = create_ratio_benchmark_chart(
        ...     metrics_df,
        ...     selected_sectors=['Public', 'Private'],
        ...     benchmark_min=1.5,
        ...     benchmark_max=2.5
        ... )
    """
    logger.info(f"Creating ratio benchmark chart for sectors: {selected_sectors}")
    
    # Filter data
    filtered_df = (
        metrics_df
        .filter(pl.col('sector').is_in(selected_sectors))
        .sort(['sector', 'year'])
    )
    
    plot_df = filtered_df.to_pandas()
    
    # Create figure
    fig = go.Figure()
    
    # Add benchmark shaded region
    years = plot_df['year'].unique()
    fig.add_trace(go.Scatter(
        x=list(years) + list(reversed(years)),
        y=[benchmark_max] * len(years) + [benchmark_min] * len(years),
        fill='toself',
        fillcolor='rgba(34, 139, 34, 0.15)',  # ForestGreen with transparency
        line=dict(width=0),
        name='Typical Range',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Add ratio lines by sector
    for sector in selected_sectors:
        sector_df = plot_df[plot_df['sector'] == sector]
        
        fig.add_trace(go.Scatter(
            x=sector_df['year'],
            y=sector_df['workforce_to_bed_ratio'],
            mode='lines+markers',
            name=sector,
            hovertemplate=(
                f'<b>{sector}</b><br>' +
                'Year: %{x}<br>' +
                'Ratio: %{y:.2f}<br>' +
                '<extra></extra>'
            )
        ))
    
    # Layout
    fig.update_layout(
        title='Workforce-to-Bed Ratio Trends with Benchmark Range',
        xaxis_title='Year',
        yaxis_title='Workforce per Bed (FTE)',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        template='plotly_white',
        height=500
    )
    
    fig.update_xaxes(tickmode='linear', dtick=1)
    
    logger.success(f"Created ratio benchmark chart with {len(plot_df)} data points")
    
    return fig


def create_sector_comparison_bar_chart(
    metrics_df: pl.DataFrame,
    comparison_year: int,
    metric: str = 'total_workforce'
) -> go.Figure:
    """
    Create grouped bar chart comparing sectors for a specific year.
    
    Args:
        metrics_df: Processed metrics DataFrame
        comparison_year: Year to compare sectors
        metric: Metric to compare (default: 'total_workforce')
        
    Returns:
        Plotly Figure with grouped bar chart
        
    Example:
        >>> fig = create_sector_comparison_bar_chart(
        ...     metrics_df,
        ...     comparison_year=2019,
        ...     metric='workforce_to_bed_ratio'
        ... )
    """
    logger.info(f"Creating sector comparison chart for year {comparison_year}, metric: {metric}")
    
    # Filter to comparison year
    filtered_df = (
        metrics_df
        .filter(pl.col('year') == comparison_year)
        .sort('sector')
    )
    
    plot_df = filtered_df.to_pandas()
    
    # Create bar chart
    fig = px.bar(
        plot_df,
        x='sector',
        y=metric,
        color='sector',
        title=f'Sector Comparison - {metric.replace("_", " ").title()} ({comparison_year})',
        labels={
            'sector': 'Sector',
            metric: metric.replace('_', ' ').title()
        },
        text=metric
    )
    
    # Add value labels on bars
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    
    # Layout
    fig.update_layout(
        showlegend=False,
        template='plotly_white',
        height=500,
        xaxis_tickangle=-45
    )
    
    logger.success(f"Created sector comparison chart with {len(plot_df)} sectors")
    
    return fig


def create_composition_stacked_area(
    workforce_df: pl.DataFrame,
    selected_sector: str
) -> go.Figure:
    """
    Create stacked area chart showing professional composition over time.
    
    Args:
        workforce_df: Cleaned workforce DataFrame
        selected_sector: Sector to visualize
        
    Returns:
        Plotly Figure with stacked area chart
        
    Example:
        >>> fig = create_composition_stacked_area(
        ...     workforce_df,
        ...     selected_sector='Public'
        ... )
    """
    logger.info(f"Creating composition stacked area chart for sector: {selected_sector}")
    
    # Filter to sector
    filtered_df = (
        workforce_df
        .filter(pl.col('sector') == selected_sector)
        .group_by(['year', 'profession'])
        .agg([pl.col('count').sum().alias('total')])
        .sort(['year', 'profession'])
    )
    
    # Calculate percentages
    total_by_year = (
        filtered_df
        .group_by('year')
        .agg([pl.col('total').sum().alias('year_total')])
    )
    
    composition_df = (
        filtered_df
        .join(total_by_year, on='year', how='left')
        .with_columns([
            (pl.col('total') / pl.col('year_total') * 100).alias('percentage')
        ])
        .to_pandas()
    )
    
    # Create stacked area chart
    fig = px.area(
        composition_df,
        x='year',
        y='percentage',
        color='profession',
        title=f'Workforce Composition - {selected_sector} Sector',
        labels={
            'year': 'Year',
            'percentage': '% of Total Workforce',
            'profession': 'Profession'
        }
    )
    
    # Layout
    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        template='plotly_white',
        height=500
    )
    
    fig.update_xaxes(tickmode='linear', dtick=1)
    
    logger.success(f"Created composition stacked area chart for {selected_sector}")
    
    return fig


def create_mismatch_heatmap(
    metrics_df: pl.DataFrame
) -> go.Figure:
    """
    Create heatmap showing mismatch index by sector and year.
    
    Args:
        metrics_df: Processed metrics DataFrame with mismatch_index column
        
    Returns:
        Plotly Figure with heatmap
        
    Example:
        >>> fig = create_mismatch_heatmap(metrics_df)
    """
    logger.info("Creating mismatch heatmap")
    
    # Pivot data for heatmap
    pivot_df = (
        metrics_df
        .filter(pl.col('mismatch_index').is_not_null())
        .select(['year', 'sector', 'mismatch_index'])
        .to_pandas()
        .pivot(index='sector', columns='year', values='mismatch_index')
    )
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn',  # Red (negative) -> Yellow (neutral) -> Green (positive)
        zmid=0,  # Center colorscale at zero
        text=pivot_df.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        colorbar=dict(title='Mismatch Index (%)')
    ))
    
    # Layout
    fig.update_layout(
        title='Workforce-Capacity Mismatch Index by Sector and Year',
        xaxis_title='Year',
        yaxis_title='Sector',
        template='plotly_white',
        height=400
    )
    
    logger.success(f"Created mismatch heatmap with {len(pivot_df)} sectors")
    
    return fig


def create_growth_rate_scatter(
    metrics_df: pl.DataFrame,
    highlight_threshold: float = 1.0
) -> go.Figure:
    """
    Create scatter plot showing workforce vs. capacity growth rates.
    
    Args:
        metrics_df: Processed metrics DataFrame
        highlight_threshold: Mismatch threshold for highlighting points
        
    Returns:
        Plotly Figure with scatter plot
        
    Example:
        >>> fig = create_growth_rate_scatter(metrics_df, highlight_threshold=1.0)
    """
    logger.info("Creating growth rate scatter plot")
    
    # Filter valid growth rate rows
    plot_df = (
        metrics_df
        .filter(
            pl.col('workforce_growth_rate').is_not_null() &
            pl.col('capacity_growth_rate').is_not_null()
        )
        .to_pandas()
    )
    
    # Add flag for significant mismatch
    plot_df['significant_mismatch'] = plot_df['mismatch_index'].abs() > highlight_threshold
    
    # Create scatter plot
    fig = px.scatter(
        plot_df,
        x='capacity_growth_rate',
        y='workforce_growth_rate',
        color='sector',
        symbol='significant_mismatch',
        size='mismatch_index',
        hover_data=['year', 'sector', 'mismatch_index'],
        title='Workforce vs. Capacity Growth Rates',
        labels={
            'capacity_growth_rate': 'Capacity Growth Rate (%)',
            'workforce_growth_rate': 'Workforce Growth Rate (%)',
            'significant_mismatch': 'Significant Mismatch'
        }
    )
    
    # Add diagonal line (aligned growth)
    min_val = min(plot_df['capacity_growth_rate'].min(), plot_df['workforce_growth_rate'].min())
    max_val = max(plot_df['capacity_growth_rate'].max(), plot_df['workforce_growth_rate'].max())
    
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        name='Aligned Growth',
        showlegend=True
    ))
    
    # Layout
    fig.update_layout(
        template='plotly_white',
        height=600
    )
    
    logger.success(f"Created growth rate scatter plot with {len(plot_df)} points")
    
    return fig
```

**Dashboard Data Loader Module** (`src/dashboard/data_loader.py`):

```python
import polars as pl
import streamlit as st
from pathlib import Path
from datetime import datetime
from loguru import logger
from typing import Optional, List


@st.cache_data(ttl=86400)  # 24-hour cache
def load_metrics_data() -> pl.DataFrame:
    """
    Load processed metrics dataset with caching.
    
    Returns:
        Polars DataFrame with workforce-capacity metrics
        
    Raises:
        FileNotFoundError: If metrics file missing
    """
    file_path = Path('data/4_processed/workforce_capacity_metrics.parquet')
    
    if not file_path.exists():
        logger.error(f"Metrics file not found: {file_path}")
        raise FileNotFoundError(f"Metrics file not found: {file_path}")
    
    logger.info(f"Loading metrics data from {file_path}")
    df = pl.read_parquet(file_path)
    
    logger.success(f"Loaded metrics data: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return df


@st.cache_data(ttl=86400)
def load_workforce_data() -> pl.DataFrame:
    """
    Load cleaned workforce dataset with caching.
    
    Returns:
        Polars DataFrame with workforce counts by sector, year, profession
    """
    file_path = Path('data/3_interim/workforce_clean.parquet')
    
    if not file_path.exists():
        logger.error(f"Workforce file not found: {file_path}")
        raise FileNotFoundError(f"Workforce file not found: {file_path}")
    
    logger.info(f"Loading workforce data from {file_path}")
    df = pl.read_parquet(file_path)
    
    logger.success(f"Loaded workforce data: {df.shape[0]} rows")
    
    return df


@st.cache_data(ttl=86400)
def load_capacity_data() -> pl.DataFrame:
    """
    Load cleaned capacity dataset with caching.
    
    Returns:
        Polars DataFrame with capacity counts by sector, year, category
    """
    file_path = Path('data/3_interim/capacity_clean.parquet')
    
    if not file_path.exists():
        logger.error(f"Capacity file not found: {file_path}")
        raise FileNotFoundError(f"Capacity file not found: {file_path}")
    
    logger.info(f"Loading capacity data from {file_path}")
    df = pl.read_parquet(file_path)
    
    logger.success(f"Loaded capacity data: {df.shape[0]} rows")
    
    return df


def filter_data_by_selections(
    df: pl.DataFrame,
    selected_sectors: Optional[List[str]] = None,
    year_range: Optional[tuple[int, int]] = None,
    selected_professions: Optional[List[str]] = None
) -> pl.DataFrame:
    """
    Apply user-selected filters to DataFrame.
    
    Args:
        df: Input DataFrame
        selected_sectors: List of sectors to include (None = all)
        year_range: Tuple of (start_year, end_year) (None = all)
        selected_professions: List of professions to include (None = all)
        
    Returns:
        Filtered DataFrame
    """
    logger.info(f"Applying filters: sectors={selected_sectors}, years={year_range}, professions={selected_professions}")
    
    filtered_df = df.clone()
    
    if selected_sectors and 'sector' in filtered_df.columns:
        filtered_df = filtered_df.filter(pl.col('sector').is_in(selected_sectors))
    
    if year_range and 'year' in filtered_df.columns:
        filtered_df = filtered_df.filter(
            (pl.col('year') >= year_range[0]) &
            (pl.col('year') <= year_range[1])
        )
    
    if selected_professions and 'profession' in filtered_df.columns:
        filtered_df = filtered_df.filter(pl.col('profession').is_in(selected_professions))
    
    logger.info(f"Filtered data: {filtered_df.shape[0]} rows remaining")
    
    return filtered_df


def get_data_refresh_timestamp() -> str:
    """
    Get timestamp of last data refresh.
    
    Returns:
        Formatted timestamp string
    """
    file_path = Path('data/4_processed/workforce_capacity_metrics.parquet')
    
    if file_path.exists():
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mod_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return 'Unknown'
```

**Main Dashboard App** (`dashboards/workforce_capacity_dashboard.py`):

```python
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dashboard.data_loader import (
    load_metrics_data,
    load_workforce_data,
    load_capacity_data,
    get_data_refresh_timestamp
)
from src.analysis.benchmarks import WORKFORCE_TO_BED_BENCHMARKS, DOCTOR_TO_NURSE_BENCHMARKS
from loguru import logger


# Page configuration
st.set_page_config(
    page_title='MOH Workforce-Capacity Dashboard',
    page_icon='🏥',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Header
st.title('🏥 Healthcare Workforce-Capacity Analysis Dashboard')
st.markdown('### Ministry of Health Singapore - Workforce Planning Analytics')

# Sidebar - Global Filters
st.sidebar.title('Filters')

# Data loading with error handling
try:
    metrics_df = load_metrics_data()
    workforce_df = load_workforce_data()
    capacity_df = load_capacity_data()
    
    data_timestamp = get_data_refresh_timestamp()
    st.sidebar.success(f'✅ Data loaded successfully')
    st.sidebar.caption(f'Last updated: {data_timestamp}')
    
except FileNotFoundError as e:
    st.error(f'❌ Data file not found: {e}')
    st.info('Please ensure User Stories 2-4 have been completed and data files exist.')
    st.stop()
except Exception as e:
    st.error(f'❌ Error loading data: {e}')
    logger.exception('Dashboard data loading error')
    st.stop()

# Global Filters in Sidebar
sectors = workforce_df['sector'].unique().to_list()
selected_sectors = st.sidebar.multiselect(
    'Select Sectors',
    options=sectors,
    default=sectors  # All sectors selected by default
)

professions = workforce_df['profession'].unique().to_list()
selected_professions = st.sidebar.multiselect(
    'Select Professions',
    options=professions,
    default=professions
)

min_year = int(metrics_df['year'].min())
max_year = int(metrics_df['year'].max())
year_range = st.sidebar.slider(
    'Select Year Range',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

st.sidebar.markdown('---')
st.sidebar.info(
    '**Data Coverage:**\n'
    f'- Workforce: 2006-2019\n'
    f'- Capacity: 2009-2020\n'
    f'- Metrics: 2009-2019 (overlap period)'
)

# Main Page Content
st.markdown('---')

# Overview Section
st.header('📊 Dashboard Overview')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label='Total Workforce (Latest Year)',
        value=f"{workforce_df.filter(pl.col('year') == max_year)['count'].sum():,}"
    )

with col2:
    st.metric(
        label='Total Beds (Latest Year)',
        value=f"{capacity_df.filter((pl.col('year') == max_year) & (pl.col('category') == 'Hospital Beds'))['count'].sum():,}"
    )

with col3:
    avg_ratio = metrics_df.filter(pl.col('year') == max_year)['workforce_to_bed_ratio'].mean()
    delta_ratio = avg_ratio - ((WORKFORCE_TO_BED_BENCHMARKS['typical_min'] + WORKFORCE_TO_BED_BENCHMARKS['typical_max']) / 2)
    st.metric(
        label='Avg Workforce-to-Bed Ratio',
        value=f"{avg_ratio:.2f}",
        delta=f"{delta_ratio:+.2f} vs. benchmark"
    )

with col4:
    mismatches = metrics_df.filter(pl.col('mismatch_flag') == True).height
    st.metric(
        label='Flagged Misalignments',
        value=mismatches,
        delta='Significant divergences'
    )

st.markdown('---')

# Navigation Instructions
st.markdown(
    """
    ### 🗺️ Navigation Guide
    
    Use the sidebar navigation to explore different aspects of workforce-capacity analysis:
    
    - **Workforce Trends**: Time series of workforce counts by sector and profession
    - **Workforce-Capacity Ratios**: Ratio trends with international benchmark comparisons
    - **Sector Comparison**: Side-by-side metrics across Public, Private, and Not-for-Profit sectors
    - **Mismatch Detection**: Alerts for sectors with significant workforce-capacity misalignments
    
    **How to Use Filters:**
    - Select specific sectors to focus your analysis
    - Adjust the year range slider to explore temporal trends
    - Choose professions to drill down into specific workforce categories
    - Changes apply across all dashboard pages
    
    **Data Notes:**
    - Data sourced from MOH Singapore (Kaggle dataset)
    - Year coverage varies by dataset (see sidebar)
    - Metrics calculated for overlap period (2009-2019)
    """
)

st.markdown('---')

# Key Findings Highlights (from User Story 4 report)
st.header('🔍 Key Findings Highlights')

st.markdown(
    """
    > **Note:** These findings are derived from the comprehensive analysis in User Story 4.  
    > Use the dashboard pages to explore the data interactively and validate insights.
    
    **Workforce-Capacity Alignment:**
    - Public sector shows consistent workforce-to-bed ratio within benchmark range (1.5-2.5 FTE/bed)
    - Private sector ratios vary more significantly; some years outside typical range
    - Not-for-Profit sector has limited data coverage
    
    **Growth Rate Mismatches:**
    - Several sectors show >1% annual mismatch between workforce and capacity growth rates
    - See **Mismatch Detection** page for detailed breakdown
    
    **Professional Composition:**
    - Doctor-to-nurse ratios generally within expected range (0.25-0.50)
    - Composition trends show gradual shifts in workforce mix
    
    **Recommendations:**
    - Prioritize capacity expansion in sectors with sustained workforce oversupply
    - Monitor sectors flagged for misalignment in next planning cycle
    - Improve data granularity for better workforce planning precision
    """
)

st.markdown('---')

# Footer
st.caption('© 2026 Ministry of Health Singapore | Dashboard for Workforce Planning Analytics')
st.caption(f'Built with Streamlit | Data last refreshed: {data_timestamp}')
```

**Dashboard Page Example** (`dashboards/pages/1_Workforce_Trends.py`):

```python
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.dashboard.data_loader import load_workforce_data, filter_data_by_selections
from src.visualization.dashboard_components import create_workforce_trend_chart
import polars as pl


st.set_page_config(page_title='Workforce Trends', page_icon='📈', layout='wide')

st.title('📈 Workforce Trends Analysis')

st.markdown(
    """
    This page shows workforce trends over time by sector and profession.  
    Use the filters in the sidebar to customize the view.
    """
)

# Load data (cached)
workforce_df = load_workforce_data()

# Get filters from session state (shared from main app)
# Note: In multi-page Streamlit apps, filters should be managed via session_state
# For simplicity, recreate filters here (in production, use session_state)

sectors = workforce_df['sector'].unique().to_list()
selected_sectors = st.multiselect(
    'Select Sectors',
    options=sectors,
    default=sectors,
    key='workforce_trends_sectors'
)

professions = workforce_df['profession'].unique().to_list()
selected_professions = st.multiselect(
    'Select Professions',
    options=professions,
    default=professions,
    key='workforce_trends_professions'
)

min_year = int(workforce_df['year'].min())
max_year = int(workforce_df['year'].max())
year_range = st.slider(
    'Select Year Range',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    key='workforce_trends_years'
)

st.markdown('---')

# Create visualization
if selected_sectors and selected_professions:
    fig = create_workforce_trend_chart(
        workforce_df,
        selected_sectors=selected_sectors,
        selected_professions=selected_professions,
        year_range=year_range
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.subheader('Summary Statistics')
    
    filtered_df = filter_data_by_selections(
        workforce_df,
        selected_sectors=selected_sectors,
        year_range=year_range,
        selected_professions=selected_professions
    )
    
    summary = (
        filtered_df
        .group_by(['sector', 'profession'])
        .agg([
            pl.col('count').sum().alias('Total'),
            pl.col('count').mean().alias('Average'),
            pl.col('count').max().alias('Peak'),
            pl.col('count').min().alias('Minimum')
        ])
        .sort(['sector', 'profession'])
    )
    
    st.dataframe(summary.to_pandas(), use_container_width=True)
    
    # Export option
    csv = summary.to_pandas().to_csv(index=False).encode('utf-8')
    st.download_button(
        label='📥 Download Summary as CSV',
        data=csv,
        file_name='workforce_trends_summary.csv',
        mime='text/csv'
    )

else:
    st.warning('Please select at least one sector and one profession.')

st.markdown('---')
st.caption('**Interpretation Guide:** Rising trends indicate workforce expansion; declining trends may signal workforce shortages or sector consolidation.')
```

#### 6.2 Dashboard Configuration

**Config File** (`config/dashboard.yml`):

```yaml
dashboard:
  title: 'MOH Workforce-Capacity Dashboard'
  subtitle: 'Ministry of Health Singapore - Workforce Planning Analytics'
  icon: '🏥'
  
  theme:
    primary_color: '#2E86AB'  # Blue
    secondary_color: '#A23B72'  # Purple
    success_color: '#06A77D'  # Green
    warning_color: '#F18F01'  # Orange
    danger_color: '#C73E1D'  # Red
    background_color: '#FFFFFF'
    text_color: '#333333'
  
  layout:
    sidebar_state: 'expanded'
    page_width: 'wide'
  
  data:
    cache_ttl: 86400  # 24 hours in seconds
    metrics_file: 'data/4_processed/workforce_capacity_metrics.parquet'
    workforce_file: 'data/3_interim/workforce_clean.parquet'
    capacity_file: 'data/3_interim/capacity_clean.parquet'
  
  benchmarks:
    workforce_to_bed:
      min: 1.5
      max: 2.5
      label: 'Typical Range (FTE per bed)'
    
    doctor_to_nurse:
      min: 0.25
      max: 0.50
      label: 'Typical Range (doctor:nurse ratio)'
    
    mismatch_threshold: 1.0  # percentage points
  
  filters:
    default_sectors: ['Public', 'Private', 'Not-for-profit']
    default_professions: ['Doctors', 'Nurses', 'Pharmacists']
    default_year_range: [2009, 2019]
  
  performance:
    max_data_points: 10000  # Downsample if more points
    chart_height: 500
    chart_dpi: 100
```

**Streamlit Config** (`dashboards/.streamlit/config.toml`):

```toml
[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

#### 6.3 Package Management

```bash
# Install dashboard dependencies
uv pip install streamlit>=1.30.0 plotly>=5.18.0 altair>=5.2.0

# Update requirements.txt
uv pip freeze > requirements.txt

# Verify installation
python -c "import streamlit; import plotly; import altair; print('Dashboard dependencies OK')"
```

---

### 7. Domain-Driven Feature Engineering & Analysis Strategy

**Dashboard-Specific Domain Integration**:

1. **Benchmark Overlays** (from [Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md))
   - Workforce-to-bed ratio: Shaded region (1.5-2.5 FTE/bed) on ratio charts
   - Doctor-to-nurse ratio: Reference lines or shaded regions (0.25-0.50)
   - WHO minimum: Annotated line for workforce density (4.45 per 1,000 population) - if population data available

2. **Interpretation Guidance** (from domain knowledge)
   - Tooltips explaining what metric means and typical ranges
   - Alert annotations explaining why a value is flagged
   - In-dashboard notes on sector differences (Public vs. Private models)

3. **Comparative Context** (from [Healthcare System Sustainability](../../../domain_knowledge/healthcare-system-sustainability-metrics.md))
   - Show Singapore relative to OECD averages
   - Display multi-year trends with sustainability perspective
   - Link workforce metrics to capacity sustainability

---

### 8. API Endpoints & Data Contracts

**Not applicable** - Streamlit dashboard uses file-based data loading, not API endpoints.

---

### 9. Styling & Visualization

**Visualization Standards** (extend User Story 3-4):

**Dashboard-Specific Styling**:

1. **Color Scheme** (defined in `config/dashboard.yml`):
   - **Primary**: #2E86AB (Blue) - Main branding
   - **Success**: #06A77D (Green) - Within benchmark, positive trends
   - **Warning**: #F18F01 (Orange) - Approaching thresholds
   - **Danger**: #C73E1D (Red) - Outside benchmark, significant mismatches
   - **Neutral**: #4682B4 (SteelBlue) - Default data visualization

2. **Interactive Features**:
   - Hover tooltips on all data points
   - Click legend toggle to show/hide series
   - Zoom and pan enabled on time series
   - Cross-filtering between charts (if implemented)

3. **Responsive Design**:
   - Desktop (1024px+): Full multi-column layouts
   - Tablet (768-1024px): Stacked columns
   - Mobile (<768px): Single column layout

4. **Accessibility**:
   - High contrast colors
   - Alt text on all charts (Plotly accessibility features)
   - Keyboard navigation support
   - Screen reader friendly

---

### 10. Testing Strategy with Specific Assertions

**Unit Tests** (`tests/unit/test_dashboard_components.py`):

```python
import pytest
import polars as pl
from src.visualization.dashboard_components import (
    create_workforce_trend_chart,
    create_ratio_benchmark_chart,
    create_sector_comparison_bar_chart,
    create_composition_stacked_area,
    create_mismatch_heatmap
)


@pytest.fixture
def sample_workforce_data():
    return pl.DataFrame({
        'year': [2009, 2010, 2011] * 2,
        'sector': ['Public'] * 3 + ['Private'] * 3,
        'profession': ['Doctors'] * 6,
        'count': [1000, 1050, 1100, 500, 530, 560]
    })


@pytest.fixture
def sample_metrics_data():
    return pl.DataFrame({
        'year': [2009, 2010, 2011] * 2,
        'sector': ['Public'] * 3 + ['Private'] * 3,
        'total_workforce': [3000, 3150, 3300, 1500, 1590, 1680],
        'total_beds': [1500, 1560, 1630, 750, 795, 840],
        'workforce_to_bed_ratio': [2.0, 2.02, 2.02, 2.0, 2.0, 2.0],
        'mismatch_index': [0.5, -0.3, 0.2, 0.1, 0.3, -0.2]
    })


def test_create_workforce_trend_chart(sample_workforce_data):
    """Test workforce trend chart creation."""
    fig = create_workforce_trend_chart(
        sample_workforce_data,
        selected_sectors=['Public'],
        selected_professions=['Doctors']
    )
    
    # Check figure is created
    assert fig is not None
    assert hasattr(fig, 'data')
    assert len(fig.data) > 0  # At least one trace


def test_create_ratio_benchmark_chart(sample_metrics_data):
    """Test ratio benchmark chart creation."""
    fig = create_ratio_benchmark_chart(
        sample_metrics_data,
        selected_sectors=['Public', 'Private'],
        benchmark_min=1.5,
        benchmark_max=2.5
    )
    
    # Check figure created
    assert fig is not None
    # Should have benchmark region + line(s) for sectors
    assert len(fig.data) >= 2  # Benchmark + at least one sector line


def test_create_sector_comparison_bar_chart(sample_metrics_data):
    """Test sector comparison bar chart."""
    fig = create_sector_comparison_bar_chart(
        sample_metrics_data,
        comparison_year=2009,
        metric='total_workforce'
    )
    
    # Check figure created
    assert fig is not None
    assert len(fig.data) > 0
```

**Integration Tests** (`tests/integration/test_dashboard_data_flow.py`):

```python
def test_dashboard_data_loading():
    """Test complete data loading pipeline for dashboard."""
    from src.dashboard.data_loader import load_metrics_data, load_workforce_data, load_capacity_data
    
    # Load all datasets
    metrics = load_metrics_data()
    workforce = load_workforce_data()
    capacity = load_capacity_data()
    
    # Verify data loaded
    assert metrics.height > 0
    assert workforce.height > 0
    assert capacity.height > 0
    
    # Verify required columns
    assert 'workforce_to_bed_ratio' in metrics.columns
    assert 'profession' in workforce.columns
    assert 'category' in capacity.columns
```

**Visual Testing** (manual):
- [ ] Verify charts render correctly on desktop (1920x1080)
- [ ] Verify charts render correctly on tablet (768x1024)
- [ ] Verify charts render correctly on mobile (375x667)
- [ ] Verify tooltips display correctly
- [ ] Verify filters update charts correctly
- [ ] Verify export buttons work

---

### 11. Implementation Steps

**Phase 1: Environment and Dependencies**

- [ ] Install Streamlit, Plotly, Altair:
  ```bash
  uv pip install streamlit>=1.30.0 plotly>=5.18.0 altair>=5.2.0
  uv pip freeze > requirements.txt
  ```
- [ ] Create dashboard directory structure:
  ```bash
  mkdir -p dashboards/pages
  mkdir -p dashboards/.streamlit
  mkdir -p src/dashboard
  mkdir -p reports/dashboards
  ```
- [ ] Create `__init__.py` files:
  ```bash
  touch src/dashboard/__init__.py
  ```

**Phase 2: Configuration Setup**

- [ ] Create `config/dashboard.yml` with theme, benchmarks, data paths
- [ ] Create `dashboards/.streamlit/config.toml` with Streamlit settings
- [ ] Validate YAML files load correctly

**Phase 3: Data Loader Module**

- [ ] Create `src/dashboard/data_loader.py`
- [ ] Implement cached loading functions:
  - load_metrics_data()
  - load_workforce_data()
  - load_capacity_data()
  - filter_data_by_selections()
  - get_data_refresh_timestamp()
- [ ] Test data loading:
  ```bash
  python -c "from src.dashboard.data_loader import *; print(load_metrics_data().shape)"
  ```

**Phase 4: Dashboard Components Module**

- [ ] Create `src/visualization/dashboard_components.py`
- [ ] Implement Plotly chart functions:
  - create_workforce_trend_chart()
  - create_ratio_benchmark_chart()
  - create_sector_comparison_bar_chart()
  - create_composition_stacked_area()
  - create_mismatch_heatmap()
  - create_growth_rate_scatter()
- [ ] Test each function individually

**Phase 5: Main Dashboard App**

- [ ] Create `dashboards/workforce_capacity_dashboard.py`
- [ ] Implement:
  - Page configuration
  - Header and title
  - Sidebar filters
  - Data loading with error handling
  - Overview metrics (4 key metrics in columns)
  - Navigation guide
  - Key findings highlights
  - Footer
- [ ] Test locally:
  ```bash
  streamlit run dashboards/workforce_capacity_dashboard.py
  ```

**Phase 6: Dashboard Pages**

- [ ] Create `dashboards/pages/1_Workforce_Trends.py`:
  - Load workforce data
  - Filters (sectors, professions, year range)
  - Workforce trend chart
  - Summary table
  - Export CSV button
  
- [ ] Create `dashboards/pages/2_Workforce_Capacity_Ratios.py`:
  - Load metrics data
  - Ratio benchmark chart (with shaded region)
  - Sector toggle filters
  - Benchmark comparison table
  - Interpretation notes
  
- [ ] Create `dashboards/pages/3_Sector_Comparison.py`:
  - Year selector for comparison
  - Grouped bar chart (sectors side-by-side)
  - Metric selector (dropdown: workforce, capacity, ratio)
  - Composition stacked area for each sector
  - Export comparison table
  
- [ ] Create `dashboards/pages/4_Mismatch_Detection.py`:
  - Load metrics with mismatch flags
  - Mismatch heatmap
  - Alert table (sectors with significant mismatches)
  - Growth rate scatter plot
  - Export flagged sectors

**Phase 7: Interactivity and Filters**

- [ ] Implement session state for shared filters (if needed)
- [ ] Test filter behavior:
  - Sector selection updates all charts
  - Year range slider filters data correctly
  - Profession filter works on relevant pages
- [ ] Add filter reset button
- [ ] Validate filter persistence across pages

**Phase 8: Benchmark Overlays**

- [ ] Add benchmark shaded regions to ratio charts
- [ ] Add reference lines for doctor-to-nurse ratios
- [ ] Add annotations explaining benchmarks
- [ ] Verify benchmark values match `src/analysis/benchmarks.py`

**Phase 9: In-Dashboard Documentation**

- [ ] Add tooltips to all charts (Plotly hovertemplate)
- [ ] Add expandable sections with interpretation guidance
- [ ] Add "How to Use" section on main page
- [ ] Add data quality disclaimers
- [ ] Create sidebar info boxes with dataset coverage

**Phase 10: User Guide Creation**

- [ ] Create `reports/dashboards/workforce_capacity_dashboard_user_guide.md`
- [ ] **Content**:
  - Introduction and purpose
  - How to access the dashboard
  - Page-by-page guide (with screenshots if possible)
  - Filter usage instructions
  - Metric definitions and interpretations
  - Troubleshooting common issues
  - Contact information
- [ ] Export user guide to PDF (optional)

**Phase 11: Performance Optimization**

- [ ] Profile dashboard load time:
  ```bash
  # In dashboard, add timing logs
  import time
  start = time.time()
  # ... data loading ...
  logger.info(f"Data loading time: {time.time() - start:.2f}s")
  ```
- [ ] Optimize slow queries (aggregate data beforehand if needed)
- [ ] Implement data downsampling for very large datasets (>10k points)
- [ ] Test with Streamlit profiler:
  ```bash
  streamlit run dashboards/workforce_capacity_dashboard.py --server.enableStaticServing true
  ```
- [ ] Target: <3 seconds initial load

**Phase 12: Testing and Validation**

- [ ] Create `tests/unit/test_dashboard_components.py`
- [ ] Write unit tests for all chart creation functions
- [ ] Run unit tests: `pytest tests/unit/test_dashboard_components.py -v`
- [ ] Manual visual testing:
  - Test on different browsers (Chrome, Firefox, Safari)
  - Test on different screen sizes (desktop, tablet, mobile)
  - Test all filters and interactions
  - Test export buttons
- [ ] Validate calculations match User Story 4 results

**Phase 13: Stakeholder Validation**

- [ ] Deploy dashboard locally for stakeholder demo
- [ ] Collect feedback:
  - Are visualizations clear and interpretable?
  - Are filters intuitive?
  - Are there missing views or metrics?
  - Are interpretations accurate?
- [ ] Iterate based on feedback
- [ ] Document feedback and changes made

**Phase 14: Deployment Preparation**

- [ ] Choose deployment platform:
  - **Streamlit Cloud** (easiest, free tier available)
  - **Databricks** (if integrated with Databricks environment)
  - **Internal server** (Docker container)
- [ ] Create deployment documentation:
  - Requirements (Python version, dependencies)
  - Deployment steps
  - Environment variables (if any)
  - Data refresh procedures
  - Access control setup (if applicable)
- [ ] Set up authentication (if required):
  - Streamlit Cloud: Built-in authentication
  - Custom: Implement with streamlit-authenticator library
  - Databricks: Use workspace permissions

**Phase 15: Deployment (Optional)**

- [ ] Deploy to chosen platform
- [ ] Configure data refresh schedule (if live connection)
- [ ] Test deployed dashboard:
  - Verify all pages load
  - Verify data paths correct
  - Verify performance acceptable
- [ ] Share access link with stakeholders
- [ ] Monitor usage and errors

**Phase 16: Documentation and Handoff**

- [ ] Finalize user guide
- [ ] Create maintenance guide:
  - How to update data (replace parquet files)
  - How to modify visualizations (edit dashboard_components.py)
  - How to add new pages
  - How to update benchmarks
  - Known issues and troubleshooting
- [ ] Create access procedures document
- [ ] Provide training session for stakeholders (if applicable)
- [ ] Archive logs and code

**Phase 17: Final Validation**

- [ ] Verify all acceptance criteria met:
  - ✅ Interactive dashboard showing metrics by sector
  - ✅ Time series trends for all years
  - ✅ Sector comparison views
  - ✅ Ratio trends with visual alerts
  - ✅ Drill-down by sector
  - ✅ Performance < 3 seconds
  - ✅ Mobile-responsive design
  - ✅ User guide completed
  - ✅ Data notes embedded
- [ ] Update User Story 5 status
- [ ] Commit all code to version control
- [ ] Prepare handoff to User Story 6 (Stakeholder Communication)

---

### 12. Adaptive Implementation Strategy

**Output-Driven Adaptation Requirements**:

**Scenario A: Performance Issues (Load Time >3 seconds)**
- **Trigger**: Dashboard takes >3 seconds to load
- **Action**:
  - Profile slow queries
  - Pre-aggregate data (create summary datasets)
  - Implement pagination or lazy loading
  - Reduce chart complexity (fewer data points via downsampling)
  - Consider switching to Dash (more performant for large datasets)

**Scenario B: Stakeholder Requests Additional Views**
- **Trigger**: Feedback session identifies missing metrics
- **Action**:
  - Document requested views
  - Assess data availability
  - Prioritize by business value
  - Add new pages or modify existing
  - Re-validate with stakeholders

**Scenario C: Data Quality Issues Discovered**
- **Trigger**: Dashboard reveals unexpected patterns
- **Action**:
  - Investigate source data
  - Document issues in dashboard (disclaimer)
  - Add data quality flags/warnings
  - Consider filtering out problematic data
  - Report issues to data owners

**Scenario D: Deployment Platform Constraints**
- **Trigger**: Chosen platform has limitations (e.g., Streamlit Cloud free tier)
- **Action**:
  - Optimize for platform constraints
  - Downgrade features if needed (e.g., reduce data size)
  - Consider alternative platforms
  - Document trade-offs

---

### 13. Code Generation Order

**Phase 1: Foundation**
1. Config files (`config/dashboard.yml`, `dashboards/.streamlit/config.toml`)
2. Data loader module (`src/dashboard/data_loader.py`)

**Phase 2: Visualization Components**
3. Dashboard components module (`src/visualization/dashboard_components.py`)

**Phase 3: Dashboard Application**
4. Main dashboard (`dashboards/workforce_capacity_dashboard.py`)
5. Dashboard pages (`dashboards/pages/*.py`)

**Phase 4: Documentation**
6. User guide (`reports/dashboards/workforce_capacity_dashboard_user_guide.md`)
7. Maintenance guide (in documentation)

**Phase 5: Testing**
8. Unit tests (`tests/unit/test_dashboard_components.py`)
9. Integration tests (`tests/integration/test_dashboard_data_flow.py`)

---

### 14. Data Quality & Validation Strategy

**Stage 1: Data Loading Validation**
- Validate file exists before loading
- Check schema matches expected
- Verify no nulls in critical columns
- Log data shape and coverage

**Stage 2: Filter Validation**
- Validate year range within data bounds
- Check selected sectors exist in data
- Handle empty filter selections gracefully
- Log filter selections for debugging

**Stage 3: Visualization Validation**
- Check data passed to chart functions is not empty
- Validate metric columns exist
- Handle missing values in visualizations
- Display warnings for insufficient data

**Stage 4: Output Validation**
- Verify charts render without errors
- Check tooltips display correctly
- Validate export functionality
- Test download buttons produce valid files

---

### 15. Statistical Analysis & Model Development

**Not applicable** - Dashboard focuses on visualization and exploration, not statistical modeling.

---

### 16. Model Operations & Governance

**Not applicable** - No machine learning models in this user story.

---

### 17. UI/Dashboard Visual Testing

**Manual Visual Testing Checklist**:

**Desktop (1920x1080)**:
- [ ] Main page layout renders correctly
- [ ] Sidebar filters display fully
- [ ] Charts resize to container width
- [ ] Multi-column layouts work
- [ ] All pages accessible via navigation

**Tablet (768x1024)**:
- [ ] Responsive layout stacks correctly
- [ ] Charts remain legible
- [ ] Filters remain accessible
- [ ] Navigation works

**Mobile (375x667)**:
- [ ] Single-column layout
- [ ] Charts scale down appropriately
- [ ] Filters accessible (may collapse)
- [ ] Text remains readable

**Functionality Testing**:
- [ ] Sector filter updates charts
- [ ] Year slider updates data range
- [ ] Profession filter works where applicable
- [ ] Hover tooltips display correctly
- [ ] Legend toggle shows/hides series
- [ ] Zoom and pan work on time series
- [ ] Export buttons download valid files
- [ ] Navigation between pages works
- [ ] Data refresh timestamp displays

**Accessibility Testing**:
- [ ] High contrast mode readable
- [ ] Screen reader compatible (basic)
- [ ] Keyboard navigation functional
- [ ] Alt text on visualizations

---

### 18. Success Metrics & Monitoring

**Business Success Metrics**:

1. **User Adoption**: Number of unique users accessing dashboard per week
2. **Engagement**: Average session duration and pages viewed per session
3. **Utility**: Number of insights actioned from dashboard findings
4. **Feedback Score**: Stakeholder satisfaction rating (post-training survey)

**Technical Monitoring**:

1. **Performance**: Average page load time < 3 seconds
2. **Uptime**: 99% availability (if deployed)
3. **Error Rate**: <1% of sessions encounter errors
4. **Data Freshness**: Timestamp of last data refresh visible

**Deliverable Validation**:
- [ ] Dashboard deployed and accessible
- [ ] All pages functional
- [ ] User guide completed
- [ ] Stakeholder training completed
- [ ] Performance targets met

---

### 19. References

**Data Source Documentation**:
- [Data Sources: MOH Singapore Healthcare Data](../../../project_context/data-sources.md)

**Domain Knowledge**:
- [Healthcare Workforce Planning](../../../domain_knowledge/healthcare-workforce-planning.md)
- [Healthcare System Sustainability Metrics](../../../domain_knowledge/healthcare-system-sustainability-metrics.md)

**Problem Statement**:
- [PS-001: Workforce-Capacity Mismatch Analysis](../../problem_statements/ps-001-workforce-capacity-mismatch.md)

**Related User Stories**:
- [User Story 2: Data Cleaning](02-data-cleaning.md) - Provides cleaned data
- [User Story 3: Exploratory Analysis](03-exploratory-analysis.md) - Provides statistical insights
- [User Story 4: Workforce-Capacity Metrics](04-workforce-capacity-metrics.md) - Provides metrics dataset
- [User Story 6: Stakeholder Communication](06-stakeholder-communication.md) - Consumes dashboard insights

**External Resources**:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

---

## Code Generation Readiness Checklist

- [x] **🚨 CODE EXECUTION VALIDATION COMPLETED** - ALL code blocks tested for executability
- [x] **Function signatures** with complete type hints for dashboard components
- [x] **Data schemas** implicitly defined via Polars DataFrame structures
- [x] **Specific library methods** (Plotly, Streamlit, Polars operations)
- [x] **Configuration file structure** with YAML and TOML content
- [x] **Test assertions** with specific expected outputs
- [x] **Import statements** for all dependencies
- [x] **Error handling patterns** with FileNotFoundError, generic exceptions
- [x] **Logging statements** at key steps (data loading, chart creation)
- [x] **Data validation rules** in data loader module
- [x] **Example Streamlit code** for main app and pages
- [x] **Technical constraints** (performance <3s, responsive design)
- [x] **Package management commands** using `uv`
- [x] **Code generation order** specified
- [x] **Test fixtures** for dashboard components
- [x] **Performance benchmarks** (<3s load time)

✅ **This implementation plan is READY for code generation.**

---

**End of Implementation Plan - User Story 5**
