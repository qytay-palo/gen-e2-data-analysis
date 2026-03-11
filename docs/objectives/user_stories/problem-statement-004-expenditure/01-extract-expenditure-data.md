# Extract National Health Expenditure & Financing Data (Lifecycle Stage: Data Extraction)

**Story ID**: PS-004-US-01  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P0 (Critical)  
**Effort Estimate**: S (2 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Data Engineer supporting healthcare financial analysis**,  
I want **to extract national health expenditure tables and financing data from the Kaggle dataset covering 2006-2018**,  
So that **financial analysts have validated expenditure data for cost driver identification and trend analysis**.

---

## 🎯 Acceptance Criteria

1. **Expenditure data extracted**
   - Downloaded: `government-health-expenditure.csv` (13 records, 2006-2018)
   - Stored in `shared/data/1_raw/expenditure/`
   - Metadata preserved including financial year information

2. **Optional supplementary data extracted**
   - Healthcare utilization data (for correlation analysis)
   - Demographic data (for per capita calculations)
   - Facility capacity data (for cost per bed analysis)

3. **Data validation passed**
   - Schema validation: required columns present (financial_year, expenditure, category)
   - Completeness: 0% missing values confirmed
   - Value ranges: expenditure amounts realistic (millions/billions SGD)
   - Time coverage: 2006-2018 confirmed

4. **Extraction documented**
   - Validation log: `logs/etl/expenditure_extraction_YYYYMMDD.log`
   - Schema documented: `shared/data/schemas/expenditure_raw_schema.yml`
   - Test coverage: ≥80%

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Extraction Method**: KaggleHub API
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#healthcare-expenditure-metrics) - Understanding expenditure categories
- [Data Sources](../../../../project_context/data-sources.md#financial-analysis) - Expenditure table specifications

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `pydantic>=2.5.0`, `kagglehub>=0.2.0`, `loguru>=0.7.0`, `pyyaml>=6.0`

### Internal Dependencies
- **Upstream**: None (first story in epic)
- **Data Sources**: Kaggle dataset `subhamjain/health-dataset-complete-singapore`
- **Config Files**: `config/databricks.yml`, `shared/config/base.yml`

---

## ✅ Implementation Tasks

### Data Extraction
- [ ] Configure KaggleHub authentication
- [ ] Create extraction script: `shared/src/data_processing/extract_expenditure_data.py`
- [ ] Extract government health expenditure table
- [ ] Extract supplementary tables for context (utilization, demographics)
- [ ] Save to `shared/data/1_raw/expenditure/`

### Validation
- [ ] Define expected schema in YAML
- [ ] Implement Pydantic validation models
- [ ] Validate completeness: 0% nulls
- [ ] Validate row count: 13 records expected
- [ ] Validate financial years: 2006-2018
- [ ] Validate expenditure amounts: positive values, realistic magnitudes

### Testing & Documentation
- [ ] Unit tests for extraction functions
- [ ] Integration test for pipeline
- [ ] Mock API for testing
- [ ] Docstrings (Google style)
- [ ] Update README

---

## 📌 Notes

**Expected Table** (from data-sources.md):
- `government-health-expenditure.csv`
- 13 years: 2006-2018
- Contains: financial year, expenditure categories, amounts

**Polars Extraction**:
```python
import polars as pl
from loguru import logger
import kagglehub

dataset_path = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore"
)

df_expenditure = pl.read_csv(
    f"{dataset_path}/government-health-expenditure/government-health-expenditure.csv"
)

assert df_expenditure.null_count().sum_horizontal()[0] == 0
logger.info(f"✓ Expenditure data extracted: {len(df_expenditure)} records")

df_expenditure.write_csv("shared/data/1_raw/expenditure/government_health_expenditure.csv")
```

**Known Considerations**:
- Financial year vs calendar year alignment (check documentation)
- Expenditure categories may include: operating costs, capital investments, subsidies
- Amounts may be in millions or billions SGD (verify units)
