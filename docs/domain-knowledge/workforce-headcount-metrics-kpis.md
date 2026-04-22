# Domain Knowledge: Workforce Headcount Metrics and KPIs

## Overview

This file documents the standard metrics and validation checks that should be used when preparing and presenting workforce headcount data in the current project scope. It is designed to support both PS-001 quality controls and PS-002 dashboard interpretations.

## Related Problem Statements

- [Problem Statement PS-001 - Workforce Data Foundation](../objectives/problem_statements/ps-001-workforce-data-foundation.md)
- [Problem Statement PS-002 - Workforce Trends Dashboard](../objectives/problem_statements/ps-002-workforce-trends-dashboard.md)

## Related Stakeholders

- **Team Lead**: Uses these metrics to assess extraction completeness and processing readiness.
- **MOH Workforce Planners**: Use these metrics to interpret headcount displays and sector views.

## Key Concepts and Terminology

### Completeness Metric
**Definition**: A measure of whether required files and fields are present and usable.
**Relevance**: Determines whether downstream analysis can proceed safely.
**Example**: Four expected source files successfully extracted.

### Quality Gate
**Definition**: A measurable threshold that must be met before a dataset or app is considered ready.
**Relevance**: Supports Definition of Done and sign-off.
**Example**: Required columns present in all four profession files.

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Source file coverage | Share of expected files extracted | extracted files / 4 | 0 to 1 | PS-001 extraction validation | source file inventory |
| Required-column coverage | Share of files containing `year`, `sector`, `count` | conforming files / 4 | 0 to 1 | PS-001 schema validation | file schemas |
| Null critical-field count | Number of rows with null `year` or `count` | count of null critical rows | 0+ | PS-001 cleaning decision support | cleaned candidate rows |
| Unknown sector count | Number of rows with missing sector standardized to `Unknown` | count where sector = `Unknown` | 0+ | Profile standardization impact | `sector` |
| Final processed row count | Retained rows after cleaning and combine | count rows in final dataset | 1+ | Output completeness check | processed Parquet |
| Distinct profession count | Number of professions in the combined dataset | count distinct profession | expected 4 | Contract integrity | `profession` |
| Distinct sector count | Number of cleaned sectors represented | count distinct sector | dataset-specific | Dashboard segmentation sanity check | `sector` |
| Dashboard load time | Seconds to first render after app start | wall-clock seconds | under 3 target | PS-002 non-functional validation | runtime logs |

## Feature Engineering Guidance

### Common Features for Workforce Metrics

#### Profession inventory flag
- **Description**: Presence of all four professions in the combined dataset.
- **Calculation**: Compare distinct `profession` values against expected file list.
- **Interpretation**: Confirms no source file was omitted during combine.
- **Use Cases**: Final export validation.
- **Example**: `doctors`, `nurses`, `pharmacists`, `physiotherapists` all present.

#### Year range boundaries
- **Description**: Minimum and maximum year values available in the clean dataset.
- **Calculation**: `min(year)` and `max(year)`.
- **Interpretation**: Defines valid dashboard slider limits.
- **Use Cases**: Filter initialization and smoke testing.
- **Example**: Slider defaults to available dataset bounds.

## Data Quality Considerations

### Profession omission
- **Description**: A missing profession file can still produce a combined dataset that looks valid at first glance.
- **Impact**: Dashboards and analyses understate total workforce trends.
- **Detection**: Compare extracted and combined profession inventory to the expected set of four.
- **Mitigation**: Treat any missing profession as a blocking issue for sign-off.

### Sector fragmentation
- **Description**: Near-duplicate sector labels split totals across categories.
- **Impact**: Stacked bar charts and sector comparisons become misleading.
- **Detection**: Review distinct sector values before and after standardization.
- **Mitigation**: Maintain an explicit standardization map and log applied changes.

## Analytical Methodologies

### Quality-gated descriptive analytics
- **Application**: All PS-001 and PS-002 output generation.
- **Assumptions**: Source data is valid only after passing extraction, schema, and cleaning gates.
- **Implementation Notes**: Apply profiling before combine, then validate final contract before dashboard consumption.
- **Interpretation**: Dashboard insights are trusted only when upstream metrics meet agreed thresholds.

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- Declaring success based only on file existence without checking schema or row-level validity.
- Hardcoding dashboard filters instead of deriving them from processed data metrics.

### Best Practices
- Include measurable thresholds in each story's acceptance criteria and Definition of Done.
- Reuse the same KPI names across profiling logs, tests, and stakeholder documentation.

## References and Sources

### Authoritative Sources
- **Workforce Data Dictionary**: Internal documentation for required fields and validation checklist.
- **Project Context Data Sources**: Internal documentation for source location and expected file inventory.

## Cross-References

### Related Domain Knowledge Files
- [workforce-analytics-terminology-glossary](workforce-analytics-terminology-glossary.md) - Shared analytical vocabulary.
- [stakeholder-team-lead-expertise](stakeholder-team-lead-expertise.md) - Delivery governance use of these metrics.
- [stakeholder-workforce-planner-expertise](stakeholder-workforce-planner-expertise.md) - Dashboard interpretation use of these metrics.

### Related Data Dictionary Entries
- [01-workforce-sharepoint](../data_dictionary/01-workforce-sharepoint.md) - Raw field definitions and validation checklist.

## Metadata

**Created**: 2026-04-22
**Last Updated**: 2026-04-22
**Updated By**: GitHub Copilot
**Update Reason**: Initial KPI library for workforce data foundation and dashboard story generation.
**Version**: 1.0

## Notes

The documented metrics are intentionally descriptive and operational. They do not introduce forecasting or inferential KPIs beyond the current project scope.