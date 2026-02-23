# User Story 6: Multi-Dimensional Sustainability Assessment and Scenario Planning

**As a** MOH strategic planning leader,  
**I want** to conduct comprehensive multi-dimensional sustainability assessment with scenario-based planning,  
**so that** I can identify critical risks, evaluate strategic intervention options, and develop evidence-based recommendations for long-term healthcare system sustainability.

## 1. 🎯 Acceptance Criteria

- Multi-dimensional sustainability assessment completed across workforce, capacity, financial, utilization dimensions
- Critical sustainability risks identified, prioritized, and quantified by dimension and sector
- Scenario analysis completed: baseline, optimistic, pessimistic trajectories modeled
- Strategic intervention options evaluated: impact on sustainability metrics quantified
- Benchmarking analysis completed: Singapore compared to peer healthcare systems (if data available)
- Sector-specific sustainability strategies recommended based on identified risks
- Sensitivity analysis completed: key assumptions tested for robustness
- Comprehensive findings report created documenting risks, scenarios, and recommendations
- All analytical outputs saved to `results/` for stakeholder review and dashboard integration

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for multi-dimensional aggregations and scenario modeling
- **Statistical Analysis**: Use scipy/statsmodels for hypothesis testing and validation
- **Scenario Modeling**: Deterministic scenario projections with sensitivity analysis
- **Visualization**: Create decision-quality charts for strategic communication
- **Documentation**: Evidence-based recommendations with quantified impacts
- **Reproducibility**: All analytical decisions documented and scripted

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Full Framework](../../../domain_knowledge/healthcare-system-sustainability-metrics.md) - Sustainability assessment methodology
- [Healthcare System Sustainability Metrics: Vulnerability and Risk Features](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#vulnerability-and-risk-features) - Risk assessment approach
- [Healthcare Workforce Planning: Workforce-Capacity Misalignment Pattern](../../../domain_knowledge/healthcare-workforce-planning.md#domain-specific-patterns) - Intervention strategies
- [Disease Burden and Mortality Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md) - Health burden context for resource planning

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Multi-dimensional analysis and scenario modeling
- **numpy**: Numerical calculations
- **scipy**: Statistical testing and analysis
- **statsmodels**: Advanced statistical modeling
- **matplotlib/seaborn**: Strategic visualization

**Internal Dependencies:**
- Depends on: Story 5 (Sustainability Metrics Engineering) - sustainability metrics and projections
- Input from: 
  - `data/4_processed/sustainability_metrics_2006_2018.parquet`
  - `data/4_processed/sustainability_projections_2019_2030.parquet`
  - `results/tables/ps-004_exploratory_findings.md` (Story 4 insights)
- Feeds into: Story 7 (Dashboard & Reporting)

## 5. ✅ Implementation Tasks

### Dimension-Specific Sustainability Assessment

#### Workforce Sustainability Assessment
- ⬜ Assess current workforce adequacy (2018 baseline):
  - Workforce-to-population ratios vs. WHO/OECD benchmarks
  - Workforce-to-bed ratios vs. optimal ranges (1.5-2.5 FTE/bed)
  - Professional composition (doctor-to-nurse ratio) vs. best practices
- ⬜ Analyze workforce trends 2006-2018:
  - Growth trajectory: accelerating, stable, or declining?
  - Profession-specific trends: which categories lagging/leading?
  - Sector disparities: Public vs. Private workforce adequacy
- ⬜ Project workforce sustainability 2019-2030:
  - Baseline projection: workforce supply under current growth rates
  - Demand projection: workforce needed based on utilization trends
  - Gap quantification: shortfall by profession and sector
- ⬜ Identify workforce sustainability risks:
  - Which professions facing critical shortages?
  - Which sectors most vulnerable?
  - Timeline: when do shortages become critical?
- ⬜ Recommend workforce interventions:
  - Medical school intake adjustments
  - Recruitment targets by profession
  - Retention strategies to reduce attrition

#### Capacity Sustainability Assessment
- ⬜ Assess current capacity adequacy (2018 baseline):
  - Bed-to-population ratios vs. international benchmarks
  - Bed utilization rates vs. optimal range (70-85%)
  - Facility distribution: geographic and sector adequacy
- ⬜ Analyze capacity trends 2009-2018:
  - Expansion trajectory: steady vs. episodic growth?
  - Sector investment patterns: Public vs. Private expansion
  - Capacity-demand alignment: utilization trends vs. expansion
- ⬜ Project capacity sustainability 2019-2030:
  - Baseline projection: capacity under historical expansion rates
  - Demand projection: bed capacity needed based on admission trends
  - Gap quantification: bed deficit by sector
- ⬜ Identify capacity sustainability risks:
  - Projected overcrowding: when utilization exceeds 85%?
  - Sector-specific deficits: which sectors need expansion priority?
  - Infrastructure implications: new facility requirements
- ⬜ Recommend capacity interventions:
  - Facility expansion targets by sector
  - Bed addition requirements by timeline
  - Alternative care models (community care to reduce bed pressure)

#### Financial Sustainability Assessment
- ⬜ Assess current expenditure sustainability (2018 baseline):
  - Health expenditure as % of GDP vs. international benchmarks
  - Real expenditure growth rate vs. GDP growth rate
  - Expenditure per capita vs. peer nations
  - Out-of-pocket spending % vs. financial protection standards
- ⬜ Analyze expenditure trends 2006-2018:
  - Spending growth trajectory: accelerating or controlled?
  - Expenditure efficiency: spending growth vs. output growth (workforce, capacity)
  - Category-specific trends: which areas driving cost growth?
- ⬜ Project financial sustainability 2019-2030:
  - Baseline projection: expenditure under historical growth rates
  - Budget constraint: sustainable spending envelope (e.g., 5% of GDP ceiling)
  - Gap quantification: projected budget shortfall
- ⬜ Identify financial sustainability risks:
  - Unsustainable expenditure growth trajectory?
  - Budget deficit timeline: when does spending exceed ceiling?
  - Efficiency concerns: rising costs without proportional output?
- ⬜ Recommend financial interventions:
  - Cost control measures: efficiency improvements
  - Revenue strategies: funding model adjustments
  - Budget allocation priorities: high-impact investment areas

#### Utilization Sustainability Assessment
- ⬜ Assess current utilization patterns (2018 baseline):
  - Hospital admission rates vs. international benchmarks
  - Demographic utilization intensity: age/gender patterns
  - Service intensity: average length of stay trends
- ⬜ Analyze utilization trends 2006-2018:
  - Demand growth trajectory: accelerating vs. stable?
  - Demographic drivers: aging population impact quantified
  - Service mix shifts: admission type changes over time
- ⬜ Project utilization sustainability 2019-2030:
  - Baseline projection: demand under demographic trends
  - Demographic adjustment: aging population impact on utilization
  - Gap quantification: demand vs. capacity availability
- ⬜ Identify utilization sustainability risks:
  - Demand growth exceeding supply expansion?
  - Demographic pressure points: which age groups driving demand?
  - Service delivery implications: need for care model shifts?
- ⬜ Recommend utilization interventions:
  - Demand management: preventive care to reduce admissions
  - Care model transformation: shift to community/ambulatory care
  - Demographic planning: age-appropriate service expansion

### Cross-Dimensional Sustainability Analysis
- ⬜ Analyze dimension interdependencies:
  - Workforce-capacity alignment: Are both growing proportionally?
  - Capacity-utilization alignment: Is capacity meeting demand?
  - Expenditure-resource alignment: Is spending translating to resources?
  - Mortality-utilization alignment: Is burden driving demand patterns?
- ⬜ Identify systemic sustainability patterns:
  - Which dimensions most aligned vs. most misaligned?
  - Where are cascading risks (one dimension's challenge creating another's)?
  - Which dimension requires priority intervention?
- ⬜ Calculate overall system sustainability score:
  - Composite score across all dimensions (from Story 5)
  - Trend: Is overall sustainability improving or deteriorating?
  - Sector breakdown: Which sector most/least sustainable?

### Scenario-Based Strategic Planning

#### Scenario 1: Baseline (Current Trajectory)
- ⬜ Define baseline assumptions:
  - Workforce growth: Historical average CAGR
  - Capacity expansion: Historical average expansion rate
  - Utilization growth: Demographic-adjusted historical trend
  - Expenditure growth: Historical average spending growth
- ⬜ Project outcomes 2030:
  - Workforce levels, capacity levels, utilization levels, expenditure levels
  - Gap quantification: shortfalls/surpluses by dimension
  - Sustainability score projection
- ⬜ Identify baseline scenario risks:
  - Which dimensions face critical challenges under baseline?
  - Timeline to crisis: when do gaps become severe?

#### Scenario 2: Optimistic (Favorable Conditions)
- ⬜ Define optimistic assumptions:
  - Workforce growth: Historical maximum CAGR + 20%
  - Capacity expansion: Accelerated expansion (historical max + 20%)
  - Utilization growth: Reduced demand (preventive care success)
  - Expenditure growth: Cost control success (historical min growth)
- ⬜ Project outcomes 2030:
  - Workforce levels, capacity levels, utilization levels, expenditure levels
  - Gap quantification: surplus/adequacy by dimension
  - Sustainability score projection
- ⬜ Assess optimistic scenario requirements:
  - What policy changes required to achieve optimistic trajectory?
  - Investment needs to enable accelerated growth
  - Feasibility: Is optimistic scenario achievable?

#### Scenario 3: Pessimistic (Adverse Conditions)
- ⬜ Define pessimistic assumptions:
  - Workforce growth: Historical minimum CAGR - 20%
  - Capacity expansion: Constrained expansion (budget limits)
  - Utilization growth: Accelerated demand (aging population impact)
  - Expenditure growth: Uncontrolled cost growth (historical max + 20%)
- ⬜ Project outcomes 2030:
  - Workforce levels, capacity levels, utilization levels, expenditure levels
  - Gap quantification: critical shortfalls by dimension
  - Sustainability score projection (risk assessment)
- ⬜ Identify pessimistic scenario risks:
  - Worst-case timeline: when do critical shortages occur?
  - Cascading failures: which dimensions fail first, triggering others?
  - Mitigation requirements: what interventions prevent worst-case?

#### Scenario Comparison and Insights
- ⬜ Create scenario comparison dashboard:
  - Side-by-side outcomes across scenarios
  - Gap magnitude comparison (baseline vs. optimistic vs. pessimistic)
  - Timeline to intervention urgency by scenario
- ⬜ Identify robust strategies:
  - Which interventions beneficial across all scenarios?
  - Which interventions critical only in pessimistic scenario?
- ⬜ Develop scenario-contingent recommendations:
  - If baseline trajectory holds: Recommend X
  - If trends worsen: Implement contingency Y

### Strategic Intervention Impact Modeling
- ⬜ Model intervention impacts:
  - **Intervention A: Accelerated Medical School Intake**
    - Assumption: +30% doctor graduation rate starting 2025
    - Impact: Workforce gap reduction by 2030
    - Cost: Training investment required
  - **Intervention B: New Hospital Construction**
    - Assumption: +15% bed capacity by 2028
    - Impact: Capacity gap reduction
    - Cost: Capital expenditure required
  - **Intervention C: Preventive Care Programs**
    - Assumption: -10% hospital admission rate by 2030
    - Impact: Reduced utilization pressure
    - Cost: Preventive program investment
  - **Intervention D: Care Model Transformation**
    - Assumption: Shift 20% of admissions to community care
    - Impact: Reduced bed utilization, lower expenditure growth
    - Cost: Community care infrastructure investment
- ⬜ Quantify intervention effectiveness:
  - Gap reduction per intervention
  - Cost-benefit analysis: cost per gap unit reduced
  - Timeline: intervention lead time and impact horizon
- ⬜ Prioritize interventions:
  - Rank by impact-to-cost ratio
  - Consider urgency: which gaps most critical?
  - Recommend intervention portfolio addressing multiple dimensions

### International Benchmarking (If Data Available)
- ⬜ Source international comparison data:
  - WHO Global Health Observatory
  - OECD Health Statistics
  - Peer nations: Australia, Japan, South Korea, UK, Canada
- ⬜ Compare Singapore sustainability metrics:
  - Workforce-to-population ratios
  - Bed-to-population ratios
  - Health expenditure as % of GDP
  - Utilization rates
- ⬜ Identify performance gaps:
  - Where Singapore above/below peer averages?
  - Which dimensions Singapore leading/lagging?
- ⬜ Derive best practice insights:
  - Which peer nations have strong sustainability?
  - What strategies explain their success?
  - Applicability to Singapore context?

### Sensitivity Analysis and Robustness Testing
- ⬜ Test key assumption sensitivity:
  - Population growth ±20%: Impact on projections?
  - Workforce growth ±30%: Gap sensitivity?
  - Utilization growth ±25%: Capacity adequacy?
  - Expenditure growth ±20%: Fiscal sustainability?
- ⬜ Identify critical assumptions:
  - Which assumptions most impact projections?
  - Where is greater precision needed?
  - Which assumptions require monitoring?
- ⬜ Assess projection robustness:
  - Do conclusions hold under sensitivity ranges?
  - Which recommendations robust, which contingent?

### Findings Synthesis and Strategic Recommendations
- ⬜ Synthesize key sustainability findings:
  - **Critical Risks Identified**: Top 3-5 sustainability challenges
  - **Priority Dimensions**: Which require immediate intervention?
  - **Timeline Urgency**: Short-term (2025), medium-term (2028), long-term (2030+)
  - **Sector Differences**: Which sectors face greatest challenges?
- ⬜ Develop strategic recommendations:
  - **Workforce Strategy**: Recruitment, training, retention recommendations
  - **Capacity Strategy**: Facility expansion, utilization optimization
  - **Financial Strategy**: Cost control, efficiency improvements, funding models
  - **Utilization Strategy**: Demand management, care model transformation
  - **Cross-Cutting Strategy**: Integrated interventions addressing multiple dimensions
- ⬜ Quantify recommendation impacts:
  - Expected gap reduction per recommendation
  - Investment requirements
  - Implementation timeline
  - Success metrics and monitoring approach
- ⬜ Prioritize recommendations:
  - High impact, low cost (quick wins)
  - High impact, high cost (strategic investments)
  - Risk mitigation priorities (prevent worst-case scenarios)

### Output and Documentation
- ⬜ Create comprehensive strategic assessment report:
  - **Executive Summary**: Key findings, risks, recommendations (2-3 pages)
  - **Dimension-Specific Assessments**: Workforce, capacity, financial, utilization (detailed)
  - **Scenario Analysis**: Baseline, optimistic, pessimistic outcomes
  - **Intervention Modeling**: Strategic option evaluations
  - **International Benchmarking**: Singapore vs. peers
  - **Strategic Recommendations**: Prioritized action plan
  - **Appendix**: Methodology, assumptions, sensitivity analysis
- ⬜ Save strategic assessment report: `results/exports/ps-004_strategic_sustainability_assessment.pdf`
- ⬜ Create executive briefing slides: `reports/presentations/ps-004_sustainability_executive_briefing.pptx`
- ⬜ Save scenario comparison tables:
  - `results/tables/ps-004_scenario_outcomes_2030.csv`
  - `results/tables/ps-004_intervention_impact_analysis.csv`
- ⬜ Save sustainability risk register: `results/tables/ps-004_sustainability_risk_register.csv`
- ⬜ Create strategic visualizations:
  - Multi-scenario projection comparison charts
  - Sustainability vulnerability heatmap (dimension × sector × year)
  - Intervention impact comparison charts
  - Strategic roadmap timeline (2025-2030)
- ⬜ Save visualizations to `reports/figures/ps-004/strategic-analysis/`

## 6. Notes

**Strategic vs. Operational Focus**: This analysis provides strategic-level guidance for long-term planning (5-10 year horizon), not operational short-term workforce/capacity decisions.

**Scenario Planning Importance**: Scenarios enable robust strategic planning under uncertainty. Recommendations should be effective across multiple plausible futures.

**Stakeholder Engagement**: Findings should drive strategic dialogue with MOH leadership. Recommendations require stakeholder validation and refinement.

**Intervention Modeling Limitations**: Impact estimates directional, not precise forecasts. Actual outcomes depend on implementation quality and external factors.

**Policy Context Integration**: Strategic recommendations should consider Singapore's healthcare policy context, political feasibility, and system-specific constraints.

**Related Stories**: 
- Depends on: Story 5 (Sustainability Metrics Engineering)
- Feeds into: Story 7 (Dashboard & Reporting) - findings inform dashboard design

**Estimated Effort**: 2 sprints (includes multi-dimensional analysis, scenario modeling, benchmarking, recommendations)
