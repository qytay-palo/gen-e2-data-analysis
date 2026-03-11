# Data Processing Module

> **Reusable data extraction, transformation, and loading (ETL) utilities**

This module provides connectors and utilities for extracting data from various sources, with a focus on Singapore health data.

---

## 📂 Module Structure

```
data_processing/
├── __init__.py
├── base_connector.py          # Abstract base class for all connectors
├── kaggle_connector.py         # Kaggle dataset connector
├── examples/                   # Example extraction scripts
│   ├── __init__.py
│   └── extract_kaggle_health_data.py
└── README.md                   # This file
```

---

## 🔌 Available Connectors

### KaggleConnector

Download datasets from Kaggle using either credential-free (kagglehub) or API-based authentication.

**Features**:
- ✅ Credential-free access using `kagglehub` (preferred)
- ✅ Traditional Kaggle API support (requires credentials)
- ✅ Automatic file detection and loading
- ✅ Retry logic for network failures
- ✅ Polars DataFrame output
- ✅ Comprehensive logging

**Usage**:

```python
from shared.src.data_processing.kaggle_connector import KaggleConnector

# Initialize connector (credential-free mode)
connector = KaggleConnector(use_kagglehub=True)

# Extract dataset
df = connector.extract(dataset="owner/dataset-name")

# Save to standardized location
connector.save_data(
    df=df,
    filename="my_dataset",
    format="parquet",
    compression="snappy"
)
```

**Installation**:

```bash
# For credential-free access (recommended)
uv pip install kagglehub

# For Kaggle API (requires ~/.kaggle/kaggle.json)
uv pip install kaggle
```

---

## 🚀 Quick Start

### 1. Extract Kaggle Dataset

```python
from shared.src.data_processing.kaggle_connector import KaggleConnector

connector = KaggleConnector(
    use_kagglehub=True,
    output_dir="shared/data/1_raw/kaggle"
)

# Download and load dataset
df = connector.extract("owner/dataset-name")

# Inspect data
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns}")
```

### 2. List Dataset Files

```python
# See all files in a dataset before downloading
files = connector.list_dataset_files("owner/dataset-name")
print(f"Available files: {files}")
```

### 3. Extract Specific File

```python
# Download specific file from multi-file dataset
df = connector.extract(
    dataset="owner/dataset-name",
    file_name="specific_file.csv"
)
```

---

## 📝 Creating Custom Connectors

To create a new data connector:

1. **Inherit from BaseConnector**:

```python
from shared.src.data_processing.base_connector import BaseConnector

class MyConnector(BaseConnector):
    def connect(self) -> bool:
        """Establish connection to data source."""
        pass
    
    def extract(self, **kwargs) -> Optional[pl.DataFrame]:
        """Extract data from source."""
        pass
```

2. **Implement Required Methods**:
   - `connect()`: Validate connection to data source
   - `extract()`: Retrieve data and return Polars DataFrame

3. **Use Inherited Utilities**:
   - `save_data()`: Save extracted data
   - `log_extraction_metadata()`: Log extraction details
   - `handle_retry()`: Retry logic for failures

---

## 🔧 Configuration

### Environment Variables

Set these in your `.env` file:

```bash
# Kaggle API (if using traditional API)
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key

# AWS S3 (for future connectors)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# Azure Blob Storage (for future connectors)
AZURE_STORAGE_ACCOUNT=your_account
AZURE_STORAGE_KEY=your_key
```

### Logging

All connectors log to:
- **Console**: INFO level and above
- **File**: `logs/etl/extraction_*.log` (DEBUG level)
- **Metadata**: `logs/etl/extraction_metadata.log`

---

## 📊 Data Output Standards

### File Formats

- **Preferred**: Parquet (better compression, faster reads)
- **Alternate**: CSV (for human readability), Feather (for fast serialization)

### Naming Conventions

- Files: `lowercase_with_underscores.parquet`
- Variables: `lowercase_with_underscores`
- Classes: `PascalCase`

### Data Types (Polars)

- **Dates**: `Date` type
- **Categories**: `Categorical` type
- **Integers**: `Int32` (prefer over `Int64`)
- **Floats**: `Float32` (prefer over `Float64`)

---

## 🧪 Testing

Run unit tests:

```bash
pytest shared/tests/unit/test_data_processing.py
```

Test data extraction:

```bash
python shared/src/data_processing/examples/extract_kaggle_health_data.py
```

---

## 🛠️ Future Enhancements

- [ ] AWS S3 connector
- [ ] Azure Blob Storage connector  
- [ ] Database connectors (PostgreSQL, MySQL)
- [ ] API connectors (REST, GraphQL)
- [ ] Streaming data connectors
- [ ] Data validation on extraction
- [ ] Incremental extraction support

---

## 📚 Additional Resources

- [Kaggle API Documentation](https://www.kaggle.com/docs/api)
- [kagglehub Documentation](https://github.com/Kaggle/kagglehub)
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [BaseConnector API](base_connector.py)

---

**Last Updated**: 2026-03-11  
**Maintainer**: Gen-E2 Data Engineering Team
