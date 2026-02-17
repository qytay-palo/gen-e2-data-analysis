---
name: 'Data Validation and Quality Assurance'
description: 'Standards for data quality checks, validation rules, and quality reporting'
applyTo: 'src/data_processing/*validator*.py, src/data_processing/*quality*.py, src/data_processing/*profiler*.py, data/3_interim/**, logs/etl/**, tests/data/**, notebooks/1_exploratory/*profile*.ipynb, notebooks/1_exploratory/*quality*.ipynb'
---

## Purpose
This document defines **mandatory data quality standards** and validation procedures. Apply these practices to ensure data integrity throughout the analysis pipeline.

## Core Principles

### 1. Validation at Every Stage
- **ALWAYS validate data** immediately after loading
- **ALWAYS validate data** before critical transformations
- **ALWAYS validate data** before saving to `data/4_processed/`
- Generate quality reports for each validation stage

### 2. Explicit Null Handling
- **NEVER ignore missing values** silently
- Document missing value patterns and decisions
- Choose appropriate strategy: impute, drop, or keep as missing
- Log how many values were affected

### 3. Schema Enforcement
- Define expected schemas for all datasets
- Validate column names, data types, and value ranges
- Reject data that doesn't match schema expectations
- Version your schemas and document changes

## Required Validation Checks

### Level 1: Schema Validation (MANDATORY)

```python
# src/data_processing/schemas.py
import polars as pl
from typing import Dict, List, Optional
from dataclasses import dataclass
from loguru import logger

@dataclass
class ColumnSchema:
    """Schema definition for a single column."""
    name: str
    dtype: pl.DataType
    nullable: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List] = None
    description: str = ""

@dataclass
class DatasetSchema:
    """Schema definition for a complete dataset."""
    name: str
    columns: List[ColumnSchema]
    version: str = "1.0.0"
    
    def get_column_names(self) -> List[str]:
        """Return list of expected column names."""
        return [col.name for col in self.columns]
    
    def get_polars_schema(self) -> Dict[str, pl.DataType]:
        """Return Polars schema dictionary."""
        return {col.name: col.dtype for col in self.columns}

# Define schema for disease surveillance data
DISEASE_SURVEILLANCE_SCHEMA = DatasetSchema(
    name="disease_surveillance",
    version="1.0.0",
    columns=[
        ColumnSchema(
            name="disease",
            dtype=pl.Utf8,
            nullable=False,
            description="Disease name (e.g., 'Dengue Fever')"
        ),
        ColumnSchema(
            name="epi_week",
            dtype=pl.Int32,
            nullable=False,
            min_value=1,
            max_value=53,
            description="Epidemiological week number"
        ),
        ColumnSchema(
            name="year",
            dtype=pl.Int32,
            nullable=False,
            min_value=2000,
            max_value=2030,
            description="Calendar year"
        ),
        ColumnSchema(
            name="case_count",
            dtype=pl.Int64,
            nullable=False,
            min_value=0,
            description="Number of reported cases"
        ),
        ColumnSchema(
            name="reporting_date",
            dtype=pl.Date,
            nullable=False,
            description="Date of report submission"
        ),
    ]
)

def validate_schema(
    df: pl.DataFrame,
    schema: DatasetSchema,
    strict: bool = True
) -> tuple[bool, List[str]]:
    """Validate DataFrame against schema definition.
    
    Args:
        df: DataFrame to validate
        schema: Expected schema definition
        strict: If True, fail on any schema violation
        
    Returns:
        Tuple of (is_valid, list of error messages)
        
    Example:
        >>> is_valid, errors = validate_schema(df, DISEASE_SURVEILLANCE_SCHEMA)
        >>> if not is_valid:
        >>>     logger.error(f"Schema validation failed: {errors}")
    """
    errors = []
    
    # Check column names
    expected_cols = set(schema.get_column_names())
    actual_cols = set(df.columns)
    
    missing = expected_cols - actual_cols
    if missing:
        errors.append(f"Missing required columns: {missing}")
    
    extra = actual_cols - expected_cols
    if extra and strict:
        errors.append(f"Unexpected columns found: {extra}")
    
    # Check data types
    for col_schema in schema.columns:
        if col_schema.name not in df.columns:
            continue
            
        actual_dtype = df[col_schema.name].dtype
        if actual_dtype != col_schema.dtype:
            errors.append(
                f"Column '{col_schema.name}': expected {col_schema.dtype}, "
                f"got {actual_dtype}"
            )
    
    # Check null constraints
    for col_schema in schema.columns:
        if not col_schema.nullable and col_schema.name in df.columns:
            null_count = df[col_schema.name].null_count()
            if null_count > 0:
                errors.append(
                    f"Column '{col_schema.name}': found {null_count} null values "
                    f"(null not allowed)"
                )
    
    # Check value ranges
    for col_schema in schema.columns:
        if col_schema.name not in df.columns:
            continue
            
        col = df[col_schema.name]
        
        if col_schema.min_value is not None:
            min_val = col.min()
            if min_val is not None and min_val < col_schema.min_value:
                errors.append(
                    f"Column '{col_schema.name}': minimum value {min_val} "
                    f"below threshold {col_schema.min_value}"
                )
        
        if col_schema.max_value is not None:
            max_val = col.max()
            if max_val is not None and max_val > col_schema.max_value:
                errors.append(
                    f"Column '{col_schema.name}': maximum value {max_val} "
                    f"above threshold {col_schema.max_value}"
                )
        
        if col_schema.allowed_values is not None:
            unique_vals = set(col.unique().to_list())
            invalid_vals = unique_vals - set(col_schema.allowed_values)
            if invalid_vals:
                errors.append(
                    f"Column '{col_schema.name}': invalid values found: {invalid_vals}"
                )
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info(f"Schema validation passed for {schema.name} v{schema.version}")
    else:
        logger.error(f"Schema validation failed with {len(errors)} errors")
        for error in errors:
            logger.error(f"  - {error}")
    
    return is_valid, errors
```

### Level 2: Data Quality Profiling (MANDATORY)

```python
# src/data_processing/data_quality_profiler.py
import polars as pl
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger
import yaml

class DataQualityProfiler:
    """Generate comprehensive data quality reports."""
    
    def __init__(self, df: pl.DataFrame, dataset_name: str = "dataset"):
        """Initialize profiler with DataFrame.
        
        Args:
            df: DataFrame to profile
            dataset_name: Descriptive name for the dataset
        """
        self.df = df
        self.dataset_name = dataset_name
        self.profile_timestamp = datetime.now()
    
    def generate_profile(self) -> Dict[str, Any]:
        """Generate comprehensive data quality profile.
        
        Returns:
            Dictionary containing quality metrics
        """
        logger.info(f"Generating quality profile for {self.dataset_name}")
        
        profile = {
            'dataset_name': self.dataset_name,
            'profile_timestamp': self.profile_timestamp.isoformat(),
            'row_count': len(self.df),
            'column_count': len(self.df.columns),
            'memory_usage_bytes': self.df.estimated_size(),
            'columns': {}
        }
        
        # Profile each column
        for col in self.df.columns:
            col_profile = self._profile_column(col)
            profile['columns'][col] = col_profile
        
        # Add summary statistics
        profile['summary'] = self._generate_summary(profile)
        
        return profile
    
    def _profile_column(self, col_name: str) -> Dict[str, Any]:
        """Profile a single column.
        
        Args:
            col_name: Name of column to profile
            
        Returns:
            Dictionary of column statistics
        """
        col = self.df[col_name]
        
        profile = {
            'dtype': str(col.dtype),
            'null_count': int(col.null_count()),
            'null_percentage': float(col.null_count() / len(self.df) * 100),
            'unique_count': int(col.n_unique()),
            'unique_percentage': float(col.n_unique() / len(self.df) * 100),
        }
        
        # Type-specific statistics
        if col.dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
            # Numeric column
            profile.update({
                'min': float(col.min()) if col.min() is not None else None,
                'max': float(col.max()) if col.max() is not None else None,
                'mean': float(col.mean()) if col.mean() is not None else None,
                'median': float(col.median()) if col.median() is not None else None,
                'std': float(col.std()) if col.std() is not None else None,
                'quartiles': {
                    'q25': float(col.quantile(0.25)) if col.quantile(0.25) is not None else None,
                    'q75': float(col.quantile(0.75)) if col.quantile(0.75) is not None else None,
                },
                'outliers_iqr': self._detect_outliers_iqr(col)
            })
        
        elif col.dtype == pl.Utf8:
            # String column
            profile.update({
                'min_length': int(col.str.lengths().min()) if col.str.lengths().min() is not None else None,
                'max_length': int(col.str.lengths().max()) if col.str.lengths().max() is not None else None,
                'mean_length': float(col.str.lengths().mean()) if col.str.lengths().mean() is not None else None,
                'sample_values': col.drop_nulls().head(5).to_list(),
            })
            
            # Include top values if categorical
            if col.n_unique() < 100:
                value_counts = col.value_counts().head(10)
                profile['top_values'] = [
                    {'value': row[0], 'count': int(row[1])}
                    for row in value_counts.iter_rows()
                ]
        
        elif col.dtype == pl.Date:
            # Date column
            profile.update({
                'min_date': str(col.min()) if col.min() is not None else None,
                'max_date': str(col.max()) if col.max() is not None else None,
                'date_range_days': (col.max() - col.min()).days if col.max() and col.min() else None,
            })
        
        return profile
    
    def _detect_outliers_iqr(self, col: pl.Series) -> int:
        """Detect outliers using IQR method.
        
        Args:
            col: Numeric column
            
        Returns:
            Count of outliers
        """
        q1 = col.quantile(0.25)
        q3 = col.quantile(0.75)
        
        if q1 is None or q3 is None:
            return 0
        
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = col.filter((col < lower_bound) | (col > upper_bound))
        return len(outliers)
    
    def _generate_summary(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics across all columns.
        
        Args:
            profile: Full profile dictionary
            
        Returns:
            Summary statistics
        """
        columns = profile['columns']
        
        return {
            'total_null_cells': sum(col['null_count'] for col in columns.values()),
            'null_percentage': sum(col['null_count'] for col in columns.values()) / 
                             (profile['row_count'] * profile['column_count']) * 100,
            'columns_with_nulls': sum(1 for col in columns.values() if col['null_count'] > 0),
            'columns_all_unique': sum(1 for col in columns.values() 
                                     if col['unique_count'] == profile['row_count']),
            'numeric_columns': sum(1 for col in columns.values() 
                                  if 'mean' in col),
            'text_columns': sum(1 for col in columns.values() 
                               if 'min_length' in col),
            'date_columns': sum(1 for col in columns.values() 
                               if 'min_date' in col),
        }
    
    def save_profile(self, output_dir: str = 'logs/etl') -> Path:
        """Save quality profile to file.
        
        Args:
            output_dir: Directory to save profile
            
        Returns:
            Path to saved profile file
        """
        profile = self.generate_profile()
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as YAML
        timestamp = self.profile_timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"{self.dataset_name}_quality_profile_{timestamp}.yml"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            yaml.dump(profile, f, default_flow_style=False, sort_keys=False)
        
        logger.info(f"Quality profile saved to: {filepath}")
        return filepath
    
    def generate_markdown_report(self, output_dir: str = 'logs/etl') -> Path:
        """Generate human-readable markdown quality report.
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            Path to saved markdown report
        """
        profile = self.generate_profile()
        
        # Create markdown content
        md_lines = [
            f"# Data Quality Report: {self.dataset_name}",
            f"\n**Generated**: {self.profile_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n## Dataset Overview",
            f"\n- **Rows**: {profile['row_count']:,}",
            f"- **Columns**: {profile['column_count']}",
            f"- **Memory Usage**: {profile['memory_usage_bytes'] / 1024 / 1024:.2f} MB",
            f"\n## Data Quality Summary",
            f"\n- **Total Null Cells**: {profile['summary']['total_null_cells']:,} "
            f"({profile['summary']['null_percentage']:.2f}%)",
            f"- **Columns with Nulls**: {profile['summary']['columns_with_nulls']} / {profile['column_count']}",
            f"- **Numeric Columns**: {profile['summary']['numeric_columns']}",
            f"- **Text Columns**: {profile['summary']['text_columns']}",
            f"- **Date Columns**: {profile['summary']['date_columns']}",
            f"\n## Column Details",
            f"\n| Column | Type | Nulls | Unique | Statistics |",
            f"|--------|------|-------|--------|------------|"
        ]
        
        for col_name, col_profile in profile['columns'].items():
            stats = []
            
            if 'mean' in col_profile:
                stats.append(f"μ={col_profile['mean']:.2f}")
                stats.append(f"σ={col_profile['std']:.2f}")
                stats.append(f"range=[{col_profile['min']:.2f}, {col_profile['max']:.2f}]")
            elif 'min_length' in col_profile:
                stats.append(f"len={col_profile['mean_length']:.1f} avg")
            elif 'min_date' in col_profile:
                stats.append(f"{col_profile['min_date']} to {col_profile['max_date']}")
            
            md_lines.append(
                f"| {col_name} | {col_profile['dtype']} | "
                f"{col_profile['null_percentage']:.1f}% | "
                f"{col_profile['unique_count']:,} | "
                f"{', '.join(stats)} |"
            )
        
        # Issues and recommendations
        md_lines.extend([
            f"\n## Issues Detected",
            ""
        ])
        
        issues_found = False
        for col_name, col_profile in profile['columns'].items():
            if col_profile['null_percentage'] > 50:
                md_lines.append(f"- ⚠️ **{col_name}**: High null rate ({col_profile['null_percentage']:.1f}%)")
                issues_found = True
            
            if 'outliers_iqr' in col_profile and col_profile['outliers_iqr'] > 0:
                md_lines.append(f"- ⚠️ **{col_name}**: {col_profile['outliers_iqr']} outliers detected")
                issues_found = True
        
        if not issues_found:
            md_lines.append("- ✅ No major issues detected")
        
        # Save markdown report
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = self.profile_timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"{self.dataset_name}_quality_report_{timestamp}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(md_lines))
        
        logger.info(f"Quality report saved to: {filepath}")
        return filepath

# Usage example
if __name__ == '__main__':
    # Load data
    df = pl.read_csv('data/1_raw/disease_data.csv')
    
    # Create profiler and generate reports
    profiler = DataQualityProfiler(df, dataset_name='disease_surveillance')
    profiler.save_profile(output_dir='logs/etl')
    profiler.generate_markdown_report(output_dir='logs/etl')
```

### Level 3: Business Rule Validation

```python
# src/data_processing/disease_data_validator.py
import polars as pl
from typing import List, Dict, Tuple
from loguru import logger
from datetime import date

class DiseaseDataValidator:
    """Validate disease surveillance data against business rules."""
    
    def __init__(self, df: pl.DataFrame):
        """Initialize validator.
        
        Args:
            df: Disease surveillance DataFrame
        """
        self.df = df
        self.validation_results: List[Dict] = []
    
    def validate_all(self) -> Tuple[bool, List[Dict]]:
        """Run all validation checks.
        
        Returns:
            Tuple of (all_passed, list of validation results)
        """
        logger.info("Starting comprehensive data validation")
        
        self.validation_results = []
        
        # Run all validation rules
        self._validate_date_consistency()
        self._validate_case_counts()
        self._validate_epi_week_ranges()
        self._validate_disease_names()
        self._validate_completeness()
        self._validate_duplicates()
        
        # Check if all passed
        all_passed = all(result['passed'] for result in self.validation_results)
        
        if all_passed:
            logger.info("✅ All validation checks passed")
        else:
            failed = [r for r in self.validation_results if not r['passed']]
            logger.error(f"❌ {len(failed)} validation check(s) failed")
        
        return all_passed, self.validation_results
    
    def _validate_date_consistency(self) -> None:
        """Validate date fields are consistent."""
        logger.info("Validating date consistency")
        
        # Check if reporting_date year matches year column
        inconsistent = self.df.filter(
            pl.col('reporting_date').dt.year() != pl.col('year')
        )
        
        passed = len(inconsistent) == 0
        
        self.validation_results.append({
            'rule': 'date_consistency',
            'description': 'Reporting date year matches year column',
            'passed': passed,
            'failure_count': len(inconsistent),
            'severity': 'ERROR'
        })
        
        if not passed:
            logger.error(f"Found {len(inconsistent)} rows with date inconsistencies")
    
    def _validate_case_counts(self) -> None:
        """Validate case count values are reasonable."""
        logger.info("Validating case counts")
        
        # Check for negative case counts
        negative_cases = self.df.filter(pl.col('case_count') < 0)
        
        # Check for suspiciously high case counts (> 10,000)
        high_cases = self.df.filter(pl.col('case_count') > 10000)
        
        passed = len(negative_cases) == 0
        
        self.validation_results.append({
            'rule': 'case_count_non_negative',
            'description': 'Case counts must be non-negative',
            'passed': passed,
            'failure_count': len(negative_cases),
            'severity': 'ERROR'
        })
        
        self.validation_results.append({
            'rule': 'case_count_reasonable',
            'description': 'Case counts should be < 10,000',
            'passed': len(high_cases) == 0,
            'failure_count': len(high_cases),
            'severity': 'WARNING'
        })
    
    def _validate_epi_week_ranges(self) -> None:
        """Validate epidemiological week numbers."""
        logger.info("Validating epi week ranges")
        
        invalid_weeks = self.df.filter(
            (pl.col('epi_week') < 1) | (pl.col('epi_week') > 53)
        )
        
        passed = len(invalid_weeks) == 0
        
        self.validation_results.append({
            'rule': 'epi_week_valid_range',
            'description': 'Epi week must be between 1 and 53',
            'passed': passed,
            'failure_count': len(invalid_weeks),
            'severity': 'ERROR'
        })
    
    def _validate_disease_names(self) -> None:
        """Validate disease names against known list."""
        logger.info("Validating disease names")
        
        # Known valid disease names
        valid_diseases = {
            'Dengue Fever',
            'Hand, Foot and Mouth Disease',
            'Influenza',
            'COVID-19',
            'Tuberculosis',
            'Chickenpox'
        }
        
        unique_diseases = set(self.df['disease'].unique().to_list())
        invalid_diseases = unique_diseases - valid_diseases
        
        passed = len(invalid_diseases) == 0
        
        self.validation_results.append({
            'rule': 'disease_names_valid',
            'description': 'Disease names must be from approved list',
            'passed': passed,
            'failure_count': len(invalid_diseases),
            'invalid_values': list(invalid_diseases),
            'severity': 'WARNING'
        })
    
    def _validate_completeness(self) -> None:
        """Validate data completeness for critical time periods."""
        logger.info("Validating data completeness")
        
        # Check if we have data for all weeks in each year
        year_week_combinations = self.df.select(['year', 'epi_week', 'disease']).unique()
        
        expected_weeks_per_year = 52  # Simplified
        years = self.df['year'].unique().to_list()
        diseases = self.df['disease'].unique().to_list()
        
        expected_rows = len(years) * len(diseases) * expected_weeks_per_year
        actual_rows = len(year_week_combinations)
        
        completeness_ratio = actual_rows / expected_rows if expected_rows > 0 else 0
        
        passed = completeness_ratio >= 0.95  # At least 95% complete
        
        self.validation_results.append({
            'rule': 'data_completeness',
            'description': 'Data should be >95% complete for all year/week/disease combinations',
            'passed': passed,
            'completeness_ratio': completeness_ratio,
            'severity': 'WARNING'
        })
    
    def _validate_duplicates(self) -> None:
        """Check for duplicate records."""
        logger.info("Checking for duplicate records")
        
        # Define uniqueness constraint: year, epi_week, disease
        unique_key_cols = ['year', 'epi_week', 'disease']
        
        total_rows = len(self.df)
        unique_rows = len(self.df.select(unique_key_cols).unique())
        
        duplicate_count = total_rows - unique_rows
        passed = duplicate_count == 0
        
        self.validation_results.append({
            'rule': 'no_duplicates',
            'description': 'No duplicate records for (year, epi_week, disease)',
            'passed': passed,
            'failure_count': duplicate_count,
            'severity': 'ERROR'
        })
    
    def generate_validation_report(self, output_path: str = 'logs/etl/validation_report.md') -> None:
        """Generate markdown validation report.
        
        Args:
            output_path: Path to save validation report
        """
        from pathlib import Path
        from datetime import datetime
        
        if not self.validation_results:
            logger.warning("No validation results to report. Run validate_all() first.")
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        md_lines = [
            "# Data Validation Report",
            f"\n**Generated**: {timestamp}",
            f"**Dataset**: {len(self.df)} rows",
            f"\n## Summary",
            f"\n**Total Checks**: {len(self.validation_results)}",
            f"**Passed**: {sum(1 for r in self.validation_results if r['passed'])}",
            f"**Failed**: {sum(1 for r in self.validation_results if not r['passed'])}",
            f"\n## Validation Results",
            f"\n| Rule | Description | Status | Failures | Severity |",
            f"|------|-------------|--------|----------|----------|"
        ]
        
        for result in self.validation_results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            failures = result.get('failure_count', 0)
            severity = result['severity']
            
            md_lines.append(
                f"| {result['rule']} | {result['description']} | "
                f"{status} | {failures} | {severity} |"
            )
        
        # Add details for failed checks
        failed_checks = [r for r in self.validation_results if not r['passed']]
        if failed_checks:
            md_lines.extend([
                f"\n## Failed Check Details",
                ""
            ])
            
            for result in failed_checks:
                md_lines.append(f"\n### {result['rule']}")
                md_lines.append(f"\n- **Description**: {result['description']}")
                md_lines.append(f"- **Failures**: {result.get('failure_count', 'N/A')}")
                md_lines.append(f"- **Severity**: {result['severity']}")
                
                if 'invalid_values' in result:
                    md_lines.append(f"- **Invalid Values**: {result['invalid_values']}")
        
        # Save report
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(md_lines))
        
        logger.info(f"Validation report saved to: {output_file}")

# Usage example
if __name__ == '__main__':
    df = pl.read_csv('data/1_raw/disease_data.csv')
    
    validator = DiseaseDataValidator(df)
    all_passed, results = validator.validate_all()
    validator.generate_validation_report('logs/etl/validation_report.md')
    
    if not all_passed:
        logger.error("Data validation failed! Review report before proceeding.")
```

## Validation Workflow

```python
# Complete validation workflow example
def validate_and_clean_disease_data(
    input_path: str,
    output_path: str,
    schema: DatasetSchema
) -> pl.DataFrame:
    """Complete validation and cleaning workflow.
    
    Args:
        input_path: Path to raw data file
        output_path: Path to save cleaned data
        schema: Expected data schema
        
    Returns:
        Cleaned and validated DataFrame
    """
    from loguru import logger
    
    logger.info(f"Starting validation workflow for: {input_path}")
    
    # 1. Load data
    df = pl.read_csv(input_path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # 2. Schema validation
    is_valid, errors = validate_schema(df, schema, strict=False)
    if not is_valid:
        logger.error(f"Schema validation failed: {errors}")
        raise ValueError("Schema validation failed")
    
    # 3. Quality profiling
    profiler = DataQualityProfiler(df, dataset_name='disease_surveillance')
    profiler.save_profile()
    profiler.generate_markdown_report()
    
    # 4. Business rule validation
    validator = DiseaseDataValidator(df)
    all_passed, results = validator.validate_all()
    validator.generate_validation_report()
    
    if not all_passed:
        critical_failures = [
            r for r in results 
            if not r['passed'] and r['severity'] == 'ERROR'
        ]
        if critical_failures:
            raise ValueError(f"Critical validation failures: {critical_failures}")
    
    # 5. Save validated data to interim directory
    from pathlib import Path
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(output_file)
    logger.info(f"Saved validated data to: {output_file}")
    
    return df
```

## Quality Metrics to Track

### Required Metrics
- **Completeness**: % of expected data present
- **Validity**: % of values matching expected formats/ranges
- **Consistency**: % of values consistent across related fields
- **Accuracy**: % of values matching ground truth (where available)
- **Timeliness**: Data freshness relative to reporting schedule
- **Uniqueness**: % of records without duplicates

### Quality Thresholds

```yaml
# config/quality_thresholds.yml
quality_thresholds:
  completeness:
    minimum: 0.95  # 95% data present
    target: 0.99
  
  validity:
    minimum: 0.98  # 98% valid values
    target: 1.0
  
  consistency:
    minimum: 0.99
    target: 1.0
  
  duplicates:
    maximum: 0.0  # Zero duplicates allowed
  
  null_rates:
    critical_columns: 0.0  # No nulls in critical columns
    other_columns: 0.1  # Max 10% nulls in other columns
```

## Anti-Patterns (AVOID)

```python
# ❌ DON'T: Silent null handling
df = df.drop_nulls()  # Which rows? How many?

# ✅ DO: Explicit logging
null_count = df.null_count().sum()
logger.info(f"Dropping {null_count} rows with null values")
df = df.drop_nulls(subset=['critical_column'])

# ❌ DON'T: No validation before processing
df = pl.read_csv('data.csv')
df = df.with_columns(pl.col('date').str.strptime(pl.Date))  # Might fail

# ✅ DO: Validate first
df = pl.read_csv('data.csv')
is_valid, errors = validate_schema(df, EXPECTED_SCHEMA)
if not is_valid:
    raise ValueError(f"Schema validation failed: {errors}")

# ❌ DON'T: Ignore outliers
df = df.filter(pl.col('case_count') > 0)  # Silent removal

# ✅ DO: Document and investigate
outliers = df.filter(pl.col('case_count') > 10000)
logger.warning(f"Found {len(outliers)} potential outliers (case_count > 10,000)")
# Save outliers for review
outliers.write_csv('logs/etl/outliers_for_review.csv')
```

## Summary Checklist

Before proceeding to analysis, verify:

- [ ] **Schema validated**: All columns present with correct types
- [ ] **Quality profile generated**: Saved to `logs/etl/`
- [ ] **Business rules checked**: All validation rules passed or warnings documented
- [ ] **Null values handled**: Missing value strategy documented and logged
- [ ] **Duplicates removed**: No duplicate records remain
- [ ] **Outliers investigated**: Extreme values reviewed and documented
- [ ] **Data saved**: Validated data saved to `data/3_interim/` with timestamp
- [ ] **Reports generated**: Quality report and validation report created
- [ ] **Thresholds met**: All quality metrics meet minimum thresholds
