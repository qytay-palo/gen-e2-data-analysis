# User Story 3: Multi-Dimensional Data Preparation and Standardization

**As a** data analyst,  
**I want** to clean, standardize, and validate multi-dimensional healthcare system data,  
**so that** I can ensure data quality and consistency across all sustainability dimensions for reliable trend analysis.

## 1. 🎯 Acceptance Criteria

- All numeric fields validated for accuracy (no negative values, outliers investigated)
- Temporal consistency validated (no retroactive changes, monotonic trends where expected)
- Categorical variables standardized (sector names, professional categories, disease classifications)
- Data transformations applied and documented (e.g., per-capita calculations, inflation adjustment)
- Outlier detection performed with flagging system (retain outliers but mark for investigation)
- Data quality scorecard updated with cleaning results
- Standardized datasets saved to `data/4_processed/` ready for analysis
- Comprehensive data cleaning report documenting all transformations and decisions
- Unit tests created for critical data validation rules

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient data cleaning and transformations
- **Validation Rules**: Document all validation logic explicitly
- **Reproducibility**: All transformations scripted and version-controlled
- **Outlier Detection**: ±3 standard deviations for statistical outliers; domain-informed thresholds
- **Output Format**: Parquet format with schema validation
- **Audit Trail**: Log all data modifications with before/after comparisons

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Standard Metrics](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#standard-metrics-and-kpis) - Valid ranges and thresholds
- [Healthcare Workforce Planning: Feature Engineering](../../../domain_knowledge/healthcare-workforce-planning.md#feature-engineering-guidance) - Workforce-specific validation rules
- [Disease Burden and Mortality Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md) - Mortality rate validation
- [Data Analysis Best Practices](.github/instructions/data-analysis-best-practices.instructions.md) - Data quality standards

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Data cleaning and transformations
- **numpy**: Statistical calculations for outlier detection
- **scipy**: Statistical tests for anomaly detection
- **loguru**: Cleaning operation logging

**Internal Dependencies:**
- Depends on: Story 2 (Data Integration & Temporal Alignment) - integrated datasets
- Input from: `data/3_interim/integrated_sustainability_data_2006_2018.parquet`
- Reuse: `src/utils/logger.py`, `src/data_processing/data_profiler.py`

## 5. ✅ Implementation Tasks

### Workforce Dimension Cleaning
- ⬜ Validate workforce counts: non-negative, reasonable ranges
  - Doctors: 8,000-20,000 (Singapore context)
  - Nurses: 15,000-45,000
  - Pharmacists: 1,500-4,000
- ⬜ Validate workforce growth: year-over-year change within -5% to +10%
- ⬜ Detect outliers: sudden spikes or drops requiring investigation
- ⬜ Standardize professional categories: consistent naming across years
- ⬜ Handle missing values: document any gaps in 2006-2018 window
- ⬜ Apply sector standardization: Public, Private, Not-for-Profit
- ⬜ Calculate total workforce: sum across professions for trend tracking

### Capacity Dimension Cleaning
- ⬜ Validate bed counts: non-negative, reasonable ranges
  - Total hospital beds: 10,000-15,000 (Singapore context)
  - Facility counts: positive integers
- ⬜ Validate capacity growth: year-over-year change within -2% to +8%
- ⬜ Detect anomalies: sudden capacity changes (facility closures/openings)
- ⬜ Standardize facility types: consistent categorization
- ⬜ Handle 2006-2008 data: apply back-fill or flag as reconstructed
- ⬜ Cross-validate: beds per facility ratio should be reasonable (200-500 beds per hospital)

### Utilization Dimension Cleaning
- ⬜ Validate admission counts: non-negative, reasonable ranges
- ⬜ Calculate admission rates: admissions per 1,000 population (require population data)
- ⬜ Validate demographic consistency: age groups sum to total, gender distribution reasonable
- ⬜ Detect seasonal anomalies: year-over-year trends should be smooth
- ⬜ Standardize age groups: consistent categorization across years
- ⬜ Handle missing demographic segments: document and flag

### Expenditure Dimension Cleaning
- ⬜ Validate expenditure amounts: non-negative, reasonable ranges
  - Total government health expenditure: SGD 8-15 billion (2006-2018)
- ⬜ Adjust for inflation: convert to constant 2018 SGD for trend analysis
  - Source inflation adjustment factors (Singapore CPI)
  - Apply to all years to enable real growth analysis
  - Document inflation methodology
- ⬜ Validate expenditure growth: real growth within 0% to +8% annually
- ⬜ Detect anomalies: sudden spending spikes or cuts
- ⬜ Standardize spending categories: consistent classification
- ⬜ Calculate per-capita expenditure: require population data

### Mortality Dimension Cleaning
- ⬜ Validate death rates: non-negative, age-standardized rates reasonable
  - All-cause mortality: 400-600 per 100,000 (typical range)
  - Disease-specific rates: validate against WHO benchmarks
- ⬜ Validate temporal consistency: death rates should trend gradually
- ⬜ Detect anomalies: sudden mortality spikes requiring investigation
- ⬜ Standardize disease categories: align with ICD classification
- ⬜ Handle missing disease categories: document incomplete coverage
- ⬜ Calculate leading causes: rank diseases by mortality burden

### Cross-Dimensional Validation
- ⬜ Validate workforce-capacity alignment:
  - Workforce-to-bed ratio: 1.5-2.5 FTE per bed
  - Flag if ratio outside expected range
- ⬜ Validate utilization-capacity alignment:
  - Bed utilization rate: 70-85% optimal
  - Admissions per bed: should be consistent over time
- ⬜ Validate expenditure-workforce alignment:
  - Expenditure per healthcare worker: should grow moderately
  - Flag if spending grows without workforce expansion
- ⬜ Validate mortality-utilization relationships:
  - High mortality diseases should correlate with admission patterns
- ⬜ Document cross-dimensional anomalies for investigation

### Outlier Detection and Flagging
- ⬜ Calculate z-scores for key metrics:
  - Workforce growth rates
  - Capacity expansion rates
  - Expenditure growth rates
  - Admission rate changes
  - Mortality rate changes
- ⬜ Flag statistical outliers: |z-score| > 3
- ⬜ Apply domain-informed thresholds:
  - Workforce growth >10% per year (flag for policy change investigation)
  - Capacity growth >8% per year (flag for facility expansion context)
  - Expenditure growth >10% real (flag for budget policy change)
- ⬜ Create outlier summary report: year, dimension, metric, value, z-score, flag
- ⬜ Retain outliers in dataset but add outlier flag field

### Data Transformation and Feature Creation
- ⬜ Calculate growth rates: year-over-year % change for all key metrics
- ⬜ Calculate indexed values: base year 2006 = 100 for trend visualization
- ⬜ Calculate per-capita metrics: workforce per capita, expenditure per capita (require population)
- ⬜ Calculate ratios: workforce-to-bed, expenditure-to-workforce, admissions-per-bed
- ⬜ Create temporal features: year index, decade indicator, pre/post-policy periods
- ⬜ Standardize units: ensure consistency (e.g., all financial in SGD millions)

### Population Data Integration (If Available)
- ⬜ Source Singapore population data 2006-2018 (Department of Statistics or external source)
- ⬜ Validate population data: reasonable growth rates (1-2% annually)
- ⬜ Integrate population data: join on year
- ⬜ Calculate per-capita metrics: workforce density, expenditure per capita, admission rates
- ⬜ Document population data source and any assumptions
- ⬜ If unavailable: flag per-capita calculations as future enhancement

### Data Quality Validation and Testing
- ⬜ Create validation test suite:
  - Test: All years 2006-2018 present
  - Test: No negative values in count/amount fields
  - Test: Sector values in allowed set
  - Test: Growth rates within expected ranges
  - Test: Cross-dimensional ratios reasonable
- ⬜ Run validation tests on cleaned data
- ⬜ Document test results: pass/fail status, issues identified
- ⬜ Update data quality scorecard with cleaning impact

### Output and Documentation
- ⬜ Save cleaned multi-dimensional dataset:
  - `data/4_processed/sustainability_data_cleaned_2006_2018.parquet`
- ⬜ Save dimension-specific cleaned datasets:
  - `data/4_processed/workforce_cleaned.parquet`
  - `data/4_processed/capacity_cleaned.parquet`
  - `data/4_processed/utilization_cleaned.parquet`
  - `data/4_processed/expenditure_cleaned.parquet`
  - `data/4_processed/mortality_cleaned.parquet`
- ⬜ Generate comprehensive data cleaning report documenting:
  - Validation rules applied
  - Outliers detected and flagged
  - Transformations applied (inflation adjustment, per-capita calculations)
  - Data quality before/after cleaning comparison
  - Recommendations for data interpretation
- ⬜ Create data dictionary for cleaned dataset:
  - Field names, types, descriptions
  - Calculated fields and formulas
  - Outlier flags and interpretation
- ⬜ Save cleaning log to `logs/etl/data_cleaning_{timestamp}.log`
- ⬜ Create unit test file: `tests/data/test_sustainability_data_quality.py`

## 6. Notes

**Inflation Adjustment Importance**: Healthcare expenditure must be adjusted for inflation to distinguish real growth from nominal growth. Use Singapore Consumer Price Index (CPI) for adjustment.

**Population Data Requirement**: Per-capita metrics are critical for sustainability analysis but require external population data. If unavailable in dataset, source from Singapore Department of Statistics.

**Outlier Retention Rationale**: Outliers may represent real policy changes (e.g., medical school intake expansion, new hospital opening). Retain but flag for contextual investigation rather than removing.

**Cross-Dimensional Validation Complexity**: Multi-dimensional cleaning requires understanding expected relationships (e.g., workforce should grow with capacity expansion). Domain knowledge essential for validation rules.

**Related Stories**: 
- Depends on: Story 2 (Data Integration)
- Enables: Story 4 (Exploratory Analysis), Story 5 (Feature Engineering)

**Estimated Effort**: 1 sprint (includes validation, cleaning, testing)
