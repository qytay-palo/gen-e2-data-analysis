# Data Dictionary Index

This index tracks the datasets currently documented for the Gen-E2 workforce analysis project.

| ID | Domain | Source | File | Refresh | Owner |
|---|---|---|---|---|---|
| 01 | Workforce analytics | SharePoint / DataDojo | [01-workforce-sharepoint.md](01-workforce-sharepoint.md) | Monthly | Team lead |

## Lineage overview

```text
SharePoint / DataDojo
  -> shared/data/1_raw/workforce/           (immutable raw CSVs — PS-001)
  -> shared/data/4_processed/
       workforce_clean.parquet              (canonical clean dataset — PS-001 output)
  -> artifacts/ps-002-workforce-trends-dashboard/   (dashboard reads parquet)
  -> artifacts/ps-003-workforce-growth-analysis/    (growth rates read parquet)
  -> artifacts/ps-004-headcount-forecasting/
       results/forecasts/forecast_table.csv
       results/metrics/model_registry.csv   (PS-004 outputs)
  -> artifacts/ps-005-forecast-dashboard-integration/  (reads PS-004 outputs)
```

## Quality expectations

- Preserve raw files without in-place edits
- Validate required columns (`year`, `sector`, `count`) and year ranges during ingestion
- Document all exclusions, nulls, and imputation decisions in `workforce_cleaning_audit.yml`
- Final clean dataset must pass schema validation before any downstream PS consumes it
