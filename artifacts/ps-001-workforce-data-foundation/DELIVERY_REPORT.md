# PS-001 Workforce Data Foundation — Delivery Report

**Date:** 2026-04-23  
**Status:** COMPLETE

---

## Executive Summary

PS-001 established the canonical workforce data foundation that all downstream problem statements (PS-002 through PS-005) depend on. The pipeline extracted four profession files from MOH SharePoint, validated their structure and quality, cleaned and standardised them into a single Parquet dataset, and surfaced the first set of analytical findings. The resulting `workforce_clean.parquet` (264 rows, 4 columns) is the shared contract for every subsequent dashboard, growth analysis, forecast, and forecast dashboard in this project.

---

## Pipeline Execution Summary

| Phase | Agent | Status | Key Output |
|-------|-------|--------|------------|
| Phase 1 — Extraction | data-extractor | ✅ PASS | `shared/data/1_raw/workforce/` (4 CSVs) |
| Phase 1 — Review | code-quality + code-reviewer | ✅ PASS | Immutability fix applied to `sharepoint_connector.py` |
| Phase 2 — Validation | data-validation | ✅ PASS | `data_quality_report.yml` — all 4 files pass schema |
| Phase 2 — Cleaning | data-cleaning | ✅ PASS | `workforce_clean.parquet` (264 rows × 4 cols) |
| Phase 2 — Review | code-quality + code-reviewer | ✅ PASS | 8 unit tests pass; alias-matching fix applied |
| Phase 3 — EDA | exploratory-analysis | ✅ PASS | 2 figures, summary CSV, findings YAML |
| Phase 3 — Review | code-quality | ✅ PASS | All artefacts verified |
| Phase 5 — Narrative | narrative-compiler | ✅ PASS | `results/narrative.md` (347 words) |

---

## Delivered Artefacts

### Shared (available to all PSes)
| File | Description |
|------|-------------|
| `shared/data/1_raw/workforce/doctors.csv` | 78 rows — immutable raw source |
| `shared/data/1_raw/workforce/nurses.csv` | 126 rows — immutable raw source |
| `shared/data/1_raw/workforce/pharmacists.csv` | 42 rows — immutable raw source |
| `shared/data/1_raw/workforce/physiotherapists.csv` | 18 rows — immutable raw source |
| `shared/data/4_processed/workforce_clean.parquet` | **Canonical dataset — 264 rows × 4 cols** |
| `shared/src/data_processing/workforce_validation.py` | Reusable validation module |
| `shared/src/data_processing/workforce_cleaning.py` | Reusable cleaning module |
| `shared/tests/unit/test_workforce_cleaning.py` | 8 unit tests (all pass) |

### PS-001 Artefacts
| File | Description |
|------|-------------|
| `scripts/extract_workforce_data.py` | Extraction pipeline entry point |
| `scripts/validate_workforce_data.py` | Validation pipeline entry point |
| `scripts/clean_workforce_data.py` | Cleaning pipeline entry point |
| `notebooks/01_extract_workforce_data.ipynb` | Executed extraction notebook |
| `notebooks/02_validate_workforce_data.ipynb` | Executed validation notebook |
| `notebooks/03_clean_workforce_data.ipynb` | Executed cleaning notebook |
| `notebooks/04_exploratory_analysis.ipynb` | Executed EDA notebook (131 KB) |
| `reports/figures/headcount_by_profession_year.png` | Line chart: headcount by profession (2006–2019) |
| `reports/figures/headcount_by_sector_year.png` | Line chart: headcount by sector (2006–2019) |
| `results/tables/data_quality_report.yml` | Schema + quality validation report |
| `results/tables/workforce_cleaning_audit.yml` | Per-profession cleaning audit |
| `results/tables/eda_summary_stats.csv` | Summary stats per profession |
| `results/tables/eda_findings.yml` | Structured key findings |
| `results/narrative.md` | Stakeholder-ready narrative |

---

## Canonical Dataset Contract

```
Path:   shared/data/4_processed/workforce_clean.parquet
Rows:   264
Schema:
  year        Int32
  sector      Categorical  (Not In Active Practice | Private | Public)
  count       Int32
  profession  Categorical  (doctors | nurses | pharmacists | physiotherapists)
```

**Do not rename or move this file.** All downstream PSes (002–005) load it from this exact path.

---

## Key Findings

- **Total 2019 workforce:** 62,484 across the four professions
- **Largest group:** Nurses (cumulative 469,457; peak 21,373 in 2019)
- **Second:** Doctors (cumulative 149,003; peak 5,166)
- **Top growth profession:** Nurses
- **Fastest growing sector:** Public
- **Coverage:** 2006–2019 for doctors/nurses/pharmacists; 2014–2019 for physiotherapists
- **Data quality:** Zero nulls, zero duplicates, zero rows dropped — the Parquet is a direct auditable consolidation of the raw sources

---

## Bugs Fixed During Pipeline

| File | Issue | Fix |
|------|-------|-----|
| `shared/src/data_processing/sharepoint_connector.py` | Would overwrite raw files on re-run | Skip download if file already exists (immutability) |
| `shared/src/data_processing/workforce_validation.py` | Column alias matching inconsistent with cleaner | Case-insensitive alias matching aligned across both modules |

---

## Handoff Chain

```
data-extractor  →  extraction_to_validation_20260422.json
data-validation →  validation_to_cleaning_20260422.json
data-cleaning   →  cleaning_to_eda_20260422.json
exploratory-analysis → eda_to_narrative_20260423.json
narrative-compiler   → narrative_to_delivery_20260423.json
```

---

## Acceptance Criteria — All Met

- [x] 4 raw CSVs downloaded to `shared/data/1_raw/workforce/` and immutable
- [x] All 4 files pass schema validation
- [x] `workforce_clean.parquet` written with correct schema and 264 rows
- [x] 8 unit tests pass for cleaning logic
- [x] EDA notebook executed with profession and sector trend charts
- [x] Stakeholder narrative written and reviewed
