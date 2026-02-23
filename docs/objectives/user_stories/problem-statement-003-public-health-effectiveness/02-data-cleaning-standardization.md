# User Story 2: School Health and Vaccination Data Cleaning and Standardization

**As a** public health program analyst,  
**I want** to clean, standardize, and validate vaccination coverage and school health screening datasets,  
**so that** I have reliable, consistent data for analyzing program effectiveness and identifying coverage gaps.

## 1. 🎯 Acceptance Criteria

- Vaccination coverage data cleaned and standardized across all vaccine types and years
- School health screening data (dental, obesity, health problems) cleaned and validated
- Coverage rates normalized to consistent percentage format (0-100%)
- Cohort classifications standardized (academic year, grade level, age group)
- Health metrics standardized to consistent measurement units and scales
- Missing values handled with documented imputation strategy or exclusion rationale
- Data quality scorecard generated showing pre/post cleaning metrics
- Clean datasets saved to `data/4_processed/school_health/` with data lineage documentation
- Transformation audit trail saved to `logs/etl/data_cleaning_school_health_{timestamp}.log`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for data cleaning and transformation
- **Platform**: Local Python environment
- **Data Validation**: Implement schema validation and range checks
- **Documentation**: All transformations logged with before/after statistics
- **Output Format**: Parquet format for processed data with schema versioning

## 3. 📚 Domain Knowledge References

- [Public Health Programs - Data Quality Considerations](../../../domain_knowledge/public-health-programs-vaccination.md#data-quality-considerations) - Coverage reporting inconsistencies and validation approaches
- [Coverage Metrics](../../../domain_knowledge/public-health-programs-vaccination.md#vaccination-coverage) - Understanding coverage calculation denominators
- [Standard Metrics and KPIs](../../../domain_knowledge/public-health-programs-vaccination.md#standard-metrics-and-kpis) - Target ranges for validation

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data cleaning and transformation
- **loguru**: Operation logging
- **pyyaml**: Configuration loading

**Internal Dependencies:**
- `src/utils/logger.py`: Logging utilities
- `src/utils/config_loader.py`: Configuration management
- Output from Story 1: Raw vaccination and school health data

## 5. ✅ Implementation Tasks

### Data Quality Assessment (Pre-Cleaning Baseline)
- ⬜ Generate baseline data quality metrics for vaccination coverage data
- ⬜ Generate baseline metrics for school health screening data
- ⬜ Document missing value patterns by program type and year
- ⬜ Identify outliers and anomalous values requiring investigation
- ⬜ Record duplicate records and inconsistencies

### Coverage Data Standardization
- ⬜ Standardize coverage rates to percentage format (0-100%)
- ⬜ Handle edge cases where coverage may exceed 100% (catch-up campaigns)
- ⬜ Normalize vaccine names to consistent taxonomy
- ⬜ Standardize cohort classifications (academic year format: YYYY-YYYY)
- ⬜ Validate coverage denominators align with enrolled student counts
- ⬜ Document any coverage calculation methodology changes over time

### School Health Metrics Standardization
- ⬜ Standardize dental health indices (DMFT score validation)
- ⬜ Normalize obesity metrics (BMI percentages, classification thresholds)
- ⬜ Standardize health problem prevalence rates (per 1,000 or percentage)
- ⬜ Validate health metric ranges against clinical norms
- ⬜ Ensure consistent age/grade level categorization
- ⬜ Handle changes in screening methodology across years

### Missing Value Treatment
- ⬜ Identify patterns in missing coverage data (random vs. systematic)
- ⬜ Determine missingness impact on temporal trend analysis
- ⬜ Apply appropriate handling strategy:
  - Exclude years with <80% completeness for specific programs
  - Document gaps in coverage series for stakeholder awareness
  - NO imputation for coverage rates (preserve data integrity)
- ⬜ Flag programs/years with incomplete data for cautious interpretation
- ⬜ Document all missing value decisions in data lineage

### Data Type and Format Validation
- ⬜ Convert year fields to integer type
- ⬜ Convert coverage percentages to float64 with 2 decimal precision
- ⬜ Convert health metrics to appropriate numeric types
- ⬜ Encode categorical variables (vaccine type, health problem category)
- ⬜ Validate date formats for academic year fields
- ⬜ Ensure all percentage values are in 0-100 range

### Outlier Detection and Handling
- ⬜ Identify coverage rates >100% and validate against program documentation
- ⬜ Detect statistical outliers in health metrics (z-score >3 or IQR method)
- ⬜ Investigate year-over-year coverage jumps >20 percentage points
- ⬜ Cross-validate extreme values with program reports or external sources
- ⬜ Document outlier handling decisions (retain with flag vs. exclude)
- ⬜ Create outlier summary report for stakeholder review

### Duplicate Record Resolution
- ⬜ Identify duplicate year-cohort-program combinations
- ⬜ Investigate cause of duplicates (data entry error vs. multiple reporting)
- ⬜ Resolve duplicates using most recent or most complete record
- ⬜ Document duplicate resolution logic
- ⬜ Validate no duplicates remain after cleaning

### Temporal Consistency Validation
- ⬜ Check for gaps in year sequences for each program
- ⬜ Validate that cohort progressions are logical (grade levels advance yearly)
- ⬜ Identify program discontinuations or methodology changes
- ⬜ Flag years with potential data quality issues for further investigation
- ⬜ Document temporal coverage completeness by program

### Data Quality Scorecard Generation
- ⬜ Calculate pre-cleaning vs. post-cleaning completeness rates
- ⬜ Document records removed and transformation applied
- ⬜ Generate summary statistics for each cleaned dataset
- ⬜ Create data quality metrics: accuracy, completeness, consistency
- ⬜ Produce before/after comparison visualizations
- ⬜ Save scorecard to `results/metrics/school_health_data_quality_scorecard.csv`

### Output and Documentation
- ⬜ Save cleaned vaccination coverage data to `data/4_processed/school_health/vaccination_coverage_clean.parquet`
- ⬜ Save cleaned school health screening data to `data/4_processed/school_health/screening_outcomes_clean.parquet`
- ⬜ Generate data lineage documentation showing all transformations
- ⬜ Create schema documentation for cleaned datasets
- ⬜ Save transformation log with timestamp and operation details
- ⬜ Document any data limitations for downstream analysis

## 6. Notes

**Coverage Rate Validation Rules:**
- Standard range: 0-100%
- Acceptable >100%: If documented catch-up vaccination campaign
- Flag for review: Coverage changes >20% year-over-year without explanation

**Health Metrics Validation:**
- DMFT Index: Range 0-32 (total deciduous + permanent teeth)
- Obesity Prevalence: 0-100% (percentage of screened students)
- Common Health Problems: Measured as rate per 1,000 students or percentage

**Handling Methodology Changes:**
- Document any changes in screening protocols or coverage calculation methods
- Flag affected years for cautious interpretation in trend analysis
- Consult domain experts if methodology impact unclear

**Data Quality Acceptance Criteria:**
- Post-cleaning completeness: >95% for core metrics
- Outliers flagged and documented: <2% of records
- Zero duplicate records after cleaning
- All values within valid ranges with exceptions documented

**Related Stories:**
- Depends on Story 1 (Data Extraction and Quality Assessment)
- Enables Story 3 (Exploratory Analysis) with reliable clean data
- Provides foundation for Story 4 (Coverage Gap Analysis)

**Validation Reference:** [Standard Metrics and KPIs](../../../domain_knowledge/public-health-programs-vaccination.md#standard-metrics-and-kpis) for target ranges

---

**Story Version**: 1.0  
**Created**: February 23, 2026  
**Status**: Ready for Sprint Planning
