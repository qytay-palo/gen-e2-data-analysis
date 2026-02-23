# Problem Statement 001: Workforce Capacity Mismatch Analysis

This directory contains all implementation code for analyzing healthcare workforce and capacity mismatches in Singapore's healthcare system (2006-2020).

## 📋 Overview

**Problem Statement**: Identify critical gaps and mismatches between healthcare workforce supply (doctors, nurses, pharmacists) and capacity demand (hospital beds, primary care facilities) across Public, Private, and Not-for-Profit sectors to inform MOH workforce planning and resource allocation strategies.

**Data Sources**: Kaggle dataset `subhamjain/health-dataset-complete-singapore` (35 CSV files, ~3.5 MB)

**Analysis Period**: 
- Workforce data: 2006-2019
- Capacity data: 2009-2020  
- Joint analysis period: 2009-2019

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**: Python 3.9+ required
2. **Virtual Environment**: Activate the project virtual environment
   ```bash
   source .venv/bin/activate
   ```
3. **Dependencies**: Install required packages
   ```bash
   uv pip install -r requirements.txt
   ```
4. **Kaggle Credentials**: Configure Kaggle API (required for data extraction)
   ```bash
   # Ensure ~/.kaggle/kaggle.json exists with valid credentials
   ```

### Running the Analysis

**User Story 1: Data Extraction and Quality Assessment**
```bash
# Extract workforce and capacity data from Kaggle
.venv/bin/python src/problem-statement-001-workforce-capacity-mismatch/scripts/01_extract_workforce_capacity_data.py

# Explore extraction results
jupyter notebook src/problem-statement-001-workforce-capacity-mismatch/notebooks/01_explore_extraction_results.ipynb
```

**User Story 2: Data Cleaning and Standardization**
```bash
# Clean and standardize extracted data
.venv/bin/python scripts/clean_workforce_capacity_data.py

# Explore cleaned data outputs
jupyter notebook src/problem-statement-001-workforce-capacity-mismatch/notebooks/explore_cleaned_data.ipynb
```

## 📂 Directory Structure

```
src/problem-statement-001-workforce-capacity-mismatch/
├── data_processing/              # Data processing modules
│   ├── __init__.py
│   ├── kaggle_extractor.py      # Kaggle dataset extraction
│   └── data_profiler.py         # Data quality profiling
├── scripts/                      # Executable scripts
│   └── 01_extract_workforce_capacity_data.py
├── notebooks/                    # Jupyter notebooks for exploration
│   └── 01_explore_extraction_results.ipynb
├── tests/                        # Unit and integration tests
└── README.md                     # This file
```

## 🔄 Execution Flow

### User Story 1: Data Extraction and Quality Assessment

**Purpose**: Extract healthcare workforce and capacity data from Kaggle and perform comprehensive quality profiling.

**Execution Steps**:
1. **Connect to Kaggle** - Download dataset using kagglehub API
2. **Extract Workforce Tables** - Load doctors, nurses, pharmacists data (3 tables)
3. **Extract Capacity Tables** - Load hospital beds, primary care facilities data (2 tables)
4. **Profile Data** - Generate quality metrics (completeness, duplicates, outliers)
5. **Generate Report** - Create markdown quality assessment report

**Inputs**:
- Kaggle dataset: `subhamjain/health-dataset-complete-singapore`
- Configuration: Kaggle API credentials from `~/.kaggle/kaggle.json`

**Outputs**:
| File | Location | Format | Description |
|------|----------|--------|-------------|
| Workforce - Doctors | `data/1_raw/workforce_doctors.csv` | CSV | Doctor counts by year/sector |
| Workforce - Nurses | `data/1_raw/workforce_nurses.csv` | CSV | Nurse counts by year/sector/type |
| Workforce - Pharmacists | `data/1_raw/workforce_pharmacists.csv` | CSV | Pharmacist counts by year/sector |
| Capacity - Hospital Beds | `data/1_raw/capacity_hospital_beds.csv` | CSV | Hospital beds by year/sector/facility type |
| Capacity - Primary Care | `data/1_raw/capacity_primary_care.csv` | CSV | Primary care facilities by year/sector |
| Quality Report | `logs/etl/data_quality_report_YYYYMMDD_HHMMSS.md` | Markdown | Data profiling results |

**Duration**: ~30 seconds (dataset cached after first download)

**Dependencies**: kagglehub, polars, loguru

### User Story 2: Data Cleaning and Standardization

**Purpose**: Clean, standardize, and validate extracted data for downstream analysis.

**Execution Steps**:
1. **Load Configuration** - Read cleaning rules from `config/cleaning_rules.yml`
2. **Load Raw Data** - Read 5 CSV files from `data/1_raw/`
3. **Clean Workforce Data** - Standardize columns, unify tables, convert types, standardize sector names, handle missing values, detect duplicates, flag outliers
4. **Clean Capacity Data** - Same cleaning steps as workforce
5. **Validate Cleaned Data** - Run schema, range, categorical, duplicate, and completeness validations
6. **Save Cleaned Data** - Write parquet files to `data/3_interim/`
7. **Generate Reports** - Create validation reports and data dictionary
8. **Log Summary** - Write transformation summary to logs

**Inputs**:
- Configuration: `config/cleaning_rules.yml` (column mappings, sector standardization, validation rules)
- Workforce data: `data/1_raw/workforce_doctors.csv`, `workforce_nurses.csv`, `workforce_pharmacists.csv`
- Capacity data: `data/1_raw/capacity_hospital_beds.csv`, `capacity_primary_care.csv`

**Outputs**:
| File | Location | Format | Description |
|------|----------|--------|-------------|
| Cleaned Workforce | `data/3_interim/workforce_clean.parquet` | Parquet | Unified and cleaned workforce data (doctors, nurses, pharmacists) |
| Cleaned Capacity | `data/3_interim/capacity_clean.parquet` | Parquet | Unified and cleaned capacity data (hospital beds, primary care) |
| Validation Report | `logs/etl/validation_report_YYYYMMDD_HHMMSS.md` | Markdown | Data quality validation results |
| Data Dictionary | `data/3_interim/data_dictionary.md` | Markdown | Schema and field descriptions |
| Transformation Log | `logs/etl/cleaning_pipeline_YYYYMMDD_HHMMSS.log` | Log | Detailed execution logs |

**Duration**: ~5 seconds (including all cleaning, validation, and I/O operations)

**Dependencies**: polars, loguru, pydantic, yaml

**Data Transformations**:
- **Column Standardization**: Convert all column names to snake_case
- **Type Conversion**: Optimize to Int32 (year, count), Categorical (profession, sector)
- **Sector Unification**: Standardize 8 sector name variations → 4 categories (Public, Private, Not-for-Profit, Inactive)
- **Table Unification**: Merge 3 workforce tables with `profession` column
- **Outlier Detection**: Flag values > IQR ± 1.5×IQR
- **Duplicate Detection**: Identify duplicate (year, sector, profession) combinations
- **Missing Value Handling**: Flag missing values, preserve original data

**Validation Checks**:
- ✅ Schema validation (required columns present, correct types)
- ✅ Value range validation (year 2006-2020, counts ≥ 0)
- ✅ Categorical value validation (sectors, professions in allowed lists)
- ✅ Duplicate validation (0 duplicates expected)
- ✅ Completeness validation (100% completeness for critical fields)

## 🛠️ Environment Setup

### Python Dependencies

All dependencies are managed via `uv` (NOT pip):

```bash
# Install packages
uv pip install kagglehub polars loguru pydantic pyyaml matplotlib seaborn

# Update requirements
uv pip freeze > requirements.txt
```

**Core Dependencies**:
- `kagglehub>=1.0.0` - Kaggle dataset extraction
- `polars>=1.38.0` - High-performance data processing
- `loguru>=0.7.0` - Structured logging
- `pydantic>=2.12.0` - Data validation
- `matplotlib>=3.7.0` - Visualizations
- `seaborn>=0.12.0` - Statistical visualizations

### Kaggle API Setup

1. Create Kaggle account at https://www.kaggle.com
2. Navigate to Account Settings → API → Create New API Token
3. Save downloaded `kaggle.json` to `~/.kaggle/kaggle.json`
4. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

## 📊 Data Quality Summary

From extraction execution (2026-02-23):

**Completeness**: 100% across all tables (0 missing values)
**Duplicates**: 0 duplicate records detected
**Tables Extracted**: 5 (3 workforce, 2 capacity)

| Table | Rows | Columns | Year Range | Sectors |
|-------|------|---------|------------|---------|
| Doctors | 78 | 4 | 2006-2019 | 3 |
| Nurses | 126 | 4 | 2006-2019 | 3 |
| Pharmacists | 42 | 3 | 2006-2019 | 3 |
| Hospital Beds | 180 | 6 | 2009-2020 | 3 |
| Primary Care | 96 | 5 | 2009-2020 | 2 |

## 🔍 Troubleshooting

### Common Issues

**Issue**: `zsh: command not found: python`  
**Solution**: Use virtual environment Python: `.venv/bin/python`

**Issue**: `ModuleNotFoundError: No module named 'kagglehub'`  
**Solution**: Install packages using `uv pip install -r requirements.txt`

**Issue**: `RuntimeError: Failed to download Kaggle dataset`  
**Solution**: 
1. Verify Kaggle credentials: `cat ~/.kaggle/kaggle.json`
2. Check file permissions: `ls -l ~/.kaggle/kaggle.json` (should be `-rw-------`)
3. Test authentication: `kaggle datasets list` (should show datasets)

**Issue**: `FileNotFoundError: data/1_raw/workforce_doctors.csv`  
**Solution**: Run extraction script first:
```bash
.venv/bin/python src/problem-statement-001-workforce-capacity-mismatch/scripts/01_extract_workforce_capacity_data.py
```

### Logs

Check execution logs for detailed error information:
- **ETL logs**: `logs/etl/workforce_extraction_YYYYMMDD.log`
- **Error logs**: `logs/errors/` (if enabled)
- **Audit logs**: `logs/audit/` (if enabled)

## 📈 Performance Considerations

### Data Size Recommendations
- **Current dataset**: ~3.5 MB total (small dataset)
- **Execution mode**: Local machine (no distributed processing needed)
- **Memory usage**: < 50 MB RAM for all operations

### Optimization Tips
1. **Kaggle caching**: Dataset cached in `~/.cache/kagglehub/` after first download
2. **Polars efficiency**: Uses lazy evaluation automatically for large files
3. **Logging**: Disable DEBUG-level logging in production for faster execution

### Expected Execution Times

| Stage | Duration | Notes |
|-------|----------|-------|
| Kaggle Download | 5-10s | First time only (cached thereafter) |
| Table Extraction | 1-2s | All 5 tables |
| Data Profiling | 1-2s | All quality metrics |
| Report Generation | <1s | Markdown output |
| **Total** | **~30s** | Including initial download |

## 📝 Next Steps

1. ✅ **User Story 1**: Data Extraction and Quality Assessment (COMPLETED)
2. ⬜ **User Story 2**: Data Cleaning and Standardization (IN PROGRESS)
3. ⬜ **User Story 3**: Exploratory Analysis
4. ⬜ **User Story 4**: Workforce Capacity Metrics Calculation
5. ⬜ **User Story 5**: Comparative Dashboard Development
6. ⬜ **User Story 6**: Findings Report Generation

## 📚 Related Documentation

- [Problem Statement 001](../../../docs/objectives/problem_statements/ps-001-workforce-capacity-mismatch.md)
- [User Story 1](../../../docs/objectives/user_stories/problem-statement-001-workforce-capacity-mismatch/01-data-extraction-quality-assessment.md)
- [User Story 2](../../../docs/objectives/user_stories/problem-statement-001-workforce-capacity-mismatch/02-data-cleaning-standardization.md)
- [Data Sources Documentation](../../../docs/project_context/data-sources.md)
- [Healthcare Workforce Planning Domain Knowledge](../../../docs/domain_knowledge/healthcare-workforce-planning.md)

## 🤝 Contributing

When adding new analysis scripts or notebooks:
1. Follow the project's Python best practices (see `.github/instructions/python-best-practices.instructions.md`)
2. Use `uv` for package management (NOT pip)
3. Add comprehensive docstrings and type hints
4. Log all operations using `loguru`
5. Save outputs to appropriate directories (`data/`, `results/`, `logs/`)
6. Update this README with execution instructions
