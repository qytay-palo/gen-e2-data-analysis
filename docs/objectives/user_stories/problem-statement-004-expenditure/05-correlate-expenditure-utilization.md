# Correlate Expenditure with Utilization & Demographics (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-004-US-05  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (4-5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financial Analyst identifying cost drivers**,  
I want **to perform correlation analysis between expenditure growth and utilization patterns (admissions) as well as demographic factors (population aging)**,  
So that **I can quantify which factors drive expenditure increases and inform policy on controllable vs unavoidable cost growth**.

---

## 🎯 Acceptance Criteria

1. **Correlation analysis completed**
   - Correlation matrix: expenditure vs utilization, population, demographics
   - Statistical significance testing: identify meaningful correlations (p < 0.05)
   - Partial correlations: control for confounding variables
   - Time-lagged correlations: test if utilization predicts future expenditure

2. **Driver quantification**
   - Regression models: expenditure ~ utilization + demographics
   - Variance explained: R² for each driver
   - Elasticity estimates: % expenditure change per % utilization change
   - Relative importance: rank drivers by explanatory power

3. **Demographic impact assessed**
   - Aging impact: correlation with elderly population share
   - Population growth impact
   - Dependency ratio correlation

4. **Deliverables**
   - Output: `results/tables/expenditure_correlation_analysis.csv`
   - Regression summary: `results/tables/expenditure_driver_regression.csv`
   - Figures: Scatter plots, correlation heatmap
   - Analysis report: Key drivers identified

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for data; scipy/statsmodels for analysis
- **Visualization**: Matplotlib/Seaborn
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#cost-driver-analysis) - Healthcare cost driver methodologies
- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objective-3) - Driver identification objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `scipy>=1.11.0`, `statsmodels>=0.14.0`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-03 (Expenditure trends - BLOCKING)
- **Data Sources**: `shared/data/3_interim/expenditure_drivers_integrated.parquet`
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### Correlation Analysis
- [ ] Calculate Pearson correlations: expenditure vs all candidate drivers
- [ ] Statistical significance testing for correlations
- [ ] Partial correlations controlling for time trends
- [ ] Time-lagged correlations (expenditure_t ~ utilization_t-1)

### Regression Modeling
- [ ] Simple linear regression: expenditure ~ utilization
- [ ] Multiple regression: expenditure ~ utilization + demographics
- [ ] Extract coefficients, R², p-values
- [ ] Calculate elasticities from log-log models

### Demographic Impact
- [ ] Correlation with elderly population share
- [ ] Correlation with population growth
- [ ] Dependency ratio correlation analysis

### Driver Ranking
- [ ] Rank drivers by correlation strength
- [ ] Rank by R² contribution in multivariate model
- [ ] Identify primary vs secondary drivers

### Visualization
- [ ] Correlation heatmap
- [ ] Scatter plots: expenditure vs key drivers
- [ ] Regression plots with confidence bands
- [ ] Save figures: `reports/figures/expenditure_drivers_*.png/pdf`

### Testing & Documentation
- [ ] Unit tests for correlation calculations
- [ ] Validate regression implementations
- [ ] Docstrings
- [ ] Driver analysis report

---

## 📌 Notes

**Correlation Analysis Example**:
```python
import polars as pl
from scipy.stats import pearsonr
import statsmodels.api as sm

df = pl.read_parquet("shared/data/3_interim/expenditure_drivers_integrated.parquet")

# Calculate correlation
exp = df['total_expenditure'].to_numpy()
util = df['total_admissions'].to_numpy()
corr, p_value = pearsonr(exp, util)

print(f"Correlation: {corr:.3f}, p-value: {p_value:.4f}")

# Regression
X = sm.add_constant(util)
model = sm.OLS(exp, X).fit()
print(model.summary())
```

**Expected Drivers**:
- **Utilization**: Strong positive correlation (more admissions = higher costs)
- **Population aging**: Positive correlation (elderly use more services)
- **Population size**: Positive but weaker (per capita already controls for this)

**Elasticity Interpretation**:
- If elasticity = 1.2: 10% increase in utilization → 12% increase in expenditure
