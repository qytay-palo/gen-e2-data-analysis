"""Kaggle dataset extraction module for healthcare workforce and capacity data.

This module provides functionality to download and extract Singapore MOH workforce
and capacity datasets from Kaggle using the kagglehub API.
"""

import kagglehub
import polars as pl
from pathlib import Path
from loguru import logger
from typing import Dict, Optional
import sys

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parents[3]))
from src.data_processing.base_connection import BaseConnection


class KaggleConnection(BaseConnection):
    """Kaggle dataset connection handler."""
    
    def __init__(self, dataset_id: str):
        """
        Initialize Kaggle connection.
        
        Args:
            dataset_id: Kaggle dataset identifier (format: owner/dataset-name)
        """
        super().__init__(name="KaggleConnection")
        self.dataset_id = dataset_id
        self.dataset_path: Optional[Path] = None
    
    def connect(self) -> Path:
        """
        Download and cache Kaggle dataset.
        
        Returns:
            Path to cached dataset directory
            
        Raises:
            RuntimeError: If authentication fails or dataset cannot be downloaded
        """
        try:
            logger.info(f"Connecting to Kaggle dataset: {self.dataset_id}")
            dataset_path_str = kagglehub.dataset_download(self.dataset_id)
            self.dataset_path = Path(dataset_path_str)
            logger.info(f"Dataset cached at: {self.dataset_path}")
            return self.dataset_path
        except Exception as e:
            error_msg = f"Failed to download Kaggle dataset: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def test_connection(self) -> bool:
        """
        Test Kaggle API authentication and dataset accessibility.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.connect()
            return True
        except RuntimeError:
            return False


def extract_workforce_tables(
    dataset_path: Path,
    output_dir: Path
) -> Dict[str, pl.DataFrame]:
    """
    Extract workforce tables from Kaggle dataset.
    
    Args:
        dataset_path: Path to downloaded Kaggle dataset
        output_dir: Directory to save raw CSV files
        
    Returns:
        Dictionary mapping table names to Polars DataFrames
        
    Raises:
        FileNotFoundError: If expected tables are missing
        ValueError: If tables have invalid structure
    """
    workforce_tables = {
        'doctors': 'number-of-doctors/number-of-doctors.csv',
        'nurses': 'number-of-nurses-and-midwives/number-of-nurses-and-midwives.csv',
        'pharmacists': 'number-of-pharmacists/number-of-pharmacists.csv'
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted_data = {}
    
    for table_name, table_path in workforce_tables.items():
        full_path = dataset_path / table_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Workforce table not found: {full_path}")
        
        logger.info(f"Loading {table_name} from {table_path}")
        df = pl.read_csv(full_path)
        
        # Validate basic structure
        if df.shape[0] == 0:
            raise ValueError(f"Table {table_name} is empty")
        
        # Save to raw data directory
        output_path = output_dir / f"workforce_{table_name}.csv"
        df.write_csv(output_path)
        logger.info(f"Saved {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        extracted_data[table_name] = df
    
    return extracted_data


def extract_capacity_tables(
    dataset_path: Path,
    output_dir: Path
) -> Dict[str, pl.DataFrame]:
    """
    Extract capacity tables from Kaggle dataset.
    
    Args:
        dataset_path: Path to downloaded Kaggle dataset
        output_dir: Directory to save raw CSV files
        
    Returns:
        Dictionary mapping table names to Polars DataFrames
        
    Raises:
        FileNotFoundError: If expected tables are missing
        ValueError: If tables have invalid structure
    """
    capacity_tables = {
        'hospital_beds': 'health-facilities/health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv',
        'primary_care': 'health-facilities/health-facilities-primary-care-dental-clinics-and-pharmacies.csv'
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted_data = {}
    
    for table_name, table_path in capacity_tables.items():
        full_path = dataset_path / table_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Capacity table not found: {full_path}")
        
        logger.info(f"Loading {table_name} from {table_path}")
        df = pl.read_csv(full_path)
        
        # Validate basic structure
        if df.shape[0] == 0:
            raise ValueError(f"Table {table_name} is empty")
        
        # Save to raw data directory
        output_path = output_dir / f"capacity_{table_name}.csv"
        df.write_csv(output_path)
        logger.info(f"Saved {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        extracted_data[table_name] = df
    
    return extracted_data
