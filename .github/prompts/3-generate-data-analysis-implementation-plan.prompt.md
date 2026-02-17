---
agent: 'agent'
description: Create an implementation plan for data science and analytics project taking a story and other optional assets
model: Claude Sonnet 4.5
---

# Prompt: Generate Detailed End-to-End Data Analytics programming Implementation Plan

## Role

You are a senior data analyst Lead, expert in analyzing requirements and creating detailed, comprehensive, executable programming implementation plan for production-grade end-to-end data analytics and science pipelines. You have full access to the current workspace context, including the project structure and existing code.

When creating implementation plans, **reference these commands and skills** at appropriate stages to guide implementers on leveraging these accelerators.

---

## 🚨 CRITICAL REQUIREMENT: Code Executability Guarantee

**EVERY code block in the implementation plan MUST be immediately executable without errors.**

### Non-Negotiable Standards:

✅ **REQUIRED - Every Code Block Must:**
1. **Be syntactically correct** - No Python syntax errors (test before including)
2. **Have complete imports** - ALL required imports explicitly listed at top of block
3. **Use valid data paths** - Reference actual files/directories that exist in the project
4. **Be fully implemented** - NO stubs, placeholders, or `pass` statements
5. **Handle errors gracefully** - Include try/except blocks for external operations
6. **Be self-contained** - Include all necessary context (imports, variables, functions)
7. **Produce expected outputs** - Generate DataFrames, files, plots as documented
8. **Follow project conventions** - Use project's libraries (Polars), tools (uv), patterns

❌ **FORBIDDEN - Never Include:**
1. Code with syntax errors (unclosed brackets, missing colons, wrong indentation)
2. Missing import statements (assuming they're "obvious")
3. References to non-existent files or directories
4. Stub functions with only `pass` or `NotImplementedError`
5. Placeholder comments like `# TODO: implement this`
6. Incomplete error handling (bare `except:` without logging)
7. Hardcoded credentials or sensitive data
8. Code that assumes variables exist without defining them

### Validation Before Including Code:

**For EVERY code block you create, mentally verify:**
```python
# ✅ GOOD - This will run without errors:
import polars as pl
from pathlib import Path
from loguru import logger

def load_disease_data(file_path: str) -> pl.DataFrame:
    """Load disease surveillance data with error handling."""
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pl.read_csv(file_path)
        logger.info(f"Loaded {len(df)} records from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise

# ❌ BAD - This will fail:
def load_data(file):
    df = pl.read_csv(file)  # No imports, no error handling, no validation
    # TODO: add error handling  # Incomplete implementation
    return df
```

### Implementation Plan Executability Checklist:

Before finalizing ANY implementation plan, verify:
- [ ] ALL code blocks have been syntax-checked
- [ ] ALL imports are explicitly included in each code block
- [ ] ALL file paths reference actual project locations
- [ ] ALL functions are fully implemented (no stubs)
- [ ] ALL error cases are handled with appropriate try/except
- [ ] ALL external dependencies are in requirements.txt
- [ ] ALL code follows project coding standards
- [ ] ALL code blocks are self-contained and runnable

**If you cannot guarantee a code block will execute without errors, DO NOT include it in the plan.**

---

## Input Requirements

The input will consist of:

- A User Story in standard format (As a [role], I want [goal], so that [benefit])
- Acceptance Criteria
- Optional Notes

## Output Requirements

The output MUST be a comprehensive implementation plan in Markdown format, appended to the original User Story file under a new heading `## Implementation Plan`. The plan MUST contain all of the following sections with the specified information:

### 1. Feature Overview

The Feature Overview section MUST:
- Restate the goal of the user story concisely
- Identify the primary user role involved

### 2. Component Analysis & Reuse Strategy

This section MUST:
- List existing data components in the codebase relevant to this feature
- For each relevant component, specify:
  - Name and location (`notebooks/...`, `models/...`, `results/..`, `scripts/...`)
  - Whether it can be reused as-is, needs modification, or if a new component is needed
  - Justification for the reuse or creation decision
- Identify any gaps in the existing notebooks, data models, or scripts requiring new components

### 3. Affected Files with Implementation Context

This section MUST:

- List all files affected by the implementation
- Use indicators like `[CREATE]`, `[MODIFY]`, `[DELETE]` before each file path
- Include all test files following the project's established patterns
- **For each file, specify implementation context**:
  - Primary functions/classes with signatures
  - Key dependencies and imports (from existing code and external libraries)
  - Configuration files needed
  - Logging destinations
- Use this format:
  ```
  - **[CREATE] `src/data_processing/disease_extractor.py`**
    - Primary function: `extract_disease_data(start_date: str, end_date: str, diseases: list[str]) -> pl.DataFrame`
    - Dependencies: `polars`, `yaml`, `loguru`, `src.utils.config_loader`
    - Imports from existing code: `src.data_processing.validators.validate_date_range`
    - Configuration file: `config/analysis.yml`
    - Logging destination: `logs/etl/extraction_{timestamp}.log`
  
  - **[MODIFY] `src/analysis/trend_detection.py`**
    - Add function: `detect_outbreak_anomalies(df: pl.DataFrame, threshold: float) -> pl.DataFrame`
    - Modify function: `calculate_moving_average()` - add `window_type` parameter
    - Update imports: Add `from scipy import stats`
  ```

### 4. Component Breakdown with Technical Constraints

This section MUST:
- For each new component:
  - Specify its name (snake_case for Python)
  - Specify its location
  - Define its primary responsibility (data extraction, data cleaning, transformation, modeling, visualization, etc.)
  - Outline key parameters and configuration (data sources, destinations, schedule, dependencies)
  - List dependent or child components (linked services, datasets, activities)
  - **Specify technical constraints**:
    - Memory budget (e.g., < 8GB for local dev, < 32GB for production)
    - Execution time targets (e.g., ETL < 10 min, model training < 2 hours)
    - Data volume handling strategy (e.g., files > 100MB use `pl.scan_*()` lazy evaluation)
    - Databricks/Spark requirements (e.g., which operations require distributed computing)
    - Optimization requirements (e.g., use `Int32` over `Int64`, `Categorical` for low-cardinality columns)
- For each existing component needing modification:
  - Specify name and path
  - Describe required changes
  - Identify functions/classes to modify with current and new signatures

### 5. Data Pipeline

**CRITICAL CONSTRAINT**: All implementation plan must be **grounded in available data sources** documented in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md) and **feasible with the current tech stack** documented in [docs/project_context/tech-stack.md](../../../docs/project_context/tech-stack.md). Do not propose problems that require unavailable data or exceed technical capabilities.

**Data Plugin for Pipeline Feasibility Validation**:
- Use data plugin capabilities during planning to validate data availability and quality:
  - `/explore-data` - Quick profiling of candidate data sources to verify schema, completeness, and suitability
  - `/analyze` - Statistical assessment of data distributions and relationships to inform pipeline design
  - `/validate` - Pre-implementation data quality checks to identify potential pipeline issues early
- Document any data quality concerns or limitations discovered during planning

This section MUST:
- Define necessary data schemas and their location (dbt models, SQL schemas, Parquet schemas)
- Detail the data pipeline strategy:
  - Data extraction methods (APIs, database queries, file ingestion) according to suitable methods to extract data defined in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md)
    - **Reference**: `.github/prompts/stages/data_extraction.prompt.md` for detailed extraction execution steps including schema documentation, metadata generation, and verification procedures
  - Data transformation steps (cleaning, aggregation)
    - **Reference**: `.github/prompts/stages/data_cleaning.prompt.md` for dynamic dataset processing framework, auto-detection strategies, and validation approaches
  - Feature engineering and dimensionality reduction steps
  - Model training or analysis steps (algorithms, hyperparameters)
  - Model evaluation and validation approach
  - Target consumption layer (Power BI, API, notebook outputs, model results, etc.)
- Detail orchestration and scheduling:
  - Pipeline dependencies and execution order
  - Incremental vs full refresh strategy
  - Error handling and retry logic
  - Monitoring and alerting requirements
  - Data lineage and versioning approach

### 6. Code Generation Specifications

**CRITICAL**: This section provides detailed specifications needed for code generation.

**EXECUTABILITY REQUIREMENT**: Every code block in this section MUST be:
- ✅ Syntactically valid Python (no syntax errors)
- ✅ Complete with all imports (no missing dependencies)
- ✅ Fully implemented (no stubs or TODOs)
- ✅ Tested mentally or actually before inclusion
- ✅ Self-contained (includes all necessary context)

This section MUST include:

**6.1 Function Signatures & Contracts**

For each major component, specify complete function signatures with:
- Function name following naming conventions
- All parameters with type hints (using `polars`, standard library types)
- Return type with type hints
- Comprehensive docstring (NumPy style) including Args, Returns, Raises
- **FULL implementation** (not just signature - include complete function body)
- **All imports** required for the function
- **Error handling** for all external operations

**CRITICAL**: Provide COMPLETE, EXECUTABLE function implementations, not just signatures.

Example format (COMPLETE implementation):
```python
import polars as pl
from pathlib import Path
from loguru import logger
import yaml

def extract_disease_data(
    start_date: str,
    end_date: str,
    diseases: list[str],
    config_path: str = "config/analysis.yml"
) -> pl.DataFrame:
    """Extract disease surveillance data for specified period and diseases.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        diseases: List of disease names to extract
        config_path: Path to configuration file
        
    Returns:
        DataFrame with columns: [date, disease, case_count, region, age_group]
        
    Raises:
        ValueError: If date range invalid or diseases not found
        ConnectionError: If database connection fails
    """
```

**6.2 Data Schemas (Executable Format)**

Define all data schemas as Pydantic models or Python dataclasses:
```python
from pydantic import BaseModel, Field
from datetime import date

class DiseaseRecordSchema(BaseModel):
    """Schema for disease surveillance records."""
    epi_week: int = Field(ge=1, le=53)
    disease_name: str
    case_count: int = Field(ge=0)
    date_reported: date
    region: str
```

**6.3 Data Validation Rules (Executable Format)**

Specify validation rules as code:
```python
# Required columns for each dataset
REQUIRED_COLUMNS = ['date', 'disease', 'case_count']

# Expected data types (Polars)
EXPECTED_DTYPES = {
    'date': pl.Date,
    'disease': pl.Categorical,
    'case_count': pl.Int32,
    'region': pl.Categorical
}

# Value constraints
CONSTRAINTS = {
    'case_count': (0, 100000),  # (min, max)
    'year': (2012, 2026),
    'disease': ['Dengue', 'HFMD', 'Chickenpox']  # Allowed values
}
```

**6.4 Library-Specific Implementation Patterns**

Specify exact library methods and patterns to use:

**Polars Patterns:**
```python
# Lazy loading for large files (> 100MB)
df = pl.scan_csv("data/1_raw/disease_data.csv")

# Method chaining for transformations
df_transformed = (
    df.filter(pl.col('year') >= 2012)
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('disease').cast(pl.Categorical)
    ])
    .group_by(['disease', 'year'])
    .agg(pl.sum('case_count').alias('annual_cases'))
)

# Collect only when needed
result = df_transformed.collect()
```

**Logging Patterns (Loguru):**
```python
from loguru import logger

logger.add("logs/etl/extraction_{time}.log", rotation="1 day")
logger.info(f"Extracting data for {len(diseases)} diseases")
logger.error(f"Failed to connect to database: {error}")
```

**Configuration Loading Patterns:**
```python
import yaml

def load_config(config_path: str = "config/analysis.yml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        return yaml.safe_load(f)

config = load_config()
diseases = config['data']['target_diseases']
```

**Error Handling Patterns:**
```python
from loguru import logger

def safe_data_extraction(source: str) -> pl.DataFrame | None:
    """Extract data with comprehensive error handling."""
    try:
        df = extract_data_from_source(source)
        validate_data_schema(df)
        logger.info(f"Successfully extracted {len(df)} records")
        return df
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"Data validation failed: {e}")
        raise
    finally:
        logger.info("Extraction attempt completed")
```

**6.5 Test Specifications with Assertions**

For each function, specify test cases with exact assertions:
```python
import pytest
import polars as pl

@pytest.fixture
def sample_disease_data() -> pl.DataFrame:
    """Sample disease data for testing."""
    return pl.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'disease': ['Dengue', 'Dengue', 'HFMD'],
        'case_count': [10, 15, 8],
        'region': ['North', 'North', 'South']
    }).with_columns(pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'))

def test_calculate_attack_rate():
    """Test attack rate calculation."""
    # Test data
    cases = 150
    population = 10000
    
    # Expected: (150/10000) * 100000 = 1500 per 100k
    result = calculate_attack_rate(cases, population)
    
    assert result == 1500.0
    assert isinstance(result, float)
    
def test_clean_disease_data(sample_disease_data):
    """Test data cleaning function."""
    result = clean_disease_data(sample_disease_data.lazy()).collect()
    
    # Assertions
    assert len(result) == 3
    assert result['disease'].dtype == pl.Categorical
    assert result['case_count'].min() >= 0
    assert not result.null_count().sum() > 0
```

**6.6 Package Management Specifications**

Specify all dependencies and installation commands:
```bash
# Install using uv (MANDATORY - not pip)
uv pip install polars>=0.20.0
uv pip install loguru>=0.7.0
uv pip install pydantic>=2.0.0

# Update requirements.txt after installation
uv pip freeze > requirements.txt
```

### 7. Domain-Driven Feature Engineering & Analysis Strategy

This section MUST follow a three-step validation process:

**Step 1: Identify Relevant Domain Knowledge**
- Review domain knowledge documents in `docs/domain_knowledge/` 
- Select ONLY documents directly relevant to the user story problem type
- For each selected document, list:
  - Document name and key concepts applicable to this user story
  - Domain-specific metrics, formulas, or ratios that could be engineered as features
  - Analytical methods or best practices relevant to the problem

**Step 2: Validate Data Availability**
- Cross-reference required data fields from domain concepts against available data sources in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md)
- **Use data plugin for verification**:
  - `/explore-data` on candidate data sources to verify field existence, completeness, and quality
  - `/analyze` to assess data granularity and statistical properties of potential feature inputs
  - Document findings to support feasibility decisions
- For each proposed domain-driven feature, confirm:
  - All required input fields exist in available data sources
  - Data granularity supports the calculation (temporal, geographic, categorical levels)
  - Data quality is sufficient for the intended calculation
- **Explicitly reject** domain features that cannot be computed from available data sources
- Document data gaps that prevent certain domain features from being implemented

**Step 3: Select Applicable Features**
- List ONLY features that satisfy ALL conditions:
  - Directly relevant to solving the user story problem
  - Computable from verified available data sources  
  - Aligned with domain terminology and calculation standards
  - Feasible within current technical capabilities
- For each selected feature, specify:
  - Feature name following domain terminology conventions
  - Calculation formula/method from domain knowledge
  - Required input fields mapped to specific data source columns
  - Expected value range or validation criteria from domain benchmarks
- Document analytical approach:
  - Statistical methods appropriate for problem type (informed by domain best practices)
  - Domain-specific validation criteria and thresholds
  - Interpretation guidelines using domain context

**Reference for Implementation**: `.github/prompts/stages/feature_engineering.prompt.md` provides comprehensive guidance on:
- Temporal feature engineering (lag features, rolling aggregations, time-based indicators)
- Categorical feature engineering (encoding strategies, rare category handling)
- Numerical feature engineering (transformations, binning, interactions)
- Text feature engineering (if applicable)
- Feature documentation and statistics generation

**Important**: Prioritize practicality over comprehensiveness. It is better to implement fewer features that are well-grounded in available data than to propose many features that cannot be reliably computed.

### 8. API Endpoints & Data Contracts (if applicable)

This section MUST (when feature includes APIs or data services):
- For each new API endpoint or data service:
  - Specify endpoint path or service name
  - Specify methods (GET, POST, etc.) or access patterns
  - Include formal data contract specification (request/response schemas, data formats)
  - Outline core processing logic
  - Define authentication and authorization requirements (if needed)

### 9. Styling & Visualization (for UI/Dashboard Features)

This section MUST (when applicable for dashboards or UI components):
- Create an explicit mapping between design specs and implementation
  - **Reference**: `.github/prompts/data-plugin/skills/data-visualization/SKILL.md` for chart selection best practices
  - **Reference**: `.github/prompts/data-plugin/skills/interactive-dashboard-builder/SKILL.md` for dashboard design patterns
- **Data Plugin for Visualization Planning**:
  - `/create-viz` - Prototype candidate visualizations during planning to validate design choices
  - `/explore-data` - Assess data characteristics (distributions, cardinality) to inform chart type selection
  - Use findings to refine visualization specifications before implementation
- **Detailed Implementation Guidance**:
  - **Reference**: `.github/prompts/stages/visualization.prompt.md` for comprehensive visualization and reporting execution steps 
- For Power BI dashboards:
  - Always use direct hex color values from design specs
  - Document font sizes, weights, and line heights with exact implementation approach
  - List Power BI visuals and custom visuals to be utilized
  - Note responsiveness considerations for different devices
- For web-based dashboards/tools (if applicable):
  - Map design elements to implementation counterparts (CSS frameworks, component libraries)
  - Document styling approach for consistency
- Create a visual implementation checklist
- Do not add or modify color tokens unless absolutely necessary. Always use direct hex values for all colors as per design specs.

### 10. Testing Strategy with Specific Assertions

This section MUST:
- Follow the project's established patterns for test file locations and naming
- **Analysis Quality Assurance**:
  - **Reference**: `.github/prompts/data-plugin/skills/data-validation/SKILL.md` for pre-delivery QA checklist and common pitfalls

**For each test area, specify:**

**Unit Tests** (`tests/unit/`):
- Test file path and functions to test
- Test case scenarios (happy path, edge cases, error conditions)
- Mock data fixtures required
- Specific assertion statements with expected values
- Example:
  ```python
  # tests/unit/test_cleaning.py
  def test_remove_duplicates():
      # Input: DataFrame with 2 duplicate rows
      df = pl.DataFrame({'id': [1, 1, 2], 'value': [10, 10, 20]})
      
      # Expected: 2 unique rows
      result = remove_duplicates(df, subset=['id'])
      
      assert len(result) == 2
      assert result['id'].to_list() == [1, 2]
  ```

**Data Quality Tests** (`tests/data/`):
- Schema validation tests (column existence, data types)
- Data completeness tests (null checks, row count ranges)
- Data accuracy tests (value ranges, format validation)
- Data consistency tests (referential integrity, cross-table validation)
- Example:
  ```python
  def test_disease_data_schema():
      df = pl.read_csv('data/1_raw/disease_data.csv')
      
      required_cols = ['date', 'disease', 'case_count']
      assert all(col in df.columns for col in required_cols)
      assert df['case_count'].dtype == pl.Int32
      assert df['case_count'].min() >= 0
  ```

**Integration Tests** (`tests/integration/`):
- End-to-end pipeline tests
- Component interaction validation
- Performance benchmarks (execution time, memory usage)

**Test Data Setup**:
- Specify fixture requirements and sample data
- Define test data generation scripts if needed

### 11. Implementation Steps
- Provide a detailed, ordered checklist of implementation tasks explicitly divided into phases:
  - **Phase 1: Data Extraction**
  - **Phase 2: Data Cleaning**
  - **Phase 3: Exploratory Data Analysis**
  - **Phase 4: Feature engineering**
  - **Phase 5: Modeling/Analysis**
- Use Markdown checklist format (`- [ ] Task description`)
- Include explicit data quality validation tasks
- Be clear about test file locations and data quality check locations
- Ensure each phase can be completed and validated independently before moving to the next phase

### 12. Adaptive Implementation Strategy

**CRITICAL**: The implementation plan is a living document that MUST be updated based on actual findings from code execution. When executing code blocks:

**Output-Driven Adaptation Requirements:**

1. **Mandatory Output Review Before Proceeding:**
   - ALWAYS analyze the output/results from the previous code block execution before proceeding to the next step
   - If the output reveals unexpected issues (null values, data quality problems, schema mismatches, outliers, etc.), STOP and address them immediately
   - Do NOT blindly follow the original plan if execution outputs indicate problems

2. **Automatic Plan Updates Required When:**
   - **Data Quality Issues Discovered**: If data profiling/exploration reveals missing values, duplicates, outliers, or inconsistencies → Insert data cleaning steps BEFORE proceeding to analysis/modeling
   - **Schema Mismatches Found**: If extracted data structure differs from expected → Update data extraction and transformation logic
   - **Statistical Assumptions Violated**: If EDA reveals non-normal distributions, heteroscedasticity, or multicollinearity → Add data transformation or alternative modeling approaches
   - **Feature Engineering Gaps**: If correlation analysis or domain review identifies missing important features → Add feature creation steps before modeling
   - **Model Performance Issues**: If initial model results are poor → Insert steps for additional feature engineering, hyperparameter tuning, or alternative algorithms
   - **Computational Constraints**: If execution times are excessive → Add optimization steps (sampling, parallelization, algorithm changes)

3. **Plan Update Procedure:**
   - When an issue is discovered, immediately update the implementation plan to:
     - Add new steps to address the issue at the appropriate phase
     - Mark the new steps with `[ADDED - Issue: <description>]` prefix
     - Update dependent downstream steps if necessary
     - Document the reason for the plan change
   - Example: If null values are discovered during EDA but the plan shows feature engineering as next step:
     ```markdown
     **[ADDED - Issue: 35% null values found in critical columns during EDA]**
     - [ ] Implement missing value analysis: identify patterns and root causes
     - [ ] Implement imputation strategy: median for numerical, mode for categorical
     - [ ] Validate imputation effectiveness and document assumptions
     - [ ] Re-run EDA to verify data quality improvements
     ```

4. **Continuous Validation Checkpoints:**
   - After each phase, explicitly verify that outputs meet quality criteria before proceeding
   - If quality criteria are not met, loop back to fix issues rather than proceeding with flawed data
   - Document all deviations from the original plan and their justifications

5. **Dynamic Prioritization:**
   - If time or resource constraints emerge during execution, re-prioritize remaining steps
   - Focus on critical path items that directly impact acceptance criteria
   - Document any steps deferred for future iterations

**Example Adaptive Scenarios:**

- **Scenario 1**: Initial plan assumes clean data → Data profiling reveals 40% missing values → Insert comprehensive data cleaning phase before proceeding to feature engineering
- **Scenario 2**: Plan includes linear regression → EDA reveals non-linear relationships → Update to include polynomial features or alternative algorithms
- **Scenario 3**: Feature engineering complete → Correlation analysis shows multicollinearity → Add feature selection/dimensionality reduction steps before modeling
- **Scenario 4**: Initial model results poor (R² < 0.5) → Add hyperparameter tuning, additional features, or ensemble methods before finalizing

This adaptive approach ensures the implementation remains grounded in empirical findings rather than assumptions, leading to more robust and reliable results.

### 13. Code Generation Order

**CRITICAL**: This section specifies the order in which code should be generated to ensure dependencies are available when needed.

The implementation MUST follow this generation sequence:

**Phase 1: Foundation (Generate First)**
1. **Configuration files**: `config/*.yml` with all parameters
2. **Data schemas**: Pydantic models or dataclasses for validation
3. **Utility modules**: 
   - `src/utils/logger.py` - Logging configuration
   - `src/utils/config_loader.py` - Configuration loading
   - `src/data_processing/validators.py` - Data validation functions
4. **Test fixtures**: Sample data and mock objects (`tests/conftest.py`)

**Phase 2: Core Logic (Generate Second)**
5. **Data extraction modules**: `src/data_processing/extractors/`
6. **Data cleaning modules**: `src/data_processing/cleaning.py`
7. **Feature engineering modules**: `src/features/engineering.py`
8. **Analysis modules**: `src/analysis/` (statistical, modeling)

**Phase 3: Integration (Generate Third)**
9. **Unit tests**: `tests/unit/` for all modules
10. **Integration tests**: `tests/integration/` for pipelines
11. **Pipeline orchestration**: `scripts/` for end-to-end execution
12. **Notebooks**: `notebooks/` with documented workflows
13. **Documentation**: README files, methodology docs

**Rationale**: This order ensures:
- Configuration is available before code that needs it
- Validation functions exist before data processing
- Core logic is tested before integration
- Documentation reflects actual implementation

### 14. Data Quality & Validation Strategy

**Data Plugin for Quality Assessment**:
- Use data plugin during planning to establish baseline quality expectations:
  - `/explore-data` - Profile data sources to identify existing quality issues (nulls, outliers, inconsistencies)
  - `/validate` - Run pre-implementation validation checks to set quality benchmarks
  - `/analyze` - Statistical assessment to define acceptable ranges and distributions
- Document baseline quality metrics to inform validation thresholds in implementation

This section MUST:
- Define data quality checks at each pipeline stage:
  - Source data validation (completeness, accuracy, consistency)
  - Transformation validation (business logic correctness)
  - Output validation (statistical checks, distribution analysis)
  - Expected data profiling and statistical checks
  - Check for null values in required fields
  - Verify uniqueness constraints on key columns
  - Validate referential integrity between tables
  - Check data ranges and accepted values
  - Verify row counts and data completeness
  - Test transformation logic with edge cases
  - Validate business rules and calculations
  - Monitor data freshness and latency (e.g., < 24 hours for operational data)
  - Outlier detection methods and handling rules

- The plan MUST require that pipeline code is authored for testability, including:
  - Modular, reusable functions with clear inputs/outputs
  - Comprehensive logging at key pipeline stages
  - Explicit error handling and data quality checks
  - Unit tests for all transformation functions (`tests/unit/`)
  - Documentation of expected data formats and schemas (docstrings, README files)

- The plan MUST include specific test assertions for all critical data quality aspects:
  - Schema validation (column existence, data types)
  - Data completeness (null checks, row counts)
  - Data accuracy (value ranges, format validation)
  - Data consistency (cross-table validation, referential integrity)
  - Transformation correctness (business logic, calculations)
  - Performance benchmarks (execution time, resource usage)

### 15. Statistical Analysis & Model Development

This section MUST (when applicable for analytical/ML features):
- Specify statistical methods and techniques:
  - Descriptive statistics to be calculated
    - **Reference**: `.github/prompts/stages/exploratory_analysis.prompt.md` for analysis execution workflow including metric calculation and statistical testing procedures
  - Hypothesis tests to be performed (with significance levels, e.g., α = 0.05)
  - Time series analysis methods (if applicable)
  - Handling of small sample sizes, imbalanced data, or rare events
  - Multiple testing correction methods (Bonferroni, FDR) when applicable
- Define modeling approach (if ML/predictive models involved):
  - Problem type (regression, classification, clustering, forecasting)
  - Candidate algorithms with justification
  - Feature selection strategy
  - Train/validation/test split ratios
  - Cross-validation approach (k-fold, time series split)
  - Hyperparameter tuning strategy (grid search, random search, Bayesian optimization)
  - **Reference**: `.github/prompts/stages/model_training.prompt.md` for comprehensive model development workflow
- Establish model evaluation criteria:
  - Primary and secondary metrics (RMSE, MAE, R², AUC-ROC, precision/recall)
  - Baseline models for comparison (mean/median, simple heuristics)
  - Performance thresholds for production deployment (specific values required)
  - Business impact metrics (cost savings, improved outcomes)
- Document model interpretability requirements:
  - Feature importance analysis (permutation, SHAP values)
  - SHAP/LIME explanations (if required)
  - Model documentation for stakeholders (assumptions, limitations, appropriate use cases)

### 16. Model Operations & Governance (for ML/predictive features)

This section MUST (when applicable for machine learning models):
- Define model versioning strategy:
  - Use MLflow, Weights & Biases, or similar model registry
  - Version naming convention (semantic versioning recommended)
  - Model metadata to track (hyperparameters, training data version, performance metrics)
- Specify experiment tracking requirements:
  - Log all hyperparameters, metrics, and key artifacts
  - Track data lineage (training data provenance)
  - Document failed experiments and learnings
- Define model packaging approach:
  - Serialization format (pickle, joblib, ONNX, SavedModel)
  - Include preprocessing pipeline with model
  - Document model input/output schemas
- Establish deployment strategy:
  - Batch scoring vs real-time inference requirements
  - API endpoint specifications (if applicable)
  - Rollback procedures to revert to previous model version
- Define production monitoring requirements:
  - Model performance monitoring (accuracy degradation over time)
  - Data drift detection (input distribution changes)
  - Concept drift detection (relationship changes)
  - Alerting thresholds and escalation procedures
- Specify retraining triggers and schedule:
  - Periodic retraining schedule (monthly, quarterly)
  - Performance-based triggers (accuracy drops below threshold)
  - Data-based triggers (significant new data available)

### 17. UI/Dashboard Visual Testing (for Dashboard/Visualization Features)

If the feature includes dashboards, reports, or UI components:
- The plan MUST include appropriate test specifications:
  - For Power BI: Manual testing checklist with specific validation points
  - For web-based dashboards: Automated testing approach (Playwright, Selenium, etc.)
  
- The plan MUST include a comprehensive Visual Testing strategy that specifies:
  - All visual aspects to be verified (exact colors, spacing, typography, chart types, etc.)
  - Standard viewport sizes to test (Mobile, Tablet, Desktop as applicable)
  - Expected data-driven behaviors (dynamic filtering, drill-through, tooltips)
  - Cross-browser/device compatibility requirements
  
- For Power BI dashboards, the plan MUST specify:
  - DAX measure validation approach
  - Visual configuration verification checklist
  - Filter and slicer interaction testing
  - Performance optimization checks (query reduction, aggregations)
  - Row-level security testing (if applicable)

### 18. Success Metrics & Monitoring

This section MUST:
- Define business success metrics:
  - KPIs to measure feature effectiveness
  - User adoption targets (dashboard views, API usage)
  - Decision impact metrics
- Specify technical monitoring:
  - Pipeline health metrics (success rate, latency)
  - Data quality metrics dashboard
  - Model performance monitoring (drift detection, accuracy over time)
  - Infrastructure metrics (CPU, memory, storage)
- Establish alerting thresholds and escalation:
  - Critical alerts (pipeline failures, data quality violations)
  - Warning thresholds (performance degradation)
  - Notification channels (email, Slack, PagerDuty)

### 19. References

If applicable, this section MUST:
- List each referenced file with a relative path and short description
- Ensure all referenced documents, APIs, or design files are linked

## Code Generation Readiness Checklist

**CRITICAL**: The implementation plan is ready for code generation ONLY if it includes:

- [ ] **🚨 CODE EXECUTION VALIDATION COMPLETED** - ALL code blocks have been tested for executability
- [ ] **Function signatures** with complete type hints for all major components
- [ ] **Data schemas** defined as Pydantic models or dataclasses
- [ ] **Specific library methods** (exact Polars operations, not generic "load data")
- [ ] **Configuration file structure** with example YAML content
- [ ] **Test assertions** with specific expected values
- [ ] **Import statements** for all dependencies (internal and external)
- [ ] **Error handling patterns** with specific exception types
- [ ] **Logging statements** at key pipeline steps with exact messages
- [ ] **Data validation rules** as executable code (column names, types, constraints)
- [ ] **Example input/output data** for each major transformation
- [ ] **Technical constraints** (memory limits, performance targets, optimization strategies)
- [ ] **Package management commands** using `uv` (not pip)
- [ ] **Code generation order** specifying which components to generate first
- [ ] **Test fixtures** with sample data for testing
- [ ] **Performance benchmarks** (expected execution times, memory usage)

**If any item is missing, the plan is NOT ready for code generation and must be enhanced.**

## Quality Criteria for Code Generation

The implementation plan MUST:

**Functional Requirements:**
- Be based on the existing data sources defined in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md) and conventions
- Prioritize pipeline and model reuse over creating new components
- Provide concrete file paths, pipeline names, and schema definitions
- Be clear and detailed enough for implementation without significant ambiguity
- Accurately reflect design specifications (for dashboard/UI features)
- Include proper Mermaid diagram formatting to ensure correct rendering
- Ensure data quality and governance considerations are addressed

**Code-Level Requirements:**
- **Be Executable**: ALL code blocks have been tested and run without errors
- **Be Validated**: Every code snippet has been syntax-checked and import-verified
- **Be Complete**: No stubs, placeholders, or TODO comments in production code
- **Be Type-Safe**: All functions have complete type hints (parameters and returns)
- **Be Testable**: Includes specific test cases with assertions and expected values
- **Be Standards-Compliant**: Follows project conventions (Polars over pandas, uv over pip, loguru over print, type hints mandatory)
- **Be Reproducible**: Includes configuration files, seed values, version pins
- **Be Maintainable**: Uses modular design with clear separation of concerns
- **Be Documented**: Includes NumPy-style docstrings for all public functions
- **Be Error-Resistant**: Specifies error handling and validation at each step
- **Be Performance-Conscious**: Specifies lazy evaluation, dtype optimization, memory management
- **Be Code-Ready**: Can be directly translated to Python without requiring design decisions

---

## Guidelines for Plan Creation

When generating the implementation plan:

**Strategic Guidelines:**
1. **Be Specific**: Use concrete file paths, library names, and configuration values
2. **Be Comprehensive**: Cover all aspects from data ingestion to monitoring
3. **Be Realistic**: Base estimates on actual data volumes and system capabilities
4. **Be Adaptive**: Treat the plan as a living document that evolves based on actual code execution outputs and findings (see section 12: Adaptive Implementation Strategy)
5. **Be Modular**: Design components that can be developed and tested independently
6. **Reference Existing Assets**: Always check workspace for reusable components before proposing new ones
7. **Follow Project Standards**: Adhere to established naming conventions, folder structure, and coding patterns in the workspace
8. **Ensure Reproducibility**: Include clear steps for environment setup, dependency management, and seed setting

**Code Generation Guidelines:**
9. **Be Executable**: Provide function signatures with complete type hints, not just descriptions
10. **Be Library-Specific**: Use exact Polars methods (`pl.scan_csv()`, `.with_columns()`), not generic pseudo-code
11. **Be Test-Driven**: Include test assertions with specific expected values for validation
12. **Be Standards-Enforcing**: Mandate uv for packages, loguru for logging, Polars over pandas (with justification if pandas needed)
13. **Be Schema-Explicit**: Define all data schemas as Pydantic models or dataclasses
14. **Be Error-Aware**: Specify exception types, error messages, and recovery strategies
15. **Be Performance-Oriented**: Include memory budgets, execution time targets, optimization strategies
16. **Be Dependency-Clear**: List all imports (internal modules and external packages) for each file
17. **Be Configuration-Driven**: Specify YAML structure, parameter names, and default values
18. **Be Order-Conscious**: Follow the code generation order (section 13) to ensure dependencies exist before use


## Example Section Format

Implementation Steps section example:
```markdown
**Implementation Checklist:**

**Phase 1: Data Extraction**

**1. Environment Setup:**
- [ ] Create Python virtual environment: `python -m venv venv` or configure conda environment
- [ ] Install required dependencies from `requirements.txt` with pinned versions
- [ ] Verify Python version meets requirements (e.g., Python 3.9+)
- [ ] Set up configuration file: `config/analysis_config.yml`
- [ ] Configure logging: `src/utils/logger.py`
- [ ] Create `.env` file with database credentials and API keys (do not commit)
- [ ] Test database/API connectivity and log connection success
- [ ] Document environment setup in `README.md` or `SETUP.md`

**2. Data Extraction:**
- [ ] Create data extraction script: `scripts/extract_data.py`
- [ ] Follow extraction procedures from `.github/prompts/stages/data_extraction.prompt.md`:

**3. Initial Data Validation:**
- [ ] Write unit tests for extraction functions: `tests/unit/test_extraction.py`
- [ ] Validate extracted data schema matches expected structure
- [ ] Check for data completeness (expected row counts, date ranges)
- [ ] Log data quality metrics (missing values, duplicates)
- [ ] Document any data extraction issues in `data/1_raw/README.md`

**Phase 2: Data Cleaning**

**4. Data Quality Assessment:**
- [ ] Create initial data quality notebook: `notebooks/1_exploratory/01_data_quality_assessment.ipynb`
- [ ] Assess missing values by column and identify patterns
- [ ] Identify duplicate records and determine deduplication strategy
- [ ] Detect outliers using statistical methods (IQR, Z-score)
- [ ] Check data types and format consistency
- [ ] Identify data quality issues requiring business clarification
- [ ] Document findings and cleaning decisions

**5. Data Cleaning Implementation:**
- [ ] Create data cleaning module: `src/data_processing/cleaning.py`
- [ ] Follow comprehensive cleaning procedures from `.github/prompts/stages/data_cleaning.prompt.md`
  - [ ] **Detect and correct categorical inconsistencies**: Analyze all categorical columns for naming variations (abbreviations, typos, case differences) that refer to the same entity using intelligent pattern matching. Use conservative similarity thresholds (0.85+) to avoid incorrectly merging legitimate variations like "Disease A" vs "Disease B" or "Type 1" vs "Type 2". Generate and review categorical cleaning reports documenting all standardization mappings applied.
  - [ ] Create data validation functions: `src/data_processing/validators.py`
  - [ ] Save cleaned data to `data/3_interim/cleaned_data.parquet`

**6. Data Cleaning Validation:**
- [ ] Write unit tests for cleaning functions: `tests/unit/test_cleaning.py`
- [ ] Validate cleaning logic with edge cases (all nulls, extreme outliers)
- [ ] Compare before/after statistics to ensure cleaning effectiveness
- [ ] Document cleaning decisions and business rules applied
- [ ] Create data cleaning report summarizing changes made

**Phase 3: Exploratory Data Analysis**

**7. Univariate Analysis:**
- [ ] Create EDA notebook: `notebooks/1_exploratory/02_exploratory_data_analysis.ipynb`

**8. Bivariate & Multivariate Analysis:**
- [ ] Analyze relationships between variables (correlation matrix, scatter plots)
- [ ] Identify significant associations and potential predictors
- [ ] Perform subgroup analysis (stratification by demographics, facility type, etc.)
- [ ] Analyze temporal patterns and trends (time series plots, seasonality)
- [ ] Test statistical hypotheses (t-tests, chi-square, ANOVA as appropriate)
- [ ] Document key insights and relationships discovered

**9. Business Insights Documentation:**
- [ ] Summarize key findings from EDA
- [ ] Identify data-driven answers to business questions
- [ ] Create visualizations for stakeholder presentation
- [ ] Document assumptions and limitations of the analysis
- [ ] Export key figures to `reports/figures/`

**Phase 4: Feature Engineering**

**10. Domain Knowledge Review & Feature Planning:**
- [ ] Review all domain knowledge documents in `docs/domain_knowledge/`
- [ ] Create domain knowledge inventory: document title, key concepts, applicable metrics/formulas
- [ ] Identify domain-specific features to engineer (e.g., epidemiological metrics, workforce ratios, burden indices)
- [ ] Map each proposed feature to domain knowledge source and calculation method
- [ ] Document domain terminology to use for feature naming and definitions
- [ ] Identify domain-specific validation criteria and benchmarks
- [ ] Create feature engineering specification document referencing domain sources

**11. Feature engineering:**
- [ ] Create feature engineering notebook: `notebooks/3_feature_engineering/01_feature_engineering.ipynb`
- [ ] Implement domain-specific features identified from domain knowledge review
- [ ] Create temporal features (day of week, month, season, holidays, epi-week aggregations)
- [ ] Create aggregated features (rolling averages, lag features, cumulative sums)
- [ ] Create derived features (ratios, differences, interactions)
- [ ] Apply domain-specific calculations (e.g., attack rates, burden metrics, workforce ratios per domain knowledge)
- [ ] Create categorical encodings (one-hot, label encoding, target encoding)
- [ ] Implement feature engineering module: `src/features/engineering.py`
- [ ] Document feature definitions, calculation logic, domain sources, and data source mappings
- [ ] Validate features against domain benchmarks and expected ranges (from domain knowledge)

**12. Feature Selection & Validation:**
- [ ] Perform feature importance analysis (correlation with target, mutual information)
- [ ] Remove highly correlated redundant features (VIF, correlation threshold)
- [ ] Implement feature selection methods (recursive elimination, L1 regularization)
- [ ] Create feature selection module: `src/features/selection.py`
- [ ] Save engineered features to `data/4_processed/features.parquet`
- [ ] Write unit tests for feature engineering: `tests/unit/test_features.py`

**Phase 5: Modeling/Analysis**

**13. Statistical Analysis (if analytical focus):**
- [ ] Create statistical analysis notebook: `notebooks/2_analysis/01_statistical_analysis.ipynb`
- [ ] Apply domain-specific analytical methods identified from domain knowledge review
- [ ] Perform descriptive statistics and summarize key metrics
- [ ] Conduct hypothesis tests to answer research questions
- [ ] Perform time series analysis (trend, seasonality decomposition) if applicable
- [ ] Apply domain-specific validation criteria and compare against domain benchmarks
- [ ] Create statistical visualizations (confidence intervals, effect sizes)
- [ ] Document statistical findings with interpretation and limitations
- [ ] Interpret results using domain terminology and context from domain knowledge
- [ ] Save analysis results to `results/tables/statistical_summary.csv`

**14. Model Development (if predictive focus):**
- [ ] Create modeling notebook: `notebooks/2_analysis/02_model_development.ipynb`
- [ ] Refer to model training procedures from `.github/prompts/stages/model_training.prompt.md`

**15. Model Evaluation:**
- [ ] Evaluate models on validation set using appropriate metrics (RMSE, MAE, R², AUC, F1)
- [ ] Perform cross-validation to assess model stability
- [ ] Analyze residuals and prediction errors
- [ ] Assess model assumptions (normality, homoscedasticity for linear models)
- [ ] Compare model performance against baseline, business requirements, and domain benchmarks
- [ ] Select final model based on evaluation criteria
- [ ] Implement model evaluation module: `src/models/evaluation.py`

**16. Model Interpretability:**
- [ ] Calculate feature importance scores (permutation importance, SHAP values)
- [ ] Create partial dependence plots for key features
- [ ] Generate SHAP summary plots and force plots (if applicable)
- [ ] Analyze prediction examples (best/worst predictions)
- [ ] Document model interpretation for stakeholders
- [ ] Save model artifacts to `models/trained_models/`

**17. Model Testing:**
- [ ] Evaluate final model on held-out test set
- [ ] Calculate final performance metrics
- [ ] Perform sensitivity analysis (robustness to input changes)
- [ ] Write unit tests for model functions: `tests/unit/test_models.py`
- [ ] Create integration test for end-to-end prediction pipeline: `tests/integration/test_pipeline.py`
- [ ] Document test results and model limitations

**Phase 6: Results & Visualization**

**18. Results Compilation:**
- [ ] Create results summary notebook: `notebooks/2_analysis/03_results_summary.ipynb`
- [ ] Compile key findings, metrics, and insights
- [ ] Create executive summary with business recommendations
- [ ] Generate final visualizations for presentation
- [ ] Save results tables to `results/tables/`
- [ ] Save results metrics to `results/metrics/model_performance.json`

**19. Dashboard Development (if applicable):**
- [ ] Refer to visualization procedures from `.github/prompts/stages/visualization.prompt.md`

**20. Documentation:**
- [ ] Update data dictionary: `docs/data_dictionary/features.md`
- [ ] Document all domain knowledge sources referenced and how they informed analysis
- [ ] Create methodology document: `docs/methodology/analysis_approach.md`
- [ ] Write user guide for dashboard/tool: `docs/user_guide.md`
- [ ] Document all assumptions, limitations, and caveats
- [ ] Add Python docstrings to all functions (NumPy style)
- [ ] Create README for notebook usage: `notebooks/README.md`
- [ ] Update project status: `PROJECT_STATUS.md`

```