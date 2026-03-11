"""
Kaggle Data Connector
====================

Connector for downloading datasets from Kaggle.
Supports both kagglehub (credential-free) and traditional Kaggle API approaches.

Author: Gen-E2 Team
Date: 2026-03-11
"""

from typing import Optional, List
from pathlib import Path
from loguru import logger
import polars as pl
import time
from .base_connector import BaseConnector


class KaggleConnector(BaseConnector):
    """
    Connector for Kaggle datasets.
    
    Supports two authentication methods:
    1. kagglehub (preferred, credential-free for public datasets)
    2. Kaggle API (requires API credentials)
    
    Example:
        >>> connector = KaggleConnector()
        >>> df = connector.extract(dataset="owner/dataset-name")
    """
    
    def __init__(
        self,
        use_kagglehub: bool = True,
        output_dir: str = "shared/data/1_raw/kaggle",
        log_dir: str = "logs/etl",
    ):
        """
        Initialize Kaggle connector.
        
        Args:
            use_kagglehub: If True, use kagglehub (credential-free).
                          If False, use traditional Kaggle API (requires credentials).
            output_dir: Directory to save downloaded datasets
            log_dir: Directory for extraction logs
        """
        super().__init__(output_dir, log_dir)
        self.use_kagglehub = use_kagglehub
        self._api = None
    
    def connect(self) -> bool:
        """
        Validate Kaggle API connection (if using Kaggle API).
        
        Returns:
            True if connection successful or using kagglehub, False otherwise
        """
        if self.use_kagglehub:
            logger.info("Using kagglehub (credential-free mode)")
            try:
                import kagglehub
                logger.success("kagglehub is available")
                return True
            except ImportError:
                logger.error("kagglehub not installed. Install with: uv pip install kagglehub")
                return False
        else:
            logger.info("Using Kaggle API (requires credentials)")
            try:
                from kaggle.api.kaggle_api_extended import KaggleApi
                
                api = KaggleApi()
                api.authenticate()
                self._api = api
                
                logger.success("Kaggle API authentication successful")
                return True
                
            except ImportError:
                logger.error("kaggle package not installed. Install with: uv pip install kaggle")
                return False
            except Exception as e:
                logger.error(f"Kaggle API authentication failed: {str(e)}")
                logger.info("Ensure ~/.kaggle/kaggle.json exists with valid credentials")
                return False
    
    def extract(
        self,
        dataset: str,
        file_name: Optional[str] = None,
        force_download: bool = False,
        **kwargs
    ) -> Optional[pl.DataFrame]:
        """
        Extract data from Kaggle dataset.
        
        Args:
            dataset: Kaggle dataset identifier (format: 'owner/dataset-name')
            file_name: Specific file to extract (if dataset contains multiple files).
                      If None, attempts to extract the first CSV file.
            force_download: If True, re-download even if file exists locally
            **kwargs: Additional arguments for data loading (e.g., separator for CSV)
        
        Returns:
            Polars DataFrame if successful, None otherwise
        
        Examples:
            >>> # Download entire dataset
            >>> df = connector.extract("owner/dataset-name")
            
            >>> # Download specific file from dataset
            >>> df = connector.extract("owner/dataset-name", file_name="data.csv")
        """
        if not self.validate_connection():
            return None
        
        try:
            start_time = time.time()
            logger.info(f"Extracting dataset: {dataset}")
            
            if self.use_kagglehub:
                df = self._extract_with_kagglehub(dataset, file_name, force_download, **kwargs)
            else:
                df = self._extract_with_api(dataset, file_name, force_download, **kwargs)
            
            if df is not None:
                extraction_time = time.time() - start_time
                logger.success(f"Extraction completed in {extraction_time:.2f}s")
                
                # Log metadata
                self.log_extraction_metadata(
                    dataset_name=dataset,
                    record_count=len(df),
                    extraction_time=extraction_time,
                    additional_info={
                        "columns": df.columns,
                        "shape": df.shape,
                        "method": "kagglehub" if self.use_kagglehub else "kaggle_api"
                    }
                )
            
            return df
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            return None
    
    def _extract_with_kagglehub(
        self,
        dataset: str,
        file_name: Optional[str],
        force_download: bool,
        **kwargs
    ) -> Optional[pl.DataFrame]:
        """Extract using kagglehub (credential-free)."""
        import kagglehub
        
        logger.info(f"Downloading dataset with kagglehub: {dataset}")
        
        # Download dataset
        dataset_path = kagglehub.dataset_download(dataset)
        logger.info(f"Dataset downloaded to: {dataset_path}")
        
        # Find and load data file
        dataset_dir = Path(dataset_path)
        return self._load_data_file(dataset_dir, file_name, **kwargs)
    
    def _extract_with_api(
        self,
        dataset: str,
        file_name: Optional[str],
        force_download: bool,
        **kwargs
    ) -> Optional[pl.DataFrame]:
        """Extract using traditional Kaggle API."""
        if not self._api:
            logger.error("Kaggle API not initialized")
            return None
        
        # Create download directory
        download_dir = self.output_dir / dataset.replace("/", "_")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Downloading dataset with Kaggle API: {dataset}")
        
        # Download dataset
        self._api.dataset_download_files(
            dataset,
            path=str(download_dir),
            unzip=True,
            force=force_download
        )
        
        logger.success(f"Dataset downloaded to: {download_dir}")
        
        # Find and load data file
        return self._load_data_file(download_dir, file_name, **kwargs)
    
    def _load_data_file(
        self,
        data_dir: Path,
        file_name: Optional[str],
        **kwargs
    ) -> Optional[pl.DataFrame]:
        """
        Load data file from directory.
        
        Args:
            data_dir: Directory containing data files
            file_name: Specific file to load, or None to auto-detect
            **kwargs: Additional arguments for data loading
        
        Returns:
            Polars DataFrame if successful, None otherwise
        """
        try:
            # If specific file requested, load it
            if file_name:
                file_path = data_dir / file_name
                if not file_path.exists():
                    logger.error(f"File not found: {file_path}")
                    return None
            else:
                # Auto-detect: find first CSV or Parquet file
                csv_files = list(data_dir.glob("*.csv"))
                parquet_files = list(data_dir.glob("*.parquet"))
                
                if csv_files:
                    file_path = csv_files[0]
                    logger.info(f"Auto-detected CSV file: {file_path.name}")
                elif parquet_files:
                    file_path = parquet_files[0]
                    logger.info(f"Auto-detected Parquet file: {file_path.name}")
                else:
                    logger.error(f"No CSV or Parquet files found in {data_dir}")
                    logger.info(f"Available files: {list(data_dir.glob('*'))}")
                    return None
            
            # Load file based on extension
            logger.info(f"Loading file: {file_path}")
            
            if file_path.suffix == ".csv":
                df = pl.read_csv(file_path, **kwargs)
            elif file_path.suffix == ".parquet":
                df = pl.read_parquet(file_path, **kwargs)
            else:
                logger.error(f"Unsupported file format: {file_path.suffix}")
                return None
            
            logger.success(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            logger.info(f"Columns: {df.columns}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading data file: {str(e)}")
            return None
    
    def list_dataset_files(self, dataset: str) -> List[str]:
        """
        List all files in a Kaggle dataset.
        
        Args:
            dataset: Kaggle dataset identifier (format: 'owner/dataset-name')
        
        Returns:
            List of file names in the dataset
        """
        if not self.validate_connection():
            return []
        
        try:
            if self.use_kagglehub:
                import kagglehub
                dataset_path = kagglehub.dataset_download(dataset)
                files = [f.name for f in Path(dataset_path).glob("*") if f.is_file()]
            else:
                if not self._api:
                    return []
                files_info = self._api.dataset_list_files(dataset).files
                files = [f.name for f in files_info]
            
            logger.info(f"Files in dataset '{dataset}': {files}")
            return files
            
        except Exception as e:
            logger.error(f"Error listing dataset files: {str(e)}")
            return []
