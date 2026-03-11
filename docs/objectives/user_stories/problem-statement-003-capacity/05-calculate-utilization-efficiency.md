# Calculate Utilization Efficiency Metrics (Lifecycle Stage: Feature Engineering)

**Story ID**: PS-003-US-05  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P0 (Critical)  
**Effort Estimate**: M (4 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Service Planner**,  
I want **to calculate proxy bed occupancy rates and utilization efficiency metrics by comparing capacity trends against admission rate trends**,  
So that **I can identify facilities operating at capacity strain vs those with excess capacity and optimize resource allocation accordingly**.

---

## 🎯 Acceptance Criteria

1. **Proxy occupancy metrics calculated**
   - Proxy occupancy rate: `(admission_rate × avg_length_of_stay) / (beds_per_1000_population × 365 days)` (simplified)
   - Utilization index: `utilization_growth / capacity_growth` (if >1, demand growing faster than supply)
   - Capacity strain indicator: flag years/facilities where proxy occupancy >85%

2. **Capacity-to-population ratios calculated**
   - Beds per 1,000 population by facility type (acute, intermediate, long-term care)
   - Trend analysis: is ratio increasing (capacity expansion) or decreasing (population growth outpacing capacity)?
   - Benchmark against international standards (WHO, OECD targets)

3. **Efficiency benchmarks established**
   - Target occupancy: 75-85% (optimal efficiency range per healthcare literature)
   - Under-utilized: <65% occupancy (potential over-investment)
   - Over-utilized: >90% occupancy (strain, quality risk)
   - Classify facilities into efficiency categories

4. **Data output requirement**
   - Output file: `results/tables/capacity_utilization_efficiency.csv`
   - Format: CSV (facility_type, year, beds_per_1000, proxy_occupancy_pct, utilization_index, efficiency_category)
   - Efficiency visualization: `reports/figures/utilization_efficiency_heatmap.png`

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ (MANDATORY)
- **Logging**: loguru
- **Testing**: pytest with ≥80% coverage

---

## 📚 Domain Knowledge References

- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objectives) - Objective 2: Assess utilization patterns
- International benchmarks: WHO bed density standards, OECD health statistics

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`: Metric calculations
- `matplotlib>=3.8.0`: Heatmap visualizations
- `loguru>=0.7.0`: Logging

### Internal Dependencies
- **Upstream**: 
  - PS-003-US-02 (Integrated capacity data - BLOCKING)
  - PS-003-US-03 (Capacity trends - RECOMMENDED)
  - PS-003-US-04 (Utilization patterns - BLOCKING)
- **Data Sources**: 
  - `shared/data/3_interim/capacity_utilization_integrated.parquet`
  - Population data (from admission rate denominators)
- **Config Files**: `config/analysis.yml` (efficiency thresholds, international benchmarks)

---

## ✅ Implementation Tasks

### Population Data Preparation
- [ ] Extract population estimates from admission rate data
- [ ] Validate population trends (should match Singapore statistics)
- [ ] Create annual population dataset

### Capacity Metrics Calculation
- [ ] Calculate beds per 1,000 population: `(total_beds / population) * 1000`
- [ ] Calculate by facility type: acute, intermediate, long-term care
- [ ] Calculate public vs private sector bed densities
- [ ] Compare against international benchmarks (WHO: 3-5 beds per 1,000)

### Proxy Occupancy Calculation
- [ ] Estimate admissions from admission rate: `rate * population / 1000`
- [ ] Estimate bed-days needed: `admissions * avg_length_of_stay` (assume or derive from data)
- [ ] Calculate proxy occupancy: `bed_days_needed / (total_beds * 365)`
- [ ] Handle missing average length of stay (use literature values: 5-7 days acute, 20-30 days intermediate)

### Utilization Index
- [ ] Calculate utilization growth rate: `(admissions_t - admissions_t-1) / admissions_t-1`
- [ ] Calculate capacity growth rate: `(beds_t - beds_t-1) / beds_t-1`
- [ ] Calculate utilization index: `utilization_growth / capacity_growth`
- [ ] Interpret: index >1 = demand outpacing supply, index <1 = supply outpacing demand

### Efficiency Classification
- [ ] Classify by proxy occupancy:
  - Under-utilized: <65%
  - Optimal: 65-85%
  - High: 85-90%
  - Over-capacity (strain): >90%
- [ ] Flag years and facility types with efficiency concerns

### Visualization
- [ ] Heatmap: proxy occupancy % by facility type and year
- [ ] Line chart: capacity trends vs utilization trends (dual-axis)
- [ ] Scatter plot: beds per 1,000 vs proxy occupancy (identify outliers)
- [ ] Export figures

### Testing & Validation
- [ ] Unit tests for metric calculations
- [ ] Validate beds per 1,000: compare against WHO reported values (if available)
- [ ] Test edge cases: zero beds, missing years

### Documentation
- [ ] Docstrings (Google style)
- [ ] Methodology document: `results/capacity_efficiency_methodology.md`
  - Proxy occupancy calculation rationale
  - Assumptions and limitations
  - International benchmark sources
- [ ] Update data dictionary

---

## 📌 Notes

**Beds per 1,000 Population (Polars)**:
```python
import polars as pl

df_density = (
    df_capacity
    .join(df_population, on='year', how='left')
    .with_columns([
        (pl.col('total_beds') / pl.col('population') * 1000).alias('beds_per_1000')
    ])
)
```

**Proxy Occupancy Calculation** (simplified):
```python
# Assume average length of stay (ALOS) from literature
ALOS_ACUTE = 5.5  # days (Singapore hospital average)

df_occupancy = (
    df_utilization
    .join(df_capacity, on=['year', 'facility_type'], how='inner')
    .with_columns([
        # Estimated bed-days needed
        (pl.col('annual_admissions') * ALOS_ACUTE).alias('bed_days_needed'),
        
        # Available bed-days
        (pl.col('total_beds') * 365).alias('bed_days_available'),
        
        # Proxy occupancy
        ((pl.col('bed_days_needed') / pl.col('bed_days_available')) * 100)
        .alias('proxy_occupancy_pct')
    ])
)
```

**Utilization Index**:
```python
df_index = (
    df.sort(['facility_type', 'year'])
    .with_columns([
        # Growth rates
        ((pl.col('annual_admissions') - pl.col('annual_admissions').shift(1)) 
         / pl.col('annual_admissions').shift(1))
        .over('facility_type')
        .alias('utilization_growth'),
        
        ((pl.col('total_beds') - pl.col('total_beds').shift(1)) 
         / pl.col('total_beds').shift(1))
        .over('facility_type')
        .alias('capacity_growth')
    ])
    .with_columns([
        (pl.col('utilization_growth') / pl.col('capacity_growth')).alias('utilization_index')
    ])
)
```

**International Benchmarks**:
- **WHO Minimum**: 3 beds per 1,000 population (essential services)
- **OECD Average**: ~5 beds per 1,000 population (acute care)
- **Target Occupancy**: 75-85% (balances efficiency and quality)
- **Singapore (2020)**: ~4.5 beds per 1,000 (estimate)

**Limitations to Document**:
- Proxy occupancy is simplified (actual occupancy requires discharge data)
- Average length of stay estimated from literature (not actual data)
- Does not account for seasonal variation or day-of-week patterns
- Aggregate metrics mask facility-level variation

**Expected Insights**:
- Acute care likely shows high occupancy (85-90%) - efficient but strained
- Long-term care likely shows lower occupancy (60-70%) - potential surplus or access issues
- Public sector likely higher occupancy than private (different demand patterns)
