"""Unit tests for configuration loader."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parents[2] / "src"))

from utils.config_loader import load_config


def test_load_config():
    """Test loading analysis configuration."""
    config = load_config("analysis")
    
    assert "data" in config
    assert "target_diseases" in config["data"]
    assert len(config["data"]["target_diseases"]) > 0


def test_load_config_not_found():
    """Test loading non-existent configuration."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_config")
