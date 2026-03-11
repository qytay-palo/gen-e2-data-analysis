# Clean & Standardize 30-Year Mortality Datasets (Lifecycle Stage: Data Preparation)

**Story ID**: PS-002-US-02  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (3 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Engineer supporting disease burden analysis**,  
I want **to clean, standardize, and integrate the 30-year mortality datasets for cancer, stroke, and ischemic heart disease into a unified schema**,  
So that **public health analysts have consistent, validated, analysis-ready mortality data spanning 1990-2019 for temporal trend analysis**.

---

## 🎯 Acceptance Criteria

1. **Schema standardization completed**
   - All three disease datasets unified with consistent columns: `year`, `disease_category`, `mortality_rate`, `rate_per_100k`, `sex`, `age_group` (if available)
   - Disease names standardized: `cancer`, `stroke`, `ischemic_heart_disease`
   - Column naming convention: lowercase with underscores
   - Data types enforced: `year` as Int32, `mortality_rate` as Float64, `disease_category` as Categorical

2. **Data quality issues resolved**
   - Missing values validated: confirm 0% null values as expected
   - Data format inconsistencies corrected (e.g., varying decimal places, rate bases)
   - Year range validated: all datasets cover 1990-2019 (30 years)
   - Rate consistency verified: all rates confirm age-standardized per 100,000 population

3. **Integrated dataset created**
   - Output file: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
   - Format: Parquet (optimized for Polars)
   - Schema documented: `shared/data/schemas/mortality_integrated_schema.yml`
   - Total expected records: ~90 records (3 diseases × 30 years)

4. **Validation & documentation**
   - Data quality report: `shared/data/3_interim/mortality_cleaning_report.csv`
   - Cleaning log: `logs/etl/mortality_cleaning_YYYYMMDD.log`
   - Test coverage: ≥80% for cleaning and standardization functions

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY for data processing)
- **Schema Validation**: Pydantic 2.5+ for data model validation
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage for cleaning functions

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#age-standardized-mortality-rate-asmr) - Understanding ASMR calculations and standardization
- [Data Sources Documentation](../../../../project_context/data-sources.md#disease-burden-analysis) - Mortality table specifications

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data cleaning and schema standardization
- `pydantic>=2.5.0`: Schema validation models
- `loguru>=0.7.0`: Structured logging
- `pyyaml>=6.0`: Schema file parsing

### Internal Dependencies
- **Upstream**: PS-002-US-01 (Extract mortality data - BLOCKING)
- **Data Sources**: `shared/data/1_raw/mortality/*.csv`
- **Config Files**: `shared/config/base.yml` (data quality thresholds)

---

## ✅ Implementation Tasks

### Schema Standardization
- [ ] Define target schema in `shared/data/schemas/mortality_integrated_schema.yml`
- [ ] Create Pydantic model for unified mortality schema
- [ ] Load all three mortality CSV files using Polars
- [ ] Rename columns to standard naming convention (lowercase, underscores)
- [ ] Add `disease_category` column identifying each disease
- [ ] Standardize disease names: consistent naming across datasets
- [ ] Cast data types: year → Int32, mortality_rate → Float64, disease_category → Categorical

### Data Quality Validation
- [ ] Validate year range: assert all years 1990-2019 present for each disease
- [ ] Validate completeness: confirm 0% null values
- [ ] Validate rate consistency: check all rates are per 100,000 population
- [ ] Check for duplicates: no duplicate year-disease combinations
- [ ] Validate value ranges: mortality rates > 0 and < 1000 (sanity check)

### Data Integration
- [ ] Concatenate all three disease datasets vertically
- [ ] Sort by disease_category, year for consistent ordering
- [ ] Generate data profile: min/max rates, year coverage per disease
- [ ] Save integrated dataset to Parquet: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`

### Quality Reporting
- [ ] Generate cleaning report: records processed, issues found, corrections applied
- [ ] Save report to `shared/data/3_interim/mortality_cleaning_report.csv`
- [ ] Log cleaning summary to `logs/etl/mortality_cleaning_YYYYMMDD.log`
- [ ] Document schema in YAML format

### Testing & Validation
- [ ] Unit tests for schema standardization functions
- [ ] Integration test for full cleaning pipeline
- [ ] Validate output: correct schema, expected record counts
- [ ] Test edge cases: handling missing columns (if any), type mismatches
- [ ] Test coverage: `pytest --cov=shared/src/data_processing`

### Documentation
- [ ] Docstrings for all cleaning functions (Google style)
- [ ] Update `shared/src/data_processing/README.md` with cleaning workflow
- [ ] Document data transformations: before/after column mappings
- [ ] Create data dictionary entry for integrated dataset

---

## 📌 Notes

**Expected Mortality Tables** (from data-sources.md):
1. `age-standardised-mortality-rate-for-cancer.csv` (30 years, 1990-2019)
2. `age-standardised-mortality-rate-for-stroke.csv` (30 years, 1990-2019)
3. `age-standardised-mortality-rate-for-ischaemic-heart-disease.csv` (30 years, 1990-2019)

**Polars Cleaning Example**:
```python
import polars as pl
from loguru import logger

# Load and standardize cancer data
df_cancer = (
    pl.read_csv("shared/data/1_raw/mortality/cancer.csv")
    .rename(lambda col: col.lower().replace(' ', '_'))
    .with_columns([
        pl.lit('cancer').alias('disease_category'),
        pl.col('year').cast(pl.Int32),
        pl.col('mortality_rate').cast(pl.Float64),
        pl.col('disease_category').cast(pl.Categorical)
    ])
)

# Similar for stroke and ischemic heart disease
df_stroke = # ... similar processing
df_ihd = # ... similar processing

# Integrate all datasets
df_integrated = pl.concat([df_cancer, df_stroke, df_ihd])

# Validate
assert df_integrated.null_count().sum_horizontal()[0] == 0, "Found nulls"
assert len(df_integrated) == 90, f"Expected 90 records, got {len(df_integrated)}"

logger.info(f"✓ Integrated {len(df_integrated)} mortality records across 3 diseases")
```

**Unified Schema**:
```yaml
# shared/data/schemas/mortality_integrated_schema.yml
schema:
  year: int32
  disease_category: categorical  # cancer, stroke, ischemic_heart_disease
  mortality_rate: float64  # age-standardized rate per 100,000
  sex: string  # if available: male, female, total
  age_group: string  # if available: aggregated age groups
```

**Data Quality Checks**:
- Confirm all three diseases have exactly 30 records (1990-2019)
- Verify rates are positive and realistic (<500 per 100k for most diseases)
- Check year continuity: no missing years
- Validate age-standardized rates: should control for demographic changes

**Known Considerations**:
- Some datasets may have sex/age breakdowns - preserve if available
- Rate bases should be consistent (per 100,000 population)
- Disease naming may vary in source files - standardize to consistent values
