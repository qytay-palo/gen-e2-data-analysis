# Domain Knowledge: MOH Workforce Planner Expertise

## Overview

This file captures the analytical perspective of MOH workforce planners who use the dashboard outputs to understand historical headcount movement across professions and sectors. Their focus is self-service exploration, fast comparisons, and confidence that displayed trends reflect the canonical processed dataset.

## Related Problem Statements

- [Problem Statement PS-002 - Workforce Trends Dashboard](../objectives/problem_statements/ps-002-workforce-trends-dashboard.md)

## Related Stakeholders

- **MOH Workforce Planners**: Use historical headcount views to identify long-term changes and sector composition.
- **Team Lead**: Needs dashboard outputs to align with approved processed data definitions.

## Key Concepts and Terminology

### Headcount Trend
**Definition**: The change in workforce count over time for a profession or segment.
**Relevance**: Core analytical view in the first dashboard tab.
**Example**: Viewing nurse headcount from 2015 to 2025 on a line chart.

### Sector Mix
**Definition**: Distribution of a profession's headcount across sectors for a given year or range.
**Relevance**: Core analytical view in the second dashboard tab.
**Example**: Comparing public versus private doctor headcount in 2024.

### Interactive Filter
**Definition**: A control that narrows the data shown in a chart without reloading the full page.
**Relevance**: Required for fast self-service exploration in PS-002.
**Example**: Year slider and profession multi-select updating charts instantly.

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Total headcount | Workforce count summed over selected dimensions | sum(count) | 0+ | Show trend magnitude | `count` |
| Profession-level headcount | Total headcount for one profession in selected years | sum(count) grouped by profession | 0+ | Compare professions | `profession`, `count` |
| Sector composition share | Share of total headcount by sector | sector count / total count | 0 to 1 | Interpret sector mix | `sector`, `count` |
| Render responsiveness | Time from filter change to chart refresh | callback completion time | near-instant target | Dashboard usability | runtime timing |

## Feature Engineering Guidance

### Common Features for Workforce Dashboarding

#### Aggregated annual totals
- **Description**: Annual total headcount by profession.
- **Calculation**: Group by `year` and `profession`, then sum `count`.
- **Interpretation**: Displays overall change in workforce size over time.
- **Use Cases**: Line chart trends, cross-profession comparison.
- **Example**: `sum(count)` for `nurses` in 2021.

#### Annual sector totals
- **Description**: Annual headcount by sector and profession.
- **Calculation**: Group by `year`, `sector`, and `profession`, then sum `count`.
- **Interpretation**: Shows the mix of workforce across sectors.
- **Use Cases**: Stacked bar chart, sector comparison.
- **Example**: Public-sector pharmacist headcount in 2023.

### Temporal Features

Use annual grain only because the documented shared contract is based on the `year` field rather than monthly timestamps.

### Aggregation Strategies

Aggregate from the canonical Parquet instead of from raw files, and keep the dashboard filters aligned to the processed contract dimensions: `year`, `profession`, and `sector`.

## Data Quality Considerations

### Misleading totals from inconsistent sector labels
- **Description**: Variant spellings or casing of sector values can split the same category.
- **Impact**: Stacked bars misrepresent the true sector mix.
- **Detection**: Distinct value review during cleaning and chart QA.
- **Mitigation**: Standardize sector labels before dashboard consumption.

### Incomplete year filtering
- **Description**: Slider bounds that do not respect available data can create empty or misleading views.
- **Impact**: Users may infer missing data rather than a filter issue.
- **Detection**: Validate slider defaults against min and max `year` in the processed dataset.
- **Mitigation**: Drive filter options dynamically from the canonical Parquet.

## Analytical Methodologies

### Descriptive trend analysis
- **Application**: Historical headcount analysis by profession and sector.
- **Assumptions**: Counts are aggregated consistently across files after PS-001 cleaning.
- **Implementation Notes**: Use direct aggregation and interactive filtering, not model-based smoothing.
- **Interpretation**: Focus on transparent descriptive views stakeholders can verify easily.

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- Using inconsistent default filters across tabs: users may think charts disagree when filters differ.
- Loading raw CSVs directly in the dashboard: this duplicates logic and bypasses the cleaned contract.

### Best Practices
- Keep chart logic thin and move reusable data loading and filtering into shared dashboard helpers where practical.
- Ensure tab modules expose a consistent interface so later PS work can append new tabs safely.

## References and Sources

### Authoritative Sources
- **Project Problem Statement PS-002**: Defines the required tabs, filters, performance target, and appendable architecture.
- **Workforce Data Dictionary**: Defines the source fields and their expected meaning.

## Cross-References

### Related Domain Knowledge Files
- [workforce-analytics-terminology-glossary](workforce-analytics-terminology-glossary.md) - Shared vocabulary used in dashboard copy and documentation.
- [workforce-headcount-metrics-kpis](workforce-headcount-metrics-kpis.md) - Core chart metrics and validation ranges.

### Related Data Dictionary Entries
- [01-workforce-sharepoint](../data_dictionary/01-workforce-sharepoint.md) - Source and field definitions that feed the canonical Parquet.

## Metadata

**Created**: 2026-04-22
**Last Updated**: 2026-04-22
**Updated By**: GitHub Copilot
**Update Reason**: Initial workforce planner context for PS-002 story generation.
**Version**: 1.0

## Notes

This stakeholder primarily needs interpretable descriptive analytics, not forecasting or causal inference in the dashboard opening state.