# User Story 2: Multi-Dimensional Data Integration and Temporal Alignment

**As a** healthcare system analyst,  
**I want** to integrate disparate healthcare datasets (workforce, capacity, utilization, expenditure, mortality) with temporal alignment,  
**so that** I can create a unified multi-dimensional time series dataset enabling comprehensive sustainability analysis.

## 1. 🎯 Acceptance Criteria

- Common temporal window identified across all dimensions (likely 2006-2018)
- All datasets temporally aligned to common year range
- Unified data schema established with dimension identifiers
- Integrated dataset created with consistent temporal granularity (annual)
- Cross-dimensional relationships validated (e.g., workforce trends vs. utilization trends)
- Missing value strategy defined and documented for temporal gaps
- Standardized sector classifications harmonized across dimensions
- Integration logic documented with clear data lineage
- Integrated dataset saved to `data/3_interim/` with comprehensive metadata
- Data integration report documenting alignment decisions and trade-offs

## 2. 🔒 Technical Constraints

- **Data Processing**: Use Polars for efficient multi-table joins and temporal alignment
- **Temporal Alignment**: Annual granularity (align all data to calendar years)
- **Schema Design**: Star schema with time dimension as primary key
- **Missing Values**: Document strategy (forward-fill, interpolation, or flagging)
- **Output Format**: Parquet format with partitioning by dimension for efficient querying
- **Data Lineage**: Track which source tables contributed to each integrated record

## 3. 📚 Domain Knowledge References

- [Healthcare System Sustainability Metrics: Multi-Dimensional Framework](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#healthcare-system-sustainability-dimensions) - Understanding dimension interdependencies
- [Healthcare System Sustainability Metrics: Comparative Trend Analysis](../../../domain_knowledge/healthcare-system-sustainability-metrics.md#feature-engineering-guidance) - Multi-dimensional growth rate alignment
- [Data Integration Best Practices](.github/instructions/data-analysis-best-practices.instructions.md) - Temporal alignment methods

## 4. 📦 Dependencies

**External Packages:**
- **polars**: Multi-dimensional data integration and joins
- **numpy**: Temporal interpolation calculations
- **loguru**: Integration operation logging

**Internal Dependencies:**
- Depends on: Story 1 (Multi-Dimensional Data Extraction) - raw datasets
- Input from: `data/1_raw/workforce/`, `data/1_raw/capacity/`, `data/1_raw/utilization/`, `data/1_raw/expenditure/`, `data/1_raw/mortality/`
- Reuse: `src/utils/logger.py` for logging

## 5. ✅ Implementation Tasks

### Temporal Coverage Analysis
- ⬜ Load all dimension datasets and extract year ranges
- ⬜ Create temporal coverage matrix:
  - Workforce: 2006-2019
  - Capacity: 2009-2020
  - Utilization: 2006-2020
  - Expenditure: 2006-2018
  - Mortality: 1990-2019 (focus 2006+)
- ⬜ Identify maximum common temporal window (2009-2018 all overlap; 2006-2019 most overlap)
- ⬜ Document decision on temporal window selection (recommend 2006-2018 for sustainability analysis)
- ⬜ Justify any trade-offs (e.g., excluding 2019-2020 due to incomplete expenditure data)

### Data Schema Harmonization
- ⬜ Define unified schema with dimensions:
  - Time dimension: year (primary key across all dimensions)
  - Sector dimension: public, private, not-for-profit (standardized)
  - Professional category: doctors, nurses, pharmacists
  - Facility type: hospital beds, primary care facilities
  - Demographic segment: age groups, gender (for utilization)
  - Disease category: for mortality data
  - Expenditure category: for financial data
- ⬜ Map source schemas to unified schema
- ⬜ Create data dictionary documenting schema mappings
- ⬜ Validate all source fields mapped correctly

### Sector Classification Standardization
- ⬜ Review sector classifications across dimensions (ensure consistency)
- ⬜ Standardize sector names: "Public" vs. "Government" → "Public"
- ⬜ Create sector mapping table for reference
- ⬜ Apply standardized classifications to all datasets
- ⬜ Validate no records lost in standardization

### Temporal Alignment and Integration
- ⬜ Filter all datasets to common temporal window (2006-2018 recommended)
- ⬜ Aggregate any sub-annual data to annual granularity
- ⬜ Create time dimension table (year, year_index for sequential analysis)
- ⬜ Join workforce dimension: left join on year
- ⬜ Join capacity dimension: left join on year
- ⬜ Join utilization dimension: left join on year
- ⬜ Join expenditure dimension: left join on year and sector
- ⬜ Join mortality dimension: left join on year
- ⬜ Validate join completeness (check for unexpected nulls)

### Missing Value Handling Strategy
- ⬜ Identify missing values in integrated dataset:
  - Capacity data missing 2006-2008 (pre-2009)
  - Expenditure data missing 2019+ (limited to 2018)
- ⬜ Define handling strategy per dimension:
  - **Workforce**: Complete 2006-2018, no imputation needed
  - **Capacity 2006-2008**: Backward-fill from 2009 OR flag as unavailable
  - **Utilization**: Complete 2006-2018, no imputation needed
  - **Expenditure**: Complete 2006-2018, no imputation needed
  - **Mortality**: Complete 2006-2018, no imputation needed
- ⬜ Apply imputation strategy and document rationale
- ⬜ Add data quality flags: `is_imputed`, `source_dimension` for traceability

### Cross-Dimensional Validation
- ⬜ Validate expected relationships:
  - Hospital admissions (utilization) should correlate with hospital beds (capacity)
  - Workforce counts should align with facility counts (capacity)
  - Expenditure growth should relate to workforce/capacity expansion
- ⬜ Calculate preliminary correlation matrix across dimensions
- ⬜ Identify any anomalies (e.g., capacity expanding without workforce growth)
- ⬜ Document validation findings

### Data Integration Quality Checks
- ⬜ Validate temporal continuity: no missing years in common window
- ⬜ Validate record counts: expected records per year per dimension
- ⬜ Validate sector coverage: all sectors represented across dimensions
- ⬜ Check for duplicate records: unique combination of year + dimension + sector
- ⬜ Validate data types: numeric fields numeric, categorical fields standardized
- ⬜ Generate integration quality scorecard

### Output and Documentation
- ⬜ Save integrated multi-dimensional dataset:
  - `data/3_interim/integrated_sustainability_data_2006_2018.parquet`
- ⬜ Create dimension-specific extracts for targeted analysis:
  - `data/3_interim/workforce_integrated.parquet`
  - `data/3_interim/capacity_integrated.parquet`
  - `data/3_interim/utilization_integrated.parquet`
  - `data/3_interim/expenditure_integrated.parquet`
  - `data/3_interim/mortality_integrated.parquet`
- ⬜ Generate comprehensive data integration report documenting:
  - Temporal alignment decisions and rationale
  - Schema harmonization mappings
  - Missing value handling strategies
  - Cross-dimensional validation results
  - Data quality scorecard
- ⬜ Create data lineage diagram showing source-to-integrated mapping
- ⬜ Save integration log to `logs/etl/data_integration_{timestamp}.log`

## 6. Notes

**Temporal Window Trade-Offs**:
- **2006-2018** (13 years): All dimensions complete except capacity 2006-2008; best for sustainability analysis
- **2009-2018** (10 years): All dimensions complete; shorter time series reduces trend analysis power
- Recommend: **2006-2018** with capacity back-filled or flagged 2006-2008

**Schema Design Rationale**:
- Star schema enables efficient multi-dimensional queries
- Annual granularity matches strategic planning horizon
- Sector dimension enables comparative analysis across healthcare system segments

**Cross-Dimensional Complexity**: Integration requires careful schema design due to varying granularities (sector-level workforce vs. age/gender utilization vs. disease-level mortality)

**Related Stories**: 
- Depends on: Story 1 (Data Extraction)
- Enables: Story 3 (Data Preparation), Story 4 (Exploratory Analysis)

**Estimated Effort**: 1 sprint (includes analysis, integration, validation)
