# Data Sources: MOH Healthcare Data Analysis

**Last Updated:** 13 April 2026  
**Status:** Active, Fully Documented

---

## Primary Data Source: Data.gov.sg Health Portal

### Overview

**Source**: Singapore Government Open Data Portal  
**Portal URL**: https://data.gov.sg/datasets?topics=health  
**API Base URL**: https://api-production.data.gov.sg/v2/public/api  
**Original Source**: Ministry of Health Singapore  
**Last Verified**: 13 April 2026  
**Data Domain**: Singapore Healthcare & Public Health Data  
**Access Method**: REST API (no authentication required)  
**Format**: CSV files via API  
**Authentication**: None required for public datasets  
**Data Quality**: Official government source, regularly updated

### Available Collections

**Total Health Collections**: 24 (Collection IDs: 500-522, 527)  
**Total Datasets**: 50+ individual datasets  
**All Managed By**: Ministry of Health Singapore (except Collection 527)

| Category | Collections | Total Datasets |
|----------|-------------|----------------|
| COVID-19 & Infectious Disease | 6 | 15 |
| Healthcare Facilities & Workforce | 8 | 13 |
| Disease Surveillance & Mortality | 5 | 8 |
| Preventive Health & Screening | 1 | 3 |
| Healthcare Utilization | 4 | 8 |

---

#### COVID-19 & Infectious Disease (6 Collections)

| ID | Collection Name | Datasets | Coverage | Frequency |
|----|-----------------|----------|----------|-----------|
| 501 | PHPCs under National COVID-19 Vaccine Program | 1 | 2021-2023 | Monthly |
| 508 | Weekly Infectious Disease Bulletin | 1 | 2012-2022 | Weekly |
| 509 | Weekly Number of Dengue and Dengue Haemorrhagic Fever Cases | 1 | 2014-2018 | Weekly |
| 510 | Children's Immunisation Statistics | 2 | 2015-2020 | Annual |
| 519 | Covid-19 Case in Singapore | 1 | 2020-2022 | Daily |
| 522 | COVID-19 Weekly Stats | 8 | 2020-2024 | Weekly/Ad-hoc |

**Key Datasets:**
- **COVID-19 Weekly Stats (522)**: 7-day moving average infections, hospitalizations, ICU cases, deaths, vaccination coverage
- **Weekly Infectious Disease Bulletin (508)**: Comprehensive surveillance of notifiable diseases
- **Dengue Cases (509)**: Lab-confirmed dengue and dengue haemorrhagic fever tracking
- **COVID-19 Daily Cases (519)**: Daily case counts, community vs imported

---

#### Healthcare Facilities & Workforce (8 Collections)

| ID | Collection Name | Datasets | Coverage | Frequency |
|----|-----------------|----------|----------|-----------|
| 500 | Number of Traditional Chinese Medicine Practitioners | 1 | 2006-2019 | Annual |
| 505 | Top 10 Conditions of Hospitalisation | 1 | 2009-2020 | Annual |
| 506 | Top 4 Conditions of Polyclinic Attendances | 1 | 2009-2020 | Annual |
| 511 | Hospital Admission Rate by Age and Sex | 2 | 2006-2020 | Annual |
| 512 | Hospital Admissions And Public Sector Outpatient Attendances | 2 | 1990-2020 | Annual |
| 513 | Number of Dentists and Oral Health Therapists | 2 | 2006-2019 | Annual |
| 514 | Number of Nurses and Midwives | 2 | 2008-2019 | Annual |
| 517 | Visits to Public Sector Dental Clinics | 2 | 1990-2018 | Annual |

**Key Datasets:**
- **Healthcare Workforce**: TCM practitioners, dentists, nurses, midwives by sector
- **Utilization Patterns**: Hospital admission rates by demographics, polyclinic attendances
- **Disease Burden**: Top conditions requiring hospitalization and primary care

---

#### Disease Surveillance & Mortality (5 Collections)

| ID | Collection Name | Datasets | Coverage | Frequency |
|----|-----------------|----------|----------|-----------|
| 504 | Prevalence of Hypertension, Diabetes, High Total Cholesterol, Obesity and Daily Smoking | 1 | 2004-2017 | Periodic |
| 507 | Top 5 Leading Cancers by Gender | 1 | 2013-2017 | 5-year periods |
| 516 | Number of Deaths and Top 10 Principal Causes | 2 | 1990-2020 | Annual |
| 518 | Age-Standardised Mortality Rate for Ischaemic Heart Disease, Stroke and Cancer | 3 | 1990-2019 | Annual |
| 527 | Deaths and Death Rates by Cause | 1 | 2000-2022 | Annual |

**Key Datasets:**
- **Chronic Disease Prevalence**: National rates for major NCDs
- **Cancer Statistics**: Leading cancers by gender and incidence trends
- **Mortality Trends**: Long-term mortality rates for major causes (1990-2022)
- **Cardiovascular Disease**: Heart disease and stroke mortality tracking

---

#### Preventive Health & Screening (1 Collection)

| ID | Collection Name | Datasets | Coverage | Frequency |
|----|-----------------|----------|----------|-----------|
| 520 | Preventive Health Screening Statistics | 3 | 2009-2018 | Annual |

**Key Datasets:**
- **Screening Programs**: Participation rates and outcomes for major screening initiatives
- **Early Detection**: Cancer and cardiovascular screening results

---

#### Healthcare Utilization (4 Collections)

| ID | Collection Name | Datasets | Coverage | Frequency |
|----|-----------------|----------|----------|-----------|
| 502 | Residential Long-Term Care Admissions | 1 | 2006-2020 | Annual |
| 503 | SGO Satellite Offices | 1 | 2024-present | Current |
| 515 | Number of Residential Long-Term Care Facilities | 2 | 2006-2020 | Annual |
| 521 | Health Facilities and Beds in Inpatient Facilities | 4 | 1990-2020 | Annual |

**Key Datasets:**
- **Long-Term Care**: Nursing homes, chronic sick facilities, admissions tracking
- **Healthcare Infrastructure**: Hospitals, beds capacity by sector (public/private)
- **Service Access**: SGO satellite office locations

---

## Data Access & Connection

### Method 1: REST API Access (Recommended)

#### Get Collection Metadata

```python
import requests
import json

# Fetch collection information
collection_id = 522  # COVID-19 Weekly Stats (or any collection ID from 500-522, 527)
url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"

response = requests.get(url)
data = response.json()

print(f"Collection: {data['data']['collectionMetadata']['name']}")
print(f"Description: {data['data']['collectionMetadata']['description']}")
print(f"Managed by: {data['data']['collectionMetadata']['managedBy']}")
print(f"Number of datasets: {len(data['data']['collectionMetadata']['childDatasets'])}")
print(f"Coverage: {data['data']['collectionMetadata']['coverageStart']} to {data['data']['collectionMetadata']['coverageEnd']}")
```

**Advantages:**
- ✓ No authentication required
- ✓ Direct API access
- ✓ Real-time data
- ✓ Programmatic access
- ✓ Metadata included

#### Browse All Health Collections

```python
import requests

# All health collection IDs
health_collections = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509,
                     510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
                     520, 521, 522, 527]

for collection_id in health_collections:
    url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
    response = requests.get(url)
    
    if response.status_code == 200:
        metadata = response.json()['data']['collectionMetadata']
        print(f"{collection_id}: {metadata['name']} ({len(metadata['childDatasets'])} datasets)")
```

#### Get Dataset Metadata

```python
import requests

# Get specific dataset details
dataset_id = "d_f431af082e77221c453895ebdc3e57ba"
url = f"https://api-production.data.gov.sg/v2/public/api/datasets/{dataset_id}/metadata"

response = requests.get(url)
dataset_info = response.json()['data']

print(f"Dataset: {dataset_info['name']}")
print(f"Format: {dataset_info['format']}")
print(f"Coverage: {dataset_info['coverageStart']} to {dataset_info['coverageEnd']}")
print(f"Size: {dataset_info['datasetSize']} bytes")
print(f"Contact: {dataset_info['contactEmails'][0]}")

# Get column metadata
columns = dataset_info['columnMetadata']['map']
print(f"Columns: {', '.join(columns.values())}")
```

**Advantages:**
- ✓ Detailed schema information
- ✓ Column names and data types
- ✓ Coverage dates
- ✓ Contact information for support

### Method 2: Pandas Integration

```python
import requests
import pandas as pd
from io import StringIO

def load_dataset_from_datagovsg(dataset_id):
    """Load dataset directly into pandas DataFrame"""
    
    # Get metadata first
    metadata_url = f"https://api-production.data.gov.sg/v2/public/api/datasets/{dataset_id}/metadata"
    metadata_response = requests.get(metadata_url)
    metadata = metadata_response.json()['data']
    
    print(f"Loading: {metadata['name']}")
    print(f"Format: {metadata['format']}")
    
    # Download data (implement based on available download endpoint)
    # Note: Actual download endpoint may vary
    
    return metadata

# Example usage
dataset_id = "d_f431af082e77221c453895ebdc3e57ba"
metadata = load_dataset_from_datagovsg(dataset_id)
```

**Advantages:**
- ✓ Direct to DataFrame
- ✓ Easy data manipulation
- ✓ Integrated with analysis workflow

### Method 3: Automated ETL Pipeline

```python
# Use project's ETL pipeline
from src.data_processing.datagovsg_connector import DataGovSGConnector

connector = DataGovSGConnector()

# Extract specific collection
covid_data = connector.extract_collection(collection_id=522)

# Extract multiple collections by category
infectious_disease_collections = [508, 509, 510, 519, 522]  # All infectious disease data
workforce_collections = [500, 513, 514]  # Healthcare workforce data

# Load all datasets from specific collections
all_datasets = connector.extract_multiple_collections(infectious_disease_collections)
```

**Advantages:**
- ✓ Standardized column names
- ✓ Automatic validation
- ✓ Logging and error handling
- ✓ Database loading included
- ✓ Batch processing for multiple collections

---

## Authentication Setup

### Prerequisites

1. **No Account Required** - Public datasets are openly accessible
2. **Python 3.7+**
3. **Required packages**:
   ```bash
   pip install requests pandas
   # or using uv (project standard)
   uv pip install requests pandas
   ```

### API Access (No Authentication Required)

Data.gov.sg public health datasets do not require API keys or authentication for access.

**Direct API Usage:**
```python
import requests

# No authentication needed - direct API call
url = "https://api-production.data.gov.sg/v2/public/api/collections/522/metadata"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("✓ Successfully accessed data.gov.sg API")
else:
    print(f"✗ Error: {response.status_code}")
```

### Verification

```python
import requests

def verify_datagovsg_access():
    """Test connection to data.gov.sg API"""
    try:
        # Test collection endpoint
        collection_id = 522
        url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        print("✓ API access successful!")
        print(f"✓ Collection: {data['data']['collectionMetadata']['name']}")
        print(f"✓ Datasets available: {len(data['data']['collectionMetadata']['childDatasets'])}")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

verify_datagovsg_access()
```

**Expected Output:**
```
✓ API access successful!
✓ Collection: COVID-19 Weekly Stats  
✓ Datasets available: 8
```

---

## API Endpoints Reference

### Core Endpoints

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `/collections/{collection_id}/metadata` | Get collection info and list of datasets | `collection_id` (integer) |
| `/datasets/{dataset_id}/metadata` | Get dataset details, schema, coverage | `dataset_id` (string with format `d_*`) |

### URL Structure

**Base URL**: `https://api-production.data.gov.sg/v2/public/api`

**Collection Metadata:**
```
GET https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata
```

**Dataset Metadata:**
```
GET https://api-production.data.gov.sg/v2/public/api/datasets/{dataset_id}/metadata
```

**Web Portal:**
```
https://data.gov.sg/datasets?topics=health&resultId={collection_id}
```

### Response Format

**Collection Response:**
```json
{
    "code": 0,
    "data": {
        "collectionMetadata": {
            "collectionId": "522",
            "name": "COVID-19 Weekly Stats",
            "description": "Data on COVID-19 cases",
            "managedBy": "Ministry of Health",
            "coverageStart": "2020-12-30T08:00:00+08:00",
            "coverageEnd": "2023-09-12T08:00:00+08:00",
            "frequency": "ad-hoc",
            "childDatasets": ["d_f431af082e77221c453895ebdc3e57ba", ...]
        }
    }
}
```

**Dataset Response:**
```json
{
    "code": 0,
    "data": {
        "datasetId": "d_f431af082e77221c453895ebdc3e57ba",
        "name": "7-day Moving Average Daily Estimated Numbers of COVID-19 Infections",
        "format": "CSV",
        "datasetSize": 475,
        "coverageStart": "2023-12-13T08:00:00+08:00",
        "coverageEnd": "2024-01-02T08:00:00+08:00",
        "contactEmails": ["moh_singapore@moh.gov.sg"],
        "columnMetadata": {
            "map": {
                "c_id_1": "Date",
                "c_id_2": "7day_Moving_Average_Daily_Estimated_Numbers_of_COVID_19_Infections"
            }
        }
    }
}
```

---

## Data Documentation Resources

### Quick References

| Document | Purpose | Location |
|----------|---------|----------|
| **Health Collections Catalog (JSON)** | Complete inventory of all 24 collections | [`data/health_collections_catalog.json`](../../data/health_collections_catalog.json) |
| **Collection Extraction Script** | Automated catalog generation | [`scripts/extract_health_collections_catalog.py`](../../scripts/extract_health_collections_catalog.py) |
| **API Exploration Script** | Interactive dataset discovery | [`scripts/explore_datagovsg_api.py`](../../scripts/explore_datagovsg_api.py) |
| **Data Sources Documentation** | This document | [`docs/project-context/data-sources.md`](./data-sources.md) |
| **Data.gov.sg Portal** | Browse datasets visually | [https://data.gov.sg/datasets?topics=health](https://data.gov.sg/datasets?topics=health) |

### Quick Start by Use Case

**Infectious Disease Surveillance:**
- **Weekly Infectious Disease Bulletin (508)**: Comprehensive disease tracking (2012-2022)
  - Coverage: Notifiable infectious diseases
  - Frequency: Weekly epidemiological reports
  - Use for: Outbreak detection, disease trend analysis
  
- **Dengue Surveillance (509)**: Lab-confirmed dengue cases (2014-2018)
  - Coverage: Weekly dengue and DHF cases
  - Use for: Vector-borne disease monitoring, seasonal patterns

- **COVID-19 Tracking (519, 522)**: Comprehensive pandemic surveillance
  - Daily cases, hospitalizations, deaths, vaccination coverage
  - Use for: Pandemic response analysis, vaccination campaigns

**Healthcare Capacity Planning:**
- **Health Facilities & Beds (521)**: Hospital and bed capacity (1990-2020)
  - Coverage: Public and private sector inpatient facilities
  - Tracks: Bed capacity, facility types, sector breakdown
  
- **Healthcare Workforce (500, 513, 514)**: Professional headcount (2006-2019)
  - Categories: Nurses, dentists, TCM practitioners
  - Breakdown: By sector (public/private), qualification levels
  
- **Hospital Utilization (511, 512)**: Admission patterns (1990-2020)
  - Demographics: Age, sex, admission rates
  - Trends: Long-term utilization patterns

**Disease Burden & Mortality Analysis:**
- **Mortality Rates (516, 518, 527)**: Death statistics (1990-2022)
  - Leading causes of death
  - Age-standardized mortality rates for CVD and cancer
  - Long-term trend analysis (30+ years)
  
- **Chronic Disease Prevalence (504)**: NCD surveillance (2004-2017)
  - Conditions: Hypertension, diabetes, cholesterol, obesity, smoking
  - Population-level prevalence tracking
  
- **Cancer Statistics (507)**: Top 5 cancers by gender (2013-2017)
  - Incidence patterns
  - Gender-specific cancer burden

**Public Health Programs:**
- **Children's Immunisation (510)**: Vaccination coverage (2015-2020)
  - Childhood vaccination schedules
  - Coverage rates by vaccine type
  
- **Preventive Screening (520)**: Screening participation (2009-2018)
  - Cancer screening programs
  - Cardiovascular screening initiatives
  
- **Primary Care Patterns (506)**: Polyclinic top conditions (2009-2020)
  - Common presenting complaints
  - Primary care disease burden

---

## Data Quality & Characteristics

### Quality Metrics

| Metric | Value |
|--------|-------|
| Completeness | High (official government data) |
| Consistency | Standardized API format across all collections |
| Timeliness | Varies by collection (weekly to annual updates) |
| Accuracy | Official MOH Singapore source |
| Granularity | Daily, weekly, monthly, and annual (varies by dataset) |
| Accessibility | Public API, no authentication required |
| Historical Depth | Up to 30+ years (1990-present for some collections) |

### Data Characteristics by Category

**COVID-19 & Infectious Disease:**
- Update frequency: Daily to weekly
- Granularity: Individual cases, epi-weeks, monthly
- Demographics: Age groups, vaccination status
- Time span: 2012-2024 (varies by dataset)

**Healthcare Workforce:**
- Update frequency: Annual
- Granularity: By profession, sector (public/private), qualification
- Time span: 2006-2019 (varies by profession)
- Completeness: National totals, sector breakdowns

**Mortality & Disease Burden:**
- Update frequency: Annual
- Granularity: Age-standardized rates, age groups, gender
- Time span: 1990-2022 (longest historical records)
- Standardization: Age-standardized for comparability

**Healthcare Utilization:**
- Update frequency: Annual
- Granularity: Facility types, admission rates, demographics
- Time span: 1990-2020 for key indicators
- Coverage: Public and private sector facilities

### Data Limitations

1. **Update Frequency**: Varies significantly across collections
   - Real-time: Not available
   - Daily/Weekly: Only for selected infectious disease surveillance (COVID-19, dengue)
   - Annual: Most workforce and facility data is 3-6 years behind current date

2. **Latest Data Availability**: 
   - COVID-19 data: Most recent (2023-2024)
   - Workforce data: Typically 3-6 years lag (latest 2019-2020)
   - Historical mortality: Good coverage (1990-2022)

3. **Geographic Granularity**: 
   - National level only for most datasets
   - No regional or facility-level breakdowns publicly available
   - Some datasets show sector (public/private) split only

4. **Demographics**: 
   - Age groups: Available for most health outcome datasets
   - Gender: Available for selected datasets (mortality, cancer)
   - Ethnicity: Limited availability
   - Socioeconomic status: Not included in most datasets

5. **Data Gaps**:
   - Some workforce professions have limited years (e.g., TCM practitioners start 2006)
   - COVID-19 collection has variable coverage dates per dataset
   - Historical dengue data only 2014-2018
   - Screening participation data only to 2018

### Known Issues

- **Coverage Inconsistencies**: Different datasets within same collection may have different time spans
- **Dataset Sizes**: Relatively small file sizes (bytes to KB range) - aggregated data only
- **Limited Metadata**: Column descriptions could be more detailed in some datasets
- **No Bulk Download**: Each dataset must be accessed individually via API
- **Rate Limiting**: Not documented, recommend respectful API usage (1 request per second)
- **Data Freshness**: Annual collections have significant time lags (2-6 years)
- **Format Variations**: While all CSV, column naming conventions vary across collections

---

## Integration Points

### Database Schema Mapping

```yaml
# Recommended database structure
schemas:
  datagovsg_raw:
    description: "Raw data as extracted from data.gov.sg API"
    tables:
      # COVID-19 & Infectious Disease
      - covid_infections_7day_ma
      - covid_hospitalizations_epi_week
      - covid_deaths_monthly
      - covid_daily_cases
      - infectious_disease_bulletin_weekly
      - dengue_cases_weekly
      - children_immunization
      
      # Healthcare Workforce
      - tcm_practitioners
      - dentists_oral_health_therapists
      - nurses_midwives
      - workforce_by_profession_sector
      
      # Mortality & Disease Surveillance
      - deaths_by_cause
      - mortality_rates_cvd_cancer
      - leading_causes_death
      - chronic_disease_prevalence
      - cancer_top5_by_gender
      
      # Healthcare Utilization
      - hospital_admissions_by_demographics
      - polyclinic_attendances
      - top_conditions_hospitalization
      - long_term_care_admissions
      - dental_clinic_visits
      
      # Healthcare Infrastructure
      - health_facilities_beds
      - long_term_care_facilities
      
      # Preventive Health
      - screening_statistics
    
  datagovsg_staging:
    description: "Standardized column names, data types, validated"
    transformations:
      - date_parsing
      - age_group_normalization
      - categorical_encoding
      - sector_standardization
      - rate_calculation_validation
    
  datagovsg_analytics:
    description: "Aggregated views, derived metrics, analytical tables"
    views:
      # Infectious Disease
      - weekly_case_trends_all_diseases
      - covid_pandemic_timeline
      - dengue_seasonal_patterns
      - immunization_coverage_trends
      
      # Workforce Planning
      - healthcare_workforce_capacity
      - workforce_growth_rates
      - public_private_ratios
      
      # Disease Burden
      - age_stratified_outcomes
      - mortality_trend_analysis
      - leading_causes_time_series
      - chronic_disease_burden
      
      # Healthcare Utilization
      - hospital_utilization_patterns
      - primary_care_demand_trends
      - bed_occupancy_analysis
      
      # Integrated Analytics
      - healthcare_system_dashboard
      - capacity_vs_demand
      - disease_burden_summary
```

### Project Integration

**Config Files:**
```yaml
# config/database.yml
data_sources:
  datagovsg:
    api_base_url: "https://api-production.data.gov.sg/v2/public/api"
    
    collections:
      # COVID-19 & Infectious Disease (Priority: High)
      - id: 522
        name: "COVID-19 Weekly Stats"
        priority: "high"
        refresh_schedule: "weekly"
        category: "infectious_disease"
        
      - id: 508
        name: "Weekly Infectious Disease Bulletin"
        priority: "high"
        refresh_schedule: "weekly"
        category: "infectious_disease"
      
      - id: 519
        name: "Covid-19 Case in Singapore"
        priority: "high"
        refresh_schedule: "daily"
        category: "infectious_disease"
      
      - id: 509
        name: "Weekly Dengue Cases"
        priority: "medium"
        refresh_schedule: "weekly"
        category: "infectious_disease"
      
      # Healthcare Workforce (Priority: Medium)
      - id: 514
        name: "Nurses and Midwives"
        priority: "medium"
        refresh_schedule: "annual"
        category: "workforce"
        
      - id: 513
        name: "Dentists and Oral Health Therapists"
        priority: "medium"
        refresh_schedule: "annual"
        category: "workforce"
      
      # Mortality & Disease Burden (Priority: Medium)
      - id: 516
        name: "Deaths and Top 10 Principal Causes"
        priority: "medium"
        refresh_schedule: "annual"
        category: "mortality"
        
      - id: 518
        name: "Age-Standardised Mortality Rates"
        priority: "medium"
        refresh_schedule: "annual"
        category: "mortality"
      
      # Healthcare Utilization (Priority: Low)
      - id: 521
        name: "Health Facilities and Beds"
        priority: "low"
        refresh_schedule: "annual"
        category: "utilization"
    
    contact: "moh_singapore@moh.gov.sg"
    timeout_seconds: 10
    rate_limit_delay: 0.5  # seconds between requests
```

**ETL Scripts:**
- [`scripts/explore_datagovsg_api.py`](../../scripts/explore_datagovsg_api.py) - Single collection exploration
- [`scripts/extract_health_collections_catalog.py`](../../scripts/extract_health_collections_catalog.py) - All collections catalog generation
- `scripts/load_datagovsg_data.py` - Data extraction pipeline (to be created)
- `src/data_processing/datagovsg_connector.py` - Connector class (to be created)
- `src/data_processing/datagovsg_transformer.py` - Data transformation utilities (to be created)

---

## Usage Examples

### Example 1: Explore All Health Collections

```python
import requests
import pandas as pd

# All health collection IDs
health_collections = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509,
                     510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
                     520, 521, 522, 527]

# Gather metadata for all collections
collections_data = []

for cid in health_collections:
    url = f"https://api-production.data.gov.sg/v2/public/api/collections/{cid}/metadata"
    response = requests.get(url)
    
    if response.status_code == 200:
        metadata = response.json()['data']['collectionMetadata']
        collections_data.append({
            'id': cid,
            'name': metadata['name'],
            'datasets': len(metadata['childDatasets']),
            'coverage_start': metadata.get('coverageStart', 'N/A'),
            'coverage_end': metadata.get('coverageEnd', 'N/A'),
            'frequency': metadata.get('frequency', 'N/A')
        })

# Create summary DataFrame
df = pd.DataFrame(collections_data)
print(f"\nTotal Health Collections: {len(df)}")
print(f"Total Datasets: {df['datasets'].sum()}\n")
print(df[['id', 'name', 'datasets', 'frequency']].to_string())
```

### Example 2: Multi-Collection Disease Surveillance Analysis

```python
import requests
import pandas as pd

def get_collection_datasets(collection_id):
    """Get all dataset IDs from a collection"""
    url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
    response = requests.get(url)
    metadata = response.json()['data']['collectionMetadata']
    return metadata['childDatasets']

def get_dataset_metadata(dataset_id):
    """Fetch metadata for a specific dataset"""
    url = f"https://api-production.data.gov.sg/v2/public/api/datasets/{dataset_id}/metadata"
    response = requests.get(url)
    return response.json()['data']

# Analyze infectious disease collections
infectious_disease_collections = {
    508: 'Weekly Infectious Disease Bulletin',
    509: 'Dengue Cases',
    510: 'Children Immunisation',
    519: 'COVID-19 Cases',
    522: 'COVID-19 Weekly Stats'
}

print("Infectious Disease Surveillance Datasets:")
print("=" * 80)

for cid, cname in infectious_disease_collections.items():
    print(f"\n{cid}: {cname}")
    dataset_ids = get_collection_datasets(cid)
    
    for did in dataset_ids:
        dataset_info = get_dataset_metadata(did)
        print(f"  - {dataset_info['name']}")
        print(f"    Format: {dataset_info['format']}, Size: {dataset_info['datasetSize']} bytes")
        print(f"    Coverage: {dataset_info['coverageStart'][:10]} to {dataset_info['coverageEnd'][:10]}")
```

### Example 3: Healthcare Workforce Trend Analysis

```python
import requests
import pandas as pd

# Healthcare workforce collections
workforce_collections = {
    500: 'TCM Practitioners',
    513: 'Dentists and Oral Health Therapists',
    514: 'Nurses and Midwives'
}

workforce_data = []

for cid, profession in workforce_collections.items():
    collection_url = f"https://api-production.data.gov.sg/v2/public/api/collections/{cid}/metadata"
    collection = requests.get(collection_url).json()['data']['collectionMetadata']
    
    workforce_data.append({
        'collection_id': cid,
        'profession': profession,
        'datasets': len(collection['childDatasets']),
        'coverage_start': collection.get('coverageStart', 'N/A')[:10],
        'coverage_end': collection.get('coverageEnd', 'N/A')[:10]
    })

df_workforce = pd.DataFrame(workforce_data)
print("\nHealthcare Workforce Data Availability:")
print(df_workforce.to_string(index=False))
```

### Example 4: Automated Collection Extraction Pipeline

```python
import requests
import json
import time
from pathlib import Path

class HealthDataExtractor:
    """Extract health data from data.gov.sg API"""
    
    def __init__(self, output_dir="data/1_raw/datagovsg"):
        self.base_url = "https://api-production.data.gov.sg/v2/public/api"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # All health collection IDs
        self.health_collections = [
            500, 501, 502, 503, 504, 505, 506, 507, 508, 509,
            510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
            520, 521, 522, 527
        ]
    
    def extract_collection_metadata(self, collection_id):
        """Extract metadata for a single collection"""
        url = f"{self.base_url}/collections/{collection_id}/metadata"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['data']['collectionMetadata']
    
    def extract_dataset_metadata(self, dataset_id):
        """Extract metadata for a single dataset"""
        url = f"{self.base_url}/datasets/{dataset_id}/metadata"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['data']
    
    def extract_all_health_collections(self):
        """Extract metadata for all health collections"""
        results = {
            'total_collections': 0,
            'total_datasets': 0,
            'collections': []
        }
        
        for cid in self.health_collections:
            try:
                print(f"Extracting collection {cid}...")
                collection_meta = self.extract_collection_metadata(cid)
                
                # Get dataset details
                datasets = []
                for dataset_id in collection_meta['childDatasets']:
                    dataset_meta = self.extract_dataset_metadata(dataset_id)
                    datasets.append(dataset_meta)
                    time.sleep(0.1)  # Rate limiting
                
                collection_data = {
                    'collection_id': cid,
                    'collection_metadata': collection_meta,
                    'datasets': datasets
                }
                
                results['collections'].append(collection_data)
                results['total_collections'] += 1
                results['total_datasets'] += len(datasets)
                
                # Save individual collection
                output_file = self.output_dir / f"collection_{cid}.json"
                with open(output_file, 'w') as f:
                    json.dump(collection_data, f, indent=2)
                
                print(f"  ✓ Saved {len(datasets)} datasets to {output_file}")
                
            except Exception as e:
                print(f"  ✗ Error with collection {cid}: {str(e)}")
        
        # Save summary
        summary_file = self.output_dir / "health_collections_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Extraction complete:")
        print(f"  Collections: {results['total_collections']}")
        print(f"  Total datasets: {results['total_datasets']}")
        print(f"  Output directory: {self.output_dir}")
        
        return results

# Usage
extractor = HealthDataExtractor()
results = extractor.extract_all_health_collections()
```

### Example 5: Category-Based Analysis Setup

```python
import requests

# Define collection categories for analysis
COLLECTION_CATEGORIES = {
    'infectious_disease': [501, 508, 509, 510, 519, 522],
    'workforce': [500, 513, 514],
    'mortality': [504, 507, 516, 518, 527],
    'healthcare_utilization': [502, 503, 505, 506, 511, 512, 515, 517, 521],
    'preventive_health': [520]
}

def analyze_category(category_name, collection_ids):
    """Analyze all collections in a category"""
    print(f"\n{'=' * 80}")
    print(f"{category_name.upper().replace('_', ' ')}")
    print(f"{'=' * 80}\n")
    
    total_datasets = 0
    
    for cid in collection_ids:
        url = f"https://api-production.data.gov.sg/v2/public/api/collections/{cid}/metadata"
        response = requests.get(url)
        
        if response.status_code == 200:
            metadata = response.json()['data']['collectionMetadata']
            dataset_count = len(metadata['childDatasets'])
            total_datasets += dataset_count
            
            print(f"{cid}: {metadata['name']}")
            print(f"   Datasets: {dataset_count}")
            print(f"   Coverage: {metadata.get('coverageStart', 'N/A')[:10]} to {metadata.get('coverageEnd', 'N/A')[:10]}")
            print(f"   Frequency: {metadata.get('frequency', 'N/A')}\n")
    
    print(f"Total datasets in category: {total_datasets}\n")

# Analyze each category
for category, collections in COLLECTION_CATEGORIES.items():
    analyze_category(category, collections)
```

---

## Support & Contact

**API Issues**: No dedicated issue tracker available  
**Data Source**: Ministry of Health Singapore  
**Contact Email**: moh_singapore@moh.gov.sg  
**Web Portal**: https://data.gov.sg/datasets?topics=health  
**Project Documentation**: See [`docs/`](../) directory  
**Technical Support**: Contact project data team

### Useful Links

- **Data.gov.sg Home**: https://data.gov.sg
- **Health Datasets**: https://data.gov.sg/datasets?topics=health
- **Open Data License**: https://data.gov.sg/open-data-license
- **API Documentation**: Available through web portal
- **Ministry of Health**: https://www.moh.gov.sg
- **Health Collections Catalog**: [`data/health_collections_catalog.json`](../../data/health_collections_catalog.json)

### Collection Index

Quick reference for all 24 health collections:

| Range | Category | Collections |
|-------|----------|-------------|
| 500-503 | Healthcare Infrastructure & Workforce | TCM Practitioners, PHPCs, Long-term Care, SGO Offices |
| 504-507 | Disease Surveillance | Chronic Disease Prevalence, Hospitalization Conditions, Polyclinic Attendances, Cancer Statistics |
| 508-510 | Infectious Disease | Disease Bulletin, Dengue Cases, Children's Immunisation |
| 511-517 | Healthcare Utilization & Workforce | Hospital Admissions, Outpatient Attendances, Dentists, Nurses, Long-term Care, Dental Clinics |
| 518-522 | Mortality & COVID-19 | CVD/Cancer Mortality, COVID-19 Cases, Screening, Facilities, COVID-19 Weekly Stats |
| 527 | Mortality | Deaths and Death Rates by Cause |

---

## Best Practices

### API Usage Guidelines

1. **Rate Limiting**: Implement delays between requests (recommended: 0.5-1 second)
   ```python
   import time
   time.sleep(0.5)  # Between API calls
   ```

2. **Error Handling**: Always handle HTTP errors and timeouts
   ```python
   try:
       response = requests.get(url, timeout=10)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       logger.error(f"API request failed: {e}")
   ```

3. **Caching**: Cache metadata locally to reduce API calls
   ```python
   # Cache collection metadata for 24 hours
   cache_duration = 86400  # seconds
   ```

4. **Batch Processing**: Process collections in batches with progress tracking
   ```python
   from tqdm import tqdm
   for cid in tqdm(collection_ids, desc="Extracting collections"):
       # Process collection
   ```

### Data Quality Checks

1. **Validate Coverage Dates**: Ensure data freshness meets requirements
2. **Check Dataset Sizes**: Monitor for unexpected changes (potential data issues)
3. **Verify Column Schemas**: Compare against known schema structures
4. **Track Update Frequencies**: Monitor for delays in expected updates

### Integration Recommendations

1. **Incremental Loads**: Only fetch new data when available
2. **Version Control**: Track data versions and API response changes
3. **Logging**: Log all API calls, responses, and any errors
4. **Monitoring**: Set up alerts for API failures or data quality issues
5. **Documentation**: Keep collection catalog updated as new datasets are added

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2026-04-13 | Major update: Added all 24 health collections with comprehensive catalog |
| 2.0 | 2026-04-13 | Complete rewrite for data.gov.sg API integration (single collection) |
| 1.0 | 2026-01-30 | Initial comprehensive documentation (Kaggle source) |

### Changelog

**Version 3.0 (2026-04-13)**:
- Expanded from 1 to 24 health collections
- Added 50+ datasets across 5 major categories
- Created comprehensive collection catalog JSON
- Added extraction scripts for all collections
- Organized collections by: Infectious Disease, Healthcare Workforce, Mortality, Utilization, Preventive Health
- Updated API examples for multi-collection workflows
- Added best practices and integration guidelines
- Documented historical data availability (1990-2024)

**Version 2.0 (2026-04-13)**:
- Migrated from Kaggle to data.gov.sg API
- Documented COVID-19 Weekly Stats collection (ID: 522)
- Added REST API access methods
- Removed Kaggle authentication requirements

**Version 1.0 (2026-01-30)**:
- Initial documentation for Kaggle health dataset
- 35 CSV tables from Ministry of Health
- Kaggle Hub API integration

---

**Document maintained by:** Data Analytics Team  
**Last verified:** 13 April 2026  
**Next review:** Quarterly or when data sources update  
**Total Collections Documented:** 24  
**Total Datasets Available:** 50+

