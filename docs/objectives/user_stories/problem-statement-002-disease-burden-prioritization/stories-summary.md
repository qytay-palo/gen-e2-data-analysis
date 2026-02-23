# User Story 1: Mortality Data Extraction and Quality Assessment

**As a** public health analyst,  
**I want** to extract and profile age-standardized mortality data for major diseases from the Kaggle dataset,  
**so that** I can establish a reliable foundation for disease burden analysis and trend detection.

## 1. 🎯 Acceptance Criteria

- Mortality datasets successfully loaded for: cancer, stroke, ischemic heart disease (1990-2019)
- Age-standardized mortality rates (ASMR) verified and validated
- Data completeness report showing year coverage and missing values by disease
- Age/gender breakdown data extracted where available
- Data quality report generated with completeness and consistency metrics
- Mortality data ranges validated (disease ASMR typically 50-300 per 100,000)
- Raw data saved to `data/1_raw/` with audit trail

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient profiling
- **Statistical Validation**: Verify ASMR calculation methodology is clear
- **Logging**: Log all ETL operations using loguru
- **Output Format**: Parquet for intermediate storage

## 3. 📚 Domain Knowledge References

- [Disease Burden & Mortality Analysis: Key Concepts](../../../domain_knowledge/disease-burden-mortality-analysis.md#age-standardized-mortality-rate-asmr)
- [Disease Burden: Standard Metrics](../../../domain_knowledge/disease-burden-mortality-analysis.md#standard-metrics-and-kpis)

## 4. 📦 Dependencies

- **kagglehub**: Kaggle dataset access
- **polars**: Data profiling and aggregation
- **loguru**: Structured logging

## 5. ✅ Implementation Tasks

- ⬜ Load mortality tables: cancer, stroke, ischemic heart disease
- ⬜ Verify ASMR values are in expected range (50-300 per 100,000)
- ⬜ Profile data completeness by disease and year
- ⬜ Check for demographic breakdowns (age/gender specific rates)
- ⬜ Generate data quality report
- ⬜ Save raw data to `data/1_raw/`

---

# User Story 2: Mortality Data Cleaning and Validation

**As a** health data analyst,  
**I want** to clean, standardize, and validate mortality data for consistency,  
**so that** I can ensure reliable trend analysis and disease burden quantification.

## 1. 🎯 Acceptance Criteria

- Column names standardized to snake_case across all disease datasets
- Year values validated (1990-2019 range)
- Disease names standardized to consistent taxonomy
- Age/gender categories standardized where demographic data present
- ASMR values validated (no negative, impossibly high values flagged)
- Missing value strategy documented
- Cleaned data saved to `data/3_interim/` with data dictionary

## 2. 🔒 Technical Constraints

- **Data Types**: Year to Int32, ASMR to Float32 (more precise than Float16)
- **Categorical Standardization**: Disease names standardized to fixed list
- **Validation Rules**: ASMR >0 and <500 per 100,000 (any outside flagged)

## 3. 📚 Domain Knowledge References

- [Disease Burden: Data Quality Considerations](../../../domain_knowledge/disease-burden-mortality-analysis.md#data-quality-considerations)

## 4. 📦 Dependencies

- **polars**: Data transformation
- **loguru**: Logging

## 5. ✅ Implementation Tasks

- ⬜ Standardize column names across diseases
- ⬜ Validate year values (1990-2019)
- ⬜ Standardize disease names (mapping inconsistencies)
- ⬜ Handle missing values (document strategy)
- ⬜ Validate ASMR ranges; flag outliers
- ⬜ Create data quality report
- ⬜ Save cleaned data to `data/3_interim/`

---

# User Story 3: Disease Burden Quantification and 30-Year Trend Analysis

**As a** policy analyst,  
**I want** to quantify current disease burden and analyze 30-year mortality trends (1990-2019),  
**so that** I can identify which diseases are rising vs. declining and prioritize intervention resources.

## 1. 🎯 Acceptance Criteria

- Current disease burden quantified (baseline ASMR for most recent available year)
- 30-year trend analysis completed for all diseases (1990-2019)
- Trend classifications assigned (rising, stable, declining) with statistical significance testing
- Trend acceleration identified (is rate of change increasing?)
- Inflection points detected (years where trend changed direction)
- Age/gender burden segmentation calculated
- Trend visualization created for all diseases
- EDA report generated with key findings and hypotheses

## 2. 🔒 Technical Constraints

- **Statistical Testing**: Use linear regression for trend significance (p<0.05)
- **Smoothing**: Apply 3-year moving average for volatile diseases
- **Trend Definition**: Rising >1% annual change, declining <-1%, stable within ±1%

## 3. 📚 Domain Knowledge References

- [Disease Burden: Trend Classification](../../../domain_knowledge/disease-burden-mortality-analysis.md#trend-classification)
- [Disease Burden: Analytical Methodologies - Trend Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md#trend-analysis-methods)

## 4. 📦 Dependencies

- **scipy**: Statistical testing (linear regression, significance)
- **numpy**: Numerical calculations
- **matplotlib/seaborn**: Visualization

## 5. ✅ Implementation Tasks

- ⬜ Calculate current ASMR by disease (baseline)
- ⬜ Calculate 30-year annual percent change (trend)
- ⬜ Apply smoothing (3-year moving average) for volatile diseases
- ⬜ Perform linear regression to test trend significance
- ⬜ Classify trends: rising/stable/declining
- ⬜ Identify inflection points (trend direction changes)
- ⬜ Calculate age-specific burden for each disease
- ⬜ Visualize all disease trends
- ⬜ Generate EDA report with findings

---

# User Story 4: Disease Priority Index Development and Comparative Ranking

**As a** healthcare resource planner,  
**I want** to develop a disease priority index combining burden magnitude, trend direction, and demographic impact,  
**so that** I can provide a unified ranking framework for resource allocation decisions.

## 1. 🎯 Acceptance Criteria

- Disease priority index calculated combining:
  - Burden magnitude (current ASMR weight 40%)
  - Trend direction/speed (weight 30%)
  - Premature mortality impact (weight 20%)
  - High-risk demographic concentration (weight 10%)
- Diseases ranked by composite priority score (1=highest priority)
- Ranking comparison to alternative weighting schemes provided (sensitivity analysis)
- Priority categories defined (Critical, High, Medium, Low)
- Benchmark comparison: Singapore burden vs. international peer countries (if data available)
- Interactive ranking visualization showing disease positions
- Findings report documenting ranking rationale and recommendations

## 2. 🔒 Technical Constraints

- **Index Calculation**: Normalize each component to 0-100 scale before weighting
- **Sensitivity**: Test alternative weightings to show robustness
- **Benchmarking**: Document data sources and year for international comparison

## 3. 📚 Domain Knowledge References

- [Disease Burden: Comparative Features](../../../domain_knowledge/disease-burden-mortality-analysis.md#comparative-features)
- [Disease Burden: Best Practices](../../../domain_knowledge/disease-burden-mortality-analysis.md#common-pitfalls-and-best-practices)

## 4. 📦 Dependencies

- **pandas**: Index calculation and ranking
- **plotly/seaborn**: Interactive visualization

## 5. ✅ Implementation Tasks

- ⬜ Normalize burden magnitude (ASMR) to 0-100 scale
- ⬜ Normalize trend score to 0-100 scale
- ⬜ Calculate premature mortality impact (Years of Life Lost proxy)
- ⬜ Calculate demographic concentration score
- ⬜ Combine components with defined weights
- ⬜ Rank diseases by composite score
- ⬜ Assign priority categories (Critical/High/Medium/Low)
- ⬜ Test sensitivity to alternative weightings
- ⬜ Benchmark vs. international burden data
- ⬜ Create ranking visualization
- ⬜ Document rationale and recommendations

---

# User Story 5: Disease Burden Dashboard and Stakeholder Analytics

**As a** MOH disease control program leader,  
**I want** an interactive dashboard showing disease burden rankings, trends, and demographic patterns,  
**so that** I can monitor disease burden and identify populations needing targeted prevention efforts.

## 1. 🎯 Acceptance Criteria

- Interactive dashboard displaying:
  - Disease priority rankings with composite scores
  - 30-year trend lines for all major diseases
  - Current ASMR by disease with comparison to targets
  - Age/gender burden distribution for each disease
- Filtering capability: Select diseases, time period, demographic group
- Alert system: Flag diseases with rising burden exceeding thresholds
- Comparative view: Disease-to-disease burden comparison
- Demographic risk view: Which age/gender groups at highest risk
- User guide documenting interpretation and data quality notes

## 2. 🔒 Technical Constraints

- **Platform**: Streamlit or Plotly/Dash
- **Interactivity**: Filters, comparisons, drill-down capability
- **Performance**: Dashboard load time <3 seconds
- **Accessibility**: Color-blind safe palette, legible text

## 3. 📚 Domain Knowledge References

- [Disease Burden: Public Health Implications](../../../domain_knowledge/disease-burden-mortality-analysis.md)

## 4. 📦 Dependencies

- **streamlit/plotly**: Dashboard framework
- **pandas/polars**: Data preparation

## 5. ✅ Implementation Tasks

- ⬜ Develop dashboard layout and design
- ⬜ Implement disease ranking visualization
- ⬜ Implement trend visualization (30-year time series)
- ⬜ Implement demographic burden breakdown
- ⬜ Add filtering for diseases, time period, demographics
- ⬜ Implement alert system for rising burden
- ⬜ Add comparative burden views
- ⬜ Create user guide
- ⬜ Test and optimize performance
- ⬜ Deploy dashboard

---

# User Story 6: Disease Burden Findings Report and Recommendations

**As a** MOH policy leadership,  
**I want** a comprehensive report communicating disease burden findings and prevention recommendations,  
**so that** I can allocate prevention program budgets based on evidence of disease burden.

## 1. 🎯 Acceptance Criteria

- Executive summary (2-3 pages): Top 5 disease priorities, key trends, recommendations
- Detailed findings: 
  - Current disease burden ranking with quantified ASMR
  - 30-year trend analysis showing rising vs. declining diseases
  - Age/gender risk stratification
  - Comparison to international benchmarks
  - Emerging disease trends requiring attention
- Recommendations:
  - Prevention program priorities aligned with burden
  - Resource allocation suggestions
  - High-risk population targeting
- Limitations and data quality notes
- Stakeholder feedback incorporated
- Professional PDF report suitable for leadership briefing

## 2. 🔒 Technical Constraints

- **Format**: Professional PDF
- **Accessibility**: Color-blind safe, legible fonts
- **Language**: Clear, non-technical for policy audience

## 3. 📚 Domain Knowledge References

- [Disease Burden: Common Pitfalls & Best Practices](../../../domain_knowledge/disease-burden-mortality-analysis.md#common-pitfalls-and-best-practices)

## 4. 📦 Dependencies

- **reportlab** or **python-pptx**: PDF/report generation

## 5. ✅ Implementation Tasks

- ⬜ Conduct stakeholder interviews to gather context and feedback
- ⬜ Write executive summary
- ⬜ Compile detailed findings with visualizations
- ⬜ Develop recommendations with evidence rationale
- ⬜ Document limitations and data quality
- ⬜ Format professionally
- ⬜ Incorporate stakeholder feedback
- ⬜ Finalize and distribute report
