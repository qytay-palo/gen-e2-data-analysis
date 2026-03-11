# Clean & Integrate Capacity and Utilization Datasets (Lifecycle Stage: Data Preparation)

**Story ID**: PS-003-US-02  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (4 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Engineer preparing capacity analysis datasets**,  
I want **to clean, standardize, and integrate facility capacity and utilization data into a unified schema with consistent facility categorizations**,  
So that **healthcare planners can perform integrated gap analysis comparing capacity supply against demand across all facility types**.

---

## 🎯 Acceptance Criteria

1. **Schema standardization completed**
   - Unified schema: `year`, `facility_category`, `sector`, `capacity_metric`, `utilization_metric`, `capacity_type`
   - Facility categorizations standardized: `acute_care`, `community_hospital`, `long_term_care`, `primary_care`
   - Sector names consistent: `public`, `private`, `not_for_profit`
   - Data types enforced: year→Int32, capacity→Int32, utilization_rate→Float64

2. **Data integration achieved**
   - Capacity and utilization joined on year and facility type
   - Missing utilization data flagged (some facility types may lack admission rates)
   - Sector-level aggregations created for macro-level analysis
   - Integrated dataset spans common time period (2009-2020 where overlapping)

3. **Data quality issues resolved**
   - Facility type naming variations standardized
   - Rate bases confirmed: admissions per 100k population
   - Duplicate records identified and removed
   - Completeness validated: expected records present for each year

4. **Output deliverables**
   - Integrated dataset: `shared/data/3_interim/capacity_utilization_integrated.parquet`
   - Schema documentation: `shared/data/schemas/capacity_integrated_schema.yml`
   - Cleaning report: `shared/data/3_interim/capacity_cleaning_report.csv`
   - Test coverage: ≥80%

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Schema Validation**: Pydantic 2.5+
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-capacity-metrics) - Understanding bed types and capacity metrics
- [Data Sources](../../../../project_context/data-sources.md#capacity-management) - Table schemas

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `pydantic>=2.5.0`, `loguru>=0.7.0`, `pyyaml>=6.0`

### Internal Dependencies
- **Upstream**: PS-003-US-01 (Extract capacity data - BLOCKING)
- **Data Sources**: `shared/data/1_raw/capacity/*.csv`, `shared/data/1_raw/utilization/*.csv`
- **Config Files**: `shared/config/base.yml`

---

## ✅ Implementation Tasks

### Schema Standardization
- [ ] Define unified schema in YAML
- [ ] Map source facility types to standard categories
- [ ] Standardize sector names (public/private/not-for-profit)
- [ ] Rename columns to consistent naming convention
- [ ] Cast data types appropriately

### Data Cleaning
- [ ] Handle facility type naming variations
- [ ] Validate capacity metrics: non-negative bed counts
- [ ] Validate utilization rates: realistic ranges
- [ ] Remove duplicates if any
- [ ] Flag missing utilization data for certain facility types

### Data Integration  
- [ ] Join capacity and utilization on year and facility category
- [ ] Create sector-level aggregations
- [ ] Calculate derived metrics: capacity per capita, utilization vs capacity ratio
- [ ] Handle non-overlapping years appropriately

### Output Generation
- [ ] Save integrated Parquet dataset
- [ ] Generate cleaning report (issues found, corrections made)
- [ ] Document schema in YAML
- [ ] Log processing summary

### Testing & Documentation
- [ ] Unit tests for cleaning functions
- [ ] Integration tests for full pipeline
- [ ] Validation tests for schema compliance
- [ ] Docstrings (Google style)

---

## 📌 Notes

**Polars Integration Example**:
```python
import polars as pl
from loguru import logger

# Load capacity data
df_capacity = pl.read_csv("shared/data/1_raw/capacity/inpatient_facilities.csv")

# Standardize facility types
facility_mapping = {
    'Acute Hospital Beds': 'acute_care',
    'Community Hospital Beds': 'community_hospital',
    # ... additional mappings
}

df_capacity = df_capacity.with_columns([
    pl.col('facility_type').map_dict(facility_mapping).alias('facility_category')
])

# Load utilization data
df_utilization = pl.read_csv("shared/data/1_raw/utilization/hospital_admissions.csv")

# Aggregate to facility level (sum across age/sex)
df_util_agg = df_utilization.group_by(['year', 'facility_category']).agg([
    pl.col('admission_rate').sum().alias('total_admission_rate')
])

# Join capacity and utilization
df_integrated = df_capacity.join(
    df_util_agg, 
    on=['year', 'facility_category'], 
    how='left'
)

logger.info(f"✓ Integrated {len(df_integrated)} capacity-utilization records")
```

**Facility Category Mapping**:
- **Acute Care**: General hospitals, specialist hospitals
- **Community Hospital**: Step-down care, rehab facilities
- **Long-Term Care**: Nursing homes, chronic sick facilities
- **Primary Care**: Polyclinics, GP clinics

**Known Challenges**:
- Admission rates may not map cleanly to all facility types
- Some facility types lack utilization metrics
- Sector breakdowns may be incomplete for certain years
