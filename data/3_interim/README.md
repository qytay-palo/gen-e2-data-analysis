# Cleaned Interim Data Dictionary

**Last Updated**: 2026-02-23 15:01:13  
**Source**: User Story 2 - Data Cleaning and Standardization

## Overview

This directory contains cleaned and standardized workforce and capacity data ready for analysis.

## Files

### 1. workforce_clean.parquet

**Records**: 246  
**Time Span**: 2006-2019  
**Professions**: Doctor, Nurse, Pharmacist

**Schema**:

| Column | Type | Description | Nulls Allowed |
|--------|------|-------------|---------------|
| year | Int32 | Calendar year | No |
| sector | Categorical | Service sector (Public, Private, Not-for-Profit, Inactive) | No |
| profession | Categorical | Healthcare profession (Doctor, Nurse, Pharmacist) | No |
| count | Int32 | Workforce headcount | No |
| specialist_category | Categorical | For doctors: na, Specialists, Non-Specialists | Yes (only for non-doctors) |
| nurse_type | Categorical | For nurses: Registered Nurses, Enrolled Nurses, Registered Midwives | Yes (only for non-nurses) |
| source_table | String | Original data source | No |
| outlier_flag | Boolean | Flagged as statistical outlier (>3 stdev) | No |
| has_missing_values | Boolean | Row had missing values in raw data | No |

**Notes**:
- Sector values standardized from multiple variations
- "Inactive" sector represents "Not in Active Practice" workforce (exclude from capacity analysis)
- Outliers flagged but not removed (may represent real extremes)

### 2. capacity_clean.parquet

**Records**: 144  
**Time Span**: 2009-2020  
**Institution Types**: Hospital, Primary Care

**Schema**:

| Column | Type | Description | Nulls Allowed |
|--------|------|-------------|---------------|
| year | Int32 | Calendar year | No |
| institution_type | String | Type of institution | No |
| sector | Categorical | Service sector (Public, Private, Not-for-Profit) | Yes |
| institution_category | Categorical | Hospital or Primary Care | No |
| num_facilities | Int32 | Number of facilities | No |
| num_beds | Int32 | Number of hospital beds | Yes (only for hospitals) |
| source_table | String | Original data source | No |
| outlier_flag | Boolean | Flagged as statistical outlier (>3 stdev) | No |
| has_missing_values | Boolean | Row had missing values in raw data | No |

**Notes**:
- num_beds only populated for hospital data, null for primary care
- Sector may be null for some facility types

## Data Quality

**Completeness**: 100% for all critical fields  
**Duplicates**: 0 exact duplicates on key columns  
**Outliers**: Flagged using z-score method (threshold=3.0 std dev)

## Cleaning Operations Performed

1. **Column Standardization**: Renamed columns to snake_case
2. **Table Unification**: Combined profession-specific tables
3. **Data Type Optimization**: Int64 → Int32, sectors → Categorical
4. **Sector Standardization**: Mapped variations to canonical values
5. **Missing Value Handling**: Flagged (no imputation applied)
6. **Duplicate Removal**: Removed 0 exact duplicates
7. **Outlier Detection**: Flagged using z-score method

## Usage

```python
import polars as pl

# Load cleaned workforce data
workforce_df = pl.read_parquet('data/3_interim/workforce_clean.parquet')

# Load cleaned capacity data
capacity_df = pl.read_parquet('data/3_interim/capacity_clean.parquet')

# Filter active workforce only (exclude "Inactive")
active_workforce = workforce_df.filter(pl.col('sector') != 'Inactive')

# Get non-outlier records
clean_workforce = workforce_df.filter(~pl.col('outlier_flag'))
```

## Next Steps

This cleaned data is ready for:
- User Story 3: Exploratory Data Analysis
- User Story 4: Trend Analysis and Forecasting
- User Story 5: Workforce Capacity Dashboard

---

*Data cleaning completed: 2026-02-23 15:01:13*
