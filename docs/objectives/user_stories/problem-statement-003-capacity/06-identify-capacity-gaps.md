# Identify Capacity Gaps by Facility Type (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-003-US-06  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner prioritizing infrastructure investments**,  
I want **to identify capacity shortages and surpluses by comparing capacity growth vs utilization growth trends across facility types**,  
So that **I can recommend targeted capacity expansion for under-resourced facilities and identify over-capacity situations for reallocation**.

---

## 🎯 Acceptance Criteria

1. **Gap analysis completed**
   - Capacity-utilization gap calculated: capacity growth vs utilization growth spread
   - Shortage identification: facility types where utilization outpaces capacity
   - Surplus identification: facility types with excess capacity vs demand
   - Gap severity ranked: critical, moderate, minimal

2. **Temporal gap evolution analyzed**
   - Historical gap trends: widening or narrowing over time
   - Inflection points: years when gaps emerged or resolved
   - Forecast implications: projected gaps if trends continue

3. **Sector-specific gaps assessed**
   - Public sector gaps vs private sector gaps
   - Cross-sector opportunities: can private capacity fill public gaps?
   - Sector balance recommendations

4. **Deliverables**
   - Output: `results/tables/capacity_gap_analysis.csv`
   - Figures: Gap charts, capacity vs utilization trends
   - Priority recommendations: Facility types needing expansion

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Visualization**: Matplotlib/Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#capacity-planning-methods) - Gap analysis methodologies
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objective-3) - Identify capacity gaps

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `matplotlib>=3.8.0`, `plotly>=5.18.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-03, PS-003-US-04 (Capacity and utilization analyses - BLOCKING)
- **Data Sources**: `shared/data/3_interim/capacity_utilization_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Gap Calculation
- [ ] Calculate capacity growth rate per facility type
- [ ] Calculate utilization growth rate per facility type
- [ ] Compute gap metric: utilization growth - capacity growth
- [ ] Classify gaps: positive = shortage, negative = surplus
- [ ] Rank gaps by severity

### Temporal Analysis
- [ ] Analyze gap trends over time
- [ ] Identify when gaps emerged or widened
- [ ] Detect inflection points
- [ ] Simple extrapolation: project future gaps

### Sector Analysis
- [ ] Calculate public vs private gaps
- [ ] Assess cross-sector reallocation opportunities
- [ ] Recommend sector-specific expansions

### Prioritization
- [ ] Priority matrix: gap severity vs interventionability
- [ ] Rank facility types needing expansion
- [ ] Identify low-priority capacity (surplus areas)

### Visualization
- [ ] Line charts: capacity vs utilization trends
- [ ] Gap charts: showing shortage/surplus by facility type
- [ ] Priority matrix scatter plot
- [ ] Save figures: `reports/figures/capacity_gaps_*.png/pdf`

### Testing & Documentation
- [ ] Unit tests for gap calculations
- [ ] Validate gap classification logic
- [ ] Docstrings
- [ ] Gap analysis report with recommendations

---

## 📌 Notes

**Polars Gap Analysis**:
```python
import polars as pl

df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

# Calculate growth rates
df_growth = df.group_by('facility_category').agg([
    ((pl.col('capacity_metric').last() / pl.col('capacity_metric').first()) - 1).alias('capacity_growth'),
    ((pl.col('utilization_metric').last() / pl.col('utilization_metric').first()) - 1).alias('utilization_growth')
])

# Gap = utilization growth - capacity growth
df_gaps = df_growth.with_columns([
    (pl.col('utilization_growth') - pl.col('capacity_growth')).alias('gap')
])

# Classify gaps
df_gaps = df_gaps.with_columns([
    pl.when(pl.col('gap') > 0.1).then('critical_shortage')
      .when(pl.col('gap') > 0.05).then('moderate_shortage')
      .when(pl.col('gap') < -0.05).then('surplus')
      .otherwise('balanced')
      .alias('gap_classification')
])
```

**Gap Severity Thresholds**:
- **Critical Shortage**: utilization growth > capacity growth by >10%
- **Moderate Shortage**: 5-10% gap
- **Balanced**: gap within ±5%
- **Surplus**: capacity growth > utilization growth by >5%

**Expected Findings**:
- **Acute Care**: Likely balanced or slight shortage
- **Community Hospitals**: Possible expansion aligned with utilization
- **Long-Term Care**: Likely shortage (aging population driving demand)
- **Primary Care**: May have surplus in some areas
