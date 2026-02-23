# Domain Knowledge: Public Health Programs and Vaccination Strategies

## Overview

Public health prevention programs, including vaccination initiatives and school health screenings, are population-level interventions designed to prevent disease and promote health. This domain covers program coverage assessment, effectiveness evaluation, and implementation strategies. Understanding public health program metrics and evaluation methodologies is essential for analyzing vaccination and school health program effectiveness.

## Related Problem Statements

- [PS-003: Public Health Program Effectiveness & Coverage Analysis](../../objectives/problem_statements/ps-003-public-health-effectiveness.md)
- [PS-002: Healthcare Burden & Disease Priority Ranking](../../objectives/problem_statements/ps-002-disease-burden-prioritization.md)

## Related Stakeholders

- **School Health Program Leaders**: Monitor program coverage and performance, identify improvement opportunities
- **MOH Disease Prevention Teams**: Assess vaccination coverage adequacy, identify at-risk populations
- **Education Ministry Partners**: Understand school program effectiveness, plan school-based interventions
- **Population Health Planning Teams**: Monitor progress toward public health prevention goals

## Key Concepts and Terminology

### Vaccination Coverage

**Definition**: Proportion of target population that has received recommended vaccines

**Standard Coverage Targets**:
- Single-dose vaccines: 90%+ population coverage
- Multi-dose vaccine series: 80%+ completion (final dose)
- Different targets for different age groups and vaccines

**Relevance**: Vaccination coverage determines population immunity levels; 85-95% coverage needed for herd immunity for most vaccines

**Types of Coverage Metrics**:
- **Immunization Coverage**: Proportion of children receiving vaccine (by age cohort)
- **Series Completion**: Percentage completing full multi-dose series (e.g., 3-dose vaccines)
- **Timeliness**: Percentage receiving vaccine on schedule vs. delayed
- **Equity Coverage**: Coverage by demographic group (detecting disparities)

**Example**: 
- DPT vaccine coverage 92% nationally, but only 78% in rural areas
- Indicates access disparity requiring targeted outreach in underserved regions

---

### Vaccine-Preventable Disease Burden

**Definition**: Disease burden (cases, deaths, hospitalizations) in diseases for which effective vaccines exist

**Relevance**: Gap between current and preventable burden shows potential impact of improving vaccination coverage

**Calculation**:
- Preventable Disease Burden = Current Burden - Burden at target coverage level
- Based on vaccine effectiveness data and epidemiological models

**Example**: 
- Current measles incidence: 5 cases per 100,000
- Achievable incidence at 95% coverage: <1 case per 100,000
- Preventable burden: 4 cases per 100,000 (represents lives that could be saved)

---

### School Health Program Effectiveness

**Definition**: Degree to which school-based health programs achieve intended health outcomes

**Key Indicators**:
- **Coverage**: Proportion of students participating in program
- **Participation**: Attendance rates and completion of screening/intervention
- **Health Outcomes**: Pre/post changes in health indicators (e.g., obesity prevalence, dental health)
- **Equity**: Program reach across different demographic groups

**Relevance**: Schools are ideal setting for population-based health interventions; reach 100% of age cohorts

**Program Types**:
- Health Screening Programs: Regular health assessments (dental, vision, physical development)
- Vaccination Programs: School-based immunization delivery
- Health Education: Curriculum-based health promotion
- Nutrition Programs: Meal programs, nutrition education

---

### Coverage Gap Analysis

**Definition**: Identifying populations not reached by public health programs

**Types of Gaps**:
- **Geographic Gaps**: Urban vs. rural, regional differences in coverage
- **Demographic Gaps**: Age, gender, socioeconomic status disparities
- **Systemic Gaps**: Underserved populations due to access barriers
- **Temporal Gaps**: Timing mismatches (e.g., programs at wrong school term)

**Relevance**: Targeting coverage improvement efforts to populations with highest gaps maximizes impact

**Example**:
- Urban coverage 95%, rural coverage 70% → Focus outreach on rural areas
- Low-income schools 65% coverage, high-income 90% → Address equity barrier (access, cost, awareness)

---

## Standard Metrics and KPIs

| Metric | Definition | Calculation | Target Range | Use Case | Data Requirements |
|--------|-----------|-------------|---------------|----------|-------------------|
| **Immunization Coverage Rate** | % of target population receiving vaccine | (Vaccinated / Target Population) × 100 | 85-95%+ | Monitor vaccination program effectiveness | Vaccine doses given, target population |
| **Series Completion Rate** | % completing multi-dose vaccine series | (Completed Series / Target Population) × 100 | 80%+ | Assess full immunization program success | Dose tracking by individual |
| **Coverage Equity Gap** | Difference in coverage between demographic groups | (Higher Coverage % - Lower Coverage %) | <5% gap | Identify disparities requiring targeted effort | Coverage by demographic group |
| **Vaccination Timeliness** | % receiving vaccine on recommended schedule | (On-time / Total Vaccinated) × 100 | >80% | Assess program implementation quality | Vaccine dates, recommended schedules |
| **School Screening Participation** | % of students participating in health screening | (Screened / Enrolled) × 100 | >90% | Monitor school health program reach | Screening participation data |
| **Preventable Disease Incidence** | Disease incidence in vaccine-preventable diseases | Cases of disease per 100,000 population | <1-10 per 100,000 (varies) | Assess population impact of vaccination programs | Disease surveillance data |
| **Screening Positive Rate** | % of screened individuals identified with health issue | (Positive Cases / Screened) × 100 | 5-20% (varies by condition) | Assess prevalence of screened conditions | Screening test results |

---

## Feature Engineering Guidance

### Common Public Health Program Analytics Features

#### Coverage Features

- **Coverage Rate by Cohort**: Vaccination coverage for specific age/school cohort
  - **Calculation**: `(Vaccinated in Cohort / Total in Cohort) × 100`
  - **Use Cases**: Track coverage progress by age group
  - **Interpretation**: >90% = adequate; 80-90% = acceptable with improvement needed; <80% = concerning

- **Coverage Trends**: Year-over-year coverage change
  - **Calculation**: `(Current Year Coverage - Previous Year Coverage)`
  - **Use Cases**: Identify improving vs. declining program performance
  - **Example**: Coverage increased 5 percentage points year-over-year indicates program expansion

- **Coverage Equity Index**: Ratio of coverage in lowest vs. highest coverage groups
  - **Calculation**: `(Min Coverage / Max Coverage) × 100`
  - **Use Cases**: Quantify disparities (target should be >90% for equity)
  - **Example**: Rural/Urban ratio of 85/95 = 89% equity index (11% disparity)

#### Outcome Features

- **Disease Incidence in Vaccinated vs. Unvaccinated**:
  - Compare disease rates between vaccinated and unvaccinated populations
  - **Use Cases**: Estimate vaccine effectiveness in real-world setting
  - **Interpretation**: Large difference validates vaccine program value

- **Screening Sensitivity and Specificity**:
  - Proportion of true cases identified (sensitivity) and false positives avoided (specificity)
  - **Use Cases**: Assess screening program quality and predictive value
  - **Interpretation**: Sensitivity >90% = good detection; specificity >95% = good positive predictive value

- **Health Outcome Improvement Index**:
  - Change in health indicator from screening period
  - **Calculation**: `((Baseline Value - Endpoint Value) / Baseline Value) × 100`
  - **Use Cases**: Assess whether school health program improves health
  - **Example**: "Obesity prevalence reduced 15% over 3 years" (screens and lifestyle intervention)

#### Demographic Stratification Features

- **Coverage by Demographic Group**:
  - Calculate coverage separately for each demographic (age, school, socioeconomic status)
  - **Use Cases**: Identify high-risk, underserved populations
  - **Interpretation**: Variations >10% warrant investigation and targeted improvement

- **Disparity Magnitude Measures**:
  - Absolute difference, relative difference, and disparity ratios across groups
  - **Use Cases**: Quantify equity gaps precisely for reporting
  - **Example**: "Rural coverage 20 percentage points lower than urban" (absolute gap) or "70% of urban coverage" (relative gap)

---

### Domain-Specific Patterns

#### Coverage Equity Disparity Pattern
**When to Apply**: When analyzing whether programs reach all populations equitably  
**Implementation**:
1. Calculate coverage by demographic groups (geographic, socioeconomic, ethnic)
2. Identify groups with lowest coverage
3. Investigate barriers (access, awareness, cost, language, trust)
4. Design targeted interventions

**Example**: 
- Vaccination coverage 95% in urban, 70% in rural areas
- Investigation reveals: limited clinic hours/locations in rural, transportation barriers, vaccine hesitancy
- **Interventions**: Mobile clinic schedule, community health worker outreach, vaccine confidence building

#### Program Expansion Success Pattern
**When to Apply**: When assessing whether program expansion reaches additional populations  
**Implementation**:
1. Compare coverage pre/post program expansion
2. Analyze coverage change in target vs. non-target populations
3. Assess time lag between expansion and coverage change (usually 1-2 year lag)

**Example**:
- School-based vaccination launched 2020
- Coverage increased 25 percentage points by 2022
- Largest gains in previously underserved schools
- **Interpretation**: Program successfully reaching intended populations; scale further

---

## Data Quality Considerations

### Coverage Reporting Inconsistencies
- **Description**: Different data sources may calculate coverage differently (denominator = age cohort vs. enrolled students vs. visited schools)
- **Impact**: Coverage estimates may not be directly comparable across years or regions
- **Detection**: Check data source documentation for coverage calculation methodology
- **Mitigation**: Standardize denominator definition; note if changes over time

### Incomplete Screening Data
- **Description**: Not all students may participate in health screening; non-participants not followed up
- **Impact**: Screening outcomes may be biased toward healthier students who participate
- **Detection**: Compare participation rates; investigate non-participants
- **Mitigation**: Document participation rates clearly; note bias limitations in analysis

### School Administrative Delays
- **Description**: Vaccine and screening data may be delayed in reporting (months of lag)
- **Impact**: Most recent coverage data may be 2-3 months old, limiting timeliness
- **Detection**: Check data reporting dates; identify lag patterns
- **Mitigation**: Note data lag clearly; plan analysis with expectation of administrative delay

### Health Outcome Attribution Challenges
- **Description**: School health screening improvements may not be solely due to intervention (confounders: family awareness, healthcare access, socioeconomic changes)
- **Impact**: Cannot isolate program effect from other factors
- **Detection**: Compare intervention vs. control groups if available
- **Mitigation**: Use quasi-experimental design (interrupted time series) or document confounders

---

## Analytical Methodologies

### Coverage Analysis
- **Application**: Assess whether programs reach target populations
- **Assumptions**: Coverage rates accurately reflect population reach; target denominator properly defined
- **Implementation Notes**: Calculate by program, cohort, and demographic; establish baseline and targets
- **Interpretation**: Gaps <5% acceptable; >10% gaps require investigation and improvement efforts

### Trend Analysis
- **Application**: Identify coverage increasing, stable, or declining over time
- **Assumptions**: Historical trends predictive of future; sustained effort required to maintain coverage
- **Implementation Notes**: Use 3+ years of data; apply smoothing if volatile
- **Interpretation**: Rising coverage indicates program growth; plateaus suggest capacity limits or saturation

### Equity Analysis
- **Application**: Quantify disparities and identify populations needing targeted outreach
- **Assumptions**: Coverage variations reflect access barriers, not population preference differences
- **Implementation Notes**: Stratify by multiple demographic dimensions; calculate multiple equity measures
- **Interpretation**: Equity gaps highlight where resources should be focused

### Outcome Evaluation
- **Application**: Assess health impact of programs (does vaccination prevent disease? Does screening improve health?)
- **Assumptions**: Outcome changes attributable to program; sufficient time for outcomes to manifest
- **Implementation Notes**: Use comparison populations if possible; account for secular trends
- **Interpretation**: Large outcome differences validate program investment

---

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- **Confusing Coverage with Impact**: High coverage doesn't guarantee outcome improvement (depends on vaccine effectiveness, screening quality)
- **Ignoring Participation Bias**: Non-participants in screening may differ systematically from participants
- **False Equity Claims**: Averaging coverage across diverse populations can mask large disparities
- **Short-Term Evaluation**: Health outcomes take time to manifest; 1-year evaluation insufficient
- **Missing Adverse Events**: Focusing on coverage/outcomes while ignoring safety signals or adverse events

### Best Practices
- **Set and Monitor Equity Targets**: Don't just track average coverage; ensure all populations reached
- **Combine Multiple Metrics**: Coverage alone insufficient; track outcomes, adverse events, and equity simultaneously
- **Use Mixed Methods**: Combine quantitative coverage data with qualitative investigation of barriers
- **Engage Communities**: Program improvements informed by local insights about barriers and solutions
- **Establish Feedback Loops**: Share findings with programs promptly; enable rapid improvement cycles
- **Benchmark Internationally**: Compare Singapore coverage to peer countries; identify gaps and opportunities

---

## References and Sources

### Authoritative Sources
- **MOH Singapore Immunization Program**: MOH publishes annual vaccination coverage and program reports
- **WHO Immunization Coverage Monitoring**: https://www.who.int/teams/immunization-vaccines-and-biologicals - Global coverage tracking and standards
- **Singapore School Health Program**: MOH school health and dental program guidelines and annual reports

### Industry Standards
- **Herd Immunity Thresholds**: Varies by disease (measles 95%, polio 85-95%, COVID-19 70-90%)
- **AAPOR Vaccination Monitoring**: Standards for coverage survey methodology and reporting
- **School Health Screening Standards**: WHO and national guidelines for school-based health assessments

---

## Cross-References

### Related Domain Knowledge Files
- [Disease Burden and Mortality Analysis](disease-burden-mortality-analysis.md) - Understanding vaccine-preventable disease burden
- [Healthcare System Sustainability Metrics](healthcare-system-sustainability-metrics.md) - Prevention program impact on system sustainability

### Related Data Dictionary Entries
- [School Health and Vaccination Data](../../data_dictionary/disease_data.md) - Field definitions for program data

---

## Metadata

**Created**: February 23, 2026  
**Last Updated**: February 23, 2026  
**Version**: 1.0  
**Status**: Initial Creation

## Notes

This domain knowledge file supports public health program evaluation. Key areas for future expansion:
- Vaccine confidence and hesitancy measurement and mitigation
- Cost-effectiveness analysis of public health programs
- Implementation science for improving program delivery
- Equity barriers and solutions for improving coverage in vulnerable populations
