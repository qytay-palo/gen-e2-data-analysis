# Extract Facility Capacity & Utilization Data (Lifecycle Stage: Data Extraction)

**Story ID**: PS-003-US-01  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (2 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Engineer supporting healthcare capacity planning**,  
I want **to extract facility capacity tables (inpatient beds, primary care clinics) and utilization data (hospital admissions) from the Kaggle health dataset**,  
So that **service planners have verified, complete capacity and utilization data for gap analysis and optimization modeling**.

---

## 🎯 Acceptance Criteria

1. **All capacity tables extracted successfully**
   - Downloaded: `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv` (180 records)
   - Downloaded: `health-facilities-primary-care-dental-clinics-and-pharmacies.csv` (96 records)
   - Downloaded: `residential-long-term-care-admissions.csv` (25 records)
   - Stored in `shared/data/1_raw/capacity/` with original file structure

2. **Utilization data extracted**
   - Downloaded: `hospital-admission-rate-by-age-and-sex.csv` (216 records, 2006-2020)
   - Stored in `shared/data/1_raw/utilization/`
   - Demographic stratification preserved: age groups, sex breakdowns

3. **Data validation passed**
   - Schema validation: required columns present (year, facility_type, sector, capacity, admissions)
   - Completeness: 0% missing values confirmed
   - Time coverage validated: inpatient facilities (2009-2020), admissions (2006-2020)
   - Row counts match expectations

4. **Extraction documented**
   - Validation log: `logs/etl/capacity_extraction_YYYYMMDD.log`
   - Schema documented: `shared/data/schemas/capacity_raw_schema.yml`
   - Test coverage: ≥80% for extraction functions

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY for data processing)
- **Extraction Method**: KaggleHub API with authentication
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-capacity-metrics) - Understanding capacity and occupancy metrics
- [Data Sources Documentation](../../../../project_context/data-sources.md#capacity-management) - Kaggle table specifications

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data processing and validation
- `pydantic>=2.5.0`: Schema validation
- `kagglehub>=0.2.0`: Kaggle dataset extraction
- `loguru>=0.7.0`: Structured logging
- `pyyaml>=6.0`: Configuration management

### Internal Dependencies
- **Upstream**: None (first story in epic)
- **Data Sources**: Kaggle dataset `subhamjain/health-dataset-complete-singapore`
- **Config Files**: `config/databricks.yml` (Kaggle credentials), `shared/config/base.yml`

---

## ✅ Implementation Tasks

### Data Extraction
- [ ] Configure KaggleHub authentication (reuse from PS-001)
- [ ] Create extraction script: `shared/src/data_processing/extract_capacity_data.py`
- [ ] Extract inpatient facility capacity table
- [ ] Extract primary care facilities table
- [ ] Extract long-term care admissions table
- [ ] Extract hospital admission rate table (utilization)
- [ ] Save to appropriate subdirectories: `1_raw/capacity/` and `1_raw/utilization/`

### Validation
- [ ] Define expected schemas in `shared/data/schemas/capacity_raw_schema.yml`
- [ ] Implement Pydantic models for schema validation
- [ ] Validate completeness: 0% missing values
- [ ] Validate row counts: inpatient (180), primary care (96), LTC (25), admissions (216)
- [ ] Validate year ranges: match expected coverage (2006-2020 or 2009-2020)
- [ ] Validate facility type categories: acute, community, nursing homes, clinics, etc.

### Quality Checks
- [ ] Check sector classifications: public, private, not-for-profit
- [ ] Validate capacity metrics: bed counts > 0
- [ ] Validate admission rates: realistic values (0-1000 per 100k population)
- [ ] Check demographic stratifications: age groups and sex categories present
- [ ] Generate validation report

### Testing & Documentation
- [ ] Unit tests for extraction functions
- [ ] Integration test for full extraction pipeline
- [ ] Validation test suite
- [ ] Mock KaggleHub API for testing
- [ ] Docstrings for all functions (Google style)
- [ ] Update documentation in `shared/src/data_processing/README.md`

---

## 📌 Notes

**Expected Capacity Tables** (from data-sources.md):
1. **Inpatient Facilities**: `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv`
   - 180 records, 2009-2020
   - Breakdowns: acute care, community hospitals, facility types
   
2. **Primary Care**: `health-facilities-primary-care-dental-clinics-and-pharmacies.csv`
   - 96 records
   - Includes: polyclinics, GP clinics, dental clinics, pharmacies

3. **Long-Term Care**: `residential-long-term-care-admissions.csv`
   - 25 records
   - Nursing homes and intermediate care

4. **Utilization**: `hospital-admission-rate-by-age-and-sex.csv`
   - 216 records, 2006-2020
   - Detailed age/sex stratification

**Polars Extraction Example**:
```python
import polars as pl
from loguru import logger
import kagglehub

# Download dataset
dataset_path = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore"
)

# Extract inpatient facilities
df_inpatient = pl.read_csv(
    f"{dataset_path}/health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private/health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv"
)

# Validate
assert df_inpatient.null_count().sum_horizontal()[0] == 0, "Found missing values"
logger.info(f"✓ Inpatient facilities extracted: {len(df_inpatient)} records")

# Save to raw directory
df_inpatient.write_csv("shared/data/1_raw/capacity/inpatient_facilities.csv")
```

**Schema Validation Template**:
```yaml
# shared/data/schemas/capacity_raw_schema.yml
inpatient_facilities:
  year: int32
  facility_type: string  # Acute care, Community hospitals, etc.
  sector: string  # Public, Private, Not-for-profit
  bed_count: int32
  facility_count: int32

hospital_admissions:
  year: int32
  age_group: string
  sex: string
  admission_rate: float64  # per 100,000 population
```

**Known Considerations**:
- Facility categorizations may vary across years (e.g., facility type naming changes)
- Some years may have incomplete sector breakdowns
- Long-term care data may be limited (only 25 records total)
- Admission rates are per 100,000 population (confirm rate base)
