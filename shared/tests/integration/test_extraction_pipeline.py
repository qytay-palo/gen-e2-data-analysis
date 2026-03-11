"""
Integration Test for Data Extraction Pipeline
=============================================

Tests the end-to-end data extraction workflow.

Author: Gen-E2 Team
Date: 2026-03-11
"""

import pytest
from pathlib import Path
import polars as pl
from shared.src.data_processing.base_connector import BaseConnector


class SimpleTestConnector(BaseConnector):
    """Simple test connector for integration testing."""
    
    def __init__(self, test_data: pl.DataFrame, **kwargs):
        """Initialize with test data."""
        super().__init__(**kwargs)
        self.test_data = test_data
    
    def connect(self) -> bool:
        """Simulate successful connection."""
        return True
    
    def extract(self, **kwargs) -> pl.DataFrame:
        """Return test data."""
        return self.test_data


@pytest.mark.integration
class TestDataExtractionPipeline:
    """Integration tests for data extraction pipeline."""
    
    def test_end_to_end_extraction_workflow(self, tmp_path, sample_disease_data):
        """
        Test complete extraction workflow:
        1. Connect to source
        2. Extract data
        3. Validate data
        4. Save to disk
        5. Reload and verify
        """
        # Step 1: Create connector
        connector = SimpleTestConnector(
            test_data=sample_disease_data,
            output_dir=str(tmp_path / "output"),
            log_dir=str(tmp_path / "logs")
        )
        
        # Step 2: Validate connection
        assert connector.validate_connection() is True
        
        # Step 3: Extract data
        extracted_df = connector.extract()
        assert isinstance(extracted_df, pl.DataFrame)
        assert len(extracted_df) > 0
        
        # Step 4: Basic data validation
        assert "disease" in extracted_df.columns
        assert "case_count" in extracted_df.columns
        assert "date" in extracted_df.columns
        
        # Validate data types
        assert extracted_df["disease"].dtype == pl.Categorical
        assert extracted_df["case_count"].dtype == pl.Int32
        assert extracted_df["date"].dtype == pl.Date
        
        # Step 5: Save data
        success = connector.save_data(
            df=extracted_df,
            filename="disease_surveillance",
            format="parquet",
            compression="snappy"
        )
        assert success is True
        
        # Step 6: Reload and verify
        output_file = tmp_path / "output" / "disease_surveillance.parquet"
        assert output_file.exists()
        
        reloaded_df = pl.read_parquet(output_file)
        
        # Verify data integrity
        assert reloaded_df.shape == extracted_df.shape
        assert reloaded_df.columns == extracted_df.columns
        
        # Verify data types preserved
        assert reloaded_df["disease"].dtype == pl.Categorical
        assert reloaded_df["case_count"].dtype == pl.Int32
    
    def test_extraction_with_transformation(self, tmp_path, sample_disease_data):
        """Test extraction with data transformation pipeline."""
        connector = SimpleTestConnector(
            test_data=sample_disease_data,
            output_dir=str(tmp_path / "output"),
            log_dir=str(tmp_path / "logs")
        )
        
        # Extract data
        df = connector.extract()
        
        # Apply transformations
        df_transformed = (
            df
            .filter(pl.col("case_count") > 85)  # Filter low counts
            .group_by("disease")
            .agg([
                pl.col("case_count").mean().alias("avg_cases"),
                pl.col("case_count").max().alias("max_cases"),
                pl.col("case_count").count().alias("num_weeks")
            ])
            .sort("avg_cases", descending=True)
        )
        
        # Save transformed data
        connector.save_data(
            df=df_transformed,
            filename="disease_summary",
            format="parquet"
        )
        
        # Verify transformed data
        output_file = tmp_path / "output" / "disease_summary.parquet"
        assert output_file.exists()
        
        reloaded_df = pl.read_parquet(output_file)
        assert "avg_cases" in reloaded_df.columns
        assert "max_cases" in reloaded_df.columns
        assert "num_weeks" in reloaded_df.columns
    
    def test_multiple_format_exports(self, tmp_path, sample_disease_data):
        """Test exporting data in multiple formats."""
        connector = SimpleTestConnector(
            test_data=sample_disease_data,
            output_dir=str(tmp_path / "output"),
            log_dir=str(tmp_path / "logs")
        )
        
        df = connector.extract()
        
        # Export in multiple formats
        formats = ["parquet", "csv", "feather"]
        
        for fmt in formats:
            success = connector.save_data(
                df=df,
                filename=f"disease_data_{fmt}",
                format=fmt
            )
            assert success is True
        
        # Verify all files exist
        output_dir = tmp_path / "output"
        assert (output_dir / "disease_data_parquet.parquet").exists()
        assert (output_dir / "disease_data_csv.csv").exists()
        assert (output_dir / "disease_data_feather.feather").exists()
    
    def test_extraction_logging(self, tmp_path, sample_disease_data):
        """Test that extraction creates proper logs."""
        connector = SimpleTestConnector(
            test_data=sample_disease_data,
            output_dir=str(tmp_path / "output"),
            log_dir=str(tmp_path / "logs")
        )
        
        # Extract data and log metadata
        df = connector.extract()
        
        connector.log_extraction_metadata(
            dataset_name="disease_surveillance",
            record_count=len(df),
            extraction_time=1.5,
            additional_info={
                "source": "test_source",
                "diseases": df["disease"].unique().to_list()
            }
        )
        
        # Verify log file exists
        log_dir = tmp_path / "logs"
        metadata_file = log_dir / "extraction_metadata.log"
        assert metadata_file.exists()
        
        # Verify log content
        content = metadata_file.read_text()
        assert "disease_surveillance" in content
        assert "test_source" in content
