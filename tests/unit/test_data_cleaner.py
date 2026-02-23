"""
Unit Tests for Data Cleaning Functions
User Story 2: Data Cleaning and Standardization

Tests all data cleaning functions with various scenarios:
- Column standardization
- Table unification  
- Data type conversion
- Sector name standardization
- Missing value handling
- Duplicate detection
- Outlier detection
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
import polars as pl
from src.data_processing.data_cleaner import (
    standardize_column_names,
    unify_workforce_tables,
    convert_data_types,
    standardize_sector_names,
    analyze_missing_values,
    handle_missing_values,
    detect_duplicates,
    detect_and_flag_outliers
)


@pytest.fixture
def sample_raw_workforce():
    """Sample raw workforce data with inconsistent naming."""
    return pl.DataFrame({
        'Year': [2018, 2019],
        'Sector': ['Public', 'Private'],
        'Count': [100, 150]
    })


@pytest.fixture
def sample_workforce_with_duplicates():
    """Sample workforce data with duplicates."""
    return pl.DataFrame({
        'year': [2018, 2018, 2019, 2020],
        'sector': ['Public', 'Public', 'Private', 'Private'],
        'count': [100, 100, 150, 200]  # Row 1 and 2 are exact duplicates
    })


@pytest.fixture
def sample_doctors_df():
    """Sample doctors workforce data."""
    return pl.DataFrame({
        'year': [2018, 2019],
        'sector': ['Public', 'Private'],
        'specialist_category': ['Specialists', 'Non-Specialists'],
        'count': [50, 75]
    })


@pytest.fixture
def sample_nurses_df():
    """Sample nurses workforce data."""
    return pl.DataFrame({
        'year': [2018, 2019],
        'nurse_type': ['Registered Nurses', 'Enrolled Nurses'],
        'sector': ['Public', 'Private'],
        'count': [200, 150]
    })


@pytest.fixture
def sample_pharmacists_df():
    """Sample pharmacists workforce data."""
    return pl.DataFrame({
        'year': [2018, 2019],
        'sector': ['Public', 'Private'],
        'count': [30, 40]
    })


class TestStandardizeColumnNames:
    """Tests for standardize_column_names function."""
    
    def test_successful_rename(self, sample_raw_workforce):
        """Test successful column name standardization."""
        mapping = {'Year': 'year', 'Sector': 'sector', 'Count': 'count'}
        result = standardize_column_names(sample_raw_workforce, mapping)
        
        assert result.columns == ['year', 'sector', 'count']
        assert result.shape[0] == sample_raw_workforce.shape[0]
    
    def test_missing_column_raises_error(self):
        """Test error when mapping includes non-existent column."""
        df = pl.DataFrame({'year': [2018, 2019], 'count': [100, 150]})
        mapping = {'Year': 'yr', 'NonExistent': 'ne'}
        
        with pytest.raises(ValueError, match="Columns not found"):
            standardize_column_names(df, mapping)
    
    def test_empty_mapping(self, sample_raw_workforce):
        """Test with empty mapping returns unchanged DataFrame."""
        result = standardize_column_names(sample_raw_workforce, {})
        assert result.columns == sample_raw_workforce.columns


class TestUnifyWorkforceTables:
    """Tests for unify_workforce_tables function."""
    
    def test_correct_row_count(self, sample_doctors_df, sample_nurses_df, sample_pharmacists_df):
        """Test unified table has correct total row count."""
        result = unify_workforce_tables(sample_doctors_df, sample_nurses_df, sample_pharmacists_df)
        
        expected_rows = len(sample_doctors_df) + len(sample_nurses_df) + len(sample_pharmacists_df)
        assert len(result) == expected_rows
    
    def test_profession_column_added(self, sample_doctors_df, sample_nurses_df, sample_pharmacists_df):
        """Test profession column is added with correct values."""
        result = unify_workforce_tables(sample_doctors_df, sample_nurses_df, sample_pharmacists_df)
        
        assert 'profession' in result.columns
        assert set(result['profession'].unique().to_list()) == {'Doctor', 'Nurse', 'Pharmacist'}
    
    def test_source_table_column_added(self, sample_doctors_df, sample_nurses_df, sample_pharmacists_df):
        """Test source_table column is added."""
        result = unify_workforce_tables(sample_doctors_df, sample_nurses_df, sample_pharmacists_df)
        
        assert 'source_table' in result.columns
        sources = set(result['source_table'].unique().to_list())
        assert sources == {'workforce_doctors', 'workforce_nurses', 'workforce_pharmacists'}
    
    def test_profession_specific_columns_nullable(self, sample_doctors_df, sample_nurses_df, sample_pharmacists_df):
        """Test profession-specific columns are nullable for other professions."""
        result = unify_workforce_tables(sample_doctors_df, sample_nurses_df, sample_pharmacists_df)
        
        # Nurses and pharmacists should have null specialist_category
        nurse_rows = result.filter(pl.col('profession') == 'Nurse')
        assert nurse_rows['specialist_category'].null_count() == len(nurse_rows)
        
        # Doctors and pharmacists should have null nurse_type
        doctor_rows = result.filter(pl.col('profession') == 'Doctor')
        assert doctor_rows['nurse_type'].null_count() == len(doctor_rows)


class TestConvertDataTypes:
    """Tests for convert_data_types function."""
    
    def test_successful_type_conversion(self):
        """Test data type conversion."""
        df = pl.DataFrame({
            'year': [2018, 2019],
            'count': [100, 150],
            'sector': ['Public', 'Private']
        })
        
        type_map = {
            'year': pl.Int32,
            'count': pl.Int32,
            'sector': pl.Categorical
        }
        
        result = convert_data_types(df, type_map)
        
        assert result['year'].dtype == pl.Int32
        assert result['count'].dtype == pl.Int32
        assert result['sector'].dtype == pl.Categorical
        assert result.shape[0] == 2
    
    def test_missing_column_raises_error(self):
        """Test error when column for conversion doesn't exist."""
        df = pl.DataFrame({'year': [2018, 2019]})
        type_map = {'year': pl.Int32, 'nonexistent': pl.String}
        
        with pytest.raises(ValueError, match="Columns not found"):
            convert_data_types(df, type_map)
    
    def test_int64_to_int32_conversion(self):
        """Test Int64 to Int32 conversion (memory optimization)."""
        df = pl.DataFrame({
            'count': pl.Series([100, 200, 300], dtype=pl.Int64)
        })
        
        result = convert_data_types(df, {'count': pl.Int32})
        assert result['count'].dtype == pl.Int32


class TestStandardizeSectorNames:
    """Tests for standardize_sector_names function."""
    
    def test_sector_standardization(self):
        """Test sector name standardization."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'sector': ['Public Sector', 'Private Sector', 'Not in Active Practice']
        })
        
        mapping = {
            'Public Sector': 'Public',
            'Private Sector': 'Private',
            'Not in Active Practice': 'Inactive'
        }
        
        result = standardize_sector_names(df, 'sector', mapping)
        
        assert result['sector'].dtype == pl.Categorical
        assert set(result['sector'].to_list()) == {'Public', 'Private', 'Inactive'}
    
    def test_missing_sector_column_raises_error(self):
        """Test error when sector column doesn't exist."""
        df = pl.DataFrame({'year': [2018, 2019]})
        
        with pytest.raises(ValueError, match="Sector column .* not found"):
            standardize_sector_names(df, 'sector', {})
    
    def test_unmapped_values_unchanged(self):
        """Test values not in mapping remain unchanged."""
        df = pl.DataFrame({
            'sector': ['Public', 'Private', 'Unknown']
        })
        
        mapping = {'Public': 'Public', 'Private': 'Private'}
        result = standardize_sector_names(df, 'sector', mapping)
        
        assert 'Unknown' in result['sector'].to_list()


class TestHandleMissingValues:
    """Tests for missing value handling."""
    
    def test_flag_strategy(self):
        """Test missing value handling with flag strategy."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'count': [100, None, 200]
        })
        
        result = handle_missing_values(df, strategy='flag')
        
        assert 'has_missing_values' in result.columns
        assert result.filter(pl.col('has_missing_values'))['has_missing_values'].count() == 1
        assert result.shape[0] == 3  # No rows dropped
    
    def test_drop_rows_strategy(self):
        """Test missing value handling with drop_rows strategy."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'count': [100, None, 200]
        })
        
        result = handle_missing_values(df, strategy='drop_rows')
        
        assert result.shape[0] == 2  # One row dropped
        assert result.null_count().sum_horizontal()[0] == 0  # No nulls remaining
    
    def test_drop_cols_strategy(self):
        """Test missing value handling with drop_cols strategy."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'count': [100, 200, 300],
            'bad_col': [None, None, None]
        })
        
        result = handle_missing_values(df, strategy='drop_cols', drop_threshold=50.0)
        
        assert 'bad_col' not in result.columns
        assert 'count' in result.columns
    
    def test_invalid_strategy_raises_error(self):
        """Test error with invalid strategy."""
        df = pl.DataFrame({'year': [2018, 2019]})
        
        with pytest.raises(ValueError, match="Invalid strategy"):
            handle_missing_values(df, strategy='invalid')


class TestDetectDuplicates:
    """Tests for duplicate detection."""
    
    def test_exact_duplicates(self, sample_workforce_with_duplicates):
        """Test duplicate detection with exact duplicates."""
        dup_count, result = detect_duplicates(
            sample_workforce_with_duplicates,
            subset=['year', 'sector', 'count']
        )
        
        assert dup_count == 1  # One duplicate pair
        assert result.shape[0] == 3  # One duplicate removed
    
    def test_no_duplicates(self):
        """Test duplicate detection when no duplicates exist."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'sector': ['Public', 'Private', 'Public'],
            'count': [100, 150, 200]
        })
        
        dup_count, result = detect_duplicates(df, subset=['year', 'sector'])
        
        assert dup_count == 0
        assert result.shape[0] == df.shape[0]
    
    def test_keep_first(self, sample_workforce_with_duplicates):
        """Test keeping first occurrence of duplicates."""
        dup_count, result = detect_duplicates(
            sample_workforce_with_duplicates,
            subset=['year', 'sector', 'count'],
            keep='first'
        )
        
        # First occurrence should be kept
        assert result.filter((pl.col('year') == 2018) & (pl.col('sector') == 'Public')).shape[0] == 1


class TestDetectAndFlagOutliers:
    """Tests for outlier detection."""
    
    def test_zscore_outlier_detection(self):
        """Test outlier flagging using z-score method."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020, 2021, 2022],
            'count': [100, 110, 105, 500, 115]  # 500 is a clear outlier
        })
        
        result = detect_and_flag_outliers(df, ['count'], threshold=2.0, method='zscore')
        
        assert 'count_outlier' in result.columns
        assert 'outlier_flag' in result.columns
        # The value 500 should be flagged
        outlier_rows = result.filter(pl.col('count_outlier'))
        assert outlier_rows['count'][0] == 500
    
    def test_iqr_outlier_detection(self):
        """Test outlier flagging using IQR method."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020, 2021, 2022],
            'count': [100, 110, 105, 115, 500]  # 500 is a clear outlier
        })
        
        result = detect_and_flag_outliers(df, ['count'], threshold=1.5, method='iqr')
        
        assert result.filter(pl.col('outlier_flag')).shape[0] >= 1
    
    def test_no_outliers(self):
        """Test when no outliers exist."""
        df = pl.DataFrame({
            'count': [100, 105, 110, 115, 120]  # No major outliers
        })
        
        result = detect_and_flag_outliers(df, ['count'], threshold=3.0, method='zscore')
        
        # All values should be false or very few flagged
        assert result['outlier_flag'].sum() == 0
    
    def test_invalid_method_raises_error(self):
        """Test error with invalid detection method."""
        df = pl.DataFrame({'count': [100, 200, 300]})
        
        with pytest.raises(ValueError, match="Invalid method"):
            detect_and_flag_outliers(df, ['count'], method='invalid')
    
    def test_zero_std_dev_handling(self):
        """Test handling of zero standard deviation."""
        df = pl.DataFrame({
            'count': [100, 100, 100, 100]  # All same values
        })
        
        result = detect_and_flag_outliers(df, ['count'], threshold=3.0, method='zscore')
        
        # Should not flag any as outliers when std=0
        assert result['outlier_flag'].sum() == 0


class TestAnalyzeMissingValues:
    """Tests for missing value analysis."""
    
    def test_analysis_structure(self):
        """Test missing value analysis returns correct structure."""
        df = pl.DataFrame({
            'year': [2018, 2019, 2020],
            'count': [100, None, 200]
        })
        
        analysis = analyze_missing_values(df)
        
        assert 'year' in analysis
        assert 'count' in analysis
        assert 'null_count' in analysis['year']
        assert 'null_percentage' in analysis['year']
    
    def test_missing_percentages(self):
        """Test missing value percentages calculated correctly."""
        df = pl.DataFrame({
            'col1': [1, 2, None, None],  # 50% missing
            'col2': [1, 2, 3, 4]  # 0% missing
        })
        
        analysis = analyze_missing_values(df)
        
        assert analysis['col1']['null_percentage'] == 50.0
        assert analysis['col2']['null_percentage'] == 0.0
