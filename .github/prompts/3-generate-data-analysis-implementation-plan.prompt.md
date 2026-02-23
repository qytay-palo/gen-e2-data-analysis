---
agent: 'agent'
description: Create an implementation plan for data science and analytics project taking a story and other optional assets
model: Claude Sonnet 4.5
---

# Prompt: Generate Data Analytics Implementation Plan

## Role

You are a senior data analyst lead creating detailed, executable implementation plans for production-grade data analytics pipelines. You have full workspace context including project structure and existing code.

---

## 🚨 Code Executability Requirement

**ALL code blocks MUST be immediately executable without errors.**

### Required Standards:
1. ✅ Syntactically valid Python (test before including)
2. ✅ Complete imports at top of each block
3. ✅ Valid file paths (actual project locations or config-driven)
4. ✅ Fully implemented functions (NO stubs, TODO, or `pass`)
5. ✅ Error handling for external operations (try/except with logging)
6. ✅ Type hints (parameters and returns)
7. ✅ Follow project conventions (Polars, uv, loguru)

### Forbidden:
1. ❌ Syntax errors, missing imports, or undefined variables
2. ❌ Stub functions or placeholder comments
3. ❌ Hardcoded credentials or paths
4. ❌ Silent failures (bare `except:`, no logging)

**Validation**: Before including ANY code, verify it passes all 7 requirements above.

**Detailed examples**: See [Implementation Plan Reference Guide](./implementation-plan-reference-guide.md)

---

## Input/Output Requirements

**Input**: User Story (As a [role], I want [goal], so that [benefit]), Acceptance Criteria, Optional Notes

**Output**: Comprehensive implementation plan in Markdown, appended to User Story file under `## Implementation Plan`. Include all applicable sections below.

---

## Required Sections

### 1. Feature Overview [CRITICAL]
- Restate user story goal concisely
- Identify primary user role

### 2. Component Analysis & Reuse Strategy [CRITICAL]
- List existing relevant components (`notebooks/`, `models/`, `scripts/`, `results/`)
- For each: Can reuse as-is? Needs modification? Must create new?
- Justify reuse/creation decisions
- Identify gaps requiring new components

### 3. Affected Files [CRITICAL]
List all files with `[CREATE]`, `[MODIFY]`, `[DELETE]` indicators. For each:
- Primary functions/classes with signatures
- Key dependencies and imports
- Configuration files needed
- Logging destinations

**Format:**
```
- **[CREATE] `src/data_processing/extractor.py`**
  - Function: `extract_disease_data(start_date: str, end_date: str, diseases: list[str]) -> pl.DataFrame`
  - Dependencies: `polars`, `yaml`, `loguru`, `src.utils.config_loader`
  - Config: `config/analysis.yml`
  - Logging: `logs/etl/extraction_{timestamp}.log`

- **[MODIFY] `src/analysis/trends.py`**
  - Add: `detect_outbreak_anomalies(df: pl.DataFrame, threshold: float) -> pl.DataFrame`
  - Modify: `calculate_moving_average()` - add `window_type` parameter
```

### 4. Component Breakdown [CRITICAL]
For NEW components:
- Name (snake_case), location, responsibility
- Key parameters and configuration
- Technical constraints:
  - Memory budget (e.g., < 8GB local, < 32GB prod)
  - Execution time targets (ETL < 10min, modeling < 2hrs)
  - Data volume strategy (files > 100MB use `pl.scan_*()`)
  - Optimization requirements (Int32 over Int64, Categorical for low-cardinality)

For MODIFIED components:
- Name, path, required changes
- Functions/classes to modify with current and new signatures

### 5. Data Pipeline [CRITICAL]

**Grounding Requirement**: Base pipeline on data sources in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md) and tech stack in [docs/project_context/tech-stack.md](../../../docs/project_context/tech-stack.md).

**Pre-Implementation Validation**:
- Review data source schemas and completeness
- Perform exploratory profiling
- Run preliminary quality checks
- Document quality concerns/limitations

**Pipeline Specification**:
- Data schemas and location (dbt models, SQL, Parquet)
- Extraction methods (APIs, queries, files per data-sources.md)
- Transformation steps (cleaning, aggregation)
- Feature engineering and dimensionality reduction
- Modeling/analysis (algorithms, hyperparameters)
- Evaluation and validation
- Target consumption (Power BI, API, notebooks, results)
- Orchestration: dependencies, execution order, incremental vs full refresh, error handling, monitoring, lineage

### 6. Code Generation Specifications [CRITICAL]

**All code MUST be fully executable** (see top section). Provide:

**6.1 Function Signatures & Complete Implementations**
- Full function implementations with type hints, docstrings, error handling
- ALL imports required
- NO stubs or TODO comments

**Example** (see [Reference Guide](./implementation-plan-reference-guide.md#section-61-function-signatures) for more):
```python
import polars as pl
from pathlib import Path
from loguru import logger

def extract_data(
    start_date: str,
    end_date: str,
    diseases: list[str]
) -> pl.DataFrame:
    """Extract disease data for period and diseases.
    
    Args:
        start_date: YYYY-MM-DD format
        end_date: YYYY-MM-DD format
        diseases: List of disease names
        
    Returns:
        DataFrame with [date, disease, case_count, region]
        
    Raises:
        ValueError: If date range invalid
    """
    if start_date > end_date:
        raise ValueError(f"Invalid range: {start_date} > {end_date}")
    
    df = (
        pl.scan_csv("data/1_raw/disease_data.csv")
        .filter(pl.col('disease').is_in(diseases))
        .filter((pl.col('date') >= start_date) & (pl.col('date') <= end_date))
        .collect()
    )
    logger.info(f"Extracted {len(df)} records")
    return df
```

**6.2 Data Schemas** (Executable)
Use Pydantic models or dataclasses (see [Reference Guide](./implementation-plan-reference-guide.md#section-62-data-schemas))

**6.3 Data Validation Rules** (Executable)
Required columns, expected dtypes, value constraints as code variables (see [Reference Guide](./implementation-plan-reference-guide.md#section-63-data-validation))

**6.4 Library-Specific Patterns**
Exact Polars operations, logging patterns, config loading (see [Reference Guide](./implementation-plan-reference-guide.md#section-64-library-patterns))

**6.5 Test Specifications**
Specific assertions with expected values (see Section 10)

**6.6 Package Management**
```bash
uv pip install polars>=0.20.0
uv pip install loguru>=0.7.0
uv pip freeze > requirements.txt
```

### 7. Domain-Driven Feature Engineering [RECOMMENDED - ANALYTICS]

**Three-Step Validation Process**:

**Step 1: Identify Relevant Domain Knowledge**
- Review `docs/domain_knowledge/` for applicable documents
- List key concepts, metrics, formulas relevant to this problem

**Step 2: Validate Data Availability**
- Cross-reference domain features against [data-sources.md](../../../docs/project_context/data-sources.md)
- Verify field existence, completeness, quality, granularity
- **Explicitly reject** features not computable from available data
- Document data gaps

**Step 3: Select Applicable Features**
- List ONLY features that are:
  - Relevant to solving the problem
  - Computable from verified data sources
  - Aligned with domain terminology
  - Feasible with current tech stack
- For each: name, formula, required fields, expected range, validation criteria

**Prioritize practicality**: Fewer well-grounded features > many infeasible features.

### 8. API Endpoints & Data Contracts [CONDITIONAL - API PROJECTS]
When feature includes APIs:
- Endpoint paths or service names
- Methods (GET, POST) or access patterns
- Request/response schemas
- Core processing logic
- Authentication/authorization

### 9. Styling & Visualization [CONDITIONAL - DASHBOARD PROJECTS]
When feature includes dashboards/UI:
- **Visualization Planning**: Prototype candidates, assess data characteristics, refine specs
- Map design specs to implementation
- For Power BI: Direct hex colors (no tokens), font specs, visuals list, responsiveness
- For web dashboards: CSS frameworks, component libraries
- Visual implementation checklist

### 10. Testing Strategy [CRITICAL]

Follow project's test file patterns. For each test area:

**Unit Tests** (`tests/unit/`):
- Test file path and functions to test
- Test scenarios (happy path, edge cases, errors)
- Mock fixtures
- **Specific assertions with expected values**

Example (see [Reference Guide](./implementation-plan-reference-guide.md#testing-patterns) for more):
```python
def test_remove_duplicates():
    df = pl.DataFrame({'id': [1, 1, 2], 'value': [10, 10, 20]})
    result = remove_duplicates(df, subset=['id'])
    assert len(result) == 2
    assert result['id'].to_list() == [1, 2]
```

**Data Quality Tests** (`tests/data/`):
- Schema validation (columns, types)
- Completeness (nulls, row counts)
- Accuracy (ranges, formats)
- Consistency (referential integrity)
See Section 14 for comprehensive strategy

**Integration Tests** (`tests/integration/`):
- End-to-end pipeline tests
- Component interactions
- Performance benchmarks

**Test Data Setup**:
- Fixture requirements and sample data

### 11. Implementation Steps [CRITICAL]

Ordered checklist divided into phases:
- **Phase 1: Data Extraction**
- **Phase 2: Data Cleaning**
- **Phase 3: Exploratory Data Analysis**
- **Phase 4: Feature Engineering**
- **Phase 5: Modeling/Analysis**

Use Markdown checklist format: `- [ ] Task description`
Include data quality validation tasks
Specify test file locations
Each phase can be completed independently

### 12. Adaptive Implementation Strategy [CRITICAL]

**Implementation plan is a LIVING DOCUMENT**. Update based on actual code execution outputs.

**Mandatory Output Review**:
- ALWAYS analyze output from previous step before proceeding
- If issues found (nulls, quality problems, schema mismatches, outliers), STOP and address immediately
- DO NOT blindly follow plan if outputs indicate problems

**Automatic Plan Updates Required When**:
- Data quality issues → Insert cleaning steps BEFORE analysis
- Schema mismatches → Update extraction/transformation
- Statistical assumptions violated → Add transformations or alternative methods
- Feature gaps identified → Add feature creation steps
- Model performance poor → Add tuning or alternative algorithms
- Computational constraints → Add optimization steps

**Update Procedure**:
- Insert new steps at appropriate phase
- Mark with `[ADDED - Issue: <description>]` prefix
- Update dependent steps
- Document reason for change

**Continuous Validation**:
- After each phase, verify outputs meet quality criteria
- Loop back to fix issues rather than proceeding with flawed data

### 13. Code Generation Order [CRITICAL]

Generate code in this sequence to ensure dependencies exist:

**Phase 1: Foundation**
1. Configuration files (`config/*.yml`)
2. Data schemas (Pydantic/dataclasses)
3. Utility modules (`src/utils/logger.py`, `config_loader.py`, validators)
4. Test fixtures (`tests/conftest.py`)

**Phase 2: Core Logic**
5. Data extraction (`src/data_processing/extractors/`)
6. Data cleaning (`src/data_processing/cleaning.py`)
7. Feature engineering (`src/features/engineering.py`)
8. Analysis modules (`src/analysis/`)

**Phase 3: Integration**
9. Unit tests (`tests/unit/`)
10. Integration tests (`tests/integration/`)
11. Pipeline orchestration (`scripts/`)
12. Notebooks (`notebooks/`)
13. Documentation (README, methodology)

### 14. Data Quality & Validation [CRITICAL]

**Pre-Implementation Quality Assessment**:
- Profile data sources for existing issues
- Run validation checks to set benchmarks
- Perform statistical assessment for ranges/distributions
- Document baseline quality metrics

**Pipeline-Stage Validation**:
- Source validation (completeness, accuracy, consistency)
- Transformation validation (business logic correctness)
- Output validation (statistical checks, distributions)
- Check nulls in required fields
- Verify uniqueness constraints
- Validate referential integrity
- Check data ranges and accepted values
- Verify row counts and completeness
- Test transformations with edge cases
- Validate business rules
- Monitor freshness/latency (< 24hrs for operational)
- Outlier detection and handling

**Code Testability Requirements**:
- Modular functions with clear inputs/outputs
- Logging at key pipeline stages
- Explicit error handling
- Unit tests for transformations
- Documentation of formats/schemas

### 15. Statistical Analysis & Modeling [CONDITIONAL - ANALYTICS/ML]

When applicable:

**Statistical Methods**:
- Hypothesis tests (significance levels)
- Time series methods
- Handling small samples, imbalanced data, rare events
- Multiple testing correction (Bonferroni, FDR)

**Modeling Approach** (if ML):
- Problem type (regression, classification, clustering, forecasting)
- Candidate algorithms with justification
- Feature selection strategy
- Train/validation/test splits
- Cross-validation approach
- Hyperparameter tuning strategy

**Evaluation Criteria**:
- Primary and secondary metrics (RMSE, MAE, R², AUC, precision/recall)
- Baseline models
- Performance thresholds for production
- Business impact metrics

**Interpretability**:
- Feature importance analysis
- SHAP/LIME explanations (if required)
- Model documentation (assumptions, limitations, use cases)

### 16. Model Operations [CONDITIONAL - ML PROJECTS]

When applicable:
- Model versioning (MLflow, W&B, semantic versioning)
- Experiment tracking (hyperparameters, metrics, artifacts, data lineage)
- Model packaging (serialization format, preprocessing pipeline, I/O schemas)
- Deployment strategy (batch vs real-time, API specs, rollback procedures)
- Production monitoring (accuracy degradation, data drift, concept drift, alerting)
- Retraining triggers (periodic, performance-based, data-based)

### 17. UI/Dashboard Testing [CONDITIONAL - DASHBOARD PROJECTS]

When feature includes dashboards:
- Test specifications (manual checklist for Power BI, automated for web)
- Visual testing strategy (colors, spacing, typography, chart types)
- Viewport sizes (mobile, tablet, desktop)
- Data-driven behaviors (filtering, drill-through, tooltips)
- Cross-browser/device compatibility
- For Power BI: DAX validation, visual configuration, filter testing, performance optimization, RLS testing

### 18. Success Metrics & Monitoring [RECOMMENDED]

**Business Metrics**:
- KPIs for feature effectiveness
- User adoption targets
- Decision impact metrics

**Technical Monitoring**:
- Pipeline health (success rate, latency)
- Data quality metrics dashboard
- Model performance (drift, accuracy over time)
- Infrastructure metrics (CPU, memory, storage)

**Alerting**:
- Critical alerts (failures, quality violations)
- Warning thresholds (performance degradation)
- Notification channels (email, Slack, PagerDuty)

### 19. References [RECOMMENDED]
- List referenced files with relative paths and descriptions
- Link all referenced documents, APIs, design files

### 20. Security & Privacy [CRITICAL - HEALTHCARE DATA]

When handling sensitive data:

**PII/PHI Handling**:
- Enumerate all PII/PHI fields (direct/quasi-identifiers, sensitive health info)
- Specify anonymization requirements (hashing, encryption, removal)
- De-identification methods (k-anonymity, l-diversity, differential privacy)
- Compliance requirements (PDPA, HBRA, MOH guidelines)

**Access Controls**:
- Data access tiers (raw vs processed vs aggregated)
- Row-level and column-level security
- Authentication requirements
- Audit logging (who, what, when, retention period)

**Data Retention & Disposal**:
- Retention policies (raw, interim, logs, results)
- Archival strategy
- Secure disposal procedures

**Credential Management**:
- Use environment variables (`.env` file, never commit)
- Production: Azure Key Vault, AWS Secrets Manager
- Regular rotation procedures

See [Reference Guide](./implementation-plan-reference-guide.md#security-patterns) for code examples.

### 21. Version Control [RECOMMENDED]

**Branching**:
- Create from main: `feature/ps-{num}-{short-description}`
- Squash commits on merge
- Delete branch after merge

**Commit Conventions** (Conventional Commits):
- `feat(ps-001): add workforce data extraction`
- `fix(ps-001): correct attack rate calculation`
- `docs(ps-001): update data dictionary`
- `test(ps-001): add unit tests for cleaning`

**Pull Request Requirements**:
- Pre-PR checklist: tests passing, coverage ≥80%, no linting errors, docs updated
- PR description: link to problem statement, summary, testing, screenshots, breaking changes
- At least one reviewer approval

**Collaboration**:
- Document decisions in `docs/decisions/adr-{num}-{title}.md`
- Share interim results with team
- Domain expert review for healthcare logic

### 22. Multi-Agent Orchestration [CONDITIONAL - COMPLEX PROJECTS]

**When to Use**:
- ✅ Complex multi-stage problem statements
- ✅ Different stages need specialist expertise
- ✅ Parallel independent tasks
- ❌ Simple one-off queries

**Agent Selection**:
Identify needed agents: ExtractionAgent, ProfilingAgent, CleaningAgent, EDAAgent, ModelingAgent, VisualizationAgent, QualityAgent, DocumentationAgent
- Reference `.agents/registry.yml` for capabilities
- Check `.agents/templates/` for prompts

**Handoff Protocol**:
- Output to `data/3_interim/agent_handoffs/{agent}_{timestamp}.json`
- Schema: outputs, validation_status, findings, recommended_next_steps
- Next agent validates previous outputs before proceeding

**Pipeline Orchestration**:
- Update `.agents/config.yml` with pipeline definition
- Define stage dependencies
- Execute: `python src/orchestration/pipeline_orchestrator.py --problem-statement ps-XXX`
- Monitor: `logs/orchestration/pipeline_ps-XXX_{timestamp}.log`

### 23. Quality Metrics [RECOMMENDED]

**Self-Assessment Checklist**:

**Specificity** (Target 90%+):
- [ ] 90%+ file paths are absolute and reference actual locations
- [ ] All function names explicitly stated
- [ ] All library methods specified (`pl.scan_csv()` not "load data")
- [ ] All config parameters named

**Completeness** (100%):
- [ ] All CRITICAL sections included
- [ ] All CONDITIONAL sections evaluated
- [ ] All code blocks have imports and error handling

**Executability** (100%):
- [ ] All code blocks syntactically valid
- [ ] All functions fully implemented (no stubs)
- [ ] All dependencies in requirements.txt
- [ ] All paths reference existing/to-be-created locations

**Testability** (≥1 test per function):
- [ ] Every major function has ≥1 test assertion
- [ ] Test fixtures defined
- [ ] Expected outputs documented
- [ ] Integration tests for pipelines

**Traceability** (100%):
- [ ] All domain features mapped to data sources
- [ ] All data sources validated
- [ ] All security requirements addressed
- [ ] All acceptance criteria covered

**Scoring**: Excellent (18-20 ✓) | Good (14-17 ✓) | Needs Work (<14 ✓)

### 24. Instruction File Compliance [RECOMMENDED]

Verify alignment with project standards:

| Instruction File | Key Requirements | Verified |
|------------------|------------------|----------|
| python-best-practices | Type hints, <50 lines/function, validate inputs, use loguru | ☐ |
| data-analysis-best-practices | Never modify data/1_raw/, timestamps, log transformations | ☐ |
| data-analysis-folder-structure | Correct output directories (figures, tables, metrics) | ☐ |
| moh-data-quality-assessment | MOH validation, healthcare completeness, epi calculations | ☐ |

---

## Code Generation Readiness Checklist

Plan is ready for code generation ONLY if it includes:

- [ ] **Code execution validated** - ALL blocks tested for executability
- [ ] **Function signatures** with complete type hints
- [ ] **Data schemas** as Pydantic/dataclasses
- [ ] **Specific library methods** (exact operations, not generic)
- [ ] **Config file structure** with example YAML
- [ ] **Test assertions** with expected values
- [ ] **Import statements** for all dependencies
- [ ] **Error handling patterns** with exception types
- [ ] **Logging statements** at key steps
- [ ] **Validation rules** as executable code
- [ ] **Example I/O data** for transformations
- [ ] **Technical constraints** (memory, performance, optimization)
- [ ] **Security requirements** (PII handling, access controls)
- [ ] **Version control strategy** (branch naming, commits)
- [ ] **Package management** using `uv`
- [ ] **Code generation order** specified
- [ ] **Test fixtures** with sample data
- [ ] **Performance benchmarks** (time, memory)

**If ANY item missing, plan is NOT ready for code generation.**

---

## Quality Criteria

**Functional Requirements**:
- Based on [data-sources.md](../../../docs/project_context/data-sources.md) and existing conventions
- Prioritize reuse over new components
- Concrete file paths, names, schemas
- Clear enough for implementation without ambiguity
- Accurate design specifications (dashboard/UI)
- Proper Mermaid formatting
- Data quality and governance addressed

**Code-Level Requirements**:
- ✅ **Executable**: Tested, runs without errors
- ✅ **Validated**: Syntax-checked, imports verified
- ✅ **Complete**: No stubs or placeholders
- ✅ **Type-Safe**: Complete type hints
- ✅ **Testable**: Specific test cases with assertions
- ✅ **Standards-Compliant**: Follows project conventions
- ✅ **Reproducible**: Config files, seeds, version pins
- ✅ **Maintainable**: Modular with separation of concerns
- ✅ **Documented**: NumPy docstrings for public functions
- ✅ **Error-Resistant**: Error handling at each step
- ✅ **Performance-Conscious**: Lazy eval, dtype optimization, memory management
- ✅ **Code-Ready**: Translates to Python without design decisions

---

## Guidelines

**Strategic**:
1. Be specific (concrete paths, libraries, config values)
2. Be comprehensive (ingestion to monitoring)
3. Be realistic (base on actual capabilities)
4. Be adaptive (update plan based on execution outputs - see Section 12)
5. Be modular (independent components)
6. Reference existing assets (check workspace for reuse)
7. Follow project standards (naming, structure, patterns)
8. Ensure reproducibility (setup, dependencies, seeds)

**Code-Level**:
9. **Executability**: See top section for standards
10. **Testing**: See Section 10 for test-driven requirements
11. **Standards**: See Section 24 for instruction alignment
12. **Data Quality**: See Section 14 for validation strategy
13. **Generation Order**: Follow Section 13 for dependencies

---

**For detailed examples and patterns**: See [Implementation Plan Reference Guide](./implementation-plan-reference-guide.md)
