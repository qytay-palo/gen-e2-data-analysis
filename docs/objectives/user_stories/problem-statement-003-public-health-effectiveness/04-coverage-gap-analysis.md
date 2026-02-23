# User Story 4: Coverage Gap Identification and Demographic Pattern Analysis

**As a** school health program manager,  
**I want** to identify specific populations and cohorts with below-target vaccination coverage and screening participation,  
**so that** I can design targeted outreach interventions and allocate resources to close coverage gaps equitably.

## 1. 🎯 Acceptance Criteria

- Coverage gaps quantified for all vaccination programs (populations not reaching 85-95% targets)
- Screening participation gaps identified by program type
- Demographic patterns in coverage analyzed (age groups, grade levels, cohorts)
- Number of students not reached by programs estimated
- Coverage equity metrics calculated (disparity ratios, equity gaps)
- Priority populations identified for targeted intervention
- Gap analysis report generated with actionable recommendations
- Coverage gap dataset created for program planning
- Report saved to `results/tables/coverage_gap_analysis_{timestamp}.csv`
- Analysis summary saved to `results/exploratory_analysis/coverage_gap_report.md`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for gap analysis and segmentation
- **Statistical Analysis**: Use scipy for disparity testing and significance
- **Platform**: Local Python environment
- **Visualization**: Matplotlib/seaborn for gap visualization
- **Documentation**: Document all gap identification methodologies

## 3. 📚 Domain Knowledge References

- [Coverage Gap Analysis](../../../domain_knowledge/public-health-programs-vaccination.md#coverage-gap-analysis) - Types of gaps and identification methods
- [Coverage Equity Index](../../../domain_knowledge/public-health-programs-vaccination.md#coverage-features) - Quantifying disparities
- [Standard Metrics - Coverage Equity Gap](../../../domain_knowledge/public-health-programs-vaccination.md#standard-metrics-and-kpis) - Target: <5% gap between demographic groups

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data segmentation and gap analysis
- **scipy**: Statistical significance testing
- **matplotlib/seaborn**: Gap visualizations
- **numpy**: Numerical computations

**Internal Dependencies:**
- Output from Story 2: Clean vaccination and screening data
- Output from Story 3: EDA findings informing gap analysis focus
- `src/analysis/`: Analysis utilities (create gap analysis module)
- `src/utils/logger.py`: Logging utilities

## 5. ✅ Implementation Tasks

### Coverage Gap Calculation
- ⬜ Identify target coverage rates for each vaccine/program (85-95% range)
- ⬜ Calculate gap to target: (Target Coverage % - Actual Coverage %)
- ⬜ Quantify gap for each vaccine type and year
- ⬜ Calculate absolute gap (percentage points) and relative gap (percentage)
- ⬜ Identify programs consistently below target across multiple years
- ⬜ Prioritize gaps by magnitude and affected population size

### Population Not Reached Estimation
- ⬜ Calculate number of students not vaccinated by vaccine type
- ⬜ Estimate students not participating in screening programs
- ⬜ Calculate cumulative unvaccinated population across all vaccines
- ⬜ Estimate at-risk population due to coverage gaps
- ⬜ Project future coverage needs based on cohort size trends
- ⬜ Document assumptions in population estimation methodology

### Demographic and Cohort Gap Analysis
- ⬜ Segment coverage by age group/grade level
- ⬜ Identify cohorts with lowest coverage rates
- ⬜ Compare coverage across demographic segments (where data available)
- ⬜ Calculate disparity ratios between highest and lowest coverage groups
- ⬜ Test statistical significance of coverage differences between groups
- ⬜ Identify systematic vs. random coverage variations

### Coverage Equity Assessment
- ⬜ Calculate Coverage Equity Index: (Min Coverage / Max Coverage) × 100
- ⬜ Assess whether equity index meets >90% target (10% disparity threshold)
- ⬜ Identify programs with largest equity gaps (>10% disparity)
- ⬜ Analyze temporal trends in equity (improving vs. worsening)
- ⬜ Calculate Gini coefficient for coverage distribution equity (if applicable)
- ⬜ Document equity gaps requiring policy attention

### Temporal Persistence Analysis
- ⬜ Identify coverage gaps persisting across multiple years
- ⬜ Distinguish chronic gaps (present 5+ years) from emerging gaps
- ⬜ Analyze whether gaps are widening or narrowing over time
- ⬜ Assess impact of past interventions on gap closure
- ⬜ Project gap trends if current patterns continue

### Geographic and System-Level Gap Analysis
- ⬜ Analyze aggregate data for potential geographic patterns (if proxies available)
- ⬜ Identify systemic barriers suggested by coverage patterns
- ⬜ Assess whether gaps correlate with program implementation timing
- ⬜ Investigate potential access barriers (school-level vs. system-level)
- ⬜ Document limitations due to lack of school-specific data

### Root Cause Hypothesis Development
- ⬜ Formulate hypotheses about causes of coverage gaps:
  - Access barriers (program availability, timing, locations)
  - Awareness gaps (parent/student knowledge of programs)
  - Vaccine hesitancy or screening refusal
  - Methodological factors (denominator definition, reporting)
- ⬜ Prioritize hypotheses for stakeholder validation
- ⬜ Recommend data collection to validate hypotheses
- ⬜ Document evidence supporting each hypothesis

### Priority Population Identification
- ⬜ Rank populations by coverage gap magnitude and affected population size
- ⬜ Identify high-priority cohorts for targeted intervention
- ⬜ Estimate resource requirements for gap closure
- ⬜ Assess feasibility of reaching target coverage for each priority group
- ⬜ Create priority matrix (coverage gap × population size)
- ⬜ Generate actionable list of priority populations

### Comparative Benchmarking
- ⬜ Compare coverage gaps to WHO/international benchmarks
- ⬜ Assess whether gaps are improving faster than peer countries
- ⬜ Identify best-in-class coverage rates as improvement targets
- ⬜ Document where Singapore programs exceed vs. fall short of benchmarks
- ⬜ Provide context for stakeholder gap interpretation

### Gap Analysis Visualization
- ⬜ Create coverage gap heatmaps (program × year, showing gap magnitude)
- ⬜ Visualize gap trends over time by program
- ⬜ Create population-not-reached visualizations (stacked bars or Pareto charts)
- ⬜ Develop equity gap visualizations (disparity ratios across groups)
- ⬜ Generate priority matrix visualization (gap size × affected population)
- ⬜ Export visualizations to `reports/figures/school_health/coverage_gaps/`

### Gap Analysis Dataset Creation
- ⬜ Create structured dataset with gap metrics:
  - Program/vaccine identifier
  - Year
  - Target coverage %
  - Actual coverage %
  - Gap to target (absolute and relative)
  - Students not reached (count)
  - Priority ranking
- ⬜ Save to `results/tables/coverage_gap_analysis.csv`
- ⬜ Document dataset schema and usage instructions

### Gap Analysis Report Generation
- ⬜ Create comprehensive gap analysis markdown report
- ⬜ Include executive summary with key gap findings
- ⬜ Document coverage gaps by program with visualizations
- ⬜ Present demographic disparity analysis
- ⬜ Provide priority population list with recommended interventions
- ⬜ Include temporal trend analysis of gap persistence
- ⬜ List root cause hypotheses for stakeholder validation
- ⬜ Provide actionable recommendations for gap closure
- ⬜ Save report to `results/exploratory_analysis/coverage_gap_report.md`

## 6. Notes

**Coverage Gap Definition:**
- **Critical Gap**: Coverage <80% (>20% gap to 100%, or >15% gap to 85% target)
- **Moderate Gap**: Coverage 80-85% (5-15% gap to 85% target)
- **Minor Gap**: Coverage 85-90% (approaching but below 90% optimal target)
- **Acceptable**: Coverage >90%

**Equity Gap Threshold:**
- Equity Index >90% (disparity <10%) = Acceptable equity
- Equity Index 80-90% (disparity 10-20%) = Moderate inequity requiring attention
- Equity Index <80% (disparity >20%) = Severe inequity requiring urgent action

**Population Impact Prioritization:**
- High Priority: Large gap (>15%) affecting >1,000 students
- Medium Priority: Moderate gap (5-15%) affecting >500 students or large gap affecting <1,000
- Lower Priority: Small gap (<5%) or very small affected population

**Data Limitations:**
- Limited demographic segmentation (age/grade available, but not socioeconomic)
- No school-level data (only aggregate national data)
- Cannot differentiate urban/rural gaps (aggregate data only)
- Document limitations clearly for stakeholder expectations

**Intervention Implications:**
- Coverage gaps inform targeted outreach program design
- Priority populations guide resource allocation decisions
- Equity gaps highlight specific populations requiring tailored approaches
- Temporal persistence analysis shows urgency of intervention

**Related Stories:**
- Depends on Story 2 (Clean Data) and Story 3 (EDA Findings)
- Informs Story 5 (Dashboard) with gap metrics and priority populations
- Directly feeds Story 6 (Recommendations) with actionable gap closure strategies

**Stakeholder Value:**
- Enables evidence-based targeting of program improvement efforts
- Quantifies scope of coverage improvement needed
- Identifies specific populations requiring intervention
- Supports budget justification for program expansion

---

**Story Version**: 1.0  
**Created**: February 23, 2026  
**Status**: Ready for Sprint Planning
