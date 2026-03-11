# Problem Statement Portfolio - Gen-E2 Singapore Health Trends Analysis

**Project**: Gen-E2 Data Analysis Project - Singapore Health Trends Analysis  
**Organization**: Ministry of Health (MOH), Singapore  
**Portfolio Owner**: Data Analysis Team  
**Last Updated**: 2026-03-11  
**Status**: Portfolio Defined - Awaiting Stakeholder Approval

---

## 📋 Portfolio Overview

This portfolio contains **5 analytics problem statements** identified through systematic analysis of MOH strategic goals, available data sources, and stakeholder needs. Each problem statement has been validated for **data availability** and **platform feasibility**, ensuring all analyses can be executed with available resources.

**Portfolio Coverage**:
- **Predictive Analytics**: 1 problem statement (forecasting future trends)
- **Descriptive Analytics**: 1 problem statement (characterizing historical patterns)
- **Prescriptive Analytics**: 1 problem statement (optimization and decision support)
- **Diagnostic Analytics**: 2 problem statements (root cause analysis and disparity assessment)

**Prioritization Status**: ✅ Complete - See [PRIORITIZATION.md](PRIORITIZATION.md) for detailed scoring and execution roadmap

---

## 🎯 Problem Statement Inventory

### P0 (Critical Priority) - Immediate Start Recommended

#### [PS-001: Healthcare Workforce Sustainability Analysis](ps-001-healthcare-workforce-sustainability.md)
- **Category**: Predictive Analytics
- **Priority**: P0 (Score: 4.4/5.0)
- **Estimated Duration**: 5-7 sprints
- **Platform**: HEALIX/Databricks - Python (Polars)
- **Status**: ✅ Ready for Backlog

**Problem**: MOH lacks 10-year healthcare workforce projections across specialties, preventing proactive recruitment and training pipeline planning in face of aging population and workforce attrition.

**Objective**: Forecast healthcare workforce supply and demand through 2030 using 13 years of historical data (2006-2019) to identify specialty-specific shortages and enable evidence-based workforce planning.

**Data Verified**: 7 workforce tables covering doctors, nurses, pharmacists, dentists (2006-2019) - ✅ Confirmed available

**Deliverables**: 
- Workforce projection report with 10-year forecasts by specialty
- Interactive workforce planning dashboard
- Projection dataset with confidence intervals
- Policy recommendations for workforce sustainability

**Why P0**: Workforce shortages are current pain point with 5-10 year lead time for training pipelines; highest urgency score (4/5).

**Start Date**: Recommended Sprint 1 (Immediate)

---

#### [PS-004: Healthcare Expenditure Drivers & Cost Control Analysis](ps-004-healthcare-expenditure-drivers.md)
- **Category**: Diagnostic Analytics
- **Priority**: P0 (Score: 4.4/5.0)
- **Estimated Duration**: 4-6 sprints
- **Platform**: HEALIX/Databricks - Python (Polars)
- **Status**: ✅ Ready for Backlog

**Problem**: Limited understanding of what drives healthcare expenditure growth (population aging vs service intensity vs disease burden) prevents targeted cost containment strategies and leads to broad budget cuts that may harm care quality.

**Objective**: Decompose 15 years of healthcare expenditure growth (2005-2020) into demographic, volume, and price components to identify primary cost drivers and cost control opportunities.

**Data Verified**: National health expenditure tables, financing scheme breakdowns, utilization data (2005-2020) - ✅ Confirmed available

**Deliverables**:
- Expenditure diagnostic report with growth decomposition analysis
- Healthcare expenditure explorer dashboard
- Integrated expenditure-utilization dataset
- Cost containment policy brief with savings estimates

**Why P0**: Financial sustainability is existential concern for healthcare system; aligns with annual budget cycles; Finance Ministry priority (urgency 4/5).

**Start Date**: Recommended Sprint 1 (Immediate - can run parallel with PS-001)

---

#### [PS-002: Disease Burden Temporal Trends Analysis](ps-002-disease-burden-temporal-trends.md)
- **Category**: Descriptive Analytics
- **Priority**: P0 (Score: 4.0/5.0)
- **Estimated Duration**: 3-5 sprints
- **Platform**: HEALIX/Databricks - Python (Polars)
- **Status**: ✅ Ready for Backlog

**Problem**: Public health program planners lack comprehensive understanding of long-term disease burden evolution, making it difficult to justify resource allocation and prioritize disease control initiatives.

**Objective**: Analyze 30 years of mortality trends (1990-2019) for major diseases (cancer, stroke, heart disease) to identify emerging priorities and quantify disease burden changes over time.

**Data Verified**: 3 age-standardized mortality rate tables covering cancer, stroke, heart disease (1990-2019) - ✅ Confirmed available

**Deliverables**:
- Disease burden trend report with 30-year analysis
- Interactive disease burden explorer dashboard
- Consolidated mortality dataset with trend indicators
- Public health prioritization policy brief

**Why P0**: Foundation for public health strategy and resource allocation; excellent feasibility (5/5 - perfect data, low complexity) enables quick completion.

**Start Date**: Recommended Sprint 2 (after PS-001/PS-004 initiated if resource-constrained)

---

### P1 (High Priority) - Near-Term Start (3-6 Months)

#### [PS-003: Healthcare Capacity & Utilization Optimization](ps-003-healthcare-capacity-optimization.md)
- **Category**: Prescriptive Analytics
- **Priority**: P1 (Score: 3.8/5.0)
- **Estimated Duration**: 5-7 sprints
- **Platform**: HEALIX/Databricks - Python (Polars)
- **Status**: ✅ Ready for Backlog

**Problem**: Uncertainty about optimal capacity allocation across facility types (acute, intermediate, primary care) prevents efficient resource deployment and leads to potential over-capacity in some areas while bottlenecks exist in others.

**Objective**: Analyze 11-year facility capacity and utilization trends (2009-2020) to identify capacity gaps, utilization imbalances, and recommend optimization strategies for infrastructure investment.

**Data Verified**: Facility capacity tables, hospital admission rates, long-term care data (2006-2020) - ✅ Confirmed available (with proxy occupancy rate limitation)

**Deliverables**:
- Capacity optimization study report with gap analysis
- Healthcare capacity planning dashboard with scenario modeling
- Capacity-utilization metrics dataset
- Infrastructure investment prioritization brief

**Why P1**: Highest business value (5/5 - multi-billion dollar investment decisions) but lower urgency (3/5 - long planning cycles) and moderate feasibility (3/5 - requires proxy metrics and optimization expertise).

**Start Date**: Recommended Sprint 4-5 (after P0 analyses underway)

**Dependencies**: May benefit from PS-001 findings (workforce constraints affect capacity) but not blocking

---

### P2 (Medium Priority) - Planned Start (6-12 Months)

#### [PS-005: Healthcare Access Equity & Demographic Disparities Analysis](ps-005-healthcare-equity-disparities.md)
- **Category**: Diagnostic Analytics (Equity Focus)
- **Priority**: P2 (Score: 2.4/5.0)
- **Estimated Duration**: 4-5 sprints
- **Platform**: HEALIX/Databricks - Python (Polars)
- **Status**: ✅ Ready for Backlog (with data limitations noted)

**Problem**: Limited visibility into healthcare access and health outcome disparities across demographic groups prevents targeted interventions to reduce health inequity and leads to one-size-fits-all policies.

**Objective**: Analyze 15+ years of utilization and health outcome data stratified by demographics (2005-2020) to identify underserved populations and quantify health outcome gaps.

**Data Verified**: Age/gender-stratified utilization and mortality data (2005-2020) - ⚠️ PARTIAL - Socioeconomic and ethnic stratification likely limited/absent

**Deliverables**:
- Healthcare equity assessment report with disparity quantification
- Health equity monitor dashboard
- Healthcare equity metrics dataset
- Health equity action plan with targeted interventions

**Why P2**: Important for social mission but constrained by data limitations (feasibility 2/5 - missing critical socioeconomic/ethnic variables) and lower urgency (2/5 - no pressing deadlines).

**Start Date**: Recommended Sprint 9-12 (after P0/P1 completion)

**Enhancement Opportunity**: **Engage MOH to obtain ethnicity and socioeconomic data before starting** - would significantly increase feasibility (2/5 → 4/5) and potentially elevate to P1 priority

---

## 📊 Portfolio Statistics

**Total Problem Statements**: 5  
**Priority Distribution**:
- P0 (Critical): 3 problem statements (60%)
- P1 (High): 1 problem statement (20%)
- P2 (Medium): 1 problem statement (20%)
- P3 (Low): 0 problem statements (0%)

**Analytical Category Distribution**:
- Predictive Analytics: 1 (20%)
- Descriptive Analytics: 1 (20%)
- Prescriptive Analytics: 1 (20%)
- Diagnostic Analytics: 2 (40%)

**Data Validation Status**: ✅ 100% (5/5) problem statements have explicit data verification against data-sources.md

**Platform Feasibility**: ✅ 100% (5/5) problem statements confirmed feasible on HEALIX/Databricks Python environment

**Estimated Total Effort**: 21-30 sprints (if executed sequentially)  
**Potential Parallel Execution**: Reduce to ~12-15 sprints with 3 analysts working in parallel

---

## 🚀 Execution Roadmap

### Phase 1: Critical Foundations (Sprint 1-5)
**Focus**: Establish baseline understanding of workforce, costs, and disease burden

**Active Problem Statements**:
- **PS-001** (Workforce) - Start Sprint 1
- **PS-004** (Expenditure) - Start Sprint 1 (parallel)
- **PS-002** (Disease Burden) - Start Sprint 2

**Resource Requirements**: 2-3 analysts (forecasting, financial, public health expertise)

**Expected Outcomes**: 
- 10-year workforce projections by specialty
- Expenditure growth decomposition and cost drivers identified
- 30-year disease burden trends quantified

**Strategic Value**: Addresses immediate stakeholder needs (workforce planning, cost control, public health prioritization)

---

### Phase 2: Strategic Optimization (Sprint 6-10)
**Focus**: Infrastructure investment optimization and resource allocation

**Active Problem Statements**:
- **PS-003** (Capacity Optimization) - Start Sprint 4-5
- Continue/complete Phase 1 analyses as needed

**Resource Requirements**: 1-2 analysts (operations research, optimization expertise)

**Expected Outcomes**:
- Capacity gap analysis with investment priorities
- Scenario models for infrastructure expansion options
- Evidence base for multi-billion dollar investment decisions

**Strategic Value**: Optimize capital deployment; prevent wasteful over-capacity or crisis from under-capacity

---

### Phase 3: Equity & Refinement (Sprint 11-15)
**Focus**: Health equity assessment and portfolio refinement

**Active Problem Statements**:
- **PS-005** (Health Equity) - Start Sprint 9-12 (after data enhancement if possible)

**Resource Requirements**: 1 analyst (equity analysis expertise)

**Expected Outcomes**:
- Demographic disparity quantification
- Vulnerable population identification
- Targeted equity intervention roadmap

**Strategic Value**: Fulfill social mission; address accessibility goals; targeted subsidy and outreach programs

**Prerequisite**: Ideally obtain enhanced demographic data (ethnicity, socioeconomic variables) before starting

---

## 📖 Related Documentation

**Problem Identification Process**:
- [Problem Identification Workflow](../../../.github/instructions/1-identify-problem-statement.prompt.md) - Methodology used to generate this portfolio
- [PRIORITIZATION.md](PRIORITIZATION.md) - Detailed scoring rationale and prioritization framework

**Project Context** (Foundation for Problem Statements):
- [Business Objectives](../../project_context/business-objectives.md) - MOH strategic goals and stakeholder needs
- [Data Sources](../../project_context/data-sources.md) - Available datasets and data quality assessment
- [Tech Stack](../../project_context/tech-stack.md) - Platform and tool capabilities

**Data Foundation**:
- [Data Dictionary Index](../../data_dictionary/index.md) - Variable definitions and data standards
- [Data Quality Standards](../../data_dictionary/index.md#data-quality-metrics) - Completeness, accuracy, timeliness metrics

**Project Planning**:
- [TODO.md](../../../TODO.md) - Comprehensive task breakdown across all domains
- [Project Phases](../../index.md#project-phases) - 8-phase data analysis lifecycle

---

## 🔄 Portfolio Lifecycle Management

**Review Frequency**: Quarterly  
**Next Review**: 2026-06-11

**Review Criteria**:
1. **Relevance**: Do problem statements still align with MOH strategic priorities?
2. **Dependencies**: Have new dependencies emerged? Are dependencies resolved?
3. **Data Availability**: Has new data become available that enables new analyses or enhances existing ones?
4. **Stakeholder Priorities**: Have stakeholder needs shifted?
5. **Completion Status**: Which problem statements are complete? What insights were gained?

**Portfolio Evolution**:
- **Add**: New problem statements may be added as new data sources or stakeholder needs emerge
- **Update**: Existing problem statements may be refined based on stakeholder feedback or data discoveries
- **Sunset**: Completed problem statements move to "Completed Archive" section
- **Reprioritize**: Priorities may shift based on changing MOH strategic focus

**Change Management**:
- All changes to problem statement portfolio require stakeholder review
- Priority changes impacting resource allocation require MOH approval
- New problem statements follow the same validation process (data verification, platform feasibility)

---

## 📞 Stakeholder Contacts

**Primary Stakeholders**:
- **MOH Healthcare Planning Division** - Workforce and capacity planning
- **MOH Finance Division** - Healthcare expenditure and budget management
- **MOH Population Health Strategy Division** - Public health and equity initiatives
- **Ministry of Finance (Budget Office)** - National healthcare budget allocation

**Problem Statement Ownership**:
- Ownership will be assigned during sprint planning
- Each problem statement will have a lead analyst and stakeholder sponsor

**Feedback & Questions**:
- Contact: [Data Analysis Team - TBD]
- Process: Review meetings scheduled at end of each sprint
- Escalation: MOH Senior Leadership for priority conflicts or resource constraints

---

## ✅ Portfolio Readiness Checklist

**Problem Statement Quality**:
- [x] All problem statements follow standardized template
- [x] All problem statements have explicit data verification (referenced data-sources.md)
- [x] All problem statements have platform feasibility confirmation (referenced tech-stack.md)
- [x] All problem statements have defined deliverables and stakeholder value
- [x] All problem statements are decomposable into user stories (8-9 stories per problem statement)

**Prioritization Completeness**:
- [x] All problem statements scored on Business Value / Feasibility / Urgency
- [x] Priority assignments (P0/P1/P2) clearly defined
- [x] Execution roadmap with phased approach created
- [x] Resource requirements identified

**Stakeholder Alignment**:
- [ ] Portfolio socialized with MOH stakeholders (PENDING)
- [ ] Priorities validated against stakeholder urgency (PENDING)
- [ ] Resource allocation approved (PENDING)
- [ ] Phase 1 start date confirmed (PENDING)

**Governance**:
- [x] Review frequency established (Quarterly)
- [x] Change management process defined
- [x] Portfolio lifecycle management documented

---

## 🎯 Success Criteria

**This problem statement portfolio will be considered successful when**:

1. **Stakeholder Adoption**: MOH teams reference problem statement analyses in policy decisions and budget proposals
2. **Decision Enabling**: At least 3 concrete policy changes or resource allocation decisions directly informed by analyses
3. **Analytical Coverage**: Portfolio provides insights across all 4 MOH strategic pillars (accessibility, population health, sustainability, evidence-based practice)
4. **Sustainability**: Problem statements transition to BAU (business-as-usual) monitoring and updating cycles
5. **Knowledge Building**: Portfolio serves as foundation for future analytical initiatives and capability building

**Measurement Approach**:
- Track policy citations and decision references in MOH documents
- Conduct stakeholder satisfaction surveys at end of each phase
- Document decision impact through case studies
- Monitor portfolio utilization metrics (dashboard usage, report downloads, dataset access)

---

**Status**: ✅ **Portfolio Defined - Ready for Stakeholder Review**

**Next Steps**:
1. Schedule stakeholder review meeting with MOH leadership
2. Present prioritization rationale and execution roadmap
3. Obtain approval for Phase 1 initiation (PS-001, PS-004, PS-002)
4. Assign problem statement ownership and allocate analysts
5. Initiate Sprint 1 planning for P0 problem statements

---

*This portfolio was generated through systematic analysis of MOH strategic objectives, comprehensive data source review, and platform capability assessment. All problem statements have been validated for data availability and technical feasibility to ensure successful execution.*
