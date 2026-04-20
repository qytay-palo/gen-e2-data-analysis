# Data Dictionary Index

This index tracks the datasets currently documented for the Gen-E2 workforce analysis project.

| ID | Domain | Source | File | Refresh | Owner |
|---|---|---|---|---|---|
| 01 | Workforce analytics | SharePoint / DataDojo | [01-workforce-sharepoint.md](01-workforce-sharepoint.md) | Monthly | Team lead |

## Lineage overview

```text
SharePoint / DataDojo
  -> shared/data/1_raw/workforce/
  -> artifacts/ps-001-workforce-trends-forecasting/data/3_interim/
  -> artifacts/ps-001-workforce-trends-forecasting/data/4_processed/
  -> artifacts/ps-001-workforce-trends-forecasting/results/
```

## Quality expectations

- preserve raw files without in-place edits
- validate required columns and year ranges during ingestion
- document limitations and missing values before modeling
