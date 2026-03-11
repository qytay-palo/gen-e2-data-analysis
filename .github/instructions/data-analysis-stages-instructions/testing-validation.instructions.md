---
name: 'Testing and Code Validation Standards'
description: 'Best practices for unit testing, integration testing, and code quality assurance'
applyTo: 'tests/**, **/*.py, src/**'
---

## Purpose
This document defines **mandatory standards** for testing and code validation. Apply these practices to ensure code reliability, maintainability, and correctness.

## Core Principles

### 1. Test-Driven Mindset
- **ALWAYS write tests** for critical business logic
- Test edge cases and error conditions
- Maintain test coverage above 80% for core modules
- Run tests before committing code

### 2. Comprehensive Test Coverage
- **Unit tests**: Test individual functions in isolation
- **Integration tests**: Test end-to-end workflows
- **Data validation tests**: Test schema compliance and quality
- **Regression tests**: Prevent previously fixed bugs from recurring

### 3. Reproducible Testing
- Use fixtures for consistent test data
- Set random seeds for deterministic tests
- Isolate tests (no dependencies between test cases)
- Clean up test artifacts after execution

## Testing Framework Setup

### Project Structure

```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_validators.py
│   ├── test_feature_engineering.py
│   └── test_models.py
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_etl_pipeline.py
│   ├── test_model_training.py
│   └── test_forecast_generation.py
└── data/                       # Test data validation
    ├── __init__.py
    ├── test_schema_validation.py
    └── fixtures/               # Sample data files
        ├── sample_disease_data.csv
        └── sample_config.yml
```

### Pytest Configuration

```python
# conftest.py (in project root)
import pytest
import polars as pl
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Set random seeds for reproducibility
np.random.seed(42)

@pytest.fixture(scope="session")
def sample_disease_data():
    """Generate sample disease surveillance data for testing."""
    dates = [datetime(2020, 1, 1) + timedelta(weeks=i) for i in range(52)]
    diseases = ['Dengue Fever', 'HFMD', 'Influenza']
    
    data = []
    for disease in diseases:
        for i, date in enumerate(dates):
            # Generate synthetic case counts with seasonality
            base_cases = np.random.poisson(50)
            seasonal = 20 * np.sin(2 * np.pi * i / 52)
            case_count = int(max(0, base_cases + seasonal))
            
            data.append({
                'disease': disease,
                'reporting_date': date,
                'epi_week': i + 1,
                'year': date.year,
                'case_count': case_count
            })
    
    return pl.DataFrame(data)


@pytest.fixture(scope="session")
def sample_features_data():
    """Generate sample data with engineered features."""
    df = pl.DataFrame({
        'date': [datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)],
        'case_count': np.random.poisson(20, 100),
        'disease': ['Dengue'] * 100
    })
    
    # Add some features
    df = df.with_columns([
        pl.col('case_count').shift(1).alias('lag_1'),
        pl.col('case_count').shift(7).alias('lag_7'),
        pl.col('case_count').rolling_mean(window_size=7).alias('ma_7')
    ])
    
    return df


@pytest.fixture(scope="function")
def temp_output_dir(tmp_path):
    """Create temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir()
    return output_dir


@pytest.fixture(scope="function")
def mock_config():
    """Provide mock configuration for testing."""
    return {
        'data': {
            'target_diseases': ['Dengue Fever', 'HFMD'],
            'date_range': {
                'start': '2020-01-01',
                'end': '2020-12-31'
            }
        },
        'model': {
            'type': 'random_forest',
            'n_estimators': 10,  # Small for fast tests
            'random_state': 42
        },
        'validation': {
            'test_size': 0.2,
            'cv_folds': 3
        }
    }
```

## Unit Test Examples

### Testing Data Loading

```python
# tests/unit/test_disease_data_loader.py
import pytest
import polars as pl
from src.data_processing.disease_data_loader import DiseaseDataLoader
from src.data_processing.schemas import DISEASE_SURVEILLANCE_SCHEMA

class TestDiseaseDataLoader:
    """Test suite for DiseaseDataLoader class."""
    
    def test_load_csv_success(self, sample_disease_data, temp_output_dir):
        """Test successful CSV loading."""
        # Setup: Save sample data to CSV
        csv_path = temp_output_dir / "test_data.csv"
        sample_disease_data.write_csv(csv_path)
        
        # Execute: Load the data
        loader = DiseaseDataLoader()
        df = loader.load_from_csv(str(csv_path))
        
        # Assert: Verify loaded data
        assert isinstance(df, pl.DataFrame)
        assert len(df) > 0
        assert 'disease' in df.columns
        assert 'case_count' in df.columns
    
    def test_load_csv_file_not_found(self):
        """Test loading non-existent file raises error."""
        loader = DiseaseDataLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_from_csv('nonexistent_file.csv')
    
    def test_load_with_schema_validation(self, sample_disease_data, temp_output_dir):
        """Test loading with schema validation."""
        csv_path = temp_output_dir / "test_data.csv"
        sample_disease_data.write_csv(csv_path)
        
        loader = DiseaseDataLoader()
        df = loader.load_from_csv(
            str(csv_path),
            validate_schema=True,
            schema=DISEASE_SURVEILLANCE_SCHEMA
        )
        
        assert len(df) > 0
    
    def test_handle_missing_columns(self, temp_output_dir):
        """Test handling of data with missing required columns."""
        # Create data missing required column
        incomplete_data = pl.DataFrame({
            'disease': ['Dengue'],
            'date': ['2020-01-01']
            # Missing 'case_count'
        })
        
        csv_path = temp_output_dir / "incomplete.csv"
        incomplete_data.write_csv(csv_path)
        
        loader = DiseaseDataLoader()
        
        with pytest.raises(ValueError, match="Missing required columns"):
            loader.load_from_csv(
                str(csv_path),
                validate_schema=True,
                schema=DISEASE_SURVEILLANCE_SCHEMA
            )


### Testing Feature Engineering

```python
# tests/unit/test_feature_engineering.py
import pytest
import polars as pl
import numpy as np
from src.features.temporal_features import create_lag_features, create_rolling_features

class TestFeatureEngineering:
    """Test suite for feature engineering functions."""
    
    def test_create_lag_features(self, sample_features_data):
        """Test lag feature creation."""
        df = create_lag_features(
            sample_features_data,
            target_column='case_count',
            group_by_columns=['disease'],
            lags=[1, 7]
        )
        
        # Check that lag columns were created
        assert 'case_count_lag_1' in df.columns
        assert 'case_count_lag_7' in df.columns
        
        # Verify lag values are correct
        # First row should have null lag (no previous data)
        assert df['case_count_lag_1'][0] is None
        
        # Second row lag_1 should equal first row value
        assert df['case_count_lag_1'][1] == df['case_count'][0]
    
    def test_create_rolling_features(self, sample_features_data):
        """Test rolling window feature creation."""
        df = create_rolling_features(
            sample_features_data,
            target_column='case_count',
            group_by_columns=['disease'],
            windows=[7],
            aggregations=['mean', 'std']
        )
        
        # Check that rolling features were created
        assert 'case_count_rolling_7w_mean' in df.columns
        assert 'case_count_rolling_7w_std' in df.columns
        
        # Verify rolling mean calculation
        window_data = df['case_count'][:7].to_numpy()
        expected_mean = np.mean(window_data)
        actual_mean = df['case_count_rolling_7w_mean'][6]
        
        assert np.isclose(actual_mean, expected_mean, rtol=1e-5)
    
    def test_lag_features_by_group(self):
        """Test that lag features respect grouping."""
        # Create data with multiple diseases
        df = pl.DataFrame({
            'disease': ['A', 'A', 'B', 'B'],
            'date': [1, 2, 1, 2],
            'value': [10, 20, 30, 40]
        })
        
        df = create_lag_features(
            df,
            target_column='value',
            group_by_columns=['disease'],
            lags=[1]
        )
        
        # Disease A lag should use Disease A values
        assert df.filter(pl.col('disease') == 'A')['value_lag_1'][1] == 10
        
        # Disease B lag should use Disease B values
        assert df.filter(pl.col('disease') == 'B')['value_lag_1'][1] == 30
    
    def test_feature_scaling(self, sample_features_data):
        """Test feature scaling transformation."""
        from src.features.feature_transformations import FeatureScaler
        
        scaler = FeatureScaler(method='standard')
        
        # Fit on data
        scaler.fit(sample_features_data, columns=['case_count'])
        
        # Transform
        df_scaled = scaler.transform(sample_features_data)
        
        # Check scaled column exists
        assert 'case_count_scaled' in df_scaled.columns
        
        # Verify mean ≈ 0 and std ≈ 1
        scaled_values = df_scaled['case_count_scaled'].drop_nulls()
        assert abs(scaled_values.mean()) < 0.1
        assert abs(scaled_values.std() - 1.0) < 0.1


### Testing Models

```python
# tests/unit/test_models.py
import pytest
import numpy as np
from sklearn.metrics import mean_absolute_error
from src.models.ml_models import MLForecaster

class TestMLForecaster:
    """Test suite for ML forecasting models."""
    
    def test_model_initialization(self):
        """Test model can be initialized with different types."""
        for model_type in ['random_forest', 'gradient_boosting', 'ridge']:
            model = MLForecaster(model_type=model_type, random_state=42)
            assert model.model is not None
            assert model.model_type == model_type
    
    def test_model_fit_predict(self):
        """Test model fitting and prediction."""
        # Generate simple synthetic data
        np.random.seed(42)
        X_train = np.random.randn(100, 5)
        y_train = X_train[:, 0] * 2 + X_train[:, 1] + np.random.randn(100) * 0.1
        
        # Fit model
        model = MLForecaster(model_type='random_forest', n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Generate predictions
        X_test = np.random.randn(20, 5)
        y_pred = model.predict(X_test)
        
        # Verify predictions
        assert y_pred.shape == (20,)
        assert not np.any(np.isnan(y_pred))
    
    def test_model_save_load(self, temp_output_dir):
        """Test model serialization and loading."""
        # Train a model
        X = np.random.randn(50, 3)
        y = X[:, 0] + X[:, 1]
        
        model = MLForecaster(model_type='ridge', random_state=42)
        model.fit(X, y)
        
        # Save model
        model_path = temp_output_dir / "test_model.pkl"
        model.save(str(model_path))
        
        # Load model
        loaded_model = MLForecaster.load(str(model_path))
        
        # Verify loaded model makes same predictions
        X_test = np.random.randn(10, 3)
        pred_original = model.predict(X_test)
        pred_loaded = loaded_model.predict(X_test)
        
        np.testing.assert_array_almost_equal(pred_original, pred_loaded)
    
    def test_cross_validation(self):
        """Test cross-validation functionality."""
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = X[:, 0] * 2 + np.random.randn(100) * 0.5
        
        model = MLForecaster(model_type='random_forest', n_estimators=10, random_state=42)
        cv_results = model.cross_validate(X, y, n_splits=3)
        
        # Verify CV results structure
        assert 'mae' in cv_results
        assert 'rmse' in cv_results
        assert 'r2' in cv_results
        
        # Verify we have results for each fold
        assert len(cv_results['mae']) == 3
        assert len(cv_results['rmse']) == 3
        assert len(cv_results['r2']) == 3
        
        # Verify values are reasonable
        assert all(mae > 0 for mae in cv_results['mae'])
        assert all(rmse > 0 for rmse in cv_results['rmse'])


## Integration Test Examples

```python
# tests/integration/test_etl_pipeline.py
import pytest
import polars as pl
from pathlib import Path
from src.data_processing.disease_data_loader import DiseaseDataLoader
from src.data_processing.disease_data_validator import DiseaseDataValidator

class TestETLPipeline:
    """Integration tests for end-to-end ETL pipeline."""
    
    def test_full_etl_pipeline(self, sample_disease_data, temp_output_dir):
        """Test complete ETL workflow from load to validated output."""
        # Step 1: Save raw data
        raw_path = temp_output_dir / "raw_data.csv"
        sample_disease_data.write_csv(raw_path)
        
        # Step 2: Load data
        loader = DiseaseDataLoader()
        df = loader.load_from_csv(str(raw_path))
        
        assert len(df) > 0
        
        # Step 3: Validate data
        validator = DiseaseDataValidator(df)
        all_passed, results = validator.validate_all()
        
        # Should pass validation (sample data is clean)
        assert all_passed
        
        # Step 4: Save processed data
        processed_path = temp_output_dir / "processed_data.csv"
        df.write_csv(processed_path)
        
        # Verify processed file exists and is readable
        assert processed_path.exists()
        df_reloaded = pl.read_csv(processed_path)
        assert len(df_reloaded) == len(df)
    
    def test_pipeline_with_data_quality_issues(self, temp_output_dir):
        """Test pipeline handles data quality issues appropriately."""
        # Create problematic data
        bad_data = pl.DataFrame({
            'disease': ['Dengue', None, 'HFMD'],  # Contains null
            'reporting_date': ['2020-01-01', '2020-01-08', '2020-01-15'],
            'case_count': [100, -5, 200],  # Contains negative
            'epi_week': [1, 2, 3],
            'year': [2020, 2020, 2020]
        })
        
        bad_path = temp_output_dir / "bad_data.csv"
        bad_data.write_csv(bad_path)
        
        # Load and validate
        loader = DiseaseDataLoader()
        df = loader.load_from_csv(str(bad_path))
        
        validator = DiseaseDataValidator(df)
        all_passed, results = validator.validate_all()
        
        # Should fail validation
        assert not all_passed
        
        # Check specific failures
        failed_rules = [r['rule'] for r in results if not r['passed']]
        assert 'case_count_non_negative' in failed_rules


# tests/integration/test_model_training.py
class TestModelTrainingPipeline:
    """Integration tests for model training workflow."""
    
    def test_train_evaluate_save_workflow(self, sample_features_data, temp_output_dir):
        """Test complete model training, evaluation, and saving."""
        from src.models.ml_models import MLForecaster
        from src.models.evaluation import calculate_forecast_metrics
        
        # Prepare data
        df = sample_features_data.drop_nulls()
        
        # Split features and target
        feature_cols = ['lag_1', 'lag_7', 'ma_7']
        X = df.select(feature_cols).drop_nulls().to_numpy()
        y = df['case_count'].to_numpy()[-len(X):]
        
        # Train-test split (time-aware)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train model
        model = MLForecaster(
            model_type='random_forest',
            n_estimators=10,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        metrics = calculate_forecast_metrics(y_test, y_pred)
        
        # Verify metrics calculated
        assert 'MAE' in metrics
        assert metrics['MAE'] >= 0
        
        # Save model
        model_path = temp_output_dir / "trained_model.pkl"
        model.save(str(model_path))
        
        # Verify model file created
        assert model_path.exists()
        
        # Load and verify predictions match
        loaded_model = MLForecaster.load(str(model_path))
        y_pred_loaded = loaded_model.predict(X_test)
        
        np.testing.assert_array_almost_equal(y_pred, y_pred_loaded)
```

## Data Validation Tests

```python
# tests/data/test_schema_validation.py
import pytest
import polars as pl
from src.data_processing.schemas import DISEASE_SURVEILLANCE_SCHEMA, validate_schema

class TestSchemaValidation:
    """Test data schema validation."""
    
    def test_valid_schema(self, sample_disease_data):
        """Test schema validation passes for valid data."""
        is_valid, errors = validate_schema(
            sample_disease_data,
            DISEASE_SURVEILLANCE_SCHEMA
        )
        
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_columns(self):
        """Test schema validation catches missing columns."""
        df = pl.DataFrame({
            'disease': ['Dengue'],
            'case_count': [100]
            # Missing other required columns
        })
        
        is_valid, errors = validate_schema(df, DISEASE_SURVEILLANCE_SCHEMA)
        
        assert not is_valid
        assert any('Missing required columns' in err for err in errors)
    
    def test_wrong_data_types(self):
        """Test schema validation catches type mismatches."""
        df = pl.DataFrame({
            'disease': ['Dengue'],
            'epi_week': ['not_a_number'],  # Should be Int32
            'year': [2020],
            'case_count': [100],
            'reporting_date': ['2020-01-01']
        })
        
        # This might pass initial load but should fail strict validation
        # Implementation depends on your validator
        is_valid, errors = validate_schema(df, DISEASE_SURVEILLANCE_SCHEMA)
        
        # At minimum, should identify the type issue
        assert len(errors) > 0 or not is_valid
    
    def test_value_range_violations(self):
        """Test schema validation catches out-of-range values."""
        df = pl.DataFrame({
            'disease': ['Dengue'],
            'epi_week': [100],  # Should be 1-53
            'year': [2020],
            'case_count': [50],
            'reporting_date': [pl.date(2020, 1, 1)]
        })
        
        is_valid, errors = validate_schema(df, DISEASE_SURVEILLANCE_SCHEMA)
        
        assert not is_valid
        assert any('epi_week' in err for err in errors)
```

## Test Automation

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Run Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests with coverage
      run: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=html
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.9
  
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Best Practices Summary

### DO
- ✅ Write tests for all critical business logic
- ✅ Use fixtures for test data
- ✅ Test edge cases and error conditions
- ✅ Maintain >80% code coverage
- ✅ Run tests before committing
- ✅ Isolate tests (no dependencies between tests)
- ✅ Use descriptive test names
- ✅ Test both happy path and failure cases

### DON'T
- ❌ Skip tests for "simple" functions
- ❌ Write tests that depend on external resources without mocking
- ❌ Commit code without running tests
- ❌ Ignore failing tests
- ❌ Write tests that depend on execution order
- ❌ Use production data in tests
- ❌ Test implementation details instead of behavior

## Testing Checklist

- [ ] **Unit tests written**: Core functions have unit tests
- [ ] **Integration tests written**: End-to-end workflows tested
- [ ] **Edge cases covered**: Boundary conditions tested
- [ ] **Error handling tested**: Exception paths validated
- [ ] **Test coverage measured**: Coverage >80% for core modules
- [ ] **Tests pass locally**: All tests run successfully
- [ ] **CI/CD configured**: Automated testing on commits
- [ ] **Fixtures used**: Test data managed with fixtures
- [ ] **Tests documented**: Test purposes clearly stated
- [ ] **Mocking applied**: External dependencies mocked appropriately

## Summary

Effective testing requires:
1. **Comprehensive coverage** - unit, integration, and data validation tests
2. **Reproducibility** - consistent test data and deterministic results
3. **Isolation** - independent tests that don't affect each other
4. **Automation** - CI/CD integration for continuous validation
5. **Documentation** - clear test names and purposes
