"""
Example: Extract Singapore Health Data from Kaggle
=================================================

This script demonstrates how to use the KaggleConnector to download
Singapore health-related datasets from Kaggle.

Usage:
    python shared/src/data_processing/examples/extract_kaggle_health_data.py

Author: Gen-E2 Team
Date: 2026-03-11
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.src.data_processing.kaggle_connector import KaggleConnector
from loguru import logger


def main():
    """Extract Singapore health datasets from Kaggle."""
    
    logger.info("=" * 80)
    logger.info("Singapore Health Data Extraction from Kaggle")
    logger.info("=" * 80)
    
    # Initialize connector (using kagglehub for credential-free access)
    connector = KaggleConnector(
        use_kagglehub=True,  # Use credential-free mode
        output_dir="shared/data/1_raw/kaggle"
    )
    
    # Example datasets related to Singapore health
    # NOTE: These are example dataset identifiers
    # Replace with actual Kaggle dataset identifiers after searching Kaggle
    
    datasets_to_extract = [
        {
            "dataset": "example/singapore-disease-surveillance",
            "file_name": "disease_data.csv",
            "output_name": "singapore_disease_surveillance"
        },
        {
            "dataset": "example/singapore-health-statistics",
            "file_name": None,  # Auto-detect first CSV file
            "output_name": "singapore_health_statistics"
        },
        # Add more datasets as needed
    ]
    
    successful_extractions = 0
    failed_extractions = 0
    
    for dataset_info in datasets_to_extract:
        logger.info("-" * 80)
        logger.info(f"Processing: {dataset_info['dataset']}")
        
        try:
            # Extract data
            df = connector.extract(
                dataset=dataset_info["dataset"],
                file_name=dataset_info.get("file_name")
            )
            
            if df is not None:
                # Save to standardized location
                success = connector.save_data(
                    df=df,
                    filename=dataset_info["output_name"],
                    format="parquet",  # Use Parquet for better performance
                    compression="snappy"
                )
                
                if success:
                    successful_extractions += 1
                    logger.success(f"Successfully extracted: {dataset_info['dataset']}")
                else:
                    failed_extractions += 1
                    logger.error(f"Failed to save: {dataset_info['dataset']}")
            else:
                failed_extractions += 1
                logger.error(f"Failed to extract: {dataset_info['dataset']}")
        
        except Exception as e:
            failed_extractions += 1
            logger.error(f"Error processing {dataset_info['dataset']}: {str(e)}")
    
    # Summary
    logger.info("=" * 80)
    logger.info("Extraction Summary")
    logger.info("=" * 80)
    logger.info(f"Total datasets: {len(datasets_to_extract)}")
    logger.info(f"Successful: {successful_extractions}")
    logger.info(f"Failed: {failed_extractions}")
    
    if successful_extractions > 0:
        logger.success("✓ Data extraction completed successfully")
    else:
        logger.warning("⚠ No datasets were successfully extracted")


if __name__ == "__main__":
    main()
