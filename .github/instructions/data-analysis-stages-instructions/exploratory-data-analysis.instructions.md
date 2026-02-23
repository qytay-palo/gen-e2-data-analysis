---
name: 'Exploratory Data Analysis (EDA) Standards'
description: 'Best practices for exploratory data analysis, initial profiling, and hypothesis generation'
applyTo: 'notebooks/1_exploratory/**, notebooks/2_analysis/*exploratory*.ipynb, src/analysis/*eda*.py, reports/figures/exploratory/**, docs/objectives/user_stories/**/*analyz*.md, docs/objectives/user_stories/**/*exploratory*.md, docs/objectives/user_stories/**/*quantif*.md'
---

## Purpose
This document defines **mandatory practices** for exploratory data analysis (EDA). Follow these guidelines when conducting initial data exploration, generating insights, and forming hypotheses.

## Core Principles

### 1. Structured Exploration
- **ALWAYS start with univariate analysis** before multivariate
- Progress systematically: distributions → relationships → patterns → insights
- Document findings and questions as you explore
- Generate reproducible visualizations

### 2. Hypothesis-Driven Investigation
- State questions explicitly before exploring
- Document expected vs actual findings
- Note surprising patterns for further investigation
- Connect findings back to business objectives

### 3. Reproducible Notebooks
- Use clear section headers and markdown explanations
- Include data loading, validation, and quality checks
- Save key visualizations to `reports/figures/`
- Export summary tables to `results/tables/`

## EDA Workflow Template

### Notebook Structure (MANDATORY)

```markdown
# Exploratory Data Analysis: [Dataset Name]

**Objective**: [Clearly state the purpose of this analysis]

**Date**: YYYY-MM-DD  
**Analyst**: [Your Name]  
**Data Source**: `path/to/data.csv` (Extraction Date: YYYY-MM-DD)

---

## 1. Setup and Data Loading

### 1.1 Import Libraries
### 1.2 Configure Environment
### 1.3 Load Data
### 1.4 Initial Validation

## 2. Data Overview

### 2.1 Dataset Dimensions
### 2.2 Column Types and Metadata
### 2.3 Missing Values Summary
### 2.4 Memory Usage

## 3. Univariate Analysis

### 3.1 Numeric Variables
### 3.2 Categorical Variables
### 3.3 Temporal Variables (Dates)

## 4. Bivariate Analysis

### 4.1 Numeric vs Numeric (Correlations)
### 4.2 Categorical vs Numeric
### 4.3 Categorical vs Categorical

## 5. Multivariate Analysis

### 5.1 Feature Interactions
### 5.2 Grouping and Aggregation
### 5.3 Time Series Patterns

## 6. Key Findings and Insights

### 6.1 Summary of Discoveries
### 6.2 Data Quality Issues
### 6.3 Hypotheses for Further Investigation
### 6.4 Recommendations for Data Cleaning

## 7. Next Steps

---
```

### Complete EDA Template Code

```python
# ============================================================================
# SECTION 1: SETUP AND DATA LOADING
# ============================================================================

# 1.1 Import Libraries
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
from datetime import datetime
from loguru import logger

# Configure plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Configure logger
logger.add('logs/analysis/eda_{time}.log', rotation="1 day")

# 1.2 Configure Paths
DATA_DIR = Path('data')
RAW_DIR = DATA_DIR / '1_raw'
FIGURES_DIR = Path('reports/figures/exploratory')
TABLES_DIR = Path('results/tables')

# Create output directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# 1.3 Load Data
logger.info("Loading disease surveillance data")

df = pl.read_csv(
    RAW_DIR / 'weekly-infectious-disease-bulletin-cases.csv',
    try_parse_dates=True
)

logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns")

# 1.4 Initial Validation
logger.info("Running initial validation checks")

# Check for expected columns
expected_columns = ['disease', 'epi_week', 'year', 'case_count']
missing_cols = set(expected_columns) - set(df.columns)

if missing_cols:
    logger.error(f"Missing expected columns: {missing_cols}")
else:
    logger.info("✓ All expected columns present")

# Check data types
logger.info(f"Column types:\n{df.dtypes}")

# ============================================================================
# SECTION 2: DATA OVERVIEW
# ============================================================================

print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)

# 2.1 Dataset Dimensions
print(f"\n📊 Dataset Dimensions:")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")
print(f"   Memory Usage: {df.estimated_size() / 1024 / 1024:.2f} MB")

# 2.2 Column Types
print(f"\n📋 Column Information:")
for col in df.columns:
    dtype = df[col].dtype
    null_count = df[col].null_count()
    null_pct = (null_count / len(df)) * 100
    unique_count = df[col].n_unique()
    
    print(f"   {col:20s} | {str(dtype):10s} | "
          f"Nulls: {null_count:6,} ({null_pct:5.2f}%) | "
          f"Unique: {unique_count:8,}")

# 2.3 Missing Values Summary
null_summary = df.null_count()
total_cells = len(df) * len(df.columns)
total_nulls = null_summary.sum_horizontal()[0]
null_percentage = (total_nulls / total_cells) * 100

print(f"\n❓ Missing Values:")
print(f"   Total Null Cells: {total_nulls:,} ({null_percentage:.2f}% of all cells)")

# Visualize missing values
fig, ax = plt.subplots(figsize=(10, 6))
null_counts = [df[col].null_count() for col in df.columns]
null_pcts = [(count / len(df)) * 100 for count in null_counts]

ax.barh(df.columns, null_pcts, color='coral')
ax.set_xlabel('Missing Values (%)')
ax.set_title('Missing Values by Column')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / '01_missing_values_summary.png', dpi=300, bbox_inches='tight')
plt.show()

logger.info(f"Saved: {FIGURES_DIR / '01_missing_values_summary.png'}")

# 2.4 First and Last Rows
print(f"\n🔍 First 5 Rows:")
print(df.head())

print(f"\n🔍 Last 5 Rows:")
print(df.tail())

# ============================================================================
# SECTION 3: UNIVARIATE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("UNIVARIATE ANALYSIS")
print("=" * 80)

# 3.1 Numeric Variables
numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Int64, pl.Float64, pl.Int32]]

print(f"\n📈 Numeric Variables Analysis:")

for col in numeric_cols:
    print(f"\n--- {col} ---")
    
    # Descriptive statistics
    stats = df[col].describe()
    print(stats)
    
    # Create distribution plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    values = df[col].drop_nulls().to_numpy()
    axes[0].hist(values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel(col)
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'Distribution of {col}')
    axes[0].grid(alpha=0.3)
    
    # Box plot
    axes[1].boxplot(values, vert=True)
    axes[1].set_ylabel(col)
    axes[1].set_title(f'Box Plot of {col}')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f'02_distribution_{col}.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info(f"Saved: {FIGURES_DIR / f'02_distribution_{col}.png'}")

# 3.2 Categorical Variables
categorical_cols = [col for col in df.columns if df[col].dtype == pl.Utf8]

print(f"\n📊 Categorical Variables Analysis:")

for col in categorical_cols:
    print(f"\n--- {col} ---")
    
    # Value counts
    value_counts = df[col].value_counts().sort('count', descending=True)
    print(f"Unique values: {df[col].n_unique()}")
    print(f"\nTop 10 values:")
    print(value_counts.head(10))
    
    # Visualize top categories
    if df[col].n_unique() <= 20:
        # Bar chart for reasonable number of categories
        fig, ax = plt.subplots(figsize=(12, 6))
        
        top_values = value_counts.head(15)
        categories = [row[0] for row in top_values.iter_rows()]
        counts = [row[1] for row in top_values.iter_rows()]
        
        ax.barh(categories, counts, color='teal', alpha=0.7)
        ax.set_xlabel('Count')
        ax.set_title(f'Distribution of {col}')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f'03_categorical_{col}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f"Saved: {FIGURES_DIR / f'03_categorical_{col}.png'}")

# 3.3 Temporal Variables
date_cols = [col for col in df.columns if df[col].dtype == pl.Date]

print(f"\n📅 Temporal Variables Analysis:")

for col in date_cols:
    print(f"\n--- {col} ---")
    
    min_date = df[col].min()
    max_date = df[col].max()
    date_range = (max_date - min_date).days if min_date and max_date else None
    
    print(f"Date Range: {min_date} to {max_date}")
    print(f"Span: {date_range} days")
    
    # Time series plot
    if date_range and date_range > 0:
        temporal_df = df.select([col]).drop_nulls()
        
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.hist(temporal_df[col].to_numpy(), bins=50, color='purple', alpha=0.6)
        ax.set_xlabel('Date')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {col}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f'04_temporal_{col}.png', dpi=300, bbox_inches='tight')
        plt.show()

# ============================================================================
# SECTION 4: BIVARIATE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("BIVARIATE ANALYSIS")
print("=" * 80)

# 4.1 Numeric vs Numeric: Correlation Matrix
if len(numeric_cols) >= 2:
    print(f"\n🔗 Correlation Matrix:")
    
    # Calculate correlations
    corr_df = df.select(numeric_cols).to_pandas().corr()
    print(corr_df)
    
    # Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, ax=ax)
    ax.set_title('Correlation Matrix')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / '05_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info(f"Saved: {FIGURES_DIR / '05_correlation_matrix.png'}")

# 4.2 Categorical vs Numeric: Group Statistics
print(f"\n📊 Categorical vs Numeric Analysis:")

# Example: Case count by disease
if 'disease' in df.columns and 'case_count' in df.columns:
    
    disease_stats = df.group_by('disease').agg([
        pl.col('case_count').count().alias('num_records'),
        pl.col('case_count').sum().alias('total_cases'),
        pl.col('case_count').mean().alias('mean_cases'),
        pl.col('case_count').median().alias('median_cases'),
        pl.col('case_count').std().alias('std_cases'),
        pl.col('case_count').min().alias('min_cases'),
        pl.col('case_count').max().alias('max_cases'),
    ]).sort('total_cases', descending=True)
    
    print("\nCase Statistics by Disease:")
    print(disease_stats)
    
    # Save summary table
    disease_stats.write_csv(TABLES_DIR / 'disease_summary_statistics.csv')
    logger.info(f"Saved: {TABLES_DIR / 'disease_summary_statistics.csv'}")
    
    # Visualize
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Total cases bar chart
    diseases = [row[0] for row in disease_stats.iter_rows()][:15]
    totals = [row[2] for row in disease_stats.iter_rows()][:15]
    
    axes[0].barh(diseases, totals, color='steelblue', alpha=0.7)
    axes[0].set_xlabel('Total Cases')
    axes[0].set_title('Total Cases by Disease (Top 15)')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Mean cases bar chart
    means = [row[3] for row in disease_stats.iter_rows()][:15]
    
    axes[1].barh(diseases, means, color='coral', alpha=0.7)
    axes[1].set_xlabel('Mean Weekly Cases')
    axes[1].set_title('Average Weekly Cases by Disease (Top 15)')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / '06_cases_by_disease.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info(f"Saved: {FIGURES_DIR / '06_cases_by_disease.png'}")

# ============================================================================
# SECTION 5: MULTIVARIATE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("MULTIVARIATE ANALYSIS")
print("=" * 80)

# 5.1 Time Series Patterns by Disease
if all(col in df.columns for col in ['year', 'disease', 'case_count']):
    
    print(f"\n📈 Time Series Analysis:")
    
    # Yearly trend by disease
    yearly_trend = df.group_by(['year', 'disease']).agg([
        pl.col('case_count').sum().alias('annual_cases')
    ]).sort(['disease', 'year'])
    
    # Get top diseases by total cases
    top_diseases = (
        df.group_by('disease')
        .agg(pl.col('case_count').sum().alias('total'))
        .sort('total', descending=True)
        .head(8)
    )
    
    top_disease_names = [row[0] for row in top_diseases.iter_rows()]
    
    # Plot time series for top diseases
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for disease in top_disease_names:
        disease_data = yearly_trend.filter(pl.col('disease') == disease)
        years = disease_data['year'].to_list()
        cases = disease_data['annual_cases'].to_list()
        
        ax.plot(years, cases, marker='o', label=disease, linewidth=2)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Annual Cases')
    ax.set_title('Temporal Trends by Disease (Top 8)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / '07_temporal_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info(f"Saved: {FIGURES_DIR / '07_temporal_trends.png'}")

# 5.2 Seasonal Patterns (if epi_week available)
if all(col in df.columns for col in ['epi_week', 'disease', 'case_count']):
    
    print(f"\n🌡️ Seasonal Pattern Analysis:")
    
    # Average cases by week across all years
    seasonal_pattern = df.group_by(['epi_week', 'disease']).agg([
        pl.col('case_count').mean().alias('avg_weekly_cases')
    ]).sort(['disease', 'epi_week'])
    
    # Plot for top diseases
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for disease in top_disease_names[:5]:  # Top 5 for clarity
        disease_data = seasonal_pattern.filter(pl.col('disease') == disease)
        weeks = disease_data['epi_week'].to_list()
        avg_cases = disease_data['avg_weekly_cases'].to_list()
        
        ax.plot(weeks, avg_cases, marker='.', label=disease, linewidth=2, alpha=0.7)
    
    ax.set_xlabel('Epidemiological Week')
    ax.set_ylabel('Average Weekly Cases')
    ax.set_title('Seasonal Patterns by Disease (Multi-Year Average)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(1, 53)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / '08_seasonal_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info(f"Saved: {FIGURES_DIR / '08_seasonal_patterns.png'}")

# ============================================================================
# SECTION 6: KEY FINDINGS
# ============================================================================

print("\n" + "=" * 80)
print("KEY FINDINGS AND INSIGHTS")
print("=" * 80)

findings = """
## Summary of Discoveries

1. **Dataset Coverage**
   - Time range: [INSERT DATE RANGE]
   - Number of diseases tracked: {n_diseases}
   - Total records: {n_records:,}

2. **Data Quality Observations**
   - Missing values: {null_pct:.2f}% of cells
   - Key issues: [DOCUMENT ANY ISSUES FOUND]

3. **Distribution Insights**
   - [DESCRIBE KEY DISTRIBUTIONAL FINDINGS]
   - [IDENTIFY OUTLIERS OR ANOMALIES]

4. **Temporal Patterns**
   - [DESCRIBE TRENDS OVER TIME]
   - [NOTE SEASONAL PATTERNS]

5. **Disease Burden**
   - Top diseases by case count: [LIST TOP 3-5]
   - Diseases with increasing trends: [IDENTIFY]
   - Diseases with decreasing trends: [IDENTIFY]

## Hypotheses for Further Investigation

1. [HYPOTHESIS 1 - e.g., "Dengue shows strong seasonal pattern - investigate climate correlations"]
2. [HYPOTHESIS 2]
3. [HYPOTHESIS 3]

## Recommendations for Data Cleaning

1. [CLEANING STEP 1 - e.g., "Handle missing values in X column using Y method"]
2. [CLEANING STEP 2]
3. [CLEANING STEP 3]

## Next Steps

1. Detailed time series decomposition for top diseases
2. Statistical testing of seasonal patterns
3. Correlation analysis with external factors (weather, demographics)
4. Develop forecasting models for high-burden diseases
"""

print(findings.format(
    n_diseases=df['disease'].n_unique() if 'disease' in df.columns else 'N/A',
    n_records=len(df),
    null_pct=(df.null_count().sum() / (len(df) * len(df.columns))) * 100
))

# Save findings to markdown file
findings_file = FIGURES_DIR / 'EDA_FINDINGS.md'
with open(findings_file, 'w') as f:
    f.write(f"# EDA Findings: {datetime.now().strftime('%Y-%m-%d')}\n\n")
    f.write(findings.format(
        n_diseases=df['disease'].n_unique() if 'disease' in df.columns else 'N/A',
        n_records=len(df),
        null_pct=(df.null_count().sum() / (len(df) * len(df.columns))) * 100
    ))

logger.info(f"Saved: {findings_file}")

print(f"\n✅ EDA Complete!")
print(f"   Figures saved to: {FIGURES_DIR}")
print(f"   Tables saved to: {TABLES_DIR}")
```

## EDA Best Practices

### 1. Always Visualize Before Analyzing

```python
# ❌ DON'T: Jump to conclusions from summary stats
mean_cases = df['case_count'].mean()
# Assume normal distribution

# ✅ DO: Visualize first, then interpret
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df['case_count'], bins=50)
plt.title('Distribution of Case Counts')

plt.subplot(1, 2, 2)
plt.boxplot(df['case_count'])
plt.title('Box Plot of Case Counts')
plt.show()

# Now interpret with visual context
```

### 2. Document Surprising Findings

```python
# Create findings log
findings_log = []

# During exploration
if outlier_count > 100:
    finding = {
        'type': 'outlier',
        'description': f'Found {outlier_count} outliers in case_count',
        'action_needed': 'Investigate data quality or real outbreak events'
    }
    findings_log.append(finding)
    logger.warning(finding['description'])

# Save findings at end
import json
with open('logs/analysis/eda_findings.json', 'w') as f:
    json.dump(findings_log, f, indent=2)
```

### 3. Use Interactive Visualizations for Exploration

```python
import plotly.express as px

# Interactive time series
fig = px.line(
    yearly_trend.to_pandas(),
    x='year',
    y='annual_cases',
    color='disease',
    title='Interactive Disease Trends Over Time',
    labels={'annual_cases': 'Annual Cases', 'year': 'Year'}
)

fig.update_layout(
    hovermode='x unified',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# Save as HTML for interactive exploration
fig.write_html(FIGURES_DIR / '09_interactive_trends.html')
logger.info(f"Saved: {FIGURES_DIR / '09_interactive_trends.html'}")

fig.show()
```

### 4. Statistical Testing for Patterns

```python
from scipy import stats

# Test for normality
def test_normality(data, variable_name):
    """Test if data follows normal distribution."""
    statistic, p_value = stats.shapiro(data)
    
    is_normal = p_value > 0.05
    
    logger.info(
        f"Normality test for {variable_name}: "
        f"p-value={p_value:.4f}, "
        f"Normal={'Yes' if is_normal else 'No'}"
    )
    
    return is_normal

# Apply to numeric columns
for col in numeric_cols:
    sample = df[col].drop_nulls().to_numpy()[:5000]  # Sample for large datasets
    test_normality(sample, col)
```

## EDA Checklist

Before moving to modeling or advanced analysis:

- [ ] **Data loaded and validated**: Schema matches expectations
- [ ] **Univariate analysis complete**: All variables profiled individually
- [ ] **Bivariate relationships explored**: Key correlations identified
- [ ] **Temporal patterns investigated**: Trends and seasonality documented
- [ ] **Outliers identified**: Extreme values investigated and documented
- [ ] **Missing values assessed**: Patterns in missing data understood
- [ ] **Visualizations saved**: Key charts exported to `reports/figures/`
- [ ] **Summary tables exported**: Statistical summaries saved to `results/tables/`
- [ ] **Findings documented**: Key insights and hypotheses written down
- [ ] **Data quality issues logged**: Problems noted for cleaning phase
- [ ] **Next steps defined**: Clear plan for subsequent analysis

## Anti-Patterns (AVOID)

```python
# ❌ DON'T: No documentation or context
df.head()
df.describe()
# What are we looking for? What did we find?

# ✅ DO: Document purpose and findings
"""
### Objective
Understand the distribution of weekly case counts to:
1. Identify typical range for forecasting
2. Detect outliers indicating potential data issues
3. Assess variability for model selection

### Findings
- Case counts range from 0 to 15,234
- Distribution is right-skewed (median=12, mean=45)
- 15 outliers > 1000 cases detected → Investigate as potential outbreak events
"""

# ❌ DON'T: Plot without saving or labels
plt.plot(x, y)
plt.show()

# ✅ DO: Proper labeling and saving
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(x, y, linewidth=2, color='steelblue')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Case Count', fontsize=12)
ax.set_title('Disease Cases Over Time', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('reports/figures/exploratory/cases_over_time.png', dpi=300)
plt.show()

# ❌ DON'T: Ignore data types
df.group_by('date').agg(pl.sum('cases'))  # Fails if 'date' is string

# ✅ DO: Validate and convert types first
df = df.with_columns(
    pl.col('date').str.strptime(pl.Date, '%Y-%m-%d')
)
df.group_by('date').agg(pl.sum('cases'))
```

## Summary

Effective EDA requires:
1. **Systematic approach**: Follow the univariate → bivariate → multivariate progression
2. **Visual inspection**: Always plot data before drawing conclusions
3. **Documentation**: Record findings, questions, and next steps
4. **Reproducibility**: Save visualizations and summary tables
5. **Critical thinking**: Question assumptions and investigate anomalies
