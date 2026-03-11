---
description: Prompt for Execution of Implementation Plans (Condensed & Optimized)
stage: Development
version: 2.0
---
# Prompt: Execute Implementation Plan

## Role

Execute a detailed implementation plan accurately and verify its completion according to specifications for end-to-end data analysis projects.

## 🚨 CRITICAL RULES - READ FIRST

### Directory Structure (MANDATORY - Hybrid Approach)

**✅ CORRECT - Self-contained problem statement package:**
```
problem-statement/ps-{num}-{descriptive-name}/
├── notebooks/              # Interactive analysis
│   ├── 1_exploratory/      # Data profiling, exploration
│   ├── 2_analysis/         # Deep-dive analysis, modeling
│   └── 3_feature_engineering/  # Feature creation
├── src/                    # Problem-specific utilities
│   ├── __init__.py
│   └── {name}_utils.py     # Custom helper functions
├── data/                   # Problem-specific data
│   ├── 3_interim/          # Intermediate processing results
│   └── 4_processed/        # Final analysis-ready datasets
├── results/                # Analysis outputs
│   ├── tables/
│   ├── metrics/
│   └── exports/
├── reports/                # Visualizations and reports
│   ├── figures/
│   ├── dashboards/
│   └── presentations/
├── models/                 # Trained models and artifacts
├── config/                 # Problem-specific configuration
│   └── config.yml
├── scripts/                # Pipeline orchestration
│   └── run_pipeline.py
├── tests/                  # Integration tests
│   └── integration/
├── logs/                   # Execution logs
│   ├── pipeline/
│   └── errors/
└── README.md              # Problem overview and instructions
```

**Shared Resources** (import from these):
```
shared/
├── src/                    # Reusable library code (IMPORT FROM HERE)
│   ├── data_processing/    # ETL, cleaning, validation
│   ├── analysis/           # Statistical algorithms
│   ├── models/             # Modeling utilities
│   └── visualization/      # Plotting functions
├── data/                   # Shared data sources
│   ├── 1_raw/              # Original source data (READ-ONLY)
│   └── 2_external/         # Reference data (READ-ONLY)
└── sql/                    # Common SQL queries
```

### Naming Convention (MANDATORY)

**Format**: `src/problem-statement-{num}-{descriptive-name}/`
- `{num}`: Zero-padded problem statement number (e.g., `001`, `002`)
- `{descriptive-name}`: Kebab-case description (e.g., `workforce-capacity-mismatch`)

**✅ Examples:**
- `src/problem-statement-001-workforce-capacity-mismatch/`
- `src/problem-statement-002-seasonal-disease-forecasting/`

### Organization Rules

1. **One Problem Statement = One Directory**: All user stories for the same problem statement share ONE directory
2. **No Shared Notebooks Directory**: Do NOT create notebooks in `notebooks/1_exploratory/`, `notebooks/2_analysis/`, etc.
3. **Problem-Statement Outputs**: Save outputs to subdirectories: `reports/figures/problem-statement-{num}/`, `results/tables/problem-statement-{num}/`

---

## Input/Output Requirements

### Input
- A detailed implementation plan (typically in Markdown format)
- User story and acceptance criteria
- Design specifications and requirements (if applicable)

### Output
- **Problem-Statement-Specific Directory Structure** (per CRITICAL RULES)
- Implementation of all required files and changes
- Verification that specifications have been met
- Completed verification checklist
- Updated README with execution instructions
- **CRITICAL Dependency Requirements**:
    - **BEFORE creating notebooks**: Execute all prerequisite scripts/code to generate required data
    - **Example**: For exploration notebook, run extraction and profiling scripts first
    - **Document dependencies**: Include markdown cell at top listing all prerequisite scripts
    - **Test execution flow**: Run all dependencies → then run notebook → verify outputs
    - **Verify data exists**: Check that all expected input files exist before running notebook cells

---

## Pre-Implementation Checklist

Before starting implementation, verify:

- [ ] **Plan Review**: All steps are clear and complete
- [ ] **Information Availability**: All necessary context is available (request clarification if not)
- [ ] **Environment Setup**: Python environment configured (see [Environment Setup](#environment-setup))
- [ ] **Execution Mode**: Determined using [Decision Tree](#execution-mode-selection)
- [ ] **Stage Identification**: Identified applicable stages from implementation plan
- [ ] **Tool Access**: Verified MCP tools availability (filesystem, SQLite if needed)

---

## Conflict Resolution & Precedence

When this prompt conflicts with the implementation plan:

| Aspect | Rule |
|--------|------|
| **Directory structure** | ALWAYS follow prompt (non-negotiable) |
| **Stage sequence** | Adapt stages to match plan's structure |
| **Code content** | Implement plan code faithfully; fix obvious bugs with documentation |
| **Tools/packages** | Prefer plan's choices unless they violate project standards |
| **Design specs** | Follow plan exactly for UI/dashboards; adapt for analysis deliverables |

**Guiding Principle**: This prompt provides *structural standards*; the implementation plan provides *functional specifications*.

---

## Execution Mode Selection

Use this decision tree to choose between Single-Agent and Multi-Agent execution:

```
START
  ├─ Does plan cover 3+ distinct stages? ────No───┐
  │                                                 │
  │  Yes                                            │
  │  ├─ Is it a full analysis lifecycle? ──No──┐   │
  │  │   (extraction→EDA→modeling→viz)          │   │
  │  │                                           │   │
  │  │  Yes                                      │   │
  │  │  └─> USE MULTI-AGENT ✅                  │   │
  │  │                                           │   │
  │  └─────────────────────────────────────────┘   │
  │                                                 │
  └─────────────────────────────────────────────>  USE SINGLE-AGENT ✅
                                                    (faster for simple tasks)
```

**When unsure**: Default to **Single-Agent** for simplicity.

---

## Execution Approaches

### Option 1: Single-Agent Execution (Default)

Execute all stages sequentially as described in [Implementation Stages](#implementation-stages).

**Use when:**
- Simple, single-stage tasks (e.g., "create EDA notebook")
- Quick exploratory analysis (1-2 stages)
- Full control over entire workflow needed
- Plan covers ≤2 stages

**Process:**
1. Follow [Implementation Stages](#implementation-stages) sequentially
2. Use MCP tools for all file operations (see [MCP Tools Quick Reference](#mcp-tools-quick-reference))
3. Create outputs in problem-statement-specific directories
4. Verify against acceptance criteria

---

### Option 2: Multi-Agent Orchestration (For Complex Pipelines)

Delegate stages to specialized agents using the `runSubagent` tool.

**Use when:**
- Full data analysis pipeline (extraction → profiling → cleaning → EDA → modeling → visualization)
- Plan covers 3+ distinct specialized stages
- Automated quality gates between stages needed
- Each stage requires specialist expertise

**Available Specialist Agents:**

| Stage | Agent | Template Path |
|-------|-------|---------------|
| Data Extraction | ExtractionAgent | `.agents/templates/extraction_agent.md` |
| Data Profiling | ProfilingAgent | `.agents/templates/profiling_agent.md` |
| Data Cleaning | CleaningAgent | `.agents/templates/cleaning_agent.md` |
| EDA | EDAAgent | `.agents/templates/eda_agent.md` |
| Modeling | ModelingAgent | `.agents/templates/modeling_agent.md` |
| Visualization | VisualizationAgent | `.agents/templates/visualization_agent.md` |
| Quality Checks | QualityAgent | `.agents/templates/quality_agent.md` |
| Documentation | DocumentationAgent | `.agents/templates/documentation_agent.md` |

**Multi-Agent Invocation Pattern:**

```
runSubagent(
  description: "{AgentName} for Problem Statement {num}",
  prompt: "Read and execute the template from .agents/templates/{agent}_agent.md
  
  Context:
  - Problem Statement: {num} - {title}
  - Previous Handoff: {path_to_handoff_file} (if applicable)
  - Input Data: {path_to_input}
  - Specific Requirements: {additional_context}
  
  Execute all steps in the template and create handoff file in:
  data/3_interim/agent_handoffs/{agent}_to_{next_agent}_{timestamp}.json
  
  Return: Handoff file path and summary of completed work."
)
```

**Example - Sequential Pipeline:**

```
1. ExtractionAgent → creates extraction handoff
2. ProfilingAgent → reads extraction handoff, creates profiling handoff
3. CleaningAgent → reads profiling handoff, creates cleaning handoff
4. EDAAgent → reads cleaning handoff, creates EDA handoff
5. Continue as needed...
```

**🔗 Details**: See [Multi-Agent Execution Guide](.github/guides/multi-agent-execution-guide.md)

---

## Environment Setup

### 1. Python Environment
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv (preferred) or pip
uv pip install -r requirements.txt
# OR: pip install -r requirements.txt
```

### 2. Verify MCP Tools Access
- Filesystem tools (REQUIRED for all implementations)
- SQLite tools (if database operations needed)
- GitHub tools (optional)

### 3. Configuration Files
- Check `config/analysis.yml` for project-specific parameters
- Review `config/cleaning_rules.yml` for data quality standards

---

## Implementation Stages

**⚠️ ADAPT TO YOUR PLAN**: Use only the stages specified in your implementation plan. Skip irrelevant stages.

### Stage 0: Environment Setup
- Configure Python environment and install packages
- Verify MCP tools availability
- Set up API keys/credentials (if needed)
- **Output**: Verified environment, logs in `logs/etl/`

### Stage 1: Problem Understanding & Setup
- Review user story and acceptance criteria
- Create problem-statement directory structure (see [CRITICAL RULES](#critical-rules---read-first))
- Document assumptions and constraints
- **Output**: Directory structure, initial README

### Stage 2: Data Collection & Extraction
- Extract data from sources (use filesystem/SQLite MCP tools)
- Implement data fetching with error handling and retries
- Save raw data with metadata and timestamps to `data/1_raw/` or `data/3_interim/`
- **Output**: Extracted data files, extraction logs

**🤖 Multi-Agent Option**: Delegate to `ExtractionAgent` (see [Multi-Agent Guide](.github/guides/multi-agent-execution-guide.md#extraction-stage))

### Stage 3: Data Profiling & Quality Assessment
- Generate data quality reports (distributions, missing values, outliers)
- Create exploration notebook in `src/problem-statement-{num}/notebooks/`
- Save profiling results to `results/tables/problem-statement-{num}/`
- **Output**: Quality report, profiling metrics, exploration notebook

**🤖 Multi-Agent Option**: Delegate to `ProfilingAgent`

### Stage 4: Data Cleaning & Preprocessing
- Implement cleaning logic based on profiling findings
- Handle missing values, outliers, type corrections
- Save cleaned data to `data/4_processed/`
- Document transformations in cleaning logs
- **Output**: Cleaned data, cleaning logs in `logs/etl/`

**🤖 Multi-Agent Option**: Delegate to `CleaningAgent`

### Stage 5: Exploratory Data Analysis (EDA)
- Conduct statistical analysis and hypothesis testing
- Create visualizations in analysis notebook
- **REQUIRED**: Save ALL figures to `reports/figures/problem-statement-{num}/`
- **REQUIRED**: Save ALL summaries to `results/tables/problem-statement-{num}/`
- **REQUIRED**: Save ALL metrics to `results/metrics/problem-statement-{num}/`
- Use timestamps in filenames (e.g., `seasonal_trends_20260225_143022.png`)
- **Output**: EDA notebook, figures, summary tables, insights

**🤖 Multi-Agent Option**: Delegate to `EDAAgent`

### Stage 6: Feature Engineering & Transformation (ML/Advanced Analytics Only)
- Design and create relevant features
- Apply transformations (scaling, encoding, etc.)
- Save processed data to `data/4_processed/`
- **Output**: Feature-engineered data, feature definitions
- **⚠️ Skip**: If analysis is descriptive/exploratory only

### Stage 7: Analysis Implementation & Modeling
- Implement analytical methods or statistical/ML models
- Perform calculations, aggregations, or predictions
- Save model artifacts to `models/problem-statement-{num}/`
- Save results to `results/metrics/problem-statement-{num}/`
- **Output**: Models, analysis results, methodology documentation

**🤖 Multi-Agent Option**: Delegate to `ModelingAgent`

### Stage 8: Results Validation & Quality Assurance
- Verify outputs meet acceptance criteria
- Validate results against benchmarks
- Write unit tests in `tests/unit/problem-statement-{num}/`
- Log validation results to `logs/audit/`
- **Output**: Test suite, validation report

**🤖 Multi-Agent Option**: Delegate to `QualityAgent`

### Stage 9: Documentation & Reporting
- Create comprehensive analysis documentation
- Generate reports with findings and recommendations
- Build dashboards/visualizations (if required)
- **Update README with execution instructions** (see [README Requirements](#readme-documentation-requirements))
- Save reports to `reports/problem-statement-{num}/`
- **Output**: Final report, updated README, presentation materials

**🤖 Multi-Agent Option**: Delegate to `VisualizationAgent` + `DocumentationAgent`

### Stage 10: Delivery & Handoff
- Package final deliverables
- Complete verification checklist
- Verify all acceptance criteria met
- **Output**: Final verification report

**🤖 Multi-Agent Option**: Delegate to `QualityAgent` for final validation

---

## MCP Tools Quick Reference

### Filesystem Tools (REQUIRED)
Use for ALL file operations:

```
Read data:     "Use filesystem tools to read data/1_raw/input.csv"
Create dir:    "Use filesystem tools to create directory results/problem-statement-001/"
Write file:    "Use filesystem tools to save results to results/tables/output.csv"
List files:    "Use filesystem tools to list files in src/problem-statement-001/"
```

### SQLite Tools (when applicable)
Use for database operations:

```
Query:         "Query using SQLite tools: SELECT * FROM patients WHERE year >= 2020"
Create table:  "Use SQLite tools to create summary table"
```

**🔗 Details**: See [MCP Tools Reference Guide](.github/guides/mcp-tools-reference.md)

---

## Code Implementation Requirements

### Implementation Fidelity

When the implementation plan includes code blocks:

✅ **Implement faithfully**:
- Use provided code as the primary reference
- Maintain type hints, docstrings, parameter definitions
- Include all error handling and validation logic
- Preserve logging and audit trail code

✅ **Allow reasonable adaptations**:
- Fix obvious bugs or syntax errors (document changes)
- Update deprecated library calls
- Adjust paths to match project structure
- Improve code quality if plan code has issues

❌ **Do NOT**:
- Create stub implementations (all functions must be complete)
- Skip error handling or validation
- Remove logging or documentation
- Ignore test coverage requirements

### Notebook Requirements

**REQUIRED**: Create at least one Jupyter notebook demonstrating:
- Loading and exploring outputs
- Visualizing key metrics and indicators
- Running validation checks
- Interactive exploration of results

**Location**: `src/problem-statement-{num}/notebooks/`
**Naming**: `{stage_number}_{descriptive_name}.ipynb` (e.g., `02_data_profiling.ipynb`)

---

## README Documentation Requirements

After implementation, **UPDATE README** with actual execution flow.

### Required README Sections

1. **Quick Start**: Command-line instructions to run the analysis
2. **Execution Flow**: Step-by-step sequence with inputs/outputs
3. **Input/Output Specifications**: Tables of file paths and formats
4. **Environment Setup**: Python environment and dependencies
5. **Troubleshooting**: Common issues and solutions

**🔗 Template**: See [README Template Examples](.github/guides/readme-templates.md)

---

## Verification Requirements

### Acceptance Criteria Verification

For each acceptance criterion in the implementation plan:

```
Acceptance Criterion 1: [Description]
✅ Verified using filesystem tools:
   - File exists: [path]
   - File size: [size] (verified non-empty)
   - Content validation: [describe checks performed]

Acceptance Criterion 2: [Description]
✅ Verified using [tool]: [specific verification steps]
```

### Design Verification (Dashboards/UI Only)

**⚠️ Only applicable for dashboard/UI deliverables. Skip for analysis reports/notebooks.**

If implementing dashboards, verify:
- Colors match design specifications exactly
- Spacing matches design values
- Typography matches design specifications
- Layout structure matches design mockups

**🔗 Details**: See [Design Verification Guide](.github/guides/design-verification-guide.md)

### Final Verification Checklist

- [ ] All files located in correct problem-statement directory
- [ ] All outputs saved with timestamps in problem-statement subdirectories
- [ ] README updated with execution instructions
- [ ] At least one notebook created for result exploration
- [ ] All acceptance criteria met and verified
- [ ] Code follows project standards (see `.github/instructions/python-best-practices.instructions.md`)
- [ ] Tests written for critical logic (if applicable)
- [ ] Logs generated for audit trail

---

## Error Handling

If implementation or verification fails:

1. **Identify**: Clearly state which part failed (stage, file, acceptance criterion)
2. **Describe**: Explain the specific issue encountered
3. **Deviation**: Describe how it deviates from the plan
4. **Solution**: Suggest possible fixes or next steps
5. **Document**: Log the error to `logs/errors/` with timestamp

---

## Deliverables Summary

Upon completion, ensure these artifacts exist:

✅ **Code & Notebooks**
- Problem-statement directory: `src/problem-statement-{num}-{name}/`
- Notebooks with results: `src/problem-statement-{num}/notebooks/`
- Scripts/modules: `src/problem-statement-{num}/{data_processing,analysis,scripts}/`

✅ **Data Outputs**
- Figures: `reports/figures/problem-statement-{num}/`
- Tables: `results/tables/problem-statement-{num}/`
- Metrics: `results/metrics/problem-statement-{num}/`

✅ **Documentation**
- Updated README: `src/problem-statement-{num}/README.md`
- Methodology docs: `docs/methodology/` (if applicable)
- Final report: `reports/problem-statement-{num}/` (if applicable)

✅ **Logs & Tests**
- Logs: `logs/etl/`, `logs/errors/`, `logs/audit/`
- Tests: `tests/unit/problem-statement-{num}/` (if applicable)

✅ **Verification**
- Completed verification checklist
- Handoff file (if using multi-agent): `data/3_interim/agent_handoffs/`

---

## Additional Resources

- [Multi-Agent Execution Guide](.github/guides/multi-agent-execution-guide.md) - Detailed agent orchestration workflows
- [MCP Tools Reference](.github/guides/mcp-tools-reference.md) - Comprehensive MCP tools documentation
- [README Templates](.github/guides/readme-templates.md) - Example README structures
- [Design Verification Guide](.github/guides/design-verification-guide.md) - Dashboard verification procedures
- [Python Best Practices](.github/instructions/python-best-practices.instructions.md) - Project coding standards
- [Data Analysis Best Practices](.github/instructions/data-analysis-best-practices.instructions.md) - Analysis methodology

---

**Version**: 2.0 (Condensed & Optimized)  
**Last Updated**: 2026-02-25  
**Target Length**: ~600 lines (vs. 1045 lines in v1.0)
