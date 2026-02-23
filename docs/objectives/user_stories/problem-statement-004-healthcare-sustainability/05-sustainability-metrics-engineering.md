# User Story 5: Sustainability Metrics Engineering and Trajectory Modeling

**As a** healthcare system planner,  
**I want** to calculate sustainability metrics (growth rates, gap indices, mismatch scores, trajectory extrapolations),  
**so that** I can quantify sustainability risks and project future gaps across healthcare system dimensions.

## 1. 🎯 Acceptance Criteria

- Comparative growth rate indices calculated for all dimensions (2006-2018)
- Mismatch indices calculated: supply-demand gap metrics, resource-utilization alignment scores
- Sustainability vulnerability scores computed: composite index across dimensions
- Trajectory extrapolation models fitted: linear and exponential projections to 2025/2030
- Projected gaps quantified: anticipated workforce shortages, capacity deficits, expenditure trajectories
- Scenario parameters defined: optimistic, baseline, pessimistic growth assumptions
- Feature engineering rationale documented with formulas and interpretation guidance
- Sustainability metrics dataset saved to `data/4_processed/` ready for advanced analysis
- Metrics documentation created explaining calculation methods and interpretation

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient feature calculations
- **Statistical Modeling**: Use scipy/statsmodels/scikit-learn for regression and projection
- **Projections**: Linear and exponential regression with confidence intervals
- **Validation**: Cross-validation where appropriate to assess projection accuracy
- **Output Format**: Parquet for metrics datasets, CSV for stakeholder-readable summaries
- **Documentation**: All formulas explicitly documented with interpretation guidance

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Feature Engineering Guidance](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#feature-engineering-guidance) - Sustainability metrics formulas
- [Healthcare System Sustainability Metrics: Multi-Dimensional Growth Rate Tracking](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#common-healthcare-sustainability-analytics-features) - Comparative growth indices
- [Healthcare System Sustainability Metrics: Forecasting Features](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#forecasting-features) - Projection methodologies
- [Healthcare Workforce Planning: Feature Engineering](../../../domain_knowledge/healthcare-workforce-planning.md#feature-engineering-guidance) - Workforce-specific metrics

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Feature engineering and calculations
- **numpy**: Numerical calculations
- **scipy**: Statistical methods
- **statsmodels**: Time series regression and forecasting
- **scikit-learn**: Regression models and validation

**Internal Dependencies:**
- Depends on: Story 3 (Data Preparation), Story 4 (Exploratory Analysis)
- Input from: `data/4_processed/sustainability_data_cleaned_2006_2018.parquet`
- Insights from: `results/tables/ps-004_exploratory_findings.md` (Story 4 findings guide feature selection)

## 5. ✅ Implementation Tasks

### Comparative Growth Rate Features
- ⬜ Calculate annual growth rates (year-over-year % change):
  - Workforce growth rate by profession and sector
  - Capacity growth rate (beds, facilities) by sector
  - Utilization growth rate (admissions) by demographic segment
  - Expenditure growth rate (real, inflation-adjusted) by category
  - Mortality rate changes by disease category
- ⬜ Calculate compound annual growth rate (CAGR) 2006-2018:
  - Formula: `((Value_2018 / Value_2006)^(1/12) - 1) × 100`
  - Calculate for all key metrics
- ⬜ Calculate relative growth indices (dimension growth relative to population growth):
  - Formula: `(Dimension_CAGR / Population_CAGR) × 100`
  - Interpretation: >100 = growing faster than population; <100 = lagging population
  - Calculate for workforce, capacity, utilization, expenditure
- ⬜ Create growth momentum feature (acceleration/deceleration):
  - Formula: `Growth_Rate[t] - Growth_Rate[t-1]`
  - Identify accelerating vs. slowing growth periods

### Supply-Demand Mismatch Indices
- ⬜ Calculate Workforce-Demand Mismatch Index:
  - Formula: `Workforce_Growth_Rate - Utilization_Growth_Rate`
  - Interpretation: Negative = workforce lagging demand (shortage risk)
  - Calculate overall and by sector
- ⬜ Calculate Capacity-Demand Mismatch Index:
  - Formula: `Capacity_Growth_Rate - Utilization_Growth_Rate`
  - Interpretation: Negative = capacity lagging demand (overcrowding risk)
- ⬜ Calculate Workforce-Capacity Alignment Index:
  - Formula: `Workforce_Growth_Rate - Capacity_Growth_Rate`
  - Interpretation: Large positive = workforce expanding faster than capacity (potential inefficiency)
- ⬜ Calculate Expenditure Efficiency Index:
  - Formula: `Expenditure_Growth_Rate - (Workforce_Growth_Rate + Capacity_Growth_Rate) / 2`
  - Interpretation: Positive = spending increasing without proportional resource expansion
- ⬜ Calculate cumulative mismatch: sum of annual mismatch indices 2006-2018
- ⬜ Apply thresholds: flag sectors where cumulative mismatch >10% or <-10%

### Sustainability Ratio Features
- ⬜ Calculate and track over time:
  - Workforce-to-bed ratio: `Total_Workforce / Total_Beds`
  - Workforce-to-population density: `Total_Workforce / Population × 1,000`
  - Bed-to-population ratio: `Total_Beds / Population × 1,000`
  - Admissions-per-bed: `Total_Admissions / Total_Beds`
  - Bed utilization rate: `(Admissions × Avg_LOS) / (Beds × 365) × 100`
  - Expenditure-per-capita: `Total_Expenditure / Population`
  - Expenditure-per-healthcare-worker: `Total_Expenditure / Total_Workforce`
- ⬜ Calculate trend in ratios: Are key ratios improving, stable, or deteriorating?
- ⬜ Compare ratios to benchmarks (WHO, OECD standards where available)

### Composite Sustainability Vulnerability Score
- ⬜ Define sustainability vulnerability score (composite index):
  - **Workforce Adequacy (30% weight)**: Based on workforce-demand mismatch index
  - **Capacity Adequacy (25% weight)**: Based on capacity-demand mismatch index
  - **Financial Sustainability (25% weight)**: Based on expenditure growth relative to economic growth
  - **Utilization Balance (20% weight)**: Based on bed utilization rate (optimal 70-85%)
- ⬜ Normalize components to 0-100 scale:
  - 100 = optimal sustainability
  - 50 = significant risk
  - <30 = critical risk
- ⬜ Calculate weighted composite score by sector and year
- ⬜ Identify sectors/years with low sustainability scores requiring intervention
- ⬜ Track sustainability score trends 2006-2018: improving or deteriorating?

### Demographic Risk Index
- ⬜ Calculate demographic-driven demand pressure:
  - Formula: `(Aging_Population_Growth + Chronic_Disease_Prevalence_Increase) / (Workforce_Growth + Capacity_Growth)`
  - Interpretation: >1.0 = demand drivers outpacing resource expansion
- ⬜ Calculate age-specific utilization intensity:
  - Admissions per capita by age group
  - Identify which age groups driving demand most
- ⬜ Project demographic risk: Apply demographic projections (if available) to estimate future demand

### Trajectory Extrapolation and Forecasting
- ⬜ Fit linear regression models for each dimension:
  - Dependent variable: Metric value (workforce count, bed count, admissions, expenditure)
  - Independent variable: Year (2006-2018)
  - Extract slope (annual change) and R² (trend strength)
- ⬜ Fit exponential regression models:
  - For metrics exhibiting exponential growth patterns
  - Compare linear vs. exponential fit (select best R²)
- ⬜ Generate projections to 2025 and 2030:
  - Project workforce supply: apply historical growth trajectory
  - Project capacity: apply historical expansion trajectory
  - Project demand (utilization): apply demographic-adjusted growth
  - Project expenditure: apply historical spending trajectory
- ⬜ Calculate 95% confidence intervals for projections:
  - Use regression prediction intervals
  - Communicate uncertainty in projections
- ⬜ Identify projected crossover points:
  - When will demand exceed supply?
  - When will expenditure exceed budget constraints?

### Scenario-Based Projection Features
- ⬜ Define scenario parameters:
  - **Optimistic Scenario**: Historical maximum growth rates applied
  - **Baseline Scenario**: Historical average growth rates applied
  - **Pessimistic Scenario**: Historical minimum growth rates applied
- ⬜ Generate multi-scenario projections:
  - Workforce projections under each scenario
  - Capacity projections under each scenario
  - Expenditure projections under each scenario
- ⬜ Calculate scenario-specific gap estimates:
  - Best case: Optimistic supply vs. baseline demand
  - Expected case: Baseline supply vs. baseline demand
  - Worst case: Pessimistic supply vs. optimistic demand
- ⬜ Quantify gap magnitude: personnel shortage, bed deficit, expenditure shortfall

### Gap Quantification and Impact Estimation
- ⬜ Calculate projected gaps by dimension:
  - **Workforce Gap 2030**: Projected demand - projected workforce supply
    - Express as absolute shortfall and % shortage
  - **Capacity Gap 2030**: Projected demand - projected bed capacity
    - Express as bed deficit and % shortfall
  - **Financial Gap 2030**: Projected expenditure - sustainable budget envelope
    - Express as SGD shortfall and % over budget
- ⬜ Translate gaps to impact metrics:
  - Workforce shortage → Patients per healthcare worker (workload impact)
  - Capacity shortage → Bed utilization rate (overcrowding impact)
  - Expenditure gap → Budget deficit as % of GDP
- ⬜ Prioritize gaps: Which dimension faces most severe projected challenge?

### Validation and Sensitivity Analysis
- ⬜ Backtest projections: Use 2006-2014 to project 2015-2018, compare to actuals
- ⬜ Calculate projection accuracy: Mean Absolute Percentage Error (MAPE)
- ⬜ Conduct sensitivity analysis: How do projections change with ±20% growth rate adjustment?
- ⬜ Document projection limitations:
  - Assumes historical trends continue (disruptions like COVID-19 invalidate)
  - Does not incorporate policy interventions
  - Uncertainty increases with projection horizon

### Feature Documentation and Interpretation Guide
- ⬜ Create metrics documentation table:
  - Metric name
  - Formula
  - Interpretation guidance (what values mean)
  - Expected range (benchmarks)
  - Use case
- ⬜ Create interpretation guide for stakeholders:
  - How to read mismatch indices
  - How to interpret sustainability scores
  - How to use projections for planning
  - Limitations and caveats
- ⬜ Save to `docs/data_dictionary/sustainability_metrics.md`

### Output and Deliverables
- ⬜ Save sustainability metrics dataset:
  - `data/4_processed/sustainability_metrics_2006_2018.parquet` (historical metrics)
  - `data/4_processed/sustainability_projections_2019_2030.parquet` (forecasts)
- ⬜ Save summary tables:
  - `results/tables/ps-004_growth_rate_summary.csv`
  - `results/tables/ps-004_mismatch_indices.csv`
  - `results/tables/ps-004_sustainability_scores.csv`
  - `results/tables/ps-004_projections_2030.csv`
  - `results/tables/ps-004_gap_quantification.csv`
- ⬜ Save metrics documentation:
  - `docs/data_dictionary/sustainability_metrics.md`
- ⬜ Create visualizations:
  - Mismatch index trends by dimension
  - Sustainability vulnerability score trends
  - Trajectory projections with confidence intervals (2006-2030)
  - Scenario comparison charts
  - Gap magnitude charts (2030 projections)
- ⬜ Save visualizations to `reports/figures/ps-004/feature-engineering/`

## 6. Notes

**Projection Methodology**:
- Linear projections suitable for stable trends (workforce, capacity growth)
- Exponential projections for accelerating trends (expenditure, demand growth)
- Confidence intervals essential to communicate uncertainty
- Projections valid only if historical trends continue (major policy changes invalidate)

**Composite Score Weighting Rationale**:
- Workforce adequacy 30% - largest weight as workforce shortages most critical
- Capacity and financial sustainability 25% each - equally important strategic dimensions
- Utilization balance 20% - operational metric, less strategic than resource dimensions

**Scenario Planning Importance**: Scenarios enable strategic planning under uncertainty. Optimistic scenario identifies best-case planning needs; pessimistic scenario identifies risk mitigation requirements.

**Domain Knowledge Application**: Feature engineering heavily informed by domain knowledge (healthcare sustainability frameworks, workforce planning principles). Validate metrics with healthcare planning experts.

**Related Stories**: 
- Depends on: Story 3 (Data Preparation), Story 4 (Exploratory Analysis)
- Feeds into: Story 6 (Advanced Analysis), Story 7 (Dashboard & Reporting)

**Estimated Effort**: 1.5 sprints (includes metric calculation, projection modeling, validation)
