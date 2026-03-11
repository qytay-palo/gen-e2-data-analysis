# Build Healthcare Capacity Planning Dashboard (Lifecycle Stage: Visualization)

**Story ID**: PS-003-US-10  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: L (8 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner tracking capacity dynamics**,  
I want **an interactive dashboard showing capacity trends, utilization patterns, gap analysis, and scenario comparisons**,  
So that **I can explore capacity data dynamically, monitor evolving gaps, and communicate infrastructure needs to stakeholders and budget committees**.

---

## 🎯 Acceptance Criteria

1. **Core dashboard features**
   - Capacity trends: line charts by facility type and sector (2009-2020)
   - Utilization patterns: demographic breakdowns, temporal trends
   - Gap visualization: shortage/surplus indicators by facility type
   - Scenario comparison: side-by-side scenario outcomes
   - Filters: facility type, sector, year range, demographics

2. **Advanced analytics**
   - Occupancy rate estimator: capacity vs utilization ratio calculator
   - Gap severity indicators: color-coded alerts (red/yellow/green)
   - Demographic drill-down: utilization by age/sex with selection
   - Scenario simulator: adjust expansion parameters interactively

3. **User experience**
   - Responsive design: desktop and tablet compatible
   - Interactive tooltips: hover for detailed metrics
   - Export capabilities: charts (PNG/PDF), data (CSV)
   - Auto-generated insights: narrative summaries for selected views
   - Help & documentation: embedded methodology guide

4. **Deployment**
   - Dashboard deployed and accessible to MOH stakeholders
   - User documentation provided
   - Code documentation and setup guide

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9; Dash/Plotly deployed on cloud
- **Primary Library**: Plotly Dash for web application
- **Data Backend**: Polars 0.20+ for fast queries
- **Visualization**: Plotly Express/Graph Objects
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage for dashboard logic

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#capacity-metrics) - Dashboard metrics
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md) - Dashboard objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `plotly>=5.18.0`, `dash>=2.14.0`, `dash-bootstrap-components>=1.5.0`, `gunicorn>=21.0.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-03 through PS-003-US-09 (All prior analyses - BLOCKING)
- **Data Sources**: 
  - `shared/data/3_interim/capacity_utilization_integrated.parquet`
  - `results/tables/capacity_gap_analysis.csv`
  - `results/tables/capacity_expansion_scenarios.csv`
- **Config Files**: `config/dashboard.yml`

---

## ✅ Implementation Tasks

### Dashboard Architecture
- [ ] Initialize Dash application
- [ ] Design multi-tab layout: Overview, Capacity, Utilization, Gaps, Scenarios
- [ ] Implement data loading and caching
- [ ] Set up component hierarchy and callbacks

### Core Visualizations
- [ ] **Capacity Trends**: Line chart with facility type selector
- [ ] **Utilization Patterns**: Demographic heatmaps and time series
- [ ] **Gap Analysis**: Bar chart showing shortage/surplus by facility
- [ ] **Scenario Comparison**: Multi-scenario overlay charts

### Interactive Features
- [ ] Facility type multi-select dropdown
- [ ] Sector filter (public/private/all)
- [ ] Year range slider
- [ ] Demographic filters (age group, sex)
- [ ] Scenario selector for comparison view

### Advanced Analytics
- [ ] Occupancy calculator: dynamic ratio display
- [ ] Gap severity alerts: color-coded indicators
- [ ] Demographic drill-down: click to expand details
- [ ] Scenario simulator: slider to adjust expansion parameters

### Data Callbacks
- [ ] Filter data based on user selections
- [ ] Update all charts on filter change
- [ ] Generate narrative insights dynamically
- [ ] Export functionality for charts and data

### Styling & UX
- [ ] Apply Bootstrap theme for professional look
- [ ] Consistent color scheme (align with MOH branding if applicable)
- [ ] Tooltips on all interactive elements
- [ ] Loading indicators
- [ ] Error handling and graceful degradation

### Deployment
- [ ] Dockerize application
- [ ] Deploy to cloud platform (AWS/Azure/GCP)
- [ ] Configure HTTPS and authentication
- [ ] Performance optimization: caching, lazy loading

### Testing & Validation
- [ ] Unit tests for callback functions
- [ ] Integration tests for workflow
- [ ] Load testing for concurrent users
- [ ] User acceptance testing with stakeholders

### Documentation
- [ ] User guide (PDF with screenshots)
- [ ] Technical README (setup, deployment)
- [ ] Code comments and docstrings
- [ ] Video tutorial (optional)

---

## 📌 Notes

**Dash Application Example**:
```python
import polars as pl
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Healthcare Capacity Planning Dashboard"))]),
    dbc.Row([
        dbc.Col([
            html.Label("Facility Type:"),
            dcc.Dropdown(
                id='facility-selector',
                options=[{'label': f, 'value': f} for f in df['facility_category'].unique()],
                value=['acute_care'],
                multi=True
            )
        ], width=3),
        dbc.Col([dcc.Graph(id='capacity-trend')], width=9)
    ])
])

@app.callback(
    Output('capacity-trend', 'figure'),
    Input('facility-selector', 'value')
)
def update_capacity_chart(facilities):
    df_filtered = df.filter(pl.col('facility_category').is_in(facilities))
    fig = px.line(df_filtered.to_pandas(), x='year', y='capacity_metric', 
                  color='facility_category', title='Capacity Trends')
    return fig
```

**Dashboard Tabs**:
1. **Overview**: Executive summary, key metrics at a glance
2. **Capacity**: Capacity trends and growth analysis
3. **Utilization**: Demographic patterns and trends
4. **Gaps**: Shortage/surplus analysis with priority indicators
5. **Scenarios**: Scenario comparison and decision support
6. **About**: Methodology, data sources, definitions

**Key Features**:
- **Gap Alerts**: Red (critical shortage), Yellow (moderate), Green (balanced)
- **Scenario Simulator**: Adjust bed additions, see impact on occupancy
- **Demographic Drill-Down**: Click demographic segment to see details
- **Export**: Download filtered data and charts for offline use

**Performance Optimization**:
- Cache loaded data using Dash caching
- Lazy load large datasets
- Precompute summary statistics
- Use Polars for fast filtering

**Authentication** (example with basic auth):
```python
import dash_auth

VALID_USERS = {'moh_planner': 'secure_password'}
dash_auth.BasicAuth(app, VALID_USERS)
```
