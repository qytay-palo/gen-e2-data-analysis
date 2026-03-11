# Identify Primary Cost Drivers & Inefficiencies (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-004-US-06  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financial Analyst prioritizing cost control initiatives**,  
I want **to identify primary cost drivers (demographic vs utilization vs intensity factors) and detect potential inefficiencies in expenditure patterns**,  
So that **I can recommend targeted cost containment strategies focusing on controllable drivers and inefficiencies**.

---

## 🎯 Acceptance Criteria

1. **Cost drivers decomposed**
   - Demographic effect quantified (population growth, aging)
   - Utilization effect quantified (volume of services)
   - Intensity effect quantified (cost per service)
   - Price effect quantified (if price index data available)

2. **Inefficiency indicators identified**
   - Cost outlier years flagged (unusually high expenditure vs utilization)
   - Efficiency metrics: cost per admission vs benchmarks
   - Productivity indicators: expenditure per healthcare worker (if workforce data integrated)

3. **Driver prioritization**
   - Primary drivers ranked by contribution to cost growth
   - Controllable vs uncontrollable drivers classified
   - High-leverage opportunities identified

4. **Deliverables**
   - Output: `results/tables/cost_driver_decomposition.csv`
   - Figures: Driver contribution charts, efficiency trends
   - Report: Cost driver analysis with action recommendations

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Analysis**: Custom decomposition algorithms or econometric methods
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#cost-decomposition-methods) - Cost driver decomposition frameworks
- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objective-4) - Identify cost drivers

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `scipy>=1.11.0`, `matplotlib>=3.8.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-05 (Correlation analysis - BLOCKING)
- **Data Sources**: `shared/data/3_interim/expenditure_drivers_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Cost Driver Decomposition
- [ ] Decompose expenditure growth into components
- [ ] Calculate demographic effect: population growth contribution
- [ ] Calculate utilization effect: admission volume contribution
- [ ] Calculate intensity effect: cost per admission contribution
- [ ] Sum decomposition: validate components sum to total growth

### Inefficiency Detection
- [ ] Flag outlier years: expenditure growth >> utilization growth
- [ ] Calculate efficiency metrics: cost per admission trends
- [ ] Compare with productivity: expenditure per healthcare worker
- [ ] Identify periods of declining efficiency

### Driver Prioritization
- [ ] Rank drivers by absolute contribution to cost growth
- [ ] Classify as controllable (intensity, efficiency) vs uncontrollable (demographics)
- [ ] Identify high-leverage interventions

### Visualization
- [ ] Waterfall chart: cost growth decomposition
- [ ] Trend charts: efficiency metrics over time
- [ ] Driver contribution pie/bar charts
- [ ] Save figures

### Testing & Documentation
- [ ] Unit tests for decomposition logic
- [ ] Validate decompositions sum correctly
- [ ] Docstrings
- [ ] Cost driver report

---

## 📌 Notes

**Decomposition Formula**:
```
Total Expenditure Change = 
  Population Effect + Utilization Effect + Intensity Effect + Interaction Terms

Where:
- Population Effect = ΔPopulation × Baseline per capita expenditure
- Utilization Effect = ΔUtilization per capita × Population × Baseline cost per unit
- Intensity Effect = ΔCost per unit × Utilization × Population
```

**Polars Implementation**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/expenditure_drivers_integrated.parquet")

# Calculate components
df = df.with_columns([
    (pl.col('population') - pl.col('population').shift(1)).alias('pop_change'),
    (pl.col('per_capita_utilization') - pl.col('per_capita_utilization').shift(1)).alias('util_change'),
    (pl.col('cost_per_admission') - pl.col('cost_per_admission').shift(1)).alias('intensity_change')
])

# Calculate contributions
df = df.with_columns([
    (pl.col('pop_change') * pl.col('per_capita_exp_baseline')).alias('pop_effect'),
    (pl.col('util_change') * pl.col('population') * pl.col('cost_baseline')).alias('util_effect'),
    (pl.col('intensity_change') * pl.col('utilization') * pl.col('population')).alias('intensity_effect')
])
```
