"""Data validation tests."""
import pytest
from pathlib import Path


def test_raw_data_directory_exists():
    """Test that raw data directory exists."""
    raw_data_path = Path("data/1_raw")
    assert raw_data_path.exists()
    assert raw_data_path.is_dir()


def test_processed_data_directory_exists():
    """Test that processed data directory exists."""
    processed_data_path = Path("data/4_processed")
    assert processed_data_path.exists()
    assert processed_data_path.is_dir()
