# Profile High-Burden Demographic Segments (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-003-US-07  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P1 (High)  
**Effort Estimate**: M (4-5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner targeting interventions**,  
I want **to profile demographic segments with disproportionately high utilization to understand their specific capacity needs**,  
So that **I can design targeted capacity expansions and care programs for high-burden populations (e.g., elderly, chronic disease patients)**.

---

## 🎯 Acceptance Criteria

1. **High-burden segments identified**
   - Top 10 demographic groups by admission rate
   - Segments with >2x average utilization rate
   - Growth rates for high-burden segments
   - Demographic concentration metrics

2. **Segment profiling completed**
   - Utilization characteristics per segment
   - Temporal trends for each high-burden group
   - Facility type preferences/needs by demographic
   - Care intensity indicators (if data available)

3. **Recommendations generated**
   - Targeted capacity needs for high-burden segments
   - Specialized service requirements
   - Priority populations for intervention programs

4. **Deliverables**
   - Output: `results/tables/high_burden_demographic_profiles.csv`
   - Figures: Demographic burden distribution, segment trends
   - Policy brief: Targeted capacity recommendations

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Visualization**: Matplotlib/Seaborn
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#demographic-health-patterns) - Demographic utilization patterns
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objective-2) - Demographic utilization drivers

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `scikit-learn>=1.3.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-04 (Utilization demographics - BLOCKING)
- **Data Sources**: `shared/data/3_interim/capacity_utilization_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### High-Burden Identification
- [ ] Calculate average utilization rate across all demographics
- [ ] Identify segments with >2x average rate
- [ ] Rank demographics by absolute utilization
- [ ] Calculate utilization concentration (% from top segments)

### Segment Profiling
- [ ] Profile each high-burden segment: age, sex, trends
- [ ] Analyze growth rates for high-burden groups
- [ ] Cross-reference with facility utilization patterns
- [ ] Assess care intensity needs

### Recommendation Development
- [ ] Map demographic needs to facility types
- [ ] Estimate capacity requirements for high-burden groups
- [ ] Identify specialized service needs (geriatric care, chronic disease)
- [ ] Priority ranking for interventions

### Visualization
- [ ] Demographic burden distribution charts
- [ ] Trend lines for high-burden segments
- [ ] Concentration curve (Lorenz-style)
- [ ] Save figures: `reports/figures/demographic_profiling_*.png/pdf`

### Policy Brief
- [ ] Executive summary: key high-burden segments
- [ ] Detailed profiles for top 5 segments
- [ ] Capacity and service recommendations
- [ ] Implementation priorities

### Testing & Documentation
- [ ] Unit tests for profiling logic
- [ ] Validate burden calculations
- [ ] Docstrings
- [ ] Policy brief generation

---

## 📌 Notes

**Polars Profiling Example**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

# Calculate average utilization
avg_rate = df['admission_rate'].mean()

# Identify high-burden segments
df_high_burden = (
    df.filter(pl.col('admission_rate') > 2 * avg_rate)
    .sort('admission_rate', descending=True)
)

# Profile top segments
top_segments = df_high_burden.head(10)
```

**Expected High-Burden Segments**:
- **Elderly (75+)**: Likely highest utilization
- **Elderly males**: May have even higher rates
- **Middle-aged chronic disease patients**: Growing segment

**Capacity Recommendations**:
- **Geriatric care facilities**: Specialized elderly care
- **Chronic disease management**: Outpatient clinics
- **Rehabilitation**: Post-acute step-down care
