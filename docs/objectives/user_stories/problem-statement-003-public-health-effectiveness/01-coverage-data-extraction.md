# User Story 1: Vaccination and School Health Program Data Extraction

**As a** public health program analyst,  
**I want** to extract vaccination coverage and school health screening data from the Kaggle dataset,  
**so that** I can assess program reach, temporal coverage, and establish a reliable foundation for public health program effectiveness analysis.

## 1. 🎯 Acceptance Criteria

- Vaccination coverage datasets successfully loaded for all available vaccines (2003-2020) by school cohort/academic year
- School health screening datasets successfully loaded: dental health indices, common health problems, obesity prevalence
- Program participation data validated for coverage calculation completeness
- Data profiling report generated showing:
  - Temporal coverage by program type (year ranges, data availability)
  - Data completeness (missing value percentages by program and year)
  - Student cohort segmentation availability (age groups, grade levels)
  - Health outcome metrics and measurement units
- Data quality issues documented with frequency and impact assessment
- Raw data saved to `data/1_raw/school_health/` with audit trail
- Data quality report saved to `logs/etl/data_quality_report_school_health_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient data loading and profiling
- **Platform**: Local Python environment (dataset <4MB)
- **Data Source**: Kaggle health-dataset-complete-singapore via kagglehub API
- **Documentation**: All operations logged using loguru
- **Output Format**: CSV for raw data with schema documentation

## 3. 📚 Domain Knowledge References

- [Public Health Programs and Vaccination](../../../domain_knowledge/public-health-programs-vaccination.md) - Understand coverage metrics, program effectiveness indicators
- [Vaccination Coverage](../../../domain_knowledge/public-health-programs-vaccination.md#vaccination-coverage) - Coverage targets and calculation methods
- [School Health Program Effectiveness](../../../domain_knowledge/public-health-programs-vaccination.md#school-health-program-effectiveness) - Key indicators and program types
- [Data Dictionary](../../../data_dictionary/) - Field-level documentation for school health data

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
- ⬜ Identify vaccination coverage tables in Kaggle dataset
- ⬜ Locate school health screening tables (dental, obesity, health problems)
- ⬜ Document table names and coverage periods for each program
- ⬜ Verify cohort segmentation availability (academic year, grade level, age)
- ⬜ Check demographic breakdown availability (gender, socioeconomic indicators)

### Data Extraction
- ⬜ Configure Kaggle API authentication
- ⬜ Download health-dataset-complete-singapore dataset
- ⬜ Extract vaccination coverage tables by vaccine type
- ⬜ Extract school health screening tables (dental indices, obesity, common health problems)
- ⬜ Verify file extraction with size and row count validation

### Data Loading and Schema Validation
- ⬜ Load vaccination coverage CSV files into Polars DataFrames
- ⬜ Load school health screening CSV files into Polars DataFrames
- ⬜ Validate schema: year column, cohort identifiers, coverage percentages, health metrics
- ⬜ Check data types (year: integer, rates: float, categorical fields)
- ⬜ Display first records and summary statistics per program
- ⬜ Document any schema inconsistencies across program tables

### Temporal Coverage Analysis
- ⬜ Identify year range for each program dataset (vaccination, screening)
- ⬜ Check for temporal gaps (missing years) in program coverage series
- ⬜ Assess whether all programs have consistent time coverage (2003-2020)
- ⬜ Document data lag (most recent available year = 2020, 5-year lag)
- ⬜ Calculate percentage coverage by program type and decade

### Data Completeness Assessment
- ⬜ Calculate null percentages for coverage rates by program and year
- ⬜ Identify years with incomplete cohort breakdowns
- ⬜ Assess whether all vaccines have coverage data across time period
- ⬜ Document missing health metrics or screening indicators
- ⬜ Validate that major programs have >95% data completeness

### Data Quality Profiling
- ⬜ Check for duplicate year-cohort-program combinations
- ⬜ Validate coverage values are between 0-100% (valid percentage range)
- ⬜ Identify statistical outliers (unusually high/low coverage or health metrics)
- ⬜ Check consistency of cohort classification across years
- ⬜ Validate health metric ranges (dental indices, obesity percentages)
- ⬜ Document any data quality concerns or anomalies

### Output and Documentation
- ⬜ Generate markdown data quality report with findings
- ⬜ Save raw CSV files to `data/1_raw/school_health/` organized by program type
- ⬜ Create data profiling summary table (program, years, completeness)
- ⬜ Document coverage calculation methodology and health metrics
- ⬜ Save ETL log to `logs/etl/` with extraction timestamp
- ⬜ Generate schema documentation for school health datasets

## 6. Notes

**Data Quality Thresholds:**
- Acceptable completeness: >95% non-null for coverage rates
- Temporal coverage: Minimum 15 years of data for trend analysis (2003-2020 = 17 years)
- Program coverage: At minimum, vaccination and dental screening programs required

**Coverage Rate Validation:**
- Verify that coverage values are percentages (0-100%)
- Check whether coverage can exceed 100% (e.g., catch-up vaccination campaigns)
- Confirm denominator used for coverage calculation (enrolled students vs. eligible population)

**Health Metrics Reference:**
- Dental health: DMFT index (Decayed, Missing, Filled Teeth)
- Obesity: BMI-based classification or percentage by grade level
- Common health problems: Prevalence rates for specific conditions

**Related Stories:**
- This story establishes the data foundation for all subsequent public health program effectiveness analysis stories
- Quality assessment directly informs Story 2 (Data Cleaning and Standardization)
- Coverage data extraction enables Story 3 (Exploratory Analysis) and Story 4 (Coverage Gap Analysis)

**Data Source Reference:** [data_sources.md](../../../docs/project_context/data-sources.md) - Section on School Health and Vaccination Programs

---

**Story Version**: 1.0  
**Created**: February 23, 2026  
**Status**: Ready for Sprint Planning
