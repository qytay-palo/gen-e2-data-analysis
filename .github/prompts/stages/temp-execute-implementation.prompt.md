---
description: Prompt for Execution of the Implementation Plan
stage: Development
---
# AI Agent Prompt: Execute Implementation Plan

## Role

Execute a detailed implementation plan accurately and verify its completion according to specifications for a end-to-end data analysis project.

## Input Requirements

The input will consist of:
- A detailed implementation plan (typically in Markdown format)
- User story and acceptance criteria
- Design specifications and requirements

## Output Requirements

The output MUST include:
- Implementation of all required files and changes
- Implementation code should be placed in:
   `src/problem-statement-{num}-{name}/`
- Verification that specifications have been met
- Completed Design Implementation Verification Checklist

## Prerequisites: Validation Checkpoint

**🛑 MANDATORY PRE-EXECUTION VALIDATION**

Before executing ANY implementation plan, verify it has successfully passed the validation stage (Prompt #4: Implementation Plan Reflection & Validation):

### Required Validation Stamp

The implementation plan MUST contain a validation stamp similar to:

```markdown
✅ **CODE VALIDATION COMPLETED**: All code blocks tested and verified executable on [DATE]
- Tested with Python [version]
- All imports verified
- All file paths validated
- Zero syntax/runtime errors
- Data quality issues analyzed and handling code added
- All adaptive steps tested and validated
- Expected outputs confirmed
```

### Validation Verification Checklist

- [ ] ✅ Validation stamp present in implementation plan
- [ ] ✅ All code blocks tested and verified executable
- [ ] ✅ Data quality handling strategies validated
- [ ] ✅ Security/privacy measures reviewed
- [ ] ✅ No fundamental feasibility blockers flagged
- [ ] ✅ All imports and dependencies verified available
- [ ] ✅ File paths validated against actual project structure

### If Validation is Missing or Incomplete

**🚫 HALT EXECUTION IMMEDIATELY:**

1. **Do NOT proceed** with implementation
2. **Return implementation plan** to validation stage (Prompt #4)
3. **Document reason** for halting:
   ```markdown
   ❌ EXECUTION BLOCKED: Implementation plan lacks validation stamp
   - Required: Code execution validation from Prompt #4
   - Status: Implementation plan must be validated before execution
   - Action: Return to validation stage
   ```
4. **Wait for validated plan** before resuming

**Rationale**: Non-validated plans contain untested code with syntax errors, missing imports, or logic bugs that will cause execution failures and waste resources.

---

## Review Requirements

After confirming validation stamp is present, review the implementation plan for:
- Clarity and completeness of all steps
- Availability of all necessary information
- Alignment with project guidelines and technical stack
- Data sources and analysis requirements

If any part of the plan is unclear or missing information, clarification MUST be requested before proceeding.

## Implementation Requirements

The implementation MUST:
- Follow the staged implementation approach outlined below
- Adhere to file paths, code structures, and configurations specified in the plan
- Follow project coding standards and best practices
- Create exact visual implementations matching design specifications
- For any service or API integration step, you MUST implement the actual data fetching, error handling, and retries as described in the plan. Stubs or placeholders are NOT considered complete. If a function is only a stub, the implementation is NOT complete.
- **Leverage MCP (Model Context Protocol) tools for all file and data operations as specified below**
- **Implement ALL code blocks provided in the implementation plan verbatim (see Code Implementation Fidelity below)**

### Code Implementation Fidelity

**CRITICAL**: When an implementation plan includes code blocks with complete function implementations, these MUST be used exactly as specified:

✅ **REQUIRED - Implement Verbatim:**
- ALL code blocks provided in the implementation plan
- All type hints, docstrings, and parameter definitions
- All error handling, retry logic, and validation checks
- All logging statements and audit trail tracking
- All unit tests specified with full test coverage
- All helper functions, utility modules, and configuration files
- All security best practices (credential handling, input validation)

❌ **FORBIDDEN - Do NOT:**
- Simplify or omit "helper" functions or "boilerplate" code
- Skip validation, error handling, or logging statements
- Reduce comprehensive error handling to basic try/except blocks
- Replace detailed implementations with stubs or placeholders
- Assume "obvious" code can be skipped or simplified
- Modify function signatures, parameters, or return types without justification
- Create partial implementations with TODO comments

**Rationale**: Implementation plan code blocks are:
- Production-ready and tested against edge cases
- Include proper error handling for real-world scenarios
- Follow security best practices
- Implement comprehensive logging for debugging and audit trails
- Support reproducibility and long-term maintainability

**Verification After Implementation**:
1. Every function specified in the plan exists and is fully implemented
2. All type hints and docstrings match the specification exactly
3. All unit tests run successfully with expected coverage
4. No functions are stubs (contain only `pass` or `NotImplementedError`)
5. All error handling, retry logic, and validation checks are present
6. All logging and metadata tracking code is functional

## MCP Tools Integration

This implementation MUST leverage available MCP (Model Context Protocol) tools for efficient execution:

### Available MCP Servers

#### 1. Filesystem Server (REQUIRED for all implementations)
Use for all file operations throughout the project structure:

**Data Operations**:
- Reading source data from `data/1_raw/`, `data/2_external/`
- Writing processed data to `data/3_interim/`, `data/4_processed/`
- Managing schemas in `data/schemas/`

**Code & Notebooks**:
- Creating/editing notebooks in `notebooks/1_exploratory/`, `notebooks/2_analysis/`, `notebooks/3_feature_engineering/`
- Managing source code in `src/` subdirectories

**Outputs & Results**:
- Creating result directories in `results/tables/`, `results/metrics/`, `results/exports/`
- Saving reports to `reports/figures/`, `reports/dashboards/`, `reports/presentations/`
- Storing models in `models/`

**Logs & Documentation**:
- Writing logs to `logs/etl/`, `logs/errors/`, `logs/audit/`
- Creating/updating documentation in `docs/`

**MCP Commands Examples**:
```
"Use filesystem tools to read data/1_raw/hospital_visits.csv"
"Use filesystem tools to create directory results/epic-001/wave-1/"
"Use filesystem tools to write the processed data to data/4_processed/clean_visits.csv"
"Use filesystem tools to list all files in notebooks/1_exploratory/"
```

#### 2. SQLite Server (when applicable)
Use for database operations:
- Querying existing databases in `data/` directory
- Creating summary tables and views
- Data validation and quality checks via SQL
- Aggregating data for analysis

**MCP Commands Examples**:
```
"Query the patient_records database using SQLite tools to get admission trends"
"Use SQLite tools to create a summary table of visits by department"
"Execute data quality checks using SQLite tools on the staging database"
```

#### 3. GitHub Server (optional, when enabled)
Use for version control and collaboration:
- Searching codebase for existing implementations
- Creating issues for tracking
- Managing pull requests

### MCP Tool Usage Requirements

When implementing any feature or analysis:

1. **File Reading**: MUST use filesystem MCP tools instead of manual file operations
   - ✅ Correct: "Use filesystem tools to read data/1_raw/input.csv"
   - ❌ Incorrect: Asking user to paste file contents

2. **Directory Management**: MUST use filesystem MCP tools for organization
   - ✅ Correct: "Use filesystem tools to create directory structure for Epic 001"
   - ❌ Incorrect: Manual directory creation commands

3. **Data Writing**: MUST use filesystem MCP tools for all outputs
   - ✅ Correct: "Use filesystem tools to save analysis results to results/tables/"
   - ❌ Incorrect: Generating code without actually saving files

4. **Database Queries**: MUST use SQLite MCP tools when databases are involved
   - ✅ Correct: "Query using SQLite tools and save results with filesystem tools"
   - ❌ Incorrect: Writing SQL without executing it

5. **Verification**: MUST use MCP tools to verify implementation
   - ✅ Correct: "Use filesystem tools to list and verify all created files"
   - ❌ Incorrect: Assuming files were created without verification

### MCP-Enhanced Implementation Workflow

For each implementation stage, follow this MCP-integrated approach:

#### Pre-Implementation
1. Use **filesystem tools** to list and read existing relevant files
2. Use **filesystem tools** to verify project structure
3. Use **SQLite tools** to check existing data (if applicable)

#### During Implementation
1. Use **filesystem tools** to create necessary directories
2. Use **filesystem tools** to read input data/configurations
3. Process data (analysis, transformation, modeling)
4. Use **filesystem tools** to write outputs to appropriate locations
5. Use **filesystem tools** to write logs for audit trail

#### Post-Implementation Verification
1. Use **filesystem tools** to list all created files and verify existence
2. Use **filesystem tools** to read outputs and validate content
3. Use **SQLite tools** to verify database changes (if applicable)
4. Document which MCP tools were used in the verification checklist

### MCP Integration in Acceptance Criteria Verification

When verifying acceptance criteria, explicitly state MCP tool usage:

```
Acceptance Criterion 1: Data extracted and saved to data/1_raw/
✅ Verified using filesystem tools: 
   - Listed directory contents: data/1_raw/hospital_visits.csv exists
   - File size: 2.5 MB (verified non-empty)
   - Read first 5 rows to confirm data structure

Acceptance Criterion 2: Quality report generated
✅ Verified using filesystem tools:
   - Report exists at: reports/quality_report_2026-02-06.md
   - Report contains required sections (checked via file read)
```

### Implementation Stages

The implementation MUST proceed through stages aligned with the data analysis lifecycle. **Adapt these stages according to the specific implementation plan provided:**

- **If the plan specifies different stages**: Follow the plan's structure exactly
- **If the plan is task-oriented**: Map tasks to appropriate lifecycle stages below
- **If the plan omits stages**: Skip irrelevant stages (e.g., modeling for descriptive analysis)
- **If the plan combines stages**: Execute combined activities as specified
- **Always prioritize**: The implementation plan's instructions over these generic stages

The following stages represent a complete data analysis lifecycle and should be selectively applied based on the implementation plan:

#### Stage 0: Environment Setup & Dependencies

**Setup Actions:**
- Configure Python environment (virtual environment, conda, etc.)
- Use **configure_python_environment** tool to set up the workspace environment
- Install all required Python packages and libraries from `requirements.txt`
- Use **install_python_packages** tool for package installation in **kernel and environment**
- Verify Python version compatibility with project requirements
- Install additional system dependencies if needed
- Document environment specifications (Python version, package versions)
- Use **get_python_environment_details** to verify installation success
- Set up any required API keys or environment variables
- Configure database connections if applicable
- Verify MCP tools availability (filesystem, SQLite, GitHub)

**🚪 VALIDATION GATE - MUST PASS BEFORE PROCEEDING:**

```python
# Environment Validation Checklist
import sys
import subprocess

print("=== Environment Validation ===")

# 1. Python version check
print(f"Python version: {sys.version}")
assert sys.version_info >= (3, 9), "❌ Python 3.9+ required"
print("✅ Python version OK")

# 2. Critical imports test
try:
    import polars as pl
    import numpy as np
    import matplotlib.pyplot as plt
    print("✅ Critical imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    raise

# 3. Verify package installations
result = subprocess.run(
    ['pip', 'list', '--format=json'],
    capture_output=True, text=True
)
if result.returncode == 0:
    print("✅ Package list accessible")
else:
    print("❌ Cannot access package list")

# 4. Test MCP filesystem tools
try:
    import os
    assert os.path.exists('data/'), "❌ Project structure not found"
    print("✅ Project structure verified")
except AssertionError as e:
    print(e)
    raise

print("\n🎉 All validation checks passed - Ready to proceed to Stage 1")
```

**Checkpoint After Stage 0:**
```python
import json
from datetime import datetime

checkpoint = {
    'stage': 0,
    'stage_name': 'Environment Setup',
    'status': 'COMPLETED',
    'timestamp': datetime.now().isoformat(),
    'python_version': sys.version,
    'packages_installed': True,
    'next_stage': 1
}

with open('logs/audit/execution_checkpoint.json', 'w') as f:
    json.dump(checkpoint, f, indent=2)
    
print("✅ Stage 0 checkpoint saved")
```

**🛑 DO NOT PROCEED** to Stage 1 if any validation checks fail. Fix environment issues first.

#### Stage 1: Problem Understanding & Setup
- Review user story and acceptance criteria thoroughly
- Understand business context and analytical objectives
- Set up project structure (directories, notebooks, configurations)
- Verify data sources and access requirements
- Document assumptions and constraints
- Use **filesystem tools** to create necessary directory structure

#### Stage 2: Data Collection & Extraction
- Extract data from source systems using appropriate methods
- Use **filesystem tools** to read data from `data/1_raw/` or `data/2_external/`
- Use **SQLite tools** for database extractions (if applicable)
- Implement data fetching logic with proper error handling and retries
- Save raw data with appropriate metadata and timestamps
- Document data lineage and extraction parameters
- Verify data completeness and successful extraction

#### Stage 3: Data Profiling & Quality Assessment

**Primary Actions:**

1. **Profile dataset using Python code**
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   import polars as pl
   from pathlib import Path
   
   # Load data
   df = pl.read_csv('data/1_raw/hospital_visits.csv')
   
   print("="*60)
   print("DATA PROFILING REPORT")
   print("="*60)
   
   # Basic info
   print(f"\n📊 DATASET OVERVIEW")
   print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
   print(f"   Size: {df.estimated_size() / 1024:.2f} KB")
   
   # Column info
   print(f"\n📋 COLUMNS:")
   for col in df.columns:
       print(f"   - {col}: {df[col].dtype}")
   
   # Missing values
   print(f"\n❓ MISSING VALUES:")
   null_counts = df.select(pl.all().is_null().sum())
   for col in df.columns:
       null_count = null_counts[col][0]
       if null_count > 0:
           pct = (null_count / len(df)) * 100
           print(f"   {col}: {null_count} ({pct:.1f}%)")
   
   # Numeric summary
   print(f"\n📈 NUMERIC SUMMARY:")
   numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Int64, pl.Float64]]
   for col in numeric_cols:
       print(f"\n   {col}:")
       print(f"      Mean: {df[col].mean():.2f}")
       print(f"      Median: {df[col].median():.2f}")
       print(f"      Min: {df[col].min()}, Max: {df[col].max()}")
   
   # Categorical distributions
   print(f"\n🏷️  CATEGORICAL DISTRIBUTIONS:")
   cat_cols = [col for col in df.columns if df[col].dtype in [pl.Utf8, pl.Categorical]]
   for col in cat_cols:
       print(f"\n   {col}: {df[col].n_unique()} unique values")
       print(df[col].value_counts().head(5))
   ```

2. **Generate comprehensive data quality reports**
   - Analyze data distributions and patterns from profiling output
   - Identify data types, formats, and schema inconsistencies
   - Document data quality issues and anomalies
   - Save findings to inform cleaning strategy

3. **Create data profiling notebooks** in `notebooks/1_exploratory/`
   - Implement profiling logic based on initial analysis
   - Generate statistical summaries
   - Create distribution visualizations using matplotlib

4. **Validate data quality thresholds**
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   # Check data quality against thresholds
   quality_issues = []
   
   # Check missing value threshold (< 5%)
   for col in df.columns:
       null_pct = (df[col].is_null().sum() / len(df)) * 100
       if null_pct > 5:
           quality_issues.append(f"{col}: {null_pct:.1f}% missing (threshold: 5%)")
   
   # Check for duplicates
   dup_count = df.shape[0] - df.unique().shape[0]
   if dup_count > 0:
       quality_issues.append(f"Duplicates: {dup_count} rows")
   
   # Report findings
   if quality_issues:
       print("⚠️  Quality issues requiring handling:")
       for issue in quality_issues:
           print(f"  - {issue}")
   else:
       print("✅ All quality checks passed")
   ```

5. **Save profiling results** using **filesystem tools** to `results/tables/`
   - Data quality summary tables
   - Missing value reports
   - Outlier detection results

6. **Establish data quality metrics and thresholds**
   - Define acceptable ranges for key variables
   - Set thresholds for missing data (e.g., <5% acceptable)
   - Document quality criteria for downstream stages

**Checkpoint After Stage 3:**
```python
from datetime import datetime
import json

checkpoint = {
    'stage': 3,
    'stage_name': 'Data Profiling',
    'status': 'COMPLETED',
    'timestamp': datetime.now().isoformat(),
    'outputs': [
        'notebooks/1_exploratory/01_data_profiling.ipynb',
        'results/tables/data_quality_report.csv',
        'results/tables/missing_value_summary.csv'
    ],
    'quality_issues_identified': ['15% missing in age', 'outliers in case_count'],
    'next_stage': 4
}

with open('logs/audit/execution_checkpoint.json', 'w') as f:
    json.dump(checkpoint, f, indent=2)
```

#### Stage 4: Data Cleaning & Preprocessing
- Implement data cleaning logic based on profiling findings
- Handle missing values using appropriate strategies
- Correct data types and format inconsistencies
- Remove or flag outliers based on business rules
- Standardize and normalize data as needed
- Use **filesystem tools** to write cleaned data to `data/3_interim/`
- Document all transformations and cleaning decisions
- Log data cleaning operations to `logs/etl/`

#### Stage 5: Exploratory Data Analysis (EDA)

**Primary Actions:**

1. **Perform statistical exploration using Python**
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   from scipy import stats
   import numpy as np
   
   print("📊 STATISTICAL ANALYSIS")
   print("="*60)
   
   # Correlation analysis
   correlation = stats.pearsonr(
       df['case_count'].to_numpy(),
       df['temperature'].to_numpy()
   )
   
   print(f"\n1️⃣  Correlation: Cases vs Temperature")
   print(f"   Pearson r: {correlation.statistic:.4f}")
   print(f"   P-value: {correlation.pvalue:.4f}")
   print(f"   Result: {'Significant' if correlation.pvalue < 0.05 else 'Not significant'}")
   
   # Group comparison
   region1 = df.filter(pl.col('region') == 'Central')['case_count'].to_numpy()
   region2 = df.filter(pl.col('region') == 'North')['case_count'].to_numpy()
   
   stat, p_val = stats.mannwhitneyu(region1, region2)
   print(f"\n2️⃣  Mann-Whitney U Test: Regional Comparison")
   print(f"   U-statistic: {stat:.2f}")
   print(f"   P-value: {p_val:.4f}")
   ```

2. **Conduct comprehensive statistical analysis**
   - Hypothesis testing based on research questions
   - Correlation and relationship analysis
   - Temporal pattern identification

3. **Create visualizations using Python**
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   import matplotlib.pyplot as plt
   from pathlib import Path
   
   print("🎨 CREATING VISUALIZATIONS")
   
   # Time series plot
   fig, ax = plt.subplots(figsize=(12, 6))
   
   monthly = df.group_by('month').agg(pl.sum('case_count'))
   ax.plot(monthly['month'], monthly['case_count'], 
           marker='o', linewidth=2)
   
   ax.set_xlabel('Month', fontsize=12)
   ax.set_ylabel('Total Cases', fontsize=12)
   ax.set_title('Monthly Disease Case Trends', fontsize=14, fontweight='bold')
   ax.grid(True, alpha=0.3)
   
   Path('reports/figures').mkdir(parents=True, exist_ok=True)
   plt.savefig('reports/figures/monthly_trends.png', dpi=300, bbox_inches='tight')
   print("✅ Saved: reports/figures/monthly_trends.png")
   plt.close()
   ```

4. **Create detailed analysis notebooks** in `notebooks/2_analysis/`
   - Implement analysis code with proper documentation
   - Add domain context and interpretation
   - Document analytical decisions and assumptions

5. **Identify key insights and anomalies**
   - Explore temporal trends, seasonality, cycles
   - Analyze correlations and relationships
   - Flag unexpected patterns for investigation

6. **Validate statistical assumptions**
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   # Check normality assumption
   stat, p_val = stats.shapiro(df['case_count'].to_numpy())
   print(f"\n📋 Assumption Checks")
   print(f"   Shapiro-Wilk test for normality:")
   print(f"   Statistic: {stat:.4f}, P-value: {p_val:.4f}")
   
   if p_val < 0.05:
       print("   ⚠️  Data is NOT normally distributed")
       print("   → Use non-parametric tests (Mann-Whitney, Kruskal-Wallis)")
   else:
       print("   ✅ Data is normally distributed")
       print("   → Parametric tests (t-test, ANOVA) appropriate")
   ```

7. **Save outputs** using **filesystem tools**:
   - Figures to `reports/figures/`
   - Analysis results to `results/tables/`
   - Summary metrics to `results/metrics/`

8. **Document findings and preliminary insights**
   - Key patterns discovered
   - Statistical significance of findings
   - Limitations and caveats

**Checkpoint After Stage 5:**
```python
from datetime import datetime
import json

checkpoint = {
    'stage': 5,
    'stage_name': 'Exploratory Data Analysis',
    'status': 'COMPLETED',
    'timestamp': datetime.now().isoformat(),
    'outputs': [
        'notebooks/2_analysis/02_eda_temporal_patterns.ipynb',
        'reports/figures/dengue_trend_2020_2025.png',
        'results/metrics/correlation_analysis.json'
    ],
    'key_findings': [
        'Strong seasonal pattern in dengue cases (peak June-August)',
        'Significant correlation between rainfall and incidence (r=0.67)'
    ],
    'next_stage': 6
}

with open('logs/audit/execution_checkpoint.json', 'w') as f:
    json.dump(checkpoint, f, indent=2)
```

#### Stage 6: Feature Engineering & Transformation
- Design and create relevant features based on domain knowledge
- Apply transformations (aggregations, encodings, scaling)
- Create derived metrics and calculated fields
- Validate feature quality and relevance
- Create feature engineering notebooks in `notebooks/3_feature_engineering/`
- Use **filesystem tools** to save processed data to `data/4_processed/`
- Document feature definitions and calculation logic

#### Stage 7: Analysis Implementation & Modeling
- Implement analytical methods or statistical models
- Perform calculations, aggregations, or predictive modeling
- Apply domain-specific analytical frameworks
- Validate analytical outputs against business logic
- Use **filesystem tools** to save model artifacts to `models/`
- Use **filesystem tools** to save analysis results to `results/`
- Document methodology and analytical approach

#### Stage 8: Results Validation & Quality Assurance
- Verify outputs meet acceptance criteria
- Validate analytical results against known benchmarks
- Perform sensitivity analysis and robustness checks
- Review results with domain experts (if applicable)
- Document validation procedures and outcomes
- Use **filesystem tools** to save validation results to `results/metrics/`
- Log validation checks to `logs/audit/`

#### Stage 9: Documentation & Reporting
- Create comprehensive analysis documentation
- Generate reports with findings, insights, and recommendations
- Create executive summaries and technical documentation
- Build interactive dashboards or visualizations (if required)
- Use **filesystem tools** to save reports to `reports/`
- **Update README.md** (if not already updated) with:
  - Project overview and objectives
  - Setup instructions (environment setup, dependency installation)
  - Notebook execution sequence and purpose (e.g., "Run notebooks in order: 01 → 02 → 03")
  - Data source descriptions and locations
  - Key findings and outputs summary
  - Usage instructions for scripts, dashboards, or models
  - Troubleshooting tips and common issues
- Ensure all code is well-commented and reproducible
- Document limitations and future improvement opportunities

#### Stage 10: Delivery & Handoff
- Package final deliverables (data, code, reports, dashboards)
- Verify all acceptance criteria are met
- Complete verification checklists
- Prepare handoff documentation
- Use **filesystem tools** to organize final outputs
- Archive logs and intermediate outputs appropriately
- Provide recommendations for next steps or iterations

## Python-Based Data Analysis During Implementation

**IMPORTANT**: The implementation plan may reference conceptual "data plugin commands" like `/explore-data`, `/create-viz`, `/analyze`. These are NOT shell commands but represent analysis capabilities that MUST be implemented using Python code via the `mcp_pylance_mcp_s_pylanceRunCodeSnippet` tool.

### Implementation Approach

Before and during implementation, use Python code to perform data analysis and validation:

### Pre-Implementation Analysis

Use Python code to gather context and validate approach:

1. **Explore Existing Data**
   - Profile datasets before writing transformation logic
   - Identify data quality issues that affect implementation approach
   - Discover actual data distributions to inform validation thresholds
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   import polars as pl
   
   # Load and profile data
   df = pl.read_csv('data/1_raw/patient_visits.csv')
   
   print(f"Shape: {df.shape}")
   print(f"Columns: {df.columns}")
   print(f"Dtypes:\n{df.dtypes}")
   
   # Check missing values
   print(f"\nNull counts:\n{df.select(pl.all().is_null().sum())}")
   
   # Summary statistics
   print(f"\nSummary:\n{df.describe()}")
   
   # Categorical distributions
   for col in ['disease', 'region']:
       if col in df.columns:
           print(f"\n{col} distribution:\n{df[col].value_counts()}")
   ```

2. **Validate Data Extraction Logic**
   - Test query logic before embedding in pipeline code
   - Ensure data transformations work as expected
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   # Test aggregation logic
   monthly_summary = (
       df.group_by(['year', 'month', 'disease'])
       .agg(pl.sum('case_count').alias('total_cases'))
       .sort(['year', 'month'])
   )
   print(monthly_summary)
   ```

### During Implementation

Use Python code to accelerate implementation:

1. **Generate Visualizations**
   - Create publication-quality charts using matplotlib/seaborn
   - Follow visualization best practices
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   import matplotlib.pyplot as plt
   from pathlib import Path
   
   # Create time series visualization
   fig, ax = plt.subplots(figsize=(12, 6))
   
   for disease in df['disease'].unique():
       disease_data = df.filter(pl.col('disease') == disease)
       ax.plot(disease_data['date'], disease_data['cases'], 
               marker='o', label=disease)
   
   ax.set_xlabel('Date')
   ax.set_ylabel('Cases')
   ax.set_title('Disease Trends Over Time')
   ax.legend()
   ax.grid(True, alpha=0.3)
   
   Path('reports/figures').mkdir(parents=True, exist_ok=True)
   plt.savefig('reports/figures/disease_trends.png', dpi=300, bbox_inches='tight')
   print("✅ Visualization saved to reports/figures/disease_trends.png")
   ```

2. **Statistical Analysis**
   - Perform statistical computations and exploratory analysis
   - Validate assumptions and test hypotheses
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   from scipy import stats
   import numpy as np
   
   # Compare two groups
   group1 = df.filter(pl.col('region') == 'Central')['case_count'].to_numpy()
   group2 = df.filter(pl.col('region') == 'North')['case_count'].to_numpy()
   
   statistic, p_value = stats.mannwhitneyu(group1, group2)
   
   print(f"Mann-Whitney U Test Results:")
   print(f"  U-statistic: {statistic:.2f}")
   print(f"  P-value: {p_value:.4f}")
   print(f"  Result: {'Significant' if p_value < 0.05 else 'Not significant'} (α=0.05)")
   ```

3. **Data Quality Validation**
   - Verify data quality and schema compliance
   - Check business rules and constraints
   
   **Execute via `mcp_pylance_mcp_s_pylanceRunCodeSnippet`:**
   ```python
   # Validate data quality
   issues = []
   
   # Check required columns
   required_cols = ['date', 'disease', 'case_count']
   missing_cols = [c for c in required_cols if c not in df.columns]
   if missing_cols:
       issues.append(f"Missing columns: {missing_cols}")
   
   # Check data types
   if df['case_count'].dtype not in [pl.Int32, pl.Int64]:
       issues.append(f"case_count has wrong type: {df['case_count'].dtype}")
   
   # Check value ranges
   if df['case_count'].min() < 0:
       issues.append("Negative case counts found")
   
   # Check null values
   null_counts = df.select(pl.all().is_null().sum())
   for col in df.columns:
       if null_counts[col][0] > 0:
           issues.append(f"{col}: {null_counts[col][0]} nulls")
   
   if issues:
       print("⚠️  Data quality issues found:")
       for issue in issues:
           print(f"  - {issue}")
   else:
       print("✅ All data quality checks passed")
   ```

### Adaptive Implementation Workflow

```
1. Review implementation plan stage
2. Identify knowledge gaps or uncertainties
3. Write Python code to gather context (using patterns above)
4. Execute code via mcp_pylance_mcp_s_pylanceRunCodeSnippet
5. Analyze results and outputs
6. Adjust implementation approach based on findings
7. Generate production code with informed decisions
8. Validate outputs using Python assertions
9. Proceed to next stage
```

This approach ensures that implementation is **data-driven and context-aware**, with all analysis capabilities implemented as executable Python code rather than conceptual commands.

## Verification Requirements

After implementation, the following verifications MUST be completed:

1. **Acceptance Criteria Verification**
   - Each acceptance criterion MUST be verified as met
   - Any discrepancies MUST be documented

2. **Design Implementation Verification**
   - Complete the Design Implementation Verification Checklist
   - The checklist MUST include the sections below

- Explicitly check that all service and API integration logic is implemented, not just stubbed.
- During verification, confirm that all functions required to fetch, process, and return data are fully implemented and tested.
- If any function is a stub or placeholder, the implementation is NOT complete. Document this as a failure and halt further verification until resolved.

### Data Quality Verification Table

The Data Quality Verification table MUST verify data processing correctness:

```
| Data Quality Check | Expected | Actual | Status |
|-------------------|----------|--------|--------|
| Input data loaded | 10,000 rows, 15 cols | 10,000 rows, 15 cols | ✅ Pass |
| Missing value % | < 5% per column | 3.2% average | ✅ Pass |
| Outlier handling | IQR method applied | Implemented, 127 outliers flagged | ✅ Pass |
| Data types | All columns correct types | 15/15 correct | ✅ Pass |
| Date range | 2020-01-01 to 2025-12-31 | Confirmed | ✅ Pass |
| Duplicates removed | 0 duplicates | 0 duplicates found | ✅ Pass |
```

### Analysis Correctness Verification Table

The Analysis Correctness Verification table MUST verify statistical/analytical outputs:

```
| Analysis Component | Specification | Implementation | Status |
|-------------------|---------------|----------------|--------|
| Aggregation method | Monthly sum by disease | `groupby(['month', 'disease']).sum()` | ✅ Match |
| Statistical test | Mann-Whitney U test (α=0.05) | `scipy.stats.mannwhitneyu()` used | ✅ Match |
| Trend detection | Linear regression | `sklearn.LinearRegression()` fitted | ✅ Match |
| Feature engineering | Rate per 100k population | `(cases/population)*100000` | ✅ Match |
| Filtering criteria | Year >= 2020, cases > 0 | Both filters applied | ✅ Match |
```

### Output Validation Table

The Output Validation table MUST verify all expected outputs were generated:

```
| Output File | Expected Location | Exists | Valid Content | Status |
|-------------|------------------|--------|---------------|--------|
| Cleaned data | data/4_processed/clean_disease_data.csv | ✅ | Schema matches, 9,873 rows | ✅ Pass |
| EDA notebook | notebooks/2_analysis/eda_trends.ipynb | ✅ | All cells executed | ✅ Pass |
| Trend figure | reports/figures/dengue_trend_2020_2025.png | ✅ | Image displays correctly | ✅ Pass |
| Summary metrics | results/metrics/summary_statistics.json | ✅ | Valid JSON, expected keys | ✅ Pass |
| Quality report | results/tables/data_quality_report.csv | ✅ | 15 rows (one per column) | ✅ Pass |
```

### Reproducibility Verification Checklist

The Reproducibility Verification checklist MUST confirm analysis can be reproduced:

```
- ✅ Random seeds set where applicable (numpy.random.seed(42), random.seed(42))
- ✅ Execution order documented (README.md lists notebook sequence)
- ✅ All dependencies logged with versions (requirements.txt with pinned versions)
- ✅ Data lineage documented (extraction timestamps, source URLs)
- ✅ Environment specifications saved (Python version, OS, package versions)
- ✅ Intermediate checkpoints saved (data/3_interim/ contains staged outputs)
- ✅ All code runs without errors from clean environment
- ✅ Results match expected outputs (within tolerance for stochastic processes)
```

### Code Quality Verification Checklist

The Code Quality Verification checklist MUST ensure production-ready code:

```
- ✅ All functions have docstrings (Google/NumPy style with examples)
- ✅ Type hints present for function parameters and returns
- ✅ No functions are stubs (all contain actual implementation, no `pass` or `NotImplementedError`)
- ✅ Error handling implemented (try-except with specific exceptions)
- ✅ Logging statements present (loguru or logging module used)
- ✅ Unit tests written for critical functions (in tests/unit/)
- ✅ All tests pass (pytest returns 0 failures)
- ✅ Code follows PEP 8 style guidelines (flake8/black formatting)
- ✅ No hardcoded credentials (environment variables or config files used)
- ✅ Input validation present (check data types, ranges, required fields)
```

## Execution Failure Recovery Protocol

### When Code Execution Fails During Implementation

**Step 1: Identify Failure Category**

#### Category A: Implementation Plan Issues (Plan Was Wrong)
**Symptoms:**
- Missing data files that implementation plan claims exist
- Incorrect column names or schema mismatches
- Wrong analysis method for available data
- Data granularity mismatch (plan expects daily, only monthly available)

**Action:**
```python
import json
from datetime import datetime

# Document the plan issue
failure_log = {
    'timestamp': datetime.now().isoformat(),
    'category': 'IMPLEMENTATION_PLAN_ISSUE',
    'stage': 'Current stage number and name',
    'issue': 'Specific description of what plan expected vs. reality',
    'expected': 'What implementation plan specified',
    'actual': 'What was actually found',
    'impact': 'Cannot proceed - fundamental assumption violated',
    'status': 'BLOCKED',
    'requires': 'Implementation plan revision'
}

with open('logs/errors/execution_failure.json', 'w') as f:
    json.dump(failure_log, f, indent=2)

print("❌ EXECUTION BLOCKED: Implementation plan issue detected")
print("📋 See logs/errors/execution_failure.json for details")
print("🔄 Action required: Return implementation plan for revision")
```
**🛑 HALT EXECUTION** - Do not proceed until plan is revised.

---

#### Category B: Environment Issues (Environment Not Ready)
**Symptoms:**
- Missing packages not listed in requirements.txt
- Python version incompatibility
- Insufficient file permissions
- API keys or credentials not set

**Action:**
```python
# Fix environment issue and document
try:
    # Example: Install missing package
    import subprocess
    subprocess.run(['pip', 'install', 'missing-package'], check=True)
    
    # Document the fix
    with open('logs/audit/environment_fixes.log', 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] Installed missing-package\n")
        f.write(f"Added to requirements.txt for future runs\n")
    
    # Update requirements.txt
    with open('requirements.txt', 'a') as f:
        f.write('missing-package==1.2.3\n')
    
    print("✅ Environment issue resolved - Continuing execution")
    
except Exception as e:
    print(f"❌ Could not resolve environment issue: {e}")
    # Document and halt if cannot fix
```
**✅ CONTINUE EXECUTION** after fix is applied and tested.

---

#### Category C: Data Quality Issues (Data Worse Than Expected)
**Symptoms:**
- Higher null rates than anticipated (plan assumed <5%, actual 20%)
- More outliers requiring handling
- Unexpected data distributions
- Data quality below acceptable thresholds

**Action:**
```python
# Apply adaptive data quality handling
import polars as pl

def handle_unexpected_nulls(df: pl.DataFrame, column: str, threshold: float = 0.3):
    """Handle unexpectedly high null rates with adaptive strategy."""
    null_rate = df[column].is_null().sum() / len(df)
    
    if null_rate > threshold:
        print(f"⚠️  High null rate in {column}: {null_rate:.1%}")
        print(f"Applying strategy: Drop column (>30% missing)")
        df = df.drop(column)
    else:
        print(f"Applying strategy: Impute with median")
        median_val = df[column].median()
        df = df.with_columns(pl.col(column).fill_null(median_val))
    
    # Log the decision
    with open('logs/audit/data_quality_adaptations.log', 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {column}: null_rate={null_rate:.1%}\n")
        f.write(f"Strategy applied: {'Drop' if null_rate > threshold else 'Impute'}\n")
    
    return df

# Apply and document
df_cleaned = handle_unexpected_nulls(df, 'problematic_column')
print("✅ Data quality issue handled - Continuing execution")
```
**✅ CONTINUE EXECUTION** with adaptive handling documented.

---

#### Category D: Logic Errors (Code Has Bugs)
**Symptoms:**
- Syntax errors in implementation plan code
- Runtime errors (TypeError, KeyError, ValueError)
- Incorrect calculations producing invalid results
- Function signature mismatches

**Action:**
```python
# Fix bug, test, document deviation
try:
    # Original (buggy) code from plan:
    # result = df['cases'] / df['population']  # KeyError if column missing
    
    # Fixed code with validation:
    if 'cases' not in df.columns or 'population' not in df.columns:
        raise ValueError("Required columns missing for rate calculation")
    
    result = (df['cases'] / df['population']) * 100000
    
    # Document the fix
    with open('logs/audit/code_fixes.log', 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] Fixed rate calculation\n")
        f.write(f"Issue: Missing column validation\n")
        f.write(f"Fix: Added validation before calculation\n")
        f.write(f"Test: Calculation verified with sample data\n")
    
    print("✅ Bug fixed and tested - Continuing execution")
    
except Exception as e:
    print(f"❌ Could not fix bug: {e}")
    print("🛑 Halting for manual review")
    raise
```
**✅ CONTINUE EXECUTION** after bug is fixed and tested.

---

### Step 2: Recovery Workflow

```python
def handle_execution_failure(stage: int, error: Exception, context: dict):
    """
    Centralized failure handling with categorization and recovery.
    
    Args:
        stage: Stage number where failure occurred
        error: The exception that was raised
        context: Additional context (stage name, action, data)
    """
    from datetime import datetime
    import json
    import traceback
    
    # Categorize the failure
    error_type = type(error).__name__
    
    if error_type in ['FileNotFoundError', 'KeyError'] and 'data' in str(error):
        category = 'IMPLEMENTATION_PLAN_ISSUE'
        recoverable = False
    elif error_type in ['ImportError', 'ModuleNotFoundError']:
        category = 'ENVIRONMENT_ISSUE'
        recoverable = True
    elif 'null' in str(error).lower() or 'missing' in str(error).lower():
        category = 'DATA_QUALITY_ISSUE'
        recoverable = True
    else:
        category = 'LOGIC_ERROR'
        recoverable = True
    
    # Log the failure
    failure_record = {
        'timestamp': datetime.now().isoformat(),
        'stage': stage,
        'stage_name': context.get('stage_name', 'Unknown'),
        'category': category,
        'error_type': error_type,
        'error_message': str(error),
        'traceback': traceback.format_exc(),
        'recoverable': recoverable,
        'context': context
    }
    
    log_path = 'logs/errors/execution_failure.json'
    with open(log_path, 'w') as f:
        json.dump(failure_record, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"❌ EXECUTION FAILURE IN STAGE {stage}")
    print(f"Category: {category}")
    print(f"Error: {error}")
    print(f"Recoverable: {'Yes' if recoverable else 'No'}")
    print(f"{'='*60}\n")
    
    if not recoverable:
        print("🛑 HALTING EXECUTION - Manual intervention required")
        print(f"📋 See {log_path} for full details")
        raise
    else:
        print("🔧 Attempting recovery...")
        return category

# Usage in implementation stages:
try:
    # Stage implementation code here
    pass
except Exception as e:
    category = handle_execution_failure(
        stage=3,
        error=e,
        context={
            'stage_name': 'Data Profiling',
            'action': 'Loading data',
            'file': 'data/1_raw/input.csv'
        }
    )
    # Apply category-specific recovery
```

---

### Step 3: Checkpointing and Restart

**After Each Successful Stage:**
```python
import json
from datetime import datetime

def save_checkpoint(stage: int, stage_name: str, outputs: list, metadata: dict = None):
    """Save execution checkpoint for recovery."""
    checkpoint = {
        'stage': stage,
        'stage_name': stage_name,
        'status': 'COMPLETED',
        'timestamp': datetime.now().isoformat(),
        'outputs': outputs,
        'metadata': metadata or {},
        'next_stage': stage + 1
    }
    
    # Save checkpoint
    with open('logs/audit/execution_checkpoint.json', 'w') as f:
        json.dump(checkpoint, f, indent=2)
    
    # Also append to history
    with open('logs/audit/checkpoint_history.jsonl', 'a') as f:
        f.write(json.dumps(checkpoint) + '\n')
    
    print(f"✅ Checkpoint saved: Stage {stage} - {stage_name}")

# Use after each stage:
save_checkpoint(
    stage=3,
    stage_name='Data Profiling',
    outputs=[
        'notebooks/1_exploratory/01_profiling.ipynb',
        'results/tables/quality_report.csv'
    ],
    metadata={'rows_processed': 10000, 'quality_score': 0.95}
)
```

**To Restart from Checkpoint:**
```python
def load_last_checkpoint():
    """Load last successful checkpoint to resume execution."""
    try:
        with open('logs/audit/execution_checkpoint.json', 'r') as f:
            checkpoint = json.load(f)
        
        print(f"📍 Last checkpoint: Stage {checkpoint['stage']} - {checkpoint['stage_name']}")
        print(f"   Completed: {checkpoint['timestamp']}")
        print(f"   Next stage: {checkpoint['next_stage']}")
        
        return checkpoint
    except FileNotFoundError:
        print("No checkpoint found - Starting from Stage 0")
        return None

# Resume from last successful point
checkpoint = load_last_checkpoint()
if checkpoint:
    start_stage = checkpoint['next_stage']
    print(f"🔄 Resuming execution from Stage {start_stage}")
else:
    start_stage = 0
    print("🆕 Starting fresh execution")
```

---

### Step 4: Final Failure Report

If execution fails and cannot be recovered, generate comprehensive failure report:

```python
def generate_failure_report(failure_stage: int, failures: list):
    """Generate comprehensive failure report for stakeholders."""
    report = f"""
# Execution Failure Report

**Date**: {datetime.now().isoformat()}
**Failed at Stage**: {failure_stage}
**Status**: INCOMPLETE

## Execution Summary

### Completed Stages:
{chr(10).join(f'- ✅ Stage {i}: {name}' for i, name in enumerate(completed_stages[:failure_stage]))}

### Failed Stage:
- ❌ Stage {failure_stage}: {failed_stage_name}

### Failure Details:

"""
    
    for failure in failures:
        report += f"""
**Error Type**: {failure['category']}
**Error Message**: {failure['error_message']}
**Recoverable**: {'Yes' if failure['recoverable'] else 'No'}
**Action Required**: {failure['action_required']}

"""
    
    report += """
## Next Steps

1. Review failure details above
2. Address root cause based on failure category
3. Resume execution from last checkpoint

## Artifacts Preserved

- Checkpoint file: `logs/audit/execution_checkpoint.json`
- Failure log: `logs/errors/execution_failure.json`
- Partial outputs: [List all outputs from completed stages]
"""
    
    with open('logs/errors/failure_report.md', 'w') as f:
        f.write(report)
    
    print("\n📄 Failure report generated: logs/errors/failure_report.md")
    return report
```

---

## Error Handling Requirements

If implementation or verification fails, the output MUST:
- Clearly identify which part of the plan failed (stage number and name)
- Categorize the failure (Plan Issue, Environment, Data Quality, Logic Error)
- Describe the specific issue encountered with full error details
- Explain how it deviates from the plan or acceptance criteria
- Document recovery actions taken (if any)
- Provide checkpoint information for restart
- Generate failure report if execution cannot continue
- Suggest possible solutions or next steps based on failure category

## Documentation Requirements

The final output MUST include:
- Confirmation of completion if successful
- Results of all verification steps
- Any command outputs or test results
- The completed Design Implementation Verification Checklist
- Any noted discrepancies or issues
