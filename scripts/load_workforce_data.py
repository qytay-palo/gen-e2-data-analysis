"""
Load Workforce Data from SharePoint

This script dynamically loads all workforce CSV files from the SharePoint folder:
/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/

Files loaded:
- doctors.csv
- nurses.csv
- pharmacists.csv
- physiotherapists.csv

Author: Data Analytics Team
Last Updated: 17 April 2026
"""

import os
import sys
from pathlib import Path

import polars as pl
from dotenv import load_dotenv
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.src.data_processing.sharepoint_connector import (
    SharePointConnector,
    SharePointSettings,
)


def setup_logging():
    """Configure logging for the script"""
    log_dir = project_root / "logs" / "etl"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_dir / "workforce_data_{time}.log",
        rotation="1 day",
        retention="30 days",
        level="INFO"
    )


def validate_environment():
    """Validate required environment variables are set"""
    required_vars = [
        "SHAREPOINT_SITE_URL",
        "SHAREPOINT_WORKFORCE_FOLDER",
        "SHAREPOINT_USERNAME",
        "SHAREPOINT_PASSWORD",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please ensure these are set in your .env file"
        )

    logger.info("✓ Username/password SharePoint environment variables are set")


def load_workforce_data(save_local: bool = True):
    """
    Load all workforce data files from SharePoint
    
    Args:
        save_local: If True, save files to local data/1_raw/workforce/ folder
    
    Returns:
        dict: Dictionary containing workforce dataframes keyed by profession
    """
    # Get workforce folder from environment
    workforce_folder = os.getenv("SHAREPOINT_WORKFORCE_FOLDER")
    username = os.getenv("SHAREPOINT_USERNAME")
    password = os.getenv("SHAREPOINT_PASSWORD")

    settings = SharePointSettings(
        site_url=os.getenv("SHAREPOINT_SITE_URL", ""),
        workforce_folder=workforce_folder or "",
        username=username,
        password=password,
    )

    # Initialize connector with username/password auth only
    connector = SharePointConnector(settings=settings)

    logger.info(f"Loading workforce data from: {workforce_folder}")
    logger.info("Using SharePoint username/password authentication for this load")
    
    # Define workforce files
    workforce_files = [
        "doctors.csv",
        "nurses.csv",
        "pharmacists.csv",
        "physiotherapists.csv"
    ]
    
    workforce_data = {}
    total_records = 0
    
    # Load each file
    for filename in workforce_files:
        file_path = f"{workforce_folder}/{filename}"
        
        try:
            logger.info(f"Loading {filename}...")
            df = connector.extract_file(file_path)
            
            # Store with key based on filename
            key = filename.replace('.csv', '')
            workforce_data[key] = df
            
            record_count = len(df)
            total_records += record_count
            
            logger.info(
                f"✓ Loaded {filename}: "
                f"{record_count:,} records, "
                f"{len(df.columns)} columns"
            )
            
            # Save locally if requested
            if save_local:
                local_dir = project_root / "shared" / "data" / "1_raw" / "workforce"
                local_dir.mkdir(parents=True, exist_ok=True)
                
                local_file = local_dir / filename
                df.write_csv(local_file)
                logger.info(f"  → Saved to {local_file}")
            
        except Exception as e:
            logger.error(f"✗ Failed to load {filename}: {e}")
            raise
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Successfully loaded {len(workforce_data)} workforce datasets")
    logger.info(f"Total records: {total_records:,}")
    logger.info(f"{'='*60}\n")
    
    return workforce_data


def combine_workforce_data(workforce_data: dict) -> pl.DataFrame:
    """
    Combine all workforce datasets into a single DataFrame
    
    Args:
        workforce_data: Dictionary of workforce dataframes
    
    Returns:
        pl.DataFrame: Combined workforce data with profession column
    """
    logger.info("Combining workforce datasets...")
    
    combined_dfs = []
    
    for profession, df in workforce_data.items():
        # Add profession column for identification
        df_with_profession = df.with_columns(
            pl.lit(profession).alias('profession')
        )
        combined_dfs.append(df_with_profession)
    
    # Concatenate all datasets
    combined_df = pl.concat(combined_dfs, how="diagonal")
    
    logger.info(f"✓ Combined dataset: {len(combined_df):,} total records")
    
    return combined_df


def display_summary(workforce_data: dict):
    """Display summary statistics for loaded data"""
    logger.info("\nDataset Summary:")
    logger.info("─" * 60)
    
    for profession, df in workforce_data.items():
        logger.info(f"\n{profession.upper()}:")
        logger.info(f"  Records: {len(df):,}")
        logger.info(f"  Columns: {', '.join(df.columns)}")
        
        # Show year range if year column exists
        if 'year' in df.columns:
            year_min = df['year'].min()
            year_max = df['year'].max()
            logger.info(f"  Year range: {year_min} - {year_max}")


def main():
    """Main execution function"""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("WORKFORCE DATA LOADER")
    logger.info("=" * 60)
    
    try:
        # Validate environment
        validate_environment()
        
        # Load workforce data
        workforce_data = load_workforce_data(save_local=True)
        
        # Display summary
        display_summary(workforce_data)
        
        # Combine into single dataset (optional)
        combined_df = combine_workforce_data(workforce_data)
        
        # Save combined dataset
        combined_file = (
            project_root
            / "shared"
            / "data"
            / "1_raw"
            / "workforce"
            / "combined_workforce.csv"
        )
        combined_df.write_csv(combined_file)
        logger.info(f"\n✓ Combined dataset saved to: {combined_file}")
        
        logger.info("\n" + "=" * 60)
        logger.info("WORKFORCE DATA LOAD COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return workforce_data
        
    except Exception as e:
        logger.error(f"\n✗ Workforce data load failed: {e}")
        raise


if __name__ == "__main__":
    workforce_data = main()
