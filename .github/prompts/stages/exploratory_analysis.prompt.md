---
description: Data Analysis Stage with MCP Integration
stage: Analysis
---

# Stage Prompt: Data Analysis

## Objective

Perform comprehensive data analysis on prepared datasets to generate insights, answer research questions, and create visualizations.

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Prepared Data**: `data/4_processed/` or `data/3_interim/`
   - Clean, validated datasets ready for analysis
   - Documented schemas in `data/schemas/`

2. **Analysis Objectives**: From user story or `docs/objectives/`
   - Research questions to answer
   - Hypotheses to test
   - Metrics to calculate
   - Comparisons to perform

3. **Analysis Specifications**:
   - Required statistical tests
   - Visualization requirements
   - Target audience for outputs
   - Acceptance criteria from user story

4. **Project Context** (REQUIRED - read before analysis):
   - **Data dictionary**: `docs/data_dictionary/`
   - **Methodology**: `docs/methodology/`
   - **Business objectives**: `docs/project_context/business-objectives.md`
   - **Domain knowledge**: Review project context for domain-specific considerations
   - Previous analysis (if building on prior work)
   
   Read these files for understanding:
   - What the data represents and how to interpret it
   - What analysis methods are appropriate
   - What business questions to answer

## Output Requirements

The analysis MUST produce:

1. **Analysis Notebooks**: `notebooks/2_analysis/{epic_id}/`
   - Jupyter notebooks with complete analysis workflow
   - Markdown explanations and interpretations
   - Code cells with analysis logic
   - Inline visualizations

2. **Result Tables**: `results/tables/{epic_id}/`
   - Summary statistics (CSV/Excel)
   - Statistical test results
   - Aggregated metrics

3. **Visualizations**: `reports/figures/{epic_id}/`
   - Charts, plots, and graphs (PNG/PDF)
   - Interactive visualizations (HTML) if applicable
   - Properly labeled with titles, axis labels, legends

4. **Analysis Summary**: `results/{epic_id}/analysis_summary.md`
   - Key findings and insights
   - Statistical significance of results
   - Answers to research questions
   - Recommendations based on analysis

5. **Metrics Report**: `results/metrics/{epic_id}_metrics.json`
   - KPIs calculated
   - Performance metrics
   - Comparison metrics

## Execution Steps

### Step 1: Analysis Setup

```
1. Create analysis directories:
   - notebooks/2_analysis/{epic_id}/
   - results/tables/{epic_id}/
   - results/metrics/{epic_id}/
   - reports/figures/{epic_id}/

2. Read prepared data files from data/4_processed/

3. Read data schemas from data/schemas/

4. Read analysis objectives from user story or docs/objectives/
```

### Step 2: Exploratory Data Analysis

```
1. Load datasets from data/4_processed/

2. Perform initial exploration:
   - Data shape (rows, columns)
   - Summary statistics (mean, median, std, min, max)
   - Distribution analysis
   - Correlation analysis
   - Missing value patterns

3. Create exploratory visualizations:
   - Histograms for distributions
   - Scatter plots for relationships
   - Box plots for outliers
   - Heat maps for correlations

4. Save exploratory notebook to notebooks/2_analysis/{epic_id}/01_eda.ipynb
```

### Step 3: Statistical Analysis

```
1. Based on research questions, perform:
   - Descriptive statistics
   - Hypothesis testing (t-tests, chi-square, ANOVA, etc.)
   - Regression analysis (if applicable)
   - Time series analysis (if applicable)
   - Cluster analysis (if applicable)

2. Calculate p-values and confidence intervals

3. Interpret statistical significance

4. Save statistical test results to results/tables/{epic_id}/statistical_tests.csv
```

### Step 4: Metric Calculation

```
1. Calculate required KPIs and metrics:
   - Performance metrics (throughput, utilization, efficiency)
   - Quality metrics (accuracy, completeness, consistency)
   - Business metrics (cost, revenue, satisfaction)
   - Trend metrics (growth rates, change over time)

2. Aggregate by relevant dimensions (time, location, category)

3. Format metrics as JSON or CSV

4. Save to results/metrics/{epic_id}_metrics.json
```

### Step 5: Visualization Generation

```
1. Create publication-quality visualizations:
   - Time series plots (line charts, area charts)
   - Distribution plots (histograms, density plots, box plots)
   - Comparison plots (bar charts, grouped bar charts)
   - Relationship plots (scatter plots, regression lines)
   - Geographic plots (maps, heat maps) if applicable

2. Apply proper styling:
   - Clear titles and labels
   - Legends and annotations
   - Consistent color schemes
   - Appropriate scales and axes

3. Export visualizations in multiple formats:
   - PNG for reports (300 DPI)
   - PDF for publications
   - HTML for interactive dashboards (if applicable)

4. Save all figures to reports/figures/{epic_id}/
```

### Step 6: Insight Generation and Documentation

```
1. Synthesize findings into actionable insights:
   - What are the key patterns discovered?
   - What are the answers to research questions?
   - What are the statistically significant findings?
   - What are the practical implications?
   - What are the recommendations?

2. Create analysis summary document with:
   - Executive summary
   - Methodology overview
   - Key findings (with references to visualizations)
   - Statistical evidence
   - Limitations and caveats
   - Recommendations

3. Write analysis summary to results/{epic_id}/analysis_summary.md
```

### Step 7: Create Analysis Notebook

```
1. Consolidate analysis into a comprehensive Jupyter notebook:
   - Introduction and objectives
   - Data loading and preparation
   - Exploratory analysis with inline visualizations
   - Statistical tests with interpretations
   - Metric calculations
   - Final visualizations
   - Conclusions and recommendations

2. Add markdown cells explaining:
   - Methodology choices
   - Interpretation of results
   - Statistical significance
   - Business implications

3. Save final notebook to notebooks/2_analysis/{epic_id}/final_analysis.ipynb
```

### Step 8: Verification

```
1. Verify all required outputs were created:
   - List files in notebooks/2_analysis/{epic_id}/
   - List files in results/tables/{epic_id}/
   - List files in results/metrics/{epic_id}/
   - List files in reports/figures/{epic_id}/

2. Verify output quality:
   - Read analysis_summary.md and check completeness
   - Read metrics JSON and validate structure
   - Check that visualizations are properly saved (file size > 0)

3. Cross-check against acceptance criteria from user story

4. Document verification results
```

## Common Analysis Patterns

**IMPORTANT**: Adapt these patterns to your specific project objectives documented in `docs/objectives/`. Use MCP filesystem tools to read your project context.

### Pattern 1: Anomaly/Outlier Detection
**When to use**: Identify unusual patterns, early warning systems
**Methods**:
```
- Baseline pattern establishment (moving averages, seasonal decomposition)
- Anomaly detection models (Z-score, IQR, isolation forest)
- Geographic clustering (spatial analysis, hot spot detection)
- Temporal trend analysis (time series forecasting)
```
**Domain Examples**:
- Healthcare: Disease outbreak detection, patient deterioration
- Finance: Fraud detection, unusual transactions
- Manufacturing: Equipment failure prediction, quality anomalies
- Retail: Demand spikes, inventory shrinkage

### Pattern 2: Utilization/Efficiency Analysis
**When to use**: Optimize resource allocation, improve efficiency
**Methods**:
```
- Utilization rates (occupancy, throughput, capacity)
- Resource allocation efficiency (input-output ratios)
- Bottleneck identification (queue analysis, wait time distribution)
- Optimization scenarios (simulation, what-if analysis)
```
**Domain Examples**:
- Healthcare: Bed capacity, staff scheduling
- Manufacturing: Machine utilization, production efficiency
- IT: Server utilization, network capacity
- Retail: Store staffing, inventory turnover

### Pattern 3: Equity/Disparity Analysis
**When to use**: Identify gaps, ensure fairness, measure accessibility
**Methods**:
```
- Demographic distribution analysis
- Disparity metrics (geographic, socioeconomic, categorical)
- Comparative statistics (between groups, regions, time periods)
- Gap quantification and trend analysis
```
**Domain Examples**:
- Healthcare: Access equity, treatment disparities
- Education: Learning outcome gaps, resource allocation
- Finance: Credit access, lending fairness
- Public Services: Service availability, response times

### Pattern 4: Process/Flow Analysis
**When to use**: Improve processes, reduce bottlenecks, optimize flows
**Methods**:
```
- Journey/process mapping (step-by-step analysis)
- Wait time/latency analysis (by stage, by type)
- Flow efficiency metrics (throughput, cycle time, completion rate)
- Constraint identification (bottleneck detection)
```
**Domain Examples**:
- Healthcare: Patient flow, discharge planning
- Supply Chain: Order fulfillment, logistics
- Customer Service: Ticket resolution, escalation paths
- Manufacturing: Production line, assembly processes

## Quality Checks

After analysis, perform these quality checks:

### 1. Analytical Rigor
```
- Are statistical methods appropriate for the data and questions?
- Are assumptions of statistical tests checked and met?
- Are confidence intervals and p-values reported correctly?
- Are effect sizes calculated and interpreted?
```

### 2. Insight Quality
```
- Do findings directly answer the research questions?
- Are insights actionable and specific?
- Are limitations and caveats clearly stated?
- Are recommendations evidence-based?
```

### 3. Visualization Quality
```
- Are all charts properly labeled (title, axes, legend)?
- Are visualizations clear and easy to interpret?
- Are color schemes accessible and meaningful?
- Are scales and ranges appropriate?
```

### 4. Documentation Quality
```
- Is the analysis reproducible from the notebook?
- Are methodological choices explained?
- Are results interpreted in context?
- Is the summary comprehensive yet concise?
```

## Error Handling

If analysis encounters issues:

1. **Write detailed error log** to `logs/errors/analysis_{epic_id}_{timestamp}.log`

2. **Document the specific issue**:
   - Which analysis step failed
   - Error message and context
   - Data quality issues discovered
   - Suggested remediation

3. **Partial Results**:
   - If some analyses completed successfully, document which ones
   - Mark incomplete analyses clearly
   - Provide preliminary insights from available results

## Success Criteria

The analysis is considered successful when:

- ✅ All research questions addressed with statistical evidence
- ✅ Analysis notebooks created and saved to `notebooks/2_analysis/{epic_id}/`
- ✅ Result tables generated and saved to `results/tables/{epic_id}/`
- ✅ Visualizations created and saved to `reports/figures/{epic_id}/`
- ✅ Analysis summary document completed in `results/{epic_id}/analysis_summary.md`
- ✅ Metrics calculated and saved to `results/metrics/{epic_id}_metrics.json`
- ✅ Quality checks passed (analytical rigor, insight quality, visualization quality)
- ✅ Acceptance criteria from user story met
- ✅ All outputs verified

## Next Stage

After successful analysis, proceed to:
- **Visualization & Reporting** stage: Create stakeholder-ready reports and dashboards
- **Model Training** stage (if applicable): Build predictive or classification models
- **Statistical Analysis** stage (if deeper statistical analysis needed)

## References

- Analysis Objectives: `docs/objectives/user_stories/`
- Data Dictionary: `docs/data_dictionary/`
- Methodology: `docs/methodology/`
- Project Structure: `README.md`
