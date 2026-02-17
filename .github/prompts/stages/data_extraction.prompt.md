---
description: Data Extraction Stage
stage: Data Acquisition
---

# Stage Prompt: Data Extraction

## Objective

Extract data from configured sources and organize it according to the project structure for automated, efficient data acquisition using Python scripts and standard file operations.

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Data Source Configuration**: `config/data_sources.yml`
   - Connection details (if database)
   - File paths (if file-based)
   - API endpoints (if API-based)
   - Authentication credentials (from environment variables)

2. **Extraction Queries** (if applicable): `sql/extractions/`
   - SQL queries for database extraction
   - Query parameters and filters

3. **Target Epic/User Story**: 
   - Epic number (e.g., epic-001)
   - User story identifier
   - Data requirements from user story acceptance criteria

4. **Project Context** (REQUIRED - read before extraction):
   - **Available data sources**: `docs/project_context/data_sources.md`
   - **Technical stack capabilities**: `docs/project_context/tech_stack.md`
   - **Business objectives**: `docs/project_context/business-objectives.md`
   
   **Read these files** to understand:
   - What data sources are available and how to access them
   - What technical platforms and tools are approved
   - What business objectives drive data needs

## Output Requirements

The extraction MUST produce:

1. **Raw Data Files**: `data/1_raw/{epic_id}/`
   - Original, immutable source data
   - Filename format: `{source_name}_{timestamp}.{format}`
   - Supported formats: CSV, JSON, Parquet, Excel

2. **Schema Documentation**: `data/schemas/{epic_id}/`
   - Data dictionary for each extracted dataset
   - Column names, data types, descriptions
   - Sample values and value ranges

3. **Extraction Metadata**: `data/1_raw/{epic_id}/metadata.json`
   - Extraction timestamp
   - Source system and version
   - Row counts and file sizes
   - Extraction parameters used

4. **Extraction Log**: `logs/etl/extraction_{epic_id}_{timestamp}.log`
   - Extraction start/end times
   - Success/failure status
   - Any warnings or errors encountered
   - Data quality summary

## Execution Steps

### Step 1: Pre-Extraction Setup

```
1. Read config/data_sources.yml to get data source configurations
2. Identify the data sources needed for this epic
3. Create target directory: data/1_raw/{epic_id}/
4. Create schema directory: data/schemas/{epic_id}/
5. List existing files to check for duplicates
```

### Step 2: Data Extraction

#### For Database Sources (SQLite/SQL):
```
1. Connect to the source database using appropriate Python libraries (sqlite3, sqlalchemy, etc.)
2. For each extraction query in sql/extractions/:
   a. Read the SQL query file
   b. Execute the query
   c. Save results to data/1_raw/{epic_id}/{table_name}.csv
   d. Record row count and extraction time
```

#### For File-Based Sources:
```
1. Read source file locations from config
2. Copy or read source files using polars, standard file operations
3. Write to data/1_raw/{epic_id}/
4. Verify file integrity (size, format)
```

#### For API Sources:
```
1. Read API configuration from config folder
2. Make API calls using requests library
3. Save API responses to data/1_raw/{epic_id}/
4. Handle pagination and rate limiting
```

### Step 3: Schema Documentation

```
1. Analyze the structure of each extracted dataset using polars
2. Generate data dictionary with:
   - Column names
   - Data types (inferred)
   - Non-null counts
   - Unique value counts
   - Sample values (first 5)
3. Write schema documentation to data/schemas/{epic_id}/{dataset_name}_schema.md
```

### Step 4: Metadata Generation

```
1. Collect extraction metadata:
   - Timestamp: Current datetime
   - Source: From config/data_sources.yml
   - Row count: From extracted data
   - File size: From file system (os.path.getsize)
   - Extraction parameters: Query filters, date ranges, etc.
2. Format as JSON
3. Write to data/1_raw/{epic_id}/metadata.json
```

### Step 5: Logging

```
1. Create extraction log with:
   - Epic ID and user story reference
   - Start time and end time
   - List of extracted datasets with row counts
   - Success/failure status for each source
   - Any errors or warnings
2. Write log to logs/etl/extraction_{epic_id}_{timestamp}.log using Python logging module
```

### Step 6: Verification

```
1. List all files in data/1_raw/{epic_id}/ using os.listdir or pathlib
2. Verify each expected file exists using os.path.exists
3. Check file sizes (should be > 0) using os.path.getsize
4. Read first 5 rows of each dataset using polars.read_csv(nrows=5)
5. Verify schema files exist in data/schemas/{epic_id}/
6. Verify metadata.json exists and is valid JSON using json.load
7. Verify extraction log exists in logs/etl/
```

## Quality Checks

After extraction, perform these quality checks:

### 1. Completeness Check
```
- All expected datasets extracted? (compare with data source config)
- Row counts match expectations? (compare with source system if possible)
- All columns present? (compare with schema documentation)
```

### 2. Integrity Check
```
- Files are not corrupted (can be opened and read)
- Data types are as expected
- No completely empty files (size > 0)
```

### 3. Documentation Check
```
- Schema documentation exists for each dataset
- Metadata.json is present and valid
- Extraction log is complete and informative
```

## Error Handling

If extraction fails or encounters issues:

1. **Write detailed error log** to `logs/errors/extraction_{epic_id}_{timestamp}.log`
2. **Document the specific failure**:
   - Which data source failed
   - Error message and stack trace
   - Potential root causes
   - Suggested remediation steps
3. **Partial Success Handling**:
   - If some datasets extracted successfully, document which ones
   - Mark failed extractions clearly in the log
   - Continue with available data if acceptable

## Success Criteria

The data extraction is considered successful when:

- ✅ All required datasets are extracted and saved to `data/1_raw/{epic_id}/`
- ✅ All files are non-empty and readable
- ✅ Schema documentation exists for each dataset in `data/schemas/{epic_id}/`
- ✅ Metadata file `metadata.json` is present and valid
- ✅ Extraction log exists in `logs/etl/` and shows success status
- ✅ Quality checks pass (completeness, integrity, documentation)

## Extraction Summary

At the end of extraction, document the extraction summary:

```markdown
### Extraction Summary

**Files and Directories**:
- Created directories: data/1_raw/epic-001/, data/schemas/epic-001/
- Files written: 5 datasets, 5 schema docs, 1 metadata file, 1 log file
- Files read: config/data_sources.yml, sql/extractions/*.sql
- Verification: Listed directories, checked file sizes, read sample rows

**Database Operations** (if applicable):
- Executed queries: 3 extraction queries from sql/extractions/
- Tables accessed: patient_visits, diagnoses, treatments
- Total rows extracted: 125,000 rows
```

## Next Stage

After successful data extraction, proceed to:
- **Data Quality Assessment** stage: Validate data completeness and integrity
- **Exploratory Data Analysis** stage: Initial analysis and profiling

## References

- Data Sources: `docs/project_context/data_sources.md`
- Tech Stack: `docs/project_context/tech_stack.md`
- Project Structure: `README.md`
