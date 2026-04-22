## Executive Summary

PS-001 established a single, trusted workforce data foundation for downstream analysis. The pipeline extracted four profession files from the MOH SharePoint source, validated their structure, and consolidated them into one analysis-ready Parquet dataset with a documented cleaning audit. This matters because every later workforce trend, growth, forecast, and dashboard deliverable now depends on one auditable source instead of separate spreadsheets. The resulting dataset gives stakeholders a reliable historical baseline for planning and reporting.

## Data Foundation

- Source: MOH SharePoint workforce folder at `/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/`
- Files combined: 4 CSVs covering doctors, nurses, pharmacists, and physiotherapists
- Clean output: 264 rows written to `shared/data/4_processed/workforce_clean.parquet`
- Year range: 2006-2019 overall; physiotherapists start in 2014
- Standard schema: `year`, `sector`, `count`, `profession` with consistent Int32 and categorical types

## Key Findings

- The latest year in scope is 2019, with a total recorded workforce of 62,484 across the covered professions.
- Nurses are the largest workforce group in the dataset, with a cumulative headcount of 469,457 and a peak annual count of 21,373.
- Doctors rank second by size, with a cumulative headcount of 149,003 and a peak annual count of 5,166.
- Pharmacists contribute 32,349 cumulatively, with a peak annual count of 1,616, while physiotherapists contribute 10,437 from 2014-2019 with a peak of 960.
- The EDA handoff identifies nurses as the top-growth profession and the public sector as the fastest-growing sector over the observed period.

## Data Quality

All four raw files passed schema validation against the required fields (`year`, `sector`, `count`). Validation found no missing required values, no duplicate rows, and no negative counts in any source file. Cleaning removed no rows and required no imputations, so the 264-row Parquet output is a direct, auditable consolidation of the validated source extracts.

## Downstream Value

This Parquet file is the shared contract for PS-002 through PS-005. It gives PS-002 a stable input for workforce trends dashboards, PS-003 a clean baseline for growth analysis, PS-004 a consistent time series for forecasting, and PS-005 a dependable source for dashboard integration without reworking extraction or cleaning logic.