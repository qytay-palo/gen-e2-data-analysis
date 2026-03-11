# Analyze 30-Year Mortality Trends (Lifecycle Stage: Exploratory Data Analysis)

**Story ID**: PS-002-US-03  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Epidemiologist**,  
I want **to analyze 30-year mortality rate trends (1990-2019) for cancer, stroke, and heart disease, calculating annual percentage changes and identifying trend patterns**,  
So that **I can quantify how disease burdens have evolved and identify diseases showing concerning increases vs successful decreases**.

---

## 🎯 Acceptance Criteria

1. **Annual percentage change calculated**
   - Year-over-year change: `(rate_t - rate_t-1) / rate_t-1 * 100` for each disease
   - Average annual percentage change (AAPC) calculated over 30-year period
   - Statistical significance tested (is trend non-zero?)

2. **Trend patterns identified**
   - Linear trends fitted using regression: `mortality_rate ~ year`
   - Trend direction: increasing, decreasing, stable (based on slope and p-value)
   - Trend magnitude: absolute change (rate in 2019 - rate in 1990)
   - Relative change: `(rate_2019 - rate_1990) / rate_1990 * 100%`

3. **Cross-disease comparisons**
   - Disease ranking by 2019 burden magnitude (which causes most deaths?)
   - Disease ranking by trend direction (which improving fastest/worsening fastest?)
   - Burden transition analysis: has leading cause of death changed 1990 vs 2019?

4. **Data output requirement**
   - Output file: `results/tables/mortality_trend_analysis.csv`
   - Format: CSV (disease, year, mortality_rate, yoy_change_pct, trend_slope, aapc, significance)
   - Trend visualization: `reports/figures/mortality_trends_30yr.png`

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Statistics**: scipy.stats, statsmodels for trend testing
- **Logging**: loguru
- **Testing**: pytest with ≥80% coverage

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#core-metrics--definitions) - Understanding mortality rate metrics
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md#objectives) - Objective 1: Quantify 30-year mortality trends

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data processing
- `scipy>=1.11.0`: Statistical tests
- `statsmodels>=0.14.0`: Linear regression, trend analysis
- `matplotlib>=3.8.0`: Trend visualizations
- `loguru>=0.7.0`: Logging

### Internal Dependencies
- **Upstream**: PS-002-US-02 (Clean mortality data - BLOCKING)
- **Data Sources**: `shared/data/3_interim/mortality_integrated_clean.parquet`
- **Config Files**: `config/analysis.yml` (significance thresholds)

---

## ✅ Implementation Tasks

### Trend Analysis
- [ ] Load cleaned mortality data (1990-2019)
- [ ] Calculate year-over-year change: `(rate_t - rate_t-1) / rate_t-1 * 100`
- [ ] Calculate AAPC: `(rate_2019 / rate_1990)^(1/29) - 1` (geometric mean)
- [ ] Fit linear trends: `statsmodels.OLS(mortality_rate ~ year)` per disease
- [ ] Extract trend metrics: slope, p-value, R-squared
- [ ] Classify trends: increasing (slope > 0, p < 0.05), decreasing, stable

### Statistical Significance Testing
- [ ] Test trend significance: t-test on regression slope
- [ ] Calculate confidence intervals for AAPC
- [ ] Test for trend change points (next story will use joinpoint regression)

### Cross-Disease Comparison
- [ ] Rank diseases by 2019 mortality rate (current burden)
- [ ] Rank by absolute change 1990-2019 (improvement magnitude)
- [ ] Rank by AAPC (% improvement rate)
- [ ] Create comparison matrix: burden vs trend direction

### Visualization
- [ ] Line charts: Mortality rate over time (1990-2019) per disease
- [ ] Slope charts: 1990 vs 2019 rates with connecting lines
- [ ] Bar charts: AAPC by disease (sorted by magnitude)
- [ ] Annotation: Mark statistically significant trends
- [ ] Export figures: PNG (reports) and PDF (publication)

### Testing & Validation
- [ ] Unit tests for AAPC calculation
- [ ] Validate trend regression against manual calculation
- [ ] Test edge cases: flat trends, missing years

### Documentation
- [ ] Docstrings (Google style)
- [ ] Analysis summary: `results/mortality_trend_insights.md`
- [ ] Update data dictionary

---

## 📌 Notes

**AAPC Calculation (Polars)**:
```python
import polars as pl

df_aapc = (
    df.group_by('disease').agg([
        pl.col('mortality_rate').first().alias('rate_1990'),
        pl.col('mortality_rate').last().alias('rate_2019'),
        ((pl.col('mortality_rate').last() / pl.col('mortality_rate').first()) ** (1/29) - 1) * 100
        .alias('aapc_pct')
    ])
)
```

**Trend Regression (statsmodels)**:
```python
import statsmodels.api as sm
import polars as pl

# For each disease
for disease in df['disease'].unique():
    df_disease = df.filter(pl.col('disease') == disease)
    
    X = df_disease['year'].to_numpy()
    y = df_disease['mortality_rate'].to_numpy()
    X = sm.add_constant(X)  # Add intercept
    
    model = sm.OLS(y, X).fit()
    slope = model.params[1]
    p_value = model.pvalues[1]
    
    logger.info(f"{disease}: slope={slope:.2f}, p={p_value:.4f}")
```

**Expected Findings** (hypotheses from epidemiology):
- **Cancer**: Likely declining or stable (improved early detection, treatment)
- **Stroke**: Likely declining (better hypertension management)
- **Heart Disease**: Likely declining (cholesterol management, lifestyle changes)
- **Overall**: Singapore likely shows favorable trends relative to global averages

**Interpretation Guidelines**:
- **p < 0.05**: Trend is statistically significant
- **Slope > 0**: Mortality rate increasing (concerning)
- **Slope < 0**: Mortality rate decreasing (positive public health impact)
- **|slope| < 0.1 per year**: Modest trend
- **|slope| ≥ 1.0 per year**: Strong trend
