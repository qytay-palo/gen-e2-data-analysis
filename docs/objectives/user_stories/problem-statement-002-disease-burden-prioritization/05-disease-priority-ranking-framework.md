# User Story 5: Disease Priority Ranking and Intervention Recommendations

**As a** MOH policy leadership team member,  
**I want** a quantitative disease priority ranking framework combining burden magnitude, trend direction, and demographic risk,  
**so that** I can make evidence-based decisions about prevention program investment and public health resource allocation.

## 1. 🎯 Acceptance Criteria

- Disease priority ranking framework developed and validated
- All major diseases ranked by composite priority score
- Priority classification created: Critical, High, Medium, Low priority
- Trend-based intervention recommendations generated:
  - Rising burden diseases → Preventive intervention urgency
  - Declining burden diseases → Successful program analysis
  - Stable burden diseases → Maintenance strategies
- Demographic-targeted intervention opportunities identified
- Priority ranking report generated with:
  - Disease rankings with justifications
  - Intervention recommendations by disease
  - Resource allocation suggestions
- Ranking results saved to `results/tables/ps-002/disease_priority_ranking_{timestamp}.csv`
- Recommendations report saved to `reports/ps-002/priority_ranking_report_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Ranking Framework**: Transparent, interpretable methodology (no black-box algorithms)
- **Validation**: Sensitivity analysis on ranking weights to ensure robustness
- **Stakeholder Alignment**: Rankings validated against stakeholder expectations
- **Documentation**: Full audit trail of ranking logic and assumptions

## 3. 📚 Domain Knowledge References

- [Disease Priority Index Construction](../../../domain_knowledge/disease-burden-mortality-analysis.md#disease-ranking-index) - Framework for multi-dimensional disease prioritization
- [Analytical Methodologies](../../../domain_knowledge/disease-burden-mortality-analysis.md#analytical-methodologies) - Best practices for disease burden comparison

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data analysis and ranking calculations
- **numpy**, **scipy**: Statistical analysis and ranking algorithms

**Internal Dependencies:**
- Story 4 output: Calculated disease burden metrics and features

## 5. ✅ Implementation Tasks

### Priority Ranking Framework Design
- ⬜ Define priority index formula: `0.4 × Burden Score + 0.3 × Trend Score + 0.3 × Demographic Risk Score`
- ⬜ Normalize all component scores to 0-100 scale
- ⬜ Document weighting rationale based on stakeholder priorities
- ⬜ Create alternative weighting scenarios for sensitivity analysis
- ⬜ Validate that framework aligns with MOH strategic priorities

### Burden Score Calculation
- ⬜ Rank diseases by absolute mortality burden (total ASMR)
- ⬜ Normalize burden to 0-100 scale: `(Disease Burden / Max Burden) × 100`
- ⬜ Calculate average annual ASMR as secondary burden metric
- ⬜ Create burden severity classification: Very High (>200/100k), High (100-200), Medium (50-100), Low (<50)
- ⬜ Validate burden scores against WHO global disease rankings

### Trend Score Calculation
- ⬜ Calculate average annual growth rate (1990-2019) for each disease
- ⬜ Assign trend scores: Rising diseases (>+2%) = 100, Stable (±2%) = 50, Declining (<-2%) = 0
- ⬜ Weight by trend magnitude: Faster growth = higher score
- ⬜ Adjust for trend acceleration: Accelerating trends score higher
- ⬜ Identify diseases with reversal patterns (was declining, now rising)

### Demographic Risk Score Calculation
- ⬜ Calculate burden concentration in vulnerable populations (elderly, young children)
- ⬜ Assign risk score based on age distribution: High elderly burden (65+) = higher score
- ⬜ Incorporate gender disparity factor (>150% male/female ratio = elevated risk)
- ⬜ Weight by premature mortality (deaths in <65 age group)
- ⬜ Normalize demographic risk to 0-100 scale

### Composite Priority Index Calculation
- ⬜ Calculate weighted composite index for each disease
- ⬜ Rank diseases from highest (1) to lowest priority score
- ⬜ Classify into priority tiers:
  - Critical Priority: Score 75-100
  - High Priority: Score 50-74
  - Medium Priority: Score 25-49
  - Low Priority: Score <25
- ⬜ Generate ranked priority list with tier classifications

### Sensitivity Analysis
- ⬜ Test alternative weighting scenarios:
  - Burden-focused: 60% / 20% / 20%
  - Trend-focused: 20% / 60% / 20%
  - Demographic-focused: 20% / 20% / 60%
- ⬜ Calculate rank-order correlation between scenarios
- ⬜ Identify diseases whose ranking is stable vs. sensitive to weights
- ⬜ Document which weighting assumptions most influence rankings
- ⬜ Validate top 5 diseases remain in top tier across all scenarios

### Intervention Recommendations by Disease
- ⬜ For Critical Priority diseases: Recommend urgent preventive intervention scale-up
- ⬜ For High Priority diseases: Recommend targeted programs for at-risk demographics
- ⬜ For Declining Burden diseases: Analyze successful interventions to scale elsewhere
- ⬜ For Rising Burden diseases: Recommend root cause analysis and intervention piloting
- ⬜ For Demographically concentrated diseases: Recommend targeted screening/prevention

### Trend-Based Strategy Development
- ⬜ Identify rising diseases requiring proactive prevention investment
- ⬜ Analyze declining diseases to understand what interventions worked
- ⬜ Recommend continuation strategies for stable low-burden diseases
- ⬜ Flag diseases with inflection points (trend reversals) for investigation
- ⬜ Prioritize intervention pilots for highest-priority rising diseases

### Resource Allocation Guidance
- ⬜ Estimate relative resource allocation based on priority scores
- ⬜ Recommend budget weighting: % of prevention budget aligned to priority tiers
- ⬜ Suggest staffing allocation across disease control programs
- ⬜ Identify underinvested areas (high priority, low current resources)
- ⬜ Document resource reallocation recommendations

### Validation and Stakeholder Review
- ⬜ Compare rankings to current MOH disease program priorities
- ⬜ Validate against WHO disease burden rankings for alignment
- ⬜ Identify any surprising rankings requiring explanation
- ⬜ Document assumptions and limitations of ranking methodology
- ⬜ Prepare stakeholder presentation with ranking justifications

### Reporting and Documentation
- ⬜ Generate comprehensive priority ranking report
- ⬜ Create executive summary with top 5 priority diseases and recommendations
- ⬜ Visualize priority scores (bar chart, heat map by dimension)
- ⬜ Document sensitivity analysis results
- ⬜ Save ranking tables to `results/tables/ps-002/`
- ⬜ Save recommendations report to `reports/ps-002/`

## 6. Notes

**Priority Index Weighting Rationale:**
- **Burden (40%)**: Absolute lives lost is primary policy concern
- **Trend (30%)**: Rising diseases require proactive intervention before becoming critical
- **Demographic Risk (30%)**: Vulnerable populations and premature mortality increase priority

**Intervention Strategy Framework:**
- **Critical Priority + Rising Trend**: Immediate prevention program scale-up
- **Critical Priority + Declining Trend**: Sustain successful interventions, study for replication
- **High Priority + Stable Trend**: Maintain current investment, monitor for changes
- **Medium/Low Priority + Rising Trend**: Early warning; pilot interventions before escalation

**Stakeholder Communication:**
- Rankings must be interpretable and defensible to non-technical policy makers
- Provide clear rationale for each disease's priority classification
- Acknowledge limitations: Rankings based on mortality only (not morbidity/disability)

**Data Limitations to Document:**
- Rankings based on mortality; DALYs would provide more comprehensive burden view
- Limited to major chronic diseases; infectious disease burden may require separate analysis
- Historical data (through 2019); pandemic impacts not captured

**Related Stories:**
- Depends on: Story 4 (Disease burden metrics and features)
- Enables: Story 6 (Dashboard and visualization)
- Informs: Policy discussions on prevention program investment
