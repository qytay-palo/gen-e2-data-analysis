---
description: Answer data questions -- from quick lookups to full analyses
argument-hint: "<question>"
---

# /analyze - Answer Data Questions

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Answer a data question, from a quick lookup to a full analysis to a formal report.

## Usage

```
/analyze <natural language question>
```

## Workflow

### 1. Understand the Question

Parse the user's question and determine:

- **Complexity level**:
  - **Quick answer**: Single metric, simple filter, factual lookup (e.g., "How many users signed up last week?")
  - **Full analysis**: Multi-dimensional exploration, trend analysis, comparison (e.g., "What's driving the drop in conversion rate?")
  - **Formal report**: Comprehensive investigation with methodology, caveats, and recommendations (e.g., "Prepare a quarterly business review of our subscription metrics")
- **Data requirements**: Which tables, metrics, dimensions, and time ranges are needed
- **Output format**: Number, table, chart, narrative, or combination

### 2. Gather Data

**If a data warehouse MCP server is connected:**

1. Explore the schema to find relevant tables and columns
2. Write SQL query(ies) to extract the needed data
3. Execute the query and retrieve results
4. If the query fails, debug and retry (check column names, table references, syntax for the specific dialect)
5. If results look unexpected, run sanity checks before proceeding

**If no data warehouse is connected:**

1. Ask the user to provide data in one of these ways:
   - Paste query results directly
   - Upload a CSV or Excel file
   - Describe the schema so you can write queries for them to run
2. If writing queries for manual execution, use the `sql-queries` skill for dialect-specific best practices
3. Once data is provided, proceed with analysis

### 3. Analyze

- Calculate relevant metrics, aggregations, and comparisons
- Identify patterns, trends, outliers, and anomalies
- Compare across dimensions (time periods, segments, categories)
- For complex analyses, break the problem into sub-questions and address each

### 4. Validate Before Presenting

Before sharing results, run through validation checks:

- **Row count sanity**: Does the number of records make sense?
- **Null check**: Are there unexpected nulls that could skew results?
- **Magnitude check**: Are the numbers in a reasonable range?
- **Trend continuity**: Do time series have unexpected gaps?
- **Aggregation logic**: Do subtotals sum to totals correctly?

If any check raises concerns, investigate and note caveats.

### 5. Present Findings

**For quick answers:**
- State the answer directly with relevant context
- Include the query used (collapsed or in a code block) for reproducibility

**For full analyses:**
- Lead with the key finding or insight
- Support with data tables and/or visualizations
- Note methodology and any caveats
- Suggest follow-up questions

**For formal reports:**
- Executive summary with key takeaways
- Methodology section explaining approach and data sources
- Detailed findings with supporting evidence
- Caveats, limitations, and data quality notes
- Recommendations and suggested next steps

### 6. Visualize Where Helpful

When a chart would communicate results more effectively than a table:

- Use the `data-visualization` skill to select the right chart type
- Generate a Python visualization or build it into an HTML dashboard
- Follow visualization best practices for clarity and accuracy

## Examples

**Quick answer:**
```
/analyze How many new users signed up in December?
```

**Full analysis:**
```
/analyze What's causing the increase in support ticket volume over the past 3 months? Break down by category and priority.
```

**Formal report:**
```
/analyze Prepare a data quality assessment of our customer table -- completeness, consistency, and any issues we should address.
```

## Tips

- Be specific about time ranges, segments, or metrics when possible
- If you know the table names, mention them to speed up the process
- For complex questions, Claude may break them into multiple queries
- Results are always validated before presentation -- if something looks off, Claude will flag it

## Output Persistence

**REQUIRED**: All analysis outputs MUST be saved to local directories following the project structure.

### Save Locations

1. **Analysis Results Tables**: `results/tables/problem-statement-{num}/analysis_results_{timestamp}.csv`
2. **Metrics and KPIs**: `results/metrics/problem-statement-{num}/metrics_{timestamp}.csv`
3. **Analysis Reports**: `results/tables/problem-statement-{num}/analysis_report_{timestamp}.md`
4. **Visualizations**: `reports/figures/problem-statement-{num}/analysis_{chart_type}_{timestamp}.png`

### Implementation Template

Include this pattern in all analysis code:

```python
from datetime import datetime
from pathlib import Path
import json

# Define output directories
RESULTS_DIR = Path('results/tables/problem-statement-{num}')
METRICS_DIR = Path('results/metrics/problem-statement-{num}')
FIGURES_DIR = Path('reports/figures/problem-statement-{num}')

# Create directories
for dir_path in [RESULTS_DIR, METRICS_DIR, FIGURES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Generate timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save analysis results
results_path = RESULTS_DIR / f'analysis_results_{timestamp}.csv'
results_df.write_csv(results_path)
print(f"✅ Saved analysis results to: {results_path}")

# Save metrics
metrics_path = METRICS_DIR / f'metrics_{timestamp}.json'
with open(metrics_path, 'w') as f:
    json.dump(metrics_dict, f, indent=2)
print(f"✅ Saved metrics to: {metrics_path}")

# Save visualizations
if creating_viz:
    fig_path = FIGURES_DIR / f'analysis_trend_{timestamp}.png'
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved visualization to: {fig_path}")
    plt.show()

# Save analysis report (for formal reports)
report_path = RESULTS_DIR / f'analysis_report_{timestamp}.md'
with open(report_path, 'w') as f:
    f.write(report_content)
print(f"✅ Saved analysis report to: {report_path}")
```

### Output Verification

After generating analysis code, verify:
- ✅ All result DataFrames have corresponding `.write_csv()` or `.write_excel()` calls
- ✅ All metrics are saved as JSON or CSV files
- ✅ All visualizations include `plt.savefig()` calls
- ✅ All file paths use the correct problem-statement directory structure
- ✅ All output files include timestamps for versioning
- ✅ Confirmation messages are printed showing saved file paths
- ✅ Output directories are created with `mkdir(parents=True, exist_ok=True)`

### User-Facing Output Messages

Always provide clear feedback about saved outputs:

```
✅ Analysis complete!

Results saved to:
📊 Analysis Results:
  - results/tables/problem-statement-001/analysis_results_20260223_141530.csv
  
📈 Metrics:
  - results/metrics/problem-statement-001/metrics_20260223_141530.json
  
📉 Visualizations:
  - reports/figures/problem-statement-001/analysis_trend_20260223_141530.png
  
📄 Report:
  - results/tables/problem-statement-001/analysis_report_20260223_141530.md
```
