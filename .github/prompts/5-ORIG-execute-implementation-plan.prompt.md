---
description: Prompt for Execution of the Implementation Plan
stage: Development
---
# AI Agent Prompt: Execute Implementation Plan

## Role

Execute a detailed implementation plan accurately and verify its completion according to specifications for an end-to-end data analysis project.

## Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Problem Statement (PS)** | Top-level analysis objective | problem-statement-001-Workforce Capacity Mismatch |
| **User Story (US)** | Deliverable subset of a problem statement | 001-{user-story-name} within problem-statement-001-Workforce Capacity Mismatch |
| **Subagent** | Specialist AI agent invoked via `#runSubagent` | ExtractionAgent, Code Reviewer Agent |
| **Handoff File** | JSON file agents use to pass validated outputs | `extraction_to_profiling_20260306.json` |
---

## 🚨 CRITICAL RULES - READ FIRST

### Directory Structure (MANDATORY)

**✅ CORRECT - All artifacts in ONE problem-statement directory:**
```
problem-statements/ps-{num}-{descriptive-name}/
├── notebooks/              # ALL notebooks for this PS
├── src/                    # Problem-specific code
│   ├── data_processing/    # ETL and cleaning code
│   ├── analysis/           # Analysis modules
│   └── scripts/            # Executable scripts
├── data/                   # Problem-specific data
│   ├── 3_interim/          # Intermediate data
│   └── 4_processed/        # Final processed data
├── results/                # Analysis results
│   ├── tables/
│   └── metrics/
├── reports/                # Reports and figures
│   └── figures/
├── models/                 # Trained models
├── config/                 # Problem-specific config
├── tests/                  # Integration tests
├── logs/                   # Execution logs
└── README.md              # Execution instructions
```

## 1. MCP Tools Quick Reference

### Filesystem Tools (REQUIRED)
Use for ALL file operations:

```
Read data:     "Use filesystem tools to read ../shared/data/1_raw/input.csv"
Create dir:    "Use filesystem tools to create directory ../problem-statements/ps-001-{name}/results/"
Write file:    "Use filesystem tools to save results to ../problem-statements/ps-001-{name}/results/tables/output.csv"
List files:    "Use filesystem tools to list files in ../problem-statements/ps-001-{name}/"
```

### SQLite Tools (when applicable)
Use for database operations:

```
Query:         "Query using SQLite tools: SELECT * FROM patients WHERE year >= 2020"
Create table:  "Use SQLite tools to create summary table"
```

### Context7 MCP (REQUIRED for Library/Framework Usage)
Use for fetching **current documentation** instead of relying on training data:

**🚨 CRITICAL RULE**: When implementing code that uses libraries, frameworks, or APIs, you MUST use Context7 to fetch current documentation. This ensures API accuracy, correct syntax, and version compatibility.

**WHEN TO USE Context7 (MANDATORY):**

| Scenario | Action | Example |
|----------|--------|----------|
| **Writing data processing code** | Fetch Polars/pandas docs | `resolve-library-id` → "polars" → `query-docs` "lazy evaluation scan_csv" |
| **Implementing forecasting models** | Fetch statsmodels/prophet docs | `resolve-library-id` → "statsmodels" → `query-docs` "ARIMA model fit predict" |
| **Building dashboards** | Fetch Plotly Dash docs | `resolve-library-id` → "plotly" → `query-docs` "Dash app layout callbacks" |
| **Using ML libraries** | Fetch scikit-learn docs | `resolve-library-id` → "scikit-learn" → `query-docs` "train_test_split cross validation" |
| **Databricks integration** | Fetch Databricks docs | `resolve-library-id` → "databricks" → `query-docs` "scheduled jobs DBFS" |
| **API integrations** | Fetch API docs | `resolve-library-id` → "requests" → `query-docs` "session retry timeout" |

**WHEN NOT TO USE Context7:**
- Writing specifications/documentation (no code implementation)
- High-level architecture planning
- Business logic that doesn't depend on external libraries
- Simple Python standard library usage (pathlib, datetime, logging)

**Context7 Workflow:**

```bash
# Step 1: Identify the library/framework
Library: "polars" (for data processing)

# Step 2: Resolve library ID
resolve-library-id({library: "polars", question: "How to use lazy evaluation with scan_csv?"})
# Returns: [{id: "polars", name: "Polars", version: "0.20.0"}]

# Step 3: Query specific documentation
query-docs({libraryId: "polars", question: "scan_csv lazy evaluation collect filter"})
# Returns: Current API syntax, examples, best practices

# Step 4: Implement using fetched documentation
# Use exact syntax from docs (not training data)
```

**Verification After Context7 Usage:**
- ✅ API method signatures match current documentation
- ✅ Parameter names and types are accurate
- ✅ Deprecated methods avoided
- ✅ Best practices from docs followed
- ✅ Version-specific features used correctly

**🚨 CRITICAL: Jupyter Notebook Requirement**

Every user story implementation MUST include at least one Jupyter notebook:
- ✅ ONE notebook minimum per user story (can have multiple if needed)
- ✅ Named following convention: `{user-story-num}_{descriptive_name}.ipynb`
- ✅ Located in `problem-statement/ps-{num}-{name}/notebooks/`
- ✅ Executes from start to finish with ZERO errors
- ✅ Generates all expected outputs (visualizations, tables, results)
- ✅ Includes markdown cells documenting each step
- ✅ Documents prerequisite scripts/data requirements in first markdown cell
- ✅ **ALL prerequisite scripts executed and data dependencies verified to exist BEFORE marking work complete**

### 2. Continuous Code Quality Analysis (MANDATORY)

**🚨 CRITICAL REQUIREMENT**: You MUST execute Code Review Agent and Jupyter Notebook Execution Agent before this task can be marked as complete. Quality checks are NOT optional and NOT end-of-implementation tasks. Failure to execute these mandatory subagents means the implementation is INCOMPLETE.

**MANDATORY SUBAGENTS (NON-NEGOTIABLE):**
1. **Code Review Agent** - Execute during implementation (after 2-3 modules) and before marking complete
2. **Jupyter Notebook Execution Agent** - Execute after creating/updating notebooks and before marking complete

**EXECUTION WORKFLOW (MANDATORY):**

```
For EACH implementation stage:
1. Implement the code/module 
→ 2. IMMEDIATELY delegate quality review (Code Review Agent) and jupyter notebook execution (Jupyter Notebook Execution Agent) 
→ 3. Fix issues found 
→ 4. Proceed to next stage
```

**WHEN TO EXECUTE SUBAGENTS (NON-NEGOTIABLE):**

| Implementation Stage | Subagent to Execute | Timing |
|---------------------|---------------------|--------|
| **BEFORE writing any code** | Directory Structure Validation | PREVENT duplicate directories, files and import path chaos |
| **After creating each module** | Code Reviewer Agent Code Review | Review error handling, types, security |
| **After completing 2-3 modules** | Dead Code Elimination | Clean up unused code before it accumulates |
| **After completing 2-3 modules** | Import Path Validation | Verify all imports match actual directory structure |
| **After creating/updating notebooks** | **Jupyter Notebook Execution Agent (MANDATORY)** | Execute ALL notebooks, verify zero errors, fix issues |
| **Before marking work complete** | **Jupyter Notebook Execution Agent (MANDATORY)** | Final notebook validation - ALL notebooks must execute successfully |
| **Before marking work complete** | **Code Reviewer Agent Comprehensive Review (MANDATORY)** | Final validation of all code quality standards |
| **Multi-Agent Orchestration for Data Analysis Lifecycle** | Specialized agent (refer to section 7) | During Implementation of multiple user stories in parallel, execute coordination subagent to manage handoffs and integration |

**MANDATORY SUBAGENT EXECUTIONS:**

Execute these subagents during implementation. Each subagent call is REQUIRED:

**🚨 CRITICAL: Code Review Agent and Jupyter Notebook Execution Agent are NON-NEGOTIABLE**
- These agents MUST be executed before marking any implementation as complete
- Failure to execute = Implementation is INCOMPLETE
- ALL notebooks MUST execute with ZERO errors before completion

---

**🧠 CRITICAL: Import Path Memory - Prevent Import Errors**

**Import Rules (MEMORIZE):**
1. **Problem-statement code imports**: `from src.{module}.{file} import {function}`
2. **Shared code imports**: `from shared.src.{module}.{file} import {function}`
3. **Notebooks**: Same import paths as scripts (must locate and add correct paths to sys.path)

**Execution Context (WHERE code runs from):**
- ✅ **Scripts**: ALWAYS run from workspace root: `python problem-statement/ps-001-workforce/src/scripts/run.py`
- ✅ **File paths in code**: Use workspace-relative paths: `/data/1_raw/input.csv`
- ❌ **Never**: `cd` into problem-statement directory before running (breaks imports)

**Before writing ANY import statement**: Verify target file exists at expected path, use hyphens in directories NOT underscores, imports use dots (.) to separate modules.

---

**a. Directory Structure Validation Agent (REQUIRED - Execute FIRST, BEFORE any code creation):**
```javascript
#runSubagent({
  description: "Validate directory structure for Problem Statement {num}",
  prompt: `CRITICAL: Validate directory structure and prevent duplicate directories BEFORE creating any files.

Problem Statement Number: {num}
Expected Directory: problem-statement/ps-{num}-{descriptive-name}/

Tasks:
1. **Check for Duplicate Directories**:
   - Search for ANY existing directories matching pattern: problem-statement/ps-*{num}*
   - List ALL matches with exact paths
   - Flag if MULTIPLE directories exist for same problem statement
   - Example duplicates to detect:
     * problem-statement/ps-003-public-health/ AND src/problem_statement_003_public_health/
     * problem-statement/ps-002/ AND problem-statement/ps-002-disease-burden/

2. **Validate Naming Convention**:
   - Verify directory name follows format: problem-statement-{num}-{descriptive-name}
   - Use HYPHENS not underscores
   - Examples:
     ✅ problem-statement/ps-001-workforce-capacity/
     ✅(underscores)
     ❌ problem-statement/ps-001/ (abbreviated)

3. **Decision Logic**:
   - If NO directory exists → Proceed with creation using correct naming
   - If ONE directory exists with CORRECT naming → Use existing directory
   - If ONE directory exists with WRONG naming → Report violation, suggest rename
   - If MULTIPLE directories exist → CRITICAL ERROR - Report all paths, recommend consolidation

Return:
- Status: "SAFE_TO_PROCEED" | "RENAME_REQUIRED" | "DUPLICATE_DETECTED" | "CONSOLIDATION_REQUIRED"
- Existing_Directories: [list of all matching directories]
- Recommended_Action: Specific steps to resolve issue
- Target_Directory: The single directory path to use`
})
```

**b. Import Path Validation Agent (REQUIRED - Execute AFTER creating files, BEFORE marking complete):**
```javascript
#runSubagent({
  description: "Validate import paths match directory structure",
  prompt: `CRITICAL: Verify all import statements match actual directory structure.

Problem Statement Directory: problem-statement/ps-{num}-{descriptive-name}/

Tasks:
1. **Validate Import Paths Against Actual Filesystem**: For each import, resolve the path relative to the importing file's location, verify the module EXISTS on filesystem, check naming consistency (hyphens vs underscores), and flag mismatches

2. **Validate Relative Imports Don't Cross Boundaries**: Files should import from their own problem-statement directory; flag if ps-001 imports from ps-002 (should use shared/src/ for shared code)

Return:
- Import_Validation_Status: "ALL_VALID" | "MISMATCHES_FOUND"
- Resolve all mismatched imports`
})
```

**c. Jupyter Notebook Execution Agent (REQUIRED - Execute AFTER creating/updating notebooks):**
```javascript
#runSubagent({
  description: "Execute all Jupyter notebooks and fix errors for Problem Statement {num}",
  prompt: `Read and execute the Jupyter Notebook Execution protocol from .github/prompts/6-test-execuetion-code.prompt.md

Context:
- Problem Statement: {num}
- Target Directory: problem-statement/ps-{num}-{descriptive-name}/
- Notebooks Location: problem-statement/ps-{num}-{descriptive-name}/notebooks/
- **MISSION**: Zero cell execution errors across all notebooks

🚨 CRITICAL: NEVER DELETE NOTEBOOK FILES
- DO NOT use rm, delete, or remove commands on .ipynb files
- FIX errors in-place by editing cells
- If notebook has duplicate cells, DELETE cells (not the file)
- If notebook has import errors, FIX imports (not delete the file)
- Only escalate if error genuinely cannot be fixed after multiple attempts

Instructions:
1. Read the complete testing protocol from .github/prompts/6-test-execuetion-code.prompt.md
2. Follow ALL phases in the "Testing Protocol" section:
   - Phase 1: Discovery (find all notebooks)
   - Phase 2: Pre-Execution Validation (imports, dependencies, environment)
   - Phase 3: Execution (jupyter nbconvert --execute)
   - Phase 4: Error Handling (diagnose and fix ALL errors)
   - Phase 5: Output Verification (cells, files, visualizations)
   - Phase 6: Documentation Updates (prerequisites, error prevention)
3. Apply the "Error Resolution & Code Adjustments" protocol for ALL errors encountered
4. Iterate until ZERO errors across all notebooks
5. Generate comprehensive report as specified in the prompt

**CRITICAL REQUIREMENTS:**
- ✅ ALL notebooks must execute from start to finish with ZERO errors
- ✅ ALL cells must have outputs (no empty execution_count)
- ✅ ALL expected files must be generated and validated
- ✅ Import cells positioned correctly (first executable cell)
- ✅ Prerequisites documented in markdown cells
- ✅ Error prevention checks added to notebooks
- ✅ **NO literal escape sequences** (`\n`, `\t`) in markdown cells (use actual line breaks instead)
- ✅ Verify notebook renders correctly when reopened in VS Code

**FAILURE CONDITION:**
If ANY notebook cannot be fixed to execute successfully:
1. Report persistent error in detail
2. Mark status as "EXECUTION_FAILED"
3. Block further implementation
4. Escalate to primary agent

Reference: See .github/prompts/6-test-execuetion-code.prompt.md for complete testing protocol and error resolution strategies.`
})
```

**d. Code Review Agent (REQUIRED):**
```javascript
#runSubagent({
  description: "Comprehensive code review for Problem Statement {num}",
  prompt: `Execute a comprehensive code quality review and fix ALL identified issues.

Context:
- Target Directory: problem-statement/ps-{num}-{descriptive-name}/
- Review ALL Python files (.py) AND ALL Jupyter notebooks (.ipynb)
- Fix issues immediately - do not just report them
- **CRITICAL**: Any errors detected during code execution MUST BE FIXED before proceeding

**Tasks:**
**🔴 CRITICAL EXECUTION REQUIREMENT - HIGHEST PRIORITY:**
Before ANY other review tasks, you MUST execute ALL code to verify zero errors:

1. **Run ALL Python Scripts (MANDATORY):**
   - List ALL .py files in the problem-statement directory (src/scripts/, src/data_processing/, src/analysis/, etc.)
   - Determine correct execution order based on dependencies
   - Execute EVERY .py file one by one
   - Check exit code for each script (must be 0)
   - Verify zero ImportError, TypeError, AttributeError, FileNotFoundError, KeyError, ValueError
   - **STOP IMMEDIATELY if any script fails** - do not proceed to next script
   - Fix ALL errors immediately before proceeding
   - Re-run failed script to confirm fix
   - Document execution results: script path, exit code, execution time, outputs generated

2. **Execute ALL Jupyter Notebooks (MANDATORY):**
   - List ALL .ipynb files in problem-statement/ps-{num}-{descriptive-name}/notebooks/
   - For EACH notebook:
     * Check that all prerequisite scripts have been run (data files exist)
     * Execute notebook
     * Verify exit code is 0
     * Check that ALL cells executed successfully (no exception outputs)
     * Verify all expected outputs are generated (figures, CSV files, etc.)
   - **STOP IMMEDIATELY if any notebook cell fails**
   - Fix ALL errors (missing imports, file paths, data issues)
   - Re-run notebook to confirm fix
   - Document execution results: notebook path, cell count, execution time, outputs generated

3. **Context7 Documentation Validation (MANDATORY - NEW):**
   - For EVERY library/framework import, verify against current documentation using Context7
   - Use `resolve-library-id` + `query-docs` to fetch current API syntax
   - Check for:
     * Deprecated methods (replace with current alternatives)
     * Incorrect parameter names/types (fix to match current docs)
     * Missing required parameters (add with correct defaults)
     * Version-incompatible features (update or remove)
   - Document which libraries were validated and any fixes applied
   - **DO NOT SKIP**: This prevents runtime errors from outdated API usage

4. **Verify All Outputs Created (MANDATORY):**
   - Check that all expected output files exist (from both scripts AND notebooks)
   - Verify file contents are valid (not empty, correct format, correct schema)
   - Verify file sizes are reasonable (not 0 bytes, not suspiciously small)
   - Open CSV/JSON files and inspect first few rows/records
   - Fix missing outputs immediately
   - Re-run code if outputs are missing or invalid

**IF ANY ERRORS FOUND: STOP - FIX - RE-RUN - VERIFY ZERO ERRORS**
**DO NOT PROCEED TO REMAINING TASKS UNTIL ALL CODE EXECUTES SUCCESSFULLY**

**After execution verification passes (ALL code runs with zero errors), proceed with additional tasks:**

5. **Verify Dynamic Data Structure Analysis Was Followed (MANDATORY):**
   - **PURPOSE**: Confirm the agent analyzed data structures DURING coding (see §6 Dynamic Data Structure Analysis)
   - For EVERY data file used in the codebase:
     * Verify code includes structure analysis (print columns/schema) BEFORE accessing columns
     * Check for comments documenting actual structure discovered
     * Verify column names in code match actual data (not assumed from plans)
     * Look for explicit rename operations if expected names differ from actual
   - Flag violations:
     * Code accesses columns without prior analysis
     * Column names assumed without verification
     * Missing structure documentation comments
   - **Evidence required**: Analysis output visible in code/notebooks showing actual columns discovered

6. **Code Formatting (Python Files AND Notebooks - MANDATORY):**
   - Format Python files: `ruff format problem-statement/ps-{num}-{descriptive-name}/ --check`
   - **Format Jupyter notebooks**: `ruff format problem-statement/ps-{num}-{descriptive-name}/**/*.ipynb --check`
   - Auto-format both file types if needed
   - **DO NOT SKIP notebook formatting**

6. **Parallel Code Review Perspectives:** Run these subagents in parallel:
   - **Data structure validator (CRITICAL)**: Execute all data loading code, inspect actual columns/keys/dtypes, verify every subsequent reference matches reality exactly (case-sensitive). Flag any KeyError, ColumnNotFoundError, or assumptions about data structure
   - Correctness reviewer: logic errors, edge cases, type issues
   - Code quality reviewer: readability, naming, duplication
   - Security reviewer: input validation, injection risks, data exposure
   - Architecture reviewer: codebase patterns, design consistency, structural alignment
   - Notebook documentation reviewer: Template variables replaced, markdown cells accurate, prerequisites clear
`
})
```

**MANDATORY ACTION AFTER EACH SUBAGENT REPORT:**

You MUST take these actions immediately after receiving subagent findings:

1. **REVIEW findings** - Read the complete subagent report
2. **TRIAGE issues** - Categorize by severity (critical → high → medium → low)
3. **FIX CRITICAL/HIGH immediately** - Do not proceed until security issues, data loss risks, and high-priority bugs are fixed
4. **REFACTOR duplicates** - If 3+ occurrences of duplicate code found, extract to shared function/module
5. **UPDATE code** - Apply all recommendations from subagent before next implementation stage
6. **DOCUMENT deferred items** - Add any medium/low priority improvements to TODO.md with issue IDs
7. **VERIFY fixes** - Re-run subagent if critical issues were found to confirm resolution

**VERIFICATION REQUIREMENT:**

Before marking implementation complete, you MUST document:
- ✅ List of all subagent executions with timestamps
- ✅ Jupyter Notebook Execution Agent report (all notebooks passing with zero errors)
- ✅ **All prerequisite scripts executed and data dependencies verified to exist**
- ✅ Summary of findings from each subagent report
- ✅ Actions taken to address critical/high priority issues
- ✅ Confirmation that all security vulnerabilities are fixed
- ✅ Refactoring completed for duplicate code (3+ occurrences)
- ✅ Final quality scores from comprehensive review
- ✅ Any deferred improvements documented in TODO.md

### 3. Naming Convention (MANDATORY)

**Format**: `problem-statement/ps-{num}-{descriptive-name}/`
- `{num}`: Zero-padded problem statement number (e.g., `001`, `002`)
- `{descriptive-name}`: Kebab-case description (e.g., `workforce-capacity-mismatch`)

**✅ Examples:**
- `problem-statement/ps-001-workforce-capacity-mismatch/`
- `problem-statement/ps-002-seasonal-disease-forecasting/`

### 4. Organization Rules

1. **One Problem Statement = One Directory**: All user stories for the same problem statement share ONE directory
2. **No Shared Notebooks Directory**: Do NOT create notebooks in `notebooks/1_exploratory/`, `notebooks/2_analysis/`, etc.
3. **Problem-Statement Outputs**: Save outputs within problem statement directory: `problem-statement/ps-{num}-{name}/reports/figures/`, `problem-statement/ps-{num}-{name}/results/tables/`

## Input Requirements

The input will consist of:
- A detailed implementation plan for the associated user story (typically in Markdown format)
- **Prerequisite Completion Documents**: ALL dependent user story completion documents (`problem-statement/ps-{num}-{descriptive-name}/US-XX-IMPLEMENTATION-COMPLETE.md`) to verify what was ACTUALLY implemented (data schemas, column names, file paths, data types) and adapt your implementation to match reality instead of making assumptions
- User story/stories and acceptance criteria
  - **Single User Story**: Implementation plan for one deliverable
  - **Multiple User Stories**: Implementation plans for multiple deliverables (may require parallel execution and coordination)
- Design specifications and requirements
- **For Parallel Execution**: Agent assignment strategy and coordination requirements

## 🚨 MANDATORY PRE-IMPLEMENTATION CHECK: Orchestration Strategy Selection

**BEFORE writing ANY code, you MUST:**

1. **Count User Stories**: Analyze the input to determine how many user stories need implementation
2. **Determine Orchestration Strategy**: Follow Section 7.1 Decision Framework
3. **Execute Strategy**: Invoke specialist agents OR implement directly based on decision

**Decision Logic (MANDATORY):**

```
IF number_of_user_stories >= 2:
    THEN use Multi-Agent Orchestration (Section 7)
    ACTION: Invoke specialist agents (ModelingAgent, ValidationAgent, etc.)
    DO NOT: Implement directly yourself
    
ELSE:
    THEN use Sequential Multi-Stage Orchestration (Section 7.2)
    ACTION: Chain specialist agents with handoffs
```

## Output Requirements

The output MUST include:
- **Problem-Statement-Specific Directory Structure**: Created per CRITICAL RULES above
- Implementation of all required files and changes
- Verification that specifications have been met
- Completed Design Implementation Verification Checklist
- **For Parallel Execution (Multiple User Stories)**:
  - Agent handoff files showing coordination and code sharing
  - Consolidation report identifying shared utilities extracted
  - Multi-user-story quality review results (see §7.3)
  - Cross-user-story integration test results

## Review Requirements

Before implementation, the implementation plan MUST be reviewed for:
- Clarity and completeness of all steps
- Availability of all necessary information
- Alignment with project guidelines and technical stack
- Completeness of design specifications (colors, spacing, typography)

If any part of the plan is unclear or missing information, clarification MUST be requested before proceeding.

## 5. Search for Existing Implementations

**MANDATORY STEP**: Before creating new features, search for similar implementations.

### a. Search Process

```javascript
// Check for existing dashboards
grep_search("dashboard", isRegexp=false, includePattern="dashboards/**")

// Check for similar analysis modules (search in both shared and problem-specific)
grep_search("forecasting|prediction", isRegexp=true, includePattern="{shared/src,problem-statement/ps-*}/**/analysis/**")

// Check for data processing patterns
semantic_search("data cleaning workflow for disease surveillance")
```

### b. Relevance Assessment

Ask these questions to determine if feature should extend existing implementation:

| Question | EXTEND if... | CREATE NEW if... |
|----------|-------------|-----------------|
| **Same domain?** | Same disease types, same health outcomes | Different health domains (workforce vs disease) |
| **Same audience?** | Same stakeholders/decision-makers | Different user groups (clinicians vs policymakers) |
| **Same workflow?** | Same analytical pipeline stages | Different methodologies |
| **Compatible config?** | Uses same config files/parameters | Requires conflicting configurations |

### c. Extension Patterns

**Pattern 1: Dashboard Extension (Multi-Page Apps)**
```python
# Existing: dashboards/workforce_capacity_dashboard.py
# New Feature: Pharmacist analysis (RELATED to workforce)
# Action: Add new page
dashboards/pages/03_💊_Pharmacist_Analysis.py
```

**Pattern 2: Module Extension (Add Functions)**
```python
# Existing: problem-statement/ps-001/analysis/burden_calculator.py
# New Feature: Calculate burden with demographic breakdown
# Action: Add function to existing module
def calculate_burden_by_demographics(df: pl.DataFrame) -> pl.DataFrame:
    """Calculate disease burden stratified by age/gender."""
```

### d. Integration Requirements

When extending existing implementations:

1. **Maintain consistency**: Same naming, code style, error handling, logging
2. **Preserve functionality**: DO NOT modify existing functions unless fixing bugs
3. **Use shared configs**: Read from existing `shared/config/*.yml` or `problem-statement/ps-{num}-{name}/config/*.yml`, add entries if needed
4. **Update documentation**: Update README with new features added

**Verification Checklist (see §8.2):**
- [ ] Searched for existing implementations
- [ ] Assessed relevance (domain, audience, workflow)
- [ ] Extended existing ONLY if relevant
- [ ] New code follows existing patterns
- [ ] No regressions in existing functionality


## 6. Implementation Requirements

The implementation MUST:
- **FIRST**: Create the problem-statement-specific directory structure per CRITICAL RULES** (see top of document)
- Follow the staged implementation approach outlined below
- Adhere to file paths, code structures, and configurations specified in the plan
- Follow project coding standards and best practices
- **Leverage MCP (Model Context Protocol) tools for all file and data operations as specified below**
- **Implement ALL code blocks provided in the implementation plan verbatim (see Code Implementation Fidelity below)**
- **Update README files to document the code running flow and execution instructions (see README Documentation Requirements below)**
- **VERIFY DATA STRUCTURES BEFORE WRITING CODE**
- **Create at least one Jupyter notebook for each execution** to facilitate user viewing of outputs and results
  - **Notebook Location**: Place notebooks in `problem-statement/ps-{num}-{name}/notebooks/` directory
  - **CRITICAL Dependency Requirements**:
    - **BEFORE creating notebooks**: Execute all prerequisite scripts/code to generate required data
    - **Document dependencies**: Include markdown cell at top listing all prerequisite scripts
    - **Test execution flow**: Run all dependencies → then run notebook → verify outputs
    - **Verify data exists**: Check that all expected input files exist before running notebook cells
    - **Check file existence explicitly**: Use `Path(file).exists()` before reading files to provide clear error messages instead of letting exceptions occur
  - Include markdown cells documenting each analysis step
  - **🚨 CRITICAL NOTEBOOK FORMATTING RULE**: When creating Jupyter notebooks, NEVER use literal `\n` characters in cell source code.

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

## 7. Multi-Agent Orchestration for Data Analysis Lifecycle

**Reference**: [Agent Configuration](.github/agents/config.yml) | [Agent Registry](.github/agents/registry.yml) | [Agent Documentation](.github/agents/README.md)

### 7.1 Orchestration Strategy Decision Framework

**Purpose**: Choose the appropriate agent orchestration strategy based on implementation requirements.

**Available Orchestration Approaches:**

| Approach | Use Case | Execution Model | Quality Gates |
|----------|----------|-----------------|---------------|
| **Sequential Single-Stage** | One user story, linear workflow | Execute one specialist agent at a time | Quality checks after each stage |
| **Sequential Multi-Stage** | One user story, complex pipeline | Chain specialist agents with handoffs | Quality checks at pipeline milestones |
| **Parallel Multi-User Story** | Multiple independent user stories | Multiple agents work simultaneously | Consolidated quality review at end |

**Decision Matrix:**

```
START: How many user stories need implementation?

├─ ONE User Story
│  ├─ Simple implementation (1-2 stages)?
│  │  └─ Use: Sequential Single-Stage
│  │     • Example: Data extraction only
│  │     • Pattern: ExtractionAgent → Code Review → Done
│  │
│  └─ Complex pipeline (3+ stages)?
│     └─ Use: Sequential Multi-Stage (Section 7.2)
│        • Example: Full ETL → EDA → Modeling → Dashboard
│        • Pattern: ExtractionAgent → ProfilingAgent → CleaningAgent → EDAAgent → ModelingAgent
│        • Quality: After each 2-3 stages
│
└─ MULTIPLE User Stories
   ├─ Are they independent or minimally coupled?
   │  └─ YES → Use: Parallel Multi-User Story
   │     • Agents work simultaneously on different user stories
   │     • Share code via handoff files
   │     • Consolidated quality review after all complete
   │
   └─ Are they tightly coupled/dependent?
      └─ NO → Use: Sequential Multi-Stage
         • Implement dependencies first
         • Then implement dependent user stories
         • Treat as single complex pipeline
```

**Key Selection Criteria:**

| Criterion | Sequential | Parallel |
|-----------|-----------|----------|
| **Number of User Stories** | 1 | > 1 |
| **Dependencies** | Linear/Sequential | Independent/Minimal |
| **Specialist Expertise** | Same domain (e.g., all modeling) | Different domains (extraction + visualization + modeling) |
| **Time Priority** | Can wait for sequential completion | Need fast delivery |
| **Code Sharing** | Within same problem statement | Across different problem statements/user stories |
| **Quality Review** | After each 2-3 stages | After ALL agents complete |

**Critical Differences:**

| Aspect | Sequential | Parallel |
|--------|-----------|----------|
| **Handoff Files** | Agent-to-agent pipeline handoffs | Agent-to-coordination-space broadcasts |
| **Code Sharing** | Via pipeline stages | Via shared handoff directory monitoring |
| **Review Timing** | Every 2-3 stages | Only after ALL agents complete |
| **Failure Impact** | Blocks next stage only | Blocks final quality review only |
| **Consolidation** | Not needed (single pipeline) | **MANDATORY** (merge shared utilities) |

### 7.2 How to Invoke Specialist Agents (Sequential Multi-Stage)

Use the `#runSubagent` tool to delegate specific lifecycle stages to specialist agents. Each agent:
- Reads its template from `.github/agents/{agent}.agent.md`
- Follows instructions in `.github/instructions/data-analysis-stages-instructions/`
- **MUST read its responsible segment** from this implementation plan for context
- Generates code, outputs, and handoff files according to specifications

**Handoff Validation Requirements:**

Before proceeding to the next stage, the **receiving agent** MUST:
1. **Verify handoff file exists** at expected location
2. **Check validation_status** is "passed" (if "failed", escalate and halt)
3. **Validate all output files** listed in handoff exist and are readable
4. **Verify data integrity** (row counts, column names, data types match expectations)
5. **Review critical_issues** - if any exist, address before proceeding
6. **Read recommended actions** and incorporate into implementation

**Example - CleaningAgent Reading Handoff from ProfilingAgent:**

```python
# In CleaningAgent implementation
import json
from pathlib import Path

handoff_path = Path("/data/3_interim/agent_handoffs/profiling_to_cleaning_20260316_150000.json")

# 1. Verify handoff exists
if not handoff_path.exists():
    raise FileNotFoundError(f"Handoff file from ProfilingAgent not found: {handoff_path}")

# 2. Load and validate
with open(handoff_path) as f:
    handoff = json.load(f)

if handoff["validation_status"] != "passed":
    raise ValueError(f"ProfilingAgent validation failed. Review findings: {handoff['findings']}")

# 3. Extract cleaning actions from previous stage
recommended_actions = handoff["recommended_cleaning_actions"]
# ['impute_missing_values_specialty_using_mode', 'handle_outliers_workforce_count_using_winsorization', ...]

# 4. Implement cleaning logic based on recommendations
for action in recommended_actions:
    if "impute_missing" in action:
        # Implement imputation logic
        pass
    elif "handle_outliers" in action:
        # Implement outlier handling logic
        pass
```
**Key Principles:**
- ✅ **Input Validation**: Each agent validates inputs before proceeding
- ✅ **Context-Aware**: Agents read previous findings and adapt implementation
- ✅ **Output Verification**: All code must execute successfully before handoff
- ✅ **Quality Gates**: Subagent reviews are MANDATORY before proceeding
- ✅ **Traceability**: Handoff files create audit trail of entire pipeline

This orchestration approach ensures **reproducible, high-quality, end-to-end data analysis implementations**.

## Verification Requirements

After implementation, the following verifications MUST be completed:

1. **Acceptance Criteria Verification**
   - Each acceptance criterion MUST be verified as met
   - Any discrepancies MUST be documented

2. **Quality Subagent Execution Verification (MANDATORY)**
   - **REQUIRED**: Verify that quality review subagents were executed during implementation
   - **REQUIRED**: Document all subagent executions with timestamps and findings
   - **REQUIRED**: Confirm critical/high priority issues from subagent reports were fixed
   - **REQUIRED**: Provide evidence that security vulnerabilities were addressed
   - **REQUIRED**: Show refactoring completed for duplicate code (3+ occurrences)
   
   **Quality Verification Checklist:**
   ```
   - [ ] Code Reviewer Agent Code Review executed after 2-3 major module
   - [ ] Dead Code Elimination subagent executed during implementation
   - [ ] Comprehensive Code Reviewer Agent review executed before marking complete
   - [ ] All critical issues from quality reports fixed
   - [ ] All high priority issues from quality reports fixed
   - [ ] Security vulnerabilities addressed (credentials, SQL injection, etc.)
   - [ ] Duplicate code refactored (3+ occurrences)
   - [ ] Medium/low priority improvements documented in TODO.md
   - [ ] Final quality report shows >80% functions with type hints, docstrings and consistent error handling patterns
   ```

3. **Design Implementation Verification**
   - Complete the Design Implementation Verification Checklist
   - The checklist MUST include the sections below

- Explicitly check that all service and API integration logic is implemented, not just stubbed.
- During verification, confirm that all functions required to fetch, process, and return data are fully implemented and tested.
- If any function is a stub or placeholder, the implementation is NOT complete. Document this as a failure and halt further verification until resolved.

## README Documentation Requirements

After implementing code, README files MUST be updated to reflect the actual code running flow and execution instructions. This ensures that future users (including stakeholders, team members, and the AI agent itself) can understand and execute the code correctly.

## README Update Process

When updating README files, follow this process:

1. **Execute All Dependencies First**: Run prerequisite scripts to generate required data
2. **Execute the Code**: Run all implemented scripts/notebooks to verify actual execution flow
3. **Document Dependency Chain**: Record which scripts must run before notebooks/other scripts
4. **Document Actual Flow**: Record the actual sequence, inputs, outputs, and timings observed
5. **Capture Error Messages**: Note common errors encountered during testing (especially missing dependencies)
6. **Verify Instructions**: Test README instructions on a fresh environment to ensure accuracy
7. **Test Notebook Prerequisites**: Verify notebooks fail gracefully if dependencies haven't run
8. **Document Folder Structure**: Update README with complete directory structure tree (see Folder Structure Documentation Requirements below)
9. **Map Import Paths to Structure**: Document import path mappings to prevent ModuleError/ImportError (see Import Path Mapping Requirements below)

## README Update Verification

After updating README files, verify:

- ✅ Quick Start commands execute successfully on a fresh environment
- ✅ Execution Flow diagram matches actual code execution sequence
- ✅ **Execution Flow includes "Must run before" dependencies for each stage**
- ✅ **Notebook prerequisites are clearly documented (scripts that must run first)**
- ✅ All input/output file paths are accurate and exist
- ✅ Environment setup instructions are complete and tested
- ✅ Execution modes work as documented
- ✅ **Troubleshooting includes solutions for missing dependencies/data files**
- ✅ Troubleshooting section addresses actual errors encountered
- ✅ All code snippets in README are syntactically correct
- ✅ Dependencies listed match `requirements.txt`
- ✅ Configuration examples match actual config files
- ✅ **Test complete execution flow**: Run all dependencies → Run notebooks → Verify outputs
- ✅ **Verify notebooks fail gracefully** if prerequisites haven't been run (with helpful error messages)

## Documentation Requirements

The final output MUST include:
- Confirmation of completion if successful
- Results of all verification steps
- Any command outputs or test results
- The completed Design Implementation Verification Checklist
- Any noted discrepancies or issues
- **Updated README files documenting code execution flow** (see README Documentation Requirements above)
- **Updated README with complete folder structure tree** (see Folder Structure Documentation Requirements above)
- **Updated README with import path mapping table** to prevent ModuleError/ImportError
- Verification that README instructions have been tested and work correctly
- **For Parallel Multi-User Story Execution** (if applicable):
  - Agent assignment and coordination summary
  - Handoff file inventory showing inter-agent communication
  - Consolidation report (shared utilities extracted, duplicate code removed)
  - Multi-user-story quality review results
  - Cross-user-story integration test results