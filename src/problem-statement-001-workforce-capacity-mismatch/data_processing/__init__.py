"""Data processing modules for Problem Statement 001: Workforce Capacity Mismatch Analysis."""

from .kaggle_extractor import KaggleConnection, extract_workforce_tables, extract_capacity_tables
from .data_profiler import profile_dataframe, detect_duplicates, identify_outliers, generate_quality_report

__all__ = [
    'KaggleConnection',
    'extract_workforce_tables',
    'extract_capacity_tables',
    'profile_dataframe',
    'detect_duplicates',
    'identify_outliers',
    'generate_quality_report',
]
