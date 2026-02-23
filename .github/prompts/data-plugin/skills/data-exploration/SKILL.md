---
name: data-exploration
description: Profile and explore datasets to understand their shape, quality, and patterns before analysis. Use when encountering a new dataset, assessing data quality, discovering column distributions, identifying nulls and outliers, or deciding which dimensions to analyze.
---

# Data Exploration Skill

Systematic methodology for profiling datasets, assessing data quality, discovering patterns, and understanding schemas.

## Data Profiling Methodology

### Phase 1: Structural Understanding

Before analyzing any data, understand its structure:

**Table-level questions:**
- How many rows and columns?
- What is the grain (one row per what)?
- What is the primary key? Is it unique?
- When was the data last updated?
- How far back does the data go?

**Column classification:**
Categorize each column as one of:
- **Identifier**: Unique keys, foreign keys, entity IDs
- **Dimension**: Categorical attributes for grouping/filtering (status, type, region, category)
- **Metric**: Quantitative values for measurement (revenue, count, duration, score)
- **Temporal**: Dates and timestamps (created_at, updated_at, event_date)
- **Text**: Free-form text fields (description, notes, name)
- **Boolean**: True/false flags
- **Structural**: JSON, arrays, nested structures

### Phase 2: Column-Level Profiling

For each column, compute:

**All columns:**
- Null count and null rate
- Distinct count and cardinality ratio (distinct / total)
- Most common values (top 5-10 with frequencies)
- Least common values (bottom 5 to spot anomalies)

**Numeric columns (metrics):**
```
min, max, mean, median (p50)
standard deviation
percentiles: p1, p5, p25, p75, p95, p99
zero count
negative count (if unexpected)
```

**String columns (dimensions, text):**
```
min length, max length, avg length
empty string count
pattern analysis (do values follow a format?)
case consistency (all upper, all lower, mixed?)
leading/trailing whitespace count
```

**Date/timestamp columns:**
```
min date, max date
null dates
future dates (if unexpected)
distribution by month/week
gaps in time series
```

**Boolean columns:**
```
true count, false count, null count
true rate
```

### Phase 3: Relationship Discovery

After profiling individual columns:

- **Foreign key candidates**: ID columns that might link to other tables
- **Hierarchies**: Columns that form natural drill-down paths (country > state > city)
- **Correlations**: Numeric columns that move together
- **Derived columns**: Columns that appear to be computed from others
- **Redundant columns**: Columns with identical or near-identical information

## Quality Assessment Framework

### Completeness Score

Rate each column:
- **Complete** (>99% non-null): Green
- **Mostly complete** (95-99%): Yellow -- investigate the nulls
- **Incomplete** (80-95%): Orange -- understand why and whether it matters
- **Sparse** (<80%): Red -- may not be usable without imputation

### Consistency Checks

Look for:
- **Value format inconsistency**: Same concept represented differently ("USA", "US", "United States", "us")
- **Type inconsistency**: Numbers stored as strings, dates in various formats
- **Referential integrity**: Foreign keys that don't match any parent record
- **Business rule violations**: Negative quantities, end dates before start dates, percentages > 100
- **Cross-column consistency**: Status = "completed" but completed_at is null

### Accuracy Indicators

Red flags that suggest accuracy issues:
- **Placeholder values**: 0, -1, 999999, "N/A", "TBD", "test", "xxx"
- **Default values**: Suspiciously high frequency of a single value
- **Stale data**: Updated_at shows no recent changes in an active system
- **Impossible values**: Ages > 150, dates in the far future, negative durations
- **Round number bias**: All values ending in 0 or 5 (suggests estimation, not measurement)

### Timeliness Assessment

- When was the table last updated?
- What is the expected update frequency?
- Is there a lag between event time and load time?
- Are there gaps in the time series?

## Pattern Discovery Techniques

### Distribution Analysis

For numeric columns, characterize the distribution:
- **Normal**: Mean and median are close, bell-shaped
- **Skewed right**: Long tail of high values (common for revenue, session duration)
- **Skewed left**: Long tail of low values (less common)
- **Bimodal**: Two peaks (suggests two distinct populations)
- **Power law**: Few very large values, many small ones (common for user activity)
- **Uniform**: Roughly equal frequency across range (often synthetic or random)

### Temporal Patterns

For time series data, look for:
- **Trend**: Sustained upward or downward movement
- **Seasonality**: Repeating patterns (weekly, monthly, quarterly, annual)
- **Day-of-week effects**: Weekday vs. weekend differences
- **Holiday effects**: Drops or spikes around known holidays
- **Change points**: Sudden shifts in level or trend
- **Anomalies**: Individual data points that break the pattern

### Segmentation Discovery

Identify natural segments by:
- Finding categorical columns with 3-20 distinct values
- Comparing metric distributions across segment values
- Looking for segments with significantly different behavior
- Testing whether segments are homogeneous or contain sub-segments

### Correlation Exploration

Between numeric columns:
- Compute correlation matrix for all metric pairs
- Flag strong correlations (|r| > 0.7) for investigation
- Note: Correlation does not imply causation -- flag this explicitly
- Check for non-linear relationships (e.g., quadratic, logarithmic)

## Schema Understanding and Documentation

### Schema Documentation Template

When documenting a dataset for team use:

```markdown
## Table: [schema.table_name]

**Description**: [What this table represents]
**Grain**: [One row per...]
**Primary Key**: [column(s)]
**Row Count**: [approximate, with date]
**Update Frequency**: [real-time / hourly / daily / weekly]
**Owner**: [team or person responsible]

### Key Columns

| Column | Type | Description | Example Values | Notes |
|--------|------|-------------|----------------|-------|
| user_id | STRING | Unique user identifier | "usr_abc123" | FK to users.id |
| event_type | STRING | Type of event | "click", "view", "purchase" | 15 distinct values |
| revenue | DECIMAL | Transaction revenue in USD | 29.99, 149.00 | Null for non-purchase events |
| created_at | TIMESTAMP | When the event occurred | 2024-01-15 14:23:01 | Partitioned on this column |

### Relationships
- Joins to `users` on `user_id`
- Joins to `products` on `product_id`
- Parent of `event_details` (1:many on event_id)

### Known Issues
- [List any known data quality issues]
- [Note any gotchas for analysts]

### Common Query Patterns
- [Typical use cases for this table]
```

### Schema Exploration Queries

When connected to a data warehouse, use these patterns to discover schema:

```sql
-- List all tables in a schema (PostgreSQL)
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Column details (PostgreSQL)
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'my_table'
ORDER BY ordinal_position;

-- Table sizes (PostgreSQL)
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Row counts for all tables (general pattern)
-- Run per-table: SELECT COUNT(*) FROM table_name
```

### Lineage and Dependencies

When exploring an unfamiliar data environment:

1. Start with the "output" tables (what reports or dashboards consume)
2. Trace upstream: What tables feed into them?
3. Identify raw/staging/mart layers
4. Map the transformation chain from raw data to analytical tables
5. Note where data is enriched, filtered, or aggregated

## Output Persistence Requirements

**CRITICAL**: All data exploration outputs MUST be saved to local directories following the project structure.

### Required Output Locations

1. **Figures and Visualizations**
   - Directory: `reports/figures/problem-statement-{num}/`
   - Format: PNG (300 dpi minimum) or PDF for publication quality
   - Naming: `{descriptive_name}_{timestamp}.png`
   - Example: `reports/figures/problem-statement-001/temporal_coverage_20260223_141530.png`

2. **Data Profiles and Summary Tables**
   - Directory: `results/tables/problem-statement-{num}/`
   - Format: CSV for data tables, Markdown for reports
   - Naming: `{profile_type}_{timestamp}.csv` or `{report_name}_{timestamp}.md`
   - Example: `results/tables/problem-statement-001/data_quality_summary_20260223_141530.csv`

3. **Analysis Results and Metrics**
   - Directory: `results/metrics/problem-statement-{num}/`
   - Format: CSV for metrics, JSON for structured results
   - Naming: `{metric_name}_{timestamp}.{csv|json}`
   - Example: `results/metrics/problem-statement-001/completeness_scores_20260223_141530.csv`

4. **Exploration Logs**
   - Directory: `logs/etl/`
   - Format: Markdown or plain text
   - Naming: `exploration_log_{timestamp}.md`
   - Example: `logs/etl/exploration_log_20260223_141530.md`

### Implementation Requirements for Notebooks and Scripts

When generating exploration code, ALWAYS include:

```python
# 1. Import datetime for timestamps
from datetime import datetime
from pathlib import Path

# 2. Define output directories
FIGURES_DIR = Path('reports/figures/problem-statement-{num}')
RESULTS_DIR = Path('results/tables/problem-statement-{num}')
METRICS_DIR = Path('results/metrics/problem-statement-{num}')

# 3. Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR.mkdir(parents=True, exist_ok=True)

# 4. Generate timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 5. Save outputs with confirmation
# For figures:
fig_path = FIGURES_DIR / f'temporal_coverage_{timestamp}.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved figure to: {fig_path}")

# For data tables:
data_path = RESULTS_DIR / f'quality_summary_{timestamp}.csv'
df_summary.write_csv(data_path)
print(f"✅ Saved data to: {data_path}")

# For metrics:
metrics_path = METRICS_DIR / f'completeness_scores_{timestamp}.csv'
metrics_df.write_csv(metrics_path)
print(f"✅ Saved metrics to: {metrics_path}")
```

### Output Verification

After generating exploration code, verify:

- ✅ All visualization cells include `plt.savefig()` calls
- ✅ All summary DataFrames have corresponding `.write_csv()` or `.write_excel()` calls
- ✅ All file paths use the correct problem-statement directory structure
- ✅ All output files include timestamps for versioning
- ✅ Confirmation messages are printed showing saved file paths
- ✅ Output directories are created with `mkdir(parents=True, exist_ok=True)`

### User-Facing Output Messages

Always provide clear feedback about saved outputs:

```
✅ Data exploration complete!

Outputs saved to:
📊 Figures:
  - reports/figures/problem-statement-001/temporal_coverage_20260223_141530.png
  - reports/figures/problem-statement-001/sector_distribution_20260223_141530.png
  
📈 Data Summaries:
  - results/tables/problem-statement-001/quality_summary_20260223_141530.csv
  - results/tables/problem-statement-001/completeness_report_20260223_141530.csv
  
📋 Metrics:
  - results/metrics/problem-statement-001/data_quality_metrics_20260223_141530.json
```
