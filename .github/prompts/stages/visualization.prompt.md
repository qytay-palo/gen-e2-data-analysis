---
description: Visualization and Reporting Stage with MCP Integration
stage: Visualization & Reporting
---

# Stage Prompt: Visualization and Reporting

## Objective

Create compelling visualizations and comprehensive reports that communicate analysis findings to stakeholders.

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Analysis Results**: 
   - `results/tables/{epic_id}/` - Summary statistics, analytical tables
   - `results/metrics/{epic_id}_metrics.json` - KPIs and performance metrics
   - `notebooks/2_analysis/{epic_id}/` - Analysis notebooks with findings

2. **Data for Visualization**:
   - `data/4_processed/{epic_id}/` - Clean datasets
   - `data/3_interim/{epic_id}/` - Intermediate processed data
   - Database tables (if using SQLite)

3. **Reporting Requirements**: From user story or stakeholder specs
   - Target audience (executives, analysts, domain experts)
   - Report format (dashboard, PDF, presentation)
   - Key messages to convey
   - Deadline and delivery format

4. **Design Specifications**:
   - Brand colors and style guide (if applicable)
   - Chart types required
   - Interactivity requirements
   - Accessibility requirements

5. **Data Volume Assessment**:
   - Total number of records to visualize
   - Expected concurrent dashboard users
   - Data refresh frequency requirements
   - Performance constraints (load time, query limits)

## Output Requirements

The visualization and reporting MUST produce:

1. **Static Visualizations**: `reports/figures/{epic_id}/`
   - High-resolution charts and plots (PNG, PDF)
   - Publication-quality graphics (300 DPI)
   - Properly labeled with titles, axes, legends
   - Accessible color schemes

2. **Interactive Dashboards**: `reports/dashboards/{epic_id}/`
   - HTML dashboards (Plotly, Bokeh)
   - Power BI files (.pbix) if applicable
   - Streamlit/Dash apps
   - Jupyter Dashboard notebooks

3. **Reports**: `reports/presentations/{epic_id}/`
   - Executive summaries (PDF)
   - Slide decks (PPTX)
   - Technical reports (Markdown/PDF)
   - Infographics

4. **Visualization Documentation**: `reports/{epic_id}/visualization_guide.md`
   - Description of each visualization
   - Data sources and calculations
   - Interpretation guidance
   - Update procedures

## Execution Steps

### Step 1: Visualization Planning

```
1. Create visualization directories:
   - reports/figures/{epic_id}/
   - reports/dashboards/{epic_id}/
   - reports/presentations/{epic_id}/

2. Read analysis results:
   - Read results/metrics/{epic_id}_metrics.json
   - Read results/tables/{epic_id}/*.csv
   - Read analysis summary from results/{epic_id}/analysis_summary.md

3. Identify key findings to visualize:
   - Most important metrics and KPIs
   - Trends and patterns discovered
   - Comparisons and relationships
   - Outliers and anomalies

4. Select appropriate chart types for each finding (see Chart Selection Guide)

5. Choose visualization tools based on requirements:
   - Data volume and performance needs
   - Interactivity requirements
   - Target audience technical proficiency
   - Deployment environment
   - See Tool Selection Matrix below for guidance
```

### Step 1.5: Tool Selection

```
Choose appropriate tools based on requirements:

**For Static Visualizations:**
- Matplotlib/Seaborn (Python) - Publication quality, full control
- ggplot2 (R) - Statistical graphics, grammar of graphics
- Plotly (static export) - Interactive-first with static output

**For Interactive Dashboards:**
- Tableau - Enterprise BI, self-service analytics, no coding
- Power BI - Microsoft ecosystem, business users
- Plotly Dash - Python-based, custom web apps, ML integration
- Streamlit - Rapid prototyping, data science focus
- Bokeh - Interactive plots, large datasets, server-side processing
- Apache ECharts - JavaScript, high performance, rich chart types
- D3.js - Complete control, custom complex visualizations
- Observable - Reactive notebooks, shareable visualizations

**For Large Datasets (>1M rows):**
- Datashader (aggregation) + HoloViews/Bokeh
- Plotly + data aggregation layer
- Apache Superset (database-native visualization)
- Grafana (time-series, monitoring)
- Consider database-side aggregation before visualization

**For Real-Time/Monitoring:**
- Grafana + Prometheus/InfluxDB
- Streamlit with auto-refresh
- Custom WebSocket-based dashboards

**Decision Factors:**
1. Data size: >1M rows → use aggregation strategies
2. Audience: Technical vs business users
3. Deployment: Cloud, on-premise, or embedded
4. Maintenance: Self-service vs developer-maintained
5. Budget: Open-source vs commercial licenses
```

### Step 2: Time Series Visualizations

```
For temporal data and trends:

1. Line Charts:
   - Daily/weekly/monthly trends
   - Multiple series comparisons
   - Confidence intervals or prediction bands
   - Annotations for significant events

2. Area Charts:
   - Cumulative trends
   - Stacked area for composition over time
   - Fill between for ranges or thresholds

3. Heat Maps:
   - Day-of-week × Hour-of-day patterns
   - Calendar heatmaps for daily values
   - Correlation matrices over time

4. Apply best practices:
   - Clear title describing what is shown
   - X-axis: Time with appropriate granularity
   - Y-axis: Labeled with units
   - Legend if multiple series
   - Grid lines for readability
   - Appropriate date formatting

5. Save visualizations
```

### Step 3: Distribution Visualizations

```
For showing data distributions and spread:

1. Histograms:
   - Frequency distributions
   - Appropriate bin sizes (Sturges' rule or Freedman-Diaconis)
   - Overlay normal distribution curve if relevant

2. Box Plots:
   - Show median, quartiles, outliers
   - Compare distributions across groups
   - Violin plots for distribution shape

3. Density Plots:
   - Smooth distribution curves
   - Multiple overlapping distributions
   - Kernel density estimation (KDE)

4. Q-Q Plots:
   - Test for normality
   - Compare to theoretical distributions

5. Apply best practices:
   - Clear title and axis labels
   - Show sample sizes
   - Mark mean/median if relevant
   - Highlight outliers or thresholds
   - Use consistent color schemes

6. Save visualizations
```

### Step 4: Comparison Visualizations

```
For comparing groups, categories, or time periods:

1. Bar Charts:
   - Vertical bars for categories
   - Horizontal bars for long labels
   - Grouped bars for multi-category comparison
   - Sorted by value for emphasis

2. Grouped/Stacked Bar Charts:
   - Compare multiple metrics across categories
   - Show composition within categories
   - Use stacking wisely (100% stacked for proportions)

3. Bullet Charts:
   - Performance vs targets
   - Show actual, target, and ranges
   - Compact comparison format

4. Small Multiples:
   - Same chart type for each category
   - Consistent scales for comparison
   - Faceted/panel charts

5. Apply best practices:
   - Start bars at zero
   - Maintain consistent colors across charts
   - Order categories meaningfully
   - Include data labels for precision
   - Show comparison baselines

6. Save visualizations
```

### Step 5: Relationship Visualizations

```
For showing correlations and relationships:

1. Scatter Plots:
   - Relationship between two variables
   - Add regression line or LOESS curve
   - Color points by category or third variable
   - Size points by magnitude

2. Correlation Heat Maps:
   - Show correlation coefficients
   - Use diverging color scheme (red-white-blue)
   - Annotate with correlation values
   - Hierarchical clustering of variables

3. Bubble Charts:
   - Three dimensions: X, Y, bubble size
   - Optional: color for fourth dimension
   - Include legend for bubble sizes

4. Network Diagrams:
   - Show relationships between entities
   - Node size by importance
   - Edge width by strength

5. Apply best practices:
   - Show correlation coefficient (R² value)
   - Include reference lines (y=x, trend)
   - Highlight significant relationships
   - Label outliers
   - Use transparency for overlapping points

6. Save visualizations
```

### Step 6: Geographic Visualizations

```
For spatial data and geographic patterns:

1. Choropleth Maps:
   - Color regions by metric value
   - Use appropriate color scales
   - Include legend with value ranges
   - Label key regions

2. Point Maps:
   - Show facility locations
   - Size by metric (visits, capacity)
   - Color by category or performance

3. Heat Maps (Spatial):
   - Density of events or facilities
   - Hot spots and cold spots
   - Gradient overlay on map

4. Apply best practices:
   - Use appropriate map projection
   - Include scale and north arrow
   - Label major landmarks or regions
   - Choose colorblind-safe palettes
   - Provide context (boundaries, cities)

5. Save visualizations
```

### Step 7: Composition Visualizations

```
For showing part-to-whole relationships:

1. Pie Charts (use sparingly):
   - Maximum 5-7 slices
   - Order slices by size
   - Pull out most important slice
   - Show percentages

2. Donut Charts:
   - Similar to pie but with center space
   - Can show total in center
   - Better for multiple rings

3. Treemaps:
   - Hierarchical composition
   - Size by value
   - Color by category or metric
   - Interactive drill-down

4. Stacked Area Charts:
   - Composition over time
   - Show cumulative total
   - Smooth or stepped

5. Apply best practices:
   - Use only when showing parts of whole
   - Ensure parts add to 100%
   - Limit number of categories
   - Use bar charts if comparison needed
   - Include actual values, not just %

6. Save visualizations
```

### Step 8: Statistical Visualizations

```
For statistical analysis results:

1. Confidence Interval Plots:
   - Show point estimates with error bars
   - 95% confidence intervals
   - Compare across groups

2. Forest Plots:
   - Meta-analysis style
   - Multiple studies or groups
   - Show effect sizes with CI

3. ROC Curves (for classification):
   - True positive vs false positive rate
   - Show AUC score
   - Diagonal reference line

4. Residual Plots:
   - Model diagnostics
   - Scatter of residuals
   - Q-Q plot of residuals

5. Survival Curves (Kaplan-Meier):
   - Time-to-event analysis
   - Multiple groups comparison
   - Confidence bands
   - Censored data indicators

6. Funnel Plots:
   - Compare performance across entities
   - Show control limits (95%, 99.8%)
   - Identify outliers
   - Use for variance monitoring

7. Control Charts (SPC):
   - Monitor process over time
   - Show mean, UCL, LCL
   - Mark special cause variation
   - Trend and shift detection

8. Waterfall Charts:
   - Show cumulative effect of changes
   - Start value → intermediate changes → end value
   - Useful for variance analysis
   - Color increases vs decreases

9. Sankey Diagrams:
   - Flow and transition visualization
   - Show magnitude of flows
   - Multi-stage processes
   - Retention/conversion funnels

10. Apply best practices:
    - Show p-values or significance
    - Mark significance levels (*, **, ***)
    - Include sample sizes
    - Show statistical test used
    - Provide interpretation guide

11. Save visualizations
```

### Step 9: Interactive Dashboard Creation

```
For dynamic, explorable visualizations:

1. Choose dashboard framework (see Tool Selection Matrix in Step 1.5)

2. Dashboard architecture:
   - Data layer: Database connections, caching strategy
   - Processing layer: Aggregations, calculations
   - Presentation layer: UI components, charts
   - Separation of concerns for maintainability

3. Performance optimization:
   - Pre-aggregate data at appropriate granularity
   - Implement caching (Redis, in-memory)
   - Use database-side calculations where possible
   - Lazy loading for non-critical components
   - Pagination for large tables (50-100 rows per page)
   - Query timeouts to prevent long-running queries
   - Connection pooling for concurrent users

4. Dashboard components:
   - Filters and controls (dropdowns, sliders, date pickers)
   - Multiple linked charts (click-to-filter)
   - Metrics cards (KPIs, summary stats)
   - Data tables (sortable, filterable, exportable)
   - Update timestamp and refresh button
   - Loading indicators for async operations
   - Error messages and empty state handling

5. Dashboard layout:
   - F-pattern layout (most important top-left)
   - Logical organization (top-to-bottom priority)
   - Responsive design (mobile-friendly breakpoints)
   - Consistent styling and spacing
   - Clear navigation and breadcrumbs
   - Collapsible sections for advanced filters

6. Add interactivity:
   - Hover tooltips with contextual details
   - Click to drill-down to detailed views
   - Zoom and pan for time series exploration
   - Cross-filtering between charts
   - Export functionality (CSV, Excel, PNG, PDF)
   - Bookmark/share specific views (URL parameters)
   - Reset filters button

7. State management:
   - Persist user selections (local storage/session)
   - Deep linking (URL reflects current state)
   - Undo/redo for exploration
   - Save custom views per user

8. Data refresh strategy:
   - Manual refresh button with last updated timestamp
   - Auto-refresh interval for real-time dashboards (30s-5min)
   - Background data updates without UI disruption
   - Visual indicator when data is stale
   - Incremental updates for large datasets

9. Performance targets:
   - Initial load: <3 seconds
   - Data refresh: <1 second for filtered views
   - Filter interactions: <500ms response
   - Support 50+ concurrent users (load test)
   - Graceful degradation under high load

10. Save dashboard files and deployment artifacts
```

### Step 10: Executive Reports and Presentations

```
For stakeholder communication:

1. Executive Summary (1-2 pages):
   - Key findings (3-5 bullet points)
   - Most important visualizations (2-3)
   - Recommendations (actionable steps)
   - Next steps

2. Slide Deck:
   - Title slide (project name, date, authors)
   - Agenda/outline
   - Background and objectives (1-2 slides)
   - Methodology (1 slide)
   - Key findings with visualizations (5-8 slides)
   - Recommendations (2-3 slides)
   - Appendix (detailed tables, technical notes)

3. Technical Report:
   - Complete methodology
   - All visualizations with descriptions
   - Statistical test results
   - Limitations and caveats
   - References and data sources

4. Infographic (for broader audience):
   - Visual storytelling
   - Minimal text, maximum impact
   - Key numbers highlighted
   - Simple, clean design

5. Save reports
```

### Step 11: Accessibility and Quality Checks

```
Ensure visualizations are accessible and high quality:

1. Color Accessibility:
   - Use colorblind-safe palettes (viridis, ColorBrewer)
   - Don't rely on color alone (use shapes, patterns)
   - Sufficient contrast ratios (WCAG standards)
   - Test with colorblind simulators

2. Text Accessibility:
   - Minimum font size 10pt for print, 12pt for screens
   - High contrast text on backgrounds
   - Clear, readable fonts (avoid decorative fonts)
   - Alt text for all visualizations

3. Data Integrity:
   - Verify data accuracy (spot check values)
   - Consistent units across visualizations
   - Correct calculations (double-check formulas)
   - Appropriate precision (decimal places)

4. Design Quality:
   - Remove chart junk (unnecessary decorations)
   - Maximize data-ink ratio
   - Consistent styling across all charts
   - Professional appearance

5. Verify all files created
```

### Step 12: Documentation and Delivery

```
1. Create visualization guide:
   - Title and description for each visualization
   - Data source and date range
   - Calculation methods
   - Interpretation notes
   - Update procedures for reproducibility

2. Organize deliverables:
   - Group by type (static, interactive, reports)
   - Consistent naming convention
   - Version control (include dates)
   - README for navigation

3. Package for delivery:
   - Create ZIP archive if needed
   - Include data dictionaries
   - Include reproduction scripts
   - Include update instructions

4. Write documentation
```

### Step 13: Verification

```
1. Verify all required outputs were created:
   - List files in reports/figures/{epic_id}/
   - List files in reports/dashboards/{epic_id}/
   - List files in reports/presentations/{epic_id}/

2. Verify visualization quality:
   - All images at required resolution (300 DPI for print)
   - All charts properly labeled with titles, axes, legends
   - All interactive dashboards functional and tested
   - All reports complete with findings and recommendations

3. Cross-check against acceptance criteria from user story

4. Verify testing completion:
   - All tests from Step 13 completed
   - Test report documented
   - Critical issues resolved

5. Document verification results
```

## Visualization Best Practices

### 1. Choose the Right Chart Type

**Chart Selection Guide:**

```
┌─────────────────────┬─────────────────────────────────────────┐
│ Data Relationship   │ Recommended Chart Type                  │
├─────────────────────┼─────────────────────────────────────────┤
│ Time series         │ Line chart, area chart                  │
│ Distribution        │ Histogram, box plot, violin plot        │
│ Comparison          │ Bar chart (vertical/horizontal)         │
│ Ranking             │ Sorted bar chart, bullet chart          │
│ Correlation         │ Scatter plot, correlation heatmap       │
│ Composition         │ Stacked bar, treemap, donut chart       │
│ Part-to-whole       │ Pie chart (≤5 slices), stacked 100%     │
│ Geographic/spatial  │ Choropleth map, point map, heatmap      │
│ Flow/process        │ Sankey diagram, funnel chart            │
│ Hierarchical        │ Treemap, sunburst, dendrogram           │
│ Network             │ Network diagram, chord diagram          │
│ Statistical         │ Box plot, violin plot, Q-Q plot         │
│ Deviation           │ Diverging bar chart, bullet chart       │
│ Multi-dimensional   │ Bubble chart, parallel coordinates      │
│ Change over time    │ Waterfall chart, slope graph            │
│ Performance         │ Gauge, bullet chart, control chart      │
└─────────────────────┴─────────────────────────────────────────┘
```

**Decision Tree:**
```
1. What is your data?
   └─> One variable
       └─> Categorical → Bar chart
       └─> Continuous → Histogram, density plot
   └─> Two variables
       └─> Both categorical → Grouped bar, heatmap
       └─> One categorical, one continuous → Bar chart, box plot
       └─> Both continuous → Scatter plot, line chart
   └─> Three+ variables
       └─> Bubble chart, faceted plots, small multiples
   └─> Time dimension → Line chart, area chart
   └─> Geographic → Map-based visualizations
   └─> Hierarchical → Treemap, sunburst
```

### 2. Design Principles

**Do's:**
```
✅ Maximize data-ink ratio (remove non-essential elements)
✅ Use consistent colors and styling across all charts
✅ Start axes at zero for bar charts (magnitude comparison)
✅ Label everything clearly (title, axes, units, legend)
✅ Include data sources and timestamps
✅ Use whitespace effectively
✅ Align and group related elements
✅ Maintain consistent scale across comparable charts
✅ Show uncertainty (confidence intervals, error bars)
✅ Order categories meaningfully (alphabetical, by value, chronological)
✅ Use color purposefully, not decoratively
✅ Provide context (benchmarks, targets, averages)
✅ Tell a story with logical flow
```

**Don'ts - Anti-Patterns:**
```
❌ 3D charts (distort perception, hard to read values)
❌ Dual-axis charts (misleading scale comparisons)
❌ Pie charts with >5 slices (hard to compare angles)
❌ Truncated axes on bar charts (exaggerates differences)
❌ Too many colors (rainbow schemes confuse)
❌ Chart junk (unnecessary decorations, backgrounds)
❌ Mixing chart types without reason
❌ Relying solely on color to convey information
❌ Tiny fonts or cramped labels
❌ Unlabeled axes or missing units
❌ Too much data in one chart (split into small multiples)
❌ Decorative fonts or all caps for body text
❌ Using area/volume for 1D comparisons (bubble distortion)
❌ Hiding zero baseline (misleading trends)
❌ Excessive precision (0.123456789 vs 0.12)
```

### 3. Storytelling with Data

**Narrative Structure:**
```
1. Setup (Context):
   - What is the situation?
   - Why does it matter?
   - What question are we answering?
   - Provide baseline/historical context

2. Conflict (Challenge/Problem):
   - What changed or went wrong?
   - Where are the gaps or opportunities?
   - Show the data that reveals the issue
   - Use annotations to highlight anomalies

3. Resolution (Insight/Recommendation):
   - What does the data tell us?
   - What action should be taken?
   - What is the expected impact?
   - Provide clear next steps
```

**Attention Guidance:**
```
✅ Lead with the key message (headline, not description)
✅ Visual hierarchy (size, color, position)
✅ Use annotations to highlight critical insights
✅ Progressive disclosure (overview → detail)
✅ Consistent reading pattern (Z-pattern, F-pattern)
✅ Call out what's important with color/size contrast
✅ Remove distractions (grays for background data)
```

**Context and Comparison:**
```
✅ Provide benchmarks (industry average, target, goal)
✅ Show trends over time (not just current state)
✅ Compare to similar entities or time periods
✅ Include sample sizes and confidence levels
✅ Show both absolute and relative changes
✅ Add reference lines (average, threshold, target)
```

**Actionability:**
```
✅ End with clear, specific recommendations
✅ Quantify expected impact ("reduce costs by 15%")
✅ Prioritize actions (what to do first)
✅ Assign accountability (who should act)
✅ Set timelines (when to implement)
✅ Define success metrics (how to measure)
```

**Progression Techniques:**
```
✅ Start with executive summary (1-slide/1-page)
✅ Provide detailed views on demand
✅ Use drill-down interactions (click for details)
✅ Layer complexity (simple → detailed)
✅ Offer multiple perspectives (time, geography, segment)
```

## Quality Checks

After visualization creation, perform these quality checks:

### 1. Visual Quality
```
- High resolution (300 DPI for print)
- Clear and readable text
- Consistent styling and colors
- Professional appearance
```

### 2. Data Accuracy
```
- Values match source data
- Calculations are correct
- Units are consistent
- Dates and time zones correct
```

### 3. Accessibility
```
- Colorblind-safe palettes
- Sufficient contrast
- Alt text provided
- Screen-reader friendly
```

### 4. Clarity
```
- Message is clear
- Labels are descriptive
- Legend is included
- Source is cited
```

## Version Control and Deployment

### Version Control Strategy

```
1. Dashboard Versioning:
   - Use semantic versioning (v1.0.0, v1.1.0, v2.0.0)
   - Tag releases in git
   - Maintain CHANGELOG.md with updates
   - Document breaking changes

2. A/B Testing:
   - Deploy new versions alongside existing
   - Route subset of users to new version
   - Collect usage metrics and feedback
   - Gradual rollout (10% → 50% → 100%)

3. Rollback Procedures:
   - Keep previous version accessible
   - Document rollback steps
   - Monitor for issues post-deployment
   - Have rollback criteria defined

4. Backup and Recovery:
   - Backup dashboard configurations
   - Export data sources and connections
   - Document dependencies and versions
   - Test recovery procedures
```

### Deployment Checklist

```
□ All tests passed (functional, performance, accessibility)
□ User acceptance testing completed
□ Documentation updated (user guide, technical docs)
□ Performance benchmarks meet targets
□ Security review completed (if applicable)
□ Data privacy compliance verified
□ Stakeholder sign-off obtained
□ Backup of previous version created
□ Monitoring and alerts configured
□ Support team trained on new features
□ Release notes prepared
□ Rollback plan documented
```

## Error Handling

If visualization creation encounters issues:

1. **Write detailed error log** to `logs/errors/visualization_{epic_id}_{timestamp}.log`

2. **Document the specific issue**:
   - Which visualization failed
   - Error message
   - Data issues encountered
   - Suggested remediation

3. **Common issues and solutions**:
   - Data too large: Implement aggregation or sampling
   - Slow performance: Add caching, optimize queries
   - Memory errors: Process data in chunks
   - Browser compatibility: Use polyfills or fallbacks
   - Missing data: Handle nulls gracefully, show empty states

## Success Criteria

The visualization and reporting is considered successful when:

- ✅ All required visualizations created and saved to `reports/figures/{epic_id}/`
- ✅ Interactive dashboards (if applicable) saved to `reports/dashboards/{epic_id}/`
- ✅ Reports and presentations saved to `reports/presentations/{epic_id}/`
- ✅ Visualization guide documented in `reports/{epic_id}/visualization_guide.md`
- ✅ All visualizations are high quality, accurate, and accessible
- ✅ Key findings clearly communicated with actionable recommendations
- ✅ Acceptance criteria from user story met
- ✅ All outputs verified and tested (Step 13 and 14)
- ✅ Performance targets met (load time <3s, interactions <500ms)
- ✅ Accessibility compliance achieved (WCAG 2.1 AA)
- ✅ User acceptance testing completed with positive feedback
- ✅ Cross-browser and device testing passed
- ✅ Documentation complete (technical and user guides)
- ✅ Version control and deployment plan in place

## Next Stage

After successful visualization, proceed to:
- **Stakeholder presentation**: Present findings to decision-makers
- **Implementation**: Act on recommendations
- **Monitoring**: Set up ongoing tracking and dashboards

## References

- Analysis Results: `results/{epic_id}/`
- Style Guide: `docs/style_guide.md` (if exists)
- User Story: `docs/objectives/user_stories/{epic_id}/`
- Project Structure: `README.md`
