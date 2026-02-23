---
name: 'Modeling and Forecasting Standards'
description: 'Best practices for building, training, evaluating, and deploying predictive models'
applyTo: 'src/models/**, notebooks/2_analysis/*model*.ipynb, notebooks/2_analysis/*forecast*.ipynb, models/**, results/metrics/**, docs/objectives/user_stories/**/*forecast*.md, docs/objectives/user_stories/**/*forecast*.md, docs/objectives/user_stories/**/*generate*.md'
---

## Purpose
This document defines **mandatory standards** for building predictive models and forecasting systems. Apply these practices to ensure reproducible, well-evaluated, and production-ready models.

## Core Principles

### 1. Reproducibility
- **ALWAYS set random seeds** for reproducible results
- Version control model code and hyperparameters
- Document model training environment and dependencies
- Save trained models with metadata (version, training date, performance)

### 2. Proper Validation
- **NEVER evaluate on training data**
- Use time-aware splits for time series data
- Implement cross-validation appropriate to the problem
- Report multiple evaluation metrics, not just one

### 3. Baseline Comparison
- **ALWAYS establish simple baselines** before complex models
- Compare new models against baseline and previous best
- Document why complex models justify their added complexity
- Choose simplest model that meets performance requirements

## Model Development Workflow

### Step 1: Establish Baselines

```python
# src/models/baselines.py
import polars as pl
import numpy as np
from typing import Dict, List, Tuple
from loguru import logger
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class NaiveForecaster:
    """Naive forecasting baselines for time series."""
    
    @staticmethod
    def naive_forecast(
        df: pl.DataFrame,
        target_column: str = 'case_count',
        group_by: List[str] = ['disease'],
        method: str = 'last_value'
    ) -> pl.DataFrame:
        """Generate naive forecast.
        
        Methods:
        - 'last_value': Forecast = last observed value
        - 'seasonal_naive': Forecast = value from same period last year
        - 'mean': Forecast = historical mean
        
        Args:
            df: Input DataFrame sorted by time
            target_column: Column to forecast
            group_by: Grouping columns
            method: Naive forecasting method
            
        Returns:
            DataFrame with forecast column added
        """
        logger.info(f"Generating {method} naive forecast")
        
        if method == 'last_value':
            # Simply repeat last observed value
            df = df.with_columns(
                pl.col(target_column).last().over(group_by).alias('forecast_naive')
            )
            
        elif method == 'seasonal_naive':
            # Use value from same week last year (lag 52 weeks)
            df = df.with_columns(
                pl.col(target_column).shift(52).over(group_by).alias('forecast_naive')
            )
            
        elif method == 'mean':
            # Historical mean
            df = df.with_columns(
                pl.col(target_column).mean().over(group_by).alias('forecast_naive')
            )
        
        return df


def evaluate_baseline_models(
    train_df: pl.DataFrame,
    test_df: pl.DataFrame,
    target_column: str = 'case_count',
    group_by: List[str] = ['disease']
) -> Dict[str, Dict[str, float]]:
    """Evaluate multiple baseline models.
    
    Args:
        train_df: Training data
        test_df: Test data with actuals
        target_column: Target variable name
        group_by: Grouping columns
        
    Returns:
        Dictionary of baseline performance metrics
    """
    logger.info("Evaluating baseline models")
    
    baseline_methods = ['last_value', 'seasonal_naive', 'mean']
    results = {}
    
    for method in baseline_methods:
        # Generate forecast
        forecast_df = NaiveForecaster.naive_forecast(
            test_df,
            target_column=target_column,
            group_by=group_by,
            method=method
        )
        
        # Calculate metrics
        y_true = forecast_df[target_column].to_numpy()
        y_pred = forecast_df['forecast_naive'].to_numpy()
        
        # Remove nulls (e.g., seasonal_naive has nulls for first year)
        mask = ~np.isnan(y_pred)
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1))) * 100
        r2 = r2_score(y_true, y_pred)
        
        results[method] = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }
        
        logger.info(f"{method}: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%, R2={r2:.3f}")
    
    return results
```

### Step 2: Time Series Modeling

```python
# src/models/time_series_models.py
import polars as pl
import numpy as np
from typing import Dict, List, Optional, Tuple
from loguru import logger
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle
from pathlib import Path
from datetime import datetime

class SARIMAXForecaster:
    """SARIMAX model for seasonal time series forecasting."""
    
    def __init__(
        self,
        order: Tuple[int, int, int] = (1, 1, 1),
        seasonal_order: Tuple[int, int, int, int] = (1, 1, 1, 52),
        trend: str = 'c'
    ):
        """Initialize SARIMAX forecaster.
        
        Args:
            order: (p, d, q) order for non-seasonal component
            seasonal_order: (P, D, Q, s) order for seasonal component
            trend: Trend component ('n', 'c', 't', 'ct')
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.model = None
        self.model_fit = None
        
    def fit(
        self,
        y: np.ndarray,
        exog: Optional[np.ndarray] = None
    ) -> 'SARIMAXForecaster':
        """Fit SARIMAX model.
        
        Args:
            y: Time series data (1D array)
            exog: Exogenous variables (optional)
            
        Returns:
            Fitted forecaster
        """
        logger.info(f"Fitting SARIMAX{self.order}x{self.seasonal_order}")
        
        self.model = SARIMAX(
            y,
            exog=exog,
            order=self.order,
            seasonal_order=self.seasonal_order,
            trend=self.trend,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        
        self.model_fit = self.model.fit(disp=False)
        
        logger.info("SARIMAX model fitted successfully")
        logger.info(f"AIC: {self.model_fit.aic:.2f}, BIC: {self.model_fit.bic:.2f}")
        
        return self
    
    def forecast(
        self,
        steps: int,
        exog: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate forecast with confidence intervals.
        
        Args:
            steps: Number of steps to forecast
            exog: Exogenous variables for forecast period
            
        Returns:
            Tuple of (forecast, lower_bound, upper_bound)
        """
        if self.model_fit is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        logger.info(f"Generating {steps}-step forecast")
        
        forecast_result = self.model_fit.get_forecast(steps=steps, exog=exog)
        
        forecast = forecast_result.predicted_mean.values
        conf_int = forecast_result.conf_int()
        lower_bound = conf_int.iloc[:, 0].values
        upper_bound = conf_int.iloc[:, 1].values
        
        return forecast, lower_bound, upper_bound
    
    def save(self, filepath: str) -> None:
        """Save fitted model to file.
        
        Args:
            filepath: Path to save model
        """
        if self.model_fit is None:
            raise ValueError("No fitted model to save")
        
        model_data = {
            'model_fit': self.model_fit,
            'order': self.order,
            'seasonal_order': self.seasonal_order,
            'trend': self.trend,
            'aic': self.model_fit.aic,
            'bic': self.model_fit.bic,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'SARIMAXForecaster':
        """Load fitted model from file.
        
        Args:
            filepath: Path to saved model
            
        Returns:
            Loaded forecaster
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        forecaster = cls(
            order=model_data['order'],
            seasonal_order=model_data['seasonal_order'],
            trend=model_data['trend']
        )
        forecaster.model_fit = model_data['model_fit']
        
        logger.info(f"Model loaded from {filepath}")
        return forecaster


class ExponentialSmoothingForecaster:
    """Exponential smoothing with seasonal components."""
    
    def __init__(
        self,
        seasonal: str = 'add',
        seasonal_periods: int = 52,
        trend: str = 'add'
    ):
        """Initialize exponential smoothing forecaster.
        
        Args:
            seasonal: 'add' or 'mul' for seasonal component
            seasonal_periods: Number of periods in season (52 for weekly data)
            trend: 'add', 'mul', or None for trend component
        """
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.trend = trend
        self.model_fit = None
        
    def fit(self, y: np.ndarray) -> 'ExponentialSmoothingForecaster':
        """Fit exponential smoothing model.
        
        Args:
            y: Time series data
            
        Returns:
            Fitted forecaster
        """
        logger.info(f"Fitting Exponential Smoothing (trend={self.trend}, seasonal={self.seasonal})")
        
        model = ExponentialSmoothing(
            y,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods,
            trend=self.trend
        )
        
        self.model_fit = model.fit()
        
        logger.info("Exponential Smoothing model fitted successfully")
        return self
    
    def forecast(self, steps: int) -> np.ndarray:
        """Generate forecast.
        
        Args:
            steps: Number of steps to forecast
            
        Returns:
            Forecast array
        """
        if self.model_fit is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        logger.info(f"Generating {steps}-step forecast")
        forecast = self.model_fit.forecast(steps)
        
        return forecast
```

### Step 3: Machine Learning Models

```python
# src/models/ml_models.py
import polars as pl
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
from datetime import datetime

class MLForecaster:
    """Machine learning models for forecasting with engineered features."""
    
    def __init__(
        self,
        model_type: str = 'random_forest',
        **model_params
    ):
        """Initialize ML forecaster.
        
        Args:
            model_type: 'random_forest', 'gradient_boosting', 'ridge', 'lasso'
            **model_params: Parameters to pass to model constructor
        """
        self.model_type = model_type
        self.model_params = model_params
        self.model = None
        self.feature_importance: Optional[Dict[str, float]] = None
        
        # Initialize model
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(**model_params)
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(**model_params)
        elif model_type == 'ridge':
            self.model = Ridge(**model_params)
        elif model_type == 'lasso':
            self.model = Lasso(**model_params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[List[str]] = None
    ) -> 'MLForecaster':
        """Fit model to training data.
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target variable (n_samples,)
            feature_names: Names of features (for importance ranking)
            
        Returns:
            Fitted forecaster
        """
        logger.info(f"Fitting {self.model_type} on {X.shape[0]} samples, {X.shape[1]} features")
        
        self.model.fit(X, y)
        
        # Extract feature importance if available
        if hasattr(self.model, 'feature_importances_') and feature_names:
            importances = self.model.feature_importances_
            self.feature_importance = {
                name: importance 
                for name, importance in zip(feature_names, importances)
            }
            
            # Log top features
            sorted_features = sorted(
                self.feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )
            logger.info("Top 10 features by importance:")
            for name, importance in sorted_features[:10]:
                logger.info(f"  {name}: {importance:.4f}")
        
        logger.info(f"{self.model_type} fitted successfully")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions.
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        predictions = self.model.predict(X)
        return predictions
    
    def cross_validate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_splits: int = 5
    ) -> Dict[str, List[float]]:
        """Perform time series cross-validation.
        
        Args:
            X: Feature matrix
            y: Target variable
            n_splits: Number of CV splits
            
        Returns:
            Dictionary of metrics for each fold
        """
        logger.info(f"Performing {n_splits}-fold time series cross-validation")
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        
        cv_results = {
            'mae': [],
            'rmse': [],
            'r2': []
        }
        
        for fold, (train_idx, val_idx) in enumerate(tscv.split(X), 1):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            # Fit and predict
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_val)
            
            # Calculate metrics
            mae = mean_absolute_error(y_val, y_pred)
            rmse = np.sqrt(mean_squared_error(y_val, y_pred))
            r2 = r2_score(y_val, y_pred)
            
            cv_results['mae'].append(mae)
            cv_results['rmse'].append(rmse)
            cv_results['r2'].append(r2)
            
            logger.info(f"Fold {fold}: MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.3f}")
        
        # Summary statistics
        logger.info(f"CV Mean MAE: {np.mean(cv_results['mae']):.2f} ± {np.std(cv_results['mae']):.2f}")
        logger.info(f"CV Mean RMSE: {np.mean(cv_results['rmse']):.2f} ± {np.std(cv_results['rmse']):.2f}")
        logger.info(f"CV Mean R2: {np.mean(cv_results['r2']):.3f} ± {np.std(cv_results['r2']):.3f}")
        
        return cv_results
    
    def save(self, filepath: str) -> None:
        """Save fitted model.
        
        Args:
            filepath: Path to save model
        """
        if self.model is None:
            raise ValueError("No fitted model to save")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'model_params': self.model_params,
            'feature_importance': self.feature_importance,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'MLForecaster':
        """Load fitted model.
        
        Args:
            filepath: Path to saved model
            
        Returns:
            Loaded forecaster
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        forecaster = cls(
            model_type=model_data['model_type'],
            **model_data['model_params']
        )
        forecaster.model = model_data['model']
        forecaster.feature_importance = model_data['feature_importance']
        
        logger.info(f"Model loaded from {filepath}")
        return forecaster
```

### Step 4: Model Evaluation

```python
# src/models/evaluation.py
import polars as pl
import numpy as np
from typing import Dict, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from pathlib import Path

def calculate_forecast_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metrics: Optional[List[str]] = None
) -> Dict[str, float]:
    """Calculate comprehensive forecast metrics.
    
    Args:
        y_true: Actual values
        y_pred: Predicted values
        metrics: List of metrics to calculate (None = all)
        
    Returns:
        Dictionary of metric values
    """
    if metrics is None:
        metrics = ['mae', 'rmse', 'mape', 'mase', 'r2', 'bias']
    
    results = {}
    
    if 'mae' in metrics:
        results['MAE'] = mean_absolute_error(y_true, y_pred)
    
    if 'rmse' in metrics:
        results['RMSE'] = np.sqrt(mean_squared_error(y_true, y_pred))
    
    if 'mape' in metrics:
        # Mean Absolute Percentage Error
        results['MAPE'] = np.mean(np.abs((y_true - y_pred) / (y_true + 1))) * 100
    
    if 'mase' in metrics:
        # Mean Absolute Scaled Error (scaled by naive forecast)
        naive_error = np.mean(np.abs(np.diff(y_true)))
        results['MASE'] = mean_absolute_error(y_true, y_pred) / (naive_error + 1e-10)
    
    if 'r2' in metrics:
        results['R2'] = r2_score(y_true, y_pred)
    
    if 'bias' in metrics:
        # Mean bias (positive = overforecast, negative = underforecast)
        results['Bias'] = np.mean(y_pred - y_true)
    
    return results


def plot_forecast_results(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    dates: Optional[np.ndarray] = None,
    confidence_intervals: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    title: str = 'Forecast vs Actual',
    save_path: Optional[str] = None
) -> None:
    """Plot forecast results with actuals.
    
    Args:
        y_true: Actual values
        y_pred: Predicted values
        dates: Date indices (optional)
        confidence_intervals: Tuple of (lower_bound, upper_bound) arrays
        title: Plot title
        save_path: Path to save figure (optional)
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    x = dates if dates is not None else np.arange(len(y_true))
    
    # Plot 1: Forecast vs Actual
    axes[0].plot(x, y_true, label='Actual', linewidth=2, color='black', alpha=0.7)
    axes[0].plot(x, y_pred, label='Forecast', linewidth=2, color='steelblue', alpha=0.7)
    
    if confidence_intervals:
        lower, upper = confidence_intervals
        axes[0].fill_between(x, lower, upper, alpha=0.2, color='steelblue', label='95% CI')
    
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')
    axes[0].set_title(title)
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Plot 2: Residuals
    residuals = y_true - y_pred
    axes[1].scatter(x, residuals, alpha=0.5, color='coral')
    axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Residuals')
    axes[1].set_title('Forecast Residuals')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Forecast plot saved to {save_path}")
    
    plt.show()


def generate_model_report(
    model_name: str,
    metrics: Dict[str, float],
    training_time: float,
    model_params: Dict[str, Any],
    output_path: str = 'results/metrics/model_report.md'
) -> None:
    """Generate markdown model evaluation report.
    
    Args:
        model_name: Name of the model
        metrics: Dictionary of evaluation metrics
        training_time: Training time in seconds
        model_params: Model hyperparameters
        output_path: Path to save report
    """
    from datetime import datetime
    
    report = [
        f"# Model Evaluation Report: {model_name}",
        f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## Model Configuration",
        f"\n```yaml"
    ]
    
    for param, value in model_params.items():
        report.append(f"{param}: {value}")
    
    report.extend([
        "```",
        f"\n## Performance Metrics",
        f"\n| Metric | Value |",
        "|--------|-------|"
    ])
    
    for metric, value in metrics.items():
        if isinstance(value, float):
            report.append(f"| {metric} | {value:.4f} |")
        else:
            report.append(f"| {metric} | {value} |")
    
    report.extend([
        f"\n## Training Information",
        f"\n- **Training Time**: {training_time:.2f} seconds",
        f"- **Training Date**: {datetime.now().strftime('%Y-%m-%d')}",
        f"\n## Model Interpretation",
        f"\n[Add interpretation of results and recommendations]"
    ])
    
    # Save report
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    logger.info(f"Model report saved to {output_file}")
```

## Model Registry and Versioning

```python
# src/models/model_registry.py
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from loguru import logger

class ModelRegistry:
    """Track and version trained models."""
    
    def __init__(self, registry_path: str = 'models/registry.json'):
        """Initialize model registry.
        
        Args:
            registry_path: Path to registry JSON file
        """
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing registry or create new
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                self.registry = json.load(f)
        else:
            self.registry = {'models': []}
    
    def register_model(
        self,
        model_name: str,
        model_type: str,
        model_path: str,
        metrics: Dict[str, float],
        hyperparameters: Dict[str, Any],
        training_data_info: Dict[str, Any],
        notes: str = ""
    ) -> str:
        """Register a trained model.
        
        Args:
            model_name: Descriptive name for the model
            model_type: Type of model (e.g., 'SARIMAX', 'RandomForest')
            model_path: Path to saved model file
            metrics: Performance metrics
            hyperparameters: Model hyperparameters
            training_data_info: Information about training data
            notes: Additional notes
            
        Returns:
            Model version ID
        """
        timestamp = datetime.now()
        version_id = f"{model_name}_v{len([m for m in self.registry['models'] if m['name'] == model_name]) + 1}"
        
        model_entry = {
            'version_id': version_id,
            'name': model_name,
            'type': model_type,
            'path': str(model_path),
            'metrics': metrics,
            'hyperparameters': hyperparameters,
            'training_data': training_data_info,
            'registered_at': timestamp.isoformat(),
            'notes': notes,
            'is_production': False
        }
        
        self.registry['models'].append(model_entry)
        self._save_registry()
        
        logger.info(f"Registered model: {version_id}")
        return version_id
    
    def promote_to_production(self, version_id: str) -> None:
        """Promote a model version to production.
        
        Args:
            version_id: Version ID to promote
        """
        # Demote existing production models
        for model in self.registry['models']:
            if model['is_production']:
                model['is_production'] = False
                logger.info(f"Demoted {model['version_id']} from production")
        
        # Promote new model
        for model in self.registry['models']:
            if model['version_id'] == version_id:
                model['is_production'] = True
                logger.info(f"Promoted {version_id} to production")
                break
        
        self._save_registry()
    
    def get_production_model(self) -> Optional[Dict[str, Any]]:
        """Get current production model.
        
        Returns:
            Production model entry or None
        """
        for model in self.registry['models']:
            if model['is_production']:
                return model
        return None
    
    def list_models(self, model_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered models.
        
        Args:
            model_name: Filter by model name (optional)
            
        Returns:
            List of model entries
        """
        if model_name:
            return [m for m in self.registry['models'] if m['name'] == model_name]
        return self.registry['models']
    
    def _save_registry(self) -> None:
        """Save registry to file."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
```

## Best Practices Summary

### DO
- ✅ Set random seeds for reproducibility
- ✅ Establish baseline models first
- ✅ Use time-aware train/test splits
- ✅ Perform cross-validation
- ✅ Report multiple metrics (MAE, RMSE, MAPE, etc.)
- ✅ Save models with metadata and versioning
- ✅ Document model limitations and assumptions
- ✅ Compare against previous best models

### DON'T
- ❌ Evaluate on training data
- ❌ Use random splits for time series
- ❌ Report only one metric
- ❌ Skip baseline comparisons
- ❌ Ignore model assumptions
- ❌ Deploy without validation
- ❌ Overfit to validation set

## Modeling Checklist

- [ ] **Baselines established**: Simple models evaluated first
- [ ] **Train/test split**: Time-aware split implemented
- [ ] **Cross-validation done**: Multiple folds evaluated
- [ ] **Multiple metrics**: MAE, RMSE, MAPE, R2 reported
- [ ] **Model saved**: Trained model serialized with metadata
- [ ] **Performance documented**: Evaluation report generated
- [ ] **Feature importance**: Top features identified and documented
- [ ] **Residuals analyzed**: Forecast errors examined
- [ ] **Model registered**: Added to model registry
- [ ] **Production criteria**: Meets minimum performance thresholds
