# User Story 7: Strategic Planning Dashboard and Comprehensive Sustainability Report

**As a** MOH strategic planning leader,  
**I want** an interactive dashboard and comprehensive report communicating healthcare system sustainability insights,  
**so that** I can monitor sustainability metrics, explore scenarios, and make evidence-based strategic planning decisions.

## 1. 🎯 Acceptance Criteria

- Interactive strategic planning dashboard deployed with multi-dimensional sustainability tracking
- Dashboard features include:
  - Multi-dimensional trend visualization (workforce, capacity, utilization, expenditure, mortality)
  - Sustainability vulnerability heat map (dimension × sector × year)
  - Scenario comparison interface (baseline, optimistic, pessimistic trajectories to 2030)
  - Gap quantification views showing projected shortfalls by dimension
  - Intervention impact simulator enabling "what-if" analysis
  - Time period filtering (historical: 2006-2018, projected: 2019-2030)
  - Sector drill-down (Public, Private, Not-for-Profit)
  - Exportable reports and charts for stakeholder sharing
- Comprehensive sustainability report created documenting:
  - Executive summary with key findings and recommendations
  - Multi-dimensional trend analysis with visualizations
  - Sustainability risk assessment and prioritization
  - Scenario analysis outcomes
  - Strategic intervention recommendations with quantified impacts
  - Implementation roadmap with timeline and success metrics
- User guide created for dashboard navigation and interpretation
- Dashboard and report shared with MOH stakeholders for validation
- Stakeholder feedback incorporated into final deliverables

## 2. 🔒 Technical Constraints

- **Dashboard Technology**: Plotly Dash or Streamlit (interactive Python-based dashboarding)
- **Visualization**: Plotly for interactive charts, matplotlib for static report charts
- **Deployment**: Local deployment initially (containerized for future web deployment)
- **Data Backend**: Parquet files from processed datasets
- **Report Format**: PDF for executive report, markdown for technical documentation
- **Accessibility**: Dashboard usable by non-technical strategic planners
- **Performance**: Dashboard responsive with <2 second load times for visualizations

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Full Framework](../../../domain_knowledge/healthcare-system-sustainability-metrics.md) - Sustainability interpretation guidance
- [Data Visualization Best Practices](.github/instructions/data-analysis-best-practices.instructions.md) - Dashboard design principles
- All domain knowledge files referenced by Stories 1-6 for contextual interpretation

## 4. 📦 Dependencies

**External Packages:**
- **plotly**: Interactive visualizations
- **dash** or **streamlit**: Dashboard framework
- **polars**: Data loading and filtering for dashboard backend
- **matplotlib/seaborn**: Static report visualizations
- **reportlab** or **weasyprint**: PDF report generation

**Internal Dependencies:**
- Depends on: All Stories 1-6 (full analytical pipeline)
- Input from: 
  - `data/4_processed/sustainability_metrics_2006_2018.parquet`
  - `data/4_processed/sustainability_projections_2019_2030.parquet`
  - `results/tables/ps-004_scenario_outcomes_2030.csv`
  - `results/tables/ps-004_intervention_impact_analysis.csv`
  - `results/exports/ps-004_strategic_sustainability_assessment.pdf` (Story 6)
  - All visualizations from Stories 4-6 in `reports/figures/ps-004/`

## 5. ✅ Implementation Tasks

### Dashboard Architecture and Setup
- ⬜ Select dashboard framework: Plotly Dash vs. Streamlit
  - Dash: More customizable, better for complex interactions
  - Streamlit: Faster development, simpler deployment
  - Recommendation: Streamlit for rapid prototyping, migrate to Dash if advanced features needed
- ⬜ Set up dashboard project structure:
  - `src/visualization/dashboard/` - Dashboard code
  - `src/visualization/dashboard/app.py` - Main dashboard application
  - `src/visualization/dashboard/components/` - Reusable visualization components
  - `src/visualization/dashboard/data/` - Data loading and filtering utilities
  - `src/visualization/dashboard/config.yml` - Dashboard configuration
- ⬜ Create data loading module: Efficient loading from parquet files with caching
- ⬜ Set up dashboard styling: MOH branding, professional color scheme

### Dashboard Component 1: Multi-Dimensional Trend Viewer
- ⬜ Create trend visualization interface:
  - **Dimension selector**: Workforce, Capacity, Utilization, Expenditure, Mortality
  - **Metric selector**: Context-specific metrics per dimension
  - **Sector filter**: Public, Private, Not-for-Profit, All
  - **Time range slider**: 2006-2018 (historical)
- ⬜ Implement visualizations:
  - Line charts: Trend over time by dimension
  - Dual-axis charts: Comparing metrics (e.g., workforce vs. capacity)
  - Indexed charts: All dimensions indexed to 2006 = 100 for comparison
  - Growth rate charts: Year-over-year % change by dimension
- ⬜ Add interactive features:
  - Hover tooltips: Show exact values and context
  - Click to drill-down: Dimension → Sector → Professional category
  - Export chart: Download as PNG/SVG for reports
- ⬜ Add trend interpretation annotations:
  - Highlight inflection points
  - Flag periods of rapid change
  - Show trend classification (accelerating, stable, declining)

### Dashboard Component 2: Sustainability Vulnerability Heatmap
- ⬜ Create heatmap visualizations:
  - **Dimension × Year**: Sustainability score by dimension over time
  - **Dimension × Sector**: Comparative sustainability across sectors
  - **Risk Matrix**: Likelihood × Impact heatmap for identified risks
- ⬜ Implement color coding:
  - Green: Strong sustainability (score >70)
  - Yellow: Moderate risk (score 50-70)
  - Red: High risk (score <50)
- ⬜ Add interactive features:
  - Click cell to see detailed metrics
  - Filter by dimension or sector
  - Tooltips explaining vulnerability drivers

### Dashboard Component 3: Scenario Explorer
- ⬜ Create scenario comparison interface:
  - **Scenario selector**: Baseline, Optimistic, Pessimistic
  - **Projection horizon slider**: 2019-2030
  - **Dimension selector**: Which metric to compare across scenarios
- ⬜ Implement scenario visualizations:
  - Multi-line chart: Dimension trajectory under each scenario
  - Confidence intervals: Uncertainty bands around projections
  - Gap visualization: Projected supply vs. demand by scenario
  - Crossover point markers: When demand exceeds supply
- ⬜ Add scenario comparison table:
  - 2030 outcomes by scenario (workforce, capacity, expenditure, gaps)
  - Row-level difference highlighting
- ⬜ Enable scenario customization:
  - Sliders to adjust growth rate assumptions
  - "What-if" analysis: See immediate projection impact

### Dashboard Component 4: Gap Quantification Dashboard
- ⬜ Create gap visualization interface:
  - **Dimension selector**: Which gap to visualize (workforce, capacity, financial)
  - **Sector breakdown**: Gap magnitude by sector
  - **Timeline view**: When gaps emerge and worsen
- ⬜ Implement gap visualizations:
  - Bar charts: Gap magnitude by dimension (2030 projection)
  - Waterfall charts: Current level → Projected demand → Projected gap
  - Timeline charts: Gap emergence and growth 2019-2030
- ⬜ Add impact quantification:
  - Translate gaps to operational metrics:
    - Workforce gap → Patients per healthcare worker
    - Capacity gap → Bed utilization rate
    - Financial gap → Budget deficit as % of GDP
- ⬜ Add urgency indicators:
  - Traffic light system: Red (critical gap), Yellow (moderate), Green (adequate)
  - Timeline to critical threshold

### Dashboard Component 5: Intervention Impact Simulator
- ⬜ Create intervention modeling interface:
  - **Intervention selector**: Choose from modeled interventions (from Story 6)
  - **Intensity slider**: Adjust intervention magnitude (e.g., ±50% from baseline)
  - **Timeline selector**: When intervention starts (2023-2028)
- ⬜ Implement intervention impact visualization:
  - Projection chart: Trajectory with vs. without intervention
  - Gap reduction quantification: How much intervention closes gap
  - Cost display: Investment required for selected intervention
  - ROI calculation: Cost per gap unit reduced
- ⬜ Enable multi-intervention analysis:
  - Checkboxes to combine interventions
  - Cumulative impact calculation
  - Total investment summary
- ⬜ Add intervention recommendations:
  - Highlight high-impact, low-cost interventions
  - Flag critical interventions (prevent worst-case scenarios)

### Dashboard Component 6: Sector Comparison View
- ⬜ Create sector benchmarking interface:
  - **Metric selector**: Sustainability metrics to compare
  - **Sector comparison**: Side-by-side Public, Private, Not-for-Profit
- ⬜ Implement sector comparison visualizations:
  - Grouped bar charts: Metric values by sector
  - Radar charts: Multi-metric sector profiles
  - Ranking tables: Which sector strongest/weakest by dimension
- ⬜ Add sector-specific insights:
  - Relative sustainability scores
  - Sector-specific challenges highlighted
  - Best practices from leading sector

### Dashboard Navigation and User Experience
- ⬜ Create dashboard landing page:
  - Executive summary with key metrics
  - Quick links to dashboard sections
  - Latest data update timestamp
- ⬜ Implement navigation:
  - Sidebar menu: Component selection
  - Breadcrumb navigation: Track location in dashboard
  - Home button: Return to landing page
- ⬜ Add contextual help:
  - Info icons with metric definitions
  - Interpretation guidance tooltips
  - Dashboard tour for first-time users
- ⬜ Implement filters and controls:
  - Global filters: Apply to all components
  - Component-specific filters
  - Reset filters button
- ⬜ Enable export functionality:
  - Export current view as PNG/PDF
  - Download underlying data as CSV
  - Generate custom report with selected charts

### Comprehensive Sustainability Report Creation
- ⬜ Compile comprehensive report (60-80 pages):
  - **Executive Summary** (5 pages):
    - Key sustainability findings
    - Critical risks identified
    - Scenario analysis summary
    - Top 5 strategic recommendations
    - Implementation timeline at-a-glance
  - **Introduction** (5 pages):
    - Problem statement and objectives
    - Data sources and methodology
    - Analytical approach overview
    - Report structure guide
  - **Healthcare System Overview** (10 pages):
    - Singapore healthcare landscape
    - Multi-dimensional framework explanation
    - Data coverage and quality assessment
    - Benchmark context (international comparison if available)
  - **Dimension-Specific Assessments** (30 pages):
    - Workforce Sustainability Assessment (8 pages)
    - Capacity Sustainability Assessment (8 pages)
    - Financial Sustainability Assessment (7 pages)
    - Utilization Sustainability Assessment (7 pages)
    - Each section includes: trends, gaps, projections, risks
  - **Multi-Dimensional Sustainability Analysis** (10 pages):
    - Cross-dimensional patterns and interdependencies
    - Composite sustainability vulnerability assessment
    - Sector-specific sustainability profiles
    - Overall system sustainability scoring
  - **Scenario Analysis** (10 pages):
    - Scenario definitions and assumptions
    - Baseline scenario outcomes and risks
    - Optimistic scenario analysis
    - Pessimistic scenario analysis
    - Scenario comparison and insights
  - **Strategic Recommendations** (10 pages):
    - Intervention portfolio overview
    - Dimension-specific recommendations (workforce, capacity, financial, utilization)
    - Cross-cutting strategic initiatives
    - Prioritization framework and timeline
    - Success metrics and monitoring approach
  - **Implementation Roadmap** (5 pages):
    - Short-term priorities (2024-2026)
    - Medium-term initiatives (2027-2028)
    - Long-term strategic goals (2029-2030)
    - Responsible parties and governance
    - Milestones and checkpoints
  - **Appendices**:
    - Detailed methodology notes
    - Data dictionary and metric definitions
    - Sensitivity analysis results
    - International benchmarking data sources
    - References and further reading
- ⬜ Integrate visualizations throughout report:
  - All key charts from exploratory, feature engineering, and strategic analysis
  - Consistent visual styling and branding
  - Clear captions with interpretation guidance
- ⬜ Format report professionally:
  - MOH branding and styling
  - Executive-friendly language (minimize jargon)
  - Clear section headers and navigation
  - Page numbers and table of contents
- ⬜ Generate PDF report using reportlab or LaTeX
- ⬜ Save report to `reports/ps-004_comprehensive_sustainability_report.pdf`

### Executive Briefing Slide Deck Creation
- ⬜ Create executive slide deck (20-25 slides):
  - Title and overview (1 slide)
  - Problem statement and objectives (1 slide)
  - Methodology overview (1-2 slides)
  - Key findings by dimension (5 slides: one per dimension)
  - Multi-dimensional sustainability summary (1-2 slides)
  - Critical risks identified (2 slides)
  - Scenario analysis overview (2-3 slides)
  - Strategic recommendations (3-4 slides)
  - Implementation roadmap (2 slides)
  - Success metrics and monitoring (1 slide)
  - Next steps and call to action (1 slide)
- ⬜ Design slides for executive audience:
  - High-level insights, not technical details
  - Visual-heavy (charts, infographics)
  - Clear action implications
  - Quantified impacts
- ⬜ Save slide deck to `reports/presentations/ps-004_executive_briefing.pptx`

### User Guide and Documentation
- ⬜ Create dashboard user guide:
  - Dashboard overview and navigation
  - Component-by-component usage instructions
  - Metric definitions and interpretation
  - Common use cases and workflows
  - Troubleshooting and FAQ
- ⬜ Create interpretation guide:
  - How to read sustainability scores
  - How to interpret scenarios
  - How to use gap metrics for planning
  - How to evaluate interventions
- ⬜ Save user guide to `docs/dashboard_user_guide.md`
- ⬜ Create video walkthrough (optional):
  - Screen recording demonstrating dashboard features
  - Narrated explanation of key insights
  - Save to `reports/ps-004_dashboard_walkthrough.mp4`

### Stakeholder Validation and Feedback
- ⬜ Share dashboard prototype with MOH stakeholders:
  - Strategic planning team
  - Healthcare system administrators
  - Budget and finance leads
  - Workforce planning authorities
- ⬜ Conduct stakeholder demo sessions:
  - Live walkthrough of dashboard features
  - Highlight key insights and scenarios
  - Gather feedback on usability and relevance
- ⬜ Collect structured feedback:
  - Dashboard functionality: missing features, improvements
  - Data insights: surprising findings, validation requests
  - Recommendations: feasibility, prioritization, refinement
  - Report clarity: comprehensiveness, readability
- ⬜ Incorporate feedback into dashboard and report:
  - Prioritize high-impact changes
  - Refine visualizations based on stakeholder needs
  - Adjust recommendations based on feasibility input

### Deployment and Handoff
- ⬜ Containerize dashboard (Docker):
  - Create Dockerfile for reproducible deployment
  - Include all dependencies and data
  - Test deployment on clean environment
- ⬜ Document deployment process:
  - Installation instructions
  - Configuration requirements
  - How to update data
  - Troubleshooting common issues
- ⬜ Create data update process:
  - Script to refresh dashboard with new data
  - Schedule for periodic updates (annual sustainability review)
- ⬜ Handoff to MOH IT/Analytics team:
  - Codebase and documentation transfer
  - Training session on dashboard maintenance
  - Support contact for questions

### Output and Deliverables
- ⬜ Save dashboard application:
  - `src/visualization/dashboard/` (full codebase)
  - `Dockerfile` for deployment
  - `README.md` with setup instructions
- ⬜ Save comprehensive sustainability report:
  - `reports/ps-004_comprehensive_sustainability_report.pdf`
- ⬜ Save executive briefing:
  - `reports/presentations/ps-004_executive_briefing.pptx`
- ⬜ Save user guide:
  - `docs/dashboard_user_guide.md`
- ⬜ Archive all visualizations:
  - `reports/figures/ps-004/dashboard/` (all dashboard charts)
  - `reports/figures/ps-004/report/` (all report charts)

## 6. Notes

**Dashboard vs. Report Trade-offs**:
- Dashboard: Interactive exploration, self-service analytics, real-time filtering
- Report: Comprehensive narrative, structured recommendations, portable document
- Both serve complementary purposes: dashboard for ongoing monitoring, report for strategic planning

**Stakeholder-Centric Design**: Dashboard and report must serve strategic planning needs, not just present data. Focus on actionable insights, not exhaustive metrics.

**Deployment Considerations**: Initial local deployment allows rapid iteration. Future web deployment enables broader access but requires infrastructure and security considerations.

**Dashboard Maintenance**: Dashboard requires periodic data updates to remain relevant. Establish update cadence (annual sustainability review cycle).

**Scenario Simulator Caution**: "What-if" analysis empowers users but requires clear guidance on limitations. Projections are directional, not precise forecasts.

**Related Stories**: 
- Depends on: All Stories 1-6 (complete analytical pipeline)
- Final deliverable summarizing entire PS-004 effort

**Estimated Effort**: 2 sprints (includes dashboard development, report compilation, stakeholder validation)
