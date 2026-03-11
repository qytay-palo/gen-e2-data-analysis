# Build Healthcare Expenditure Analysis Dashboard (Lifecycle Stage: Visualization)

**Story ID**: PS-004-US-09  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: L (7-8 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financial Planner tracking expenditure trends**,  
I want **an interactive dashboard displaying 15-year expenditure trends, driver decomposition, benchmarking, and cost control opportunities**,  
So that **I can monitor cost dynamics, explore drivers interactively, and communicate financial insights to budget committees and policymakers**.

---

## 🎯 Acceptance Criteria

1. **Core visualizations**
   - Expenditure trends: total, per capita, growth rates (2006-2018)
   - Driver decomposition: demographic, utilization, intensity contributions
   - Correlation analysis: expenditure vs utilization/demographics
   - Benchmarking: Singapore vs OECD comparisons
   - Cost control opportunities: priority matrix, savings potential

2. **Interactive features**
   - Year range slider
   - Metric selector: total expenditure, per capita, % GDP
   - Driver toggle: show/hide decomposition components
   - Benchmark toggle: overlay international comparisons
   - Opportunity filter: by category, savings potential

3. **User experience**
   - Responsive design
   - Tooltips with detailed metrics
   - Export: charts (PNG/PDF), data (CSV)
   - Auto-generated insights
   - Help documentation

4. **Deployment**
   - Dashboard deployed and accessible
   - User documentation provided
   - Code documentation

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9; Dash/Plotly deployed on cloud
- **Primary Library**: Plotly Dash
- **Data Backend**: Polars 0.20+
- **Visualization**: Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md) - Dashboard objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `plotly>=5.18.0`, `dash>=2.14.0`, `dash-bootstrap-components>=1.5.0`, `gunicorn>=21.0.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-03 through PS-004-US-08 (All analyses - BLOCKING)
- **Data Sources**: All PS-004 results tables
- **Config Files**: `config/dashboard.yml`

---

## ✅ Implementation Tasks

### Dashboard Architecture
- [ ] Initialize Dash app
- [ ] Design multi-tab layout: Overview, Trends, Drivers, Benchmarking, Opportunities
- [ ] Data loading and caching
- [ ] Component hierarchy

### Core Visualizations
- [ ] Expenditure trends: line charts
- [ ] Driver decomposition: waterfall/stacked bar
- [ ] Correlation: scatter plots
- [ ] Benchmarking: bar/line comparisons
- [ ] Opportunities: priority matrix

### Interactivity
- [ ] Year range slider
- [ ] Metric selector dropdown
- [ ] Driver component toggles
- [ ] Benchmark comparison toggle
- [ ] Opportunity filters

### Data Callbacks
- [ ] Filter data based on selections
- [ ] Update charts
- [ ] Generate narratives
- [ ] Export functionality

### Styling & UX
- [ ] Bootstrap theme
- [ ] Tooltips
- [ ] Loading spinners
- [ ] Error handling

### Deployment
- [ ] Dockerize
- [ ] Deploy to cloud
- [ ] HTTPS and authentication
- [ ] Performance optimization

### Testing & Documentation
- [ ] Unit tests
- [ ] Integration tests
- [ ] User guide
- [ ] Technical documentation

---

## 📌 Notes

**Dashboard Tabs**:
1. **Overview**: Key metrics, summary statistics
2. **Trends**: Expenditure growth over time
3. **Drivers**: Decomposition and correlation analysis
4. **Benchmarking**: International comparisons
5. **Opportunities**: Cost control initiatives
6. **About**: Methodology, glossary

**Key Features**:
- **Trend Extrapolation**: Project future expenditure based on historical trends
- **Driver Simulator**: Adjust utilization/demographics, see expenditure impact
- **Savings Calculator**: Select opportunities, estimate total savings
