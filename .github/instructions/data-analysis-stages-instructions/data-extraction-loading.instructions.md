---
name: 'Data Extraction and Loading Standards'
description: 'Best practices for extracting, loading, and managing raw data from various sources'
applyTo: 'data/1_raw/**, data/2_external/**, src/data_processing/*loader*.py, src/data_processing/*connector*.py, src/data_processing/*extractor*.py, scripts/extract*.py, notebooks/1_exploratory/*extract*.ipynb, notebooks/1_exploratory/*load*.ipynb, sql/extractions/**, docs/objectives/user_stories/**/*extract*.md, '
---

## Purpose
This document provides **mandatory guidelines** for data extraction and loading operations. Follow these practices when acquiring data from databases, APIs, files, or external sources.

## Core Principles

### 1. Data Immutability
- **NEVER modify files in `data/1_raw/`** after initial extraction
- Save extracted data with timestamps: `disease_data_20260217.csv`
- Use version suffixes for updated extractions: `disease_data_v2.csv`
- Document extraction metadata (source, timestamp, query) in companion files

### 2. Source Documentation
- **ALWAYS create a metadata file** alongside raw data files
- Include source URL, extraction date, query used, and row count
- Store metadata as JSON or YAML in same directory

### 3. Extraction Reproducibility
- Save exact SQL queries, API endpoints, and parameters used
- Use configuration files for extraction parameters (never hardcode)
- Log extraction statistics (rows extracted, duration, filters applied)

## Required Patterns

### Data Extraction Function Template

```python
from pathlib import Path
from datetime import datetime
import polars as pl
import yaml
from loguru import logger

def extract_disease_data(
    source_path: str,
    output_dir: str = 'data/1_raw',
    config_path: str = 'config/extraction.yml'
) -> tuple[pl.DataFrame, dict]:
    """Extract disease surveillance data from source.
    
    Args:
        source_path: Path to data source (file, URL, DB connection string)
        output_dir: Directory to save extracted data (default: data/1_raw)
        config_path: Path to extraction configuration file
        
    Returns:
        Tuple of (DataFrame, metadata dict)
        
    Raises:
        FileNotFoundError: If source file doesn't exist
        ValueError: If extraction fails validation
        
    Example:
        >>> df, meta = extract_disease_data('https://data.gov/disease.csv')
        >>> logger.info(f"Extracted {meta['row_count']} rows")
    """
    logger.info(f"Starting data extraction from: {source_path}")
    
    # Load extraction configuration
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Extract data
    try:
        df = pl.read_csv(source_path)
        logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
    
    # Generate metadata
    timestamp = datetime.now()
    metadata = {
        'source_path': source_path,
        'extraction_timestamp': timestamp.isoformat(),
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': df.columns,
        'dtypes': {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
        'file_size_bytes': Path(source_path).stat().st_size if Path(source_path).exists() else None,
        'extractor_version': '1.0.0'
    }
    
    # Save to raw directory with timestamp
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"disease_data_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
    output_file = output_path / filename
    df.write_csv(output_file)
    logger.info(f"Saved raw data to: {output_file}")
    
    # Save metadata
    meta_file = output_path / f"{filename.replace('.csv', '_metadata.yml')}"
    with open(meta_file, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False)
    logger.info(f"Saved metadata to: {meta_file}")
    
    return df, metadata
```

### SQL Extraction Template

**File Location**: `sql/extractions/extract_weekly_disease_cases.sql`

```sql
-- Purpose: Extract weekly infectious disease case counts
-- Source: surveillance_db.disease_cases table
-- Last Updated: 2026-02-17
-- Parameters: start_date, end_date, disease_list

SELECT 
    disease_name,
    epi_week,
    epi_year,
    CAST(reporting_date AS DATE) as reporting_date,
    SUM(case_count) as total_cases,
    COUNT(DISTINCT reporting_facility) as facility_count,
    MAX(last_updated) as data_timestamp
FROM surveillance_db.disease_cases
WHERE 
    reporting_date >= :start_date
    AND reporting_date <= :end_date
    AND disease_name IN :disease_list
    AND data_quality_flag = 'VALID'
GROUP BY 
    disease_name,
    epi_week,
    epi_year,
    reporting_date
ORDER BY 
    disease_name,
    epi_year,
    epi_week;

-- Expected row count: ~10,000-50,000 rows per year
-- Execution time: ~5-15 seconds
```

**Corresponding Python Extraction Script**:

```python
# scripts/extract_weekly_disease_cases.py
import polars as pl
import yaml
from pathlib import Path
from datetime import datetime
from loguru import logger

def execute_sql_extraction(
    sql_file: str,
    connection_string: str,
    params: dict,
    output_dir: str = 'data/1_raw'
) -> None:
    """Execute SQL extraction and save results.
    
    Args:
        sql_file: Path to SQL query file
        connection_string: Database connection string
        params: Query parameters (start_date, end_date, etc.)
        output_dir: Output directory for raw data
    """
    logger.info(f"Executing SQL extraction: {sql_file}")
    
    # Read SQL query
    with open(sql_file) as f:
        query = f.read()
    
    # Execute query (example using database connector)
    # Replace with actual DB library (sqlalchemy, psycopg2, etc.)
    df = pl.read_database(query, connection_string, **params)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(output_dir) / f"weekly_disease_cases_{timestamp}.csv"
    
    # Save extracted data
    df.write_csv(output_file)
    logger.info(f"Saved {len(df)} rows to {output_file}")
    
    # Save extraction metadata
    metadata = {
        'query_file': sql_file,
        'extraction_timestamp': datetime.now().isoformat(),
        'parameters': params,
        'row_count': len(df),
        'column_count': len(df.columns)
    }
    
    meta_file = output_file.with_suffix('.yml')
    with open(meta_file, 'w') as f:
        yaml.dump(metadata, f)
    
if __name__ == '__main__':
    # Load configuration
    with open('config/extraction.yml') as f:
        config = yaml.safe_load(f)
    
    execute_sql_extraction(
        sql_file='sql/extractions/extract_weekly_disease_cases.sql',
        connection_string=config['database']['connection_string'],
        params={
            'start_date': '2020-01-01',
            'end_date': '2024-12-31',
            'disease_list': config['target_diseases']
        }
    )
```

### API Extraction Template

```python
# src/data_processing/api_connector.py
import requests
import polars as pl
from typing import Optional, Dict, List
from loguru import logger
from datetime import datetime
from pathlib import Path
import time

class APIDataExtractor:
    """Extract data from REST APIs with retry logic and rate limiting."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        rate_limit_calls: int = 100,
        rate_limit_period: int = 60
    ):
        """Initialize API extractor.
        
        Args:
            base_url: Base URL for API
            api_key: Optional API key for authentication
            rate_limit_calls: Max API calls per period
            rate_limit_period: Rate limit period in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        self.call_timestamps: List[float] = []
        
    def _check_rate_limit(self) -> None:
        """Enforce rate limiting by delaying if necessary."""
        now = time.time()
        
        # Remove timestamps outside the current period
        self.call_timestamps = [
            ts for ts in self.call_timestamps 
            if now - ts < self.rate_limit_period
        ]
        
        # Wait if rate limit would be exceeded
        if len(self.call_timestamps) >= self.rate_limit_calls:
            sleep_time = self.rate_limit_period - (now - self.call_timestamps[0])
            logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
            
        self.call_timestamps.append(now)
    
    def extract_endpoint(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        max_retries: int = 3
    ) -> pl.DataFrame:
        """Extract data from API endpoint with retry logic.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            max_retries: Maximum retry attempts on failure
            
        Returns:
            DataFrame containing extracted data
            
        Raises:
            requests.HTTPError: If request fails after all retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
        
        for attempt in range(max_retries):
            try:
                self._check_rate_limit()
                
                logger.info(f"Fetching: {url} (attempt {attempt + 1}/{max_retries})")
                response = requests.get(url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                df = pl.DataFrame(data)
                logger.info(f"Successfully extracted {len(df)} records")
                return df
                
            except requests.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        
        raise RuntimeError(f"Failed to extract data after {max_retries} attempts")

# Usage example
if __name__ == '__main__':
    extractor = APIDataExtractor(
        base_url='https://api.data.gov/disease',
        api_key='YOUR_API_KEY',
        rate_limit_calls=100,
        rate_limit_period=60
    )
    
    df = extractor.extract_endpoint(
        endpoint='/weekly-cases',
        params={'year': 2024, 'disease': 'dengue'}
    )
    
    # Save to raw directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path('data/1_raw') / f'api_disease_data_{timestamp}.csv'
    df.write_csv(output_file)
```

## Extraction Checklist

Before completing any data extraction task, verify:

- [ ] **Source documented**: Created metadata file with source details
- [ ] **Timestamp included**: Filename includes extraction timestamp
- [ ] **Raw directory**: Data saved to `data/1_raw/` (never `data/4_processed/`)
- [ ] **Immutability**: Original source file not modified
- [ ] **Logging**: All extraction steps logged with INFO level
- [ ] **Error handling**: Try-except blocks catch and log failures
- [ ] **Configuration**: Extraction parameters in config file (not hardcoded)
- [ ] **Validation**: Row count and column names verified
- [ ] **SQL saved**: Query saved to `sql/extractions/` if applicable
- [ ] **API limits**: Rate limiting implemented if using APIs
- [ ] **Credentials**: No credentials committed to version control

## Anti-Patterns (AVOID)

```python
# ❌ DON'T: Hardcoded paths and parameters
df = pl.read_csv('/Users/john/desktop/data.csv')
diseases = ['Dengue', 'HFMD']  # Use config file instead

# ❌ DON'T: Modify raw data
df = pl.read_csv('data/1_raw/disease_data.csv')
df = df.drop_nulls()  # This is cleaning, not extraction
df.write_csv('data/1_raw/disease_data.csv')  # NEVER overwrite raw

# ❌ DON'T: Silent failures
try:
    df = pl.read_csv(source)
except:
    pass  # Should log error and raise

# ❌ DON'T: No metadata or documentation
df = pl.read_csv('http://api.data.com/download')
df.write_csv('data.csv')  # Where did this come from?

# ✅ DO: Proper extraction with documentation
df, metadata = extract_disease_data(
    source_path='http://api.data.com/download',
    output_dir='data/1_raw',
    config_path='config/extraction.yml'
)
# Metadata saved automatically with extraction details
```

## Configuration File Structure

**File**: `config/extraction.yml`

```yaml
# Data extraction configuration
version: '1.0.0'
last_updated: '2026-02-17'

# Database connections
database:
  host: 'localhost'
  port: 5432
  database: 'surveillance_db'
  schema: 'public'
  # Use environment variables for sensitive data
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}

# API configurations
api:
  base_url: 'https://api.data.gov/v1'
  api_key: ${API_KEY}
  rate_limit_calls: 100
  rate_limit_period: 60  # seconds
  timeout: 30

# Extraction parameters
extraction:
  date_range:
    start_date: '2020-01-01'
    end_date: '2024-12-31'
  
  target_diseases:
    - 'Dengue Fever'
    - 'Hand, Foot and Mouth Disease'
    - 'Influenza'
    - 'COVID-19'
  
  # Data quality filters
  filters:
    min_case_count: 0
    exclude_incomplete_weeks: true
    data_quality_flag: 'VALID'

# Output settings
output:
  raw_data_dir: 'data/1_raw'
  metadata_format: 'yaml'  # or 'json'
  include_timestamp: true
  compression: null  # or 'gzip', 'snappy'
```

## External Data Documentation

**File**: `data/2_external/README.md`

```markdown
# External Reference Data

This directory contains external reference data from third-party sources.

## Files

### population_demographics.csv
- **Source**: Singapore Department of Statistics
- **URL**: https://www.singstat.gov.sg/population
- **Download Date**: 2026-01-15
- **Description**: Population estimates by age group and planning area
- **Update Frequency**: Annual (last updated: 2025)
- **License**: Singapore Open Data License

### disease_taxonomy.json
- **Source**: WHO International Classification of Diseases (ICD-11)
- **URL**: https://icd.who.int/browse11
- **Download Date**: 2026-01-20
- **Description**: Disease codes and hierarchical classification
- **Update Frequency**: As needed (stable reference)
- **License**: WHO public use

### public_holidays.csv
- **Source**: Ministry of Manpower Singapore
- **URL**: https://www.mom.gov.sg/public-holidays
- **Download Date**: 2026-01-10
- **Description**: Singapore public holiday calendar 2020-2030
- **Usage**: Control variable for healthcare utilization patterns
```

## SQL Query Documentation Template

**File**: `sql/extractions/README.md`

```markdown
# SQL Extraction Queries

## Query Inventory

| File | Purpose | Source Table | Est. Rows | Runtime |
|------|---------|--------------|-----------|---------|
| extract_weekly_disease_cases.sql | Weekly aggregated cases | disease_cases | 50K/yr | 10s |
| extract_facility_data.sql | Healthcare facility info | facilities | 500 | 1s |
| extract_demographic_data.sql | Patient demographics | patient_demographics | 1M | 60s |

## Usage

Execute queries using the extraction script:

\`\`\`bash
python scripts/extract_from_database.py \
    --query sql/extractions/extract_weekly_disease_cases.sql \
    --output data/1_raw/disease_cases.csv \
    --params config/extraction_params.yml
\`\`\`

## Query Standards

All SQL queries must include:
1. Header comment with purpose and metadata
2. Parameters clearly marked with `:parameter_name`
3. Expected row count estimate
4. Execution time estimate
5. Data quality filters (WHERE clauses)
6. Explicit column selection (avoid SELECT *)
```

## Validation After Extraction

```python
def validate_extraction(
    df: pl.DataFrame,
    expected_columns: List[str],
    min_rows: int = 1
) -> None:
    """Validate extracted data meets minimum requirements.
    
    Args:
        df: Extracted DataFrame
        expected_columns: List of required column names
        min_rows: Minimum expected row count
        
    Raises:
        ValueError: If validation fails
    """
    # Check row count
    if len(df) < min_rows:
        raise ValueError(f"Expected at least {min_rows} rows, got {len(df)}")
    
    # Check columns
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check for completely null columns
    null_cols = [col for col in df.columns if df[col].null_count() == len(df)]
    if null_cols:
        logger.warning(f"Columns with all null values: {null_cols}")
    
    logger.info(f"Extraction validation passed: {len(df)} rows, {len(df.columns)} columns")
```

## Dynamic Data Extraction Workflow

Before starting any extraction work, use this workflow to check for existing data and configurations:

### 1. Check Existing Data Status

```python
from pathlib import Path
import yaml
from loguru import logger
from datetime import datetime

def check_extraction_status(project_root: str = '.') -> dict:
    """Check current data extraction status and existing configurations.
    
    Returns:
        Dictionary with status information about existing data and configs
    """
    project_path = Path(project_root)
    status = {
        'raw_data_exists': False,
        'raw_data_files': [],
        'extraction_config_exists': False,
        'extraction_config_path': None,
        'extraction_scripts': [],
        'recommended_action': None
    }
    
    # Check for raw data
    raw_data_path = project_path / 'data' / '1_raw'
    if raw_data_path.exists():
        raw_files = list(raw_data_path.glob('*'))
        raw_files = [f for f in raw_files if f.is_file() and not f.name.startswith('.')]
        status['raw_data_exists'] = len(raw_files) > 0
        status['raw_data_files'] = [f.name for f in raw_files]
    
    # Check for extraction configuration
    possible_configs = [
        project_path / 'config' / 'extraction.yml',
        project_path / 'config' / 'analysis.yml',
        project_path / 'config' / 'databricks.yml'
    ]
    
    for config_path in possible_configs:
        if config_path.exists():
            status['extraction_config_exists'] = True
            status['extraction_config_path'] = str(config_path)
            logger.info(f"Found configuration: {config_path}")
            break
    
    # Check for extraction scripts
    scripts_path = project_path / 'scripts'
    if scripts_path.exists():
        extraction_scripts = list(scripts_path.glob('*extract*.py')) + \
                           list(scripts_path.glob('*etl*.py'))
        status['extraction_scripts'] = [s.name for s in extraction_scripts]
    
    # Check SQL extraction queries
    sql_path = project_path / 'sql' / 'extractions'
    if sql_path.exists():
        sql_scripts = list(sql_path.glob('*.sql'))
        status['sql_extraction_queries'] = [s.name for s in sql_scripts]
    
    # Determine recommended action
    if status['raw_data_exists']:
        status['recommended_action'] = 'use_existing'
        logger.info(f"Found {len(status['raw_data_files'])} existing raw data files")
    elif status['extraction_config_exists']:
        status['recommended_action'] = 'run_extraction'
        logger.info("No raw data found, but extraction config exists - run extraction")
    else:
        status['recommended_action'] = 'create_config'
        logger.warning("No raw data or extraction config found - setup needed")
    
    return status

# Usage
status = check_extraction_status()
print(f"Raw data exists: {status['raw_data_exists']}")
print(f"Config available: {status['extraction_config_exists']}")
print(f"Recommended action: {status['recommended_action']}")
```

### 2. Dynamic Data Extraction Based on Status

```python
def execute_dynamic_extraction(
    project_root: str = '.',
    force_reextract: bool = False
) -> None:
    """Dynamically execute data extraction based on project status.
    
    Args:
        project_root: Root directory of the project
        force_reextract: Force re-extraction even if data exists
    """
    from pathlib import Path
    import yaml
    import polars as pl
    
    # Check current status
    status = check_extraction_status(project_root)
    project_path = Path(project_root)
    
    # Decision logic
    if status['raw_data_exists'] and not force_reextract:
        logger.info("Raw data already exists - skipping extraction")
        logger.info(f"Existing files: {', '.join(status['raw_data_files'])}")
        return
    
    # Load configuration (prioritize extraction.yml, fallback to analysis.yml)
    config = None
    config_paths = [
        project_path / 'config' / 'extraction.yml',
        project_path / 'config' / 'analysis.yml'
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            logger.info(f"Loading configuration from: {config_path}")
            with open(config_path) as f:
                config = yaml.safe_load(f)
            break
    
    if not config:
        raise FileNotFoundError(
            "No extraction configuration found. Create config/extraction.yml or config/analysis.yml"
        )
    
    # Extract data based on configuration
    # This is a template - customize based on your data sources
    
    # Example 1: If config specifies raw data path
    if 'data' in config and 'raw_data_path' in config['data']:
        raw_path = project_path / config['data']['raw_data_path']
        raw_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Raw data directory ready: {raw_path}")
    
    # Example 2: If config specifies data sources
    if 'sources' in config:
        for source_name, source_config in config['sources'].items():
            logger.info(f"Extracting from source: {source_name}")
            extract_from_source(source_config, raw_path)
    
    # Example 3: If using SQL extractions
    if status.get('sql_extraction_queries'):
        for sql_file in status['sql_extraction_queries']:
            logger.info(f"Executing SQL extraction: {sql_file}")
            execute_sql_extraction(
                sql_file=project_path / 'sql' / 'extractions' / sql_file,
                config=config
            )
    
    # Example 4: If using extraction scripts
    if status['extraction_scripts']:
        import subprocess
        for script in status['extraction_scripts']:
            script_path = project_path / 'scripts' / script
            logger.info(f"Running extraction script: {script}")
            subprocess.run(['python', str(script_path)], check=True)
    
    logger.info("Dynamic extraction completed")

def extract_from_source(source_config: dict, output_dir: Path) -> None:
    """Extract data from a configured source.
    
    Args:
        source_config: Source configuration dictionary
        output_dir: Output directory for raw data
    """
    source_type = source_config.get('type', 'file')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if source_type == 'file':
        # File-based extraction
        source_path = source_config['path']
        df = pl.read_csv(source_path)
        
        output_file = output_dir / f"{source_config.get('name', 'data')}_{timestamp}.csv"
        df.write_csv(output_file)
        logger.info(f"Extracted {len(df)} rows to {output_file}")
        
    elif source_type == 'api':
        # API-based extraction
        from src.data_processing.api_connector import APIDataExtractor
        
        extractor = APIDataExtractor(
            base_url=source_config['base_url'],
            api_key=source_config.get('api_key')
        )
        
        df = extractor.extract_endpoint(
            endpoint=source_config['endpoint'],
            params=source_config.get('params', {})
        )
        
        output_file = output_dir / f"{source_config.get('name', 'api_data')}_{timestamp}.csv"
        df.write_csv(output_file)
        logger.info(f"Extracted {len(df)} rows to {output_file}")
        
    elif source_type == 'database':
        # Database extraction
        connection_string = source_config.get('connection_string')
        query = source_config.get('query')
        
        df = pl.read_database(query, connection_string)
        
        output_file = output_dir / f"{source_config.get('name', 'db_data')}_{timestamp}.csv"
        df.write_csv(output_file)
        logger.info(f"Extracted {len(df)} rows to {output_file}")
    
    # Save metadata
    metadata = {
        'source': source_config.get('name', 'unknown'),
        'extraction_timestamp': datetime.now().isoformat(),
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': df.columns,
        'source_config': source_config
    }
    
    meta_file = output_file.with_suffix('.yml')
    with open(meta_file, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False)
```

### 3. Configuration Template for Extraction

If no extraction config exists, create `config/extraction.yml` with this template:

```yaml
# Data extraction configuration
version: '1.0.0'
last_updated: '2026-02-23'

# Data sources configuration
sources:
  disease_surveillance:
    type: 'file'  # or 'api', 'database'
    name: 'disease_surveillance_data'
    path: 'path/to/source/data.csv'  # or URL for API
    description: 'Weekly disease surveillance data'
    
  # Example API source
  # weather_data:
  #   type: 'api'
  #   name: 'weather_api_data'
  #   base_url: 'https://api.weather.com/v1'
  #   endpoint: '/daily-weather'
  #   api_key: ${WEATHER_API_KEY}
  #   params:
  #     start_date: '2020-01-01'
  #     end_date: '2024-12-31'
  
  # Example database source
  # patient_records:
  #   type: 'database'
  #   name: 'patient_data'
  #   connection_string: ${DB_CONNECTION_STRING}
  #   query: 'SELECT * FROM patients WHERE updated_at >= :start_date'
  #   params:
  #     start_date: '2020-01-01'

# Output configuration
output:
  raw_data_dir: 'data/1_raw'
  external_data_dir: 'data/2_external'
  metadata_format: 'yaml'
  include_timestamp: true
  
# Extraction parameters
extraction:
  date_range:
    start_date: '2020-01-01'
    end_date: null  # null means current date
  
  batch_size: 10000  # For large extractions
  retry_attempts: 3
  timeout_seconds: 300

# Data validation
validation:
  min_rows: 1
  required_columns: []
  check_duplicates: true
  check_nulls: true
```

### 4. Complete Extraction Workflow Script

Save as `scripts/extract_data.py`:

```python
#!/usr/bin/env python3
"""
Dynamic data extraction script.
Automatically detects and uses existing configurations.
"""
import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from utils.logger import setup_logger
from loguru import logger

# Import the dynamic extraction functions defined above
# (In practice, these would be in src/data_processing/extraction.py)

def main():
    """Main extraction execution."""
    parser = argparse.ArgumentParser(description='Extract data dynamically')
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-extraction even if data exists'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check status, do not extract'
    )
    args = parser.parse_args()
    
    setup_logger("data_extraction", "logs/etl")
    
    logger.info("Starting dynamic data extraction workflow")
    
    # Check current status
    status = check_extraction_status()
    
    logger.info(f"Raw data exists: {status['raw_data_exists']}")
    logger.info(f"Configuration available: {status['extraction_config_exists']}")
    logger.info(f"Recommended action: {status['recommended_action']}")
    
    if status['raw_data_files']:
        logger.info(f"Existing raw files: {', '.join(status['raw_data_files'])}")
    
    if args.check_only:
        logger.info("Check-only mode - exiting without extraction")
        return
    
    # Execute extraction
    try:
        execute_dynamic_extraction(force_reextract=args.force)
        logger.info("Data extraction completed successfully")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise

if __name__ == "__main__":
    main()
```

### 5. Usage Examples

```bash
# Check if data exists without extracting
python scripts/extract_data.py --check-only

# Extract data (skips if data already exists)
python scripts/extract_data.py

# Force re-extraction even if data exists
python scripts/extract_data.py --force

# Use with uv
uv run python scripts/extract_data.py
```

### 6. Integration with Existing Project

The dynamic workflow automatically:
- ✅ Detects existing data in `data/1_raw/`
- ✅ Finds and uses existing configs (`config/analysis.yml`, `config/databricks.yml`)
- ✅ Locates extraction scripts in `scripts/`
- ✅ Discovers SQL queries in `sql/extractions/`
- ✅ Creates necessary directories if missing
- ✅ Saves metadata with timestamps
- ✅ Logs all operations

## Summary

Key takeaways for data extraction:
1. **Never modify raw data** - treat `data/1_raw/` as read-only after extraction
2. **Document everything** - save metadata with every extraction
3. **Use configurations** - avoid hardcoding parameters
4. **Log extensively** - track what was extracted, when, and from where
5. **Handle errors gracefully** - implement retries and informative error messages
6. **Validate immediately** - check row counts and column schemas after extraction
7. **Check before extracting** - use dynamic workflow to avoid duplicate work
8. **Leverage existing configs** - reuse project configurations when available
