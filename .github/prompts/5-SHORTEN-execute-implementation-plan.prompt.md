---
description: Prompt for Execution of the Implementation Plan
stage: Development
version: 2.0
---

# AI Agent Prompt: Execute Implementation Plan

## Role

Execute a detailed implementation plan accurately and verify its completion according to specifications for an end-to-end data analysis project.

## Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Problem Statement (PS)** | Top-level analysis objective | PS-001: Workforce Capacity Mismatch |
| **User Story (US)** | Deliverable subset of a problem statement | US-001 within PS-001 |
| **Subagent** | Specialist AI agent invoked via `#runSubagent` | ExtractionAgent, Code Reviewer Agent |
| **Handoff File** | JSON file agents use to pass validated outputs | `extraction_to_profiling_20260306.json` |
---

## 🚨 CRITICAL RULES - READ FIRST

### Rule 1: Directory Structure - Hybrid Approach (MANDATORY)

**See [FOLDER-STRUCTURE-REFERENCE.md](FOLDER-STRUCTURE-REFERENCE.md) for complete details.**

**✅ CORRECT - Self-contained problem-statement package:**
```
problem-statement/ps-{num}-{descriptive-name}/
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

**Shared Resources (Reusable Code):**
```
shared/
├── src/                    # Shared utilities
│   ├── data_processing/    # Loaders, validators
│   ├── analysis/           # Statistical functions
│   └── visualization/      # Chart generators
├── data/                   # Raw data sources
│   ├── 1_raw/              # Original source data
│   └── 2_external/         # Reference data
├── config/                 # Base configuration
└── tests/unit/             # Tests for shared code
```

**Format**: `problem-statement/ps-{num}-{descriptive-name}/`
- `{num}`: Zero-padded PS number (e.g., `001`, `002`)
- `{descriptive-name}`: Kebab-case (e.g., `seasonal-pattern-forecasting`)

**✅ Examples:**
- `problem-statement/ps-001-seasonal-pattern-forecasting/`
- `problem-statement/ps-002-disease-burden-prioritization/`

**❌ FORBIDDEN:**
- `problem-statements/ps_001/` (underscores)
- `src/problem-statement-001/` (old structure)
- Mixing shared and problem-specific code in same directory

**Organization Principles:**
1. **Shared Code**: Reusable functions → `shared/src/`
2. **Problem-Specific Code**: One-time use → `problem-statement/ps-{num}/src/`
3. **Raw Data**: Shared across problems → `shared/data/1_raw/`
4. **Processed Data**: Problem-specific → `problem-statement/ps-{num}/data/`
5. **Import Pattern**: Add `sys.path.append(shared_path)` to access shared code

### Rule 2: Quality Gates Are Non-Negotiable (MANDATORY)

**🚨 CRITICAL**: Quality review subagents MUST be executed DURING implementation. Implementation without quality reviews is INCOMPLETE.

**WHEN TO EXECUTE (Reference §6 for details):**

| Stage | Subagent | Purpose |
|-------|----------|---------|
| **BEFORE any code** | Directory Structure Validation | Prevent duplicate directories |
| **After each module** | Code Reviewer Agent (Incremental) | Catch issues early |
| **After 2-3 modules** | Dead Code Elimination | Remove unused code |
| **After file creation** | Import Path Validation | Verify imports match filesystem |
| **Before completion** | Code Reviewer Agent (Comprehensive) | Final quality gate |

**See §6 for detailed subagent invocation patterns.**

### Rule 3: Implement Code Exactly As Specified (MANDATORY)

When implementation plan includes complete code blocks:
- ✅ **USE VERBATIM**: Type hints, docstrings, error handling, logging, tests
- ❌ **NO STUBS**: Functions with only `pass` or `NotImplementedError` = INCOMPLETE
- ❌ **NO PLACEHOLDERS**: "TODO: implement later" = INCOMPLETE

**Rationale**: Plan code is production-ready, security-tested, and handles edge cases.

**See §4.1 for verification checklist.**

### Rule 4: Check for Existing Implementations First (MANDATORY)

**Before creating new features:**
1. Search workspace for similar implementations
2. Assess if new feature is **relevant and related** to existing
3. **EXTEND** if domains/audiences/contexts align
4. **CREATE SEPARATE** if use cases differ

**See §3 for extension patterns and decision logic.**

---

## Quick Reference: Implementation Workflow

```
1. Read Implementation Plan
   ↓
2. Plan Clear? → If No: Request Clarification
   ↓ If Yes
3. Validate Directory Structure (§6.1)
   ↓
4. Check Existing Implementations (§3)
   ↓
5. Implement Code
   ↓
6. Incremental Quality Review (§6.2)
    ↓
7. Issues Found? → If Yes: Fix Critical/High → Back to Step 5
   ↓ If No
8. Update README (§7)
   ↓
9. Final Quality Review (§6.3)
   ↓
10. Verify Acceptance Criteria (§8)
    ↓
11. Complete
```

---

## Input & Output Requirements

### Input
You will receive:
- Detailed implementation plan (Markdown format)
- User story and acceptance criteria
- Design specifications (colors, spacing, layouts)
- Configuration requirements

### Output
You MUST deliver:
- **Problem-statement directory** following Rule 1
- **Fully implemented code** (no stubs)
- **Updated README** with execution instructions (§7)
- **Quality verification report** (§6.4)
- **Acceptance criteria verification** (§8)

---

## §2: Pre-Implementation Review

**STOP**: Before writing any code, verify the implementation plan has:

- [ ] Clear step-by-step instructions for all stages
- [ ] File paths and directory structure specified
- [ ] Complete code blocks (not pseudocode)
- [ ] Design specifications (if UI/dashboard work)
- [ ] Configuration files and their locations
- [ ] Expected inputs and outputs defined
- [ ] Acceptance criteria listed

**If ANY item is missing or unclear:** Request clarification before proceeding.

---

## §3: Search for Existing Implementations

**MANDATORY STEP**: Before creating new features, search for similar implementations.

### §3.1 Search Process

```javascript
// Check for existing dashboards
grep_search("dashboard", isRegexp=false, includePattern="dashboards/**")

// Check for similar analysis modules
grep_search("forecasting|prediction", isRegexp=true, includePattern="src/**/analysis/**")

// Check for data processing patterns
semantic_search("data cleaning workflow for disease surveillance")
```

### §3.2 Relevance Assessment

Ask these questions to determine if feature should extend existing implementation:

| Question | EXTEND if... | CREATE NEW if... |
|----------|-------------|-----------------|
| **Same domain?** | Same disease types, same health outcomes | Different health domains (workforce vs disease) |
| **Same audience?** | Same stakeholders/decision-makers | Different user groups (clinicians vs policymakers) |
| **Same workflow?** | Same analytical pipeline stages | Different methodologies |
| **Compatible config?** | Uses same config files/parameters | Requires conflicting configurations |

### §3.3 Extension Patterns

**Pattern 1: Dashboard Extension (Multi-Page Apps)**
```python
# Existing: dashboards/workforce_capacity_dashboard.py
# New Feature: Pharmacist analysis (RELATED to workforce)
# Action: Add new page
dashboards/pages/3_💊_Pharmacist_Analysis.py
```

**Pattern 2: Module Extension (Add Functions to Shared Library)**
```python
# Existing: shared/src/analysis/burden_calculator.py
# New Feature: Calculate burden with demographic breakdown
# Action: Add function to shared module (if reusable across problems)
def calculate_burden_by_demographics(df: pl.DataFrame) -> pl.DataFrame:
    """Calculate disease burden stratified by age/gender."""
```

**Pattern 3: Separate Implementation**
```python
# Existing: problem-statement/ps-001-seasonal-forecasting/ (disease trends)
# New Feature: School absenteeism analysis (UNRELATED)
# Action: Create new problem statement directory
problem-statement/ps-004-school-absenteeism/
```

### §3.4 Integration Requirements

When extending existing implementations:

1. **Maintain consistency**: Same naming, code style, error handling, logging
2. **Preserve functionality**: DO NOT modify existing functions unless fixing bugs
3. **Use shared configs**: Read from existing `config/*.yml`, add entries if needed
4. **Update documentation**: Update README with new features added

**Verification Checklist (see §8.2):**
- [ ] Searched for existing implementations
- [ ] Assessed relevance (domain, audience, workflow)
- [ ] Extended existing ONLY if relevant
- [ ] New code follows existing patterns
- [ ] No regressions in existing functionality

---

## §4: Implementation Requirements

### §4.1 Code Fidelity

**When implementation plan includes complete code blocks:**

✅ **Implement verbatim:**
- Type hints and docstrings
- Error handling and retry logic
- Logging statements
- Input validation
- Unit tests with full coverage
- Security best practices

**Verification after implementation:**
- [ ] Every function from plan exists and is fully implemented
- [ ] Type hints and docstrings match specification
- [ ] Unit tests run successfully
- [ ] No stubs (`pass`, `NotImplementedError`, `TODO`)
- [ ] Error handling present for edge cases
- [ ] Logging captures critical events

### §4.2 Notebook Requirements

**Create at least one Jupyter notebook** for each execution to facilitate result viewing:

- **Location**: `problem-statement/ps-{num}-{name}/notebooks/`
- **Purpose**: Load outputs, visualize metrics, run validation, explore results
- **Self-contained**: Runnable independently after prerequisite scripts
- **Import Pattern**: Add `sys.path.append()` to access shared utilities from `shared/src/`

**CRITICAL Dependency Requirements:**
1. **BEFORE creating notebooks**: Execute all prerequisite scripts to generate data
2. **Document dependencies**: Markdown cell at top lists required scripts
3. **Test execution flow**: Run dependencies → run notebook → verify outputs
4. **Graceful failures**: Check data files exist, show helpful error if missing

**Example notebook header:**
```markdown
# Analysis Results Explorer

## Prerequisites
Run these scripts BEFORE executing this notebook:
1. `python scripts/01_extract_data.py`
2. `python scripts/02_clean_data.py`

## Expected Data Files
- `data/4_processed/cleaned_data.csv`
- `results/metrics/quality_scores.json`
```

---

## §5: Multi-Agent Orchestration

### §5.1 When to Use Subagents

Use `#runSubagent` for:
- ✅ Data extraction and loading (ExtractionAgent)
- ✅ Data quality assessment (ProfilingAgent)
- ✅ Exploratory analysis (EDAAgent)
- ✅ Statistical modeling (ModelingAgent)
- ✅ Code quality review (Code Reviewer Agent)

### §5.2  Stage-to-Agent Mapping

| Stage | Agent | Template | Input | Output |
|-------|-------|----------|-------|--------|
| **Data Collection** | ExtractionAgent | `.agents/extraction.agent.md` | Raw data paths | Extracted CSV + handoff |
| **Data Profiling** | ProfilingAgent | `.agents/profiling.agent.md` | Extraction handoff | Quality report + handoff |
| **EDA** | EDAAgent | `.agents/eda.agent.md` | Cleaned data | Insights + visualizations |
| **Modeling** | ModelingAgent | `.agents/modeling.agent.md` | Analysis-ready data | Models + performance metrics |
| **Quality Review** | Code Reviewer Agent | `.agents/code-reviewer.agent.md` | Code files | Quality report + fixes |

### §5.3 Simplified Invocation Pattern

**Single Agent (No Handoff):**
```javascript
#runSubagent({
  description: "Data extraction for PS-001",
  prompt: `Execute ExtractionAgent from .agents/extraction.agent.md
  
  Context:
  - Problem Statement: 001 (Workforce Capacity Mismatch)
  - Data Sources: data/1_raw/workforce_doctors.csv, data/1_raw/capacity_hospital_beds.csv
  - Target Output: data/3_interim/extracted_data_20260306.csv
  
  Return: Extraction handoff file path and row count summary`
})
```

**Sequential Pipeline (With Handoffs):**
```javascript
// Step 1: Extract
#runSubagent({...}) → extraction_handoff.json

// Step 2: Profile (reads extraction handoff)
#runSubagent({
  prompt: `Execute ProfilingAgent with input from: data/3_interim/agent_handoffs/extraction_handoff.json`
}) → profiling_handoff.json

// Step 3: Clean (reads profiling handoff)
#runSubagent({...}) → cleaned data + cleaning_handoff.json
```

### §5.4 Handoff Protocol

**Handoff File Format:**
```json
{
  "agent_name": "ProfilingAgent",
  "timestamp": "20260306_141530",
  "stage": 3,
  "validation_status": "passed",
  "outputs": {
    "report": "results/tables/problem-statement-001/data_quality_report.md",
    "metrics": "results/metrics/problem-statement-001/quality_metrics.json"
  },
  "findings": {
    "overall_quality_score": 87.5,
    "recommended_cleaning_actions": ["impute_missing_values", "handle_outliers"]
  },
  "recommended_next_step": "cleaning"
}
```

**Location**: `data/3_interim/agent_handoffs/`

See [`.agents/README.md`](.agents/README.md) for complete documentation.

---

## §6: Quality Gates (MANDATORY)

### §6.1 Directory Structure Validation (Execute FIRST)

**Before writing any code:**

```javascript
#runSubagent({
  description: "Validate directory structure for PS-{num}",
  prompt: `Check for duplicate directories matching: src/*{num}*
  
  Return:
  - Status: SAFE_TO_PROCEED | RENAME_REQUIRED | DUPLICATE_DETECTED
  - Existing_Directories: [list all matches]
  - Target_Directory: Single directory to use`
})
```

**Decision Logic:**
- No directory exists → Create with correct naming
- One directory, correct naming → Use existing
- One directory, wrong naming → Report violation, suggest rename
- Multiple directories → **CRITICAL ERROR** - consolidate required

### §6.2 Incremental Code Review (After Each 2-3 Modules)

```javascript
#runSubagent({
  description: "Code review for all blocks",
  prompt: `Review code quality for:
  - problem-statement/ps-{num}-{name}/**/*.py
  - problem-statement/ps-{num}-{name}/notebooks/*.ipynb
  
  Execute parallel reviews:
  - Correctness (logic, edge cases, types)
  - Code quality (readability, naming, duplication)
  - Security (input validation, injection risks)
  - Architecture (pattern consistency)
  
  FIX all critical/high issues immediately.
  Return: Fixed code + quality report`
})
```

### §6.3 Import Path Validation (After File Creation)

```javascript
#runSubagent({
  description: "Validate import paths",
  prompt: `Verify all imports in problem-statement/ps-{num}-{name}/ match filesystem.
  
  Check:
  - Module exists on filesystem (no typos)
  - Naming consistency (hyphens vs underscores)
  - Shared imports use sys.path.append(shared_path)
  - No circular imports
  
  Return: ALL_VALID | MISMATCHES_FOUND with fixes`
})
```

### §6.4 Final Comprehensive Review (Before Completion)

```javascript
#runSubagent({
  description: "Comprehensive review for PS-{num}",
  prompt: `Final quality gate before marking complete.
  
  Verify:
  1. All functions fully implemented (no stubs and no errors)
  2. >80% functions have type hints
  3. >80% functions have docstrings
  4. Consistent error handling patterns
  5. No security vulnerabilities
  6. Duplicate code refactored (3+ occurrences)
  7. All unit tests pass
  
  Return: Quality scorecard + any blocking issues`
})
```

### §6.5 Mandatory Actions After Each Subagent Report

1. **REVIEW** findings completely
2. **TRIAGE** by severity (critical → high → medium → low)
3. **FIX CRITICAL/HIGH** immediately before proceeding
4. **REFACTOR** duplicate code (3+ occurrences)
5. **UPDATE** code with all recommendations
6. **DOCUMENT** deferred medium/low items in TODO.md
7. **VERIFY** fixes by re-running subagent if critical issues found

### §6.6 Quality Verification Checklist

Before marking implementation complete:

- [ ] Directory Structure Validation executed (§6.1)
- [ ] Incremental Code Review executed after major modules (§6.2)
- [ ] Import Path Validation executed (§6.3)
- [ ] Dead Code Elimination executed (if applicable)
- [ ] Comprehensive Review executed (§6.4)
- [ ] All critical issues fixed
- [ ] All high priority issues fixed
- [ ] Security vulnerabilities addressed
- [ ] Duplicate code refactored
- [ ] Medium/low items documented in TODO.md
- [ ] Final quality scores: >80% type hints, >80% docstrings

---

## §7: README Documentation Requirements

### §7.1 Priority Levels

**Priority 1 (MANDATORY - All Implementations):**
- Quick Start (copy-paste commands for common case)
- Execution Flow (with dependency chain and blocking requirements)
- Input/Output Specifications

**Priority 2 (REQUIRED for Complex Implementations):**
- Environment Setup (if non-standard dependencies)
- Troubleshooting (common errors encountered during testing)

**Priority 3 (Optional):**
- Performance Considerations
- Advanced Execution Modes

### §7.2 Required Sections

#### Quick Start
```markdown
## Quick Start

# Run complete pipeline
python problem-statement/ps-001-{name}/scripts/run_all.py

# View results in notebook
jupyter notebook problem-statement/ps-001-{name}/notebooks/results_explorer.ipynb
```

#### Execution Flow

**CRITICAL: Document blocking dependencies:**

```markdown
## Execution Flow

### Stage 1: Extract (BLOCKER for all downstream stages)
python scripts/01_extract_data.py
→ Outputs: data/3_interim/extracted_data.csv

### Stage 2: Clean (BLOCKER for analysis)
python scripts/02_clean_data.py
→ Requires: data/3_interim/extracted_data.csv
→ Outputs: data/4_processed/cleaned_data.csv

### Stage 3: Analyze (Can run after cleaning)
python scripts/03_analyze.py
→ Requires: data/4_processed/cleaned_data.csv

### Stage 4: Visualize (Can run in parallel with Stage 3)
python scripts/04_visualize.py
→ Requires: data/4_processed/cleaned_data.csv

### Notebooks (Run AFTER all stages complete)
jupyter notebook notebooks/results_explorer.ipynb
→ Requires: ALL outputs from Stages 1-4

**Execution Rules:**
- ⛔ BLOCKER: Stage N cannot start until Stage N-1 completes
- ✅ PARALLEL: Stages 3 and 4 can run simultaneously
- ⚠️ NOTEBOOKS: Fail gracefully if prerequisites missing
```

#### Input/Output Specifications

```markdown
## Input/Output Specifications

### Inputs
| File | Location | Format | Required Fields |
|------|----------|--------|----------------|
| Raw disease data | `data/1_raw/disease_data.csv` | CSV | date, disease, case_count, region |

### Outputs
| File | Location | Format | Description |
|------|----------|--------|-------------|
| Cleaned data | `data/4_processed/cleaned_data.csv` | CSV | Standardized disease cases |
```

#### Troubleshooting

**Include actual errors encountered:**

```markdown
## Troubleshooting

### FileNotFoundError: data/3_interim/extracted_data.csv
**Cause**: Trying to run Stage 2 before Stage 1
**Solution**: Run `python scripts/01_extract_data.py` first

### ImportError: No module named 'polars'
**Cause**: Missing dependencies
**Solution**: `uv pip install -r requirements.txt`

### Logs
- ETL logs: `logs/etl/`
- Error logs: `logs/errors/`
```

### §7.3 README Update Process

1. **Execute all dependencies first** to generate required data
2. **Run all scripts/notebooks** to verify actual execution flow
3. **Document dependency chain** (which must run before which)
4. **Capture error messages** encountered during testing
5. **Test instructions** on fresh environment
6. **Verify graceful failures** (notebooks show helpful errors if data missing)

### §7.4 README Verification Checklist

- [ ] Quick Start commands work on fresh environment
- [ ] Execution Flow matches actual code sequence
- [ ] Blocking dependencies clearly marked
- [ ] Notebook prerequisites documented
- [ ] All file paths accurate and exist
- [ ] Environment setup tested
- [ ] Troubleshooting includes actual errors encountered
- [ ] All code snippets syntactically correct
- [ ] Complete execution flow tested: dependencies → notebooks → outputs verified

---

## §8: Verification & Completion

### §8.1 Acceptance Criteria Verification

For each acceptance criterion:
- [ ] Criterion met as specified
- [ ] Evidence documented (test results, outputs, screenshots)
- [ ] Any discrepancies noted with explanations

### §8.2 Extension Verification (If Extended Existing Code)

- [ ] Searched for existing implementations
- [ ] Assessed relevance (domain, audience, workflow)
- [ ] Extended existing only if relevant
- [ ] New code follows established patterns
- [ ] No regressions in existing functionality
- [ ] Shared configurations used consistently
- [ ] Documentation updated with new features

### §8.3 Implementation Verification

- [ ] Problem-statement directory follows Rule 1 naming
- [ ] All code from plan implemented (no stubs)
- [ ] Type hints and docstrings present
- [ ] Error handling implemented
- [ ] Logging implemented
- [ ] Unit tests pass
- [ ] Notebooks executable after prerequisites run
- [ ] README updated with execution flow

### §8.4 Quality Verification

- [ ] All quality subagents executed (see §6.6)
- [ ] Critical/high issues fixed
- [ ] Security vulnerabilities addressed
- [ ] Duplicate code refactored
- [ ] Final quality scores >80%

### §8.5 Documentation Verification

- [ ] README includes Quick Start (Priority 1)
- [ ] README includes Execution Flow with blockers (Priority 1)
- [ ] README includes Input/Output specs (Priority 1)
- [ ] README includes Troubleshooting (Priority 2)
- [ ] README tested on fresh environment

---

## §9: Error Recovery Patterns

### §9.1 Subagent Execution Failures

**Symptom**: Subagent returns error status in handoff file

**Recovery:**
1. Read error details from handoff file
2. Check logs in `logs/errors/` for stack traces
3. **If data issue**: Fix data source, re-run from failed stage
4. **If code issue**: Fix implementation, re-run subagent
5. Document recovery actions in verification report

### §9.2 Partial Data Extraction Failures

**Symptom**: Some data sources load, others fail

**Recovery:**
1. Log successful vs failed sources separately
2. **If minimum threshold met**: Continue with available data, document in handoff
3. **If critical data missing**: Retry failed sources with exponential backoff
4. **If retries exhausted**: Escalate to user with error details

### §9.3 Import Path Mismatches

**Symptom**: ImportError when running code despite imports looking correct

**Recovery:**
1. Execute Import Path Validation subagent (§6.3)
2. Check for hyphen/underscore inconsistencies (`problem-statement-001` vs `problem_statement_001`)
3. Verify `__init__.py` files exist in all package directories
4. Check `PYTHONPATH` includes workspace root

### §9.4 Quality Gate Failures

**Symptom**: Comprehensive Review finds >20 critical/high issues

**Recovery:**
1. **DO NOT** attempt to fix all at once
2. **Categorize** by module/file
3. **Fix module by module**, re-running incremental review after each
4. **Track progress** in checklist
5. **Re-run comprehensive review** only after all modules pass incremental

### §9.5 README Verification Failures

**Symptom**: Following README Quick Start produces errors

**Recovery:**
1. Create fresh virtual environment
2. Step through README instructions one at a time
3. Document exact error message at each failure point
4. Fix instruction causing error
5. Continue from that point
6. Repeat until complete flow succeeds

---

## §10: Final Deliverables Checklist

Before submitting implementation as complete:

### Core Deliverables
- [ ] Problem-statement directory created with correct naming (Rule 1)
- [ ] All code fully implemented (no stubs - Rule 3)
- [ ] Notebooks created and tested (§4.2)
- [ ] README updated with execution flow (§7)

### Quality Deliverables
- [ ] All quality subagents executed (§6)
- [ ] Quality verification checklist complete (§6.6)
- [ ] Critical/high issues fixed
- [ ] Security vulnerabilities addressed

### Verification Deliverables
- [ ] Acceptance criteria verified (§8.1)
- [ ] Extension verification complete if applicable (§8.2)
- [ ] Implementation verification complete (§8.3)
- [ ] Documentation verification complete (§8.5)

### Documentation Deliverables
- [ ] README Quick Start tested and working
- [ ] Execution flow documented with blockers
- [ ] Troubleshooting section includes actual errors
- [ ] Complete execution tested: dependencies → notebooks → outputs

---

## Appendices

### Appendix A: Cross-Reference Map

| Section | Related Sections |
|---------|------------------|
| **Rule 1**: Directory Structure | §8.3 (Implementation Verification) |
| **Rule 2**: Quality Gates | §6 (Quality Gates details) |
| **Rule 3**: Code Fidelity | §4.1 (Code Fidelity), §8.3 (Verification) |
| **Rule 4**: Existing Implementations | §3 (Search Process), §8.2 (Extension Verification) |
| **§6.1**: Directory Validation | §9.3 (Import Path Recovery) |
| **§6.2**: Incremental Review | §9.4 (Quality Gate Recovery) |
| **§7**: README Requirements | §9.5 (README Recovery) |

### Appendix B: Command Quick Reference

```bash
# Activate environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Format code
ruff format problem-statement/ps-{num}-{name}/

# Run tests
pytest problem-statement/ps-{num}-{name}/tests/ -v

# Check logs
tail -f problem-statement/ps-{num}-{name}/logs/errors/error_20260306.log
```

### Appendix C: File Path Template

**Problem-Specific Structure:**
```
problem-statement/ps-{num}-{name}/
├── notebooks/
│   └── {stage}_{description}.ipynb
├── src/
│   ├── data_processing/
│   │   └── {purpose}.py
│   ├── analysis/
│   │   └── {algorithm}.py
│   └── scripts/
│       └── {stage}_{action}.py
├── data/
│   ├── 3_interim/
│   └── 4_processed/
├── results/
│   ├── tables/
│   └── metrics/
├── reports/
│   └── figures/
├── models/
├── tests/
│   └── integration/
│       └── test_{workflow}.py
├── config/
├── logs/
└── README.md
```

**Shared Resources:**
```
shared/
├── src/
│   ├── data_processing/       # Loaders, validators
│   ├── analysis/               # Statistical functions
│   └── visualization/          # Chart generators
├── data/
│   ├── 1_raw/                  # Original data
│   ├── 2_external/             # Reference data
│   └── 3_interim/
│       └── agent_handoffs/
│           └── {agent}_to_{agent}_{timestamp}.json
├── config/                     # Base configuration
└── tests/unit/                 # Tests for shared code
```

---
