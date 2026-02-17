---
description: Model Training Stage with MCP Integration
stage: Model Training & Machine Learning
---

# Stage Prompt: Model Training and Machine Learning

## Objective

Develop, train, and evaluate machine learning models to make predictions, classify outcomes, or detect patterns.

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Feature Datasets**: `data/4_processed/{epic_id}/features/`
   - Training set (features + target)
   - Validation set (if available)
   - Test set (for final evaluation)
   - Feature documentation

2. **Modeling Requirements**: From user story or analysis objectives
   - Problem type (classification, regression, clustering, anomaly detection)
   - Target variable (what to predict)
   - Success metrics (accuracy, F1, RMSE, etc.)
   - Model interpretability requirements
   - Performance constraints (speed, memory)

3. **Modeling Specifications**:
   - Algorithms to try (baseline + candidates)
   - Hyperparameter search strategy
   - Cross-validation approach
   - Class imbalance handling (if applicable)

4. **Project Context** (REQUIRED - read before modeling):
   - **Business objectives**: `docs/project_context/business-objectives.md` (understand what to optimize)
   - **Tech stack**: `docs/project_context/tech_stack.md` (deployment constraints)
   - **Domain knowledge**: For interpreting feature importance and model decisions
   - Previous models (if improving existing)
   
   Read these files to understand:
   - What the model should optimize (business metric)
   - What deployment constraints exist (speed, interpretability)
   - What technical platform will host the model

## Output Requirements

The model training MUST produce:

1. **Trained Models**: `models/{epic_id}/`
   - Serialized model files (.pkl, .joblib, .h5)
   - Model metadata (hyperparameters, features used)
   - Preprocessing pipelines (scalers, encoders)
   - Model versioning information

2. **Model Training Notebooks**: `notebooks/2_analysis/{epic_id}/` or `notebooks/models/`
   - Data preparation and splitting
   - Baseline model training
   - Model experimentation
   - Hyperparameter tuning
   - Final model training and evaluation

3. **Model Evaluation Results**: `results/metrics/{epic_id}_model_performance.json`
   - Training metrics
   - Validation metrics
   - Test metrics
   - Cross-validation scores
   - Confusion matrix (classification)
   - Feature importance scores

4. **Model Visualizations**: `reports/figures/{epic_id}/model/`
   - ROC curves (classification)
   - Precision-recall curves
   - Feature importance plots
   - Learning curves
   - Residual plots (regression)
   - Confusion matrices

5. **Model Documentation**: `models/{epic_id}/model_card.md`
   - Model description and purpose
   - Training data details
   - Performance metrics
   - Limitations and biases
   - Intended use and deployment notes

## Execution Steps

### Step 1: Model Training Setup

```
1. Create model directories:
   - models/{epic_id}/
   - notebooks/models/ (if not exists)
   - reports/figures/{epic_id}/model/

2. Read feature datasets using Polars:
   import polars as pl
   train_df = pl.read_csv('data/4_processed/{epic_id}/features/train_features.csv')
   test_df = pl.read_csv('data/4_processed/{epic_id}/features/test_features.csv')
   # Read feature documentation

3. Verify data quality:
   - Check for missing values (train_df.null_count())
   - Verify feature dtypes (train_df.dtypes)
   - Confirm target variable exists
   - Check class balance (for classification: train_df['target'].value_counts())
   - Validate temporal ordering (if time series data)

4. Split features (X) and target (y):
   X_train = train_df.drop('target_column')
   y_train = train_df.select('target_column')
   # Convert to appropriate format for modeling library (e.g., numpy, polars DataFrame if needed)
```

### Step 1.5: Initialize Experiment Tracking

```
Set up experiment tracking for reproducibility and comparison:

1. Install MLflow (if not already installed):
   uv pip install mlflow

2. Initialize experiment:
   import mlflow
   mlflow.set_experiment(f"{epic_id}_model_training")
   mlflow.set_tracking_uri("file:./mlruns")  # or remote server

3. Set up experiment metadata:
   mlflow.set_tag("project", "epic_id")
   mlflow.set_tag("stage", "model_training")
   mlflow.set_tag("date", datetime.now().isoformat())

4. Log dataset information:
   mlflow.log_param("train_size", len(train_df))
   mlflow.log_param("test_size", len(test_df))
   mlflow.log_param("n_features", len(X_train.columns))

All subsequent model training steps will log to MLflow for tracking.
```

### Step 2: Baseline Model

```
Create simple baseline model for comparison:

For Classification:
- Majority class classifier (always predict most common class)
- Random classifier
- Simple logistic regression (no tuning)

For Regression:
- Mean predictor (always predict mean of target)
- Median predictor
- Simple linear regression (no feature engineering)

For Clustering:
- Random clustering
- Single-feature clustering

For Anomaly Detection:
- Z-score based (statistical threshold)
- Simple percentile-based

For Time Series:
- Naive forecast (last value persistence)
- Seasonal naive (same period last year/cycle)
- Moving average baseline

1. Train baseline model with MLflow tracking:
   with mlflow.start_run(run_name="baseline_model"):
       mlflow.log_param("model_type", "baseline")
       # Train and log baseline
       
2. Evaluate on validation/test set
3. Record baseline metrics to MLflow
4. Save baseline results

Note: ALL subsequent models MUST outperform this baseline to be considered viable.
```

### Step 3: Model Selection and Training

```
Train multiple candidate models with experiment tracking:

For Classification:
- Logistic Regression (interpretable, fast)
- Random Forest (robust, feature importance)
- Gradient Boosting (XGBoost, LightGBM, CatBoost)
- Support Vector Machines (kernel tricks)
- Neural Networks (for complex patterns)

For Regression:
- Linear Regression (interpretable baseline)
- Ridge/Lasso Regression (regularization)
- Random Forest Regressor
- Gradient Boosting Regressor
- Neural Networks

For Clustering:
- K-Means (centroid-based)
- DBSCAN (density-based)
- Hierarchical clustering
- Gaussian Mixture Models

For Anomaly Detection:
- Isolation Forest
- One-Class SVM
- Autoencoder (neural network)
- Local Outlier Factor (LOF)

For Time Series Forecasting:
- ARIMA/SARIMA (statistical)
- Prophet (trend + seasonality)
- LSTM/GRU (deep learning)
- XGBoost with lag features

1. For each model type:
   with mlflow.start_run(run_name=f"{model_name}"):
       a. Log hyperparameters: mlflow.log_params(params)
       b. Train on training set (record start time)
       c. Evaluate on validation set
       d. Log metrics: mlflow.log_metrics({"accuracy": acc, "f1": f1})
       e. Log training time and memory usage
       f. Log model artifact: mlflow.sklearn.log_model(model, "model")
   
2. Compare all models on validation set (use mlflow.search_runs())
3. Select top 2-3 performing models for tuning

Note: Track ALL experiments systematically for reproducibility.
```

### Step 4: Hyperparameter Tuning

```
Optimize top-performing models:

1. Define hyperparameter search space:
   - Learning rate, max depth, n_estimators (tree models)
   - C, penalty (logistic regression)
   - Number of layers, neurons, dropout (neural networks)

2. Choose search strategy:
   - Grid Search (exhaustive, small space)
   - Random Search (efficient, large space)
   - Bayesian Optimization (smarter search)
   - Optuna, Hyperopt (advanced frameworks)

3. Cross-validation strategy (CRITICAL - choose correctly):
   
   For Independent Data (no temporal/spatial structure):
   - K-fold CV (k=5 or k=10)
   - Stratified K-fold (for imbalanced classes)
   
   For Time Series Data (temporal ordering matters):
   - TimeSeriesSplit (expanding window)
   - Custom walk-forward validation
   - NEVER use random k-fold for temporal data
   
   For Spatial Data (geographic clustering):
   - Spatial cross-validation
   - Leave-one-region-out CV
   
   For Grouped Data (hierarchical structure):
   - GroupKFold (keep groups together)
   - Leave-one-group-out CV

4. Run hyperparameter tuning with MLflow:
   with mlflow.start_run(run_name=f"{model_name}_tuning", nested=True):
       for trial in hyperparameter_search:
           with mlflow.start_run(nested=True):
               mlflow.log_params(trial_params)
               score = cross_validate(model, X, y, cv=cv_strategy)
               mlflow.log_metric("cv_score", score.mean())
   
5. Select best hyperparameters
6. Save tuning results to MLflow
```

### Step 5: Final Model Training

```
Train final model with best hyperparameters:

1. Retrain on full training set (train + validation):
   with mlflow.start_run(run_name="final_model"):
       - Use best hyperparameters from tuning
       - Fit on combined train+validation data
       - Log all final hyperparameters
       - Save training metrics

2. Handle class imbalance (if applicable):
   - SMOTE (Synthetic Minority Over-sampling)
   - Class weights (class_weight='balanced')
   - Undersampling majority class
   - Ensemble methods (BalancedRandomForest)
   - Cost-sensitive learning

3. Feature selection (if beneficial):
   - Remove low-importance features (threshold-based)
   - Recursive feature elimination
   - L1 regularization (Lasso)
   - Correlation-based removal

4. Train final model
5. Save trained model with MLflow:
   mlflow.sklearn.log_model(final_model, "model", 
                            registered_model_name=f"{epic_id}_model")
```

### Step 5.5: Model Calibration (for Classification)

```
Ensure predicted probabilities are reliable (critical for probabilistic predictions):

1. When calibration is needed:
   - Model outputs will be used as probabilities (not just class labels)
   - Decision thresholds need to be set based on probabilities
   - Cost-benefit analysis requires accurate probability estimates
   - Examples: risk scoring, threshold-based alerts, confidence intervals

2. Calibrate model:
   from sklearn.calibration import CalibratedClassifierCV, calibration_curve
   
   calibrated_model = CalibratedClassifierCV(
       base_estimator=final_model,
       method='isotonic',  # or 'sigmoid' for smaller datasets
       cv='prefit'  # if model already trained
   )
   calibrated_model.fit(X_val, y_val)

3. Evaluate calibration:
   y_prob = calibrated_model.predict_proba(X_test)[:, 1]
   prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
   
   # Expected Calibration Error (ECE)
   ece = np.mean(np.abs(prob_true - prob_pred))
   mlflow.log_metric("calibration_error", ece)

4. Visualize calibration:
   plt.plot(prob_pred, prob_true, marker='o', label='Model')
   plt.plot([0, 1], [0, 1], linestyle='--', label='Perfect')
   plt.xlabel('Predicted Probability')
   plt.ylabel('True Probability')
   plt.title('Calibration Curve')
   plt.savefig(f'reports/figures/{epic_id}/model/calibration_curve.png')

5. Use calibrated model for final predictions if ECE improves

Note: Skip if only using predicted classes, not probabilities.
```

### Step 6: Model Evaluation

```
Comprehensively evaluate final model:

For Classification:
- Accuracy, Precision, Recall, F1-score
- ROC-AUC score
- Confusion matrix
- Classification report (per-class metrics)
- Precision-Recall curve
- Calibration plot (if probabilities used)

For Regression:
- R² score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE), RMSE
- Mean Absolute Percentage Error (MAPE)
- Residual plots (check for patterns)
- Actual vs Predicted plot
- Prediction interval coverage

For Clustering:
- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz score
- Cluster size distribution
- Within-cluster sum of squares
- Inter-cluster distances

For Anomaly Detection:
- Precision, Recall, F1 (if labels available)
- False positive rate
- Detection rate
- ROC-AUC
- Anomaly score distribution

For Time Series:
- Forecast accuracy (MAE, RMSE, MAPE)
- Directional accuracy
- Coverage of prediction intervals
- Residual autocorrelation (should be random)

1. Evaluate on held-out test set
2. Calculate all relevant metrics and log to MLflow:
   mlflow.log_metrics({
       "test_accuracy": accuracy,
       "test_f1": f1_score,
       "test_roc_auc": roc_auc
   })
3. Create evaluation visualizations
4. Save evaluation results
```

### Step 6.5: Translate Metrics to Business Impact

```
Translate technical metrics into business outcomes for stakeholders:

1. Create business impact table:

   Example for Binary Classification (Detection/Alert System):
   
   | Metric | Value | Business Translation |
   |--------|-------|---------------------|
   | Precision: 0.75 | 75% alerts are correct | 1 in 4 alerts are false alarms |
   | Recall: 0.90 | Catches 90% of events | Misses 1 in 10 actual events |
   | F1: 0.82 | Balanced performance | Good trade-off between precision/recall |
   | Inference: 50ms | Predictions in 50ms | Real-time decision support possible |
   
   Example for Regression (Demand Forecasting):
   
   | Metric | Value | Business Translation |
   |--------|-------|---------------------|
   | MAPE: 8% | 8% average error | Forecast off by ~8 units per 100 |
   | MAE: $1,200 | $1,200 average error | Typical over/under by $1,200 |
   | R²: 0.85 | Explains 85% variance | Model captures most patterns |

2. Calculate cost-benefit (if costs known):
   
   cost_false_positive = <operational_cost_per_false_alert>
   cost_false_negative = <missed_opportunity_cost>
   cost_true_positive = <intervention_cost> - <prevented_loss>
   
   expected_value = (
       (tp_rate * cost_true_positive) +
       (fp_rate * cost_false_positive) +
       (fn_rate * cost_false_negative) +
       (tn_rate * 0)  # correct rejections have no cost
   )
   
   # Compare to baseline expected value
   improvement = expected_value_model - expected_value_baseline
   
3. Estimate business metrics:
   - Time savings (hours/week)
   - Cost reduction ($/year)
   - Quality improvement (defect rate reduction)
   - Risk reduction (incidents prevented)
   - Revenue impact (opportunities captured)

4. Document business impact in model card

5. Create executive summary visualization:
   - Simple bar chart comparing model vs baseline on business metric
   - ROI calculation if applicable
   - Key decision points and recommended thresholds

Note: Align impact metrics with project objectives (see docs/project_context/business-objectives.md)
```

### Step 7: Feature Importance Analysis

```
Understand which features drive predictions:

1. Calculate feature importance:
   - Tree-based: Gini importance, split count
   - Permutation importance (model-agnostic)
   - SHAP values (Shapley Additive Explanations)
   - Coefficients (for linear models)

2. Visualize feature importance:
   - Bar chart of top 20 features
   - SHAP summary plot
   - SHAP dependence plots (feature interactions)
   - Partial dependence plots

3. Interpret results:
   - Which features are most predictive?
   - Do results align with domain knowledge?
   - Are there unexpected important features?
   - Feature interactions discovered?

4. Save feature importance
```

### Step 8: Model Interpretation and Validation

```
Ensure model is reliable and trustworthy:

1. Model interpretation:
   - Explain individual predictions (LIME, SHAP)
   - Identify decision boundaries
   - Understand model behavior in edge cases
   - Check for spurious correlations

2. Bias and fairness checks:
   - Performance across demographic groups
   - Disparate impact analysis
   - Equalized odds assessment
   - Check for protected attribute leakage

3. Robustness checks:
   - Performance on different data slices
   - Sensitivity to input perturbations
   - Out-of-distribution detection
   - Adversarial examples (if applicable)

4. Learning curves:
   - Training vs validation performance
   - Check for overfitting/underfitting
   - Estimate value of more data

5. Save validation results
```

### Step 9: Model Comparison and Selection

```
Compare all trained models systematically:

1. Create comparison table:
   - Model name
   - Training time
   - Inference speed
   - Memory footprint
   - All evaluation metrics
   - Interpretability score
   - Complexity score

2. Consider trade-offs:
   - Performance vs interpretability
   - Accuracy vs speed
   - Complexity vs maintainability
   - Cost of errors (false positives vs false negatives)

3. Select final production model:
   - Best performance on key metric
   - Meets deployment constraints
   - Acceptable interpretability
   - Stakeholder requirements

4. Save comparison results
```

### Step 10: Model Persistence

```
Save everything needed to use model in production:

1. Save trained model with MLflow:
   
   # Log model with signature and input example
   from mlflow.models.signature import infer_signature
   
   signature = infer_signature(X_train, model.predict(X_train))
   input_example = X_train.head(1)
   
   mlflow.sklearn.log_model(
       sk_model=final_model,
       artifact_path="model",
       signature=signature,
       input_example=input_example,
       registered_model_name=f"{epic_id}_model"
   )
   
   # Alternative: Traditional serialization
   import joblib
   model_path = f"models/{epic_id}/model_v{version}_{timestamp}.joblib"
   joblib.dump(final_model, model_path)

2. Save preprocessing artifacts:
   - Scalers (StandardScaler, MinMaxScaler)
   - Encoders (LabelEncoder, OneHotEncoder)
   - Imputers (SimpleImputer)
   - Feature selectors
   - Full sklearn Pipeline (recommended)
   
   # Save as part of MLflow model or separately
   preprocessing_path = f"models/{epic_id}/preprocessing_v{version}.joblib"
   joblib.dump(preprocessing_pipeline, preprocessing_path)

3. Save model metadata:
   metadata = {
       "model_version": version,
       "creation_date": datetime.now().isoformat(),
       "hyperparameters": model.get_params(),
       "feature_names": list(X_train.columns),
       "feature_order": list(X_train.columns),
       "target_variable": target_name,
       "training_data_stats": {
           "n_samples": len(X_train),
           "feature_means": X_train.mean().to_dict(),
           "feature_stds": X_train.std().to_dict()
       },
       "performance_metrics": {
           "test_accuracy": test_accuracy,
           "test_f1": test_f1
       },
       "mlflow_run_id": mlflow.active_run().info.run_id
   }
   
   import json
   with open(f"models/{epic_id}/metadata_v{version}.json", 'w') as f:
       json.dump(metadata, f, indent=2)

4. Create model package:
   models/{epic_id}/
   ├── model_v{version}_{timestamp}.joblib
   ├── preprocessing_v{version}.joblib
   ├── metadata_v{version}.json
   ├── model_card.md
   ├── requirements.txt
   └── monitoring_baseline.json (see Step 13.5)

5. Generate requirements.txt:
   uv pip freeze > models/{epic_id}/requirements.txt

6. Test model loading:
   # Verify model can be loaded and used
   loaded_model = joblib.load(model_path)
   test_prediction = loaded_model.predict(X_test.head(1))
   assert test_prediction is not None
```

### Step 11: Model Documentation

```
Create comprehensive model card:

1. Model Overview:
   - Model name and version
   - Model type and algorithm
   - Purpose and use case
   - Creation date and author

2. Intended Use:
   - Primary use case
   - Target users
   - Out-of-scope uses

3. Training Data:
   - Data sources
   - Date range
   - Sample size
   - Feature descriptions
   - Known biases or limitations

4. Performance:
   - Evaluation metrics on test set
   - Comparison to baseline
   - Performance across subgroups
   - Confidence intervals

5. Limitations:
   - Known failure modes
   - Data quality dependencies
   - Bias and fairness concerns
   - Temporal limitations (data drift)

6. Deployment:
   - Input format
   - Output format
   - Inference speed
   - Resource requirements
   - Monitoring recommendations

7. Write model card
```

### Step 12: Model Training Notebook

```
Create reproducible training notebook:

1. Notebook structure:
   - Introduction and objectives
   - Data loading and exploration
   - Feature preparation
   - Baseline model
   - Model experimentation
   - Hyperparameter tuning
   - Final model training
   - Evaluation and visualization
   - Model persistence
   - Conclusions and next steps

2. Best practices:
   - Set random seeds for reproducibility
   - Document all hyperparameters
   - Include markdown explanations
   - Show all evaluation metrics
   - Include visualizations inline

3. Save notebook
```

### Step 13: Verification

```
1. Verify all required outputs were created:
   - List files in models/{epic_id}/
   - List files in results/metrics/{epic_id}/
   - Verify model_card.md exists
   - Verify all evaluation visualizations saved
   - Verify MLflow tracking data exists

2. Verify model can be loaded and used:
   # Test traditional loading
   import joblib
   loaded_model = joblib.load(f"models/{epic_id}/model_v{version}.joblib")
   loaded_preprocessing = joblib.load(f"models/{epic_id}/preprocessing_v{version}.joblib")
   
   # Test MLflow loading
   model_uri = f"models:/{epic_id}_model/{version}"
   mlflow_model = mlflow.sklearn.load_model(model_uri)
   
   # Make predictions on sample data
   sample_data = X_test.head(5)
   predictions = loaded_model.predict(sample_data)
   
   # Verify predictions are reasonable (not NaN, within expected range)
   assert not np.isnan(predictions).any()
   assert predictions.shape[0] == len(sample_data)

3. Cross-check against acceptance criteria from user story:
   - Performance metrics meet or exceed thresholds
   - Model satisfies interpretability requirements
   - Inference speed meets deployment constraints
   - All required documentation complete

4. Document verification results in notebook
```

### Step 13.5: Prepare for Model Monitoring

```
Set up foundations for production monitoring (drift detection, performance tracking):

1. Define monitoring metrics:
   
   Performance Metrics:
   - Track model performance on new data (accuracy, F1, MAE, etc.)
   - Set alert thresholds (e.g., >10% performance degradation)
   
   Data Drift Metrics:
   - Feature distribution shifts (Population Stability Index - PSI)
   - Covariate drift (KL divergence, Wasserstein distance)
   - Missing value rates
   
   Prediction Drift:
   - Output distribution changes
   - Prediction confidence distribution
   
   Operational Metrics:
   - Inference latency (p50, p95, p99)
   - Error rates and exceptions
   - Data quality issues

2. Create monitoring baselines (reference distributions from training):
   
   import json
   
   # Use Polars for statistics if needed
   X_train_pl = X_train if hasattr(X_train, 'to_numpy') else X_train
   
   monitoring_baseline = {
       "version": version,
       "creation_date": datetime.now().isoformat(),
       "training_data_stats": {
           "feature_stats": {
               col: {
                   "mean": float(X_train_pl[col].mean()),
                   "std": float(X_train_pl[col].std()),
                   "min": float(X_train_pl[col].min()),
                   "max": float(X_train_pl[col].max()),
                   "q25": float(X_train_pl[col].quantile(0.25)),
                   "q50": float(X_train_pl[col].quantile(0.50)),
                   "q75": float(X_train_pl[col].quantile(0.75)),
                   "missing_rate": float(X_train_pl[col].isna().mean())
               }
               for col in X_train_pl.columns
           }
       },
       "prediction_stats": {
           "train_predictions": {
               "mean": float(y_train_pred.mean()),
               "std": float(y_train_pred.std()),
               "distribution": np.histogram(y_train_pred, bins=10)[0].tolist()
           },
           "test_predictions": {
               "mean": float(y_test_pred.mean()),
               "std": float(y_test_pred.std()),
               "distribution": np.histogram(y_test_pred, bins=10)[0].tolist()
           }
       },
       "performance_baseline": {
           "test_accuracy": float(test_accuracy),
           "test_f1": float(test_f1),
           # Add other metrics
       },
       "alert_thresholds": {
           "performance_degradation": 0.10,  # 10% drop triggers alert
           "psi_threshold": 0.2,  # PSI > 0.2 indicates significant drift
           "missing_rate_threshold": 0.05,  # >5% missing triggers alert
           "latency_p95_ms": 200  # p95 latency threshold
       }
   }
   
   # Save monitoring baseline
   with open(f"models/{epic_id}/monitoring_baseline.json", 'w') as f:
       json.dump(monitoring_baseline, f, indent=2)

3. Document monitoring plan in model card:
   - What metrics will be monitored
   - Alert thresholds and escalation procedures
   - Retraining triggers and schedule
   - Data quality checks

4. Create monitoring script template (optional):
   # scripts/monitor_model_{epic_id}.py
   # Template for production monitoring
   # - Load monitoring baseline
   # - Calculate drift metrics on new data
   # - Check performance on labeled data (if available)
   # - Send alerts if thresholds exceeded

Note: Actual monitoring implementation happens during deployment stage.
```

## Model Training Best Practices

### 1. Avoid Data Leakage
```
❌ Don't use test data during training or hyperparameter tuning
❌ Don't use future information to predict past (time series)
❌ Don't include target-derived features
❌ Don't fit preprocessing on entire dataset before splitting
✅ Fit preprocessing on training data only
✅ Use proper cross-validation (temporal for time series)
✅ Keep test set completely held out until final evaluation
✅ Use pipelines to prevent leakage (sklearn Pipeline)
```

### 2. Handle Imbalanced Classes
```
✅ Use stratified splitting to preserve class distribution
✅ Try SMOTE or other sampling techniques
✅ Use class weights (class_weight='balanced')
✅ Choose appropriate metrics (F1, ROC-AUC, PR-AUC, not just accuracy)
✅ Consider cost-sensitive learning
✅ Use ensemble methods (BalancedRandomForest)
✅ Adjust decision threshold based on business costs
```

### 3. Regularization and Generalization
```
✅ Use cross-validation to detect overfitting
✅ Apply regularization (L1, L2, dropout, early stopping)
✅ Monitor train vs validation performance curves
✅ Use ensemble methods to reduce variance
✅ Keep models as simple as possible (Occam's Razor)
✅ Validate on out-of-distribution data if available
```

### 4. Reproducibility
```
✅ Set random seeds everywhere (np.random.seed, random.seed, tf.random.set_seed)
✅ Document all hyperparameters
✅ Version training data (data lineage)
✅ Save complete environment (uv pip freeze > requirements.txt)
✅ Use version control for code
✅ Use experiment tracking (MLflow)
✅ Save model artifacts with metadata
```

### 5. Temporal Data Handling (for Time Series)
```
❌ Don't use random k-fold cross-validation
❌ Don't shuffle time series data
❌ Don't use future features to predict past
✅ Use chronological train/test splits
✅ Use TimeSeriesSplit or walk-forward validation
✅ Account for seasonality and trends
✅ Test on out-of-sample future periods
✅ Handle holiday/special events explicitly
```

### 6. Tool Stack Compliance
```
✅ Use Polars (import polars as pl) for data processing
✅ Use uv for package management (uv pip install <package>)
✅ Convert to numpy only when required by model library (Polars preferred)
✅ Use MLflow for experiment tracking
✅ Follow project-specific conventions and structure
```

### 7. Domain-Specific Considerations
```
Adapt best practices to your domain:

For forecasting problems (e.g., demand, sales, epidemiology):
✅ Use temporal validation
✅ Check for seasonality and trends
✅ Provide prediction intervals, not just point estimates
✅ Validate lead time (how far ahead predictions are useful)

For detection/alert systems (e.g., fraud, anomaly, outbreak):
✅ Optimize for early detection (recall)
✅ Balance false positives vs false negatives based on costs
✅ Calibrate probabilities for threshold-based decisions
✅ Measure actionability (time to respond)

For risk scoring (e.g., credit, health, safety):
✅ Ensure model interpretability
✅ Test for demographic bias
✅ Calibrate probability estimates
✅ Validate on subgroups

For recommendation systems:
✅ Use user-based splits (not random)
✅ Account for cold-start problems
✅ Measure diversity and novelty, not just accuracy
```

## Success Criteria

The model training is considered successful when:

- ✅ Trained model(s) saved to `models/{epic_id}/` with version and timestamp
- ✅ Model significantly outperforms baseline (document improvement)
- ✅ Evaluation metrics meet user story acceptance criteria
- ✅ Feature importance analyzed and documented
- ✅ Model card created in `models/{epic_id}/model_card.md`
- ✅ Training notebook created with clear documentation
- ✅ All evaluation visualizations saved to `reports/figures/{epic_id}/model/`
- ✅ Model can be loaded and used for predictions (verified)
- ✅ No data leakage detected (preprocessing fitted on training only)
- ✅ All outputs verified and tested
- ✅ MLflow experiments tracked and logged
- ✅ Monitoring baseline created in `models/{epic_id}/monitoring_baseline.json`
- ✅ Business impact documented and translated from metrics
- ✅ Model calibrated if probabilities are used
- ✅ Temporal validation used if data has time structure

## Next Stage

After successful model training, proceed to:
- **Model Deployment**: Deploy model to production environment
- **Monitoring**: Set up performance monitoring and drift detection
- **Iteration**: Retrain with new data or improved features

## References

- Feature Data: `data/4_processed/{epic_id}/features/`
- User Story: `docs/objectives/user_stories/{epic_id}/`
- Tech Stack: `docs/project_context/tech_stack.md`
- Project Structure: `README.md`
