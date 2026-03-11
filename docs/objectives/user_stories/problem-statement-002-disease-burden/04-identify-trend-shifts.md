# Detect Trend Inflection Points & Shifts (Lifecycle Stage: Exploratory Data Analysis)

**Story ID**: PS-002-US-04  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (4-5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Analyst examining disease burden evolution**,  
I want **to detect inflection points, trend accelerations, and decelerations in 30-year mortality data using statistical methods like Joinpoint regression**,  
So that **I can identify critical periods when disease burden trajectories changed direction and inform policy makers about emerging threats or improving trends**.

---

## 🎯 Acceptance Criteria

1. **Inflection point detection completed**
   - Joinpoint regression applied to each disease time series
   - Significant trend change points identified with 95% confidence intervals
   - At least 2-3 trend segments identified per disease (if warranted by data)
   - Joinpoint years documented: year, disease, previous slope, new slope

2. **Trend acceleration/deceleration quantified**
   - Annual percentage change (APC) calculated for each trend segment
   - Trend classification: accelerating decline, steady decline, stagnation, increasing, accelerating increase
   - Statistical significance tested for each trend segment (p-value < 0.05)
   - Comparison of trend periods: pre-2000 vs post-2000 vs 2010s

3. **Statistical validation performed**
   - Goodness of fit assessed: R² for each trend model
   - Model selection: optimal number of joinpoints identified (avoid overfitting)
   - Residual analysis: check for autocorrelation in time series
   - Sensitivity analysis: test robustness to outlier years

4. **Deliverables generated**
   - Output file: `results/tables/mortality_trend_changepoints.csv`
   - Figures: Trend segments visualized with joinpoints highlighted
   - Statistical summary: APC for each segment, significance levels
   - Report section: Narrative interpretation of trend shifts

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for data processing
- **Statistical Tools**: statsmodels, scipy for time series analysis
- **Visualization**: Matplotlib/Seaborn for trend segment plots
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage for statistical functions

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#temporal-trend-features) - Trend analysis methods and APC calculations
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md#objective-1) - Objective: Identify inflection points and trend shifts

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Time series data manipulation
- `statsmodels>=0.14.0`: Time series regression and changepoint detection
- `scipy>=1.11.0`: Statistical tests
- `matplotlib>=3.8.0`: Trend visualization
- `ruptures>=1.1.0`: Alternative changepoint detection methods
- `loguru>=0.7.0`: Structured logging

### Internal Dependencies
- **Upstream**: PS-002-US-03 (Analyze mortality trends - BLOCKING)
- **Data Sources**: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
- **Config Files**: `config/analysis.yml` (statistical significance thresholds)

---

## ✅ Implementation Tasks

### Joinpoint Regression Analysis
- [ ] Implement Joinpoint regression using piecewise linear regression
- [ ] Test models with 0-4 joinpoints for each disease
- [ ] Select optimal model using BIC/AIC criteria (avoid overfitting)
- [ ] Extract joinpoint years and slope changes
- [ ] Calculate 95% confidence intervals for joinpoint locations
- [ ] Document optimal number of joinpoints per disease

### Annual Percentage Change (APC)
- [ ] Calculate APC for each trend segment: `APC = (exp(β) - 1) × 100`
- [ ] Test statistical significance of each APC (p-value < 0.05)
- [ ] Compute average APC (AAPC) across entire 30-year period
- [ ] Compare APC across segments: identify acceleration/deceleration
- [ ] Flag segments with statistically significant changes

### Trend Classification
- [ ] Classify each segment: rapidly declining, declining, stable, increasing, rapidly increasing
- [ ] Define thresholds: |APC| < 1% = stable, 1-3% = moderate, >3% = rapid
- [ ] Create trend narrative: "Cancer mortality declined 2%/year 1990-2005, then stabilized 2005-2019"
- [ ] Identify diseases with most dramatic trend shifts

### Visualization
- [ ] Create trend segment plots: mortality rate vs year with joinpoints marked
- [ ] Overlay linear regression lines for each segment
- [ ] Annotate with APC values and significance stars
- [ ] Facet by disease for side-by-side comparison
- [ ] Style for publication quality (clear legends, axis labels)
- [ ] Save figures: `reports/figures/mortality_trend_changepoints.png` (and PDF)

### Statistical Validation
- [ ] Goodness of fit: calculate R² for each model
- [ ] Residual diagnostics: check for autocorrelation using Durbin-Watson test
- [ ] Sensitivity analysis: re-run excluding potential outlier years
- [ ] Cross-validation: split data to test model stability (if appropriate)

### Testing & Documentation
- [ ] Unit tests for Joinpoint regression implementation
- [ ] Validate APC calculation: test with known trend data
- [ ] Test edge cases: no joinpoints, multiple joinpoints
- [ ] Docstrings for all statistical functions (Google style)
- [ ] Document methodology: explain Joinpoint approach in results README

---

## 📌 Notes

**Joinpoint Regression Overview**:
- Identifies years where mortality trends change slope significantly
- Fits piecewise linear models with varying numbers of "joinpoints"
- Selects optimal model balancing fit quality vs parsimony

**Implementation Approach (Polars + statsmodels)**:
```python
import polars as pl
import numpy as np
from statsmodels.regression.linear_model import OLS
from scipy.optimize import minimize
from loguru import logger

# Load mortality data
df = pl.read_parquet("shared/data/3_interim/mortality_trends_integrated_clean.parquet")

# Filter for one disease
df_cancer = df.filter(pl.col('disease_category') == 'cancer')

# Time variable for regression
X = df_cancer['year'].to_numpy()
y = np.log(df_cancer['mortality_rate'].to_numpy())  # Log transform for APC

# Fit piecewise regression (simplified example - full implementation more complex)
def piecewise_linear(x, x0, a1, a2, b):
    """Piecewise linear model with one joinpoint at x0"""
    return np.where(x < x0, a1*x + b, a2*x + (a1-a2)*x0 + b)

# Optimize to find best joinpoint location
# ... (full implementation would use grid search + significance testing)

logger.info(f"✓ Identified joinpoint at year {optimal_joinpoint}")
```

**Statistical Criteria**:
- **Model Selection**: Use BIC (Bayesian Information Criterion) - penalizes model complexity
- **Significance Testing**: Each joinpoint must improve fit significantly (permutation test, p<0.05)
- **APC Significance**: Slope coefficients must be statistically significant

**Alternative Tools**:
- `ruptures` library: Modern changepoint detection with various algorithms
- Segmented regression: Alternative to Joinpoint
- STATA Joinpoint software: Gold standard for epidemiological trend analysis (can export R code)

**Expected Findings** (hypotheses):
- **Cancer**: Possible inflection ~2000-2005 due to screening programs and treatment advances
- **Stroke**: Likely declining trend throughout due to hypertension control
- **Ischemic Heart Disease**: May show inflection reflecting lifestyle changes and medical interventions

**Interpretation Guidelines**:
- Joinpoint before 2000: Reflect foundational public health shifts
- Joinpoint 2000-2010: Likely reflect specific program implementations
- Joinpoint post-2010: Recent healthcare system changes or demographic shifts

**Output Schema**:
```yaml
# results/tables/mortality_trend_changepoints.csv
columns:
  disease_category: categorical
  segment_number: int
  start_year: int
  end_year: int
  apc: float  # annual percentage change
  apc_95ci_lower: float
  apc_95ci_upper: float
  p_value: float
  trend_direction: string  # rapidly_declining, declining, stable, increasing, rapidly_increasing
```
