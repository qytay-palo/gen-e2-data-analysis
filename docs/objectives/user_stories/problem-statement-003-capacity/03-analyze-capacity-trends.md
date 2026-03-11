# Analyze 11-Year Capacity Evolution by Facility Type (Lifecycle Stage: Exploratory Data Analysis)

**Story ID**: PS-003-US-03  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner assessing infrastructure needs**,  
I want **to analyze how facility capacity evolved from 2009-2020 across acute care, community hospitals, long-term care, and primary care sectors**,  
So that **I can identify which facility types expanded rapidly, stagnated, or declined and understand capacity distribution between public and private sectors**.

---

## 🎯 Acceptance Criteria

1. **Capacity growth trends calculated**
   - Year-over-year capacity growth rates for each facility type
   - Compound annual growth rates (CAGR) 2009-2020
   - Absolute capacity changes: 2020 capacity - 2009 baseline
   - Growth volatility: standard deviation of annual growth rates

2. **Sector comparisons completed**
   - Public vs private capacity growth analyzed
   - Sector share trends: % of total beds in public vs private
   - Divergence analysis: facility types where public/private growth differs

3. **Capacity distribution analysis**
   - Capacity per capita: beds per 10,000 population (if population data available)
   - Facility type proportions: % of total capacity in acute vs community vs LTC
   - Identification of capacity concentration or diversification trends

4. **Deliverables produced**
   - Output: `results/tables/capacity_growth_analysis_2009_2020.csv`
   - Figures: Capacity trends by facility type, sector comparisons
   - Summary report: Key capacity evolution insights

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Visualization**: Matplotlib/Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-capacity-metrics) - Capacity benchmarks
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objective-1) - Capacity quantification objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-02 (Clean capacity data - BLOCKING)
- **Data Sources**: `shared/data/3_interim/capacity_utilization_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Growth Rate Calculations
- [ ] Calculate YoY growth: `(capacity_t - capacity_t-1) / capacity_t-1 * 100`
- [ ] Calculate CAGR: `(end_capacity / start_capacity)^(1/years) - 1`
- [ ] Compute growth statistics per facility type
- [ ] Identify years with exceptional growth or contraction

### Sector Analysis
- [ ] Compare public vs private growth rates
- [ ] Calculate sector share over time
- [ ] Statistical tests for growth differences
- [ ] Identify sector-specific trends

### Capacity Distribution
- [ ] Calculate total capacity by facility type per year
- [ ] Compute proportional distribution
- [ ] Analyze shifts in capacity mix
- [ ] Assess concentration vs diversification

### Visualization
- [ ] Line charts: capacity over time by facility type
- [ ] Stacked area: proportional capacity by facility type
- [ ] Bar charts: CAGR comparisons
- [ ] Sector comparison charts
- [ ] Save figures: `reports/figures/capacity_trends_*.png/pdf`

### Testing & Documentation
- [ ] Unit tests for growth calculations
- [ ] Validation: growth rates calculated correctly
- [ ] Docstrings for all functions
- [ ] Analysis summary report

---

## 📌 Notes

**Polars Growth Calculation**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

df_growth = (
    df.sort(['facility_category', 'sector', 'year'])
    .with_columns([
        ((pl.col('capacity_metric') - pl.col('capacity_metric').shift(1)) / 
         pl.col('capacity_metric').shift(1) * 100)
        .over(['facility_category', 'sector'])
        .alias('yoy_growth_pct')
    ])
)

# CAGR
df_cagr = (
    df.group_by(['facility_category', 'sector']).agg([
        pl.col('capacity_metric').first().alias('start_capacity'),
        pl.col('capacity_metric').last().alias('end_capacity'),
        (pl.col('year').max() - pl.col('year').min()).alias('years')
    ])
    .with_columns([
        ((pl.col('end_capacity') / pl.col('start_capacity')) ** (1 / pl.col('years')) - 1) * 100
        .alias('cagr_pct')
    ])
)
```

**Expected Insights**:
- **Acute Care**: Likely moderate growth (established infrastructure)
- **Community Hospitals**: Possibly rapid growth (policy push for intermediate care)
- **Long-Term Care**: Likely high growth (aging population)
- **Primary Care**: Steady growth (population increase)
