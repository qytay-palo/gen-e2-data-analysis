# Problem Statement PS-001: Healthcare Workforce-Capacity Mismatch Analysis

## Problem Statement Metadata

```yaml
problem_statement_id: PS-001
title: Healthcare Workforce-Capacity Mismatch Analysis
analysis_category: Diagnostic & Descriptive Analytics
dependencies: None
status: Ready for Backlog Refinement
estimated_duration: 4-6 sprints
complexity: Medium
priority: CRITICAL
```

---

## Executive Summary

Currently, **MOH lacks comprehensive visibility into structural alignment between healthcare workforce supply and facility capacity**, which prevents optimal resource allocation and contributes to inefficiencies in care delivery. By systematically analyzing workforce trends (doctors, nurses, pharmacists) against facility capacity and bed availability across sectors (public, private, not-for-profit), **we can identify critical workforce-capacity mismatches and enable evidence-based workforce planning decisions** that improve operational efficiency and ensure sustainable healthcare delivery.

---

## Problem Statement Hypothesis

> We believe that analyzing workforce-to-capacity ratios across healthcare sectors and facilities will reveal structural imbalances that drive inefficiencies. We'll know we're successful when MOH leadership can articulate specific workforce-capacity gaps by sector and facility type, and can prioritize workforce planning investments based on quantified need.

---

## Objectives

1. **Establish Workforce-Capacity Baseline**: Calculate workforce-to-bed ratios, staffing density metrics, and capacity utilization benchmarks across all sectors (2006-2019)

2. **Identify Sectoral Misalignments**: Quantify workforce and capacity growth rates by sector to reveal which sectors are over/under-resourced relative to demand

3. **Detect Emerging Trends**: Track workforce composition changes (e.g., doctor vs. nurse ratios) to identify structural shifts and planning needs

4. **Enable Comparative Analysis**: Provide context by benchmarking Singapore's workforce-to-capacity ratios against international standards where available

---

## Stakeholders and Value Proposition

**Primary Stakeholders**:
- **Ministry of Health Policy Makers** - Develop long-term workforce planning strategies and sector-specific investment priorities
- **Healthcare System Administrators** - Optimize staffing decisions and facility resource allocation
- **Hospital/Facility Directors** - Manage within-sector workforce planning and capacity management
- **Human Resource/Workforce Planning Team** - Target recruitment and retention efforts based on evidence-based gap analysis

**Business Value**:
- **Decision Enabled**: Workforce planning investments prioritized by evidence of workforce-capacity gaps
- **Efficiency Gain**: Optimize staffing deployment across sectors, reducing idle capacity and staffing shortages
- **Quality Improvement**: Appropriate staffing levels support better patient outcomes and staff satisfaction
- **Risk Reduction**: Proactive workforce planning prevents future capacity constraints and service disruptions

---

## Data Requirements (High-Level)

**Data Domains Available** ✅:
- Healthcare Workforce datasets (doctors, nurses, pharmacists by sector, 2006-2019)
- Healthcare Facilities datasets (hospital beds, primary care facilities by type/sector)

**Data Completeness Assessment**:
- ✅ Workforce data: Complete by role and sector (2006-2019)
- ✅ Capacity data: Hospital beds documented by facility type and sector
- ⚠️ **Data Gap**: Primary care capacity (clinic visits, appointment slots) not available at detailed level
- ⚠️ **Data Gap**: No facility-level breakdown - only sector-level aggregates

**Data Quality Considerations**:
- ✅ 100% data completeness (no missing values)
- ✅ Official government source with high accuracy
- ⚠️ Annual granularity only (not monthly/quarterly for detecting short-term fluctuations)

---

## Initial Considerations

**Analytical Approach**:
- **Exploratory Analysis**: Workforce and capacity trend visualizations by sector and role
- **Descriptive Statistics**: Workforce-to-bed ratios, staffing density metrics, growth rate comparisons
- **Comparative Analysis**: Cross-sector benchmarking and ratio analysis
- **Time Series Analysis**: Multi-year trend detection to identify growth patterns and inflection points

**Platform Feasibility** (per [tech_stack.md](../../../docs/project_context/tech-stack.md)):
- **Primary Platform**: Local Python environment (data volume small, <4MB)
- **Language**: Python (using Polars for data processing)
- **Compute**: Local compute sufficient (no distributed processing needed)
- **Data Access**: File-based (CSV from Kaggle dataset)
- **Tools Available**: Python 3.9+, Polars, matplotlib/seaborn for visualization

**Technical Feasibility Check** ✅:
- ✅ All required data documented in data_sources.md
- ✅ Current tech stack supports Python-based time series and ratio analysis
- ✅ Data volume and complexity suitable for local processing
- ✅ No specialized tools required beyond standard analytics stack

---

## Expected Outcomes and Deliverables

**Stakeholder Outcomes**:
1. **Quantified Workforce-Capacity Gaps** - Clear evidence of workforce-to-bed misalignments by sector for decision-making
2. **Sector-Specific Insights** - Understanding of which sectors are under-resourced and need prioritized workforce investment
3. **Strategic Planning Data** - Historical workforce and capacity trends to inform 5-10 year workforce planning strategies

**Concrete Deliverables**:

📊 **Analytical Report** (Primary):
- Executive summary with key findings and recommendations
- Workforce and capacity trend visualizations (2006-2019)
- Workforce-to-bed ratio analysis by sector
- Sectoral growth rate comparisons
- Identification of workforce-capacity misalignments with quantified impact
- Sector-specific recommendations for workforce planning

📈 **Interactive Dashboard** (Optional, Secondary):
- Workforce-to-capacity ratio trends by sector
- Comparative metrics across sectors
- Filtering by role (doctors/nurses/pharmacists) and sector
- Year-over-year growth rate tracking

📋 **Curated Dataset** (Reference):
- Standardized, cleaned workforce and facility datasets (available for downstream analysis)
- Derived metrics (ratios, growth rates, density measures) for policy/planning use

---

## Dependencies and Assumptions

**Problem Statement Dependencies**:
- Depends on: None
- Blocks: PS-002 (Disease Priority Ranking) may benefit from workforce-capacity context
- Related to: PS-004 (Long-term Healthcare Sustainability) for workforce planning trends

**Key Assumptions**:
- ✅ Workforce-to-bed ratio is a valid proxy for workforce-capacity alignment
- ✅ Historical workforce and capacity data are accurate and representative
- ✅ Sector-level comparisons are meaningful for policy decisions (not overly simplified)

---

## Risks and Open Questions

**Potential Blockers**:
- **Risk**: Limited facility-level detail - analysis constrained to sector-level aggregates
  - *Mitigation*: Clarify analysis scope with stakeholders; sector-level insights still valuable for strategic planning
- **Risk**: Data lag - most recent data from 2019
  - *Mitigation*: Identify available updated data sources during Sprint 1; use 2019 as baseline for future planning
- **Risk**: No primary care visit/appointment data - cannot assess clinic capacity
  - *Mitigation*: Focus analysis on acute care capacity; scope primary care separately if needed

**Open Questions for Stakeholder Refinement**:
- Which international benchmarks (workforce-to-bed ratios) would be most useful for comparison?
- Are there sector-specific workforce planning priorities that should be highlighted?
- What timeframe should workforce planning recommendations cover (3, 5, 10 years)?

---

## Problem Statement Readiness

**Readiness Checklist**:
- [x] Data domains explicitly verified against data_sources.md
- [x] Platform and technical feasibility confirmed (tech_stack.md reviewed)
- [x] Problem statement decomposable into user stories (5-8 stories anticipated)
- [x] Deliverable format and access method defined
- [x] Stakeholders identified and value proposition clear

**Status**: ✅ **READY FOR BACKLOG REFINEMENT**

This problem statement is ready for detailed user story development and sprint planning.

---

## Related Documentation

- **Data Sources**: [data_sources.md](../../../docs/project_context/data-sources.md)
- **Tech Stack**: [tech_stack.md](../../../docs/project_context/tech-stack.md)
- **Business Objectives**: [business-objectives.md](../../../docs/project_context/business-objectives.md)
- **Data Dictionary**: [disease_data.md](../../../docs/data_dictionary/)

---

**Document Version**: 1.0  
**Status**: Ready for Backlog Refinement  
**Last Updated**: February 23, 2026
