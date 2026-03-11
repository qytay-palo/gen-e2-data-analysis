# Benchmark Against International Expenditure Standards (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-004-US-07  
**Epic**: Healthcare Expenditure Drivers & Cost Control Analysis  
**Priority**: P1 (High)  
**Effort Estimate**: M (5-6 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Financial Policy Maker evaluating Singapore's cost performance**,  
I want **to benchmark Singapore's healthcare expenditure against OECD and WHO standards including expenditure as % of GDP, per capita spending, and growth rates**,  
So that **I can assess whether Singapore is spending efficiently relative to peer countries and identify areas of over/under-spending**.

---

## 🎯 Acceptance Criteria

1. **External benchmark data acquired**
   - OECD Health Statistics: expenditure data for peer countries
   - WHO Global Health Expenditure Database: international comparisons
   - Key metrics: expenditure % GDP, per capita, public vs private share
   - Peer countries: Japan, South Korea, Australia, UK, USA, Germany

2. **Comparative analysis completed**
   - Singapore vs OECD average: expenditure gaps quantified
   - Singapore vs high-performing peers: best practice identification
   - Trend comparison: Singapore growth vs international growth
   - Public-private mix comparison

3. **Performance assessment**
   - Outperformance areas: where Singapore spends less for similar outcomes
   - Underperformance areas: where Singapore spends more
   - Efficiency indicators: expenditure per health outcome unit

4. **Deliverables**
   - Output: `results/tables/international_expenditure_benchmarking.csv`
   - Figures: Benchmarking charts, peer country comparisons
   - Report: International expenditure performance assessment

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+
- **External Data**: OECD API, WHO database
- **Visualization**: Matplotlib/Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#international-expenditure-benchmarks) - OECD/WHO benchmarking methods
- [Problem Statement PS-004](../../../problem_statements/ps-004-healthcare-expenditure-drivers.md#objective-3) - International benchmarking

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `requests>=2.31.0`, `matplotlib>=3.8.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-004-US-03 (Expenditure trends - BLOCKING)
- **Data Sources**: 
  - Internal: `shared/data/3_interim/expenditure_drivers_integrated.parquet`
  - External: OECD database, WHO GHED
- **Config Files**: `config/analysis.yml`

---

## ✅ Implementation Tasks

### External Data Acquisition
- [ ] Access OECD Health Statistics (API or download)
- [ ] Access WHO Global Health Expenditure Database
- [ ] Extract expenditure metrics for peer countries
- [ ] Save to `shared/data/2_external/oecd_who_expenditure.csv`

### Benchmark Calculations
- [ ] Calculate Singapore expenditure as % GDP
- [ ] Calculate per capita expenditure in USD PPP
- [ ] Compare with OECD averages and peer countries
- [ ] Calculate gaps and rankings

### Trend Comparison
- [ ] Compare Singapore growth rates with international trends
- [ ] Assess convergence or divergence
- [ ] Identify periods where Singapore diverged from peers

### Visualization
- [ ] Bar charts: Singapore vs peers (latest year)
- [ ] Time series: Singapore vs OECD average over time
- [ ] Scatter plot: expenditure % GDP vs health outcomes (if data available)
- [ ] Save figures

### Testing & Documentation
- [ ] Validate external data quality
- [ ] Unit tests for benchmarking calculations
- [ ] Docstrings
- [ ] Benchmarking report

---

## 📌 Notes

**Data Sources**:
- **OECD Health Statistics**: https://data-explorer.oecd.org/
- **WHO GHED**: https://apps.who.int/nha/database

**Key Metrics**:
- Expenditure as % GDP (typical range: 6-12% for high-income countries)
- Per capita expenditure in USD PPP (purchasing power parity)
- Public vs private expenditure share

**Expected Findings**:
- Singapore likely lower expenditure % GDP than US, similar to Asian peers
- Efficient spending: good outcomes for moderate expenditure
