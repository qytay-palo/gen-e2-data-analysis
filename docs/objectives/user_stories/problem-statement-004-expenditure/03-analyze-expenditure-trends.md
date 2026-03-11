# Analyze 15-Year Expenditure Growth Patterns (Lifecycle Stage: Exploratory Data Analysis)

**Story ID**: PS-004-US-03  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financial Analyst assessing cost trends**,  
I want **to analyze 15-year government health expenditure growth patterns (2006-2018) including absolute growth, real vs nominal growth, and acceleration periods**,  
So that **I can understand historical cost dynamics and identify periods of exceptional expenditure growth or restraint**.

---

## 🎯 Acceptance Criteria

1. **Growth rates calculated**
   - Year-over-year growth rates (nominal and real terms)
   - Compound annual growth rate (CAGR) 2006-2018
   - Per capita expenditure growth trends
   - Inflation-adjusted real expenditure growth (if CPI data available)

2. **Trend analysis completed**
   - Identification of high-growth vs low-growth periods
   - Expenditure acceleration/deceleration detection
   - Comparison with GDP growth (if data available)
   - Expenditure as % of GDP trends (if GDP data available)

3. **Category-level analysis** (if expenditure categories available)
   - Growth rates by expenditure category
   - Category share changes over time
   - Fastest-growing expenditure categories identified

4. **Deliverables**
   - Output: `results/tables/expenditure_growth_analysis_2006_2018.csv`
   - Figures: Expenditure trends, growth rate charts
   - Summary report: Key expenditure evolution insights

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Visualization**: Matplotlib/Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-expenditure-analysis) - Expenditure trend methodologies
- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objective-1) - Expenditure growth objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-02 (Integrated expenditure data - BLOCKING)
- **Data Sources**: `shared/data/3_interim/expenditure_drivers_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Growth Calculations
- [ ] Calculate YoY expenditure growth: `(exp_t - exp_t-1) / exp_t-1 * 100`
- [ ] Calculate CAGR: `(end_exp / start_exp)^(1/years) - 1`
- [ ] Calculate per capita expenditure growth
- [ ] Adjust for inflation if CPI data available (real growth)

### Trend Analysis
- [ ] Identify high-growth periods (growth >5%)
- [ ] Identify low-growth or decline periods
- [ ] Detect acceleration/deceleration using second derivative
- [ ] Compare with economic indicators (if available)

### Category Analysis (if data supports)
- [ ] Calculate growth rates by category
- [ ] Analyze category share changes
- [ ] Identify fastest-growing categories

### Visualization
- [ ] Line chart: total expenditure over time
- [ ] Bar chart: YoY growth rates
- [ ] Area chart: expenditure by category (stacked)
- [ ] Save figures: `reports/figures/expenditure_trends_*.png/pdf`

### Testing & Documentation
- [ ] Unit tests for growth calculations
- [ ] Validate CAGR formula
- [ ] Docstrings
- [ ] Analysis summary report

---

## 📌 Notes

**Polars Growth Calculation**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/expenditure_drivers_integrated.parquet")

df_growth = df.sort('year').with_columns([
    ((pl.col('total_expenditure') - pl.col('total_expenditure').shift(1)) / 
     pl.col('total_expenditure').shift(1) * 100).alias('yoy_growth_pct')
])

# CAGR
start_exp = df.filter(pl.col('year') == 2006)['total_expenditure'][0]
end_exp = df.filter(pl.col('year') == 2018)['total_expenditure'][0]
years = 2018 - 2006
cagr = ((end_exp / start_exp) ** (1 / years) - 1) * 100
```

**Expected Insights**:
- Steady growth likely (healthcare costs typically rise with GDP)
- Possible acceleration post-2010 (aging population impact)
- Per capita growth may outpace total growth if population growth slow
