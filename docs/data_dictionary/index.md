# Data Dictionary — Singapore Infectious Disease Analysis

**Project**: MOH Singapore – Infectious Disease Burden Analysis  
**Platform**: HEALIX/Databricks  
**Last Updated**: April 2026

---

## Index

| # | Domain | File | Owner / SME | Status |
|---|--------|------|-------------|--------|
| 1 | Infectious Diseases (Kaggle) | [01-infectious-diseases-kaggle.md](01-infectious-diseases-kaggle.md) | MOH Epidemiology Unit | ⏳ Pending extraction |

---

## Lineage Overview

```
Kaggle (external)
  └─ shared/data/1_raw/          ← immutable raw files
       └─ [per-dataset folder]
            └─ ps-*/data/3_interim/   ← cleaned / validated
                 └─ ps-*/data/4_processed/  ← analysis-ready
```

## Data Quality Standards

| Check | Threshold | Action on Failure |
|-------|-----------|-------------------|
| Missing values | < 20% per column | Flag & document in data dictionary |
| Duplicate rows | 0 exact duplicates | Drop duplicates, log count |
| Date format | ISO 8601 (YYYY-MM-DD) | Parse & coerce, log failures |
| Value ranges | Disease-specific | Flag outliers, do not drop |

---

*Each domain file below follows the template: field definitions, data types, value ranges, quality notes, lineage, and sample values.*
