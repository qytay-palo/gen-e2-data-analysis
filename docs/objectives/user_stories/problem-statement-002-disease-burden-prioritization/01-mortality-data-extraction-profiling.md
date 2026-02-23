# User Story 1: Disease Mortality Data Extraction and Profiling

**As a** public health analyst,  
**I want** to extract and profile age-standardized mortality data for major diseases from the Kaggle dataset,  
**so that** I can assess data completeness, temporal coverage, and establish a reliable foundation for disease burden analysis.

## 1. 🎯 Acceptance Criteria

- Mortality datasets successfully loaded for major diseases: cancer, stroke, ischemic heart disease (1990-2019)
- Age-standardized mortality rate (ASMR) data validated for correct standardization methodology
- Demographic breakdowns (age, gender) extracted where available
- Data profiling report generated showing:
  - Temporal coverage by disease (year ranges)
  - Data completeness (missing value percentages by disease and year)
  - Demographic segmentation availability
  - Disease classification consistency
- Data quality issues documented with frequency and impact assessment
- Raw mortality data saved to `data/1_raw/` with audit trail
- Data quality report saved to `logs/etl/data_quality_report_mortality_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient data loading and profiling
- **Platform**: Local Python environment (dataset <4MB)
- **Data Source**: Kaggle health-dataset-complete-singapore via kagglehub API
- **Documentation**: All operations logged using loguru
- **Output Format**: CSV for raw data with schema documentation

## 3. 📚 Domain Knowledge References

- [Disease Burden and Mortality Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md) - Understand ASMR, burden metrics, disease classification
- [Disease Burden Metrics](../../../domain_knowledge/disease-burden-mortality-analysis.md#disease-burden-metrics) - Standard metrics for disease burden quantification
- [Data Dictionary - Mortality Tables](../../../data_dictionary/) - Field-level mortality data documentation

## 4. 📦 Dependencies

**External Packages:**
- **kagglehub**: Kaggle dataset extraction
- **polars**: DataFrame processing and profiling
- **loguru**: Structured logging
- **pyyaml**: Configuration loading

**Internal Dependencies:**
- `src/utils/config_loader.py`: Load analysis configuration
- `src/utils/logger.py`: Logging setup
- `src/data_processing/base_connection.py`: Base connection pattern

## 5. ✅ Implementation Tasks

### Data Source Identification
- ⬜ Identify mortality data tables in Kaggle dataset
- ⬜ Document table names for cancer, stroke, heart disease mortality
- ⬜ Verify ASMR standardization methodology in metadata
- ⬜ Check demographic breakdown availability (age groups, gender)

### Data Extraction
- ⬜ Configure Kaggle API authentication
- ⬜ Download health-dataset-complete-singapore dataset
- ⬜ Extract mortality tables for major diseases (cancer, stroke, ischemic heart disease)
- ⬜ Extract demographic mortality breakdowns if available
- ⬜ Verify file extraction with size and row count validation

### Data Loading and Schema Validation
- ⬜ Load mortality CSV files into Polars DataFrames
- ⬜ Validate schema: year column, disease identifier, ASMR values, demographic fields
- ⬜ Check data types (year: integer, rates: float, categorical fields)
- ⬜ Display first records and summary statistics per disease
- ⬜ Document any schema inconsistencies across disease tables

### Temporal Coverage Analysis
- ⬜ Identify year range for each disease dataset
- ⬜ Check for temporal gaps (missing years) in mortality series
- ⬜ Assess whether all diseases have consistent time coverage (1990-2019)
- ⬜ Document data lag (most recent available year)
- ⬜ Calculate percentage coverage by disease and decade

### Data Completeness Assessment
- ⬜ Calculate null percentages for ASMR values by disease and year
- ⬜ Identify years with incomplete demographic breakdowns
- ⬜ Assess whether age-standardization is consistently applied
- ⬜ Document missing disease categories or demographic segments
- ⬜ Validate that major diseases have >95% data completeness

### Data Quality Profiling
- ⬜ Check for duplicate year-disease combinations
- ⬜ Validate ASMR values are positive (no negative mortality rates)
- ⬜ Identify statistical outliers (unusually high/low mortality rates)
- ⬜ Check consistency of disease classification across years
- ⬜ Validate demographic breakdown consistency (age groups, gender)
- ⬜ Document any data quality concerns or anomalies

### Output and Documentation
- ⬜ Generate markdown data quality report with findings
- ⬜ Save raw mortality CSV files to `data/1_raw/mortality/`
- ⬜ Create data profiling summary table (disease, years, completeness)
- ⬜ Document disease classification scheme and ASMR methodology
- ⬜ Save ETL log to `logs/etl/` with extraction timestamp
- ⬜ Generate schema documentation for mortality datasets

## 6. Notes

**Data Quality Thresholds:**
- Acceptable completeness: >95% non-null for ASMR values
- Temporal coverage: Minimum 20 years of data for trend analysis
- Disease coverage: At minimum, cancer, stroke, ischemic heart disease

**ASMR Validation:**
- Verify that rates are age-standardized (check metadata or documentation)
- Confirm standard population used (WHO World Standard Population recommended)
- Validate that rates are per 100,000 population

**Related Stories:**
- This story establishes the data foundation for all subsequent disease burden analysis stories
- Quality assessment directly informs Story 2 (Data Cleaning and Standardization)

**Data Source Reference:** [data_sources.md](../../../docs/project_context/data-sources.md) - Section on Health Outcomes & Mortality
