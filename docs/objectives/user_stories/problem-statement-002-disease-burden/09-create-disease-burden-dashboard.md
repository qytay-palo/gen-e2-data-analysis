# Build Disease Burden Trends Explorer Dashboard (Lifecycle Stage: Visualization)

**Story ID**: PS-002-US-09  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: L (7-8 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Policy Maker tracking disease burden trends**,  
I want **an interactive dashboard displaying 30-year mortality trends with drill-down capabilities, trend comparisons, and international benchmarking**,  
So that **I can explore disease patterns dynamically, share insights with stakeholders, and inform policy decisions with real-time data visualization**.

---

## 🎯 Acceptance Criteria

1. **Core visualization features implemented**
   - Interactive time series charts: mortality rates 1990-2019 with selectable diseases
   - Trend comparison view: overlay multiple diseases on single chart
   - Joinpoint visualization: trend segments highlighted with slope annotations
   - Heat map: year × disease matrix showing mortality rate changes
   - Filters: disease selection, year range slider, view modes (absolute vs relative change)

2. **Advanced analytics integrated**
   - Trend statistics panel: APC, CAGR, trend direction for selected disease
   - International benchmarking: toggle to overlay Singapore vs WHO/OECD averages
   - Priority matrix: interactive scatter plot (burden vs urgency) with clickable disease points
   - Predictive preview: simple linear extrapolation showing next 5 years trend

3. **User experience & interactivity**
   - Responsive design: works on desktop and tablets
   - Tooltips: hover over data points for detailed statistics
   - Download capabilities: export charts as PNG/PDF, data as CSV
   - Narrative insights: auto-generated text summaries for selected trends
   - Help documentation: embedded user guide and methodology explanations

4. **Deployment & documentation**
   - Dashboard deployed: Plotly Dash app running on Databricks or cloud platform
   - Access URL: shared with MOH stakeholders
   - User documentation: PDF guide with screenshots and feature descriptions
   - Code documentation: README with setup and customization instructions

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9; Dash/Plotly deployed on cloud (AWS/Azure)
- **Primary Library**: Plotly Dash for interactive web application
- **Data Backend**: Polars 0.20+ for fast data queries
- **Visualization**: Plotly Express/Graph Objects for charts
- **Logging**: loguru for application monitoring
- **Testing**: pytest with ≥80% coverage for dashboard logic; UI testing with Selenium (optional)

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md) - Metrics displayed in dashboard
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md) - Dashboard objectives and stakeholder needs

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Backend data processing
- `plotly>=5.18.0`: Interactive visualizations
- `dash>=2.14.0`: Web application framework
- `dash-bootstrap-components>=1.5.0`: Responsive UI components
- `gunicorn>=21.0.0`: Production WSGI server
- `loguru>=0.7.0`: Application logging

### Internal Dependencies
- **Upstream**: PS-002-US-03 through PS-002-US-08 (All prior analyses - BLOCKING)
- **Data Sources**: 
  - `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
  - `results/tables/mortality_trend_changepoints.csv`
  - `results/tables/disease_burden_prioritization_matrix.csv`
  - `results/tables/international_mortality_benchmarking.csv`
- **Config Files**: `config/dashboard.yml` (styling, layout, deployment settings)

---

## ✅ Implementation Tasks

### Dashboard Architecture
- [ ] Initialize Dash application structure
- [ ] Design page layout: header, sidebar filters, main content area, footer
- [ ] Create component hierarchy: filters → data callbacks → visualizations
- [ ] Implement data loading: cache Parquet files for fast access
- [ ] Set up routing: multi-page dashboard (overview, details, benchmarking, prioritization)

### Core Visualizations
- [ ] **Trend Time Series**: Line chart with disease selector and year range slider
- [ ] **Multi-Disease Comparison**: Overlaid line chart comparing selected diseases
- [ ] **Joinpoint Segments**: Annotated segmented regression with APC labels
- [ ] **Heat Map**: Year × disease matrix colored by mortality rate
- [ ] **Rate of Change Charts**: Bar chart showing APC by disease

### Advanced Analytics Views
- [ ] **Benchmarking Panel**: Singapore vs WHO vs high-income comparison chart
- [ ] **Priority Matrix**: Scatter plot (burden vs urgency) with disease labels
- [ ] **Trend Decomposition**: Stacked area chart showing proportional burden
- [ ] **Forecast Preview**: Dotted line extending trends 5 years into future

### Interactivity & Filters
- [ ] Disease multi-select dropdown (cancer, stroke, IHD, all)
- [ ] Year range slider (1990-2019)
- [ ] View mode toggle: absolute rates vs % change from baseline
- [ ] Benchmark toggle: show/hide international comparisons
- [ ] Annotation controls: show/hide APC values, joinpoints, confidence bands

### Data Callbacks
- [ ] Callback: filter data based on selected diseases and year range
- [ ] Callback: update all charts when filters change
- [ ] Callback: generate narrative insights based on selected disease
- [ ] Callback: export chart to PNG/PDF on button click
- [ ] Callback: download filtered data as CSV

### Narrative Insights (Auto-Generated)
- [ ] Template-based text generation: "Cancer mortality declined X% from 1990-2019..."
- [ ] Trend classification: "This represents a steady decline..."
- [ ] Benchmark comparison: "Singapore's rate is Y% below WHO average..."
- [ ] Priority assessment: "This disease ranks #Z in priority..."

### Styling & UX
- [ ] Apply Bootstrap theme (e.g., "COSMO" or "FLATLY" for professional look)
- [ ] Color scheme: consistent with MOH branding (if applicable)
- [ ] Tooltips: informative hover text on all chart elements
- [ ] Loading spinners: show while data updates
- [ ] Error handling: graceful messages for missing data or filters

### Deployment
- [ ] Containerize with Docker: create Dockerfile for reproducible deployment
- [ ] Deploy to cloud: AWS Elastic Beanstalk, Azure App Service, or Databricks Apps
- [ ] Configure HTTPS: secure dashboard access
- [ ] Set up authentication: basic auth or OAuth for MOH users
- [ ] Performance optimization: caching, lazy loading for large datasets

### Testing & Validation
- [ ] Unit tests for data callback functions
- [ ] Integration tests for end-to-end dashboard workflows
- [ ] UI testing: Selenium tests for key interactions (optional)
- [ ] Load testing: ensure dashboard handles concurrent users
- [ ] User acceptance testing: gather feedback from stakeholders

### Documentation
- [ ] User guide: PDF with screenshots, feature descriptions, use cases
- [ ] Technical documentation: README with setup, deployment, customization
- [ ] Code comments: docstrings for all callbacks and functions
- [ ] Video tutorial: 5-minute walkthrough (optional)

---

## 📌 Notes

**Dash Application Structure Example**:
```python
import polars as pl
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from loguru import logger

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# Load data
df = pl.read_parquet("shared/data/3_interim/mortality_trends_integrated_clean.parquet")

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Disease Burden Trends Explorer"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Diseases:"),
            dcc.Dropdown(
                id='disease-selector',
                options=[{'label': d, 'value': d} for d in df['disease_category'].unique()],
                value=['cancer'],
                multi=True
            ),
            html.Label("Year Range:"),
            dcc.RangeSlider(
                id='year-slider',
                min=1990, max=2019, step=1,
                value=[1990, 2019],
                marks={y: str(y) for y in range(1990, 2020, 5)}
            )
        ], width=3),
        dbc.Col([
            dcc.Graph(id='trend-chart')
        ], width=9)
    ])
])

# Callback: update chart based on filters
@callback(
    Output('trend-chart', 'figure'),
    Input('disease-selector', 'value'),
    Input('year-slider', 'value')
)
def update_chart(selected_diseases, year_range):
    # Filter data
    df_filtered = (
        df.filter(pl.col('disease_category').is_in(selected_diseases))
        .filter(pl.col('year').is_between(year_range[0], year_range[1]))
    )
    
    # Create chart
    fig = px.line(
        df_filtered.to_pandas(),
        x='year', y='mortality_rate',
        color='disease_category',
        title='Mortality Trends',
        labels={'mortality_rate': 'Mortality Rate (per 100k)', 'year': 'Year'}
    )
    
    logger.info(f"Chart updated: diseases={selected_diseases}, years={year_range}")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
```

**Dashboard Pages/Tabs**:
1. **Overview**: Key trends at a glance, summary statistics
2. **Trend Explorer**: Interactive time series with drill-down
3. **International Benchmarking**: Comparison with global standards
4. **Prioritization**: Priority matrix and resource allocation recommendations
5. **About/Methodology**: Data sources, methods, glossary

**Key Features**:
- **Responsiveness**: Use Bootstrap grid system for mobile-friendly layout
- **Performance**: Precompute summary statistics; use Polars for fast filtering
- **Accessibility**: Color-blind friendly palettes; alt text for charts
- **Export**: Download visible data, export charts for presentations

**Deployment Options**:
1. **Databricks Apps** (if available): Deploy directly on Databricks platform
2. **AWS Elastic Beanstalk**: Simple Python app deployment
3. **Docker + Cloud Run (GCP)**: Containerized deployment
4. **Heroku**: Quick prototyping and sharing

**Authentication**:
```python
# Basic authentication
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'moh_analyst': 'secure_password'
}

dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
```

**Caching for Performance**:
```python
from dash import callback_context
import functools

@functools.lru_cache(maxsize=32)
def load_data(disease):
    """Cache data loading for faster repeated access"""
    return pl.read_parquet(f"data/disease_{disease}.parquet")
```

**Export Functionality**:
```python
@callback(
    Output('download-data', 'data'),
    Input('export-button', 'n_clicks'),
    State('disease-selector', 'value')
)
def export_data(n_clicks, selected_diseases):
    if n_clicks:
        df_export = df.filter(pl.col('disease_category').is_in(selected_diseases))
        return dcc.send_data_frame(df_export.to_pandas().to_csv, "mortality_trends.csv")
```

**Expected User Workflows**:
1. **Quick overview**: Load dashboard → see all trends at a glance
2. **Deep dive**: Select specific disease → adjust year range → examine joinpoints
3. **Comparison**: Select multiple diseases → compare relative burden over time
4. **Benchmarking**: Toggle benchmarks → see Singapore vs WHO
5. **Export**: Download filtered data → create custom reports externally

**Success Metrics**:
- Dashboard loads in < 3 seconds
- Chart updates in < 1 second after filter change
- Mobile-responsive (works on tablets)
- Positive user feedback from stakeholders (>80% satisfaction)
