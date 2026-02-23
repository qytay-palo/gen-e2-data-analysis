# User Story 3: Exploratory Disease Burden and Trend Analysis

**As a** public health analyst,  
**I want** to explore mortality patterns, trends, and demographic distributions across major diseases over 30 years,  
**so that** I can identify high-burden diseases, detect emerging trends, and formulate hypotheses for targeted disease burden analysis.

## 1. 🎯 Acceptance Criteria

- Exploratory analysis completed for all major diseases (cancer, stroke, ischemic heart disease)
- 30-year mortality trends (1990-2019) visualized for each disease
- Disease burden comparisons created showing absolute and relative mortality
- Demographic burden analysis completed (age-group and gender patterns)
- Trend classification identified: rising, stable, or declining burden by disease
- Key patterns documented: inflection points, acceleration/deceleration in burden
- EDA report generated with visualizations and initial findings
- Exploratory notebook and visualizations saved to `notebooks/2_analysis/ps-002/`
- Initial findings summary saved to `results/tables/ps-002/eda_findings_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Visualization**: Use matplotlib/seaborn for publication-quality charts
- **Statistical Analysis**: Use scipy for trend detection and statistical tests
- **Platform**: Local Python environment with Jupyter notebook for EDA
- **Output**: Save all visualizations to `reports/figures/ps-002/`

## 3. 📚 Domain Knowledge References

- [Disease Burden Metrics](../../../domain_knowledge/disease-burden-mortality-analysis.md#standard-metrics-and-kpis) - Standard burden quantification metrics
- [Trend Classification](../../../domain_knowledge/disease-burden-mortality-analysis.md#trend-classification) - Categorizing disease burden trajectories
- [Temporal Features](../../../domain_knowledge/disease-burden-mortality-analysis.md#trend-features) - Time-series feature engineering for disease trends

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data analysis and transformations
- **matplotlib**, **seaborn**: Visualization
- **scipy**: Statistical analysis and trend detection
- **numpy**: Numerical calculations

**Internal Dependencies:**
- Story 2 output: Cleaned mortality data in `data/3_interim/mortality_cleaned/`

## 5. ✅ Implementation Tasks

### Data Loading and Preparation
- ⬜ Load cleaned mortality datasets from interim folder
- ⬜ Verify data completeness and temporal coverage for EDA
- ⬜ Create working dataset with all diseases for comparative analysis
- ⬜ Set up Jupyter notebook for exploratory analysis

### Absolute Mortality Burden Analysis
- ⬜ Calculate total mortality burden by disease (sum ASMR across years)
- ⬜ Rank diseases by absolute mortality burden (highest to lowest)
- ⬜ Visualize disease burden comparison (bar chart: disease vs. total ASMR)
- ⬜ Calculate disease-specific mortality fractions (% of total mortality)
- ⬜ Identify top 3 diseases by absolute burden

### 30-Year Mortality Trend Visualization
- ⬜ Create line charts showing ASMR trends (1990-2019) for each major disease
- ⬜ Plot all diseases on same chart for comparative trend view
- ⬜ Add trend lines (linear regression) to visualize direction
- ⬜ Annotate key inflection points (years where trend direction changes)
- ⬜ Calculate trend slopes: mortality change per year for each disease

### Trend Classification
- ⬜ Calculate year-over-year growth rates for each disease
- ⬜ Classify diseases as "Rising" (>2% average annual increase), "Stable" (±2%), or "Declining" (>2% decrease)
- ⬜ Identify diseases with trend acceleration (growth rate increasing over time)
- ⬜ Flag diseases with inflection points (shift from declining to rising or vice versa)
- ⬜ Create summary table: disease, trend classification, average growth rate

### Demographic Burden Analysis
- ⬜ Analyze age-group-specific mortality rates for each disease
- ⬜ Identify which age groups bear highest burden by disease
- ⬜ Visualize age-stratified mortality (heat map or stacked area chart)
- ⬜ Compare male vs. female mortality burdens by disease
- ⬜ Calculate gender mortality ratios (male ASMR / female ASMR)
- ⬜ Identify diseases with significant gender disparities

### Comparative Disease Burden Analysis
- ⬜ Calculate relative disease burden (disease ASMR / average ASMR)
- ⬜ Create disease burden index showing relative severity
- ⬜ Compare burden trends across diseases side-by-side
- ⬜ Identify diseases with disproportionate burden in specific demographics
- ⬜ Generate comparative visualizations (small multiples or faceted charts)

### Hypothesis Formulation
- ⬜ Document key patterns observed (rising vs. declining diseases)
- ⬜ Formulate hypotheses for disease priority analysis
- ⬜ Identify diseases requiring urgent intervention based on rising trends
- ⬜ Note demographic segments with concentrated burden for targeting
- ⬜ List potential risk factors or interventions for exploration

### Visualization and Reporting
- ⬜ Save all visualizations to `reports/figures/ps-002/eda/`
- ⬜ Create publication-quality charts (300 DPI, labeled axes, clear titles)
- ⬜ Generate EDA findings summary markdown document
- ⬜ Document data quality observations from EDA
- ⬜ Save exploratory notebook to `notebooks/2_analysis/ps-002/`

## 6. Notes

**Key Visualizations to Create:**
1. Disease burden comparison bar chart (absolute ASMR totals)
2. 30-year trend lines for all major diseases (multi-line chart)
3. Trend classification summary (color-coded by rising/stable/declining)
4. Age-stratified burden heat map
5. Gender mortality ratio comparison
6. Small multiples showing disease-specific trends with demographic breakdowns

**Analytical Focus:**
- Identify the "highest priority" diseases by both absolute burden and trend direction
- Detect which demographics need targeted interventions
- Understand temporal patterns: are improvements plateauing? Are new threats emerging?

**Statistical Methods:**
- Linear regression for trend slopes
- Year-over-year percentage change for growth rates
- Simple moving averages to smooth volatility

**Related Stories:**
- Depends on: Story 2 (Cleaned mortality data)
- Enables: Story 4 (Feature engineering for burden metrics), Story 5 (Disease priority ranking)
