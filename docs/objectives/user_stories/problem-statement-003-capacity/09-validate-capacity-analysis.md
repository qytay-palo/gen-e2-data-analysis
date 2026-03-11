# Validate Capacity Gap Analysis & Recommendations (Lifecycle Stage: Validation)

**Story ID**: PS-003-US-09  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (3 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Scientist ensuring analytical rigor**,  
I want **to validate capacity gap calculations, test robustness of expansion scenarios, and verify recommendation reliability**,  
So that **infrastructure planners can confidently act on gap analysis without risk of flawed conclusions driving costly investment errors**.

---

## 🎯 Acceptance Criteria

1. **Gap calculation validation**
   - Mathematical correctness verified for gap metrics
   - Sensitivity to outlier years tested
   - Alternative gap definitions compared
   - Consistency checks: gaps align with qualitative domain knowledge

2. **Scenario robustness testing**
   - Scenario outcomes tested with varied assumptions
   - Extreme scenarios (optimistic/pessimistic) modeled
   - Key assumptions stress-tested: utilization growth, cost per bed
   - Recommendation stability assessed

3. **Data quality validation**
   - Source data quality re-confirmed
   - Missing data impact quantified
   - Aggregation logic verified (no double-counting)
   - Cross-validation with external benchmarks (if available)

4. **Validation report**
   - Output: `results/tables/capacity_validation_report.csv`
   - Robustness summary: which findings are robust vs sensitive
   - Confidence ratings: high/medium/low confidence per recommendation
   - Caveats documented

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **Statistical Testing**: scipy, numpy
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#validation-methods) - Validation best practices
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md) - Ensuring robust capacity planning

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `scipy>=1.11.0`, `numpy>=1.24.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-06, PS-003-US-08 (Gap analysis and scenarios - BLOCKING)
- **Data Sources**: All capacity analysis outputs
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Gap Calculation Validation
- [ ] Verify mathematical formulas for gap metrics
- [ ] Test with synthetic data (known gaps)
- [ ] Recalculate gaps excluding outlier years
- [ ] Compare alternative gap definitions

### Scenario Robustness Testing
- [ ] Sensitivity analysis: vary cost assumptions ±20%
- [ ] Vary utilization growth projections (optimistic/pessimistic)
- [ ] Test different budget constraints
- [ ] Assess recommendation stability

### Data Quality Checks
- [ ] Re-validate source data completeness
- [ ] Check for double-counting in aggregations
- [ ] Verify sector classifications
- [ ] Cross-reference with MOH published statistics (if available)

### Assumption Testing
- [ ] Document all key assumptions
- [ ] Test impact of relaxing each assumption
- [ ] Identify most influential assumptions
- [ ] Flag high-risk assumptions

### Confidence Rating
- [ ] Rate each finding: high/medium/low confidence
- [ ] High confidence: robust across scenarios and assumptions
- [ ] Medium: sensitive to some assumptions but directionally stable
- [ ] Low: highly sensitive, requires additional data

### Validation Reporting
- [ ] Compile validation test results
- [ ] Document robustness findings
- [ ] List caveats and limitations
- [ ] Update gap analysis report with confidence ratings

### Testing & Documentation
- [ ] Unit tests for validation functions
- [ ] Validate validation logic (meta-testing)
- [ ] Docstrings
- [ ] Validation methodology documentation

---

## 📌 Notes

**Validation Testing Example**:
```python
import polars as pl
import numpy as np
from scipy import stats

# Load gap analysis results
df_gaps = pl.read_csv("results/tables/capacity_gap_analysis.csv")

# Sensitivity: recalculate gaps excluding outlier years
df_no_outliers = df.filter(
    (pl.col('year') != 2020)  # Exclude COVID year
)

# Recalculate gaps
gaps_robust = calculate_gaps(df_no_outliers)

# Compare original vs robust gaps
gap_correlation = np.corrcoef(df_gaps['gap'], gaps_robust['gap'])[0,1]

# If correlation > 0.9, gaps are robust
assert gap_correlation > 0.9, "Gaps highly sensitive to outliers"
```

**Confidence Rating Criteria**:
- **High Confidence**: 
  - Gap >10% and consistent across multiple years
  - Robust to outlier exclusion
  - Aligns with domain expert expectations
  
- **Medium Confidence**:
  - Gap 5-10% or some year-to-year variation
  - Moderately sensitive to assumptions
  - Plausible but needs caution
  
- **Low Confidence**:
  - Gap <5% or highly volatile
  - Very sensitive to assumptions
  - Requires additional data/analysis

**Key Assumptions to Test**:
- Utilization growth rate projections
- Cost per bed estimates
- Population growth assumptions
- Bed occupancy efficiency targets

**Expected Validation Results**:
- Most gaps likely robust (large, consistent over time)
- Scenario recommendations may be moderately sensitive to cost assumptions
- Data quality likely high (official government source)
