# Domain Knowledge: Workforce Forecasting Feature Engineering Guide

## Overview

This guide captures the feature engineering patterns and analytical guardrails for workforce growth analysis, annual headcount forecasting, and forecast dashboard integration. It is grounded in the documented annual workforce headcount contract and is intended to support PS-003, PS-004, and PS-005 without introducing unsupported demand-side or facility-level assumptions.

## Related Problem Statements

- [Problem Statement PS-003 - Workforce Growth Analysis](../objectives/problem_statements/ps-003-workforce-growth-analysis.md)
- [Problem Statement PS-004 - Headcount Forecasting Models](../objectives/problem_statements/ps-004-headcount-forecasting.md)
- [Problem Statement PS-005 - Forecast Dashboard Integration](../objectives/problem_statements/ps-005-forecast-dashboard-integration.md)

## Related Stakeholders

- **Team Lead**: Needs derived features and growth metrics to remain traceable to the canonical annual headcount dataset.
- **MOH Workforce Planners**: Need interpretable growth and forecast outputs that can be compared across professions without hidden transformations.

## Key Concepts and Terminology

### Annual Analytical Grain
**Definition**: The level at which workforce records are aggregated for analysis, using one record set per `year`, `profession`, and optional `sector` grouping.
**Relevance**: All documented downstream analytics are constrained to annual headcount because the validated shared contract does not include a monthly or facility-level time axis.
**Example**: Forecasting nurse headcount from 2015 to 2025 using one annual value per year.

### Year-on-Year Growth Rate
**Definition**: Percentage change between the current year's headcount and the previous year's headcount.
**Relevance**: Core PS-003 metric for comparing acceleration or contraction across professions and sectors.
**Example**: `(count_2025 - count_2024) / count_2024 * 100`.

### Compound Annual Growth Rate
**Definition**: The smoothed annualized growth rate between the first and last observed values across a multi-year period.
**Relevance**: Used in PS-003 to compare long-run growth across professions and sectors.
**Example**: `(final / initial) ^ (1 / n_years) - 1`.

### Forecast Horizon
**Definition**: The future period covered by model predictions beyond the latest observed year.
**Relevance**: PS-004 and PS-005 are explicitly limited to a five-year annual forecast horizon.
**Example**: If the last observed year is 2025, the forecast horizon is 2026 to 2030.

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| YoY growth rate | Annual percentage change in headcount | `(current - prior) / prior * 100` | dataset-specific | Growth trend analysis | `year`, `count`, grouping columns |
| CAGR | Annualized growth between first and last valid observations | `(final / initial) ^ (1 / n_years) - 1` | dataset-specific | Long-run profession or sector comparison | ordered annual headcount series |
| MAE | Mean absolute error over validation window | average of `abs(actual - predicted)` | 0+ | Model comparison | actual and predicted counts |
| RMSE | Root mean squared error over validation window | `sqrt(mean((actual - predicted)^2))` | 0+ | Model comparison and tie-break | actual and predicted counts |
| MAPE | Mean absolute percentage error over validation window | average of `abs((actual - predicted) / actual) * 100` | 0+ | Champion model selection | positive actual counts |
| MAPE target met | Indicator that the profession-level forecast meets the stated target | `MAPE < 10%` | true or false | Registry reporting | profession-level MAPE |

## Feature Engineering Guidance

### Common Features for Workforce Forecasting

#### Time index
- **Description**: A monotonically increasing annual feature used by linear baseline models.
- **Calculation**: Use `year` directly or normalize to `year - min(year)` within each profession series.
- **Interpretation**: Captures linear directional trend over time.
- **Use Cases**: Linear regression baseline and chart ordering.
- **Example**: `t = 0, 1, 2, ...` for a profession's yearly series.

#### Lagged headcount
- **Description**: Prior-year observed headcount used to preserve short-term temporal dependence.
- **Calculation**: `count.shift(1)` within each profession or sector group after sorting by `year`.
- **Interpretation**: Highlights whether current headcount depends strongly on the previous period.
- **Use Cases**: Feature QA, exploratory diagnostics, and optional baseline enrichments if the modeling scope expands.
- **Example**: 2025 doctor lag value equals the observed doctor headcount in 2024.

#### Rolling trend summaries
- **Description**: Smoothed annual summaries such as 2-year or 3-year rolling averages.
- **Calculation**: Rolling mean over sorted annual `count` values within each profession.
- **Interpretation**: Separates short-term volatility from longer-run direction.
- **Use Cases**: Exploratory validation and forecast chart context.
- **Example**: 3-year rolling average for pharmacists in 2025 uses 2023 to 2025 actuals.

#### Growth features
- **Description**: Derived series including YoY percentage change and absolute change.
- **Calculation**: Use sorted annual counts and compute both delta and percentage delta by group.
- **Interpretation**: Distinguishes fast-growing professions from those with high absolute growth but low rate change.
- **Use Cases**: PS-003 tab visuals and forecast plausibility checks.
- **Example**: Physiotherapist absolute change from 2024 to 2025.

### Domain-Specific Patterns

#### Groupwise annual series preparation
**Description**: Each profession should be modelled and validated as its own annual time series.
**When to Apply**: PS-003 metric derivation and all PS-004 forecasting tasks.
**Implementation**: Sort by `profession` and `year`, aggregate annual counts, and derive features within each profession partition.
**Example**: Build separate annual series for doctors, nurses, pharmacists, and physiotherapists.

#### Sector-aware descriptive growth calculation
**Description**: Growth metrics should be computed for both profession totals and profession-by-sector slices when data coverage supports it.
**When to Apply**: PS-003 growth analysis outputs and dashboard filters.
**Implementation**: Compute grouped annual totals by `profession, sector, year`, then derive YoY and CAGR with explicit handling for zero or missing denominators.
**Example**: Compute CAGR for public-sector nurses across the available annual window.

### Temporal Features

Use only annual ordering derived from the `year` field. Do not fabricate monthly, quarterly, or seasonal features because those grains are not documented in the shared workforce contract.

### Aggregation Strategies

Aggregate `count` with sums after grouping by the documented dimensions. Preserve one record per analytical grouping and year before deriving growth or forecast outputs. Keep forecast outputs at annual profession level because that is the PS-004 export contract consumed by PS-005.

## Data Quality Considerations

### Zero or missing denominator in growth calculations
- **Description**: YoY and CAGR formulas can become undefined when the prior or initial value is zero or missing.
- **Impact**: Produces infinite or misleading growth rates.
- **Detection**: Flag groups where prior-year count or initial count is `0` or null before calculation.
- **Mitigation**: Emit null growth values with documented reason rather than forcing a numeric output.

### Short or sparse profession series
- **Description**: Some professions may not have enough stable annual observations for reliable ARIMA fitting.
- **Impact**: Model fitting may fail or overfit.
- **Detection**: Check count of non-null annual observations and continuity of years before model training.
- **Mitigation**: Fall back to the documented linear baseline and record the rationale in logs and registry outputs.

### Non-positive actuals in MAPE evaluation
- **Description**: MAPE is unstable when actual headcount is zero.
- **Impact**: Validation metrics become undefined or distorted.
- **Detection**: Review held-out windows for zero actual counts before scoring.
- **Mitigation**: Document exclusion logic or use a safe guard while retaining MAE and RMSE as secondary metrics.

## Analytical Methodologies

### Descriptive growth analysis
- **Application**: PS-003 YoY and CAGR reporting.
- **Assumptions**: Annual counts are additive and comparable over time after upstream cleaning.
- **Implementation Notes**: Use grouped Polars transformations and avoid dashboard-layer recomputation where an exported table already exists.
- **Interpretation**: Compare both absolute count changes and relative percentage growth to avoid misleading rank orders.

### Baseline-versus-ARIMA forecast comparison
- **Application**: PS-004 model selection by profession.
- **Assumptions**: Chronological validation with no shuffling and annual headcount history as the only approved input signal.
- **Implementation Notes**: Fit linear regression with `year` as the baseline, fit ARIMA on the ordered annual series, and compare on the last three years.
- **Interpretation**: Prefer the lowest-error model, but retain the simpler linear model when the documented tie-break condition is met.

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- Deriving monthly or facility-level features from an annual-only contract.
- Mixing historical actual aggregation logic between PS-003, PS-004, and PS-005 so the charts and forecast registry disagree.
- Loading fitted model objects in the dashboard layer when the documented integration contract is CSV-only.

### Best Practices
- Engineer and validate all derived metrics from the canonical Parquet rather than raw CSVs.
- Keep feature derivation deterministic and partitioned by profession or profession-sector grouping.
- Export machine-readable outputs with stable schemas so dashboard integration remains runtime-only and restart-free.

## References and Sources

### Authoritative Sources
- **Project Problem Statements PS-003 to PS-005**: Internal scope, formulas, model-selection rules, and dashboard integration contracts.
- **Project Context Data Sources**: Documents the workforce source inventory and annual headcount field contract.
- **Project Tech Stack**: Defines the Polars-first processing approach, Dash integration pattern, and approved modeling libraries.

## Cross-References

### Related Domain Knowledge Files
- [stakeholder-team-lead-expertise](stakeholder-team-lead-expertise.md) - Delivery governance and sign-off expectations.
- [stakeholder-workforce-planner-expertise](stakeholder-workforce-planner-expertise.md) - Dashboard interpretation needs for growth and forecast views.
- [workforce-analytics-terminology-glossary](workforce-analytics-terminology-glossary.md) - Shared vocabulary used in stories and outputs.
- [workforce-headcount-metrics-kpis](workforce-headcount-metrics-kpis.md) - Validation metric definitions and KPI naming.

### Related Data Dictionary Entries
- [01-workforce-sharepoint](../data_dictionary/01-workforce-sharepoint.md) - Source field definitions and validation expectations.

## Metadata

**Created**: 2026-04-22
**Last Updated**: 2026-04-22
**Updated By**: GitHub Copilot
**Update Reason**: Added forecasting-oriented feature engineering guidance for PS-003, PS-004, and PS-005 story generation.
**Version**: 1.0

## Notes

This guide intentionally stops at workforce supply forecasting. It does not cover demand forecasting, vacancy analysis, or training-pipeline features because those inputs are not documented in the current repository context.