# Extract & Validate Mortality Rate Data (Lifecycle Stage: Data Extraction)

**Story ID**: PS-002-US-01  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (2 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Data Analyst**,  
I want **to extract and validate 30-year mortality rate tables for cancer, stroke, and ischemic heart disease from the Kaggle dataset**,  
So that **epidemiologists have verified age-standardized mortality data spanning 1990-2019 for temporal trend analysis**.

---

## 🎯 Acceptance Criteria

1. **All mortality tables extracted**
   - `age-standardised-mortality-rate-for-cancer.csv` (30 years, 1990-2019)
   - `age-standardised-mortality-rate-for-stroke.csv` (30 years)
   - `age-standardised-mortality-rate-for-ischaemic-heart-disease.csv` (30 years)
   - Stored in `shared/data/1_raw/mortality/`

2. **Data quality validation passed**
   - 100% completeness verified (no missing values)
   - Year range: 1990-2019 (30 continuous years)
   - Age-standardized rates validated (rates per 100,000 population)
   - Schema validation: required columns (year, disease, mortality_rate, gender)

3. **Data output documented**
   - Output files: 3 CSV files in `shared/data/1_raw/mortality/`
   - Schema documented: `shared/data/schemas/mortality_raw_schema.yml`
   - Validation report: `logs/etl/mortality_extraction_YYYYMMDD.log`

4. **Validation tests passed**
   - Test coverage: ≥80% for extraction functions
   - Integration test: end-to-end extraction pipeline

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Extraction**: KaggleHub API
- **Logging**: loguru
- **Testing**: pytest with ≥80% coverage

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#4-age-standardized-mortality-rate-asmr) - Understanding ASMR methodology
- [Data Sources](../../../../project_context/data-sources.md) - Disease burden tables specifications

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data processing
- `kagglehub>=0.2.0`: Kaggle extraction
- `pydantic>=2.5.0`: Schema validation
- `loguru>=0.7.0`: Logging
- `pyyaml>=6.0`: Configuration

### Internal Dependencies
- **Upstream**: None (first story)
- **Data Sources**: Kaggle dataset `subhamjain/health-dataset-complete-singapore`
- **Config Files**: `config/databricks.yml` (Kaggle credentials)

---

## ✅ Implementation Tasks

### Data Extraction
- [ ] Configure KaggleHub authentication
- [ ] Create extraction script: `shared/src/data_processing/extract_mortality_data.py`
- [ ] Extract 3 mortality rate tables using KaggleHub API
- [ ] Save to `shared/data/1_raw/mortality/` with timestamps

### Validation
- [ ] Define schema: `shared/data/schemas/mortality_raw_schema.yml`
- [ ] Validate completeness (0% missing values)
- [ ] Validate year range (1990-2019, continuous)
- [ ] Validate rate ranges (positive values, realistic magnitudes)
- [ ] Generate validation report

### Testing & Validation
- [ ] Unit tests for extraction functions
- [ ] Integration test for full pipeline
- [ ] Mock KaggleHub for unit tests
- [ ] Validation test suite for schema compliance

### Documentation
- [ ] Docstrings (Google style)
- [ ] Update `shared/src/data_processing/README.md`
- [ ] Document schema in YAML
- [ ] Log extraction summary

---

## 📌 Notes

**Expected Tables**:
- Cancer mortality: 30 records (annual 1990-2019)
- Stroke mortality: 30 records
- Heart disease mortality: 30 records

**Polars Validation**:
```python
import polars as pl

df = pl.read_csv("shared/data/1_raw/mortality/mortality-cancer.csv")
assert df.null_count().sum_horizontal()[0] == 0
assert df['year'].min() == 1990 and df['year'].max() == 2019
logger.info(f"✓ Cancer mortality validated: {len(df)} records")
```

**Age-Standardization Note**: Data is already age-standardized by MOH (per 100,000 population), enabling valid temporal comparisons without demographic adjustment.
