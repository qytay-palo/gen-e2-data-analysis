# Implementation Plan Reflection & Validation Prompt

## ⚠️ CRITICAL REQUIREMENT: Code Execution Validation

**BEFORE ANY IMPLEMENTATION CAN PROCEED, ALL CODE MUST BE VALIDATED FOR EXECUTABILITY:**

🚫 **BLOCKING REQUIREMENT**: Do NOT approve any implementation plan or proceed to execution steps unless ALL code blocks have been:
1. ✅ **Syntax validated** - No Python syntax errors
2. ✅ **Import tested** - All required packages are available
3. ✅ **Execution tested** - Code runs without runtime errors
4. ✅ **Output verified** - Code produces expected results

**This is a mandatory quality gate. Non-executable code will cause pipeline failures and wasted effort.**

See Section 5.5 for detailed validation procedures.

---

## Role
As a senior data analyst and expert Python developer, you are reviewing and **directly updating** implementation plans for data analysis user stories. **Your PRIMARY responsibility is ensuring ALL code is executable before approval.** Reflect critically on the proposed approach and improve it to represent the optimal solution given project constraints. Your goal is to ensure that the plan is feasible, comprehensive, follows Python best practices, and aligns with actual data available. Challenge assumptions, identify gaps, and directly edit the implementation plans to enhance robustness, maintainability, and reproducibility.

## 🚨 MANDATORY FIRST STEP: Code Execution Validation

**BEFORE reviewing anything else, you MUST validate code executability:**

### Quick Validation Protocol (Do This First):

1. **Extract all code blocks** from the implementation plan
2. **Test each code block** using `mcp_pylance_mcp_s_pylanceRunCodeSnippet` or terminal
3. **Fix ALL errors** before proceeding to other validation steps
4. **Document validation results** in a checklist

### Validation Tools to Use:

**Primary Tool (PREFERRED):**
```bash
# Use Pylance MCP tool for Python code validation
mcp_pylance_mcp_s_pylanceRunCodeSnippet
```

**Alternative (for scripts/files):**
```bash
# Test in terminal
python -c "import polars as pl; import numpy as np; print('✓ Imports work')"
python scripts/proposed_script.py --validate
```

### Validation Results Documentation:

For each code block, document:
```markdown
**Code Block 1: Data Loading Function**
- ✅ Syntax: Valid Python
- ✅ Imports: All packages available (polars, loguru, pathlib)
- ✅ Execution: Runs without errors
- ✅ Output: Produces expected DataFrame
- Status: APPROVED ✓

**Code Block 2: Feature Engineering**
- ❌ Syntax: Missing closing parenthesis on line 15
- ❌ Imports: Missing 'from datetime import datetime'
- Status: BLOCKED - Must fix before approval
- Fix applied: [describe fix]
- Re-test: ✅ Now passes
```

### Blocking Criteria:

**You CANNOT approve any implementation plan if:**
- ❌ ANY code block has syntax errors
- ❌ ANY import fails (package not available OR project not installed)
- ❌ ANY code block produces runtime errors (including `ModuleNotFoundError` for local imports)
- ❌ ANY function is a stub (contains only `pass` or `NotImplementedError`)
- ❌ ANY file path references non-existent files
- ❌ ANY code block is not self-contained (missing context)

**If validation fails, you MUST:**
1. Fix the code in the implementation plan
2. Re-test the fixed code
3. Document the fix
4. Verify all fixes before approval

---

## Prerequisites
Before validating implementation plans, review the project's data sources documentation ([docs/project_context/data_sources.md](../../../docs/project_context/data_sources.md)) to understand:
1. **Data access methods** (API, database, file download, etc.)
2. **Available datasets** (names, schemas, record counts, time spans)
3. **Data characteristics** (granularity, update frequency, completeness, quality)
4. **Technical constraints** (authentication, rate limits, access restrictions)
5. **Known limitations** (missing fields, aggregation levels, data gaps)

## Your Task
Review the implementation plan in each user story against the following comprehensive checklist. **Reflect on whether this is the best approach** given the constraints, then **directly update the implementation plan** to address any gaps, misalignments, or opportunities for improvement. Use the project's actual data sources documentation to ensure alignment. Make the implementation plan production-ready.

---

## Quick Validation Checklist (30-Second Triage)

**Use this for rapid assessment before detailed review:**

### 🚨 BLOCKERS (Must Fix Immediately - STOP EVERYTHING ELSE)
- [ ] **Code execution validation NOT completed** → **STOP - DO THIS FIRST (See Section: Mandatory First Step)**
- [ ] **ANY code has syntax errors** → **STOP - Fix and re-test**
- [ ] **ANY imports fail** → **STOP - Add to requirements.txt or find alternatives**
- [ ] **ANY code is stub/incomplete** → **STOP - Complete implementation**
- [ ] Data sources don't match documentation → **GO TO Section 1**
- [ ] Required data doesn't exist → **ESCALATE** (See Section 9.1 for rejection criteria)

### ⚠️ CRITICAL (High Priority)
- [ ] Wrong visualization types (time series → pie chart) → **GO TO Section 2.3**
- [ ] Missing security/privacy measures → **GO TO Section 5.4**
- [ ] No error handling → **GO TO Section 6.2**
- [ ] Fundamental feasibility issues → **ESCALATE** (See Section 9.1)

### 📋 IMPORTANT (Medium Priority)
- [ ] Incomplete pipeline stages → **GO TO Section 5.1**
- [ ] Missing Python best practices → **GO TO Section 6**
- [ ] Inadequate documentation → **GO TO Section 5.1.8**
- [ ] Unclear analysis methods → **GO TO Section 4.1**

**For detailed validation, proceed with full checklist below.**

---

## 1. Data Source Alignment Validation

### 1.1 Data Extraction Methods
**Review the project's data sources documentation, then check:**

- [ ] Does the implementation plan use the correct extraction method for this project?
  - API calls (verify endpoint, authentication method)
  - Database queries (verify connection method, credentials handling)
  - File downloads (verify source, download mechanism)
  - Web scraping (verify legality, rate limits, parsing approach)
  - Cloud storage (verify bucket/container access, credentials)

- [ ] Are authentication/access requirements addressed?
  - API keys, tokens, credentials properly referenced
  - Service account setup mentioned
  - Access permissions validated

- [ ] Are correct identifiers used?
  - Dataset/table names match documentation
  - File paths are accurate
  - Query parameters are correct

- [ ] Is the extraction method consistent with project infrastructure?
  - Uses existing connectors/modules if available
  - Follows project conventions
  - Includes error handling and retry logic

**Common Red Flags:**
- ❌ Extraction method doesn't match documented data source
- ❌ References non-existent datasets, tables, or files
- ❌ Missing extraction tasks entirely
- ❌ Assumes capabilities not supported (e.g., real-time when data is batch)
- ❌ Ignores authentication requirements
- ❌ No error handling for network/access issues

### 1.2 Data Availability Check
**Cross-reference against the project's data sources documentation:**

For each dataset/table/file referenced in the implementation plan, verify:

- [ ] **Existence**: Dataset/table/file actually exists and is accessible
- [ ] **Time span**: Temporal coverage matches user story requirements
  - Check start date, end date, update frequency
  - Identify any gaps in temporal coverage
- [ ] **Schema match**: Required columns/fields are present
  - Verify field names (case sensitivity, naming conventions)
  - Check data types match expected usage
- [ ] **Granularity**: Level of detail matches analysis needs
  - Temporal: hourly/daily/weekly/monthly/annual?
  - Geographic: national/regional/city/facility/individual?
  - Demographic: age groups, individual level?
- [ ] **Sufficient volume**: Record count adequate for statistical validity
  - Minimum samples per group for comparisons
  - Enough historical data for trends

**Common Misalignments to Check:**
- User story needs fine-grained data → Check if only aggregated data available
- Needs real-time/streaming → Check if data is batch/periodic only
- Requires specific breakdowns → Check if aggregation prevents desired slicing
- Wants historical trends → Check if sufficient temporal coverage exists
- Needs geographic analysis → Check if location data granular enough
- Requires demographic details → Check if PII restrictions limit access

### 1.3 Data Quality Assumptions
**Review data sources documentation for quality characteristics, then validate:**

- [ ] **Completeness**: Implementation plan addresses missing data appropriately
  - If data is complete: acknowledgment that no imputation needed
  - If data has gaps: imputation/handling strategy specified
- [ ] **Known anomalies**: Special periods or outliers are handled
  - Data disruptions (e.g., system changes, policy changes, crisis periods)
  - Seasonal effects or cyclical patterns
- [ ] **Update frequency**: Analysis design matches data refresh rate
  - Real-time/streaming data → appropriate real-time processing
  - Batch/periodic data → appropriate batch processing windows
  - Static/historical → acknowledgment of no updates
- [ ] **Documented limitations**: All known constraints are acknowledged
  - Granularity limitations
  - Coverage gaps (temporal, geographic, demographic)
  - Accuracy/precision limitations
  - Bias or sampling issues

---

## 2. Exploratory Data Analysis (EDA) Validation

### 2.1 Data Characterization
**Required EDA Steps:**
- [ ] Shape inspection (rows, columns) for each dataset
- [ ] Data type verification (numeric, categorical, datetime)
- [ ] Descriptive statistics (mean, median, std, min, max) for numeric variables
- [ ] Value range checks (verify against expected/documented ranges)
- [ ] Unique value counts for categorical variables
- [ ] Duplicate detection

### 2.2 Data Appropriateness for Analysis Type

**Time Series Data:**
If user story involves trends, seasonality, forecasting:
- [ ] Dataset has temporal dimension (year, month, date, timestamp)
- [ ] Sufficient time points for analysis (minimum 2-3 years for trends, more for seasonality)
- [ ] Consistent time intervals match analysis needs (hourly/daily/monthly/annual)
- [ ] Missing time periods identified and handled

**Demographic Analysis:**
If user story involves age, gender, race comparisons:
- [ ] Dataset contains demographic breakdowns
- [ ] Categories are clearly defined
- [ ] Sample sizes per group are adequate
- [ ] Statistical significance testing is planned

**Geographic Analysis:**
If user story involves location-based comparisons:
- [ ] Dataset has geographic identifiers (coordinates, regions, facilities, addresses)
- [ ] Geographic granularity matches analysis needs
- [ ] Coverage across locations is balanced (check for gaps)
- [ ] Spatial data quality assessed (accuracy, completeness)

**Cross-sectional Analysis:**
If comparing groups at single time point:
- [ ] Data from consistent time period
- [ ] Comparable metrics across groups

### 2.3 Visualization Appropriateness

**Match visualization to data type:**

| Data Type | Appropriate Visualizations | Inappropriate Visualizations |
|-----------|---------------------------|------------------------------|
| **Time series** (temporal data) | ✓ Line charts, area charts<br>✓ Seasonal decomposition plots<br>✓ Trend + seasonality components | ❌ Pie charts<br>❌ Static bar charts (for many time points) |
| **Categorical distributions** | ✓ Bar charts<br>✓ Grouped bar charts<br>✓ Stacked bar charts | ❌ Line charts<br>❌ Scatter plots |
| **Comparisons (groups)** | ✓ Grouped bar charts<br>✓ Box plots<br>✓ Violin plots | ❌ Single pie chart with many categories |
| **Correlations (numeric)** | ✓ Scatter plots<br>✓ Correlation matrices<br>✓ Heatmaps | ❌ Bar charts |
| **Proportions (parts of whole)** | ✓ Pie charts (≤5 categories)<br>✓ Stacked bar charts<br>✓ Treemaps | ❌ Line charts |
| **Geographic/Spatial** | ✓ Choropleth maps<br>✓ Location scatter maps<br>✓ Bubble maps | ❌ (Check if geographic data available) |
| **Distributions** | ✓ Histograms<br>✓ Density plots<br>✓ Box plots | ❌ Pie charts |

**Check Implementation Plan:**
- [ ] Visualizations match data type and structure
- [ ] Interactive dashboards use appropriate tools (Plotly, Dash, Streamlit, Tableau, Power BI)
- [ ] Time-changing data uses line/area charts, not static comparisons
- [ ] Heatmaps used for 2D patterns (time × category, factor1 × factor2)
- [ ] Geographic visualizations only if location data available with sufficient detail

**General Validation Principles:**
```
✓ GOOD: Line chart for temporal trends (any time series data)
✓ GOOD: Heatmap for 2D patterns (time × category, geographic × metric)
✓ GOOD: Bar chart for categorical comparisons (few categories)
❌ BAD: Pie chart for temporal data (time series → line chart)
❌ BAD: Bar chart for 15+ time points (use line chart)
❌ BAD: Geographic map without location coordinates/boundaries
```

---

## 3. Data Processing & Transformation Validation

### 3.1 Data Cleaning Tasks
**Check that standard cleaning steps are included (adapt based on data characteristics):**
- [ ] Date/time parsing and standardization (handling format variations, timezones)
- [ ] Column name standardization (consistent naming: snake_case, clear conventions)
- [ ] Data type conversions (string → numeric, datetime, categorical) with error handling
- [ ] Missing value handling (imputation, removal, flagging) with documentation
- [ ] Duplicate detection and removal (with configurable key columns)
- [ ] Outlier detection strategy (IQR, Z-score, domain-specific thresholds)
- [ ] Text cleaning (if working with free-text fields: whitespace, encoding, normalization)
- [ ] Unit standardization (currency, measurements, percentages) with validation
- [ ] Data validation checks (range checks, referential integrity, business rules)

### 3.2 Feature Engineering
**Check if appropriate features are created based on analysis needs:**
- [ ] Temporal features: year, month, quarter, day_of_week, hour (if temporal data)
- [ ] Derived metrics: rates, ratios, growth rates, per-capita/normalized values
- [ ] Aggregations: totals, averages, medians by relevant groupings
- [ ] Categorical encodings: one-hot, label encoding (for modeling)
- [ ] Interaction features: combinations of variables (if needed for analysis)
- [ ] Flags/indicators: special periods, outliers, thresholds, categories

**Validate Feature Data Availability:**
Every proposed feature must be computable from available data sources. Cross-reference the implementation plan's feature list against [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md) to ensure: (1) all required input fields exist in documented data sources, (2) data granularity supports the calculation (e.g., computing weekly aggregations requires daily/hourly data, not monthly), (3) any domain-driven features (attack rates, burden indices, workforce ratios) have the necessary base data available. **Reject features that cannot be reliably computed** from existing data sources, and update the implementation plan to remove these pending data acquisition.

### 3.3 Data Integration
**For multi-table/multi-source analyses:**
- [ ] Join keys identified and validated (common columns across datasets)
- [ ] Join type specified and appropriate (inner, left, right, outer, cross)
- [ ] Handling of mismatched granularity (e.g., daily vs monthly, facility vs regional)
- [ ] Schema alignment (consistent column names, data types, units)
- [ ] Handling of missing matches (strategy for unmatched records)
- [ ] Data lineage tracking (source of each field after integration)

---

## 4. Analysis Method Validation

### 4.1 Statistical Methods Appropriateness
**Match method to data and question:**

| Analysis Goal | Appropriate Methods | Check Implementation |
|--------------|---------------------|---------------------|
| **Trend detection** | Linear regression, moving averages, time series decomposition | [ ] Method specified<br>[ ] Libraries included |
| **Group comparisons** | t-tests, ANOVA, chi-square tests | [ ] Statistical tests named<br>[ ] Significance level defined (α=0.05) |
| **Anomaly detection** | Z-scores, IQR method, control charts, isolation forest | [ ] Threshold defined<br>[ ] Validation approach |
| **Clustering** | K-means, hierarchical, DBSCAN | [ ] Distance metric<br>[ ] Optimal clusters method |
| **Forecasting** | ARIMA, exponential smoothing, Prophet, LSTM | [ ] Train/test split<br>[ ] Evaluation metrics |
| **Classification** | Logistic regression, decision trees, random forest, SVM | [ ] Class balance checked<br>[ ] Metrics appropriate for problem |
| **Regression** | Linear, polynomial, ridge, lasso, random forest | [ ] Assumptions validated<br>[ ] Residual analysis |

### 4.2 Model Validation
**If predictive modeling involved:**
- [ ] Train/test split strategy (e.g., temporal split for time series)
- [ ] Cross-validation approach (if appropriate)
- [ ] Performance metrics defined (RMSE, MAE, accuracy, precision/recall)
- [ ] Baseline model for comparison
- [ ] Overfitting prevention (regularization, validation set)

### 4.3 Causal Inference Considerations
**If claiming causation:**
- [ ] Appropriate causal inference methods used (not just correlation)
- [ ] Confounding variables considered
- [ ] Limitations explicitly stated
- [ ] Language is careful ("associated with" vs "causes")

---

## 5. Implementation Completeness Check

### 5.1 End-to-End Pipeline Coverage
**Verify ALL stages are addressed:**

1. **Data Extraction** ✓
   - [ ] Connection to data source (using documented method)
   - [ ] Authentication/access handling
   - [ ] Download/caching strategy (if applicable)
   - [ ] Data loading into workspace

2. **Data Validation** ✓
   - [ ] Schema validation (structure, fields, types)
   - [ ] Quality checks (completeness, accuracy, consistency)
   - [ ] Error handling and logging

3. **Data Preprocessing** ✓
   - [ ] Cleaning steps (missing values, duplicates, outliers)
   - [ ] Transformation steps (types, formats, normalization)
   - [ ] Feature engineering (derived fields, aggregations)

4. **Exploratory Data Analysis** ✓
   - [ ] Summary statistics
   - [ ] Distribution analysis
   - [ ] Relationship/correlation analysis
   - [ ] Pattern identification

5. **Statistical Analysis** ✓
   - [ ] Hypothesis tests
   - [ ] Modeling (if applicable)
   - [ ] Validation

6. **Visualization** ✓
   - [ ] Exploratory plots
   - [ ] Final presentation visualizations
   - [ ] Interactive dashboards (if specified)

7. **Interpretation & Reporting** ✓
   - [ ] Results documentation
   - [ ] Limitations and assumptions documented
   - [ ] Recommendations provided
   - [ ] Business/research insights articulated

8. **Code Documentation** ✓
   - [ ] Docstrings for functions and classes (Google/NumPy style, with examples)
   - [ ] README/documentation files (setup, usage, examples)
   - [ ] Reproducibility instructions (step-by-step execution guide)
   - [ ] Environment/dependency specifications (requirements.txt, environment.yml)
   - [ ] Type hints for function parameters and return values
   - [ ] Inline comments for complex logic or business rules

9. **Code Quality & Testing** ✓
   - [ ] Unit tests for critical functions (data transformations, calculations)
   - [ ] Integration tests for pipeline stages
   - [ ] Data validation tests (schema, ranges, business rules)
   - [ ] Error handling with informative messages
   - [ ] Logging at appropriate levels (INFO, WARNING, ERROR)
   - [ ] Code follows PEP 8 style guidelines
   - [ ] Functions are modular and reusable
   - [ ] Avoid hardcoded values (use config files or constants)

### 5.2 Dependency Management
**Check all dependencies are realistic:**

**External Packages:**
- [ ] All packages are accessible (open-source, licensed, or available in environment)
- [ ] Package versions specified (if critical for reproducibility)
- [ ] Installation instructions provided (pip, conda, npm, etc.)
- [ ] No unavailable proprietary tools or expired subscriptions
- [ ] Language-appropriate libraries (Python, R, SQL, etc.)

**Common packages by category (verify availability for project):**
```
Data Manipulation: polars, numpy, dplyr, data.table
Statistical Analysis: scipy, statsmodels, scikit-learn, stats, forecast
Visualization: matplotlib, seaborn, plotly, ggplot2, altair
ML/AI: tensorflow, pytorch, keras, xgboost, lightgbm
Database: sqlalchemy, psycopg2, pymongo, pyodbc
API: requests, httpx, aiohttp
Cloud: boto3 (AWS), google-cloud, azure-sdk
```

**Internal Dependencies:**
- [ ] References to internal modules that actually exist in the project
- [ ] Uses project connectors/utilities if available
- [ ] Follows project conventions and patterns
- [ ] No references to non-existent internal modules

### 5.3 Configuration & Environment
**Infrastructure considerations (based on project setup):**
- [ ] Platform/environment specified correctly (cloud, on-prem, local, notebook environment)
- [ ] Compute requirements considered (memory, CPU, GPU if needed)
- [ ] Storage requirements addressed (disk space, database capacity)
- [ ] Output storage plan (where results saved, retention policy)
- [ ] Logging framework referenced or specified (Python logging, loguru)
- [ ] Configuration management (env vars, config files, secrets handling)
- [ ] Scalability considerations (if dealing with large data volumes)
- [ ] Performance optimization (vectorization, chunking, parallel processing)
- [ ] Memory management (chunked reading, garbage collection for large datasets)

### 5.4 Security & Privacy
**Critical security checks (especially for healthcare/sensitive data):**
- [ ] **Credentials management**: No hardcoded passwords, API keys, or tokens
  - Use environment variables or secure credential stores
  - Credentials in .gitignore (never committed to version control)
- [ ] **PII/PHI protection**: Personal/health information handling compliant with regulations
  - Data anonymization/pseudonymization where required
  - Access controls and audit logging for sensitive data
- [ ] **Data encryption**: At-rest and in-transit encryption for sensitive data
- [ ] **Input validation**: Sanitize inputs to prevent injection attacks (SQL, command)
- [ ] **Error messages**: Don't expose sensitive information in logs/errors
- [ ] **Third-party dependencies**: Security audit of external packages
- [ ] **Data retention**: Clear policies on data storage duration and deletion

### 5.5 Code Execution Validation ⚠️ MANDATORY QUALITY GATE

**🚫 BLOCKING REQUIREMENT - NO EXCEPTIONS:**

Before approving ANY implementation plan, you MUST validate code executability by actually running ALL code blocks. This is not optional.

**EXECUTION PROCESS:**

1. **Create test environment** (if needed):
   ```bash
   cd /Users/qytay/Documents/GitHub/gen-e2-data-analysis-MOH
   source .venv/bin/activate
   ```

2. **Test each code block** using preferred method:
   
   **Method A: Pylance MCP Tool (PREFERRED)**
   ```python
   # Use mcp_pylance_mcp_s_pylanceRunCodeSnippet for each code block
   # This validates syntax, imports, and execution
   ```
   
   **Method B: Terminal Execution**
   ```bash
   # Test imports first
   python -c "import polars as pl; import numpy as np; print('✓')"
   
   # Test complete script
   python scripts/test_code_block.py
   ```

3. **Document results** for each block:
   - Syntax validation: Pass/Fail
   - Import verification: Pass/Fail  
   - Execution test: Pass/Fail
   - Output verification: Pass/Fail

4. **Fix ALL failures** before proceeding

5. **Re-test after fixes** to confirm resolution

**Why This is Critical:**
- Next step after plan approval is immediate execution
- Syntax errors waste significant time and resources
- Runtime errors discovered during execution disrupt workflow
- Missing imports cause pipeline failures
- Invalid file paths halt entire analysis
- Non-executable code damages credibility and project timelines

**Pre-Notebook Output Requirements - ALL MUST PASS:**
- [ ] **Syntax validation**: Check for Python syntax errors (missing colons, unclosed brackets, indentation)
- [ ] **Import verification**: Test ALL imports - verify packages are installed and accessible
  ```python
  # Test each import separately
  import polars as pl
  import numpy as np
  import matplotlib.pyplot as plt
  # etc.
  ```
- [ ] **Run code snippets**: Execute ALL code blocks using `mcp_pylance_mcp_s_pylanceRunCodeSnippet` or terminal
- [ ] **Data path validation**: Confirm all referenced data files/paths actually exist
  ```python
  # Verify paths before using
  import os
  assert os.path.exists('data/1_raw/sample_data.csv'), "Data file not found"
  ```
- [ ] **Variable definition check**: Ensure all variables are defined before use (no NameError)
- [ ] **Function signature validation**: Verify correct number of arguments for all function calls
- [ ] **Data type compatibility**: Check operations don't mix incompatible types
- [ ] **Error-free execution**: Code runs without runtime errors (AttributeError, TypeError, ValueError, etc.)
- [ ] **Output verification**: Validate that expected outputs (DataFrames, plots, metrics) are actually produced
- [ ] **Environment compatibility**: Test with project's Python environment and dependencies

**Mandatory Validation Process:**

**Step 1: Extract & Inventory**
- [ ] Extract ALL code segments from implementation plan
- [ ] Create checklist of every code block requiring validation
- [ ] Identify dependencies between code blocks (execution order)

**Step 2: Test Imports First**
- [ ] Test EVERY import statement individually
- [ ] Verify package availability in environment
- [ ] Fix missing packages (add to requirements.txt) or find alternatives
- [ ] Document all import dependencies

**Step 3: Validate File Paths**

**⚠️ Never assume working directory** - Use explicit path construction from file location.

- [ ] List ALL file paths referenced in code
- [ ] Use `pathlib.Path` for cross-platform path construction
- [ ] Calculate paths relative to file location (not assumed CWD)
- [ ] Validate path existence before file operations
- [ ] Test paths from the file's actual execution location

**Recommended Pattern:**
```python
from pathlib import Path

# Calculate project root from file location
# Example: notebook in src/problem-statement-001/notebooks/
notebook_dir = Path.cwd()  # Or Path(__file__).parent for scripts
project_root = notebook_dir.parent.parent.parent  # Adjust depth as needed
data_path = project_root / 'data' / '3_interim' / 'file.parquet'

# Validate before using
if not data_path.exists():
    raise FileNotFoundError(f"Not found: {data_path}")
```

**Common Mistakes:**
- ❌ `df = pl.read_csv('data/file.csv')` - assumes CWD is project root
- ❌ Hardcoded absolute paths - not portable across machines
- ✅ Use Path construction from file location with existence checks

**Step 4: Execute Each Code Block**
- [ ] Run each code segment using validation tools (see tool selection guide below)
- [ ] Start with simple blocks (imports, path validation, data loading)
- [ ] Progress to complex blocks (transformations, analysis)
- [ ] Verify path resolution works from file's actual location
- [ ] Capture and review all outputs

**Tool Selection Guide:**
- **Use `mcp_pylance_mcp_s_pylanceRunCodeSnippet`** (PREFERRED):
  - ✓ For Python code snippets (single blocks, functions)
  - ✓ Quick validation of imports and small functions
  - ✓ Testing expressions and calculations
  - ✓ No shell escaping/quoting issues
  - ✓ Automatically uses workspace Python environment
   - ✓ Independent code blocks with NO variable dependencies
  
- **Use Terminal (`run_in_terminal`)**:
  - ✓ For running complete scripts (`.py` files)
  - ✓ When testing CLI tools or command-line arguments
  - ✓ For integration testing of full pipelines
  - ✓ When working with notebooks (execute via `jupyter nbconvert --execute`)
  - ✓ **Testing interdependent code blocks** (blocks that share variables)
  - ⚠️ Requires proper Python path/environment activation

**Terminal Execution Examples:**
```bash
# Test imports in terminal
python -c "import polars as pl; import numpy as np; print('✓ Imports successful')"

# Run complete script
python scripts/data_processing.py

# Execute notebook (validates all cells)
jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb --output test_output.ipynb

# Test with specific data file
python scripts/analyze.py --input data/1_raw/sample.csv
```

**Handling Interdependent Code Blocks:**

When code blocks depend on variables from previous blocks (e.g., Block 2 uses `df` from Block 1), use one of these approaches:

**Option A: Combine into Test Script** (Recommended)
```python
# test_validation.py
import polars as pl

# Block 1: Load data
df = pl.read_csv('data/1_raw/data.csv')
print(f"✓ Block 1: Loaded {df.shape[0]} rows")

# Block 2: Clean data (depends on df)
df_clean = df.drop_nulls(subset=['date', 'cases'])
print(f"✓ Block 2: Cleaned to {df_clean.shape[0]} rows")

# Block 3: Transform (depends on df_clean)
df_final = df_clean.with_columns([
    (pl.col('cases') / pl.col('population') * 100000).alias('rate')
])
print(f"✓ Block 3: Added rate column")
print("✅ All interdependent blocks validated")
```
**Execute via terminal**: `python test_validation.py`

**Option B: Cumulative Validation with Context**
Test each block by including necessary context from previous blocks:
```python
# Test Block 2 with Block 1 context
import polars as pl
df = pl.read_csv('data/1_raw/data.csv')  # Context from Block 1
df_clean = df.drop_nulls(subset=['date', 'cases'])  # Block 2 to test
print(f"✓ Block 2 successful: {df_clean.shape}")
```

**Step 4b: Analyze Output & Adapt Implementation Plan (CRITICAL)**

**🔍 MANDATORY WORKFLOW - Follow These Steps:**

1. **RUN your EDA code first** → Review the actual output
2. **ANALYZE output for data quality issues** → What problems exist in THIS specific dataset?
3. **IDENTIFY actual issues present** → List only issues you observed in output
4. **ADD targeted handling steps** → For each discovered issue, add specific code to implementation plan
5. **IGNORE issues not present** → Do NOT add handling for problems that don't exist in your data

**⚠️ CRITICAL: Output-Driven Approach (NOT Checklist-Driven)**

**❌ WRONG APPROACH:**
- Going through reference table and "checking off" each issue type
- Adding handling code for issues that don't exist in your data
- Applying examples mechanically without understanding context

**✅ CORRECT APPROACH:**
```python
# 1. Run EDA first
df = pl.read_csv('data.csv')
print(df.describe())  # Look at actual output
print(df.select(pl.all().is_null().sum()))  # Check what's actually missing

# 2. Analyze what YOU see in output:
# OUTPUT SHOWS: 'age' has 200/1000 nulls (20%), max=125 (impossible)
#               'gender' looks fine, no issues
#               'date' has proper format, no nulls

# 3. Address ONLY what you found:
# - Need to handle age nulls (20% is handleable)
# - Need to fix impossible age values (>120)
# - gender and date are fine → NO handling code needed
```

**The reference table below is for GUIDANCE ONLY** - use it to understand common issues and handling approaches, but ONLY implement handling for issues you actually discover in your data output.

**Data Quality Issues Discovered → Add Handling Steps (REFERENCE GUIDE)**

| Output Finding | Detection Signal | Required Next Steps | Add to Implementation Plan |
|----------------|------------------|---------------------|----------------------------|
| **Outliers detected** | `df.describe()` shows extreme min/max<br>Box plots show points beyond whiskers | - [ ] Investigate outliers (data entry errors vs real extremes)<br>- [ ] Document outlier handling strategy (remove, cap, transform, keep)<br>- [ ] Create outlier detection function with configurable thresholds<br>- [ ] Validate downstream analysis with/without outliers | ```python<br># Add outlier detection & handling<br>def detect_outliers(df, col, method='IQR', threshold=1.5):<br>    """Detect outliers using IQR or Z-score"""<br>    if method == 'IQR':<br>        Q1, Q3 = df[col].quantile([0.25, 0.75])<br>        IQR = Q3 - Q1<br>        lower = Q1 - threshold * IQR<br>        upper = Q3 + threshold * IQR<br>        return df.filter((pl.col(col) < lower) | (pl.col(col) > upper))<br>``` |
| **Missing data patterns** | `.null_count()` shows nulls<br>`df.select(pl.all().is_null().sum())` | - [ ] Quantify missingness (% per column, patterns across rows)<br>- [ ] Determine if Missing at Random (MAR) or systematic<br>- [ ] Choose imputation strategy (mean, median, mode, forward-fill, model-based)<br>- [ ] Document impact on analysis validity | ```python<br># Analyze missingness<br>missing_summary = df.select([<br>    (pl.col(c).is_null().sum() / len(df) * 100).alias(f"{c}_missing_%")<br>    for c in df.columns<br>])<br># Strategy: drop if >30% missing, impute if <30%<br>``` |
| **Categorical inconsistencies** | `.value_counts()` shows:<br>- Typos ('Male' vs 'male')<br>- Multiple encodings (1/0 vs Yes/No)<br>- Unexpected categories | - [ ] Standardize categorical values (case normalization, mapping)<br>- [ ] Create category validation rules<br>- [ ] Document encoding scheme (label mapping)<br>- [ ] Handle 'Unknown'/'Other' categories consistently | ```python<br># Standardize categories<br>df = df.with_columns([<br>    pl.col('gender').str.to_lowercase().replace({<br>        'm': 'male', 'f': 'female',<br>        '1': 'male', '0': 'female'<br>    })<br>])<br># Validate against allowed values<br>``` |
| **Date/time issues** | Non-sequential dates<br>Future dates<br>Invalid formats | - [ ] Parse dates with multiple format handlers<br>- [ ] Validate date ranges (earliest/latest reasonable dates)<br>- [ ] Handle timezone conversions if needed<br>- [ ] Fill date gaps for time series (identify missing periods) | ```python<br># Robust date parsing<br>df = df.with_columns([<br>    pl.col('date').str.strptime(pl.Date, '%Y-%m-%d', strict=False)<br>])<br># Validate range<br>df = df.filter(<br>    (pl.col('date') >= datetime(2000, 1, 1)) &<br>    (pl.col('date') <= datetime.now())<br>)<br>``` |
| **Data type mismatches** | Numeric stored as string<br>Categories as numbers | - [ ] Convert types with error handling (try-except for invalid values)<br>- [ ] Flag conversion failures for manual review<br>- [ ] Validate ranges after conversion | ```python<br># Safe type conversion<br>df = df.with_columns([<br>    pl.col('cases').cast(pl.Int64, strict=False)<br>])<br># Check conversion failures<br>failed = df.filter(pl.col('cases').is_null())<br>``` |
| **Duplicate records** | `.unique()` count < total rows<br>Key columns have duplicates | - [ ] Define uniqueness criteria (which columns define a unique record)<br>- [ ] Investigate duplicate sources (data entry, ETL issues)<br>- [ ] Choose deduplication strategy (keep first/last/aggregate)<br>- [ ] Log removed duplicates for audit | ```python<br># Detect duplicates<br>duplicates = df.filter(<br>    pl.struct(['patient_id', 'date']).is_duplicated()<br>)<br># Remove duplicates (keep first)<br>df = df.unique(subset=['patient_id', 'date'], keep='first')<br>``` |
| **Skewed distributions** | Histograms highly right-skewed<br>Most values near zero | - [ ] Consider log transformation for modeling<br>- [ ] Use median instead of mean for central tendency<br>- [ ] Apply non-parametric tests (Mann-Whitney vs t-test)<br>- [ ] Document distribution characteristics in limitations | ```python<br># Transform skewed variable<br>df = df.with_columns([<br>    pl.col('income').log1p().alias('log_income')<br>])<br># Use robust statistics<br>median_income = df['income'].median()<br>``` |
| **Imbalanced classes** | `.value_counts()` shows 95/5 split | - [ ] Use stratified sampling for train/test split<br>- [ ] Apply SMOTE or class weighting for modeling<br>- [ ] Use appropriate metrics (F1, precision-recall vs accuracy)<br>- [ ] Consider collecting more minority class data | ```python<br># Check class balance<br>class_dist = df['outcome'].value_counts()<br>print(f"Class imbalance ratio: {class_dist[0] / class_dist[1]}")<br># Plan: Use class_weight='balanced' in models<br>``` |
| **Correlation issues** | Heatmap shows multicollinearity (r > 0.9) | - [ ] Calculate VIF (Variance Inflation Factor)<br>- [ ] Remove redundant features for regression<br>- [ ] Use PCA or feature selection<br>- [ ] Document feature relationships | ```python<br># Check correlation<br>corr_matrix = df.select(numeric_cols).corr()<br>high_corr = corr_matrix[corr_matrix > 0.9]<br># Plan: Drop one of highly correlated pairs<br>``` |
| **Insufficient sample size** | Group counts < 30 per category<br>Short time series (< 24 months) | - [ ] Flag low-power comparisons<br>- [ ] Consider grouping rare categories<br>- [ ] Use exact tests (Fisher's) instead of asymptotic tests<br>- [ ] Document statistical limitations<br>- [ ] Recommend data collection expansion | ```python<br># Check sample sizes<br>group_sizes = df.group_by('category').count()<br>small_groups = group_sizes.filter(pl.col('count') < 30)<br>if len(small_groups) > 0:<br>    print(f"⚠️  {len(small_groups)} groups with n<30")<br>``` |

**Mandatory Actions After Analyzing Output:**

1. **Update Implementation Plan with Handling Steps (ADAPTED TO YOUR DATA)**
   - [ ] For EACH data quality issue **actually discovered in your output**, add specific handling tasks to implementation plan
   - [ ] Do NOT add handling for issues that don't exist in your data
   - [ ] If you find issues not in the reference table, create appropriate handling steps
   - [ ] Include detection code, handling logic, and validation steps
   - [ ] Prioritize issues by impact on analysis validity
   - [ ] **Justify each handling decision** - why this approach for this specific issue?

2. **Create Data Quality Functions (ONLY FOR ACTUAL ISSUES)**
   - [ ] Write reusable functions for each handling strategy
   - [ ] Include logging for tracking applied transformations
   - [ ] Document assumptions and thresholds

3. **Test ALL New Handling Code**
   - [ ] Run detection code to confirm it identifies the issue
   - [ ] Execute handling code and verify it resolves the issue

---

## 🔒 FINAL APPROVAL GATE

**Before approving ANY implementation plan, complete this checklist:**

### Code Executability (MANDATORY - MUST BE 100%)
- [ ] ALL code blocks extracted and inventoried
- [ ] ALL code blocks tested using validation tools
- [ ] ALL syntax errors fixed and re-tested
- [ ] ALL import statements verified (packages available)
- [ ] ALL file paths validated (files/directories exist)
- [ ] ALL functions fully implemented (no stubs)
- [ ] ALL code blocks executed without errors
- [ ] ALL expected outputs verified
- [ ] Validation results documented for each code block

### Plan Quality (Standard Validation)
- [ ] Data sources match project documentation
- [ ] Analysis methods appropriate for data type
- [ ] Visualizations match data structure
- [ ] All pipeline stages covered
- [ ] Security/privacy requirements addressed
- [ ] Testing strategy comprehensive
- [ ] Documentation complete

### Approval Decision
- [ ] **APPROVED** - All code validated, all checks passed
- [ ] **BLOCKED** - Issues documented, fixes required before approval

**Sign-off:** Implementation plan validated and ready for execution ✓

---

## Post-Validation: Update Implementation Plan

**After validation, you MUST update the implementation plan to include:**

1. **Validation Status Section** (add at the end of implementation plan):
```markdown
## ✅ Code Validation Status

**Validation Date:** [Date]
**Validator:** AI Agent (Reflection Stage)
**Status:** APPROVED for execution

### Validation Summary:
- Total code blocks: [X]
- Syntax validation: ✅ All passed
- Import verification: ✅ All passed  
- Execution tests: ✅ All passed
- Output verification: ✅ All passed

### Tested Components:
1. Data extraction functions - ✅ Executed successfully
2. Data cleaning pipeline - ✅ Executed successfully
3. Feature engineering - ✅ Executed successfully
4. Analysis methods - ✅ Executed successfully
5. Visualization code - ✅ Executed successfully

### Environment Verified:
- Python version: [version]
- Key packages: polars [version], numpy [version], etc.
- Project path: /Users/qytay/Documents/GitHub/gen-e2-data-analysis-MOH

**All code blocks are executable and ready for production deployment.**
```

2. **Fix Documentation** (for any code that was corrected):
```markdown
### Code Corrections Applied:

**Issue 1:** Missing import statement in data loading function
- Original: Missing `from pathlib import Path`
- Fixed: Added import at top of function
- Re-tested: ✅ Passes

**Issue 2:** Syntax error in feature engineering (line 25)
- Original: Unclosed parenthesis
- Fixed: Added closing parenthesis
- Re-tested: ✅ Passes
```

This ensures the next person knows the code has been validated and is ready to execute.
   - [ ] Validate downstream analysis works with cleaned data
   - [ ] **Zero tolerance for errors in new code**

4. **Document Impact**
   - [ ] Record what % of data affected by each issue
   - [ ] Document handling decisions and rationale
   - [ ] Note limitations introduced by handling choices

**Example Workflow:**
```python
# 1. Run initial EDA code
df = pl.read_csv('data.csv')
print(df.describe())
print(df.select(pl.all().is_null().sum()))
# OUTPUT SHOWS: 'age' column has 15% nulls, 3 outliers > 120 years

# 2. ANALYZE OUTPUT → Identify issues:
#    - Missing age data (15%)
#    - Invalid ages (biologically impossible)

# 3. ADD HANDLING STEPS TO PLAN:
# - [ ] Investigate age missingness pattern
# - [ ] Impute age using median by gender
# - [ ] Cap age at reasonable max (100 years)
# - [ ] Flag records with data quality issues

# 4. WRITE & TEST HANDLING CODE:
def clean_age_data(df: pl.DataFrame) -> pl.DataFrame:
    """Clean age column: impute missing, cap outliers"""
    # Detect issues
    missing_count = df['age'].is_null().sum()
    outliers = df.filter(pl.col('age') > 120)
    
    print(f"Found {missing_count} missing ages, {len(outliers)} outliers")
    
    # Handle: impute with median by gender
    df = df.with_columns([
        pl.col('age').fill_null(
            pl.col('age').median().over('gender')
        )
    ])
    
    # Cap at 100
    df = df.with_columns([
        pl.when(pl.col('age') > 100)
          .then(100)
          .otherwise(pl.col('age'))
          .alias('age')
    ])
    
    return df

# 5. TEST the handling code
df_cleaned = clean_age_data(df)
assert df_cleaned['age'].is_null().sum() == 0, "Still have missing ages"
assert df_cleaned['age'].max() <= 100, "Still have invalid ages"
print("✓ Age cleaning successful")

# 6. VALIDATE downstream analysis works
# Re-run analysis code with cleaned data to ensure no errors
```

**🚫 BLOCKING CHECKPOINT:**
- ❌ Do NOT proceed if new handling code has errors
- ❌ Do NOT skip testing adaptive steps
- ❌ Do NOT assume handling will work without validation

**Step 5: Fix All Errors (Zero Tolerance)**
- [ ] **Syntax errors**: Fix missing colons, incorrect indentation, unclosed brackets/parentheses
- [ ] **Import errors**: Install missing packages or use alternative libraries
- [ ] **NameError**: Define all variables before use, fix typos in variable names
- [ ] **AttributeError**: Verify objects have the called methods/attributes
- [ ] **TypeError**: Fix incompatible data type operations
- [ ] **ValueError**: Fix invalid values passed to functions
- [ ] **KeyError**: Verify dictionary keys and DataFrame columns exist
- [ ] **FileNotFoundError**: Fix file paths or create missing files
- [ ] **Logic errors**: Verify calculations, fix function arguments

**Step 6: Re-test After Fixes**
- [ ] Re-run ALL modified code blocks
- [ ] Verify fixes didn't introduce new errors
- [ ] Confirm expected outputs are produced

**Step 7: Integration Test**
- [ ] Run code blocks in execution order (end-to-end)
- [ ] Verify data flows correctly between steps
- [ ] Confirm final outputs meet requirements

**Step 8: Document Validation**
- [ ] Add validation stamp to implementation plan:
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

**Step 9: Only After 100% Pass Rate**
- [ ] Output as notebook or implementation file
- [ ] Approve implementation plan for execution
- [ ] Provide to next stage with confidence


**🚫 STOP - Red Flags (DO NOT output notebook/approve plan if ANY present):**
- ❌ **Syntax errors**: Missing colons, unclosed brackets, indentation errors
- ❌ **Import errors**: Required packages not installed or unavailable
- ❌ **File path errors**: Referenced data files don't exist at specified paths
- ❌ **Runtime exceptions**: Code throws any exception during execution
- ❌ **Function call errors**: Wrong number of arguments, invalid parameter names
- ❌ **Variable errors**: Variables used before definition, typos in variable names
- ❌ **Type errors**: Incompatible data types in operations
- ❌ **Attribute errors**: Methods/attributes don't exist on objects
- ❌ **Key errors**: Dictionary keys or DataFrame columns don't exist
- ❌ **Logic errors**: Calculations produce wrong results
- ❌ **Untested code**: ANY code block that hasn't been executed and verified

**Example Validation Workflow (Follow This Pattern):**

```python
# STEP 1: Test imports individually
test_code = """
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path
print("All imports successful")
"""
# → RUN using mcp_pylance_mcp_s_pylanceRunCodeSnippet
# → VERIFY: No ImportError

# STEP 2: Test path resolution and data loading
test_code = """
from pathlib import Path
import polars as pl

# Calculate project root from file location
notebook_dir = Path.cwd()
project_root = notebook_dir.parent.parent.parent
data_path = project_root / 'data' / '1_raw' / 'sample_data.csv'

if not data_path.exists():
    raise FileNotFoundError(f"Not found: {data_path}")

df = pl.read_csv(data_path)
print(f"✓ Loaded {df.shape[0]} rows from: {data_path}")
"""
# → RUN and verify path resolves correctly + data loads
# → VERIFY: DataFrame has expected structure

# STEP 4: Test data transformation
test_code = """
# Assumes df is loaded from previous step
if 'cases' not in df.columns:
    raise KeyError("Column 'cases' not found")
if 'population' not in df.columns:
    raise KeyError("Column 'population' not found")

df['rate'] = (df['cases'] / df['population']) * 100000
print(f"Rate statistics:")
print(df['rate'].describe())
print(f"✓ Transformation successful")
"""
# → RUN and verify calculation works
# → VERIFY: No division by zero, results are reasonable

# STEP 5: Test visualization
test_code = """
import matplotlib.pyplot as plt

if 'date' not in df.columns:
    raise KeyError("Column 'date' not found")

plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['cases'])
plt.title('Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Cases')
plt.tight_layout()
print("✓ Visualization created successfully")
"""
# → RUN and verify plotting works without errors

# STEP 6: Only after ALL tests pass with ✓
# → Add validation stamp to implementation plan
# → Output notebook or approve for execution
```

**Validation Checklist (Must Complete Before Approval):**
```markdown
- [ ] All imports tested individually - 0 ImportError
- [ ] All file paths verified - 0 FileNotFoundError  
- [ ] All code blocks executed - 0 runtime errors
- [ ] Outputs analyzed for data quality issues (Step 4b)
- [ ] Handling steps added for discovered issues (outliers, missing data, inconsistencies)
- [ ] All adaptive/handling code tested and validated - 0 errors
- [ ] All outputs verified - expected results produced
- [ ] Integration test passed - end-to-end execution successful
- [ ] Validation documented in implementation plan
```

**🛑 MANDATORY QUALITY GATE:**

**This is a BLOCKING requirement with ZERO tolerance for failures:**
- ❌ If validation fails → FIX all errors → RE-VALIDATE → Only then proceed
- ❌ Do NOT output notebooks/scripts with untested code
- ❌ Do NOT approve implementation plans with known errors
- ❌ Do NOT proceed to execution phase without 100% validation

**Consequence of skipping validation:**
- Pipeline failures during execution
- Wasted developer time debugging
- Delayed project timelines
- Loss of stakeholder confidence
- Increased technical debt

**If you cannot validate code due to missing tools or environment, explicitly state this and defer implementation approval until validation can be completed.**

---

## 6. Python Best Practices Validation

### 6.1 Code Structure & Organization
**Check for proper Python project structure:**
- [ ] Clear separation of concerns (data loading, processing, analysis, visualization)
- [ ] Functions are focused and do one thing well (single responsibility)
- [ ] Classes used appropriately (not over-engineering with unnecessary OOP)
- [ ] Module organization follows logical grouping
- [ ] Imports are organized (standard lib, third-party, local)
- [ ] No circular dependencies between modules
- [ ] **Path handling uses `pathlib.Path` with explicit construction from file location**
- [ ] **No hardcoded absolute paths or working directory assumptions**
- [ ] **Paths calculated relative to script/notebook location, not assumed CWD**

### 6.2 Error Handling & Robustness
**Ensure code handles failures gracefully:**
- [ ] Try-except blocks with specific exception types (not bare `except:`)
- [ ] Custom exceptions for domain-specific errors
- [ ] Proper error messages that aid debugging
- [ ] Cleanup in finally blocks (file handles, connections)
- [ ] Validation of inputs before processing
- [ ] Graceful degradation when non-critical features fail
- [ ] Retry logic for network operations (with exponential backoff)

### 6.3 Performance & Efficiency
**Check for performance best practices:**
- [ ] Vectorized operations (polars/numpy) instead of loops where possible
- [ ] Efficient data structures (sets for membership tests, dicts for lookups)
- [ ] Chunked processing for large datasets (avoid loading everything in memory)
- [ ] Database queries optimized (proper indexes, avoid N+1 queries)
- [ ] Caching of expensive computations
- [ ] Lazy evaluation where appropriate (generators, itertools)
- [ ] Profiling identified bottlenecks (not premature optimization)

### 6.4 Reproducibility & Version Control
**Ensure results can be reproduced:**
- [ ] Random seeds set for stochastic operations (random, numpy, sklearn)
- [ ] Package versions pinned (requirements.txt with specific versions)
- [ ] Data versioning strategy (DVC, timestamps, checksums)
- [ ] Git workflow follows best practices (meaningful commits, .gitignore)
- [ ] No generated files or data committed (unless specifically needed)
- [ ] Clear instructions for environment setup
- [ ] Intermediate results can be cached and reused

---

## 7. Scenario Coverage Validation

### 7.1 Acceptance Criteria Mapping
**For each acceptance criterion:**
- [ ] At least one implementation task addresses it
- [ ] Task is specific and measurable
- [ ] Success can be objectively verified
- [ ] No acceptance criteria are orphaned (without tasks)

### 7.2 Edge Cases & Data Limitations
**Check if implementation handles project-specific limitations:**
- [ ] Known data anomalies or disruption periods
- [ ] Missing variables or incomplete coverage
- [ ] Limited granularity (temporal, geographic, categorical)
- [ ] Sparse data (limited historical records, small sample sizes)
- [ ] Data aggregation constraints
- [ ] Privacy/anonymization impacts on analysis
- [ ] Data quality issues documented in data sources

### 7.3 Known Data Constraints
**Validate awareness of documented constraints (examples - adapt to your project):**

| Constraint Type | Potential Implications | Check Implementation |
|----------------|----------------------|---------------------|
| Temporal granularity | Limited to available intervals (hourly/daily/monthly/annual) | [ ] Acknowledged in limitations |
| Geographic aggregation | Analysis constrained to available geographic levels | [ ] Uses appropriate data |
| Data freshness | Latest data date limits recency of insights | [ ] Noted in assumptions |
| Update frequency | Real-time vs batch determines monitoring capabilities | [ ] Design matches data refresh |
| Completeness | Missing data affects analysis methods | [ ] Handling strategy specified |
| Sample size | Small samples limit statistical power | [ ] Power analysis or caveats included |
| Bias/Representativeness | Sampling or collection bias affects generalizability | [ ] Limitations documented |

---

## 8. Output Quality Validation

### 8.1 Deliverables Checklist
**Ensure implementation produces:**
- [ ] **Analysis artifacts**: Cleaned datasets, intermediate results
- [ ] **Visualizations**: Publication-quality charts, interactive dashboards
- [ ] **Statistical outputs**: Test results, model performance metrics
- [ ] **Documentation**: Analysis report, methodology description
- [ ] **Code**: Reproducible scripts/notebooks with documentation
- [ ] **Recommendations**: Actionable insights for stakeholders

### 8.2 Stakeholder Alignment
**Check outputs match user needs:**
- [ ] Technical detail appropriate for audience (epidemiologist vs executive)
- [ ] Visualizations are interpretable by non-technical users
- [ ] Recommendations are actionable (not just observations)
- [ ] Limitations and caveats are clearly stated

---

## 9. Risk & Feasibility Assessment

### 9.1 Technical Feasibility & Escalation Criteria

**When to ITERATE vs. ESCALATE/REJECT:**

**✅ ITERATE (Fix Within Implementation Plan):**
Minor to moderate issues that can be resolved through code/approach changes:
- ✓ Wrong visualization types → Replace with appropriate charts
- ✓ Missing error handling → Add try-except blocks and validation
- ✓ Incomplete EDA steps → Add missing analysis tasks
- ✓ Suboptimal methods → Replace with better statistical approaches
- ✓ Missing documentation → Add docstrings and comments
- ✓ Security gaps → Add credential management and input validation
- ✓ Performance issues → Optimize with vectorization, chunking

**🚫 ESCALATE/REJECT (Fundamental Flaws - Cannot Proceed):**
Critical blockers requiring data acquisition, scope change, or redesign:
- ❌ **Data doesn't exist**: Required data not available in documented sources
- ❌ **Wrong granularity**: Needs daily data but only monthly available (cannot disaggregate)
- ❌ **Infrastructure mismatch**: Real-time analysis required but data is batch-only
- ❌ **Insufficient volume**: Advanced ML requires 10,000+ samples but only 100 available
- ❌ **Invalid causal claims**: Claiming causation without experimental/quasi-experimental design
- ❌ **Privacy violations**: Analysis requires PII but data is anonymized/aggregated
- ❌ **Missing dimensions**: Geographic analysis but no location data available
- ❌ **Temporal misalignment**: Needs historical trend (5+ years) but only 6 months available

**Escalation Actions:**

When fundamental flaws detected:

1. **FLAG AS BLOCKED** - Mark implementation plan with:
   ```markdown
   🚫 **IMPLEMENTATION BLOCKED - FUNDAMENTAL FEASIBILITY ISSUE**
   
   **Issue**: [Specific blocker, e.g., "Required daily case data not available - only monthly aggregates exist"]
   
   **Impact**: [How this prevents user story completion]
   
   **Recommendation**: [Choose appropriate path below]
   ```

2. **RECOMMEND RESOLUTION PATH:**

   **Path A: Scope Reduction**
   - Modify user story to match available data
   - Adjust acceptance criteria to feasible level
   - Example: "Monthly trend analysis" instead of "daily forecasting"
   
   **Path B: Alternative Approach**
   - Propose different analysis method that works with available data
   - Example: Use proxy variables, aggregate to appropriate level
   - Document limitations clearly
   
   **Path C: Reject User Story**
   - If no viable path forward with current resources
   - Recommend deferring until data/infrastructure available

3. **DOCUMENT DECISION** - Add to implementation plan:
   ```markdown
   ## Feasibility Assessment
   
   **Status**: 🚫 Blocked
   **Blocker**: [Specific issue]
   **Recommended Path**: [A/B/C with details]
   **Next Steps**: [What needs to happen before implementation can proceed]
   **Stakeholder Notification**: Required - expectations must be reset
   ```

**Red flags for infeasibility (check against project constraints):**
- ❌ Requires data not available in documented sources
- ❌ Needs infrastructure not available (real-time when data is batch, etc.)
- ❌ Advanced ML without sufficient data volume or quality
- ❌ Causal inference without appropriate experimental/quasi-experimental design
- ❌ Analysis requiring granularity not available in data
- ❌ Privacy-violating analysis with anonymized/aggregated data
- ❌ Geographic/spatial analysis without location data

### 9.3 Dependency Risks
**Potential blockers:**
- [ ] External data sources availability confirmed (APIs, third-party data)
- [ ] Cross-user-story dependencies identified and sequenced
- [ ] Shared code/data dependencies managed
- [ ] Compute/infrastructure resources available when needed
- [ ] Team member availability and expertise aligned with tasks

---

## Action Required

**⚠️ REMINDER: Code execution validation (Section 5.5) is MANDATORY before proceeding to any execution phase. All code must be tested and verified executable.**

For each user story implementation plan:

### 1. Critical Assessment
First, briefly reflect (in 2-3 sentences):
- Is this the optimal approach given constraints?
- What are the critical gaps or issues?
- Does it need minor tweaks or major restructuring?
- **Can all proposed code blocks be executed without errors?**

### 2. Update the Implementation Plan
**Directly edit the implementation plan file** to:

✅ **Fix Critical Issues:**
- Align data extraction with documented data sources
- Correct visualization types to match data structure
- Add missing error handling and validation
- Include security/privacy measures (credential management, PII handling)
- Specify concrete statistical methods with parameters

✅ **Enhance Quality:**
- Add Python best practices (type hints, docstrings, logging)
- Include unit tests for critical functions
- Add data validation steps
- Improve code modularity and reusability
- Add performance optimizations where needed

✅ **Ensure Completeness:**
- Verify all 9 pipeline stages are covered:
  1. Data Extraction
  2. Data Validation
  3. Data Preprocessing
  4. Exploratory Data Analysis
  5. Statistical Analysis
  6. Visualization
  7. Interpretation & Reporting
  8. Code Documentation
  9. Code Quality & Testing
- Map every acceptance criterion to specific tasks
- Add edge case handling
- **⚠️ CRITICAL: Validate ALL code blocks execute without errors (Section 5.5)**

### 3. Structure Your Updates
When updating the implementation plan, organize tasks clearly:

```markdown
## Implementation Tasks

### Phase 1: Data Acquisition & Validation
- [ ] Extract data from [specific source] using [method]
- [ ] Validate schema matches expected structure (check columns: X, Y, Z)
- [ ] Check data quality (completeness, ranges, duplicates)
- [ ] Log extraction metrics and any issues

### Phase 2: Data Processing & Feature Engineering
- [ ] Clean and transform data (handle missing values, convert types)
- [ ] Engineer features: [list specific features]
- [ ] Validate transformations with unit tests

### Phase 3: Exploratory Data Analysis
- [ ] Generate descriptive statistics for [specific variables]
- [ ] Create visualizations: [specific chart types for specific purposes]
- [ ] Identify patterns, outliers, and anomalies

### Phase 4: Statistical Analysis & Modeling
- [ ] Apply [specific method] with parameters: [specify]
- [ ] Validate results using [specific approach]
- [ ] Compare against baseline

### Phase 5: Visualization & Reporting
- [ ] Create dashboard with [specific components]
- [ ] Document findings and limitations
- [ ] Provide actionable recommendations

### Phase 6: Code Quality & Documentation
- [ ] Add comprehensive docstrings (Google/NumPy style)
- [ ] Include type hints for all functions
- [ ] Write unit tests for [specific functions]
- [ ] Add logging at INFO, WARNING, ERROR levels
- [ ] Create README with setup and usage instructions
```

### 4. Code Execution Validation (MANDATORY)
**Before approving the implementation plan:**
- [ ] Extract all code blocks from the implementation plan
- [ ] Test EVERY code block using `mcp_pylance_mcp_s_pylanceRunCodeSnippet` tool or terminal
- [ ] Fix ALL errors (syntax, import, runtime, logic)
- [ ] Re-test until 100% of code executes successfully
- [ ] Add validation stamp to implementation plan
- [ ] Document any code changes made during validation

**Only after validation passes → Proceed to next step**

### 5. Brief Change Summary
After updating, provide a concise summary (3-5 bullet points) of key improvements made:
- What critical issues were fixed
- What enhancements were added
- Why these changes improve the implementation
- **Confirmation that all code has been validated and executes without errors**

---

## Validation Checklist Summary

Run through this quick checklist for each implementation plan:

```
⚠️ CODE EXECUTION VALIDATION (MANDATORY - SECTION 5.5)
[ ] ALL imports tested and verified available
[ ] ALL file paths validated and exist
[ ] ALL code blocks executed successfully (0 errors)
[ ] ALL outputs verified (expected results produced)
[ ] Integration test passed (end-to-end execution)
[ ] Validation stamp added to implementation plan
🚫 BLOCKING: Cannot proceed without 100% pass rate

DATA SOURCE ALIGNMENT
[ ] Extraction method matches documented data source
[ ] All referenced datasets/tables/files exist
[ ] Time span requirements match available data
[ ] Data granularity acknowledged and appropriate

EDA APPROPRIATENESS
[ ] Visualizations match data type (time → line charts)
[ ] Statistical methods suit data structure
[ ] EDA steps are comprehensive (shape, stats, distributions)

IMPLEMENTATION COMPLETENESS
[ ] All 9 pipeline stages have tasks (extraction → testing)
[ ] Every acceptance criterion has implementing tasks
[ ] Dependencies (packages, internal modules) are realistic
[ ] Edge cases and limitations handled
[ ] Error handling and logging included

PYTHON CODE QUALITY
[ ] Functions are modular and well-documented
[ ] Type hints used appropriately
[ ] Error handling with specific exceptions
[ ] Performance considerations addressed
[ ] Unit tests for critical functionality

SECURITY & PRIVACY
[ ] No hardcoded credentials
[ ] PII/PHI handling compliant
[ ] Input validation present
[ ] Secure credential management

TECHNICAL FEASIBILITY
[ ] No unavailable data sources required
[ ] Infrastructure assumptions match reality
[ ] Methods match available data size and quality
[ ] Outputs are well-defined and measurable

DOCUMENTATION & QUALITY
[ ] Limitations explicitly documented
[ ] Code reproducibility considered
[ ] Stakeholder outputs specified
```

---

## Examples of Good vs Bad Implementation Elements

### ❌ BAD: Data Extraction
```
- □ Extract data from undocumented database
- □ Connect to API without authentication plan
- □ Download files from unspecified source
```
**Issues:** Doesn't match documented data source; no authentication; vague source.

### ✓ GOOD: Data Extraction
```
- □ Extract data using [documented method, e.g., API endpoint, Kaggle, S3 bucket]
- □ Configure authentication per documentation (API key, OAuth, credentials)
- □ Load data into [workspace format] (DataFrame, database table, parquet files)
- □ Validate schema matches expected structure (fields, types, constraints)
```

---

### ❌ BAD: Visualization
```
- □ Create pie chart showing temporal trends over multiple years
- □ Make bar chart with 15+ time points
- □ Use geographic map without location data
```
**Issues:** Pie charts wrong for time series; bar charts poor for many time points; maps without coordinates.

### ✓ GOOD: Visualization
```
- □ Create line chart showing trends over time (for time series data)
- □ Generate heatmap for 2D patterns (time × category, location × metric)
- □ Build interactive dashboard for exploring patterns (Plotly, Dash, etc.)
- □ Use appropriate chart types matched to data structure
```

---

### ❌ BAD: Analysis Method
```
- □ Apply real-time algorithms to batch data
- □ Analyze hourly patterns with annual data
- □ Build deep learning model with 50 data points
```
**Issues:** Method doesn't match data characteristics; insufficient data for approach.

### ✓ GOOD: Analysis Method
```
- □ Apply appropriate statistical method for data structure
- □ Match temporal analysis to data granularity (annual → long-term trends)
- □ Use methods suitable for sample size (simple stats for small n)
- □ Include validation against known patterns or holdout data
```

---

### ❌ BAD: Dependency
```
- Internal: `src.nonexistent.module`
- External: `proprietary_lib`, `unavailable_api`
```
**Issues:** These modules don't exist in project or aren't accessible.

### ✓ GOOD: Dependency
```
- External: Standard open-source libraries (polars, scikit-learn, plotly, etc.)
- Internal: Documented project modules that exist (src.data_processing.connector, src.utils.logger)
```

---

### ❌ BAD: Python Code Quality
```python
# No type hints, no docstring, bare except
def process(data):
    try:
        result = data.apply(lambda x: x * 2)  # What is this doing?
        return result
    except:
        return None
```
**Issues:** No documentation, no type hints, bare except hides errors, unclear logic.

### ✓ GOOD: Python Code Quality
```python
import polars as pl
import logging

logger = logging.getLogger(__name__)

def calculate_disease_rate(
    case_data: pl.DataFrame,
    population: int,
    multiplier: int = 100000
) -> pl.DataFrame:
    """
    Calculate disease incidence rate per population.
    
    Args:
        case_data: DataFrame with 'cases' column
        population: Total population size
        multiplier: Rate per N people (default 100,000)
    
    Returns:
        DataFrame with added 'rate' column
    
    Raises:
        ValueError: If population is zero or negative
        KeyError: If 'cases' column missing
    
    Example:
        >>> df = pl.DataFrame({'cases': [100, 200]})
        >>> calculate_disease_rate(df, 1000000)
    """
    if population <= 0:
        raise ValueError(f"Population must be positive, got {population}")
    
    if 'cases' not in case_data.columns:
        raise KeyError("Input DataFrame must contain 'cases' column")
    
    try:
        case_data = case_data.with_columns(
            ((pl.col('cases') / population) * multiplier).alias('rate')
        )
        logger.info(f"Calculated rates for {len(case_data)} records")
        return case_data
    except Exception as e:
        logger.error(f"Failed to calculate rates: {e}")
        raise
```
**Good practices:** Type hints, comprehensive docstring, input validation, specific exceptions, logging.

---

### ❌ BAD: Security
```python
API_KEY = "sk-1234567890abcdef"  # Hardcoded!
db_password = "admin123"  # Committed to git!

query = f"SELECT * FROM patients WHERE id = {user_input}"  # SQL injection!
```
**Issues:** Hardcoded credentials, SQL injection vulnerability, exposed in version control.

### ✓ GOOD: Security
```python
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load from environment variables
load_dotenv()
API_KEY = os.getenv('MOH_API_KEY')
if not API_KEY:
    raise ValueError("MOH_API_KEY environment variable not set")

# Use parameterized queries
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    # Parameterized query prevents SQL injection
    query = text("SELECT * FROM patients WHERE id = :patient_id")
    result = conn.execute(query, {"patient_id": user_input})
```
**Good practices:** Environment variables, credentials never hardcoded, parameterized queries, validation.

---

## Final Instruction

**Take action immediately**: Review each user story implementation plan systematically using this checklist. **Don't just identify issues—fix them directly** by updating the implementation plan. Reflect deeply on the optimal approach, then make the necessary changes.

**Update the files** to ensure:
- ✅ Data extraction aligns with documented sources
- ✅ Methods are appropriate for data structure and analysis goals  
- ✅ Python best practices are followed (type hints, error handling, logging, tests)
- ✅ Security/privacy measures are in place
- ✅ All pipeline stages are complete and detailed
- ✅ Tasks are specific, actionable, and measurable

**Your updates should transform the implementation plan into a production-ready, comprehensive guide** that a developer can follow step-by-step to successfully complete the user story. If the plan is already optimal, simply proceed to the next user story.

Prioritize **data availability**, **method appropriateness**, **Python best practices**, **security/privacy**, and **end-to-end completeness**.
