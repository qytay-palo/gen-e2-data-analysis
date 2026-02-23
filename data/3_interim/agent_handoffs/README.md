# Agent Handoff Protocol

## Overview
The handoff protocol defines how agents communicate context, outputs, and findings to downstream agents in the pipeline.

## Handoff File Location
```
data/3_interim/agent_handoffs/{source_agent}_to_{target_agent}_{timestamp}.json
```

## Schema Definition

### Required Fields
All handoff files must include these fields:

```json
{
  "agent_name": "string",           // Name of the agent creating this handoff
  "timestamp": "string",             // Format: YYYYMMDD_HHMMSS
  "stage": "integer",                // Pipeline stage number (0-10)
  "problem_statement": "string",     // Problem statement number (e.g., "001")
  "outputs": {                       // All files created by this agent
    "code": "string",                // Path to generated Python code
    "data": "string",                // Path to data outputs (if any)
    "logs": "string",                // Path to log files
    ...                              // Agent-specific outputs
  },
  "validation_status": "string",     // "passed" | "failed" | "warning"
  "findings": {},                    // Agent-specific findings (flexible structure)
  "recommended_next_step": "string"  // Next agent name or action
}
```

### Optional but Recommended Fields
```json
{
  "execution_time_seconds": 123.45,
  "memory_usage_mb": 245.3,
  "warnings": ["list", "of", "warnings"],
  "errors": ["list", "of", "errors"],
  "quality_metrics": {},
  "metadata": {}
}
```

## Agent-Specific Schemas

### ExtractionAgent Handoff
```json
{
  "agent_name": "ExtractionAgent",
  "timestamp": "20260223_141530",
  "stage": 2,
  "problem_statement": "001",
  "outputs": {
    "code": "src/problem-statement-001/wave-1/01_extract_data.py",
    "data": "data/3_interim/extracted_data_20260223_141530.csv",
    "logs": "logs/etl/extraction_20260223_141530.log"
  },
  "validation_status": "passed",
  "data_characteristics": {
    "rows": 12345,
    "columns": 45,
    "memory_mb": 23.5,
    "schema": {
      "date": "Date",
      "disease": "Utf8",
      "case_count": "Int32",
      ...
    }
  },
  "findings": {
    "data_sources_accessed": ["kaggle:moh-disease-surveillance"],
    "missing_columns": [],
    "unexpected_columns": ["extra_field"],
    "warnings": ["Column 'extra_field' not in expected schema"]
  },
  "recommended_next_step": "profiling"
}
```

### ProfilingAgent Handoff
```json
{
  "agent_name": "ProfilingAgent",
  "timestamp": "20260223_142015",
  "stage": 3,
  "problem_statement": "001",
  "outputs": {
    "code": "src/problem-statement-001/wave-1/02_profile_data.py",
    "report": "results/tables/problem-statement-001/data_quality_report.md",
    "metrics": "results/metrics/problem-statement-001/quality_metrics.json"
  },
  "validation_status": "passed",
  "data_quality_assessment": {
    "overall_score": 87.5,
    "completeness_score": 92.1,
    "validity_score": 83.2,
    "consistency_score": 88.0,
    "critical_issues_count": 0,
    "warnings_count": 3
  },
  "findings": {
    "missing_values_threshold_exceeded": false,
    "columns_with_missing_values": {
      "age_group": {"count": 123, "percentage": 1.0},
      "postal_code": {"count": 456, "percentage": 3.7}
    },
    "outliers_detected": true,
    "outlier_columns": ["case_count"],
    "schema_issues": [],
    "recommended_cleaning_actions": [
      "impute_missing_values: ['age_group', 'postal_code']",
      "handle_outliers: ['case_count'] (IQR method)",
      "standardize_categories: ['disease_name']"
    ]
  },
  "recommended_next_step": "cleaning"
}
```

### CleaningAgent Handoff
```json
{
  "agent_name": "CleaningAgent",
  "timestamp": "20260223_142530",
  "stage": 4,
  "problem_statement": "001",
  "outputs": {
    "code": "src/problem-statement-001/wave-1/03_clean_data.py",
    "data": "data/4_processed/cleaned_data.csv",
    "logs": "logs/etl/cleaning_20260223_142530.log"
  },
  "validation_status": "passed",
  "cleaning_summary": {
    "transformations_applied": [
      "Imputed 123 missing values in 'age_group' using mode",
      "Imputed 456 missing values in 'postal_code' using forward-fill",
      "Removed 45 outliers in 'case_count' (>3 IQR)",
      "Standardized 234 disease names to MOH classification"
    ],
    "rows_before": 12345,
    "rows_after": 12300,
    "rows_removed": 45,
    "rows_removed_percentage": 0.36
  },
  "findings": {
    "data_quality_improved": true,
    "quality_score_before": 87.5,
    "quality_score_after": 95.2,
    "critical_issues_resolved": 0,
    "warnings_resolved": 2
  },
  "recommended_next_step": "eda"
}
```

### EDAAgent Handoff
```json
{
  "agent_name": "EDAAgent",
  "timestamp": "20260223_143015",
  "stage": 5,
  "problem_statement": "001",
  "outputs": {
    "code": "src/problem-statement-001/wave-2/04_exploratory_analysis.py",
    "figures": [
      "reports/figures/problem-statement-001/01_univariate_distributions.png",
      "reports/figures/problem-statement-001/02_correlation_matrix.png",
      "reports/figures/problem-statement-001/03_temporal_patterns.png"
    ],
    "summary": "results/tables/problem-statement-001/eda_summary.csv",
    "notebook": "notebooks/1_exploratory/problem-statement-001_eda.ipynb"
  },
  "validation_status": "passed",
  "analysis_summary": {
    "variables_analyzed": 25,
    "figures_generated": 8,
    "statistical_tests_performed": 15,
    "significant_relationships_found": 12
  },
  "findings": {
    "key_insights": [
      "Strong seasonal pattern in dengue cases (seasonal strength: 0.85)",
      "Negative correlation between healthcare capacity and mortality (r=-0.68, p<0.001)",
      "Significant regional disparities in workforce distribution (ANOVA p<0.001)"
    ],
    "temporal_patterns": {
      "seasonality_detected": true,
      "trend": "increasing",
      "cyclical_period_months": 12
    },
    "recommended_features": [
      "month_of_year",
      "lagged_cases_1_month",
      "lagged_cases_3_months",
      "capacity_utilization_rate",
      "region_fixed_effects"
    ],
    "modeling_recommendations": [
      "Use SARIMAX for seasonal forecasting",
      "Consider interaction terms: capacity * demand",
      "Include regional fixed effects for spatial heterogeneity"
    ]
  },
  "recommended_next_step": "modeling"
}
```

### ModelingAgent Handoff
```json
{
  "agent_name": "ModelingAgent",
  "timestamp": "20260223_144030",
  "stage": 7,
  "problem_statement": "001",
  "outputs": {
    "code": "src/problem-statement-001/wave-3/05_modeling.py",
    "models": "models/problem-statement-001/",
    "metrics": "results/metrics/problem-statement-001/model_performance.json",
    "notebook": "notebooks/2_analysis/problem-statement-001_modeling.ipynb"
  },
  "validation_status": "passed",
  "modeling_summary": {
    "models_trained": 3,
    "best_model": "SARIMAX",
    "best_model_path": "models/problem-statement-001/sarimax_model.pkl"
  },
  "findings": {
    "model_performance": {
      "SARIMAX": {"RMSE": 12.34, "MAE": 8.56, "MAPE": 5.2},
      "Prophet": {"RMSE": 15.67, "MAE": 10.23, "MAPE": 6.8},
      "XGBoost": {"RMSE": 18.90, "MAE": 12.45, "MAPE": 8.1}
    },
    "feature_importance": {
      "lagged_cases_1_month": 0.45,
      "month_of_year": 0.28,
      "capacity_utilization_rate": 0.15,
      "region": 0.12
    },
    "validation_strategy": "time_series_cross_validation",
    "forecast_horizon_months": 6
  },
  "recommended_next_step": "visualization"
}
```

## Validation Rules

### File Existence Checks
Before creating a handoff, verify all output files exist:
```python
import os
from pathlib import Path

def validate_outputs(outputs: dict) -> bool:
    """Validate that all output files exist."""
    for output_type, file_path in outputs.items():
        if isinstance(file_path, str):
            if not Path(file_path).exists():
                raise FileNotFoundError(f"{output_type} file not found: {file_path}")
        elif isinstance(file_path, list):
            for fp in file_path:
                if not Path(fp).exists():
                    raise FileNotFoundError(f"{output_type} file not found: {fp}")
    return True
```

### Validation Status Rules
- **"passed"**: All validation gates met, proceed to next agent
- **"warning"**: Non-critical issues found, can proceed with caution
- **"failed"**: Critical issues, do NOT proceed to next agent

### Required Next Steps
Map recommended_next_step to valid agent names:
- `"profiling"` → ProfilingAgent
- `"cleaning"` → CleaningAgent
- `"eda"` → EDAAgent
- `"modeling"` → ModelingAgent
- `"visualization"` → VisualizationAgent
- `"quality_check"` → QualityAgent
- `"documentation"` → DocumentationAgent
- `"re_extraction"` → ExtractionAgent (retry)
- `"complete"` → Pipeline finished

## Retention Policy
- Handoff files are retained for 30 days (configurable in `.agents/config.yml`)
- Archived to `data/3_interim/agent_handoffs/archive/` after retention period
- Can be used for debugging and auditing pipeline execution

## Usage Example

```python
import json
from datetime import datetime
from pathlib import Path

def create_handoff(
    agent_name: str,
    stage: int,
    problem_statement: str,
    outputs: dict,
    findings: dict,
    next_step: str
) -> Path:
    """Create a handoff file for the next agent."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    handoff_data = {
        "agent_name": agent_name,
        "timestamp": timestamp,
        "stage": stage,
        "problem_statement": problem_statement,
        "outputs": outputs,
        "validation_status": "passed",
        "findings": findings,
        "recommended_next_step": next_step
    }
    
    # Validate outputs exist
    validate_outputs(outputs)
    
    # Create handoff file
    next_agent_name = next_step
    handoff_file = Path(
        f"data/3_interim/agent_handoffs/"
        f"{agent_name.lower()}_to_{next_agent_name}_{timestamp}.json"
    )
    
    with open(handoff_file, 'w') as f:
        json.dump(handoff_data, f, indent=2)
    
    return handoff_file
```

## See Also
- [Multi-Agent Config](../.agents/config.yml)
- [Agent Registry](../.agents/registry.yml)
- [Orchestration Utilities](../src/orchestration/)
