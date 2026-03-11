# Disease Burden Prioritization Framework (Lifecycle Stage: Feature Engineering & Insights)

**Story ID**: PS-002-US-07  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (4-5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Policy Director allocating program budgets**,  
I want **to rank diseases by burden magnitude, trend urgency, and interventionability to create an evidence-based prioritization framework**,  
So that **I can justify resource allocation decisions with objective criteria and focus investments on highest-impact opportunities**.

---

## 🎯 Acceptance Criteria

1. **Multi-criteria prioritization model developed**
   - Burden magnitude score: based on absolute mortality rate and years of life lost
   - Trend urgency score: based on annual percentage change and acceleration
   - Interventionability score: expert assessment of preventability and treatment effectiveness
   - Composite priority score: weighted combination of three dimensions

2. **Disease rankings generated**
   - Overall priority ranking: diseases ordered by composite score
   - Dimension-specific rankings: separate rankings for burden, trend, interventionability
   - Priority quadrants: high burden + increasing vs high burden + declining, etc.
   - Top 5 priority diseases identified for immediate action

3. **Resource allocation recommendations**
   - Investment increase recommendations: diseases needing more resources
   - Investment maintenance: diseases with adequate resources
   - Investment reallocation opportunities: over-resourced diseases
   - Quantified budget implications: suggested % changes based on priority scores

4. **Deliverables produced**
   - Output file: `results/tables/disease_burden_prioritization_matrix.csv`
   - Priority quadrant visualization: scatter plot (burden vs trend urgency)
   - Executive scorecard: top priorities with justification
   - Policy brief: Evidence-based resource allocation recommendations (8-10 pages)

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for scoring and ranking
- **Multi-Criteria Analysis**: Custom scoring framework or AHP (Analytic Hierarchy Process)
- **Visualization**: Matplotlib/Plotly for priority matrices
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage for scoring functions

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#disability-adjusted-life-years-dalys) - Understanding DALY calculations for burden assessment
- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md) - Prioritization frameworks in public health
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md#objective-4) - Objective: Generate actionable prioritization insights

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Scoring and ranking analytics
- `scikit-learn>=1.3.0`: Normalization and scoring utilities
- `matplotlib>=3.8.0`: Priority matrix visualizations
- `seaborn>=0.13.0`: Heatmaps and quadrant plots
- `loguru>=0.7.0`: Structured logging

### Internal Dependencies
- **Upstream**: PS-002-US-03, PS-002-US-04, PS-002-US-05 (All trend analyses - BLOCKING)
- **Data Sources**: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
- **Config Files**: `config/analysis.yml` (scoring weights, priority thresholds)

---

## ✅ Implementation Tasks

### Dimension 1: Burden Magnitude Scoring
- [ ] Calculate absolute burden: latest year (2019) mortality rate
- [ ] Estimate years of life lost (YLL): mortality rate × average years lost per death
- [ ] Normalize burden scores to 0-100 scale (min-max normalization)
- [ ] Weight by population impact: consider prevalence if data available

### Dimension 2: Trend Urgency Scoring
- [ ] Extract annual percentage change (APC) from previous analysis
- [ ] Assign urgency points: increasing trends = higher urgency
- [ ] Factor in trend acceleration: rapidly increasing > slowly increasing
- [ ] Penalty for declining trends: stable or improving = lower urgency
- [ ] Normalize urgency scores to 0-100 scale

### Dimension 3: Interventionability Scoring
- [ ] Define interventionability dimensions: preventability, treatability, cost-effectiveness
- [ ] Expert assessment: gather public health expert ratings (0-10 scale) for each disease
- [ ] Preventability factors: lifestyle modifiable (high) vs genetic (low)
- [ ] Treatment effectiveness: availability of proven interventions
- [ ] Normalize interventionability scores to 0-100 scale

### Composite Priority Score
- [ ] Define scoring weights: burden (40%), trend urgency (30%), interventionability (30%)
- [ ] Calculate weighted composite score: `Priority = 0.4*Burden + 0.3*Urgency + 0.3*Interventionability`
- [ ] Rank diseases by composite priority score (1 = highest priority)
- [ ] Sensitivity analysis: test different weighting schemes

### Priority Quadrants & Segmentation
- [ ] Create 2×2 matrix: High/Low burden × Increasing/Declining trend
- [ ] Assign diseases to quadrants
- [ ] Quadrant interpretations:
  - **High burden + increasing**: URGENT PRIORITY - immediate action needed
  - **High burden + declining**: MAINTAIN EFFORTS - current programs working
  - **Low burden + increasing**: EMERGING THREAT - early intervention opportunity
  - **Low burden + declining**: SUCCESS STORY - document and sustain
- [ ] Generate quadrant assignments for all diseases

### Resource Allocation Recommendations
- [ ] Current resource allocation: gather existing program budgets (if available)
- [ ] Recommended allocation: proportional to priority scores
- [ ] Gap analysis: over-resourced vs under-resourced diseases
- [ ] Reallocation scenarios: simulate budget shifts
- [ ] Impact projections: estimate mortality reduction from reallocation

### Visualization
- [ ] Priority matrix scatter plot: burden (x-axis) vs urgency (y-axis), point size = interventionability
- [ ] Ranking table: all diseases with scores and ranks
- [ ] Quadrant plot: 2×2 matrix with disease labels
- [ ] Budget allocation chart: current vs recommended
- [ ] Save figures: `reports/figures/disease_prioritization_*.png/pdf`

### Policy Brief Development
- [ ] Executive summary: top 3-5 priority diseases
- [ ] Methodology explanation: scoring framework and weights
- [ ] Detailed findings: scores and rankings for all diseases
- [ ] Recommendations: specific resource allocation actions
- [ ] Implementation roadmap: phased approach to reallocation

### Testing & Validation
- [ ] Unit tests for scoring functions
- [ ] Validate normalization: all scores 0-100
- [ ] Test ranking logic: ties handled appropriately
- [ ] Sensitivity analysis: how do results change with different weights?
- [ ] Expert review: validate interventionability assessments

---

## 📌 Notes

**Polars Prioritization Example**:
```python
import polars as pl
from sklearn.preprocessing import MinMaxScaler
from loguru import logger

# Load mortality trends with APC
df = pl.read_parquet("shared/data/3_interim/mortality_trends_integrated_clean.parquet")

# Get latest year data
df_latest = df.filter(pl.col('year') == 2019)

# Burden magnitude score (normalize to 0-100)
df_scored = df_latest.with_columns([
    ((pl.col('mortality_rate') - pl.col('mortality_rate').min()) / 
     (pl.col('mortality_rate').max() - pl.col('mortality_rate').min()) * 100)
    .alias('burden_score')
])

# Add trend urgency from previous analysis
df_scored = df_scored.join(df_apc, on='disease_category', how='left')
df_scored = df_scored.with_columns([
    pl.when(pl.col('apc') > 2).then(100)
      .when(pl.col('apc') > 0).then(70)
      .when(pl.col('apc') > -2).then(40)
      .otherwise(20)
      .alias('urgency_score')
])

# Interventionability (manual scoring or from config)
interventionability = {
    'cancer': 60,  # Moderate - screening helps but genetics important
    'stroke': 90,   # High - preventable via hypertension control
    'ischemic_heart_disease': 85  # High - lifestyle and medication
}
df_scored = df_scored.with_columns([
    pl.col('disease_category').map_dict(interventionability).alias('interventionability_score')
])

# Composite priority score
df_scored = df_scored.with_columns([
    (0.4 * pl.col('burden_score') + 
     0.3 * pl.col('urgency_score') + 
     0.3 * pl.col('interventionability_score'))
    .alias('priority_score')
])

# Rank by priority
df_priority = df_scored.with_columns([
    pl.col('priority_score').rank(descending=True).alias('priority_rank')
])

logger.info(f"✓ Priority scoring complete for {len(df_priority)} diseases")
```

**Interventionability Assessment Criteria**:

**High Interventionability (70-100)**:
- Strong evidence base for prevention (e.g., smoking cessation → lung cancer)
- Cost-effective interventions available (e.g., statins for IHD)
- Controllable risk factors (e.g., hypertension → stroke)

**Moderate Interventionability (40-69)**:
- Some prevention opportunities but limited effectiveness
- Treatment available but expensive or limited reach
- Mix of controllable and non-controllable factors

**Low Interventionability (0-39)**:
- Largely genetic or unavoidable risk factors
- Limited proven prevention strategies
- Expensive treatments with modest effectiveness

**Expected Priority Rankings** (hypotheses):
1. **High Priority**: Diseases with high burden + increasing trend + high interventionability
2. **Moderate Priority**: High burden but declining (maintain programs) OR low burden but rapidly increasing
3. **Low Priority**: Low burden + declining trends

**Scoring Weight Sensitivity**:
- Test alternative weights: equal weights (33/33/33), burden-heavy (50/25/25), urgency-heavy (25/50/25)
- Document robustness: do top priorities remain stable across weighting schemes?

**Output Schema**:
```yaml
# results/tables/disease_burden_prioritization_matrix.csv
columns:
  disease_category: categorical
  burden_score: float  # 0-100
  urgency_score: float  # 0-100
  interventionability_score: float  # 0-100
  priority_score: float  # 0-100 composite
  priority_rank: int  # 1 = highest priority
  quadrant: string  # high_burden_increasing, etc.
  recommendation: string  # increase_resources, maintain, etc.
```

**Policy Brief Structure**:
1. Executive summary (1-2 pages)
2. Methodology & scoring framework (2 pages)
3. Findings: rankings and scores (2-3 pages)
4. Recommendations: resource allocation (2-3 pages)
5. Appendix: sensitivity analysis, data sources
