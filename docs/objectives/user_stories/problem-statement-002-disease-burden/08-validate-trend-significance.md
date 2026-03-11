# Validate Statistical Significance of Trends (Lifecycle Stage: Validation)

**Story ID**: PS-002-US-08  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (3 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Scientist ensuring analytical rigor**,  
I want **to validate the statistical significance of mortality trends using hypothesis testing, confidence intervals, and robustness checks**,  
So that **policy makers can confidently rely on trend findings without risk of spurious patterns or chance fluctuations**.

---

## 🎯 Acceptance Criteria

1. **Trend significance testing completed**
   - Null hypothesis tests: are trends significantly different from zero? (p < 0.05)
   - Linear regression significance: slope coefficients tested for each disease
   - Confidence intervals: 95% CI calculated for all annual percentage changes
   - Multiple testing correction: Bonferroni or FDR adjustment applied

2. **Robustness validation performed**
   - Outlier sensitivity: trends recalculated excluding potential outlier years
   - Alternative time periods: trends tested for 1990-2009 vs 2010-2019 subsets
   - Different trend models: compare linear vs exponential vs polynomial trends
   - Bootstrap validation: resampling to assess trend stability

3. **Assumption testing conducted**
   - Normality of residuals: Shapiro-Wilk or Q-Q plots
   - Homoscedasticity: constant variance of residuals over time
   - Autocorrelation: Durbin-Watson test for serial correlation
   - Linearity: residual plots to check linear model appropriateness

4. **Validation report generated**
   - Output file: `results/tables/mortality_trend_validation_report.csv`
   - Statistical test results: p-values, confidence intervals, test statistics
   - Robustness summary: sensitivity to outliers and model specifications
   - Recommendations: which trends are robust vs require cautious interpretation

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for data processing
- **Statistical Testing**: scipy, statsmodels for hypothesis tests
- **Visualization**: Matplotlib for diagnostic plots
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage for validation functions

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#temporal-trend-features) - Statistical methods for trend analysis
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md) - Ensuring robust trend identification

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data manipulation
- `scipy>=1.11.0`: Statistical tests (t-tests, normality tests)
- `statsmodels>=0.14.0`: Regression diagnostics, Durbin-Watson test
- `matplotlib>=3.8.0`: Diagnostic plots (residuals, Q-Q plots)
- `numpy>=1.24.0`: Bootstrap resampling
- `loguru>=0.7.0`: Structured logging

### Internal Dependencies
- **Upstream**: PS-002-US-03, PS-002-US-04 (Trend analyses - BLOCKING)
- **Data Sources**: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
- **Config Files**: `config/analysis.yml` (significance thresholds, alpha levels)

---

## ✅ Implementation Tasks

### Trend Significance Testing
- [ ] Linear regression for each disease: mortality_rate ~ year
- [ ] Extract slope coefficients and standard errors
- [ ] Calculate t-statistics and p-values for slopes
- [ ] Test null hypothesis: H₀: slope = 0 (no trend)
- [ ] 95% confidence intervals for slopes
- [ ] Bonferroni correction for multiple comparisons (3 diseases)

### Robustness Checks
- [ ] Outlier detection: identify years with residuals > 2 std dev
- [ ] Sensitivity analysis: recalculate trends excluding each potential outlier
- [ ] Subset analysis: trends for 1990-2009 vs 2010-2019
- [ ] Model comparison: linear vs exponential vs segmented regression (AIC/BIC)
- [ ] Document robust trends: significant across multiple specifications

### Assumption Validation
- [ ] Normality test: Shapiro-Wilk test on residuals (p > 0.05 = normal)
- [ ] Q-Q plots: visual assessment of residual normality
- [ ] Homoscedasticity: Breusch-Pagan test for constant variance
- [ ] Autocorrelation: Durbin-Watson statistic (value ~2 = no autocorrelation)
- [ ] Linearity check: residual plots (should show no pattern)

### Bootstrap Validation
- [ ] Implement bootstrap resampling: 1,000 bootstrap samples
- [ ] Recalculate trend slopes for each bootstrap sample
- [ ] Generate bootstrap confidence intervals (percentile method)
- [ ] Compare bootstrap CI with standard regression CI
- [ ] Assess trend stability: coefficient of variation across bootstrap samples

### Diagnostic Visualization
- [ ] Residual plots: residuals vs fitted values (check homoscedasticity)
- [ ] Q-Q plots: assess normality of residuals
- [ ] Time series of residuals: check for autocorrelation patterns
- [ ] Save diagnostic plots: `reports/figures/trend_validation_diagnostics_*.png`

### Validation Reporting
- [ ] Compile test results: all p-values, confidence intervals, test statistics
- [ ] Robustness summary: trends unchanged vs sensitive to outliers
- [ ] Recommendation flags: robust (green), caution (yellow), unreliable (red)
- [ ] Generate validation report CSV
- [ ] Update analytical report with validation section

### Testing & Documentation
- [ ] Unit tests for statistical test functions
- [ ] Validate bootstrap implementation: test with known distributions
- [ ] Test assumption checks with simulated data
- [ ] Docstrings for all validation functions
- [ ] Methodology documentation: explain statistical tests used

---

## 📌 Notes

**Polars + statsmodels Validation Example**:
```python
import polars as pl
import statsmodels.api as sm
from scipy import stats
from loguru import logger

# Load mortality data
df = pl.read_parquet("shared/data/3_interim/mortality_trends_integrated_clean.parquet")

# Linear regression for cancer
df_cancer = df.filter(pl.col('disease_category') == 'cancer')
X = df_cancer['year'].to_numpy()
y = df_cancer['mortality_rate'].to_numpy()

# Add constant for intercept
X_with_const = sm.add_constant(X)

# Fit OLS regression
model = sm.OLS(y, X_with_const).fit()

# Extract statistics
slope = model.params[1]
p_value = model.pvalues[1]
ci_lower, ci_upper = model.conf_int()[1]

logger.info(f"Cancer trend: slope={slope:.4f}, p={p_value:.4f}, 95% CI=[{ci_lower:.4f}, {ci_upper:.4f}]")

# Test assumptions
residuals = model.resid
shapiro_stat, shapiro_p = stats.shapiro(residuals)
dw_statistic = sm.stats.stattools.durbin_watson(residuals)

logger.info(f"Normality (Shapiro-Wilk): p={shapiro_p:.4f}")
logger.info(f"Autocorrelation (Durbin-Watson): {dw_statistic:.4f}")

# Robustness: exclude outliers
outliers = np.abs(residuals) > 2 * np.std(residuals)
if outliers.any():
    model_robust = sm.OLS(y[~outliers], X_with_const[~outliers]).fit()
    logger.info(f"Robust trend (excl. outliers): slope={model_robust.params[1]:.4f}")
```

**Bootstrap Validation Example**:
```python
import numpy as np

def bootstrap_trend(X, y, n_bootstrap=1000):
    """Calculate bootstrap confidence interval for trend slope"""
    n = len(X)
    slopes = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(n, size=n, replace=True)
        X_boot = X[indices]
        y_boot = y[indices]
        
        # Fit model
        X_boot_const = sm.add_constant(X_boot)
        model_boot = sm.OLS(y_boot, X_boot_const).fit()
        slopes.append(model_boot.params[1])
    
    # 95% confidence interval (percentile method)
    ci_lower = np.percentile(slopes, 2.5)
    ci_upper = np.percentile(slopes, 97.5)
    
    return np.mean(slopes), ci_lower, ci_upper

mean_slope, boot_ci_lower, boot_ci_upper = bootstrap_trend(X, y)
logger.info(f"Bootstrap 95% CI: [{boot_ci_lower:.4f}, {boot_ci_upper:.4f}]")
```

**Statistical Significance Thresholds**:
- **p-value < 0.05**: Statistically significant trend (standard threshold)
- **p-value < 0.01**: Highly significant (stronger evidence)
- **p-value < 0.001**: Very highly significant (very strong evidence)

**Multiple Testing Correction**:
- Testing 3 diseases → Bonferroni correction: α = 0.05/3 = 0.017
- Adjust significance threshold to 0.017 to control family-wise error rate

**Interpretation Guidelines**:
- **Robust trend**: Significant (p < 0.05) AND survives outlier exclusion AND bootstrap CI excludes 0
- **Potentially robust**: Significant but sensitive to outliers or model specification
- **Unreliable trend**: Non-significant (p ≥ 0.05) OR highly sensitive to outliers

**Durbin-Watson Interpretation**:
- DW < 1.5: Positive autocorrelation (concern for time series)
- 1.5 ≤ DW ≤ 2.5: No autocorrelation (good)
- DW > 2.5: Negative autocorrelation

**Expected Validation Results**:
- Cancer, stroke, IHD trends likely robust (30 years data, consistent trends)
- Autocorrelation possible due to time series nature (may need ARIMA models)
- Linear trends may oversimplify (Joinpoint may better capture reality)

**Output Schema**:
```yaml
# results/tables/mortality_trend_validation_report.csv
columns:
  disease_category: categorical
  slope: float  # regression slope
  p_value: float  # significance test
  ci_95_lower: float
  ci_95_upper: float
  shapiro_p: float  # normality test
  durbin_watson: float  # autocorrelation
  robust_to_outliers: boolean
  validation_status: string  # robust, caution, unreliable
```
