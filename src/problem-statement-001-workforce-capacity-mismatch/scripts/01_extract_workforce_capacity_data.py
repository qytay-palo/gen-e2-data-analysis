"""Main extraction script for healthcare workforce and capacity data.

This script orchestrates the extraction of workforce and capacity data from Kaggle,
performs data quality profiling, and generates comprehensive quality reports.

Usage:
    python scripts/01_extract_workforce_capacity_data.py

Requirements:
    - Kaggle API credentials configured in ~/.kaggle/kaggle.json
    - Required packages: kagglehub, polars, loguru
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parents[3]))
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.utils.logger import setup_logger
from data_processing.kaggle_extractor import (
    KaggleConnection,
    extract_workforce_tables,
    extract_capacity_tables
)
from data_processing.data_profiler import (
    profile_dataframe,
    detect_duplicates,
    generate_quality_report
)


def main():
    """Main extraction and profiling workflow."""
    
    # Setup logging
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    setup_logger("workforce_extraction", "logs/etl")
    
    logger.info("=" * 80)
    logger.info("WORKFORCE AND CAPACITY DATA EXTRACTION - START")
    logger.info("=" * 80)
    
    try:
        # Configuration
        DATASET_ID = "subhamjain/health-dataset-complete-singapore"
        OUTPUT_DIR = Path("data/1_raw")
        REPORT_DIR = Path("logs/etl")
        
        # Step 1: Connect to Kaggle and download dataset
        logger.info("Step 1: Connecting to Kaggle dataset")
        kaggle_conn = KaggleConnection(DATASET_ID)
        
        if not kaggle_conn.test_connection():
            logger.error("Kaggle connection test failed - check credentials")
            sys.exit(1)
        
        dataset_path = kaggle_conn.connect()
        logger.info(f"Dataset available at: {dataset_path}")
        
        # Step 2: Extract workforce tables
        logger.info("Step 2: Extracting workforce tables (doctors, nurses, pharmacists)")
        workforce_data = extract_workforce_tables(dataset_path, OUTPUT_DIR)
        logger.info(f"Extracted {len(workforce_data)} workforce tables")
        
        # Step 3: Extract capacity tables
        logger.info("Step 3: Extracting capacity tables (hospital beds, primary care)")
        capacity_data = extract_capacity_tables(dataset_path, OUTPUT_DIR)
        logger.info(f"Extracted {len(capacity_data)} capacity tables")
        
        # Step 4: Profile all extracted data
        logger.info("Step 4: Profiling extracted data")
        all_profiles = {}
        
        for table_name, df in workforce_data.items():
            profile = profile_dataframe(df, f"workforce_{table_name}")
            all_profiles[f"workforce_{table_name}"] = profile
            
            # Check for duplicates
            dup_count, dup_rows = detect_duplicates(df)
            if dup_count > 0:
                logger.warning(f"Found {dup_count} duplicates in workforce_{table_name}")
        
        for table_name, df in capacity_data.items():
            profile = profile_dataframe(df, f"capacity_{table_name}")
            all_profiles[f"capacity_{table_name}"] = profile
            
            # Check for duplicates
            dup_count, dup_rows = detect_duplicates(df)
            if dup_count > 0:
                logger.warning(f"Found {dup_count} duplicates in capacity_{table_name}")
        
        # Step 5: Generate quality report
        logger.info("Step 5: Generating data quality report")
        report_path = REPORT_DIR / f"data_quality_report_{timestamp}.md"
        generate_quality_report(all_profiles, report_path)
        
        logger.info("=" * 80)
        logger.info("EXTRACTION AND PROFILING COMPLETED SUCCESSFULLY")
        logger.info(f"Raw data saved to: {OUTPUT_DIR}")
        logger.info(f"Quality report saved to: {report_path}")
        logger.info("=" * 80)
        
    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
