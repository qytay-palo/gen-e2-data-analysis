# Schema Correction Guide
**Date**: 2026-02-23  
**Applies to**: User Stories 3, 4, 5  
**Status**: MANDATORY corrections for implementation

---

## 📋 Executive Summary

During implementation plan validation, **critical schema mismatches** were discovered between the assumed data schemas in all three user story implementation plans and the actual cleaned data produced by User Story 2.

**This document provides the authoritative schema reference and correction mappings that MUST be used during implementation.**

---

## ✅ Actual Cleaned Data Schemas (AUTHORITATIVE)

### Workforce Data (`data/3_interim/workforce_clean.parquet`)

**Validated Schema** (10 columns):
```python
{
    'year': Int32,
    'sector': Categorical,           # Public, Private, Not-for-Profit, Inactive
    'specialist_category': Categorical,
    'count': Int32,                  # ✅ Workforce count
    'profession': Categorical,       # Doctors, Nurses, Pharmacists
    'source_table': String,
    'nurse_type': Categorical,       # null for non-nurses
    'has_missing_values': Boolean,
    'count_outlier': Boolean,
    'outlier_flag': Boolean
}
```

**Required Columns for Analysis** (minimal subset):
```python
['year', 'sector', 'profession', 'count']
```

**Status**: ✅ **NO CHANGES NEEDED** - Implementation plans already use correct column names

---

### Capacity Data (`data/3_interim/capacity_clean.parquet`)

**Validated Schema** (13 columns):
```python
{
    'year': Int32,
    'institution_type': String,      # ⚠️ NOT 'category'
    'facility_type_a': String,
    'sector': Categorical,           # Public, Private, Not-for-Profit
    'num_facilities': Int32,
    'num_beds': Int32,               # ⚠️ NOT 'count' (for hospital beds)
    'institution_category': String,
    'source_table': String,
    'facility_type_b': String,
    'has_missing_values': Boolean,
    'num_facilities_outlier': Boolean,
    'num_beds_outlier': Boolean,
    'outlier_flag': Boolean
}
```

**Required Columns for Analysis** (minimal subset for hospital beds):
```python
['year', 'sector', 'institution_type', 'num_beds']
```

**Status**: ❌ **CORRECTIONS REQUIRED** - See mapping table below

---

## 🔧 Required Corrections: Capacity Data Mappings

| **Assumed (INCORRECT)** | **Actual (CORRECT)** | **Usage Context** |
|-------------------------|----------------------|-------------------|
| `pl.col('category')` | `pl.col('institution_type')` | Filtering hospital data |
| `pl.col('count')` | `pl.col('num_beds')` | Hospital bed counts |
| `'category': Categorical` | `'institution_type': String` | Schema validation |
| `category == 'Hospital Beds'` | `institution_type == 'Hospital'` | Filter expression |
| `['year', 'sector', 'category', 'count']` | `['year', 'sector', 'institution_type', 'num_beds']` | Required columns list |

**Critical Note**: `institution_type` is a Polars string column (not categorical), while the original plans assumed `category` would be categorical.

---

## 📊 Validated Data Availability

### Hospital Beds Data (Primary Use Case)

**Filtering Expression**:
```python
# ❌ INCORRECT (original plans)
capacity_df.filter(pl.col('category') == 'Hospital Beds')

# ✅ CORRECT (actual schema)
capacity_df.filter(pl.col('institution_type') == 'Hospital')
```

**Validated Counts**:
- **Total hospital records**: 36 (covering 2009-2020)
- **Sectors available**: Public, Private, Not-for-Profit
- **Total beds (2019)**: 11,321
- **Year range**: 2009-2020 (12 years)

**Aggregation Example**:
```python
# ❌ INCORRECT
hospital_beds = capacity_df.filter(
    pl.col('category') == 'Hospital Beds'
).group_by(['year', 'sector']).agg([
    pl.col('count').sum().alias('total_beds')
])

# ✅ CORRECT
hospital_beds = capacity_df.filter(
    pl.col('institution_type') == 'Hospital'
).group_by(['year', 'sector']).agg([
    pl.col('num_beds').sum().alias('total_beds')
])
```

### Other Institution Types Available

```python
institution_types = [
    'Hospital',                      # Primary focus for this analysis
    'Primary Care Facilities',       # Future scope
    'Dental Clinics',                # Future scope
    'Pharmacies',                    # Future scope
    'Residential Long-Term'          # Future scope
]
```

**For User Stories 3-5**: Only `institution_type == 'Hospital'` is in scope.

---

## 🔍 Impact Assessment by User Story

### User Story 3: Exploratory Analysis

**Files Affected**:
- Implementation plan section "2.2 Data Integration & Preparation"
- Function: `create_comparative_dataset()`
- Validation rules section

**Lines to Correct**:
1. **Line 332**: Schema documentation - change `category` → `institution_type`, `count` → `num_beds`
2. **Line 579**: Filter expression - change `pl.col('category') == 'Hospital Beds'` → `pl.col('institution_type') == 'Hospital'`
3. **Line 582**: Aggregation - change `pl.col('count')` → `pl.col('num_beds')`
4. **Line 1285**: Required columns array - update to `['year', 'sector', 'institution_type', 'num_beds']`
5. **Line 1314**: Categorical values validation - change to `'institution_type': {'values': ['Hospital', 'Primary Care Facilities', ...]}`
6. **Line 1474**: Test fixtures - update mock data to use `institution_type` and `num_beds`

**Estimated Changes**: ~8-10 code blocks

---

### User Story 4: Workforce-Capacity Metrics

**Files Affected**:
- Implementation plan section "2.1 Data Integration Requirements"
- Function: `calculate_all_workforce_capacity_ratios()`
- Function: `calculate_mismatch_index()`

**Lines to Correct**:
1. **Line 346**: Schema documentation - change `category` → `institution_type`, `count` → `num_beds`
2. **Line 474**: Filter expression in `calculate_all_workforce_capacity_ratios()`
3. **Line 477**: Aggregation - change `pl.col('count')` → `pl.col('num_beds')`
4. **Line 546**: Filter expression in `calculate_mismatch_index()`
5. **Line 549**: Aggregation - change aggregation column
6. **Line 1216**: Test fixtures - update mock data

**Estimated Changes**: ~8-10 code blocks

---

### User Story 5: Interactive Dashboard

**Files Affected**:
- Implementation plan section "2. Data Integration Requirements"
- Module: `data_loader.py`
- Dashboard main page (KPI metrics)

**Lines to Correct**:
1. **Line 401**: Schema documentation
2. **Line 1126**: Dashboard KPI calculation - update filter and column reference

**Estimated Changes**: ~5-8 code blocks

---

## ✅ Validation Checklist for Implementation

Before marking any user story as "complete", verify:

- [ ] All capacity data filters use `pl.col('institution_type')` NOT `pl.col('category')`
- [ ] All bed count aggregations use `pl.col('num_beds')` NOT `pl.col('count')`
- [ ] All hospital filters use `institution_type == 'Hospital'` NOT `category == 'Hospital Beds'`
- [ ] Schema validation dictionaries updated to reflect actual column names
- [ ] Test fixtures updated with correct column names
- [ ] Data pipeline documentation updated
- [ ] All imports execute without errors
- [ ] All code blocks execute without `ColumnNotFoundError`

---

## 📝 Example Code Corrections

### Before (INCORRECT)
```python
def load_capacity_data(file_path: str) -> pl.DataFrame:
    """Load and validate capacity data."""
    df = pl.read_parquet(file_path)
    
    # Validate schema
    required_cols = ['year', 'sector', 'category', 'count']
    assert all(col in df.columns for col in required_cols)
    
    # Filter to hospital beds
    hospital_beds = df.filter(pl.col('category') == 'Hospital Beds')
    
    # Aggregate by sector and year
    return hospital_beds.group_by(['year', 'sector']).agg([
        pl.col('count').sum().alias('total_beds')
    ])
```

### After (CORRECT)
```python
def load_capacity_data(file_path: str) -> pl.DataFrame:
    """Load and validate capacity data."""
    df = pl.read_parquet(file_path)
    
    # Validate schema
    required_cols = ['year', 'sector', 'institution_type', 'num_beds']
    assert all(col in df.columns for col in required_cols)
    
    # Filter to hospitals
    hospital_beds = df.filter(pl.col('institution_type') == 'Hospital')
    
    # Aggregate by sector and year
    return hospital_beds.group_by(['year', 'sector']).agg([
        pl.col('num_beds').sum().alias('total_beds')
    ])
```

---

## 🚨 MANDATORY Action Items

**BEFORE starting implementation of User Stories 3, 4, or 5:**

1. ✅ Read this schema correction guide completely
2. ✅ Review the implementation plan for your user story
3. ✅ Identify ALL instances of incorrect column references
4. ✅ Update code blocks with correct column names
5. ✅ Test code execution with actual data files
6. ✅ Verify no `ColumnNotFoundError` exceptions
7. ✅ Update test fixtures to match actual schema

**Code review focus**: Search for any string containing `'category'` or `'Hospital Beds'` in capacity-related code - these are likely errors.

---

## 📚 References

- **Validation Report**: [IMPLEMENTATION_PLAN_VALIDATION_REPORT.md](IMPLEMENTATION_PLAN_VALIDATION_REPORT.md)
- **Actual Data Files**: 
  - `data/3_interim/workforce_clean.parquet`
  - `data/3_interim/capacity_clean.parquet`
- **User Story 2** (Data Cleaning): Produced these schemas
- **Validation Date**: 2026-02-23
- **Validator**: GitHub Copilot (Claude Sonnet 4.5)

---

**End of Schema Correction Guide**
