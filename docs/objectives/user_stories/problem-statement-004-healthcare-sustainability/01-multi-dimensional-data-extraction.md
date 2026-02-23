# User Story 1: Multi-Dimensional Healthcare System Data Extraction

**As a** strategic planning analyst,  
**I want** to extract and profile multi-dimensional healthcare system data (workforce, capacity, utilization, expenditure, mortality) from the Kaggle dataset,  
**so that** I can assess data completeness across all system dimensions and establish a reliable foundation for long-term sustainability analysis.

## 1. 🎯 Acceptance Criteria

- Workforce datasets successfully loaded: doctors, nurses, pharmacists (2006-2019) by sector
- Capacity datasets successfully loaded: hospital beds and primary care facilities (2009-2020) by sector
- Utilization datasets successfully loaded: hospital admissions by age/gender (2006-2020)
- Expenditure datasets successfully loaded: government health spending by sector (2006-2018)
- Mortality datasets successfully loaded: death rates by disease category (1990-2019)
- Data profiling report generated for each dimension showing:
  - Record counts and temporal coverage by dimension
  - Data completeness (missing value percentages)
  - Time series continuity validation (gaps identified)
  - Data type and field validation
  - Cross-dimensional temporal alignment assessment
- Multi-dimensional data quality scorecard generated comparing completeness across dimensions
- Raw data saved to `data/1_raw/` with proper categorization by dimension
- Comprehensive data extraction report saved to `logs/etl/` with timestamp

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient multi-file data profiling
- **Data Loading**: Load from Kaggle dataset using kagglehub API (reuse existing extractor)
- **Environment**: Local Python environment, no distributed processing needed
- **Documentation**: All transformations logged using loguru
- **Output Format**: Parquet format for intermediate storage with schema validation
- **Memory Management**: Process datasets sequentially to avoid memory constraints

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Overview](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#overview) - Understand multi-dimensional sustainability framework
- [Healthcare System Sustainability Metrics: Four Critical Dimensions](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#healthcare-system-sustainability-dimensions) - Context for each data dimension
- [Healthcare Workforce Planning: Key Concepts](../../../domain_knowledge/healthcare-workforce-planning.md#key-concepts-and-terminology) - Workforce data interpretation
- [Disease Burden and Mortality Analysis](../../../domain_knowledge/disease-burden-mortality-analysis.md) - Mortality data context

## 4. 📦 Dependencies

**External Packages:**
- **kagglehub**: Data extraction from Kaggle datasets
- **polars**: DataFrame processing and profiling
- **loguru**: Structured logging of ETL operations
- **pandas**: Alternative if Polars profiling insufficient

**Internal Dependencies:**
- Reuse `src/data_processing/kaggle_extractor.py` from PS-001
- Reuse `src/data_processing/data_profiler.py` from PS-001
- Reuse `src/utils/config_loader.py` for configuration management
- Reuse `src/utils/logger.py` for logging setup

## 5. ✅ Implementation Tasks

### Data Extraction Configuration
- ⬜ Create `config/ps-004-sustainability.yml` with target datasets for all dimensions
- ⬜ Define dataset mappings: workforce tables, capacity tables, utilization tables, expenditure tables, mortality tables
- ⬜ Configure extraction parameters (years, sectors, granularity)
- ⬜ Set up logging configuration for multi-dimensional extraction

### Workforce Dimension Extraction
- ⬜ Extract number-of-doctors (2006-2019) by sector
- ⬜ Extract number-of-nurses-and-midwives (2006-2019) by sector
- ⬜ Extract number-of-pharmacists (2006-2019) by sector
- ⬜ Verify temporal coverage: 2006-2019 complete
- ⬜ Profile: record counts per year, sector coverage, missing values
- ⬜ Save to `data/1_raw/workforce/`

### Capacity Dimension Extraction
- ⬜ Extract health-facilities-and-beds (hospital beds) by sector (2009-2020)
- ⬜ Extract health-facilities-primary-care by sector (2009-2020)
- ⬜ Verify temporal coverage: 2009-2020 complete
- ⬜ Profile: record counts per year, facility type distribution
- ⬜ Save to `data/1_raw/capacity/`

### Utilization Dimension Extraction
- ⬜ Extract hospital-admissions-by-age-and-gender (2006-2020)
- ⬜ Verify demographic dimensions: age groups, gender
- ⬜ Verify temporal coverage: 2006-2020 complete
- ⬜ Profile: admission counts by demographic segment and year
- ⬜ Save to `data/1_raw/utilization/`

### Expenditure Dimension Extraction
- ⬜ Extract government-health-expenditure (2006-2018) by sector
- ⬜ Verify sector/spending category breakdowns
- ⬜ Verify temporal coverage: 2006-2018 complete
- ⬜ Profile: expenditure amounts, growth trends, sector distribution
- ⬜ Save to `data/1_raw/expenditure/`

### Mortality Dimension Extraction
- ⬜ Extract death-rates-by-disease (1990-2019)
- ⬜ Verify disease categories and classification
- ⬜ Verify temporal coverage: 1990-2019 complete (focus on 2006+ for alignment)
- ⬜ Profile: disease prevalence, temporal trends
- ⬜ Save to `data/1_raw/mortality/`

### Cross-Dimensional Data Quality Assessment
- ⬜ Create temporal alignment matrix showing year coverage across all dimensions
- ⬜ Identify common temporal window (likely 2006-2018 where all dimensions overlap)
- ⬜ Calculate completeness scores by dimension (% of expected records present)
- ⬜ Identify data gaps requiring attention in next story
- ⬜ Compare granularity across dimensions (sector-level, age-level, disease-level)

### Data Profiling and Quality Reporting
- ⬜ Generate dimension-specific profiling reports:
  - Workforce: Professional category distribution, sector coverage
  - Capacity: Facility type distribution, bed count ranges
  - Utilization: Demographic coverage, admission rate ranges
  - Expenditure: Spending category distribution, amount ranges
  - Mortality: Disease category distribution, rate ranges
- ⬜ Create multi-dimensional summary comparing:
  - Temporal coverage by dimension
  - Data completeness by dimension
  - Record counts by dimension
  - Identified quality issues by dimension
- ⬜ Generate executive summary highlighting cross-dimensional data readiness

### Output and Documentation
- ⬜ Save dimension-specific raw datasets to organized subdirectories
- ⬜ Generate comprehensive multi-dimensional data extraction report (markdown)
- ⬜ Create data quality scorecard comparing dimensions
- ⬜ Document any dimension-specific data quality concerns
- ⬜ Save ETL log with timestamps and operations performed to `logs/etl/multi_dimensional_extraction_{timestamp}.log`
- ⬜ Create data dictionary template for each dimension

## 6. Notes

**Data Access**: Use the Kaggle dataset documented in [data_sources.md](../../../project_context/data-sources.md). Reuse existing Kaggle extraction utilities from PS-001 implementation.

**Quality Thresholds**: 
- Acceptable completeness: >95% non-null for key fields per dimension
- Temporal coverage: All dimensions should have majority coverage 2006-2018
- Cross-dimensional alignment: Identify common analysis window

**Multi-Dimensional Complexity**: This story differs from PS-001 Story 1 by extracting data across 5 distinct dimensions instead of 2, requiring careful organization and comprehensive cross-dimensional profiling.

**Related Stories**: This foundational story enables all subsequent PS-004 stories. Output feeds directly into Story 2 (Data Integration & Temporal Alignment).

**Estimated Effort**: 1 sprint (includes setup, extraction, profiling across all dimensions)
