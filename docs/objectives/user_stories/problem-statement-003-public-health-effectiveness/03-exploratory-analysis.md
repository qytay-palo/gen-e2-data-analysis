# User Story 3: School Health Program Coverage and Outcome Exploratory Analysis

**As a** public health program analyst,  
**I want** to perform exploratory analysis of vaccination coverage rates and school health screening outcomes over time,  
**so that** I can identify trends, patterns, and initial insights about program effectiveness and health outcome improvements.

## 1. 🎯 Acceptance Criteria

- Coverage rate trends visualized for all vaccination programs (2003-2020)
- School health screening participation rates analyzed by program type
- Health outcome trends analyzed (dental health, obesity prevalence, common health problems)
- Year-over-year changes in coverage and outcomes quantified
- Program performance patterns identified (improving, stable, declining)
- Cohort-level comparisons conducted (age groups, grade levels)
- Initial hypotheses formulated about coverage gaps and effectiveness
- EDA report generated with key findings and visualizations
- Report saved to `results/exploratory_analysis/school_health_eda_report_{timestamp}.md`
- Key visualizations exported to `reports/figures/school_health/`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for aggregation and analysis
- **Visualization**: Use matplotlib/seaborn for exploratory visualizations
- **Platform**: Local Python environment
- **Statistical Analysis**: Use scipy for basic trend analysis and correlation
- **Documentation**: Document all analytical findings with supporting evidence

## 3. 📚 Domain Knowledge References

- [Vaccination Coverage](../../../domain_knowledge/public-health-programs-vaccination.md#vaccination-coverage) - Coverage targets and interpretation
- [School Health Program Effectiveness](../../../domain_knowledge/public-health-programs-vaccination.md#school-health-program-effectiveness) - Key indicators and program types
- [Coverage Gap Analysis](../../../domain_knowledge/public-health-programs-vaccination.md#coverage-gap-analysis) - Types of gaps and patterns
- [Standard Metrics and KPIs](../../../domain_knowledge/public-health-programs-vaccination.md#standard-metrics-and-kpis) - Target ranges for interpretation

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data aggregation and analysis
- **matplotlib**: Visualization
- **seaborn**: Statistical visualizations
- **scipy**: Trend analysis and statistical tests
- **numpy**: Numerical computations

**Internal Dependencies:**
- Output from Story 2: Clean vaccination coverage and screening data
- `src/utils/logger.py`: Logging utilities
- `src/visualization/`: Visualization utilities (create if needed)

## 5. ✅ Implementation Tasks

### Data Preparation for EDA
- ⬜ Load cleaned vaccination coverage data from `data/4_processed/school_health/`
- ⬜ Load cleaned school health screening data
- ⬜ Verify data quality and completeness for analysis
- ⬜ Create analysis-ready datasets with consistent temporal structure
- ⬜ Document data characteristics (time range, cohorts, metrics available)

### Vaccination Coverage Trend Analysis
- ⬜ Calculate coverage rates by vaccine type and year
- ⬜ Visualize coverage trends for all vaccines over 17-year period
- ⬜ Identify vaccines achieving >90% target coverage
- ⬜ Detect vaccines with below-target coverage (<85%)
- ⬜ Calculate year-over-year coverage change rates
- ⬜ Classify trend patterns: improving (increasing coverage), stable, declining
- ⬜ Identify inflection points or sudden coverage changes

### School Health Screening Participation Analysis
- ⬜ Calculate screening participation rates by program type and year
- ⬜ Visualize participation trends (dental, obesity, health problem screening)
- ⬜ Assess achievement of >90% participation target
- ⬜ Identify programs with increasing vs. decreasing participation
- ⬜ Analyze temporal patterns (consistent vs. variable participation)
- ⬜ Document any participation gaps or program discontinuations

### Health Outcome Trend Analysis
- ⬜ Analyze dental health trends (DMFT index over time)
- ⬜ Analyze obesity prevalence trends by cohort
- ⬜ Analyze common health problem prevalence trends
- ⬜ Visualize outcome trends with confidence intervals
- ⬜ Identify improving vs. worsening health outcomes
- ⬜ Correlate health outcomes with screening participation rates
- ⬜ Document potential program impact on health improvements

### Cohort and Demographic Analysis
- ⬜ Compare coverage rates across age groups/grade levels
- ⬜ Analyze screening participation by cohort
- ⬜ Identify cohorts with highest/lowest coverage
- ⬜ Assess whether coverage varies by demographic segment (where data available)
- ⬜ Document cohort-specific patterns requiring targeted intervention

### Program Performance Benchmarking
- ⬜ Compare coverage rates against WHO/MOH targets (85-95%)
- ⬜ Identify high-performing programs (>90% coverage consistently)
- ⬜ Identify underperforming programs (<80% coverage)
- ⬜ Analyze gap between current and target coverage
- ⬜ Estimate number of students not reached by programs
- ⬜ Prioritize programs with largest coverage gaps

### Correlation and Relationship Analysis
- ⬜ Analyze correlation between coverage rates and health outcomes
- ⬜ Investigate relationship between screening participation and outcome detection
- ⬜ Explore temporal relationships (lag between coverage and health impact)
- ⬜ Identify potential confounding factors (methodology changes, demographic shifts)
- ⬜ Formulate hypotheses about program effectiveness mechanisms

### Statistical Summary Generation
- ⬜ Calculate summary statistics for all coverage metrics
- ⬜ Generate distribution analysis (mean, median, quartiles) by program
- ⬜ Perform statistical tests for trend significance (linear regression, Mann-Kendall)
- ⬜ Calculate coefficient of variation to assess coverage stability
- ⬜ Document statistical findings with confidence levels

### Visualization Development
- ⬜ Create time series plots for vaccination coverage by vaccine type
- ⬜ Create time series plots for school health screening participation
- ⬜ Create health outcome trend visualizations (dental, obesity, health problems)
- ⬜ Generate comparative bar charts (coverage by cohort)
- ⬜ Create heatmaps showing coverage patterns across years and programs
- ⬜ Develop summary dashboard with key trends
- ⬜ Export all visualizations to `reports/figures/school_health/`

### Hypothesis Formulation
- ⬜ Formulate hypotheses about coverage gap causes
- ⬜ Hypothesize about demographic populations with lower coverage
- ⬜ Propose explanations for health outcome trends
- ⬜ Identify programs requiring deeper investigation
- ⬜ Document hypotheses for validation in Story 4 (Coverage Gap Analysis)

### EDA Report Generation
- ⬜ Create comprehensive markdown EDA report
- ⬜ Include executive summary with key finding highlights
- ⬜ Document coverage trends for all programs
- ⬜ Document health outcome trends and patterns
- ⬜ Include all visualizations with interpretations
- ⬜ List initial hypotheses and questions for further analysis
- ⬜ Provide recommendations for targeted analysis in subsequent stories
- ⬜ Save report to `results/exploratory_analysis/school_health_eda_report.md`

## 6. Notes

**Coverage Target Reference:**
- Single-dose vaccines: 90%+ population coverage
- Multi-dose vaccine series: 80%+ completion
- School screening: >90% participation target

**Trend Classification:**
- **Improving**: Coverage increasing >5 percentage points over analysis period
- **Stable**: Coverage change within ±5 percentage points
- **Declining**: Coverage decreasing >5 percentage points

**Health Outcome Interpretation:**
- Dental Health: Lower DMFT index = better oral health
- Obesity: Monitor trends; increasing prevalence = concern
- Common Health Problems: Increasing detection may indicate better screening OR worsening health

**Statistical Significance:**
- Use p<0.05 threshold for trend significance
- Report confidence intervals for all trend estimates
- Apply Bonferroni correction for multiple comparisons

**Temporal Considerations:**
- Data lag: Most recent data from 2020 (5-year lag)
- Consider potential COVID-19 impact on 2020 data
- Document any methodology changes affecting time series comparability

**Related Stories:**
- Depends on Story 2 (Clean Data)
- Informs Story 4 (Coverage Gap Analysis) with initial patterns
- Provides foundation for Story 5 (Dashboard Development)
- Feeds Story 6 (Recommendations) with evidence-based insights

**Stakeholder Value:**
- Provides first comprehensive view of program performance over 17 years
- Identifies high-priority programs requiring improvement
- Validates program success stories for communication

---

**Story Version**: 1.0  
**Created**: February 23, 2026  
**Status**: Ready for Sprint Planning
