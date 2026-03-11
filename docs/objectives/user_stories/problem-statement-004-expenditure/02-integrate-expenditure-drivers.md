# Integrate Expenditure with Utilization & Demographics (Lifecycle Stage: Data Preparation)

**Story ID**: PS-004-US-02  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (5 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Engineer preparing cost analysis datasets**,  
I want **to integrate expenditure data with utilization metrics (admissions) and demographic data (population, age structure) into a unified analytical dataset**,  
So that **financial analysts can perform driver analysis correlating costs with utilization patterns and population characteristics**.

---

## 🎯 Acceptance Criteria

1. **Data integration completed**
   - Expenditure joined with utilization data on year/financial_year
   - Population data integrated for per capita calculations
   - Demographic age structure data joined for aging impact analysis
   - Common time period established (2006-2018 overlap)

2. **Derived metrics calculated**
   - Per capita expenditure: total expenditure / population
   - Cost per admission: expenditure / total admissions
   - Expenditure growth rate: YoY % change
   - Age-adjusted expenditure: controlling for demographic changes

3. **Data quality ensured**
   - Year/financial year alignment validated
   - Missing data identified and documented
   - Unit consistency: all monetary values in same currency (SGD)
   - Duplicates removed

4. **Output deliverables**
   - Integrated dataset: `shared/data/3_interim/expenditure_drivers_integrated.parquet`
   - Schema documentation: `shared/data/schemas/expenditure_integrated_schema.yml`
   - Integration report: documented joins and derived metrics
   - Test coverage: ≥80%

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#expenditure-analysis-methods) - Cost driver analysis frameworks
- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objective-2) - Integration objectives

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `pydantic>=2.5.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-01 (Extract expenditure - BLOCKING)
- **Data Sources**: 
  - `shared/data/1_raw/expenditure/*.csv`
  - `shared/data/1_raw/utilization/*.csv` (from PS-003)
  - Population data (may need external source or derive from admission rate denominators)
- **Config Files**: `shared/config/base.yml`

---

## ✅ Implementation Tasks

### Data Integration
- [ ] Load expenditure, utilization, and demographic datasets
- [ ] Align financial_year with calendar year (resolve any offset)
- [ ] Join expenditure with utilization on year
- [ ] Join with population/demographic data
- [ ] Filter to common time period: 2006-2018

### Derived Metrics
- [ ] Calculate per capita expenditure
- [ ] Calculate cost per admission
- [ ] Calculate YoY expenditure growth rate
- [ ] Age-adjust expenditure (if age structure data available)
- [ ] Calculate expenditure per bed (using capacity data)

### Data Quality
- [ ] Validate year alignment across sources
- [ ] Check for missing data and document
- [ ] Ensure unit consistency (all SGD, same year basis)
- [ ] Remove any duplicates

### Output & Documentation
- [ ] Save integrated Parquet dataset
- [ ] Document schema in YAML
- [ ] Generate integration report: joins performed, metrics derived
- [ ] Log integration summary

### Testing
- [ ] Unit tests for join logic
- [ ] Validate derived metrics with sample calculations
- [ ] Integration test for full pipeline
- [ ] Docstrings

---

## 📌 Notes

**Polars Integration Example**:
```python
import polars as pl

df_exp = pl.read_csv("shared/data/1_raw/expenditure/government_health_expenditure.csv")
df_util = pl.read_csv("shared/data/1_raw/utilization/hospital_admissions.csv")

# Aggregate utilization to annual level
df_util_agg = df_util.group_by('year').agg([
    pl.col('admission_rate').sum().alias('total_admissions')
])

# Join expenditure and utilization
df_integrated = df_exp.join(df_util_agg, 
    left_on='financial_year', right_on='year', how='inner')

# Calculate per capita expenditure (assuming population column exists)
df_integrated = df_integrated.with_columns([
    (pl.col('total_expenditure') / pl.col('population')).alias('per_capita_expenditure')
])

# Calculate cost per admission
df_integrated = df_integrated.with_columns([
    (pl.col('total_expenditure') / pl.col('total_admissions')).alias('cost_per_admission')
])
```

**Known Challenges**:
- Financial year may differ from calendar year (e.g., Apr-Mar vs Jan-Dec)
- Population data may need to be sourced externally or derived
- Admission rates vs absolute admissions conversion needed
