"""
Pytest Configuration and Shared Fixtures
========================================

Shared fixtures and configuration for all tests.

Author: Gen-E2 Team
Date: 2026-03-11
"""

import pytest
from pathlib import Path
import polars as pl
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """Create a temporary directory for test data."""
    data_dir = tmp_path_factory.mktemp("test_data")
    yield data_dir
    # Cleanup after all tests
    shutil.rmtree(data_dir, ignore_errors=True)


@pytest.fixture
def sample_disease_data():
    """
    Sample disease surveillance data for testing.
    
    Returns:
        Polars DataFrame with sample disease data
    """
    return pl.DataFrame({
        "date": [
            "2026-01-01", "2026-01-08", "2026-01-15", "2026-01-22",
            "2026-01-01", "2026-01-08", "2026-01-15", "2026-01-22",
        ],
        "disease": [
            "Dengue", "Dengue", "Dengue", "Dengue",
            "HFMD", "HFMD", "HFMD", "HFMD"
        ],
        "case_count": [120, 150, 135, 140, 80, 95, 85, 90],
        "region": [
            "North", "North", "North", "North",
            "South", "South", "South", "South"
        ]
    }).with_columns([
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d"),
        pl.col("disease").cast(pl.Categorical),
        pl.col("region").cast(pl.Categorical),
        pl.col("case_count").cast(pl.Int32)
    ])


@pytest.fixture
def sample_workforce_data():
    """
    Sample healthcare workforce data for testing.
    
    Returns:
        Polars DataFrame with sample workforce data
    """
    return pl.DataFrame({
        "year": [2024, 2024, 2024, 2025, 2025, 2025],
        "category": [
            "Doctors", "Nurses", "Allied Health",
            "Doctors", "Nurses", "Allied Health"
        ],
        "headcount": [15000, 45000, 20000, 15500, 47000, 21000],
        "forecast": [16000, 48000, 22000, 16500, 50000, 23000]
    }).with_columns([
        pl.col("category").cast(pl.Categorical),
        pl.col("headcount").cast(pl.Int32),
        pl.col("forecast").cast(pl.Int32)
    ])


@pytest.fixture
def sample_csv_file(tmp_path, sample_disease_data):
    """
    Create a sample CSV file for testing.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        sample_disease_data: Sample disease data fixture
    
    Returns:
        Path to the created CSV file
    """
    csv_path = tmp_path / "sample_disease_data.csv"
    sample_disease_data.write_csv(csv_path)
    return csv_path


@pytest.fixture
def sample_parquet_file(tmp_path, sample_disease_data):
    """
    Create a sample Parquet file for testing.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        sample_disease_data: Sample disease data fixture
    
    Returns:
        Path to the created Parquet file
    """
    parquet_path = tmp_path / "sample_disease_data.parquet"
    sample_disease_data.write_parquet(parquet_path, compression="snappy")
    return parquet_path


@pytest.fixture
def mock_kaggle_dataset(tmp_path):
    """
    Create a mock Kaggle dataset directory structure.
    
    Args:
        tmp_path: Pytest temporary directory fixture
    
    Returns:
        Path to mock dataset directory
    """
    dataset_dir = tmp_path / "mock_kaggle_dataset"
    dataset_dir.mkdir(parents=True)
    
    # Create sample CSV file
    df = pl.DataFrame({
        "id": [1, 2, 3],
        "name": ["Dataset A", "Dataset B", "Dataset C"],
        "value": [100, 200, 300]
    })
    
    df.write_csv(dataset_dir / "data.csv")
    
    return dataset_dir


@pytest.fixture
def mock_config():
    """
    Mock configuration for testing.
    
    Returns:
        Dictionary with test configuration
    """
    return {
        "data": {
            "target_diseases": ["Dengue", "HFMD", "Influenza"],
            "start_year": 2020,
            "end_year": 2026,
        },
        "logging": {
            "level": "INFO",
            "format": "{time} | {level} | {message}"
        },
        "analysis": {
            "confidence_level": 0.95,
            "significance_level": 0.05
        }
    }


def pytest_configure(config):
    """
    Custom pytest configuration.
    
    Register custom markers for test categorization.
    """
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for workflows"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers", "data: Data validation tests"
    )
    config.addinivalue_line(
        "markers", "databricks: Tests requiring Databricks connection"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test items during collection.
    
    Automatically mark tests based on their location.
    """
    for item in items:
        # Mark tests in unit/ directory as unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark tests in integration/ directory as integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark tests in data/ directory as data tests
        if "data" in str(item.fspath):
            item.add_marker(pytest.mark.data)
