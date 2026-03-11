"""
Unit Tests for BaseConnector
============================

Tests for the abstract base connector class.

Author: Gen-E2 Team
Date: 2026-03-11
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import polars as pl
from shared.src.data_processing.base_connector import BaseConnector


class MockConnector(BaseConnector):
    """Mock connector for testing BaseConnector."""
    
    def connect(self) -> bool:
        """Mock connect method."""
        return True
    
    def extract(self, **kwargs) -> pl.DataFrame:
        """Mock extract method."""
        return pl.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [10.5, 20.3, 15.7]
        })


class TestBaseConnector:
    """Test suite for BaseConnector."""
    
    @pytest.fixture
    def connector(self, tmp_path):
        """Create a mock connector instance."""
        return MockConnector(
            output_dir=str(tmp_path / "output"),
            log_dir=str(tmp_path / "logs")
        )
    
    @pytest.fixture
    def sample_df(self):
        """Create a sample Polars DataFrame."""
        return pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "disease": ["Dengue", "HFMD", "Influenza", "Dengue", "COVID-19"],
            "case_count": [100, 50, 75, 120, 200],
            "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
        })
    
    def test_connector_initialization(self, connector):
        """Test connector initialization creates directories."""
        assert connector.output_dir.exists()
        assert connector.log_dir.exists()
    
    def test_validate_connection_success(self, connector):
        """Test successful connection validation."""
        assert connector.validate_connection() is True
    
    def test_validate_connection_failure(self, connector):
        """Test failed connection validation."""
        connector.connect = Mock(return_value=False)
        assert connector.validate_connection() is False
    
    def test_save_data_parquet(self, connector, sample_df):
        """Test saving data in Parquet format."""
        success = connector.save_data(
            df=sample_df,
            filename="test_data",
            format="parquet",
            compression="snappy"
        )
        
        assert success is True
        
        # Verify file was created
        output_file = connector.output_dir / "test_data.parquet"
        assert output_file.exists()
        
        # Verify data can be read back
        loaded_df = pl.read_parquet(output_file)
        assert loaded_df.shape == sample_df.shape
        assert loaded_df.columns == sample_df.columns
    
    def test_save_data_csv(self, connector, sample_df):
        """Test saving data in CSV format."""
        success = connector.save_data(
            df=sample_df,
            filename="test_data_csv",
            format="csv"
        )
        
        assert success is True
        
        # Verify file was created
        output_file = connector.output_dir / "test_data_csv.csv"
        assert output_file.exists()
    
    def test_save_data_unsupported_format(self, connector, sample_df):
        """Test error handling for unsupported format."""
        success = connector.save_data(
            df=sample_df,
            filename="test_data",
            format="invalid_format"
        )
        
        assert success is False
    
    def test_log_extraction_metadata(self, connector):
        """Test extraction metadata logging."""
        connector.log_extraction_metadata(
            dataset_name="test_dataset",
            record_count=1000,
            extraction_time=5.5,
            additional_info={"source": "test_source"}
        )
        
        # Verify metadata file was created
        metadata_file = connector.log_dir / "extraction_metadata.log"
        assert metadata_file.exists()
        
        # Verify metadata was written
        content = metadata_file.read_text()
        assert "test_dataset" in content
        assert "1000" in content
    
    def test_handle_retry_success_first_attempt(self, connector):
        """Test retry logic with successful first attempt."""
        mock_func = Mock(return_value="success")
        
        result = connector.handle_retry(mock_func, max_retries=3)
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    def test_handle_retry_success_after_failures(self, connector):
        """Test retry logic with success after failures."""
        mock_func = Mock(side_effect=[Exception("fail"), Exception("fail"), "success"])
        
        result = connector.handle_retry(mock_func, max_retries=3, delay=0.1)
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    def test_handle_retry_all_failures(self, connector):
        """Test retry logic with all attempts failing."""
        mock_func = Mock(side_effect=Exception("fail"))
        
        result = connector.handle_retry(mock_func, max_retries=3, delay=0.1)
        
        assert result is None
        assert mock_func.call_count == 3
    
    def test_extract_method(self, connector):
        """Test extract method returns DataFrame."""
        df = connector.extract()
        
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3
        assert "name" in df.columns
