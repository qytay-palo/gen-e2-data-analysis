# Decompose Healthcare Expenditure Growth Components (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-004-US-04  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: L (6-7 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financing Policy Analyst**,  
I want **to decompose 15-year expenditure growth (2005-2020) into demographic effects (population aging, growth), volume effects (more services), and price/intensity effects (cost per service)**,  
So that **I can identify whether cost growth is driven by unavoidable factors (aging population) vs controllable factors (utilization intensity, prices) and target interventions accordingly**.

---

## 🎯 Acceptance Criteria

1. **Expenditure decomposition completed**
   - Growth decomposed into 3 components:
     1. **Demographic effect**: Population size and age structure changes
     2. **Volume effect**: Changes in utilization rates (more admissions per capita)
     3. **Price/intensity effect**: Changes in cost per service (residual after accounting for demographic + volume)
   - Annual decomposition calculated for each year 2006-2020
   - Cumulative contribution calculated: % of total growth attributable to each component

2. **Decomposition methodology validated**
   - Method: Index decomposition analysis (IDA) or Laspeyres index approach
   - Cross-validation: sum of components equals total expenditure growth
   - Sensitivity analysis: results stable under alternative decomposition methods

3. **Findings documented**
   - Primary driver identified: which component contributes most to growth?
   - Temporal patterns: has dominant driver changed over time (e.g., aging accelerating post-2015)?
   - Policy implications: where can interventions have most impact?

4. **Data output requirement**
   - Output file: `results/tables/expenditure_decomposition.csv`
   - Format: CSV (year, total_growth_pct, demographic_contribution_pct, volume_contribution_pct, price_contribution_pct)
   - Decomposition visualization: `reports/figures/expenditure_decomposition_waterfall.png`

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Advanced Methods**: Custom decomposition implementation or econometric packages
- **Logging**: loguru
- **Testing**: pytest with ≥80% coverage

---

## 📚 Domain Knowledge References

- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objectives) - Objective 2: Identify primary drivers through decomposition
- Health economics literature: Index decomposition analysis (IDA) methods

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data processing
- `matplotlib>=3.8.0` or `plotly>=5.18.0`: Waterfall charts
- `loguru>=0.7.0`: Logging
- `statsmodels>=0.14.0` (optional): Econometric validation

### Internal Dependencies
- **Upstream**: 
  - PS-004-US-02 (Integrated expenditure data - BLOCKING)
  - PS-004-US-03 (Expenditure trends - BLOCKING)
- **Data Sources**: 
  - `shared/data/3_interim/expenditure_drivers_integrated.parquet` (expenditure + utilization + demographics)
- **Config Files**: `config/analysis.yml` (decomposition method selection)

---

## ✅ Implementation Tasks

### Data Preparation
- [ ] Load integrated dataset: expenditure, population, utilization, age structure
- [ ] Calculate base year values (2005): expenditure, population, utilization rate, age mix
- [ ] Calculate end year values (2020): same variables
- [ ] Prepare annual time series for dynamic decomposition

### Decomposition Method Implementation

**Option 1: Laspeyres Decomposition (Simpler)**
- [ ] Calculate demographic effect:
  - Effect of population growth: `(pop_2020 / pop_2005) * exp_2005 - exp_2005`
  - Effect of aging: Use age-specific utilization × population age structure changes
  
- [ ] Calculate volume effect:
  - Effect of utilization change: `(util_rate_2020 / util_rate_2005) * exp_demographic - exp_demographic`
  
- [ ] Calculate price/intensity effect (residual):
  - `exp_2020 - exp_demographic - exp_volume`

**Option 2: Logarithmic Mean Divisia Index (LMDI, Preferred)**
- [ ] Implement LMDI decomposition:
  - Demographic: `Σ[L(exp_t, exp_t-1) * ln(pop_t / pop_t-1)]`
  - Volume: `Σ[L(exp_t, exp_t-1) * ln(util_t / util_t-1)]`
  - Price: `Σ[L(exp_t, exp_t-1) * ln(price_t / price_t-1)]`
  - Where L(a,b) = (a-b)/ln(a/b) (logarithmic mean)

- [ ] Calculate annually (2006-2020) for dynamic analysis
- [ ] Calculate cumulative contributions over full period

### Component Validation
- [ ] Verify additive property: `sum(components) = total_growth`
- [ ] Handle edge cases: zero values, negative growth
- [ ] Cross-check with alternative methods (Laspeyres vs LMDI)

### Sensitivity Analysis
- [ ] Test alternative base years (2005 vs 2010)
- [ ] Test alternative age groupings (5-year vs 10-year age bands)
- [ ] Quantify uncertainty in decomposition estimates

### Interpretation & Insights
- [ ] Identify dominant driver: rank components by contribution magnitude
- [ ] Temporal pattern analysis: when did each component peak?
- [ ] Policy implications: 
  - High demographic effect → unavoidable (aging population)
  - High volume effect → potential over-utilization (policy target)
  - High price effect → cost control opportunity (negotiate prices, efficiency)

### Visualization
- [ ] Waterfall chart: decomposition showing cumulative contributions
- [ ] Stacked area chart: annual contributions over time
- [ ] Pie chart: cumulative contribution shares 2005-2020
- [ ] Export figures

### Testing & Validation
- [ ] Unit tests for decomposition formulas
- [ ] Validate perfect decomposition: components sum to total
- [ ] Test edge cases: zero growth, negative growth, missing data

### Documentation
- [ ] Docstrings (Google style)
- [ ] Methodology document: `results/expenditure_decomposition_methodology.md`
  - Decomposition method rationale (why LMDI vs Laspeyres)
  - Mathematical formulas
  - Assumptions and limitations
  - Sensitivity analysis results
- [ ] Policy brief: `results/expenditure_drivers_summary.md`
  - Top 3 drivers with evidence
  - Policy recommendations per driver
- [ ] Update data dictionary

---

## 📌 Notes

**Laspeyres Decomposition (Simplified Example)**:
```python
import polars as pl

# Base year: 2005
base_exp = df.filter(pl.col('year') == 2005).select('expenditure').item()
base_pop = df.filter(pl.col('year') == 2005).select('population').item()
base_util = df.filter(pl.col('year') == 2005).select('utilization_rate').item()

# End year: 2020
end_exp = df.filter(pl.col('year') == 2020).select('expenditure').item()
end_pop = df.filter(pl.col('year') == 2020).select('population').item()
end_util = df.filter(pl.col('year') == 2020).select('utilization_rate').item()

# Decomposition
demographic_effect = (end_pop / base_pop) * base_exp - base_exp
volume_effect = (end_util / base_util) * (base_exp + demographic_effect) - (base_exp + demographic_effect)
price_effect = end_exp - (base_exp + demographic_effect + volume_effect)

total_growth = end_exp - base_exp
assert abs((demographic_effect + volume_effect + price_effect) - total_growth) < 0.01

logger.info(f"Total growth: ${total_growth:,.2f}")
logger.info(f"  Demographic: {demographic_effect/total_growth*100:.1f}%")
logger.info(f"  Volume: {volume_effect/total_growth*100:.1f}%")
logger.info(f"  Price: {price_effect/total_growth*100:.1f}%")
```

**LMDI Formula (for reference)**:
```
Logarithmic Mean: L(a, b) = (a - b) / ln(a / b)

Component contribution = L(exp_t, exp_t-1) * ln(factor_t / factor_t-1)
```

**Expected Findings** (hypotheses):
- **Demographic effect**: ~30-40% of growth (Singapore's aging population well-documented)
- **Volume effect**: ~20-30% (healthcare utilization increasing beyond demographic effects)
- **Price/intensity effect**: ~30-50% (technology advancement, treatment intensity, labor costs)

**Policy Implications by Driver**:
| Driver | Contribution | Controllability | Policy Levers |
|--------|-------------|----------------|---------------|
| Demographic | 30-40% | Low (aging unavoidable) | Plan capacity, workforce for aging population |
| Volume | 20-30% | Medium | Reduce over-utilization, preventive care, efficiency |
| Price/Intensity | 30-50% | High | Price negotiation, generic drugs, standardized protocols, technology assessment |

**Limitations**:
- Residual method: Price effect captures all unmodeled drivers (could include quality improvements, new technology, administrative costs)
- Aggregate analysis: Sector-specific drivers (e.g., primary vs specialist care) masked
- Data constraints: Limited granularity for detailed price decomposition
