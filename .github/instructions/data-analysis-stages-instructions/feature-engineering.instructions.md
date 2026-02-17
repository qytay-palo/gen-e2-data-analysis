---
name: 'Feature Engineering Standards'
description: 'Best practices for creating, transforming, and selecting features for analysis and modeling'
applyTo: 'src/features/**, notebooks/3_feature_engineering/**, src/data_processing/*transform*.py, src/data_processing/*feature*.py'
---

## Purpose
This document defines **mandatory standards** for feature engineering. Apply these practices when creating derived variables, transforming features, and preparing data for modeling.

## Core Principles

### 1. Reproducible Transformations
- **ALWAYS document transformation logic** with clear comments
- Use functions or classes for complex feature engineering
- Save transformation parameters for consistent application to new data
- Version control feature engineering code

### 2. Avoid Data Leakage
- **NEVER use future information** to create features
- Fit transformations on training data only, apply to validation/test
- Be cautious with aggregations that might include target information
- Document temporal dependencies clearly

### 3. Domain-Driven Features
- Create features that make epidemiological sense
- Consult domain knowledge documentation
- Document the rationale behind each engineered feature
- Validate features with subject matter experts

## Feature Engineering Workflow

### Step 1: Temporal Features

```python
# src/features/temporal_features.py
import polars as pl
from typing import List
from loguru import logger

def create_temporal_features(
    df: pl.DataFrame,
    date_column: str = 'reporting_date'
) -> pl.DataFrame:
    """Create temporal features from date column.
    
    Features created:
    - year, month, day_of_week, day_of_year
    - quarter, week_of_year
    - is_weekend, is_month_start, is_month_end
    - days_since_epoch (for trend modeling)
    
    Args:
        df: Input DataFrame with date column
        date_column: Name of date column
        
    Returns:
        DataFrame with additional temporal features
        
    Example:
        >>> df = create_temporal_features(df, date_column='reporting_date')
        >>> print(df.columns)  # Includes year, month, day_of_week, etc.
    """
    logger.info(f"Creating temporal features from {date_column}")
    
    # Ensure date column is proper Date type
    df = df.with_columns(
        pl.col(date_column).cast(pl.Date)
    )
    
    # Create temporal features
    df = df.with_columns([
        # Basic date components
        pl.col(date_column).dt.year().alias('year'),
        pl.col(date_column).dt.month().alias('month'),
        pl.col(date_column).dt.day().alias('day'),
        pl.col(date_column).dt.weekday().alias('day_of_week'),  # Monday=1, Sunday=7
        pl.col(date_column).dt.ordinal_day().alias('day_of_year'),
        
        # Week and quarter
        pl.col(date_column).dt.week().alias('week_of_year'),
        pl.col(date_column).dt.quarter().alias('quarter'),
        
        # Boolean flags
        (pl.col(date_column).dt.weekday() >= 6).alias('is_weekend'),
        (pl.col(date_column).dt.day() == 1).alias('is_month_start'),
        
        # Cyclical encoding for month (important for seasonality)
        (2 * 3.14159 * pl.col(date_column).dt.month() / 12).sin().alias('month_sin'),
        (2 * 3.14159 * pl.col(date_column).dt.month() / 12).cos().alias('month_cos'),
        
        # Cyclical encoding for day of week
        (2 * 3.14159 * pl.col(date_column).dt.weekday() / 7).sin().alias('dow_sin'),
        (2 * 3.14159 * pl.col(date_column).dt.weekday() / 7).cos().alias('dow_cos'),
        
        # Days since reference point (for trend)
        (pl.col(date_column) - pl.date(2020, 1, 1)).dt.total_days().alias('days_since_2020'),
    ])
    
    logger.info(f"Created {12} temporal features")
    return df


def create_lag_features(
    df: pl.DataFrame,
    target_column: str,
    group_by_columns: List[str],
    lags: List[int] = [1, 2, 3, 4, 7, 14, 28]
) -> pl.DataFrame:
    """Create lagged features for time series prediction.
    
    Args:
        df: Input DataFrame sorted by time within groups
        target_column: Column to create lags from
        group_by_columns: Columns defining time series groups (e.g., ['disease'])
        lags: List of lag periods to create
        
    Returns:
        DataFrame with lag features added
        
    Example:
        >>> # Create 1-week, 2-week, and 4-week lags
        >>> df = create_lag_features(
        ...     df, 
        ...     target_column='case_count',
        ...     group_by_columns=['disease'],
        ...     lags=[1, 2, 4]
        ... )
    """
    logger.info(f"Creating lag features for {target_column} with lags: {lags}")
    
    for lag in lags:
        df = df.with_columns(
            pl.col(target_column)
            .shift(lag)
            .over(group_by_columns)
            .alias(f'{target_column}_lag_{lag}')
        )
        logger.debug(f"Created lag_{lag} feature")
    
    logger.info(f"Created {len(lags)} lag features")
    return df


def create_rolling_features(
    df: pl.DataFrame,
    target_column: str,
    group_by_columns: List[str],
    windows: List[int] = [4, 8, 12, 26, 52],
    aggregations: List[str] = ['mean', 'std', 'min', 'max']
) -> pl.DataFrame:
    """Create rolling window features.
    
    Args:
        df: Input DataFrame sorted by time within groups
        target_column: Column to calculate rolling statistics on
        group_by_columns: Columns defining time series groups
        windows: List of window sizes (in time periods)
        aggregations: List of aggregation functions
        
    Returns:
        DataFrame with rolling features added
        
    Example:
        >>> # Create 4-week and 12-week rolling means
        >>> df = create_rolling_features(
        ...     df,
        ...     target_column='case_count',
        ...     group_by_columns=['disease'],
        ...     windows=[4, 12],
        ...     aggregations=['mean', 'std']
        ... )
    """
    logger.info(f"Creating rolling features for {target_column}")
    
    for window in windows:
        for agg in aggregations:
            feature_name = f'{target_column}_rolling_{window}w_{agg}'
            
            if agg == 'mean':
                df = df.with_columns(
                    pl.col(target_column)
                    .rolling_mean(window_size=window, min_periods=1)
                    .over(group_by_columns)
                    .alias(feature_name)
                )
            elif agg == 'std':
                df = df.with_columns(
                    pl.col(target_column)
                    .rolling_std(window_size=window, min_periods=1)
                    .over(group_by_columns)
                    .alias(feature_name)
                )
            elif agg == 'min':
                df = df.with_columns(
                    pl.col(target_column)
                    .rolling_min(window_size=window, min_periods=1)
                    .over(group_by_columns)
                    .alias(feature_name)
                )
            elif agg == 'max':
                df = df.with_columns(
                    pl.col(target_column)
                    .rolling_max(window_size=window, min_periods=1)
                    .over(group_by_columns)
                    .alias(feature_name)
                )
            
            logger.debug(f"Created {feature_name}")
    
    total_features = len(windows) * len(aggregations)
    logger.info(f"Created {total_features} rolling features")
    return df
```

### Step 2: Domain-Specific Features

```python
# src/features/disease_features.py
import polars as pl
from loguru import logger
from typing import Optional

def create_outbreak_indicators(
    df: pl.DataFrame,
    case_column: str = 'case_count',
    group_by: str = 'disease',
    threshold_method: str = 'iqr',
    multiplier: float = 1.5
) -> pl.DataFrame:
    """Create outbreak indicator features.
    
    An outbreak is flagged when case counts exceed a threshold based on
    historical patterns.
    
    Args:
        df: Input DataFrame
        case_column: Column containing case counts
        group_by: Column to group by (usually 'disease')
        threshold_method: 'iqr' or 'percentile' or 'std'
        multiplier: Multiplier for threshold calculation
        
    Returns:
        DataFrame with outbreak indicator features
        
    Example:
        >>> df = create_outbreak_indicators(df, threshold_method='iqr')
        >>> # Creates: is_outbreak, outbreak_magnitude
    """
    logger.info(f"Creating outbreak indicators using {threshold_method} method")
    
    if threshold_method == 'iqr':
        # IQR method: Flag if > Q3 + multiplier * IQR
        df = df.with_columns([
            pl.col(case_column).quantile(0.75).over(group_by).alias('_q3'),
            pl.col(case_column).quantile(0.25).over(group_by).alias('_q1'),
        ])
        
        df = df.with_columns(
            (pl.col('_q3') - pl.col('_q1')).alias('_iqr')
        )
        
        df = df.with_columns(
            (pl.col('_q3') + multiplier * pl.col('_iqr')).alias('outbreak_threshold')
        )
        
    elif threshold_method == 'percentile':
        # Percentile method: Flag if > 95th percentile
        df = df.with_columns(
            pl.col(case_column)
            .quantile(0.95)
            .over(group_by)
            .alias('outbreak_threshold')
        )
        
    elif threshold_method == 'std':
        # Standard deviation method: Flag if > mean + multiplier * std
        df = df.with_columns([
            pl.col(case_column).mean().over(group_by).alias('_mean'),
            pl.col(case_column).std().over(group_by).alias('_std'),
        ])
        
        df = df.with_columns(
            (pl.col('_mean') + multiplier * pl.col('_std')).alias('outbreak_threshold')
        )
    
    # Create outbreak indicator
    df = df.with_columns([
        (pl.col(case_column) > pl.col('outbreak_threshold')).alias('is_outbreak'),
        (pl.col(case_column) / pl.col('outbreak_threshold')).alias('outbreak_magnitude'),
    ])
    
    # Clean up temporary columns
    temp_cols = [col for col in df.columns if col.startswith('_')]
    df = df.drop(temp_cols)
    
    outbreak_count = df.filter(pl.col('is_outbreak')).height
    logger.info(f"Flagged {outbreak_count} outbreak periods")
    
    return df


def create_growth_rate_features(
    df: pl.DataFrame,
    case_column: str = 'case_count',
    group_by: List[str] = ['disease'],
    periods: List[int] = [1, 4, 12]
) -> pl.DataFrame:
    """Create growth rate features.
    
    Calculate percentage change and absolute change over various periods.
    
    Args:
        df: Input DataFrame sorted by time
        case_column: Column containing case counts
        group_by: Columns to group by
        periods: List of periods for growth calculation
        
    Returns:
        DataFrame with growth rate features
    """
    logger.info(f"Creating growth rate features for periods: {periods}")
    
    for period in periods:
        # Percentage change
        df = df.with_columns(
            ((pl.col(case_column) - pl.col(case_column).shift(period).over(group_by)) 
             / (pl.col(case_column).shift(period).over(group_by) + 1))  # +1 to avoid division by zero
            .alias(f'growth_rate_{period}w_pct')
        )
        
        # Absolute change
        df = df.with_columns(
            (pl.col(case_column) - pl.col(case_column).shift(period).over(group_by))
            .alias(f'growth_rate_{period}w_abs')
        )
    
    logger.info(f"Created {len(periods) * 2} growth rate features")
    return df


def create_seasonality_features(
    df: pl.DataFrame,
    case_column: str = 'case_count',
    date_column: str = 'reporting_date',
    group_by: str = 'disease'
) -> pl.DataFrame:
    """Create seasonality features based on historical patterns.
    
    Args:
        df: Input DataFrame
        case_column: Column containing case counts
        date_column: Date column
        group_by: Column to group by
        
    Returns:
        DataFrame with seasonality features
    """
    logger.info("Creating seasonality features")
    
    # Extract month if not already present
    if 'month' not in df.columns:
        df = df.with_columns(
            pl.col(date_column).dt.month().alias('month')
        )
    
    # Calculate historical average for each month-disease combination
    monthly_avg = df.group_by([group_by, 'month']).agg([
        pl.col(case_column).mean().alias('historical_monthly_avg'),
        pl.col(case_column).std().alias('historical_monthly_std'),
    ])
    
    # Join back to main dataframe
    df = df.join(monthly_avg, on=[group_by, 'month'], how='left')
    
    # Create seasonality index (current / historical average)
    df = df.with_columns(
        (pl.col(case_column) / (pl.col('historical_monthly_avg') + 1))
        .alias('seasonality_index')
    )
    
    # Create z-score relative to seasonal baseline
    df = df.with_columns(
        ((pl.col(case_column) - pl.col('historical_monthly_avg')) 
         / (pl.col('historical_monthly_std') + 1))
        .alias('seasonal_zscore')
    )
    
    logger.info("Created 4 seasonality features")
    return df
```

### Step 3: Feature Scaling and Encoding

```python
# src/features/feature_transformations.py
import polars as pl
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pickle
from pathlib import Path
from loguru import logger

@dataclass
class ScalingParameters:
    """Store parameters for feature scaling."""
    method: str  # 'standard', 'minmax', 'robust'
    feature_stats: Dict[str, Dict[str, float]]
    
    def save(self, filepath: str) -> None:
        """Save scaling parameters to file."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        logger.info(f"Saved scaling parameters to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'ScalingParameters':
        """Load scaling parameters from file."""
        with open(filepath, 'rb') as f:
            params = pickle.load(f)
        logger.info(f"Loaded scaling parameters from {filepath}")
        return params


class FeatureScaler:
    """Scale numeric features with fit-transform pattern."""
    
    def __init__(self, method: str = 'standard'):
        """Initialize scaler.
        
        Args:
            method: Scaling method - 'standard', 'minmax', or 'robust'
        """
        self.method = method
        self.params: Optional[ScalingParameters] = None
    
    def fit(self, df: pl.DataFrame, columns: List[str]) -> 'FeatureScaler':
        """Fit scaler to training data.
        
        Args:
            df: Training DataFrame
            columns: List of numeric columns to scale
            
        Returns:
            Fitted scaler (self)
        """
        logger.info(f"Fitting {self.method} scaler on {len(columns)} columns")
        
        feature_stats = {}
        
        for col in columns:
            if self.method == 'standard':
                # Z-score normalization: (x - mean) / std
                mean_val = df[col].mean()
                std_val = df[col].std()
                feature_stats[col] = {'mean': mean_val, 'std': std_val}
                
            elif self.method == 'minmax':
                # Min-max scaling: (x - min) / (max - min)
                min_val = df[col].min()
                max_val = df[col].max()
                feature_stats[col] = {'min': min_val, 'max': max_val}
                
            elif self.method == 'robust':
                # Robust scaling: (x - median) / IQR
                median_val = df[col].median()
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                feature_stats[col] = {'median': median_val, 'iqr': iqr}
        
        self.params = ScalingParameters(
            method=self.method,
            feature_stats=feature_stats
        )
        
        logger.info(f"Scaler fitted on {len(columns)} features")
        return self
    
    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        """Transform data using fitted parameters.
        
        Args:
            df: DataFrame to transform
            
        Returns:
            Transformed DataFrame
            
        Raises:
            ValueError: If scaler not fitted
        """
        if self.params is None:
            raise ValueError("Scaler not fitted. Call fit() first.")
        
        logger.info(f"Transforming {len(self.params.feature_stats)} features")
        
        df_transformed = df.clone()
        
        for col, stats in self.params.feature_stats.items():
            if self.method == 'standard':
                df_transformed = df_transformed.with_columns(
                    ((pl.col(col) - stats['mean']) / stats['std'])
                    .alias(f'{col}_scaled')
                )
                
            elif self.method == 'minmax':
                df_transformed = df_transformed.with_columns(
                    ((pl.col(col) - stats['min']) / (stats['max'] - stats['min']))
                    .alias(f'{col}_scaled')
                )
                
            elif self.method == 'robust':
                df_transformed = df_transformed.with_columns(
                    ((pl.col(col) - stats['median']) / stats['iqr'])
                    .alias(f'{col}_scaled')
                )
        
        return df_transformed
    
    def fit_transform(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
        """Fit and transform in one step.
        
        Args:
            df: DataFrame to fit and transform
            columns: Columns to scale
            
        Returns:
            Transformed DataFrame
        """
        self.fit(df, columns)
        return self.transform(df)
    
    def save_params(self, filepath: str) -> None:
        """Save fitted parameters to file."""
        if self.params is None:
            raise ValueError("No parameters to save. Fit scaler first.")
        self.params.save(filepath)
    
    def load_params(self, filepath: str) -> None:
        """Load parameters from file."""
        self.params = ScalingParameters.load(filepath)


def create_categorical_encodings(
    df: pl.DataFrame,
    categorical_columns: List[str],
    encoding_method: str = 'label',
    min_frequency: int = 5
) -> Tuple[pl.DataFrame, Dict]:
    """Encode categorical variables.
    
    Args:
        df: Input DataFrame
        categorical_columns: List of categorical columns to encode
        encoding_method: 'label', 'onehot', or 'frequency'
        min_frequency: Minimum frequency for category (rare categories -> 'Other')
        
    Returns:
        Tuple of (encoded DataFrame, encoding mappings dictionary)
    """
    logger.info(f"Encoding {len(categorical_columns)} categorical columns using {encoding_method}")
    
    encoding_mappings = {}
    df_encoded = df.clone()
    
    for col in categorical_columns:
        # Group rare categories
        value_counts = df[col].value_counts()
        rare_categories = [
            row[0] for row in value_counts.iter_rows() 
            if row[1] < min_frequency
        ]
        
        if rare_categories:
            logger.info(f"{col}: Grouping {len(rare_categories)} rare categories as 'Other'")
            df_encoded = df_encoded.with_columns(
                pl.when(pl.col(col).is_in(rare_categories))
                .then(pl.lit('Other'))
                .otherwise(pl.col(col))
                .alias(col)
            )
        
        if encoding_method == 'label':
            # Label encoding: assign integer to each category
            unique_values = sorted(df_encoded[col].unique().to_list())
            mapping = {val: idx for idx, val in enumerate(unique_values)}
            
            df_encoded = df_encoded.with_columns(
                pl.col(col).replace(mapping).alias(f'{col}_encoded')
            )
            
            encoding_mappings[col] = {'type': 'label', 'mapping': mapping}
            
        elif encoding_method == 'onehot':
            # One-hot encoding
            df_encoded = df_encoded.to_dummies(columns=[col], separator='_')
            unique_values = sorted(df[col].unique().to_list())
            encoding_mappings[col] = {'type': 'onehot', 'categories': unique_values}
            
        elif encoding_method == 'frequency':
            # Frequency encoding: replace with frequency of occurrence
            freq_map = {}
            for row in df_encoded[col].value_counts().iter_rows():
                freq_map[row[0]] = row[1] / len(df_encoded)
            
            df_encoded = df_encoded.with_columns(
                pl.col(col).replace(freq_map).alias(f'{col}_freq')
            )
            
            encoding_mappings[col] = {'type': 'frequency', 'mapping': freq_map}
    
    logger.info(f"Encoded {len(categorical_columns)} categorical features")
    return df_encoded, encoding_mappings
```

### Step 4: Feature Selection

```python
# src/features/feature_selection.py
import polars as pl
from typing import List, Tuple
from loguru import logger

def select_features_by_correlation(
    df: pl.DataFrame,
    target_column: str,
    feature_columns: List[str],
    correlation_threshold: float = 0.95
) -> List[str]:
    """Select features by removing highly correlated pairs.
    
    Args:
        df: Input DataFrame
        target_column: Target variable name
        feature_columns: List of feature column names
        correlation_threshold: Threshold for removing correlated features
        
    Returns:
        List of selected feature names
    """
    logger.info(f"Selecting features from {len(feature_columns)} candidates")
    
    # Calculate correlation matrix
    corr_df = df.select(feature_columns).to_pandas().corr().abs()
    
    # Find pairs of highly correlated features
    upper_tri = corr_df.where(
        np.triu(np.ones(corr_df.shape), k=1).astype(bool)
    )
    
    # Identify features to drop
    to_drop = [
        column for column in upper_tri.columns 
        if any(upper_tri[column] > correlation_threshold)
    ]
    
    selected_features = [col for col in feature_columns if col not in to_drop]
    
    logger.info(
        f"Removed {len(to_drop)} highly correlated features. "
        f"Selected {len(selected_features)} features."
    )
    
    return selected_features


def select_features_by_variance(
    df: pl.DataFrame,
    feature_columns: List[str],
    variance_threshold: float = 0.01
) -> List[str]:
    """Remove low-variance features.
    
    Args:
        df: Input DataFrame
        feature_columns: List of feature column names
        variance_threshold: Minimum variance threshold
        
    Returns:
        List of selected feature names
    """
    logger.info(f"Filtering features by variance threshold: {variance_threshold}")
    
    selected_features = []
    
    for col in feature_columns:
        variance = df[col].var()
        if variance >= variance_threshold:
            selected_features.append(col)
    
    removed_count = len(feature_columns) - len(selected_features)
    logger.info(f"Removed {removed_count} low-variance features")
    
    return selected_features
```

## Complete Feature Engineering Pipeline

```python
# Example: End-to-end feature engineering pipeline
from pathlib import Path
import polars as pl
from loguru import logger

def feature_engineering_pipeline(
    df: pl.DataFrame,
    target_column: str = 'case_count',
    save_params: bool = True,
    params_dir: str = 'models/feature_engineering'
) -> pl.DataFrame:
    """Complete feature engineering pipeline.
    
    Args:
        df: Input DataFrame (must be sorted by date within disease groups)
        target_column: Target variable for prediction
        save_params: Whether to save transformation parameters
        params_dir: Directory to save parameters
        
    Returns:
        DataFrame with engineered features
    """
    logger.info("Starting feature engineering pipeline")
    
    # Create output directory
    Path(params_dir).mkdir(parents=True, exist_ok=True)
    
    # 1. Temporal features
    df = create_temporal_features(df, date_column='reporting_date')
    
    # 2. Lag features (avoid data leakage - only use past data)
    df = create_lag_features(
        df,
        target_column=target_column,
        group_by_columns=['disease'],
        lags=[1, 2, 3, 4, 8, 12, 26, 52]
    )
    
    # 3. Rolling features
    df = create_rolling_features(
        df,
        target_column=target_column,
        group_by_columns=['disease'],
        windows=[4, 8, 12, 26, 52],
        aggregations=['mean', 'std', 'min', 'max']
    )
    
    # 4. Growth rates
    df = create_growth_rate_features(
        df,
        case_column=target_column,
        group_by=['disease'],
        periods=[1, 4, 12, 26]
    )
    
    # 5. Outbreak indicators
    df = create_outbreak_indicators(
        df,
        case_column=target_column,
        group_by='disease',
        threshold_method='iqr'
    )
    
    # 6. Seasonality features
    df = create_seasonality_features(
        df,
        case_column=target_column,
        date_column='reporting_date',
        group_by='disease'
    )
    
    # 7. Categorical encoding
    if 'disease' in df.columns:
        df, encoding_mappings = create_categorical_encodings(
            df,
            categorical_columns=['disease'],
            encoding_method='label'
        )
        
        if save_params:
            import pickle
            with open(f'{params_dir}/categorical_encodings.pkl', 'wb') as f:
                pickle.dump(encoding_mappings, f)
    
    # 8. Feature scaling (fit only on training data in practice)
    numeric_features = [
        col for col in df.columns 
        if df[col].dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]
        and col != target_column
    ]
    
    scaler = FeatureScaler(method='robust')
    df = scaler.fit_transform(df, numeric_features)
    
    if save_params:
        scaler.save_params(f'{params_dir}/scaler_params.pkl')
    
    logger.info(f"Feature engineering complete. Final shape: {df.shape}")
    logger.info(f"Total features: {len(df.columns)}")
    
    return df
```

## Best Practices Summary

### DO
- ✅ Document feature rationale and engineering logic
- ✅ Create features that align with domain knowledge
- ✅ Use fit-transform pattern to avoid data leakage
- ✅ Save transformation parameters for production use
- ✅ Validate features don't use future information
- ✅ Create interpretable features when possible
- ✅ Remove low-variance and highly correlated features

### DON'T
- ❌ Use future information in feature creation (data leakage)
- ❌ Apply transformations fitted on test data to training data
- ❌ Create features without documenting their purpose
- ❌ Ignore domain knowledge when engineering features
- ❌ Create hundreds of features without selection
- ❌ Scale features before splitting train/test data

## Checklist

Before using engineered features for modeling:

- [ ] **Features documented**: Each feature's purpose and calculation explained
- [ ] **No data leakage**: Features don't use future information
- [ ] **Fit-transform applied**: Parameters fit on training, applied to test
- [ ] **Parameters saved**: Transformation parameters saved for production
- [ ] **Features validated**: Checked for null values and reasonable ranges
- [ ] **Feature selection done**: Removed redundant and low-variance features
- [ ] **Domain validation**: Features reviewed by subject matter experts
- [ ] **Code tested**: Feature engineering functions have unit tests
