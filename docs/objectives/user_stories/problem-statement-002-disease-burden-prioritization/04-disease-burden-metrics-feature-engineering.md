# User Story 4: Disease Burden Metrics and Feature Engineering

**As a** public health analyst,  
**I want** to calculate comprehensive disease burden metrics and derived features,  
**so that** I can quantify burden across multiple dimensions and prepare analytical features for disease priority ranking.

## 1. 🎯 Acceptance Criteria

- Disease burden metrics calculated for all major diseases:
  - Absolute burden: Total ASMR across time period
  - Trend metrics: Growth rate, cumulative burden change, trend acceleration
  - Demographic burden: Age-specific rates, gender ratios, burden concentration
  - Relative burden: Disease burden indexed to population average
- Derived features engineered following domain knowledge guidelines:
  - Temporal features (year-over-year growth, indexed growth, momentum)
  - Comparative features (relative burden, disease ranking indices)
  - Demographic features (age stratification, gender concentration)
- All features documented with formulas and interpretation guidelines
- Feature dataset saved to `data/4_processed/disease_burden_metrics.csv`
- Feature engineering documentation saved to `docs/data_dictionary/disease_burden_features.md`
- Validation report confirming feature quality saved to `results/tables/ps-002/feature_validation_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient feature calculation
- **Formula Documentation**: All features documented with mathematical formulas
- **Validation**: Cross-validate calculated metrics against WHO benchmarks where available
- **Reproducibility**: Feature calculation code modularized in `src/features/disease_burden.py`

## 3. 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../domain_knowledge/disease-burden-mortality-analysis.md#feature-engineering-guidance) - Comprehensive feature engineering patterns for disease burden analysis
- [Standard Metrics and KPIs](../../../domain_knowledge/disease-burden-mortality-analysis.md#standard-metrics-and-kpis) - Reference formulas and typical ranges

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Feature engineering transformations
- **numpy**: Statistical calculations
- **scipy**: Statistical methods for advanced features

**Internal Dependencies:**
- Story 2 output: Cleaned mortality data
- Story 3 output: EDA findings informing feature selection

## 5. ✅ Implementation Tasks

### Temporal Trend Features
- ⬜ Calculate year-over-year growth rate: `(ASMR[t] - ASMR[t-1]) / ASMR[t-1] × 100` for each disease
- ⬜ Calculate cumulative growth indexed to baseline (1990): `(ASMR[t] / ASMR[1990]) × 100`
- ⬜ Calculate growth momentum: `Current Growth Rate - Previous Growth Rate`
- ⬜ Identify trend acceleration/deceleration periods
- ⬜ Smooth trends using 3-year moving averages to reduce noise
- ⬜ Calculate average annual growth rate across full 30-year period

### Absolute Burden Metrics
- ⬜ Calculate total burden (sum ASMR 1990-2019) by disease
- ⬜ Calculate average annual ASMR for each disease
- ⬜ Calculate burden variability (standard deviation of ASMR over time)
- ⬜ Calculate premature mortality index (if age-at-death data available)
- ⬜ Rank diseases by absolute burden magnitude

### Relative Burden Metrics
- ⬜ Calculate disease burden relative to population average: `(Disease ASMR / Avg ASMR) × 100`
- ⬜ Calculate disease-specific mortality fraction: `Disease Deaths / Total Deaths × 100`
- ⬜ Calculate relative trend: Disease growth rate compared to average disease growth rate
- ⬜ Create burden severity index (absolute burden × trend direction)

### Demographic Stratification Features
- ⬜ Calculate age-group-specific mortality rates for each disease
- ⬜ Identify peak burden age group for each disease
- ⬜ Calculate demographic burden concentration: `(Burden in top age group / Total burden) × 100`
- ⬜ Calculate gender mortality ratio: `(Male ASMR / Female ASMR) × 100`
- ⬜ Identify diseases with >150% gender disparity (male or female)
- ⬜ Calculate elderly burden proportion (65+ age group mortality %)

### Trend Classification Features
- ⬜ Classify diseases as "Rising", "Stable", or "Declining" based on average growth rate
- ⬜ Flag diseases with >2% average annual increase (rising burden)
- ⬜ Flag diseases with >2% average annual decrease (declining burden)
- ⬜ Identify inflection points (years where trend direction reverses)
- ⬜ Calculate years-to-double metric for rising diseases
- ⬜ Create trend stability index (variance in year-over-year growth rates)

### Disease Priority Index Construction
- ⬜ Normalize all metrics to 0-100 scale for comparability
- ⬜ Define weighted priority index: `0.4 × Burden + 0.3 × Trend + 0.3 × Demographic Risk`
- ⬜ Calculate composite priority index for each disease
- ⬜ Rank diseases by priority index score
- ⬜ Validate index sensitivity to weight changes
- ⬜ Document index construction methodology

### Feature Validation
- ⬜ Validate year-over-year growth rates are within reasonable ranges (-20% to +20%)
- ⬜ Check cumulative growth indices start at 100 (baseline year)
- ⬜ Validate demographic burden proportions sum to 100%
- ⬜ Cross-check calculated metrics against WHO Global Health Observatory where available
- ⬜ Identify and investigate any anomalous feature values
- ⬜ Generate feature quality report with validation results

### Feature Documentation
- ⬜ Document all features with formulas, interpretation, and typical ranges
- ⬜ Create feature data dictionary in markdown format
- ⬜ Document data sources and calculation methods for each feature
- ⬜ Include example interpretations for stakeholder understanding
- ⬜ Save to `docs/data_dictionary/disease_burden_features.md`

### Output and Code Modularization
- ⬜ Save feature dataset to `data/4_processed/disease_burden_metrics.csv`
- ⬜ Create reusable feature engineering module: `src/features/disease_burden.py`
- ⬜ Write unit tests for feature calculation functions
- ⬜ Generate feature correlation matrix to check for redundancy
- ⬜ Save feature validation report to `results/tables/ps-002/`

## 6. Notes

**Feature Engineering Principles:**
- All features should be interpretable to stakeholders (avoid black-box calculations)
- Document formulas explicitly so non-technical users understand methodology
- Validate against external benchmarks (WHO, academic literature)

**Priority Index Rationale:**
- **Burden (40% weight)**: Absolute magnitude of lives lost is primary concern
- **Trend (30% weight)**: Rising diseases require proactive intervention
- **Demographic Risk (30% weight)**: Concentrated burden in vulnerable populations increases priority

**Feature Quality Checks:**
- No features with >20% missing values
- Outliers validated against domain knowledge (not just statistical thresholds)
- Feature correlations <0.8 to avoid redundancy

**Reusability:**
- Feature engineering code should be modular and reusable for future mortality data updates
- Functions should accept flexible inputs for different diseases or time periods

**Related Stories:**
- Depends on: Story 2 (Cleaned data), Story 3 (Exploratory insights)
- Enables: Story 5 (Disease priority ranking), Story 6 (Visualization dashboard)
