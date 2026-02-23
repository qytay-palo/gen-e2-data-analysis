# Problem Statement 001: Workforce-Capacity Mismatch

**Status**: 🚧 In Progress  
**Priority**: High  
**Owner**: Data Analytics Team

---

## Overview

This problem statement addresses the critical need to understand and quantify potential mismatches between healthcare workforce availability and infrastructure capacity in Singapore's healthcare system. By analyzing temporal trends, sectoral patterns, and workforce-capacity relationships, we aim to identify gaps, forecast future needs, and inform strategic workforce planning.

**Full Problem Statement**: [PS-001 Workforce-Capacity Mismatch](../../docs/objectives/problem_statements/ps-001-workforce-capacity-mismatch.md)

---

## User Stories - Implementation Status

### ✅ User Story 3: Exploratory Workforce and Capacity Analysis (COMPLETED)

**Objective**: Conduct comprehensive EDA to identify patterns, trends, and relationships in workforce and capacity data.

**Status**: ✅ Complete (2026-02-23)

**Deliverables**:
- [x] Statistical analysis module: `src/analysis/workforce_statistics.py`
- [x] Visualization module: `src/visualization/workforce_plots.py`
- [x] Jupyter notebook with executed analysis: `notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb`
- [x] EDA summary report: `docs/methodology/eda-workforce-capacity-summary.md`

**Outputs Generated**:
- **6 PNG visualizations** (300 DPI) in `reports/figures/problem-statement-001/`
- **6 CSV summary tables** in `results/tables/problem-statement-001/`
- **3 JSON statistical metrics** in `results/metrics/problem-statement-001/`

**Key Findings**:
1. All sectors growing at similar rates (~4-7% annually, ANOVA p=0.275)
2. Strong correlation between workforce and bed capacity (r=0.965, p<0.001)
3. FTE-per-bed ratios exceed industry benchmarks (Private ~10.6, Public ~3.9 vs. benchmark 1.5-2.5)
4. Public sector shows fastest growth (6.9% CAGR), driven by nursing expansion

**Execution Instructions**:
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Launch Jupyter notebook
jupyter notebook notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb

# 3. Run all cells (skip cell #13 if composition chart error occurs)
# OR execute via notebook API
```

**Related Documentation**:
- [EDA Summary Report](../../docs/methodology/eda-workforce-capacity-summary.md)
- [User Story 3 Details](../../docs/objectives/user_stories/us-003-exploratory-workforce-capacity-analysis.md)
- [Implementation Verification](./IMPLEMENTATION_VERIFICATION.md#user-story-3)

---

### 🔄 User Story 4: Metrics Calculation and Mismatch Detection (IN PROGRESS)

**Objective**: Calculate quantitative metrics to identify workforce-capacity gaps.

**Status**: ⏳ Pending

**Planned Deliverables**:
- [ ] Metrics calculation module
- [ ] Mismatch detection algorithms
- [ ] Threshold configuration
- [ ] Metrics validation notebook

**Dependencies**: 
- ✅ User Story 3 (EDA) completed - provides benchmark values
- ⏳ Awaiting metric threshold definitions

---

### ⏳ User Story 5: Executive Dashboard Development (PENDING)

**Objective**: Create interactive dashboard for stakeholder consumption.

**Status**: Not started

**Planned Deliverables**:
- [ ] Dashboard design mockups
- [ ] Interactive visualization implementation
- [ ] Data refresh pipeline
- [ ] Deployment documentation

**Dependencies**:
- ⏳ User Story 4 (metrics calculation) must be completed first
- ⏳ Dashboard framework selection required

---

## Project Structure

```
src/problem-statement-001/
├── README.md                          # This file
├── IMPLEMENTATION_VERIFICATION.md     # Validation checklists
├── data_processing/                   # ETL and cleaning scripts
│   └── ... (from User Story 1-2)
├── notebooks/                         # Analysis notebooks
│   └── (linked to main notebooks/ directory)
├── scripts/                           # Automation scripts
│   └── ... (from User Story 1-2)
└── tests/                             # Unit and integration tests
    └── ... (from User Story 1-2)
```

**Note**: This directory serves as the organizational hub for PS-001. Actual code modules reside in `src/analysis/`, `src/visualization/`, etc. following project-wide conventions.

---

## Data Sources

### Input Data
- **Workforce**: `data/3_interim/workforce_clean.parquet`
  - Coverage: 2006-2019 (527 records)
  - Dimensions: Sector × Profession × Year
  
- **Capacity**: `data/3_interim/capacity_clean.parquet`
  - Coverage: 2009-2020 (193 records)
  - Dimensions: Sector × Institution Type × Year

### Generated Outputs
All analysis outputs timestamped with format `YYYYMMDD_HHMMSS`:

- **Figures**: `reports/figures/problem-statement-001/`
- **Tables**: `results/tables/problem-statement-001/`
- **Metrics**: `results/metrics/problem-statement-001/`

---

## Key Modules Developed

### 1. Statistical Analysis (`src/analysis/workforce_statistics.py`)

**Functions**:
- `calculate_growth_rates()` - Year-over-year percentage changes
- `calculate_indexed_growth()` - Baseline-indexed growth values
- `calculate_composition_metrics()` - Percentage distributions by profession
- `calculate_workforce_to_bed_ratio()` - FTE-per-bed intensity metrics
- `test_sector_growth_differences()` - ANOVA/Kruskal-Wallis hypothesis testing
- `test_workforce_capacity_correlation()` - Pearson/Spearman correlation tests

**Usage Example**:
```python
from analysis.workforce_statistics import calculate_growth_rates

growth_df = calculate_growth_rates(
    df=workforce_df,
    value_col='total',
    group_col='sector',
    time_col='year',
    baseline_year=2006
)
```

### 2. Visualization Utilities (`src/visualization/workforce_plots.py`)

**Functions**:
- `plot_temporal_trends()` - Time series line plots with grouping
- `plot_sector_comparison()` - Grouped bar charts (before/after)
- `plot_composition_stacked()` - Stacked area charts for composition
- `plot_workforce_capacity_scatter()` - Scatter plots with regression lines
- `plot_growth_rate_comparison()` - Bar charts with error bars

**Usage Example**:
```python
from visualization.workforce_plots import plot_temporal_trends

fig = plot_temporal_trends(
    df=workforce_df,
    time_col='year',
    value_col='total',
    group_col='sector',
    title='Workforce Trends by Sector',
    output_path='reports/figures/trends.png',
    dpi=300
)
```

---

## Reproducibility

### Environment Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/gen-e2-data-analysis.git
cd gen-e2-data-analysis

# 2. Create virtual environment with uv
uv venv
source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
uv pip install -r requirements.txt
```

### Data Preparation
User Stories 1-2 (data extraction and cleaning) must be completed first:
```bash
# Run cleaning pipeline
python scripts/clean_workforce_capacity_data.py

# Verify data quality
pytest tests/data/test_cleaned_data_quality.py
```

### Analysis Execution
```bash
# Option 1: Interactive notebook
jupyter notebook notebooks/2_analysis/exploratory_workforce_capacity_analysis.ipynb

# Option 2: Command-line execution (future implementation)
python scripts/run_eda_workforce_capacity.py
```

---

## Testing Strategy

### Unit Tests
```bash
# Test statistical functions
pytest tests/unit/test_workforce_statistics.py -v

# Test visualization functions
pytest tests/unit/test_workforce_plots.py -v
```

### Data Validation Tests
```bash
# Validate cleaned data schema and quality
pytest tests/data/test_cleaned_data_quality.py -v
```

### Integration Tests
```bash
# Test end-to-end pipeline
pytest tests/integration/test_eda_pipeline.py -v
```

---

## Performance Considerations

- **Data Loading**: Using Polars for efficient parquet reading (~10-50ms for datasets)
- **Visualization Rendering**: Matplotlib with GPU acceleration disabled for reproducibility
- **Memory Usage**: Peak ~500MB during full notebook execution
- **Execution Time**: Complete EDA notebook runs in ~2-3 minutes

---

## Known Issues and Limitations

### Issue 1: Composition Stacked Chart Error
**Description**: Cell #13 in EDA notebook fails with "Index contains duplicate entries" during pivot operation.

**Impact**: Minor - one visualization missing out of seven total charts.

**Workaround**: Skip cell #13; composition analysis still available via summary tables.

**Status**: 🐛 Open - pending fix in `src/visualization/workforce_plots.py`

### Issue 2: Missing 2020 Workforce Data
**Description**: Capacity data extends to 2020 but workforce data ends at 2019.

**Impact**: Limits joint analysis to 2009-2019 period only.

**Workaround**: None - data gap in source systems.

**Status**: 📊 Data limitation - documented in EDA summary report

---

## Next Steps

### Immediate Priorities
1. ✅ **Complete User Story 3** - DONE
2. 🔄 **Start User Story 4**: Metrics calculation module implementation
3. 📋 **Define metric thresholds**: Based on EDA findings, establish sector-specific benchmarks

### Future Enhancements
- Fix composition stacked chart pivot error
- Expand profession coverage to include allied health professionals
- Incorporate institution-level granularity (beyond sector aggregation)
- Add forecasting models for workforce demand projection

---

## References

- [Problem Statement Document](../../docs/objectives/problem_statements/ps-001-workforce-capacity-mismatch.md)
- [User Story Backlog](../../docs/objectives/user_stories/README.md)
- [EDA Summary Report](../../docs/methodology/eda-workforce-capacity-summary.md)
- [Data Dictionary](../../docs/data_dictionary/)
- [Coding Standards](.github/instructions/python-best-practices.instructions.md)

---

**Last Updated**: 2026-02-23  
**Contributors**: Data Science Team  
**Contact**: For questions, consult project documentation or open an issue.
