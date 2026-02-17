# Instructions Directory

This directory contains **instruction files** that define mandatory best practices, standards, and guidelines for the data analysis project. Each instruction file targets specific stages of the data analysis lifecycle or specific file types.

## 📚 Instruction Files Overview

### 1. **General Standards**

#### [python-best-practices.instructions.md](python-best-practices.instructions.md)
- **Applies To**: `**/*.py`, `**/*.ipynb`
- **Purpose**: Python coding conventions, code organization, and best practices
- **Key Topics**:
  - Code organization and structure
  - Data handling with Polars
  - Memory management
  - Error handling and logging
  - Type hints and documentation

#### [data-analysis-best-practices.instructions.md](data-analysis-best-practices.instructions.md)
- **Applies To**: `docs/objectives/problem_statements/*`, `docs/objectives/user_stories/*`
- **Purpose**: Overall data analysis workflow and lifecycle best practices
- **Key Topics**:
  - Folder structure and file organization
  - Logger setup and usage
  - Data immutability rules
  - Documentation standards
  - General workflow principles

#### [data-analysis-folder-structure.instructions.md](data-analysis-folder-structure.instructions.md)
- **Applies To**: `src/problem-statement-*/**`
- **Purpose**: Standard project structure and organization
- **Key Topics**:
  - Directory hierarchy
  - Phase-based organization
  - File placement guidelines
  - Initialization steps

---

### 2. **Data Pipeline Stages**

#### [data-extraction-loading.instructions.md](data-extraction-loading.instructions.md)
- **Applies To**: 
  - `data/1_raw/**`
  - `data/2_external/**`
  - `src/data_processing/*loader*.py`
  - `src/data_processing/*connector*.py`
  - `src/data_processing/*extractor*.py`
  - `scripts/extract*.py`
  - `notebooks/1_exploratory/*extract*.ipynb`
  - `sql/extractions/**`
- **Purpose**: Standards for extracting and loading data from various sources
- **Key Topics**:
  - Data immutability (never modify raw data)
  - Source documentation and metadata
  - SQL extraction templates
  - API extraction with retry logic
  - Reproducible extraction workflows

#### [data-validation-quality.instructions.md](data-validation-quality.instructions.md)
- **Applies To**:
  - `src/data_processing/*validator*.py`
  - `src/data_processing/*quality*.py`
  - `src/data_processing/*profiler*.py`
  - `data/3_interim/**`
  - `logs/etl/**`
  - `tests/data/**`
  - `notebooks/1_exploratory/*profile*.ipynb`
  - `notebooks/1_exploratory/*quality*.ipynb`
- **Purpose**: Data quality assurance and validation standards
- **Key Topics**:
  - Schema validation
  - Data quality profiling
  - Business rule validation
  - Quality metrics tracking
  - Validation workflow templates

---

### 3. **Analysis Stages**

#### [exploratory-data-analysis.instructions.md](exploratory-data-analysis.instructions.md)
- **Applies To**:
  - `notebooks/1_exploratory/**`
  - `notebooks/2_analysis/*exploratory*.ipynb`
  - `src/analysis/*eda*.py`
  - `reports/figures/exploratory/**`
- **Purpose**: Best practices for initial data exploration and hypothesis generation
- **Key Topics**:
  - Structured EDA workflow
  - Univariate, bivariate, and multivariate analysis
  - Visualization best practices
  - Finding documentation
  - Reproducible notebooks

#### [feature-engineering.instructions.md](feature-engineering.instructions.md)
- **Applies To**:
  - `src/features/**`
  - `notebooks/3_feature_engineering/**`
  - `src/data_processing/*transform*.py`
  - `src/data_processing/*feature*.py`
- **Purpose**: Standards for creating, transforming, and selecting features
- **Key Topics**:
  - Temporal features (lags, rolling windows)
  - Domain-specific features (outbreak indicators, seasonality)
  - Feature scaling and encoding
  - Feature selection methods
  - Avoiding data leakage

#### [modeling-forecasting.instructions.md](modeling-forecasting.instructions.md)
- **Applies To**:
  - `src/models/**`
  - `notebooks/2_analysis/*model*.ipynb`
  - `notebooks/2_analysis/*forecast*.ipynb`
  - `models/**`
  - `results/metrics/**`
- **Purpose**: Best practices for building and evaluating predictive models
- **Key Topics**:
  - Baseline model establishment
  - Time series modeling (SARIMAX, Exponential Smoothing)
  - Machine learning models
  - Model evaluation and metrics
  - Model registry and versioning

---

### 4. **Communication & Quality Assurance**

#### [visualization-reporting.instructions.md](visualization-reporting.instructions.md)
- **Applies To**:
  - `src/visualization/**`
  - `reports/figures/**`
  - `reports/dashboards/**`
  - `reports/presentations/**`
  - `notebooks/**/`
  - `results/exports/**`
- **Purpose**: Standards for creating effective visualizations and reports
- **Key Topics**:
  - Chart type selection
  - Audience-appropriate design
  - Publication-quality figures
  - Dashboard design principles
  - Report templates

#### [testing-validation.instructions.md](testing-validation.instructions.md)
- **Applies To**:
  - `tests/**`
  - `**/*.py`
  - `src/**`
- **Purpose**: Testing and code quality assurance standards
- **Key Topics**:
  - Unit testing
  - Integration testing
  - Data validation testing
  - Test automation and CI/CD
  - Code coverage requirements

---

## 🎯 How to Use These Instructions

### For AI Assistants (GitHub Copilot)
The instruction files are automatically applied based on the `applyTo` glob patterns in each file's frontmatter. When working on files matching these patterns, the AI will follow the guidelines defined in the corresponding instruction file.

### For Developers
1. **Before starting a new task**, review the relevant instruction file(s)
2. **Reference templates** provided in the instruction files
3. **Follow checklists** at the end of each instruction file
4. **Use anti-pattern examples** to avoid common mistakes

### Finding the Right Instruction File

**By Task Type:**
- Extracting data → [data-extraction-loading.instructions.md](data-extraction-loading.instructions.md)
- Cleaning data → [data-validation-quality.instructions.md](data-validation-quality.instructions.md)
- Exploring data → [exploratory-data-analysis.instructions.md](exploratory-data-analysis.instructions.md)
- Creating features → [feature-engineering.instructions.md](feature-engineering.instructions.md)
- Building models → [modeling-forecasting.instructions.md](modeling-forecasting.instructions.md)
- Creating visualizations → [visualization-reporting.instructions.md](visualization-reporting.instructions.md)
- Writing tests → [testing-validation.instructions.md](testing-validation.instructions.md)

**By File Location:**
```bash
# Working in src/data_processing/loader.py
→ Use: data-extraction-loading.instructions.md, python-best-practices.instructions.md

# Working in notebooks/1_exploratory/eda.ipynb
→ Use: exploratory-data-analysis.instructions.md, python-best-practices.instructions.md

# Working in src/features/
→ Use: feature-engineering.instructions.md, python-best-practices.instructions.md

# Working in src/models/
→ Use: modeling-forecasting.instructions.md, python-best-practices.instructions.md

# Working in tests/
→ Use: testing-validation.instructions.md, python-best-practices.instructions.md
```

---

## 🔑 Key Principles Across All Instructions

### 1. **Reproducibility**
- Set random seeds
- Save parameters and configurations
- Version control all code
- Document data sources

### 2. **Documentation**
- Clear docstrings for all functions
- Inline comments for complex logic
- README files in major directories
- Metadata for all outputs

### 3. **Data Integrity**
- Never modify raw data (`data/1_raw/`)
- Validate at every stage
- Track data lineage
- Log transformations

### 4. **Code Quality**
- Type hints for function signatures
- Comprehensive error handling
- Unit tests for critical logic
- >80% test coverage target

### 5. **Separation of Concerns**
- Raw data separate from processed
- Notebooks for exploration, scripts for production
- Configuration separate from code
- Clear folder organization

---

## 📊 Instruction File Relationship Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     General Standards                           │
│  ┌───────────────────┐  ┌──────────────────────────────────┐   │
│  │ Python Best       │  │ Data Analysis Best Practices &   │   │
│  │ Practices         │  │ Folder Structure                 │   │
│  └───────────────────┘  └──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Pipeline Stages                          │
│                                                                 │
│  1. Extraction ───► 2. Validation ───► 3. EDA                  │
│                                                                 │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │ Data        │   │ Data         │   │ Exploratory  │        │
│  │ Extraction  │   │ Validation   │   │ Data         │        │
│  │ & Loading   │   │ & Quality    │   │ Analysis     │        │
│  └─────────────┘   └──────────────┘   └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Modeling Pipeline                             │
│                                                                 │
│  4. Feature Engineering ───► 5. Modeling ───► 6. Reporting     │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │ Feature      │   │ Modeling &   │   │ Visualization│       │
│  │ Engineering  │   │ Forecasting  │   │ & Reporting  │       │
│  └──────────────┘   └──────────────┘   └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Quality Assurance                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Testing & Code Validation                                │  │
│  │ (Applied throughout all stages)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Maintenance

### Updating Instructions
When updating instruction files:
1. Update the relevant `.instructions.md` file
2. Update the `applyTo` glob patterns if file locations change
3. Update this README if new instruction files are added
4. Test that AI assistants correctly apply the instructions

### Adding New Instructions
To add a new instruction file:
1. Create `[topic-name].instructions.md` in this directory
2. Include frontmatter with `name`, `description`, and `applyTo` fields
3. Follow the existing template structure
4. Update this README with the new file
5. Update the main project's [.github/copilot-instructions.md](..//copilot-instructions.md) if needed

---

## 📞 Questions or Issues?

If you find issues with these instructions or need clarification:
1. Review the specific instruction file in question
2. Check the anti-patterns section for common mistakes
3. Refer to code examples in the instruction files
4. Consult the main project documentation in `docs/`

---

**Last Updated**: February 17, 2026  
**Version**: 1.0.0
