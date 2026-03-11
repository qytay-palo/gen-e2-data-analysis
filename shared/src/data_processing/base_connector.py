"""
Base Data Connector
===================

Abstract base class for all data connectors.
Provides common functionality for data extraction, logging, and error handling.

Author: Gen-E2 Team
Date: 2026-03-11
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger
import polars as pl
from datetime import datetime


class BaseConnector(ABC):
    """Abstract base class for data connectors."""
    
    def __init__(
        self,
        output_dir: str = "shared/data/1_raw",
        log_dir: str = "logs/etl",
    ):
        """
        Initialize the base connector.
        
        Args:
            output_dir: Directory to save extracted data
            log_dir: Directory for extraction logs
        """
        self.output_dir = Path(output_dir)
        self.log_dir = Path(log_dir)
        
        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        log_file = self.log_dir / f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logger.add(
            log_file,
            rotation="100 MB",
            retention="30 days",
            level="INFO"
        )
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to data source.
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def extract(self, **kwargs) -> Optional[pl.DataFrame]:
        """
        Extract data from source.
        
        Returns:
            Polars DataFrame containing extracted data, or None if extraction failed
        """
        pass
    
    def validate_connection(self) -> bool:
        """
        Validate connection before extraction.
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            logger.info("Validating connection...")
            is_connected = self.connect()
            
            if is_connected:
                logger.success("Connection validation passed")
            else:
                logger.error("Connection validation failed")
            
            return is_connected
            
        except Exception as e:
            logger.error(f"Connection validation error: {str(e)}")
            return False
    
    def save_data(
        self,
        df: pl.DataFrame,
        filename: str,
        format: str = "parquet",
        compression: str = "snappy"
    ) -> bool:
        """
        Save extracted data to file.
        
        Args:
            df: Polars DataFrame to save
            filename: Output filename (without extension)
            format: Output format ('parquet', 'csv', 'feather')
            compression: Compression algorithm
                        - For parquet: 'snappy', 'gzip', 'lz4', 'zstd'
                        - For feather: 'uncompressed', 'lz4', 'zstd'
                        - For csv: No compression
        
        Returns:
            True if save successful, False otherwise
        """
        try:
            filepath = self.output_dir / f"{filename}.{format}"
            
            logger.info(f"Saving data to {filepath}")
            logger.info(f"DataFrame shape: {df.shape}")
            
            if format == "parquet":
                df.write_parquet(filepath, compression=compression)
            elif format == "csv":
                df.write_csv(filepath)
            elif format == "feather":
                # Feather only supports specific compression types
                valid_ipc_compression = ['uncompressed', 'lz4', 'zstd']
                ipc_compression = compression if compression in valid_ipc_compression else 'lz4'
                df.write_ipc(filepath, compression=ipc_compression)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Log file size
            file_size_mb = filepath.stat().st_size / (1024 * 1024)
            logger.success(f"Data saved successfully: {file_size_mb:.2f} MB")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False
    
    def log_extraction_metadata(
        self,
        dataset_name: str,
        record_count: int,
        extraction_time: float,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        """
        Log metadata about the extraction.
        
        Args:
            dataset_name: Name of the extracted dataset
            record_count: Number of records extracted
            extraction_time: Time taken for extraction (seconds)
            additional_info: Additional metadata to log
        """
        metadata = {
            "dataset": dataset_name,
            "timestamp": datetime.now().isoformat(),
            "record_count": record_count,
            "extraction_time_seconds": extraction_time,
        }
        
        if additional_info:
            metadata.update(additional_info)
        
        logger.info(f"Extraction metadata: {metadata}")
        
        # Save metadata to file
        metadata_file = self.log_dir / "extraction_metadata.log"
        with open(metadata_file, "a") as f:
            f.write(f"{metadata}\n")
    
    def handle_retry(
        self,
        func,
        max_retries: int = 3,
        delay: float = 1.0,
        **kwargs
    ):
        """
        Retry logic for network failures.
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            delay: Delay between retries (seconds)
            **kwargs: Arguments to pass to function
        
        Returns:
            Function result if successful, None otherwise
        """
        import time
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries}")
                result = func(**kwargs)
                return result
            
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    return None
