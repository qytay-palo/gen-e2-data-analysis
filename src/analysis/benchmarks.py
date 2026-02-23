"""
International Healthcare Workforce Benchmarks

This module contains benchmark values from WHO, OECD, and healthcare workforce planning literature
for comparison with Singapore healthcare metrics.

Data Sources:
- WHO: https://www.who.int/docs/default-source/documents/workforcedensity.pdf
- OECD Health Statistics 2025
- Healthcare Workforce Planning Domain Knowledge (internal)

References:
- docs/domain_knowledge/healthcare-workforce-planning.md
- docs/domain_knowledge/healthcare-system-sustainability-metrics.md
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class BenchmarkSource:
    """Metadata for benchmark data source."""
    organization: str
    year: int
    url: str
    notes: str


# Workforce-to-Bed Ratio Benchmarks
WORKFORCE_TO_BED_BENCHMARKS: Dict[str, float] = {
    'typical_min': 1.5,  # FTE per bed (lower end of typical range)
    'typical_max': 2.5,  # FTE per bed (upper end of typical range)
    'understaffed_threshold': 1.0,  # Below this indicates potential understaffing
    'overstaffed_threshold': 3.0,  # Above this may indicate overstaffing
}

WORKFORCE_TO_BED_SOURCE = BenchmarkSource(
    organization='Healthcare Workforce Planning Literature',
    year=2025,
    url='docs/domain_knowledge/healthcare-workforce-planning.md',
    notes='Ranges vary by healthcare system model (acute care vs. integrated care)'
)

# Workforce Density Benchmarks (per 1,000 population)
WORKFORCE_DENSITY_BENCHMARKS: Dict[str, float] = {
    'who_minimum': 4.45,  # Minimum health workers per 1,000 population (WHO)
    'oecd_doctors_avg': 3.5,  # Average doctors per 1,000 (OECD countries)
    'oecd_nurses_avg': 8.0,  # Average nurses per 1,000 (OECD countries)
    'developed_country_total': 12.0,  # Total health workers per 1,000 (developed countries)
}

WORKFORCE_DENSITY_SOURCE = BenchmarkSource(
    organization='WHO / OECD',
    year=2024,
    url='https://www.who.int/docs/default-source/documents/workforcedensity.pdf',
    notes='WHO minimum for adequate healthcare delivery; OECD averages for comparison'
)

# Doctor-to-Nurse Ratio Benchmarks
DOCTOR_TO_NURSE_BENCHMARKS: Dict[str, float] = {
    'typical_min': 0.25,  # 1 doctor : 4 nurses
    'typical_max': 0.50,  # 1 doctor : 2 nurses
    'optimal_range_mid': 0.33,  # 1 doctor : 3 nurses (common target)
}

DOCTOR_TO_NURSE_SOURCE = BenchmarkSource(
    organization='Healthcare Workforce Planning Literature',
    year=2025,
    url='docs/domain_knowledge/healthcare-workforce-planning.md',
    notes='Varies by care model; nursing-intensive models have lower ratios'
)

# Mismatch Detection Thresholds
MISMATCH_THRESHOLDS: Dict[str, float] = {
    'significant_divergence': 1.0,  # Growth rate difference > 1% considered significant
    'severe_divergence': 3.0,  # Growth rate difference > 3% considered severe
    'min_years_sustained': 3,  # Minimum years of divergence to flag as problematic
}

# Healthcare Expenditure Benchmarks
EXPENDITURE_BENCHMARKS: Dict[str, float] = {
    'who_out_of_pocket_max': 30.0,  # Out-of-pocket spending should be < 30% of total
    'oecd_health_expenditure_gdp': 8.8,  # Health expenditure as % of GDP (OECD average)
    'oecd_gdp_share_avg': 9.0,  # Healthcare as % of GDP (OECD average)
}

EXPENDITURE_SOURCE = BenchmarkSource(
    organization='WHO / OECD',
    year=2024,
    url='https://www.oecd.org/health/health-data.htm',
    notes='Financial sustainability benchmarks'
)

# All benchmarks consolidated
ALL_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    'workforce_to_bed': {
        'values': WORKFORCE_TO_BED_BENCHMARKS,
        'source': WORKFORCE_TO_BED_SOURCE
    },
    'workforce_density': {
        'values': WORKFORCE_DENSITY_BENCHMARKS,
        'source': WORKFORCE_DENSITY_SOURCE
    },
    'doctor_to_nurse': {
        'values': DOCTOR_TO_NURSE_BENCHMARKS,
        'source': DOCTOR_TO_NURSE_SOURCE
    },
    'mismatch_thresholds': {
        'values': MISMATCH_THRESHOLDS,
        'source': BenchmarkSource(
            organization='Internal Analysis Framework',
            year=2026,
            url='docs/methodology/',
            notes='Thresholds for flagging significant workforce-capacity misalignments'
        )
    },
    'expenditure': {
        'values': EXPENDITURE_BENCHMARKS,
        'source': EXPENDITURE_SOURCE
    }
}


def get_benchmark_description(benchmark_name: str) -> str:
    """
    Get a human-readable description of a benchmark and its source.
    
    Parameters
    ----------
    benchmark_name : str
        Name of the benchmark category ('workforce_to_bed', 'workforce_density', etc.)
        
    Returns
    -------
    str
        Formatted description with benchmark values and source information
        
    Example
    -------
    >>> print(get_benchmark_description('workforce_to_bed'))
    Workforce-to-Bed Ratio Benchmarks
    Typical Range: 1.5 - 2.5 FTE per bed
    Source: Healthcare Workforce Planning Literature (2025)
    """
    if benchmark_name not in ALL_BENCHMARKS:
        return f"Benchmark '{benchmark_name}' not found. Available: {list(ALL_BENCHMARKS.keys())}"
    
    benchmark = ALL_BENCHMARKS[benchmark_name]
    values = benchmark['values']
    source = benchmark['source']
    
    desc = f"\n{benchmark_name.replace('_', ' ').title()} Benchmarks\n"
    desc += "=" * 60 + "\n"
    
    for key, value in values.items():
        desc += f"{key.replace('_', ' ').title()}: {value}\n"
    
    desc += f"\nSource: {source.organization} ({source.year})\n"
    desc += f"Notes: {source.notes}\n"
    
    return desc
