# Model Capacity Expansion Scenarios (Lifecycle Stage: Optimization & Scenarios)

**Story ID**: PS-003-US-08  
**Epic**: Healthcare System Capacity & Utilization Optimization  
**Priority**: P1 (High)  
**Effort Estimate**: L (6-7 days)  
**Created**: March 11, 2026

---

## 📝 User Story Description

As a **Healthcare Infrastructure Planner evaluating investment options**,  
I want **to model capacity expansion scenarios testing different investment strategies (acute vs community vs long-term care) and their impact on utilization efficiency**,  
So that **I can recommend optimal infrastructure investment mix maximizing population health outcomes per dollar spent**.

---

## 🎯 Acceptance Criteria

1. **Scenario models developed**
   - Baseline scenario: current capacity trajectory projected forward
   - Scenario A: Prioritize acute care expansion
   - Scenario B: Prioritize community hospital expansion  
   - Scenario C: Prioritize long-term care expansion
   - Scenario D: Balanced expansion across facility types

2. **Scenario impacts quantified**
   - Projected bed occupancy rates under each scenario
   - Estimated wait times/access improvements
   - Cost implications per scenario
   - Population coverage metrics

3. **Optimization analysis performed**
   - Cost-effectiveness analysis: beds added per million dollar invested
   - Pareto frontier: identify efficient scenarios
   - Sensitivity analysis: how do results change with different assumptions?

4. **Deliverables**
   - Output: `results/tables/capacity_expansion_scenarios.csv`
   - Figures: Scenario comparison charts, cost-effectiveness curves
   - Decision support report: Recommended investment strategy

---

## 🔒 Technical Constraints

- **Platform**: Databricks Runtime 13.3.x, Python 3.9
- **Primary Library**: Polars 0.20+ for data; scipy/PuLP for optimization
- **Visualization**: Matplotlib/Plotly
- **Logging**: loguru
- **Testing**: pytest ≥80% coverage

---

## 📚 Domain Knowledge References

- [Domain Knowledge Research](../../../problem_statements/DOMAIN_KNOWLEDGE_RESEARCH.md#capacity-planning-optimization) - Optimization methods
- [Problem Statement PS-003](../../../problem_statements/ps-003-healthcare-capacity-optimization.md#objective-4) - Capacity optimization strategies

---

## 📦 Dependencies

### External Packages
- `polars>=0.20.0`, `scipy>=1.11.0`, `pulp>=2.7.0` (linear programming), `matplotlib>=3.8.0`, `loguru>=0.7.0`

### Internal Dependencies
- **Upstream**: PS-003-US-06 (Gap analysis - BLOCKING)
- **Data Sources**: `shared/data/3_interim/capacity_utilization_integrated.parquet`, `results/tables/capacity_gap_analysis.csv`
- **Config Files**: `config/analysis.yml` (cost assumptions, expansion targets)

---

## ✅ Implementation Tasks

### Scenario Definition
- [ ] Define baseline projection: linear extrapolation of current trends
- [ ] Define expansion scenarios: bed additions by facility type
- [ ] Set budget constraints: total investment available
- [ ] Define cost per bed by facility type (from domain knowledge)

### Impact Modeling
- [ ] Project utilization under each scenario
- [ ] Calculate occupancy rates: utilization / capacity
- [ ] Estimate wait time improvements (simplified proxy)
- [ ] Calculate population coverage changes

### Cost-Effectiveness Analysis
- [ ] Calculate cost per scenario
- [ ] Calculate benefits per scenario (e.g., beds added, occupancy improvement)
- [ ] Compute cost-effectiveness ratios
- [ ] Identify Pareto-efficient scenarios

### Optimization (Optional Advanced)
- [ ] Formulate as linear programming problem
- [ ] Objective: maximize access improvement subject to budget constraint
- [ ] Decision variables: beds to add per facility type
- [ ] Solve using PuLP or scipy.optimize

### Sensitivity Analysis
- [ ] Vary cost assumptions: ±20%
- [ ] Vary utilization growth projections
- [ ] Test different budget levels
- [ ] Assess robustness of recommendations

### Visualization
- [ ] Scenario comparison charts: capacity by facility type
- [ ] Cost-effectiveness frontier
- [ ] Occupancy rate projections
- [ ] Save figures: `reports/figures/capacity_scenarios_*.png/pdf`

### Decision Support Report
- [ ] Executive summary: recommended scenario
- [ ] Scenario details: assumptions, results
- [ ] Cost-benefit analysis
- [ ] Implementation roadmap

### Testing & Documentation
- [ ] Unit tests for scenario modeling functions
- [ ] Validate projections against baselines
- [ ] Docstrings
- [ ] Decision support report generation

---

## 📌 Notes

**Scenario Modeling Example**:
```python
import polars as pl
import numpy as np

# Baseline projection
df = pl.read_parquet("shared/data/3_interim/capacity_utilization_integrated.parquet")

# Calculate historical CAGR
cagr = 0.03  # 3% annual growth (example)

# Project 5 years forward
years_ahead = 5
baseline_capacity_2025 = current_capacity * (1 + cagr) ** years_ahead

# Scenario A: Add 500 acute care beds
scenario_a_capacity_2025 = baseline_capacity_2025 + 500

# Calculate occupancy
scenario_a_occupancy = projected_utilization_2025 / scenario_a_capacity_2025
```

**Cost Assumptions** (example, to be validated):
- **Acute care bed**: SGD 500k - 1M per bed (construction + equipment)
- **Community hospital bed**: SGD 300k - 500k per bed
- **Long-term care bed**: SGD 200k - 400k per bed

**Optimization Formulation** (if using LP):
```
Maximize: ∑(population_coverage_improvement_i * beds_added_i)
Subject to:
  ∑(cost_per_bed_i * beds_added_i) ≤ Budget
  beds_added_i ≥ 0
```

**Expected Recommendations**:
- **Balanced approach**: Likely most robust
- **Long-term care priority**: If elderly population growing rapidly
- **Community hospital focus**: If objective is to reduce acute care pressure
