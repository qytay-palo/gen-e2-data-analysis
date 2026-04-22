# Domain Knowledge: Workforce Analytics Terminology Glossary

## Overview

This glossary defines the common workforce analytics language needed for the current project scope. It supports consistent interpretation across data foundation and dashboard work and is intentionally limited to concepts grounded in the documented annual workforce headcount data.

## Related Problem Statements

- [Problem Statement PS-001 - Workforce Data Foundation](../objectives/problem_statements/ps-001-workforce-data-foundation.md)
- [Problem Statement PS-002 - Workforce Trends Dashboard](../objectives/problem_statements/ps-002-workforce-trends-dashboard.md)

## Related Stakeholders

- **Team Lead**: Uses these definitions to enforce a stable data contract.
- **MOH Workforce Planners**: Use these definitions to interpret dashboard metrics consistently.

## Key Concepts and Terminology

### Workforce Headcount
**Definition**: The number of personnel recorded for a profession, sector, and year.
**Relevance**: The central metric in both PS-001 and PS-002.
**Example**: A `count` of `18234` nurses in a given year and sector.

### Canonical Dataset
**Definition**: The approved processed dataset that downstream analysis must consume.
**Relevance**: Ensures all analytical outputs use the same cleaned input.
**Example**: `shared/data/4_processed/workforce_clean.parquet`.

### Schema Validation
**Definition**: Checking whether the source files contain the required fields and parseable types needed for the shared contract.
**Relevance**: Prevents ingestion drift and downstream failures.
**Example**: Confirming each CSV can produce logical columns `year`, `sector`, and `count`.

### Data Quality Profiling
**Definition**: Measuring completeness, uniqueness, validity, and consistency before finalizing a cleaned dataset.
**Relevance**: Required before combining the four profession files.
**Example**: Counting null `count` rows and distinct sector label variants.

### Sector
**Definition**: The organizational grouping in which workforce counts are reported.
**Relevance**: A core dashboard dimension and a required source field.
**Example**: `Public`, `Private`, or `Unknown` after standardization.

### Appendable Tab Architecture
**Definition**: A dashboard structure where tabs are defined as list elements that can be extended without rewriting the core app.
**Relevance**: Required for PS-003 and PS-005.
**Example**: Building a `tabs = [...]` list and allowing future modules to `append()` new tabs.

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Null rate | Share of rows missing a field | null rows / total rows | 0 to 1 | Data quality profiling | any field |
| Distinct sector count | Number of unique sector labels after standardization review | count distinct sector | 1+ | Category quality checks | `sector` |
| Combined row count | Total records in the canonical dataset | sum of retained rows | 1+ | Validate final output completeness | all cleaned files |
| Year coverage | Minimum and maximum years available | min(year), max(year) | dataset-specific | Dashboard filter bounds | `year` |

## Feature Engineering Guidance

### Common Features for Workforce Data

#### Profession
- **Description**: A derived label identifying the source profession file after combine.
- **Calculation**: Assign from source filename or extraction metadata.
- **Interpretation**: Enables cross-file comparison.
- **Use Cases**: Multi-line trend chart, profession filter.
- **Example**: `profession = "doctors"` for rows extracted from `doctors.csv`.

#### Standardized sector label
- **Description**: Cleaned version of the raw sector value used across all datasets.
- **Calculation**: Trim whitespace, harmonize casing/spelling, fill missing with `Unknown`.
- **Interpretation**: Prevents fragmented category analysis.
- **Use Cases**: Stacked bar charts, grouped summaries.
- **Example**: `public ` and `Public` both standardized to `Public`.

### Domain-Specific Patterns

#### Multi-file harmonization
**Description**: Multiple profession files form one analytical dataset only after schema alignment and standardization.
**When to Apply**: Any cross-profession trend analysis.
**Implementation**: Standardize columns, apply shared cleaning rules, then union all files with a derived profession field.
**Example**: Combine four CSV inputs into one Parquet output.

### Temporal Features

The project is constrained to annual headcount analysis using the documented `year` field. Do not imply monthly time series views unless a new data contract is introduced.

### Aggregation Strategies

Use sums of `count` grouped by `year`, `profession`, and optionally `sector`. Avoid averaging counts across categories unless the analytical question explicitly calls for it.

## Data Quality Considerations

### Non-parseable year values
- **Description**: Year values may arrive as strings or malformed values.
- **Impact**: Breaks sorting, filtering, and time-series aggregation.
- **Detection**: Parse checks during schema validation.
- **Mitigation**: Reject or drop invalid rows according to the documented cleaning rules.

### Negative counts
- **Description**: Workforce headcount cannot be negative.
- **Impact**: Produces invalid totals and misleading charts.
- **Detection**: Validate `count >= 0`.
- **Mitigation**: Flag in profiling and resolve before final export.

## Analytical Methodologies

### Descriptive aggregation
- **Application**: Producing historical trend and sector views.
- **Assumptions**: Cleaned source counts are additive across valid groupings.
- **Implementation Notes**: Use grouped sums in Polars and preserve annual grain.
- **Interpretation**: Outputs should be directly explainable to non-technical stakeholders.

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- Treating the four source files as having perfectly identical schemas without validation.
- Mixing raw and processed datasets in the same dashboard workflow.

### Best Practices
- Keep terminology aligned across story documents, data quality logs, and dashboard labels.
- Use the same canonical field names in every downstream artifact.

## References and Sources

### Authoritative Sources
- **Workforce Data Dictionary**: Internal field definitions and source file inventory.
- **Problem Statements PS-001 and PS-002**: Internal scope and acceptance targets.

## Cross-References

### Related Domain Knowledge Files
- [stakeholder-team-lead-expertise](stakeholder-team-lead-expertise.md) - Delivery governance perspective.
- [stakeholder-workforce-planner-expertise](stakeholder-workforce-planner-expertise.md) - Dashboard interpretation perspective.
- [workforce-headcount-metrics-kpis](workforce-headcount-metrics-kpis.md) - Metric definitions used in validation and charting.

### Related Data Dictionary Entries
- [01-workforce-sharepoint](../data_dictionary/01-workforce-sharepoint.md) - Source schema expectations and validation checklist.

## Metadata

**Created**: 2026-04-22
**Last Updated**: 2026-04-22
**Updated By**: GitHub Copilot
**Update Reason**: Initial terminology support for workforce data foundation and dashboard stories.
**Version**: 1.0

## Notes

This glossary should be expanded only when new workforce dimensions are formally documented in project context files.