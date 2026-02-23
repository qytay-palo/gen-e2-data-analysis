---
name: moh-data-quality-assessment
description: Singapore MOH data quality standards and validation criteria for disease surveillance data
version: 1.0.0
applies_to: [ProfilingAgent, CleaningAgent]
tags: [singapore, moh, data-quality, healthcare, validation]
---

# MOH Data Quality Assessment Skill

## Overview
This skill provides Singapore Ministry of Health (MOH) specific data quality standards, validation rules, and assessment criteria for disease surveillance and healthcare capacity datasets.

## When to Use
- When profiling disease surveillance data
- Before cleaning/transforming MOH-sourced datasets
- When validating data against Singapore healthcare standards
- When calculating data quality scores

## MOH Data Quality Dimensions

### 1. Completeness (30% weight)
**Definition**: Percentage of required fields populated

**MOH Requirements**:
- **Mandatory fields** for disease surveillance: `date`, `disease_code`, `case_count`, `region`
- **Optional but recommended**: `age_group`, `gender`, `severity`, `postal_sector`

**Scoring**:
```python
completeness_score = (
    sum(1 for col in mandatory_fields if missing_pct[col] == 0) / 
    len(mandatory_fields) * 100
)
```

**Quality Gates**:
- ≥95%: Excellent
- 80-94%: Acceptable
- <80%: Unacceptable (flag for data source review)

### 2. Validity (25% weight)
**Definition**: Percentage of values passing domain rules

**MOH Validation Rules**:

#### Disease Codes
- Must match ICD-10-SG classification
- Notifiable diseases must be flagged (Dengue, COVID-19, HFMD, etc.)
- Valid codes: `A00-U99` (ICD-10 ranges)

```python
NOTIFIABLE_DISEASES = [
    'A90', 'A91',      # Dengue fever
    'B34.1',           # Hand, foot and mouth disease
    'U07.1',           # COVID-19
    'A15-A19',         # Tuberculosis
    # ... see MOH Infectious Diseases Act for complete list
]
```

#### Date Ranges
- Must be within valid reporting period (2012-present for historical analysis)
- Future dates not allowed
- Must be in ISO format: `YYYY-MM-DD`

#### Age Groups (MOH Standard Bins)
```python
VALID_AGE_GROUPS = [
    '0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
    '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
    '60-64', '65-69', '70-74', '75-79', '80-84', '85+'
]
```

#### Regions (Singapore Planning Areas/Clusters)
```python
VALID_REGIONS = [
    'Central', 'North', 'South', 'East', 'West',
    'North-East', 'South-East', 'South-West'
]
```

#### Case Counts
- Must be non-negative integers
- Outliers: >3 standard deviations from disease-specific mean flagged for review
- Zero counts acceptable (no cases reported)

### 3. Consistency (20% weight)
**Definition**: Data types and formats match expected schema

**MOH Schema Standards**:
```python
EXPECTED_SCHEMA = {
    'date': pl.Date,
    'disease_code': pl.Utf8,
    'disease_name': pl.Categorical,  # Use categorical for efficiency
    'case_count': pl.Int32,          # Int32 sufficient for Singapore population
    'region': pl.Categorical,
    'age_group': pl.Categorical,
    'severity': pl.Categorical,      # ['Mild', 'Moderate', 'Severe', 'Critical']
}
```

### 4. Uniqueness (15% weight)
**Definition**: Appropriate cardinality for each field

**Expected Cardinality**:
- `date + disease_code + region + age_group`: Should be unique (primary key)
- `disease_code`: ~50-100 unique values (common reportable diseases)
- `region`: 8 unique values (Singapore clusters)
- `age_group`: 18 unique values (standard bins)

**Validation**:
```python
# Check for duplicates
duplicates = df.groupby(['date', 'disease_code', 'region', 'age_group']).count()
duplicates = duplicates.filter(pl.col('count') > 1)

if len(duplicates) > 0:
    # Flag as data quality issue
    pass
```

### 5. Timeliness (10% weight)
**Definition**: Data freshness and reporting lag

**MOH Reporting Requirements**:
- Weekly surveillance data: Updated within 7 days of week end
- Monthly aggregates: Updated within 15 days of month end
- Data older than 6 months considered historical (lower timeliness score)

## Data Quality Scoring Formula

```python
def calculate_moh_quality_score(df: pl.DataFrame) -> dict:
    """
    Calculate MOH data quality score (0-100).
    
    Returns:
        dict with overall score and dimension scores
    """
    scores = {}
    
    # 1. Completeness (30%)
    mandatory_fields = ['date', 'disease_code', 'case_count', 'region']
    missing_rates = {col: df[col].null_count() / len(df) for col in mandatory_fields}
    completeness = (sum(1 for rate in missing_rates.values() if rate == 0) / 
                   len(mandatory_fields)) * 100
    scores['completeness_score'] = completeness
    
    # 2. Validity (25%)
    valid_dates = df.filter(
        (pl.col('date') >= pl.date(2012, 1, 1)) & 
        (pl.col('date') <= pl.date.today())
    ).height / len(df) * 100
    
    valid_regions = df.filter(
        pl.col('region').is_in(VALID_REGIONS)
    ).height / len(df) * 100
    
    validity = (valid_dates + valid_regions) / 2
    scores['validity_score'] = validity
    
    # 3. Consistency (20%)
    # Check actual vs expected dtypes
    correct_types = sum(
        1 for col, dtype in EXPECTED_SCHEMA.items()
        if col in df.columns and df[col].dtype == dtype
    ) / len(EXPECTED_SCHEMA) * 100
    scores['consistency_score'] = correct_types
    
    # 4. Uniqueness (15%)
    expected_rows = len(df)
    unique_rows = df.unique(subset=['date', 'disease_code', 'region', 'age_group']).height
    uniqueness = (unique_rows / expected_rows) * 100
    scores['uniqueness_score'] = uniqueness
    
    # 5. Timeliness (10%)
    max_date = df['date'].max()
    days_old = (pl.date.today() - max_date).days
    timeliness = max(0, 100 - (days_old / 180 * 100))  # Decay over 6 months
    scores['timeliness_score'] = timeliness
    
    # Overall score (weighted average)
    overall = (
        completeness * 0.30 +
        validity * 0.25 +
        correct_types * 0.20 +
        uniqueness * 0.15 +
        timeliness * 0.10
    )
    scores['overall_quality_score'] = round(overall, 1)
    
    return scores
```

## Critical Quality Gates

### Gate 1: Completeness Check
```python
if completeness_score < 95:
    critical_issues.append(
        f"Completeness below MOH standard: {completeness_score}% (required: ≥95%)"
    )
```

### Gate 2: Disease Code Validation
```python
invalid_codes = df.filter(
    ~pl.col('disease_code').str.contains(r'^[A-U]\d{2}(\.\d+)?$')
)
if len(invalid_codes) > 0:
    critical_issues.append(
        f"Invalid ICD-10-SG codes detected: {len(invalid_codes)} records"
    )
```

### Gate 3: Duplicate Detection
```python
duplicates = df.groupby(['date', 'disease_code', 'region', 'age_group']).count()
duplicates = duplicates.filter(pl.col('count') > 1)
if len(duplicates) > 0:
    critical_issues.append(
        f"Duplicate records found: {len(duplicates)} groups"
    )
```

## Recommended Cleaning Actions

Based on quality assessment, recommend specific actions:

```python
def recommend_cleaning_actions(quality_scores: dict, issues: dict) -> list:
    """Generate recommended cleaning actions based on quality assessment."""
    actions = []
    
    if quality_scores['completeness_score'] < 95:
        for col, missing_pct in issues['missing_values'].items():
            if missing_pct > 5:
                if col in ['age_group', 'gender']:
                    actions.append(f"impute_categorical: {col} (mode imputation)")
                elif col in ['case_count']:
                    actions.append(f"impute_numeric: {col} (median imputation)")
                else:
                    actions.append(f"drop_rows: {col} (critical field with high missingness)")
    
    if 'invalid_disease_codes' in issues:
        actions.append("standardize_disease_codes: Map to ICD-10-SG standard")
    
    if 'invalid_regions' in issues:
        actions.append("standardize_regions: Map to MOH regional clusters")
    
    if 'duplicates_found' in issues:
        actions.append("remove_duplicates: Keep most recent record per key")
    
    return actions
```

## Example Usage

```python
import polars as pl
from pathlib import Path

# Load data
df = pl.read_csv('data/3_interim/extracted_disease_data.csv')

# Calculate quality scores
scores = calculate_moh_quality_score(df)

# Generate quality report
quality_report = f"""
# MOH Data Quality Report

## Overall Quality Score: {scores['overall_quality_score']}/100

### Dimension Scores
- Completeness: {scores['completeness_score']}/100 (30% weight)
- Validity: {scores['validity_score']}/100 (25% weight)
- Consistency: {scores['consistency_score']}/100 (20% weight)
- Uniqueness: {scores['uniqueness_score']}/100 (15% weight)
- Timeliness: {scores['timeliness_score']}/100 (10% weight)

## Quality Assessment
{get_quality_assessment(scores['overall_quality_score'])}

## Recommended Actions
{chr(10).join(f'- {action}' for action in recommend_cleaning_actions(scores, issues))}
"""

# Save report
Path('results/tables/data_quality_report.md').write_text(quality_report)
```

## References
- [MOH Infectious Diseases Act](https://sso.agc.gov.sg/Act/IDA1976)
- [ICD-10-SG Classification](https://www.moh.gov.sg/hpp/doctors/guidelines/icd-10-sg)
- [MOH Data Standards](https://www.moh.gov.sg/resources-statistics)
- [Singapore Healthcare System Overview](https://www.healthhub.sg)
