"""Configuration loader utility."""
import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_name: str = "analysis") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_name: Name of the config file (without .yml extension)
    
    Returns:
        Dictionary containing configuration parameters
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_path = Path(__file__).parents[2] / "config" / f"{config_name}.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config
