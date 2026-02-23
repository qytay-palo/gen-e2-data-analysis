"""
Data Quality Tests for Cleaned Workforce and Capacity Data
User Story 2: Data Cleaning and Standardization

These tests validate the cleaned data files meet all quality standards:
- Schema compliance
- No nulls in critical fields
- Valid categorical values
- Proper data types
- Year ranges
- Positive counts
- No duplicates
- Completeness thresholds
"""

import pytest
import polars as pl
from pathlib import Path
import yaml


@pytest.fixture(scope="module")
def config():
    """Load cleaning configuration."""
    config_path = Path('config/cleaning_rules.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def workforce_df():
    """Load cleaned workforce data."""
    data_path = Path('data/3_interim/workforce_clean.parquet')
    if not data_path.exists():
        pytest.skip(f"Cleaned workforce data not found at {data_path}")
    return pl.read_parquet(data_path)


@pytest.fixture(scope="module")
def capacity_df():
    """Load cleaned capacity data."""
    data_path = Path('data/3_interim/capacity_clean.parquet')
    if not data_path.exists():
        pytest.skip(f"Cleaned capacity data not found at {data_path}")
    return pl.read_parquet(data_path)


class TestWorkforceDataQuality:
    """Data quality tests for cleaned workforce data."""
    
    def test_schema_compliance(self, workforce_df):
        """Verify cleaned workforce data matches expected schema."""
        required_columns = [
            'year', 'sector', 'profession', 'count',
            'source_table', 'outlier_flag', 'has_missing_values'
        ]
        
        for col in required_columns:
            assert col in workforce_df.columns, f"Missing required column: {col}"
    
    def test_data_types(self, workforce_df):
        """Verify all data types are correct."""
        assert workforce_df['year'].dtype == pl.Int32
        assert workforce_df['sector'].dtype == pl.Categorical
        assert workforce_df['profession'].dtype == pl.Categorical
        assert workforce_df['count'].dtype == pl.Int32
        assert workforce_df['source_table'].dtype == pl.String
        assert workforce_df['outlier_flag'].dtype == pl.Boolean
        assert workforce_df['has_missing_values'].dtype == pl.Boolean
    
    def test_no_nulls_critical_fields(self, workforce_df):
        """Verify no null values in critical columns."""
        critical_columns = ['year', 'sector', 'profession', 'count']
        
        for col in critical_columns:
            null_count = workforce_df[col].null_count()
            assert null_count == 0, f"Column '{col}' has {null_count} null values"
    
    def test_valid_sectors(self, workforce_df, config):
        """Verify all sector values are standardized."""
        valid_sectors = set(config['valid_values']['sectors'])
        actual_sectors = set(workforce_df['sector'].unique().to_list())
        
        invalid = actual_sectors - valid_sectors
        assert len(invalid) == 0, f"Invalid sector values found: {invalid}"
    
    def test_valid_professions(self, workforce_df, config):
        """Verify all profession values are valid."""
        valid_professions = set(config['valid_values']['professions'])
        actual_professions = set(workforce_df['profession'].unique().to_list())
        
        invalid = actual_professions - valid_professions
        assert len(invalid) == 0, f"Invalid profession values found: {invalid}"
    
    def test_year_range(self, workforce_df, config):
        """Verify year values are within expected range."""
        min_year = config['value_constraints']['workforce']['year_min']
        max_year = config['value_constraints']['workforce']['year_max']
        
        actual_min = workforce_df['year'].min()
        actual_max = workforce_df['year'].max()
        
        assert actual_min >= min_year, f"Year minimum {actual_min} below {min_year}"
        assert actual_max <= max_year, f"Year maximum {actual_max} above {max_year}"
    
    def test_positive_counts(self, workforce_df):
        """Verify all count values are non-negative."""
        min_count = workforce_df['count'].min()
        assert min_count >= 0, f"Negative count values found: {min_count}"
    
    def test_no_duplicates(self, workforce_df):
        """Verify no duplicate records in cleaned data."""
        # Define uniqueness criteria
        key_cols = ['year', 'sector', 'profession', 'specialist_category', 'nurse_type', 'source_table']
        
        # Filter to only key columns that exist
        existing_keys = [col for col in key_cols if col in workforce_df.columns]
        
        total_rows = len(workforce_df)
        unique_rows = len(workforce_df.unique(subset=existing_keys))
        duplicate_count = total_rows - unique_rows
        
        assert duplicate_count == 0, f"Found {duplicate_count} duplicate records"
    
    def test_completeness_score(self, workforce_df, config):
        """Verify overall data completeness meets target."""
        critical_columns = ['year', 'sector', 'profession', 'count']
        
        total_cells = len(workforce_df) * len(critical_columns)
        null_cells = sum(workforce_df[col].null_count() for col in critical_columns)
        completeness = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0
        
        target = config['quality_thresholds']['completeness_target']
        assert completeness >= target, f"Completeness {completeness:.2f}% below target {target}%"
    
    def test_profession_specific_columns(self, workforce_df):
        """Verify profession-specific columns are handled correctly."""
        if 'specialist_category' in workforce_df.columns:
            # Only doctors should have non-null specialist_category
            nurse_rows = workforce_df.filter(pl.col('profession') == 'Nurse')
            assert nurse_rows['specialist_category'].null_count() == len(nurse_rows), \
                "Nurses should have null specialist_category"
        
        if 'nurse_type' in workforce_df.columns:
            # Only nurses should have non-null nurse_type
            doctor_rows = workforce_df.filter(pl.col('profession') == 'Doctor')
            assert doctor_rows['nurse_type'].null_count() == len(doctor_rows), \
                "Doctors should have null nurse_type"
    
    def test_source_table_values(self, workforce_df):
        """Verify source_table values are valid."""
        valid_sources = {'workforce_doctors', 'workforce_nurses', 'workforce_pharmacists'}
        actual_sources = set(workforce_df['source_table'].unique().to_list())
        
        assert actual_sources == valid_sources, \
            f"Unexpected source_table values: {actual_sources - valid_sources}"
    
    def test_outlier_flag_is_boolean(self, workforce_df):
        """Verify outlier_flag contains only boolean values."""
        unique_values = set(workforce_df['outlier_flag'].unique().to_list())
        assert unique_values.issubset({True, False}), \
            f"outlier_flag has non-boolean values: {unique_values}"
    
    def test_reasonable_outlier_percentage(self, workforce_df, config):
        """Verify outlier percentage doesn't exceed threshold."""
        outlier_count = workforce_df['outlier_flag'].sum()
        total_rows = len(workforce_df)
        outlier_pct = (outlier_count / total_rows * 100) if total_rows > 0 else 0
        
        max_allowed = config['quality_thresholds']['max_outlier_percentage']
        assert outlier_pct <= max_allowed, \
            f"Outlier percentage {outlier_pct:.2f}% exceeds max {max_allowed}%"


class TestCapacityDataQuality:
    """Data quality tests for cleaned capacity data."""
    
    def test_schema_compliance(self, capacity_df):
        """Verify cleaned capacity data has required columns."""
        required_columns = [
            'year', 'num_facilities', 'source_table'
        ]
        
        for col in required_columns:
            assert col in capacity_df.columns, f"Missing required column: {col}"
    
    def test_data_types(self, capacity_df):
        """Verify all data types are correct."""
        assert capacity_df['year'].dtype == pl.Int32
        assert capacity_df['num_facilities'].dtype == pl.Int32
        assert capacity_df['source_table'].dtype == pl.String
        
        # Sector may be Categorical if present
        if 'sector' in capacity_df.columns:
            assert capacity_df['sector'].dtype == pl.Categorical
        
        # num_beds should be Int32 if present
        if 'num_beds' in capacity_df.columns:
            assert capacity_df['num_beds'].dtype == pl.Int32
    
    def test_no_nulls_critical_fields(self, capacity_df):
        """Verify no null values in critical columns."""
        critical_columns = ['year', 'num_facilities']
        
        for col in critical_columns:
            null_count = capacity_df[col].null_count()
            assert null_count == 0, f"Column '{col}' has {null_count} null values"
    
    def test_valid_sectors(self, capacity_df, config):
        """Verify all sector values are standardized (where sector exists)."""
        if 'sector' not in capacity_df.columns:
            pytest.skip("sector column not present in capacity data")
        
        valid_sectors = set(config['valid_values']['sectors'])
        # Exclude nulls from check
        actual_sectors =  set(capacity_df['sector'].drop_nulls().unique().to_list())
        
        invalid = actual_sectors - valid_sectors
        assert len(invalid) == 0, f"Invalid sector values found: {invalid}"
    
    def test_year_range(self, capacity_df, config):
        """Verify year values are within expected range."""
        min_year = config['value_constraints']['capacity']['year_min']
        max_year = config['value_constraints']['capacity']['year_max']
        
        actual_min = capacity_df['year'].min()
        actual_max = capacity_df['year'].max()
        
        assert actual_min >= min_year, f"Year minimum {actual_min} below {min_year}"
        assert actual_max <= max_year, f"Year maximum {actual_max} above {max_year}"
    
    def test_positive_facility_counts(self, capacity_df):
        """Verify all facility count values are non-negative."""
        min_facilities = capacity_df['num_facilities'].min()
        assert min_facilities >= 0, f"Negative facility count found: {min_facilities}"
    
    def test_positive_bed_counts(self, capacity_df):
        """Verify all bed count values are non-negative (where applicable)."""
        if 'num_beds' not in capacity_df.columns:
            pytest.skip("num_beds column not present")
        
        # Exclude nulls (primary care facilities don't have beds)
        min_beds = capacity_df['num_beds'].drop_nulls().min()
        assert min_beds >= 0, f"Negative bed count found: {min_beds}"
    
    def test_completeness_score(self, capacity_df, config):
        """Verify overall data completeness meets target."""
        critical_columns = ['year', 'num_facilities']
        
        total_cells = len(capacity_df) * len(critical_columns)
        null_cells = sum(capacity_df[col].null_count() for col in critical_columns)
        completeness = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0
        
        target = config['quality_thresholds']['completeness_target']
        assert completeness >= target, f"Completeness {completeness:.2f}% below target {target}%"
    
    def test_source_table_values(self, capacity_df):
        """Verify source_table values are valid."""
        valid_sources = {'capacity_hospital_beds', 'capacity_primary_care'}
        actual_sources = set(capacity_df['source_table'].unique().to_list())
        
        assert actual_sources == valid_sources, \
            f"Unexpected source_table values: {actual_sources - valid_sources}"
    
    def test_institution_category_values(self, capacity_df):
        """Verify institution_category values are valid (if present)."""
        if 'institution_category' not in capacity_df.columns:
            pytest.skip("institution_category column not present")
        
        valid_categories = {'Hospital', 'Primary Care'}
        actual_categories = set(capacity_df['institution_category'].unique().to_list())
        
        invalid = actual_categories - valid_categories
        assert len(invalid) == 0, f"Invalid institution_category values: {invalid}"
    
    def test_hospital_beds_have_num_beds(self, capacity_df):
        """Verify hospital facilities have bed counts."""
        if 'num_beds' not in capacity_df.columns:
            pytest.skip("num_beds column not present")
        
        if 'institution_category' in capacity_df.columns:
            hospital_rows = capacity_df.filter(pl.col('institution_category') == 'Hospital')
            if len(hospital_rows) > 0:
                # Hospital beds should have non-null num_beds
                null_beds = hospital_rows['num_beds'].null_count()
                assert null_beds == 0, f"Hospital rows have {null_beds} null bed counts"


class TestCrossDatasetValidation:
    """Cross-dataset validation tests."""
    
    def test_overlapping_year_range(self, workforce_df, capacity_df):
        """Verify workforce and capacity data have overlapping years."""
        workforce_years = set(workforce_df['year'].unique().to_list())
        capacity_years = set(capacity_df['year'].unique().to_list())
        
        overlap = workforce_years & capacity_years
        assert len(overlap) > 0, "No overlapping years between workforce and capacity data"
        
        # Log the overlap for reference
        print(f"Overlapping years: {sorted(overlap)}")
        print(f"Overlap period: {min(overlap)}-{max(overlap)} ({len(overlap)} years)")
    
    def test_record_counts_reasonable(self, workforce_df, capacity_df):
        """Verify cleaned datasets have reasonable record counts."""
        # Workforce should have multiple years * sectors * professions
        assert len(workforce_df) > 50, f"Workforce records ({len(workforce_df)}) seem too few"
        
        # Capacity should have multiple years * facility types
        assert len(capacity_df) > 20, f"Capacity records ({len(capacity_df)}) seem too few"
    
    def test_data_freshness(self, workforce_df, capacity_df):
        """Verify datasets contain recent data."""
        workforce_max_year = workforce_df['year'].max()
        capacity_max_year = capacity_df['year'].max()
        
        # Should have data up to at least 2018
        assert workforce_max_year >= 2018, f"Workforce data only up to {workforce_max_year}"
        assert capacity_max_year >= 2018, f"Capacity data only up to {capacity_max_year}"
