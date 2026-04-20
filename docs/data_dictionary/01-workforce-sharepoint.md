# Workforce Data Dictionary

## Dataset summary

- Domain: healthcare workforce analytics
- Source: MOH SharePoint / DataDojo
- Source folder: `/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/`
- Local raw location: `shared/data/1_raw/workforce/`
- Expected refresh frequency: monthly
- Business owner: team lead
- Primary stakeholder question: how has workforce supply changed historically and what does the next five years suggest?

## Files in scope

| File | Description | Notes |
|---|---|---|
| `doctors.csv` | Medical doctor workforce data | expected monthly refresh |
| `nurses.csv` | Nursing workforce data | expected monthly refresh |
| `pharmacists.csv` | Pharmacist workforce data | expected monthly refresh |
| `physiotherapists.csv` | Physiotherapist workforce data | expected monthly refresh |

## Common expected fields

Because source schema may vary by profession file, validate the presence and meaning of these fields during ingestion.

| Field | Expected type | Example | Notes |
|---|---|---|---|
| `year` | integer | `2025` | critical for trend analysis |
| `sector` | string | `Public` | standardize category spelling |
| `count` | integer | `18234` | must be non-negative |
| `profession` | string | `doctors` | derived after combining files |

## Data quality notes

- schema may differ slightly across files
- some files may require column name standardization before combining
- missing or partial latest-month records should be logged, not silently dropped
- final forecast dataset should document any gaps, exclusions, and imputation rules

## Lineage tracking

```text
SharePoint raw CSV
  -> shared connector extraction
  -> shared/data/1_raw/workforce/
  -> interim standardized workforce tables
  -> processed forecasting dataset
  -> trend tables / forecast outputs
```

## Validation checklist

- confirm file download timestamp
- confirm row count > 0
- confirm column count > 0
- confirm `year` values are parseable if present
- confirm no negative workforce counts
