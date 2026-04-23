# Data Sources: MOH Workforce Trends Analysis

**Last Updated:** 23 April 2026  
**Status:** Active, Fully Documented

---

## Primary Data Source: SharePoint (Ministry of Health)

### Overview

**Source**: Ministry of Health SharePoint  
**Site**: TestSite-FileSync  
**Site URL**: `https://paloit2016.sharepoint.com/sites/TestSite-FileSync`  
**Primary Folder**: `Shared Documents/gen-e2-data-analysis test/`  
**Data Domain**: Healthcare Workforce Analytics  
**Access Method**: SharePoint REST API / Microsoft Graph API  
**Format**: CSV files  
**Update Frequency**: Monthly (varies by dataset)  
**Data Quality**: Enterprise-grade with governance controls

### Data Repository Structure

**SharePoint Site**: TestSite-FileSync  
**Primary Data Folder**: `Shared Documents/gen-e2-data-analysis test/`

**Available Datasets:**
- `doctors.csv` - Doctor workforce data
- `nurses.csv` - Nursing staff data
- `pharmacists.csv` - Pharmacist workforce data
- `physiotherapists.csv` - Physiotherapist workforce data

### Data Categories & Coverage

| Dataset File | Description | Update Frequency | Format |
|--------------|-------------|------------------|--------|
| `doctors.csv` | Medical doctors workforce data | Monthly | CSV |
| `nurses.csv` | Registered nurses and midwives data | Monthly | CSV |
| `pharmacists.csv` | Pharmacist workforce data | Monthly | CSV |
| `physiotherapists.csv` | Physiotherapist workforce data | Monthly | CSV |

**Data Location**: `Shared Documents/gen-e2-data-analysis test/`
**Local landing zone**: `shared/data/1_raw/workforce/`

**Primary stakeholder for this delivery**: Team lead

---

## Data Access & Connection

### Method 1: SharePoint REST API (Recommended for Automation)

```python
import os
import polars as pl
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from pathlib import Path
import io

# Load credentials from environment variables
site_url = os.getenv("SHAREPOINT_SITE_URL")
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")

# Authenticate using credentials
ctx = ClientContext(site_url).with_credentials(
    UserCredential(username, password)
)

# Define workforce data folder
workforce_folder_path = "Shared Documents/gen-e2-data-analysis test"

# List of workforce files to download
workforce_files = ["doctors.csv", "nurses.csv", "pharmacists.csv", "physiotherapists.csv"]

# Download and load all workforce files dynamically
workforce_data = {}

for filename in workforce_files:
    file_url = f"{workforce_folder_path}/{filename}"
    
    # Download file
    response = ctx.web.get_file_by_server_relative_url(file_url).download()
    ctx.execute_query()
    
    # Load into Polars DataFrame
    csv_content = response.value.decode('utf-8')
    df = pl.read_csv(io.StringIO(csv_content))
    
    # Store with key based on filename (without extension)
    key = filename.replace('.csv', '')
    workforce_data[key] = df
    print(f"✓ Loaded {filename}: {len(df)} records")

# Access individual datasets
doctors_df = workforce_data['doctors']
nurses_df = workforce_data['nurses']
pharmacists_df = workforce_data['pharmacists']
physiotherapists_df = workforce_data['physiotherapists']

print(f"\nTotal datasets loaded: {len(workforce_data)}")
```

**Advantages:**
- ✓ Automated scheduled extraction
- ✓ Programmatic access to metadata
- ✓ Works with CI/CD pipelines
- ✓ Access control and audit logging

### Method 2: Microsoft Graph API (Modern Approach)

```python
import os
from msal import ConfidentialClientApplication
import requests
import polars as pl
import io

# Load Azure AD credentials from environment variables
client_id = os.getenv("SHAREPOINT_CLIENT_ID")
client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
site_id = os.getenv("SHAREPOINT_SITE_ID")
drive_id = os.getenv("SHAREPOINT_DRIVE_ID")

authority = f"https://login.microsoftonline.com/{tenant_id}"

app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

# Get access token
token = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" not in token:
    raise Exception(f"Authentication failed: {token.get('error_description')}")

headers = {"Authorization": f"Bearer {token['access_token']}"}

# Define workforce files
workforce_folder = "Shared Documents/gen-e2-data-analysis test"
workforce_files = ["doctors.csv", "nurses.csv", "pharmacists.csv", "physiotherapists.csv"]

# Download and load all workforce files dynamically
workforce_data = {}

for filename in workforce_files:
    file_path = f"{workforce_folder}/{filename}"
    
    # Build Graph API URL
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{file_path}:/content"
    
    # Download file
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Load into Polars DataFrame
    df = pl.read_csv(io.BytesIO(response.content))
    
    # Store with key based on filename
    key = filename.replace('.csv', '')
    workforce_data[key] = df
    print(f"✓ Loaded {filename}: {len(df)} records")

# Access individual datasets
doctors_df = workforce_data['doctors']
nurses_df = workforce_data['nurses']
pharmacists_df = workforce_data['pharmacists']
physiotherapists_df = workforce_data['physiotherapists']
```

**Advantages:**
- ✓ Modern authentication (OAuth 2.0)
- ✓ Better security with app registrations
- ✓ Access to full Microsoft 365 ecosystem
- ✓ Granular permission control

### Method 3: Automated ETL Pipeline (Recommended)

```python
import os
from shared.src.data_processing.sharepoint_connector import SharePointConnector

# Connector reads credentials from environment variables automatically
# Requires: SHAREPOINT_SITE_URL, SHAREPOINT_CLIENT_ID, SHAREPOINT_CLIENT_SECRET, SHAREPOINT_TENANT_ID
connector = SharePointConnector()

# Define workforce folder path
workforce_folder = "Shared Documents/gen-e2-data-analysis test"

# Method 1: Extract all CSV files from workforce folder
all_workforce_files = connector.extract_folder(
    folder_path=workforce_folder,
    file_pattern="*.csv"
)

print(f"Loaded {len(all_workforce_files)} workforce datasets")

# Method 2: Extract specific files dynamically
workforce_files = ["doctors.csv", "nurses.csv", "pharmacists.csv", "physiotherapists.csv"]
workforce_data = {}

for filename in workforce_files:
    file_path = f"{workforce_folder}/{filename}"
    df = connector.extract_file(file_path)
    
    key = filename.replace('.csv', '')
    workforce_data[key] = df
    print(f"✓ Loaded {filename}: {len(df)} records")

# Access individual datasets
doctors_df = workforce_data['doctors']
nurses_df = workforce_data['nurses']
pharmacists_df = workforce_data['pharmacists']
physiotherapists_df = workforce_data['physiotherapists']
```

**Advantages:**
- ✓ Standardized column naming
- ✓ Automatic validation
- ✓ Logging and error handling
- ✓ Database loading included
- ✓ Caching for performance

---

## Authentication Setup

### Prerequisites

1. **MOH Account** with SharePoint access
2. **Python 3.9+**
3. **Required packages**:
   ```bash
    uv pip install Office365-REST-Python-Client msal requests python-dotenv polars
   ```

### Option A: Azure AD App Registration (Recommended for Production)

**Step 1**: Register Application in Azure AD
1. Login to Azure Portal → Azure Active Directory
2. App registrations → New registration
3. Name: "MOH Analytics ETL"
4. Supported account types: "Single tenant"
5. Register

**Step 2**: Configure API Permissions
1. API permissions → Add permission
2. Microsoft Graph → Application permissions
3. Add: `Sites.Read.All`, `Files.Read.All`
4. Grant admin consent

**Step 3**: Create Client Secret
1. Certificates & secrets → New client secret
2. Description: "ETL Pipeline Secret"
3. Expires: 24 months
4. Copy the secret value (shown once)

**Step 4**: Configure Environment Variables
```bash
# Add to .env file (NEVER commit this file to version control)
SHAREPOINT_TENANT_ID="your-tenant-id"
SHAREPOINT_CLIENT_ID="your-client-id"
SHAREPOINT_CLIENT_SECRET="your-client-secret"
SHAREPOINT_SITE_URL="https://paloit2016.sharepoint.com/sites/TestSite-FileSync"
SHAREPOINT_SITE_ID="paloit2016.sharepoint.com,{site-guid},{web-guid}"
SHAREPOINT_DRIVE_ID="your-drive-id"
SHAREPOINT_WORKFORCE_FOLDER="Shared Documents/gen-e2-data-analysis test"
```

**Load environment variables in Python:**
```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Access variables
site_url = os.getenv("SHAREPOINT_SITE_URL")
client_id = os.getenv("SHAREPOINT_CLIENT_ID")
# Never log or print these values!
```

### Option B: User Credentials (Development Only)

```bash
# Add to .env file (NEVER commit this file to version control)
SHAREPOINT_USERNAME="your_email@moh.gov.sg"
SHAREPOINT_PASSWORD="your_password"
SHAREPOINT_SITE_URL="https://paloit2016.sharepoint.com/sites/TestSite-FileSync"
SHAREPOINT_WORKFORCE_FOLDER="Shared Documents/gen-e2-data-analysis test"
```

**Load in Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")  # Never log this!
site_url = os.getenv("SHAREPOINT_SITE_URL")
```

**⚠️ Warning**: Not recommended for production. Use app registration (Option A) instead.

### Verification

```python
import os
from dotenv import load_dotenv
from shared.src.data_processing.sharepoint_connector import SharePointConnector

# Load environment variables
load_dotenv()

# Verify required environment variables
required_vars = [
    "SHAREPOINT_SITE_URL",
    "SHAREPOINT_CLIENT_ID",
    "SHAREPOINT_CLIENT_SECRET",
    "SHAREPOINT_TENANT_ID",
    "SHAREPOINT_WORKFORCE_FOLDER"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

# Test connection
try:
    connector = SharePointConnector()
    
    # List workforce files
    workforce_folder = os.getenv("SHAREPOINT_WORKFORCE_FOLDER")
    files = connector.list_files(workforce_folder)
    
    print("✓ Authentication successful!")
    print(f"Found {len(files)} files in workforce folder")
    print(f"Files: {[f['name'] for f in files]}")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
```

---

## Security Best Practices

### Environment Variable Management

**✓ DO:**
- Store credentials in `.env` file (add to `.gitignore`)
- Use `python-dotenv` to load environment variables
- Use different credentials for dev/staging/production
- Rotate secrets regularly (every 90 days minimum)
- Use Azure Key Vault or similar for production secrets
- Set appropriate file permissions: `chmod 600 .env`

**✗ DON'T:**
- Commit `.env` files to version control
- Hardcode credentials in source code
- Log or print credential values
- Share credentials via email or chat
- Use production credentials in development

### Example .gitignore

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Credentials
kaggle.json
credentials.json
secrets.yml

# Azure/SharePoint
azure_credentials.json
sharepoint_config.json
```

### Using Azure Key Vault (Production Recommended)

```python
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Use Azure Key Vault for production secrets
key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
kv_uri = f"https://{key_vault_name}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve secrets
sharepoint_client_id = client.get_secret("sharepoint-client-id").value
sharepoint_client_secret = client.get_secret("sharepoint-client-secret").value
sharepoint_tenant_id = client.get_secret("sharepoint-tenant-id").value

# Use in connector
connector = SharePointConnector(
    client_id=sharepoint_client_id,
    client_secret=sharepoint_client_secret,
    tenant_id=sharepoint_tenant_id
)
```

### Environment Variable Validation

```python
# src/config/environment.py
import os
from typing import Dict, List
from dotenv import load_dotenv

class EnvironmentConfig:
    """Centralized environment variable management"""
    
    REQUIRED_VARS = [
        "SHAREPOINT_SITE_URL",
        "SHAREPOINT_CLIENT_ID",
        "SHAREPOINT_CLIENT_SECRET",
        "SHAREPOINT_TENANT_ID",
        "SHAREPOINT_WORKFORCE_FOLDER",
    ]
    
    @classmethod
    def load_and_validate(cls) -> Dict[str, str]:
        """Load and validate all required environment variables"""
        load_dotenv()
        
        missing = []
        config = {}
        
        for var in cls.REQUIRED_VARS:
            value = os.getenv(var)
            if not value:
                missing.append(var)
            else:
                config[var] = value
        
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}\\n"
                f"Please set these in your .env file"
            )
        
        return config
    
    @classmethod
    def get_sharepoint_config(cls) -> Dict[str, str]:
        """Get SharePoint-specific configuration"""
        config = cls.load_and_validate()
        return {
            "site_url": config["SHAREPOINT_SITE_URL"],
            "client_id": config["SHAREPOINT_CLIENT_ID"],
            "client_secret": config["SHAREPOINT_CLIENT_SECRET"],
            "tenant_id": config["SHAREPOINT_TENANT_ID"],
        }

# Usage
from src.config.environment import EnvironmentConfig

config = EnvironmentConfig.get_sharepoint_config()
connector = SharePointConnector(**config)
```

---

## Data Documentation Resources

### Quick References

| Document | Purpose | Location |
|----------|---------|----------|
| **Workforce Data Catalog** | File schemas & column definitions | SharePoint: `/Data Governance/Workforce_Data_Catalog.xlsx` |
| **Data Dictionary** | Column definitions & business rules | [`docs/data_dictionary/`](../data_dictionary/) |
| **ETL Pipeline Guide** | Automation setup & scheduling | [`docs/DATA_EXTRACTION_AUTOMATION_GUIDE.md`](../DATA_EXTRACTION_AUTOMATION_GUIDE.md) |
| **SharePoint API Guide** | SharePoint & Graph API examples | This document |
| **Data Source Configuration** | Environment variables & setup | This document |

### Key Datasets by Use Case

**Workforce Analytics:**
- `doctors.csv` - Medical doctor workforce data (Updated monthly)
- `nurses.csv` - Registered nurses and midwives data (Updated monthly)
- `pharmacists.csv` - Pharmacist workforce data (Updated monthly)
- `physiotherapists.csv` - Physiotherapist workforce data (Updated monthly)

**Location**: `/sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce/`

**Common Analyses:**
- Workforce trends over time
- Staff distribution by sector (public/private)
- Comparative analysis across healthcare professions
- Workforce capacity planning
- Staff-to-population ratios

---

## Data Quality & Characteristics

### Quality Metrics

| Metric | Value | Verification Method |
|--------|-------|---------------------|
| Completeness | 95%+ | Automated null checks |
| Consistency | High | Cross-file validation |
| Timeliness | Real-time to weekly | Update timestamp monitoring |
| Accuracy | Validated | Source system reconciliation |
| Granularity | Transactional to summary | Varies by dataset |

### Data Governance

**Data Stewardship:**
- Each dataset has designated data owner
- Update schedules documented in metadata
- Change logs maintained in SharePoint version history

**Access Control:**
- Role-based permissions (Read/Write/Manage)
- Audit logging for all data access
- Compliance with MOH data policies

**Data Lineage:**
- Source system documented for each file
- Transformation logic tracked
- Data refresh schedules automated

### Data Limitations

1. **Access Restrictions**: Some datasets require elevated permissions
2. **File Size**: Large files (>100MB) may require special handling
3. **Version Control**: SharePoint versioning enabled (50 versions retained)
4. **Network Dependency**: Requires MOH network or VPN access
5. **Rate Limiting**: API calls subject to Microsoft throttling limits

### Known Issues

- **Excel Date Formats**: May require conversion handling
- **Column Naming**: Some legacy files have inconsistent naming
- **Encoding**: Ensure UTF-8 for special characters
- **File Locks**: Active editing can prevent automated access

---

## Integration Points

### Database Schema Mapping

```yaml
# Recommended database structure
schemas:
  sharepoint_raw:
    description: "Raw data as extracted from SharePoint"
    refresh: "Hourly/Daily based on source"
    
  sharepoint_staging:
    description: "Standardized, validated data"
    transformations: "Column renaming, type casting, validation"
    
  sharepoint_analytics:
    description: "Aggregated views, business metrics"
    views: "KPIs, dashboards, reports"
```

### Project Integration

**Config Files:**
```yaml
# config/data_sources.yml
# Note: Sensitive values should use environment variable references
sharepoint:
  site_url: "${SHAREPOINT_SITE_URL}"  # e.g., https://moh.sharepoint.com/sites/DataDojo
  workforce_folder: "${SHAREPOINT_WORKFORCE_FOLDER}"  # /sites/DataDojo/Shared Documents/Gen-e2/data-analysis/workforce
  
  workforce_files:
    - doctors.csv
    - nurses.csv
    - pharmacists.csv
    - physiotherapists.csv
  
  refresh_schedule: 
    workforce: "0 2 1 * *"  # Monthly on 1st at 2 AM
  
  priority: "high"
  
  authentication:
    tenant_id: "${SHAREPOINT_TENANT_ID}"
    client_id: "${SHAREPOINT_CLIENT_ID}"
    client_secret: "${SHAREPOINT_CLIENT_SECRET}"
  
  local_storage:
    raw_data_path: "shared/data/1_raw/workforce"
    processed_path: "data/2_processed/workforce"
```

**ETL Scripts:**
- [`shared/src/data_processing/sharepoint_connector.py`](../../shared/src/data_processing/sharepoint_connector.py) - SharePoint connector class
- [`scripts/load_sharepoint_data.py`](../../scripts/load_sharepoint_data.py) - Main extraction script
- [`scripts/load_workforce_data.py`](../../scripts/load_workforce_data.py) - Workforce-specific loader

---

## Usage Examples

### Example 1: Extract Single File

```python
import os
from dotenv import load_dotenv
from shared.src.data_processing.sharepoint_connector import SharePointConnector
import polars as pl

# Load environment variables
load_dotenv()

# Initialize connector (reads from environment variables)
connector = SharePointConnector()

# Get workforce folder path from environment
workforce_folder = os.getenv("SHAREPOINT_WORKFORCE_FOLDER")

# Download and load doctors data
file_path = f"{workforce_folder}/doctors.csv"
df = connector.extract_file(file_path)

print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns}")
print(df.head())
```

### Example 2: Batch Extract All Workforce Files

```python
import os
from dotenv import load_dotenv
from shared.src.data_processing.sharepoint_connector import SharePointConnector
import polars as pl
from loguru import logger

# Load environment variables
load_dotenv()

# Initialize connector
connector = SharePointConnector()

# Get workforce folder path
workforce_folder = os.getenv("SHAREPOINT_WORKFORCE_FOLDER")

# Define workforce files
workforce_files = ["doctors.csv", "nurses.csv", "pharmacists.csv", "physiotherapists.csv"]

# Extract and load all workforce datasets
workforce_data = {}

for filename in workforce_files:
    file_path = f"{workforce_folder}/{filename}"
    
    try:
        df = connector.extract_file(file_path)
        key = filename.replace('.csv', '')
        workforce_data[key] = df
        logger.info(f"✓ Loaded {filename}: {len(df)} records, {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"✗ Failed to load {filename}: {e}")

print(f"\nTotal datasets loaded: {len(workforce_data)}")

# Combine all workforce data for analysis
for name, df in workforce_data.items():
    # Add profession column for identification
    df = df.with_columns(pl.lit(name).alias('profession'))
    workforce_data[name] = df

# Concatenate all datasets
combined_workforce = pl.concat(list(workforce_data.values()))
print(f"Combined workforce data: {len(combined_workforce)} total records")
```

### Example 3: Automated Scheduled ETL for Workforce Data

```python
# Run via cron or task scheduler
import os
from dotenv import load_dotenv
from src.data_processing.etl_pipeline import run_sharepoint_etl
from loguru import logger
from pathlib import Path

# Load environment variables
load_dotenv()

# Verify required environment variables
required_vars = [
    "SHAREPOINT_SITE_URL",
    "SHAREPOINT_CLIENT_ID",
    "SHAREPOINT_CLIENT_SECRET",
    "SHAREPOINT_TENANT_ID",
    "SHAREPOINT_WORKFORCE_FOLDER"
]

for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Configure logging
log_dir = Path("logs/etl")
log_dir.mkdir(parents=True, exist_ok=True)
logger.add(log_dir / "workforce_etl_{time}.log", rotation="1 day")

# Execute workforce ETL
try:
    workforce_folder = os.getenv("SHAREPOINT_WORKFORCE_FOLDER")
    workforce_files = ["doctors.csv", "nurses.csv", "pharmacists.csv", "physiotherapists.csv"]
    
    results = run_sharepoint_etl(
        folder_path=workforce_folder,
        file_list=workforce_files,
        target_db="moh_analytics",
        target_schema="workforce",
        validate=True,
        save_local=True,
        local_path="shared/data/1_raw/workforce"
    )
    
    logger.info(f"ETL completed successfully")
    logger.info(f"Files processed: {results['files_processed']}")
    logger.info(f"Total records: {results['total_records']}")
    logger.info(f"Data saved to: {results['local_path']}")
    
except Exception as e:
    logger.error(f"ETL failed: {e}")
    raise
```

---

## Support & Contact

**SharePoint Access Issues**: MOH IT Service Desk (servicedesk@moh.gov.sg)  
**Data Quality Concerns**: Data Governance Team (data-governance@moh.gov.sg)  
**API/Integration Support**: Analytics Engineering Team  
**Project Documentation**: See [`docs/`](../) directory

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.2 | 2026-04-17 | Updated to DataDojo site with dynamic workforce folder and CSV files |
| 2.1 | 2026-04-17 | Updated all examples to use OS environment variables for security |
| 2.0 | 2026-04-15 | Migrated to SharePoint as primary data source |
| 1.0 | 2026-01-30 | Initial documentation (Kaggle-based) |

---

**Document maintained by:** Data Analytics Team  
**Last verified:** 17 April 2026  
**Next review:** Monthly or when data sources change

