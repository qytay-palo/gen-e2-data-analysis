# Domain Knowledge: Team Lead Expertise for Workforce Analytics Delivery

## Overview

This file captures the delivery and governance perspective of the team lead responsible for sign-off on the workforce analytics backlog. The team lead is the primary stakeholder for PS-001 and a sign-off stakeholder for PS-002. Their focus is trust, auditability, reusability, and adherence to the documented local-first analytics architecture.

## Related Problem Statements

- [Problem Statement PS-001 - Workforce Data Foundation](../objectives/problem_statements/ps-001-workforce-data-foundation.md)
- [Problem Statement PS-002 - Workforce Trends Dashboard](../objectives/problem_statements/ps-002-workforce-trends-dashboard.md)

## Related Stakeholders

- **Team Lead**: Needs confidence that the data foundation is reproducible, validated, and safe for downstream analytics.
- **MOH Workforce Planners**: Depend on the team lead to approve that dashboards are built on trusted processed datasets.

## Key Concepts and Terminology

### Data Contract
**Definition**: A stable, documented agreement on file path, schema, and column meaning that downstream work can depend on.
**Relevance**: PS-001 establishes the shared contract at `shared/data/4_processed/workforce_clean.parquet`.
**Example**: Downstream dashboards expect `year`, `sector`, `count`, and `profession` with consistent dtypes.

### Auditability
**Definition**: The ability to trace what data was extracted, what transformations were applied, and what records were altered or dropped.
**Relevance**: Required for stakeholder trust and for debugging downstream discrepancies.
**Example**: A cleaning audit YAML documents dropped null rows and removed duplicates.

### Reusable Component Boundary
**Definition**: A shared implementation surface designed to be reused across problem statements without duplicating logic.
**Relevance**: The SharePoint connector and the appendable Dash tab list are both reusable boundaries.
**Example**: PS-003 and PS-005 can append tabs without changing the PS-002 core app structure.

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Extraction completeness | Share of required source files successfully downloaded | downloaded files / 4 | 0 to 1 | Validate PS-001 extraction readiness | source file inventory |
| Schema conformance rate | Share of files containing required fields | conforming files / 4 | 0 to 1 | Validate the shared data contract | file schema metadata |
| Duplicate row count | Number of exact duplicate records removed | count of duplicate rows | 0+ | Measure cleaning impact | all raw rows |
| Dashboard startup time | Seconds from app launch to first render | wall-clock seconds | under 3 seconds target | Validate PS-002 usability | dashboard runtime logs |

## Feature Engineering Guidance

### Common Features for Workforce Delivery Governance

#### Data lineage attributes
- **Extraction timestamp**:
  - **Description**: Time a raw file was downloaded.
  - **Calculation**: Captured during extraction and logged.
  - **Interpretation**: Supports freshness and traceability checks.
  - **Use Cases**: Audit, rerun comparison, stakeholder sign-off.
  - **Example**: `2026-04-22T10:15:00+08:00` recorded for `doctors.csv`.

#### Canonical data typing
- **Standardized dtype map**:
  - **Description**: Target types required by the shared Parquet contract.
  - **Calculation**: `year` and `count` cast to `Int32`; `sector` and `profession` cast to categorical/string-enum equivalent.
  - **Interpretation**: Ensures consistent downstream behavior.
  - **Use Cases**: Trend analysis, dashboard filtering, forecasting.
  - **Example**: `sector` standardized to a single category set before export.

## Data Quality Considerations

### Missing critical fields
- **Description**: Null `year` or `count` rows undermine temporal analysis and aggregation correctness.
- **Impact**: Causes invalid trends, filtering errors, or aggregation failures.
- **Detection**: Null count per required field during profiling.
- **Mitigation**: Drop these rows and log them in the audit output.

### Silent schema drift
- **Description**: Source files may change header names or data types across refreshes.
- **Impact**: Breaks ingestion or creates inconsistent combined datasets.
- **Detection**: Per-file schema validation against required logical columns.
- **Mitigation**: Explicit schema checks and standardization rules before combine.

## Analytical Methodologies

### Delivery-readiness validation
- **Application**: Use before downstream PS work starts.
- **Assumptions**: Data source and file inventory are stable enough for the current delivery.
- **Implementation Notes**: Validate extraction, schema, quality, and final output path as separate lifecycle checkpoints.
- **Interpretation**: A PS is ready for sign-off only when all checkpoints pass and are logged.

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- Building downstream analysis directly from raw CSVs: this bypasses the shared contract and makes results non-reproducible.
- Coupling dashboard tabs to the main app file: this makes later demo extensions harder to append safely.

### Best Practices
- Keep raw files immutable and write all standardization into explicit processed outputs.
- Require every downstream feature to depend on the shared Parquet contract rather than bespoke local tables.

## References and Sources

### Authoritative Sources
- **Project Problem Statements**: Internal project documents defining scope, success criteria, and delivery contracts.
- **Project Tech Stack**: Internal standards for Polars, Dash, YAML config, and logging.

## Cross-References

### Related Domain Knowledge Files
- [workforce-analytics-terminology-glossary](workforce-analytics-terminology-glossary.md) - Shared vocabulary used in ingestion and dashboard stories.
- [workforce-headcount-metrics-kpis](workforce-headcount-metrics-kpis.md) - Metrics referenced in acceptance criteria and validation.

### Related Data Dictionary Entries
- [01-workforce-sharepoint](../data_dictionary/01-workforce-sharepoint.md) - Source file inventory and expected common fields.

## Metadata

**Created**: 2026-04-22
**Last Updated**: 2026-04-22
**Updated By**: GitHub Copilot
**Update Reason**: Initial stakeholder knowledge capture for PS-001 and PS-002 user story generation.
**Version**: 1.0

## Notes

This stakeholder view emphasizes delivery risk reduction, stable interfaces, and auditability rather than analytical novelty.