# User Story 4: Multi-Dimensional Exploratory Trend Analysis

**As a** strategic planning analyst,  
**I want** to analyze 15+ year historical trends across all healthcare system dimensions (workforce, capacity, utilization, expenditure, mortality),  
**so that** I can identify key patterns, growth trajectories, and preliminary sustainability risks to inform deeper analysis.

## 1. 🎯 Acceptance Criteria

- Time series plots created for all dimensions showing 2006-2018 trends
- Growth rate analysis completed for each dimension with trend classification (accelerating, stable, declining)
- Comparative trend analysis across dimensions identifying misalignments
- Sector-specific trend patterns identified and documented
- Correlation analysis completed showing relationships between dimensions
- Preliminary sustainability risks identified based on trend divergences
- Exploratory findings documented with supporting visualizations
- EDA report saved to `results/tables/` with key insights highlighted
- All visualizations saved to `reports/figures/ps-004/exploratory/`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient time series aggregations
- **Visualization**: Use matplotlib/seaborn for publication-quality charts
- **Statistical Analysis**: Use scipy/statsmodels for trend detection and correlation
- **Trend Classification**: Use regression slope and R² for trend characterization
- **Output Format**: PNG/PDF for visualizations, markdown for EDA report

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Multi-Dimensional Framework](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#healthcare-system-sustainability-dimensions) - Expected sustainability patterns
- [Healthcare System Sustainability Metrics: Comparative Trend Analysis](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#feature-engineering-guidance) - Growth rate interpretation
- [Healthcare Workforce Planning: Domain-Specific Patterns](../../../domain_knowledge/healthcare-workforce-planning.md#domain-specific-patterns) - Workforce trend interpretation
- [Disease Burden and Mortality Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md) - Mortality trend context

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Time series aggregations and calculations
- **matplotlib**: Visualization creation
- **seaborn**: Statistical visualizations
- **scipy**: Statistical analysis and correlation
- **statsmodels**: Trend line fitting and decomposition

**Internal Dependencies:**
- Depends on: Story 3 (Data Preparation) - cleaned datasets
- Input from: `data/4_processed/sustainability_data_cleaned_2006_2018.parquet`
- Reuse: `src/visualization/` utilities (if available from prior problem statements)

## 5. ✅ Implementation Tasks

### Workforce Dimension Exploratory Analysis
- ⬜ Create time series plot: Total workforce 2006-2018 (all professions combined)
- ⬜ Create profession-specific plots: Doctors, Nurses, Pharmacists trends
- ⬜ Calculate annual growth rates: year-over-year % change for each profession
- ⬜ Fit trend lines: linear regression to identify acceleration/deceleration
- ⬜ Sector comparison: Public vs. Private vs. Not-for-Profit workforce trends
- ⬜ Professional composition analysis: Doctor-to-nurse ratio trends over time
- ⬜ Identify patterns:
  - Which professions growing fastest/slowest?
  - Any inflection points (policy changes)?
  - Sector-specific growth differences?
- ⬜ Document key findings: workforce dimension patterns

### Capacity Dimension Exploratory Analysis
- ⬜ Create time series plot: Total hospital beds 2009-2018 (note limited historical data)
- ⬜ Create facility-specific plots: Hospital beds vs. primary care facilities
- ⬜ Calculate annual capacity expansion rates: year-over-year % change
- ⬜ Fit trend lines: identify capacity expansion trajectory
- ⬜ Sector comparison: Public vs. Private capacity growth
- ⬜ Identify patterns:
  - Steady capacity expansion or episodic (new hospital openings)?
  - Sector differences in capacity investment?
  - Capacity growth accelerating or slowing?
- ⬜ Document key findings: capacity dimension patterns

### Utilization Dimension Exploratory Analysis
- ⬜ Create time series plot: Total hospital admissions 2006-2018
- ⬜ Create demographic breakdown plots: Admissions by age group and gender
- ⬜ Calculate annual admission rate changes: year-over-year % change
- ⬜ Fit trend lines: identify demand growth trajectory
- ⬜ Demographic trend analysis: Which age groups driving admission growth?
- ⬜ Calculate bed utilization rates: admissions relative to bed capacity
- ⬜ Identify patterns:
  - Demand growing faster/slower than capacity?
  - Aging population driving admission growth?
  - Gender-specific utilization patterns?
- ⬜ Document key findings: utilization dimension patterns

### Expenditure Dimension Exploratory Analysis
- ⬜ Create time series plot: Real government health expenditure 2006-2018 (inflation-adjusted)
- ⬜ Create expenditure category breakdown: spending by sector or program area
- ⬜ Calculate annual expenditure growth rates: real year-over-year % change
- ⬜ Fit trend lines: identify spending trajectory (accelerating, stable, controlled)
- ⬜ Calculate per-capita expenditure trends: spending per person (if population data available)
- ⬜ Compare expenditure growth to GDP growth: assess fiscal sustainability
- ⬜ Identify patterns:
  - Spending outpacing economic growth?
  - Which expenditure categories growing fastest?
  - Any cost control inflection points?
- ⬜ Document key findings: financial sustainability patterns

### Mortality Dimension Exploratory Analysis
- ⬜ Create time series plot: All-cause mortality rate 2006-2018
- ⬜ Create disease-specific plots: Leading causes of mortality trends
- ⬜ Calculate annual mortality rate changes: year-over-year % change
- ⬜ Identify disease burden shifts: which diseases increasing/decreasing in mortality
- ⬜ Correlate mortality trends with utilization: high-mortality diseases driving admissions?
- ⬜ Identify patterns:
  - Overall mortality improving or worsening?
  - Chronic disease mortality trends (diabetes, heart disease)?
  - Infectious disease mortality trends?
- ⬜ Document key findings: population health burden patterns

### Comparative Multi-Dimensional Trend Analysis
- ⬜ Create indexed growth chart: All dimensions indexed to 2006 = 100
  - Workforce growth trajectory
  - Capacity growth trajectory
  - Utilization growth trajectory
  - Expenditure growth trajectory
  - Mortality trends (inverse)
- ⬜ Calculate comparative growth rates: average annual growth by dimension
- ⬜ Identify growth rate misalignments:
  - Demand (utilization) growing faster than supply (workforce, capacity)?
  - Expenditure growing faster than workforce/capacity expansion?
  - Mortality burden shifting while resources static?
- ⬜ Create heatmap: Year-over-year growth rates across all dimensions
- ⬜ Document comparative patterns: which dimensions aligned vs. diverging?

### Correlation and Relationship Analysis
- ⬜ Calculate correlation matrix: Pearson correlation across all dimensions
  - Workforce vs. Capacity
  - Workforce vs. Utilization
  - Capacity vs. Utilization
  - Expenditure vs. Workforce
  - Expenditure vs. Capacity
  - Mortality vs. Utilization
- ⬜ Create scatter plots: Key dimension relationships
  - Workforce growth vs. Capacity growth (expect positive correlation)
  - Expenditure growth vs. Workforce growth (expect positive correlation)
  - Utilization growth vs. Capacity growth (assess if aligned)
- ⬜ Identify unexpected relationships:
  - Strong correlations requiring explanation
  - Weak correlations indicating misalignment
- ⬜ Document relationship insights

### Preliminary Sustainability Risk Identification
- ⬜ Identify workforce sustainability risks:
  - Workforce growth lagging demand growth? (potential shortages)
  - Workforce-to-capacity ratios declining? (understaffing)
- ⬜ Identify capacity sustainability risks:
  - Capacity growth lagging demand growth? (overcrowding risk)
  - Utilization rates exceeding optimal threshold? (>85% utilization)
- ⬜ Identify financial sustainability risks:
  - Expenditure growth outpacing economic growth? (fiscal pressure)
  - Expenditure growing without corresponding workforce/capacity expansion? (inefficiency)
- ⬜ Identify utilization sustainability risks:
  - Demand growth accelerating? (future capacity challenges)
  - Demographic shifts driving utilization? (aging population impact)
- ⬜ Prioritize risks: rank by severity and immediacy
- ⬜ Document preliminary risk assessment for deeper investigation in Story 6

### Sector-Specific Pattern Analysis
- ⬜ Compare Public vs. Private sector trends across dimensions:
  - Workforce growth rates
  - Capacity expansion rates
  - Expenditure allocation
- ⬜ Identify sector-specific sustainability patterns:
  - Public sector specific challenges?
  - Private sector specific challenges?
  - Cross-sector divergences requiring attention?
- ⬜ Document sector comparison insights

### Visualization Suite Creation
- ⬜ Create comprehensive exploratory visualization suite:
  - Time series plots for each dimension (5 plots)
  - Indexed growth comparison chart (1 plot)
  - Correlation matrix heatmap (1 plot)
  - Sector comparison charts (3-4 plots)
  - Growth rate heatmap across years and dimensions (1 plot)
  - Key relationship scatter plots (3-4 plots)
- ⬜ Apply consistent styling: clear titles, axis labels, legends
- ⬜ Add annotations: policy changes, data limitations
- ⬜ Save all visualizations to `reports/figures/ps-004/exploratory/`

### EDA Report Documentation
- ⬜ Create comprehensive EDA report documenting:
  1. **Executive Summary**
     - Key patterns identified across dimensions
     - Preliminary sustainability risks highlighted
     - Recommendations for deeper investigation
  2. **Workforce Dimension Findings**
     - Trends, growth rates, sector patterns
     - Composition shifts (professional mix)
  3. **Capacity Dimension Findings**
     - Expansion trends, sector investments
     - Capacity adequacy relative to demand
  4. **Utilization Dimension Findings**
     - Demand growth patterns, demographic drivers
     - Bed utilization intensity
  5. **Expenditure Dimension Findings**
     - Spending growth trends, fiscal sustainability
     - Expenditure efficiency patterns
  6. **Mortality Dimension Findings**
     - Disease burden trends, mortality shifts
     - Implications for resource planning
  7. **Comparative Multi-Dimensional Insights**
     - Growth rate alignments and misalignments
     - Cross-dimensional correlations
     - Preliminary sustainability risk assessment
  8. **Sector-Specific Patterns**
     - Public, Private, Not-for-Profit comparisons
  9. **Recommendations for Advanced Analysis**
     - Metrics to engineer (Story 5)
     - Deep-dive analyses needed (Story 6)
- ⬜ Save EDA report to `results/tables/ps-004_exploratory_findings.md`

### Output and Deliverables
- ⬜ Save summary statistics tables: `results/tables/ps-004_dimension_trends_summary.csv`
- ⬜ Save correlation matrix: `results/tables/ps-004_dimension_correlations.csv`
- ⬜ Save growth rate summary: `results/tables/ps-004_growth_rates_by_dimension.csv`
- ⬜ Save all visualizations: `reports/figures/ps-004/exploratory/`
- ⬜ Save EDA report: `results/tables/ps-004_exploratory_findings.md`

## 6. Notes

**Trend Classification Approach**:
- **Accelerating**: Positive and increasing slope (R² > 0.7)
- **Stable**: Consistent slope with moderate fit (R² > 0.5)
- **Declining**: Negative or decreasing slope
- **Volatile**: Low R² (<0.5) indicating inconsistent pattern

**Data Limitations Context**:
- Capacity data limited to 2009-2018: shorter time series reduces trend detection power
- Expenditure data through 2018 only: missing recent years
- Population data may be external: affects per-capita calculations

**Exploratory vs. Confirmatory**: This story focuses on hypothesis generation and pattern identification. Story 6 (Advanced Analysis) will conduct confirmatory statistical analysis and scenario modeling.

**Related Stories**: 
- Depends on: Story 3 (Data Preparation)
- Feeds into: Story 5 (Feature Engineering), Story 6 (Advanced Analysis)

**Estimated Effort**: 1.5 sprints (includes analysis, visualization, reporting across 5 dimensions)
