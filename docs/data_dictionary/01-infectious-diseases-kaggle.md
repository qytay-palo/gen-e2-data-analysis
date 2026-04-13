# Data Dictionary — Infectious Diseases Dataset (Kaggle)

**Domain**: Singapore Weekly Infectious Disease Counts  
**Source**: Kaggle — *to be confirmed after extraction*  
**Raw Location**: `shared/data/1_raw/infectious-diseases/`  
**Refresh Frequency**: Weekly (MOH publishes weekly epidemiological bulletins)  
**Business Owner**: MOH Epidemiology & Disease Intelligence Division  
**Status**: ⏳ Pending extraction

---

## Dataset Overview

Weekly case counts of notifiable infectious diseases in Singapore, used to:
- Identify seasonal patterns and cyclical trends
- Forecast outbreak risk periods for Dengue, HFMD, influenza-like illnesses
- Guide resource allocation across disease surveillance programs

---

## Expected Schema (to be validated post-extraction)

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `epi_week` | Date/String | Epidemiological week start date | `2019-01-07` | ISO week; verify format |
| `disease` | String | Notifiable disease name | `Dengue Fever` | Standardise casing |
| `cases` | Integer | Weekly case count | `482` | Negative values invalid |
| `year` | Integer | Calendar year | `2019` | Derived from epi_week |
| `week_number` | Integer | ISO week number (1–53) | `2` | Derived from epi_week |

---

## Known Data Quality Considerations

| Issue | Handling Strategy |
|-------|------------------|
| Reporting lag (last 1–2 weeks provisional) | Flag provisional weeks; exclude from forecasting training set |
| Disease name changes over time | Map historical names to current taxonomy |
| Zero-count vs missing | Treat zero as true zero; NULL = not reported |
| Outbreak spikes (e.g., COVID-19 2020) | Mark as anomaly; exclude from seasonal baseline |

---

## Lineage

```
Kaggle API download
  → shared/data/1_raw/infectious-diseases/
      → ps-*/data/3_interim/cleaned_disease_weekly.parquet
          → ps-*/data/4_processed/disease_features.parquet
```

---

*Update this file after running the data extractor agent.*
