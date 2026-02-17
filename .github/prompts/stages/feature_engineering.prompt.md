---
description: Feature Engineering Stage with MCP Integration
stage: Feature Engineering
---

# Stage Prompt: Feature Engineering

## Objective

Transform prepared data into meaningful features that capture patterns, relationships, and domain knowledge for analysis or modeling.

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Prepared Data**: `data/4_processed/` or `data/3_interim/`
   - Clean, validated datasets
   - Documented data types and schemas

2. **Feature Requirements**: From user story or analysis objectives
   - Target variable (if for modeling)
   - Required feature types (numerical, categorical, temporal, text)
   - Domain-specific features needed
   - Feature selection criteria

3. **Feature Engineering Specifications**:
   - Transformation methods needed
   - Aggregation windows (for time-based features)
   - Encoding strategies (one-hot, label, target encoding)
   - Scaling/normalization requirements

4. **Project Context** (REQUIRED - read before feature engineering):
   - **Data dictionary**: `docs/data_dictionary/`
   - **Business objectives**: `docs/project_context/business-objectives.md`
   - **Domain knowledge**: `docs/project_context/domain-knowledge.md` Review project context for domain-specific features
   - Previous feature sets (if building on prior work)
   
   Read these files to understand:
   - What features make business sense
   - What domain-specific patterns to capture
   - What features align with objectives

## Output Requirements

The feature engineering MUST produce:

1. **Feature Engineering Notebook**: `notebooks/3_feature_engineering/{epic_id}/`
   - Complete feature creation workflow
   - Transformation logic and rationale
   - Feature validation and quality checks
   - Inline visualizations of feature distributions

2. **Feature Dataset**: `data/4_processed/{epic_id}/features/`
   - Engineered feature sets (CSV/Parquet)
   - Train/test splits (if applicable)
   - Feature matrices ready for modeling

3. **Feature Documentation**: `data/schemas/{epic_id}/feature_dictionary.md`
   - Feature name and description
   - Creation logic and formula
   - Data type and value range
   - Missingness handling approach
   - Importance/relevance notes

4. **Feature Statistics**: `results/metrics/{epic_id}_feature_stats.json`
   - Feature distributions (mean, std, min, max)
   - Correlation matrix (with target if applicable)
   - Feature importance scores (if available)
   - Missingness rates

5. **Feature Transformation Pipeline**: `src/features/{epic_id}_feature_pipeline.py`
   - Reusable feature engineering code
   - Preprocessing classes/functions
   - Transformation pipeline (sklearn Pipeline or custom)

## Execution Steps

### Step 1: Feature Engineering Setup

```
1. Create feature directories:
   - notebooks/3_feature_engineering/{epic_id}/
   - data/4_processed/{epic_id}/features/
   - src/features/

2. Read prepared data from data/4_processed/

3. Read data schemas from data/schemas/

4. Read feature requirements from user story
```

**Example MCP Commands**:
- "Use filesystem tools to create directory notebooks/3_feature_engineering/epic-001/"
- "Use filesystem tools to read data/4_processed/epic-001/clean_patient_visits.csv"
- "Use filesystem tools to read data/schemas/epic-001/patient_visits_schema.md"

### Step 2: Temporal Feature Engineering (for time-series data)

```
1. Extract datetime components:
   - Year, month, day, day_of_week, hour, minute
   - Quarter, week_of_year, day_of_year
   - Is_weekend, is_holiday flags
   - Shift (morning/afternoon/evening/night)

2. Create lag features (past values):
   - Previous day/week/month values
   - Rolling averages (7-day, 14-day, 30-day)
   - Rolling standard deviations

3. Create lead features (future indicators):
   - Next period predicted values (if available)
   - Trend indicators (increasing/decreasing)

4. Create time-based aggregations:
   - Visits per hour/day/week/month
   - Average wait time by time period
   - Peak vs off-peak indicators

5. Save temporal features notebook
```

### Step 3: Categorical Feature Engineering

```
1. Identify categorical variables:
   - Department, diagnosis_code, patient_type
   - Geographic categories (region, facility)
   - Classification categories (urgency, severity)

2. Apply encoding strategies:
   - One-hot encoding for low cardinality (<10 unique values)
   - Label encoding for ordinal categories
   - Target encoding for high cardinality (with proper CV)
   - Frequency encoding (count of occurrences)
   - Hash encoding for very high cardinality (>100 unique values)
   - Weight of Evidence (WOE) encoding for risk modeling
   - Binary encoding for moderate cardinality (10-50 values)

3. Create categorical aggregations:
   - Count of events per category
   - Percentage distribution across categories
   - Category-specific statistics

4. Handle rare categories:
   - Group infrequent categories into "Other"
   - Threshold: <5% occurrence

5. Save categorical features notebook
```

### Step 4: Numerical Feature Engineering

```
1. Create derived numerical features:
   - Ratios (e.g., wait_time / avg_wait_time)
   - Differences (e.g., actual_time - expected_time)
   - Products (e.g., staff_count * utilization_rate)
   - Percentiles and ranks

2. Create binned features:
   - Age groups (0-18, 19-35, 36-55, 56+)
   - Wait time buckets (0-15min, 15-30min, 30-60min, 60+min)
   - Utilization bands (low, medium, high)

3. Apply transformations:
   - Log transformation (for skewed distributions)
   - Square root transformation
   - Box-Cox transformation (for normality)

4. Create interaction features:
   - Department × Time_of_day
   - Patient_age × Diagnosis_severity
   - Capacity × Demand

5. Consider advanced numerical techniques:
   - Quantile transformations (uniform or normal distribution)
   - Power transformations (Yeo-Johnson for zero/negative values)
   - Rank-based features for robustness to outliers

7. Save numerical features notebook
```

### Step 5: Domain-Specific Feature Engineering

```
Create features specific to your business domain:

**CRITICAL**: Read `docs/project_context/business-objectives.md` and `docs/data_dictionary/` to understand domain-specific features

1. Entity-level features:
   - Frequency metrics (events per time period)
   - Recurrence indicators (repeat events within timeframe)
   - Status flags and classifications
   - Behavior indicators

2. Organizational-level features:
   - Capacity/utilization rates
   - Performance percentiles
   - Resource ratios
   - Efficiency scores

3. Temporal pattern features:
   - Seasonal indicators (domain-specific seasons)
   - Day-of-week patterns
   - Time-of-day patterns
   - Holiday/event effects

4. Geographic features (if applicable):
   - Distance metrics
   - Density indicators
   - Location classifications
   - Regional characteristics

**Domain Examples**:
- Healthcare: Visit frequency, capacity utilization, seasonal flu patterns, readmission indicators
- Retail: Purchase frequency, store traffic, holiday shopping patterns, customer churn indicators
- Finance: Transaction frequency, account utilization, end-of-quarter effects, default risk indicators
- Manufacturing: Equipment uptime, defect rates, production cycles, maintenance patterns

5. Save domain features notebook
```

### Step 5a: Text Feature Engineering (if text data present and where relevant)

```
1. Basic text features:
   - Text length (character count, word count)
   - Special character counts (punctuation, numbers, uppercase)
   - Readability scores (Flesch-Kincaid, etc.)
   - Sentiment scores

2. Vectorization methods:
   - Bag-of-Words (CountVectorizer) for simple text
   - TF-IDF (TfidfVectorizer) for weighted importance
   - N-grams (bigrams, trigrams) for phrase patterns
   - Hash vectorization for memory efficiency

3. Advanced text features:
   - Topic modeling outputs (LDA, NMF)
   - Named entity recognition (NER) counts
   - Word embeddings (Word2Vec, GloVe, FastText averages)
   - Pre-trained transformer embeddings (BERT, domain-specific models)

4. Domain-specific text patterns:
   - Keyword matching for specific terms
   - Regular expression patterns
   - Custom dictionary-based features

5. Consider computational constraints:
   - Limit vocabulary size (max_features parameter)
   - Use sparse matrices for memory efficiency
   - Apply dimensionality reduction after vectorization

6. Save text features notebook
```

### Step 6: Feature Scaling and Normalization

```
1. Identify features requiring scaling:
   - Features with different units or scales
   - Features for distance-based algorithms
   - Features for neural networks

2. Apply appropriate scaling:
   - StandardScaler (mean=0, std=1) for normally distributed
   - MinMaxScaler (0-1) for bounded ranges
   - RobustScaler (for outlier-resistant scaling)
   - Normalizer (for vector normalization)

3. Important: Fit scaler on training data only
   - Save scaler object for future use
   - Apply same transformation to test data

4. Save scaler objects
```

### Step 7: Feature Selection

```
1. Calculate feature importance:
   - Correlation with target variable
   - Mutual information scores
   - Chi-square test for categorical features
   - Variance thresholds (remove low-variance features)

2. Remove redundant features:
   - High correlation between features (>0.95)
   - Multicollinearity check (VIF > 10)

3. Apply feature selection methods:
   - SelectKBest (top K features)
   - Recursive Feature Elimination (RFE)
   - L1-based feature selection (Lasso)
   - Tree-based feature importance
   - SHAP values for model-agnostic importance
   - Permutation importance for robustness
   - Boruta algorithm for all-relevant features

4. Statistical validation:
   - ANOVA F-test for numerical-categorical relationships
   - Chi-square test with p-value thresholds (<0.05)
   - Mutual information with threshold (>0.01)
   - Stability selection across bootstrap samples

5. Create selected feature set

6. Document feature selection rationale:
   - Number of features before/after selection
   - Selection criteria used
   - Features removed and why
   - Performance impact of selection

7. Save feature importance scores
```

### Step 8: Create Final Feature Dataset

```
1. Combine all engineered features:
   - Temporal features
   - Categorical features (encoded)
   - Numerical features (transformed)
   - Domain-specific features
   - Selected features only

2. Handle missing values:
   - Imputation strategies (mean, median, mode, forward fill)
   - Create missingness indicators (if informative)
   - Document imputation logic

3. Create train/test/validation splits (if applicable):
   - Time-based split for time-series (no random shuffle)
   - Stratified split for classification (maintain class balance)
   - Random split for other cases
   - Typical ratios: 70/15/15 or 80/20

4. Verify data quality:
   - No missing values in critical features
   - No infinite values
   - Correct data types
   - Expected value ranges

5. Save final feature datasets
```

### Step 9: Feature Documentation

```
1. Create comprehensive feature dictionary:
   - Feature name (column name)
   - Description (what it represents)
   - Creation logic (formula or transformation)
   - Data type (int, float, category)
   - Value range (min, max, or categories)
   - Missing value handling
   - Importance notes

2. Document feature engineering decisions:
   - Why certain features were created
   - Why certain transformations were applied
   - Why certain features were removed
   - Assumptions made

3. Write feature dictionary to data/schemas/{epic_id}/feature_dictionary.md
```

### Step 10: Create Reusable Feature Pipeline

```
1. Convert notebook logic into production code:
   - Feature transformation functions
   - Preprocessing classes
   - sklearn Pipeline or custom pipeline

2. Create modular feature engineering pipeline:
   - TemporalFeatureExtractor class
   - CategoricalEncoder class
   - NumericalTransformer class
   - DomainFeatureCreator class
   - FeatureSelector class

3. Add pipeline orchestration:
   - Combine all transformers
   - Fit on training data
   - Transform train/test consistently

4. Save pipeline code to src/features/{epic_id}_feature_pipeline.py
```

### Step 11: Feature Statistics and Validation

```
1. Calculate feature statistics:
   - Descriptive statistics (mean, std, min, max, percentiles)
   - Distribution metrics (skewness, kurtosis)
   - Correlation matrix
   - Feature importance scores

2. Validate feature quality:
   - Check for data leakage (target info in features)
   - Verify no future data used in past predictions
   - Confirm no infinite or NaN values
   - Validate value ranges are sensible

3. Create feature correlation heatmap

4. Calculate feature stability metrics:
   - Feature distributions across time periods (if temporal data)
   - Population Stability Index (PSI) for key features
   - Expected value ranges for monitoring

5. Save statistics to results/metrics/{epic_id}_feature_stats.json

6. Create feature versioning metadata:
   - Feature set version number
   - Creation timestamp
   - Dependencies (data sources, package versions)
   - Git commit hash (if applicable)
   - Feature schema/registry entry
```

### Step 12: Verification

```
1. Verify all required outputs were created:
   - List files in notebooks/3_feature_engineering/{epic_id}/
   - List files in data/4_processed/{epic_id}/features/
   - Verify src/features/{epic_id}_feature_pipeline.py exists
   - Verify data/schemas/{epic_id}/feature_dictionary.md exists
   - Verify results/metrics/{epic_id}_feature_stats.json exists

2. Verify feature dataset quality:
   - Read feature dataset and check shape
   - Verify no missing values (or expected missing values only)
   - Verify correct number of features
   - Verify train/test split sizes are correct

3. Cross-check against user story acceptance criteria

4. Document verification results
```

## Feature Engineering Best Practices

### 1. Avoid Data Leakage
```
❌ Don't use future information to predict the past
❌ Don't use target variable to create features
❌ Don't include test data when fitting transformers
✅ Fit transformers on training data only
✅ Use time-aware splitting for time-series
✅ Create features using only past information
```

### 2. Handle Missing Values Properly
```
✅ Understand why data is missing (MCAR, MAR, MNAR)
✅ Choose appropriate imputation strategy
✅ Create missingness indicators if informative
✅ Document missing value handling
```

### 3. Scale Features Appropriately
```
✅ Scale features for distance-based algorithms
✅ Fit scaler on training data only
✅ Save scaler for consistent test/production transforms
✅ Choose scaling method based on distribution
```

### 4. Document Everything
```
✅ Feature name and description
✅ Creation logic and formula
✅ Transformation applied
✅ Assumptions made
```

### 5. Reduce Data Complexity
```
✅ Apply dimensionality reduction when dealing with high-dimensional data
✅ Use feature selection to keep only the most informative features
✅ Use clustering to group similar entities and reduce categorical cardinality
✅ Remove features with >95% correlation to others
✅ Eliminate near-zero variance features (variance < 0.01)
```

Complexity reduction improves model interpretability and prevents overfitting. Focus on retaining features that provide unique information and align with business objectives. Simpler feature sets often perform better and are easier to explain to stakeholders. Balance comprehensiveness with parsimony by systematically evaluating feature importance and removing those that add noise rather than signal.

### 6. Know When to Stop
```
✅ Stop when additional features show diminishing returns (<1% improvement)
✅ Stop when feature count exceeds interpretability threshold (>50-100 features)
✅ Stop when computational cost outweighs marginal gains
✅ Prioritize features that align with business objectives over marginal statistical improvements
```

Feature engineering has diminishing returns. The first 20 well-engineered features typically provide 80% of model performance. Additional features should demonstrate clear value through cross-validation or domain relevance. Consider the maintenance burden of complex feature pipelines in production environments.

## Quality Checks

After feature engineering, perform these quality checks:

### 1. Data Quality
```
- No missing values (unless expected and handled)
- No infinite values
- Correct data types (int, float, category)
- Value ranges are sensible and expected
```

### 2. Feature Quality
```
- Features capture domain knowledge
- Features show variation (not constant)
- Features are not highly redundant (correlation < 0.95)
- Features make logical sense
```

### 3. Pipeline Quality
```
- Pipeline is reusable and modular
- Pipeline can transform new data consistently
- Pipeline code is well-documented
- Pipeline handles edge cases (missing values, outliers)
```

### 4. Documentation Quality
```
- Feature dictionary is comprehensive
- Creation logic is clearly explained
- Assumptions are documented
- Transformation rationale is provided
```

## Error Handling

If feature engineering encounters issues:

1. **Write detailed error log** to `logs/errors/feature_engineering_{epic_id}_{timestamp}.log`

2. **Document the specific issue**:
   - Which feature creation failed
   - Error message and stack trace
   - Data quality issues discovered
   - Suggested remediation

3. **Partial Success**:
   - If some features created successfully, document which ones
   - Mark incomplete features clearly
   - Proceed with available features if acceptable

## Success Criteria

The feature engineering is considered successful when:

- ✅ All required features created and saved to `data/4_processed/{epic_id}/features/`
- ✅ Feature engineering notebooks created in `notebooks/3_feature_engineering/{epic_id}/`
- ✅ Feature dictionary documented in `data/schemas/{epic_id}/feature_dictionary.md`
- ✅ Feature statistics calculated and saved to `results/metrics/{epic_id}_feature_stats.json`
- ✅ Reusable feature pipeline created in `src/features/{epic_id}_feature_pipeline.py`
- ✅ Train/test splits created (if applicable)
- ✅ No data leakage detected
- ✅ Quality checks passed (data, feature, pipeline, documentation)
- ✅ Acceptance criteria from user story met
- ✅ All outputs verified

## Next Stage

After successful feature engineering, proceed to:
- **Model Training** stage: Train predictive or classification models
- **Statistical Analysis** stage: Perform hypothesis testing with engineered features
- **Visualization** stage: Create feature importance visualizations

## References

- Data Dictionary: `docs/data_dictionary/`
- User Story: `docs/objectives/user_stories/{epic_id}/`
- Project Structure: `README.md`
- Tech Stack: `docs/project_context/tech_stack.md`
