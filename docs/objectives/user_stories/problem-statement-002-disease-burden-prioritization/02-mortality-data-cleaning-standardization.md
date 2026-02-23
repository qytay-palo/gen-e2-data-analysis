# User Story 2: Mortality Data Cleaning and Standardization

**As a** public health analyst,  
**I want** to clean, standardize, and validate mortality datasets for all major diseases,  
**so that** I can perform reliable disease burden comparisons and trend analysis with high-quality data.

## 1. 🎯 Acceptance Criteria

- All mortality datasets cleaned with documented transformations
- Disease names standardized across all tables (consistent naming convention)
- Temporal data validated: year fields converted to appropriate data types
- Missing values handled using domain-appropriate methods (interpolation, exclusion)
- Demographic categories standardized (age groups, gender labels)
- Data validation checks passed:
  - No negative mortality rates
  - Logical age group sequences
  - Consistent time series (no illogical spikes)
- Cleaned datasets saved to `data/3_interim/mortality_cleaned/`
- Data cleaning report saved to `logs/etl/data_cleaning_mortality_{timestamp}.md`

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient transformations
- **Data Quality**: Maintain data lineage for all transformations
- **Validation**: Apply domain-specific validation rules for mortality data
- **Documentation**: Log all cleaning operations with before/after metrics

## 3. 📚 Domain Knowledge References

- [Disease Burden Analysis: Data Quality Considerations](../../../domain_knowledge/disease-burden-mortality-analysis.md#data-quality-considerations) - Domain-specific quality issues and mitigation strategies
- [ASMR Validation Guidelines](../../../domain_knowledge/disease-burden-mortality-analysis.md#age-standardized-mortality-rate-asmr) - Ensure proper standardization

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data transformation and validation
- **numpy**: Statistical calculations for outlier detection
- **loguru**: Transformation logging

**Internal Dependencies:**
- Story 1 output: Raw mortality data in `data/1_raw/mortality/`
- `src/utils/logger.py`: Logging utilities
- `src/data_processing/data_profiler.py`: Validation functions

## 5. ✅ Implementation Tasks

### Disease Name Standardization
- ⬜ Create disease name mapping dictionary (raw → standardized names)
- ⬜ Standardize disease names: "Malignant Neoplasms" → "Cancer"
- ⬜ Apply mapping across all mortality tables consistently
- ⬜ Validate no duplicate disease entries after standardization
- ⬜ Document disease classification scheme

### Temporal Data Validation
- ⬜ Convert year columns to integer data type
- ⬜ Validate year range: 1990-2019 (expected mortality data period)
- ⬜ Check for illogical year sequences (e.g., 1899 instead of 1999)
- ⬜ Sort data by disease and year chronologically
- ⬜ Identify and document any temporal gaps

### Missing Value Handling
- ⬜ Identify patterns in missing ASMR values (specific years? diseases?)
- ⬜ For isolated missing years (1-2 years): Apply linear interpolation
- ⬜ For systematic gaps (>3 consecutive years): Document and exclude
- ⬜ Document missing value decisions in cleaning log
- ⬜ Flag interpolated values for transparency in analysis

### Outlier Detection and Validation
- ⬜ Calculate z-scores for ASMR values by disease
- ⬜ Flag values >3 standard deviations from disease-specific mean
- ⬜ Manually review flagged outliers for data entry errors
- ⬜ Validate outliers against external sources (WHO mortality database)
- ⬜ Document verified outliers as legitimate vs. corrected errors

### Demographic Standardization
- ⬜ Standardize age group labels (e.g., "0-14", "15-44", "45-64", "65+")
- ⬜ Standardize gender labels: "Male", "Female" (consistent capitalization)
- ⬜ Validate age group sequences are logical and complete
- ⬜ Check for demographic category consistency across diseases
- ⬜ Document demographic breakdown schema

### Data Type Optimization
- ⬜ Convert year to Int16 (range 1990-2100 sufficient)
- ⬜ Convert ASMR values to Float32 (sufficient precision)
- ⬜ Convert disease names to Categorical (memory efficient)
- ⬜ Convert demographic categories to Categorical
- ⬜ Measure memory reduction from type optimization

### Data Validation Checks
- ⬜ Validate no negative ASMR values exist
- ⬜ Check ASMR values are within reasonable range (0-500 per 100k)
- ⬜ Validate time series monotonicity (no abrupt unexplained changes >50%)
- ⬜ Check demographic totals match overall mortality where applicable
- ⬜ Validate all diseases have minimum 20 years of clean data
- ⬜ Run completeness checks: >95% non-null for critical fields

### Output and Documentation
- ⬜ Save cleaned datasets to `data/3_interim/mortality_cleaned/`
- ⬜ Generate data cleaning report with before/after metrics
- ⬜ Document all transformations applied (disease mapping, interpolations)
- ⬜ Create data lineage log showing transformation pipeline
- ⬜ Save cleaning validation results to `logs/etl/`
- ⬜ Update data dictionary with cleaned schema

## 6. Notes

**Interpolation Guidelines:**
- Use linear interpolation ONLY for isolated missing years (1-2 consecutive)
- For demographic breakdowns, interpolate within demographic groups
- Flag all interpolated values in a separate column for transparency

**Outlier Review Process:**
- Outliers flagged automatically but require manual review
- Cross-reference with WHO Global Health Observatory for validation
- Document justification for keeping or correcting outliers

**Quality Metrics to Track:**
- Percentage of values imputed/interpolated
- Number of outliers detected and handled
- Memory reduction from data type optimization
- Completeness improvement from cleaning

**Related Stories:**
- Depends on: Story 1 (Data Extraction and Profiling)
- Enables: Story 3 (Exploratory Disease Burden Analysis)
