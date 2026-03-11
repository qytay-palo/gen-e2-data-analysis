# Analyze Utilization Patterns by Demographics (Lifecycle Stage: Exploratory Data Analysis)

**Story ID**: PS-003-US-04  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner understanding demand drivers**,  
I want **to analyze hospital admission patterns by age, sex, and demographic groups from 2006-2020 to identify high-burden populations**,  
So that **I can understand which demographic segments drive utilization and inform capacity planning for aging populations or specific groups**.

---

## 🎯 Acceptance Criteria

1. **Demographic utilization profiles created**
   - Admission rates calculated by age group and sex
   - Highest-utilizing demographics identified
   - Age-sex pyramids for admission rates
   - Temporal trends: how demographic utilization changed over time

2. **Growth analysis by demographics**
   - Fastest-growing demographic segments identified
   - Aging population impact quantified
   - Sex differentials analyzed
   - Cohort effects identified (if visible in data)

3. **Utilization concentration metrics**
   - Top demographic segments contributing to total admissions
   - Concentration indices: % of admissions from specific age/sex groups
   - Dependency ratios: elderly utilization vs working-age utilization

4. **Deliverables**
   - Output: `results/tables/utilization_demographic_profiles.csv`
   - Figures: Age-sex pyramids, demographic trends
   - Summary: High-burden populations report

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Visualization**: Matplotlib/Seaborn
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-utilization-patterns) - Demographic utilization patterns
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objective-2) - Assess utilization patterns

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-02 (Clean utilization data - BLOCKING)
- **Data Sources**: `shared/data/3_interim/capacity_utilization_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Demographic Profiling
- [ ] Aggregate admission rates by age group and sex
- [ ] Identify highest-utilizing demographics
- [ ] Calculate demographic shares of total utilization
- [ ] Create age-sex stratified summary tables

### Temporal Trends
- [ ] Analyze utilization trends by demographic group
- [ ] Identify fastest-growing segments
- [ ] Compare 2006 vs 2020 demographic profiles
- [ ] Detect shifts in utilization patterns

### Concentration Analysis
- [ ] Calculate top demographics contributing to admissions
- [ ] Compute concentration indices
- [ ] Assess elderly vs working-age utilization
- [ ] Dependency ratio calculations

### Visualization
- [ ] Create age-sex pyramids for utilization
- [ ] Line charts: utilization trends by age group
- [ ] Heatmaps: age × year utilization matrix
- [ ] Save figures: `reports/figures/utilization_demographics_*.png/pdf`

### Testing & Documentation
- [ ] Unit tests for demographic calculations
- [ ] Validate aggregations
- [ ] Docstrings
- [ ] High-burden populations summary report

---

## 📌 Notes

**Polars Demographic Analysis**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

# Demographic profiles
df_demo = (
    df.group_by(['year', 'age_group', 'sex']).agg([
        pl.col('admission_rate').sum().alias('total_admission_rate')
    ])
    .with_columns([
        pl.col('total_admission_rate').rank(descending=True).over('year').alias('rank')
    ])
)

# Identify high-burden demographics
high_burden = df_demo.filter(pl.col('rank') <= 5)
```

**Expected Findings**:
- **Elderly (65+)**: Highest admission rates
- **Sex patterns**: Males may have higher utilization for certain age groups
- **Growth**: Elderly utilization likely growing fastest (population aging)
