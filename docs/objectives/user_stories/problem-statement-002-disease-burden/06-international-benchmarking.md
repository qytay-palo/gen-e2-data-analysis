# International Benchmarking Against WHO Standards (Lifecycle Stage: Advanced Analysis)

**Story ID**: PS-002-US-06  
**Epic**: National Disease Burden Temporal Trends Analysis  
**Priority**: P1 (High)  
**Effort Estimate**: M (5-6 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Public Health Policy Maker evaluating Singapore's healthcare system performance**,  
I want **to benchmark Singapore's disease mortality trends against WHO global averages and high-income country standards (OECD, IHME data)**,  
So that **I can identify areas where Singapore outperforms international peers (success stories) and areas needing improvement (performance gaps)**.

---

## 🎯 Acceptance Criteria

1. **External benchmark data acquired**
   - WHO Global Health Observatory (GHO) mortality data downloaded for cancer, stroke, IHD
   - OECD Health Statistics mortality rates extracted for comparable countries
   - High-income country peer group defined (e.g., Japan, South Korea, Australia, UK, USA)
   - Benchmark data standardized to match Singapore's metrics (age-standardized per 100k)

2. **Comparative analysis completed**
   - Singapore vs WHO global average: mortality rate differences calculated for each year
   - Singapore vs high-income average: performance gap quantified
   - Peer country rankings: Singapore's rank among comparable nations
   - Trend convergence/divergence: is Singapore gap widening or narrowing over time?

3. **Performance assessment delivered**
   - Outperformance areas: diseases where Singapore has lower mortality than benchmarks
   - Underperformance areas: diseases where Singapore lags behind peers
   - Trend comparison: is Singapore improving faster or slower than global trends?
   - Statistical significance testing: are differences statistically meaningful?

4. **Deliverables generated**
   - Output file: `results/tables/international_mortality_benchmarking.csv`
   - Visualization: Multi-panel comparison (Singapore vs benchmarks over time)
   - Benchmarking report: Performance summary with international context
   - Executive brief: 3-page summary for policy makers

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for data integration and analysis
- **External Data**: WHO API or CSV downloads, OECD data portal access
- **Visualization**: Matplotlib/Plotly for international comparisons
- **Logging**: loguru (NOT print statements)
- **Testing**: pytest with ≥80% coverage for benchmarking functions

---

## 📚 Domain Knowledge References

- [Disease Burden Feature Engineering Guide](../../../../domain_knowledge/disease-burden-feature-engineering-guide.md#age-standardized-mortality-rate-asmr) - Understanding ASMR for international comparisons
- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#international-benchmarks-disease-burden) - International benchmark sources
- [Problem Statement PS-002](../../../problem_statements/ps-002-disease-burden-temporal-trends.md#objective-3) - Objective: Benchmark against international standards

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Data integration and comparative analytics
- `requests>=2.31.0`: API calls to WHO GHO, OECD data portal
- `matplotlib>=3.8.0`: Benchmark visualization
- `seaborn>=0.13.0`: Statistical comparison charts
- `scipy>=1.11.0`: Statistical significance testing
- `loguru>=0.7.0`: Structured logging

### Internal Dependencies
- **Upstream**: PS-002-US-03 (Analyze mortality trends - BLOCKING)
- **Data Sources**: 
  - Internal: `shared/data/3_interim/mortality_trends_integrated_clean.parquet`
  - External: WHO GHO, OECD Health Statistics, IHME GBD database
- **Config Files**: `config/analysis.yml` (peer country list, API endpoints)

---

## ✅ Implementation Tasks

### External Data Acquisition
- [ ] Identify WHO GHO API endpoints for cancer, stroke, IHD mortality
- [ ] Download WHO global mortality data (1990-2019 if available)
- [ ] Access OECD Health Statistics via API or manual download
- [ ] Extract IHME Global Burden of Disease (GBD) estimates for comparison
- [ ] Define peer country list: Japan, South Korea, Taiwan, Australia, UK, Germany, USA
- [ ] Save external data to `shared/data/2_external/who_oecd_mortality_benchmarks.csv`

### Data Standardization
- [ ] Verify age-standardization: ensure WHO/OECD data uses same standard population
- [ ] Align time periods: match overlapping years (likely 1990-2018 for OECD)
- [ ] Standardize disease categories: map WHO ICD codes to Singapore categories
- [ ] Integrate Singapore data with benchmark data (common schema)
- [ ] Handle missing data: interpolation or flagging for incomplete benchmarks

### Comparative Analysis
- [ ] Calculate Singapore - WHO global average difference for each year
- [ ] Calculate Singapore - high-income average difference
- [ ] Rank Singapore among peer countries for each disease and year
- [ ] Compute convergence metric: is gap narrowing over time?
- [ ] Statistical testing: t-tests for significant differences

### Performance Assessment
- [ ] Identify outperformance: diseases where Singapore < peer average
- [ ] Identify underperformance: diseases where Singapore > peer average
- [ ] Quantify magnitude: % difference from benchmarks
- [ ] Trend comparison: Singapore APC vs global APC
- [ ] Generate performance scorecard: summary metrics

### Visualization
- [ ] Multi-panel time series: Singapore vs WHO vs high-income average
- [ ] Scatter plot: Singapore vs peer countries (latest year)
- [ ] Gap chart: difference from benchmark over time
- [ ] Rank chart: Singapore's position among peers
- [ ] Save figures: `reports/figures/international_mortality_benchmarking_*.png/pdf`

### Reporting
- [ ] Executive summary: key performance insights (3 pages)
- [ ] Detailed benchmarking report: methodology, findings, interpretation
- [ ] Success stories: areas where Singapore leads
- [ ] Improvement opportunities: areas to target based on peer performance
- [ ] Policy implications: what explains Singapore's position?

### Testing & Validation
- [ ] Unit tests for data integration functions
- [ ] Validate benchmark data: spot-check against published WHO/OECD reports
- [ ] Test gap calculation logic with sample data
- [ ] Validate rankings: ensure consistent ranking methodology
- [ ] Docstrings for all benchmarking functions

---

## 📌 Notes

**Data Sources**:
1. **WHO Global Health Observatory (GHO)**
   - URL: https://www.who.int/data/gho
   - Indicator codes: age-standardized NCD mortality rates
   - API: https://ghoapi.azureedge.net/api/

2. **OECD Health Statistics**
   - URL: https://data-explorer.oecd.org/
   - Dataset: Causes of mortality
   - Format: CSV download or API access

3. **IHME Global Burden of Disease (GBD)**
   - URL: http://ghdx.healthdata.org/gbd-results-tool
   - Comprehensive disease burden estimates
   - Download tool: can specify countries, diseases, years

**Polars Integration Example**:
```python
import polars as pl
import requests
from loguru import logger

# Example: WHO GHO API call
def fetch_who_mortality(indicator_code, year_range):
    """Fetch WHO mortality data via API"""
    base_url = "https://ghoapi.azureedge.net/api"
    endpoint = f"{base_url}/{indicator_code}"
    response = requests.get(endpoint)
    data = response.json()
    # Parse and convert to Polars DataFrame
    df_who = pl.DataFrame(data['value'])
    return df_who

# Integrate with Singapore data
df_singapore = pl.read_parquet("shared/data/3_interim/mortality_trends_integrated_clean.parquet")
df_who = fetch_who_mortality("cancer_mortality", "1990-2019")

# Calculate performance gap
df_comparison = (
    df_singapore
    .join(df_who.rename({'rate': 'who_global_avg'}), on=['year', 'disease_category'], how='left')
    .with_columns([
        (pl.col('mortality_rate') - pl.col('who_global_avg')).alias('gap_from_who'),
        ((pl.col('mortality_rate') / pl.col('who_global_avg') - 1) * 100).alias('gap_pct')
    ])
)

logger.info(f"✓ Benchmarking complete: {len(df_comparison)} year-disease comparisons")
```

**Peer Country Selection Criteria**:
- High-income status (World Bank classification)
- Similar healthcare system sophistication
- Comparable demographic characteristics (aging population)
- Data availability (complete time series)

**Suggested Peers**: Japan, South Korea, Taiwan, Australia, New Zealand, UK, Germany, France

**Expected Findings** (hypotheses):
- **Cancer**: Singapore likely outperforms global average, close to best-in-class
- **Stroke**: Singapore may lead due to excellent hypertension control programs
- **IHD**: Possibly middle-of-pack among high-income countries

**Interpretation Caveats**:
- Age-standardization differences across sources
- ICD code version changes over time
- Data completeness varies by country
- Cultural factors (e.g., diet, smoking prevalence) affect comparability

**Output Schema**:
```yaml
# results/tables/international_mortality_benchmarking.csv
columns:
  year: int32
  disease_category: categorical
  singapore_rate: float64
  who_global_avg: float64
  high_income_avg: float64
  singapore_rank: int  # among peer countries
  gap_from_who: float64  # negative = outperformance
  gap_from_peers: float64
  gap_trend: string  # converging, diverging, stable
```
