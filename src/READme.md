# Source Code

Here we describe some of the python modules in the src directory. 



## modeling/model_summary.py

### `ModelingUtilities`

A utility class for streamlined evaluation and comparison of multiple scikit-learn binary classification models.

#### Features

- **Batch model training**: Fit multiple models with one call
- **Automatic threshold optimization**: Find thresholds that maximize F-beta scores
- **Comprehensive metrics**: Average Precision, F-beta, Recall, Precision, ROC-AUC, Brier Score
- **Built-in visualizations**: Precision-Recall curves and confusion matrices
- **Method chaining**: Clean, readable workflow
- **Imbalanced data support**: Designed for rare event prediction

#### Quick Start
```python
from src.modeling.model_summary import ModelingUtilities

# 1. Initialize with models
models = {
    'random_forest': RandomForestClassifier(),
    'logistic_regression': LogisticRegression()
}
model_util = ModelingUtilities(dict_of_models=models)

# 2. Fit and evaluate with method chaining
model_util.fit_models(X_train, y_train) \
          .save_training_probabilities(X_train) \
          .save_test_probabilities(X_val, testing_type='validation')

# 3. Find optimal thresholds (maximizes F2 score for train data)
best_thresholds = model_util.get_train_best_fbeta_thresholds(y_train, beta=2)

# 4. Get comprehensive metrics
metrics = model_util.get_metrics(y_val, beta=2, return_dataframe=True)
print(metrics)

# 5. Visualize results
model_util.plt_precision_recall_curve(y_val, beta=2, save_to='pr_curve.png')
model_util.create_confusion_matrix(y_val, beta=2, save_to_dir='results/')
```

#### Key Methods

| Method | Purpose |
|--------|---------|
| `fit_models(X_train, y_train)` | Train all models |
| `save_test_probabilities(X_val, testing_type)` | Generate predictions |
| `get_train_best_fbeta_thresholds(y_train, beta)` | Find optimal thresholds for TRAIN data |
| `get_metrics(y_data, beta, return_dataframe)` | Compute all metrics |
| `plt_precision_recall_curve(y_val, beta, save_to)` | Plot PR curves |
| `create_confusion_matrix(y_val, beta, save_to_dir)` | Generate confusion matrices |

##### Helper Function
```python
from src.modeling.model_summary import train_val_model_metrics_df

# Quick train/validation comparison
data_dict = {
    'train': {'X': X_train, 'y': y_train},
    'validation': {'X': X_val, 'y': y_val}
}

metrics_df = train_val_model_metrics_df(models_dict=models, data_dict=data_dict)
```

## pipeline/transformers.py

Custom scikit-learn transformers for meteorological feature engineering.

### `HourlyRates`

Calculate hourly rate of change for meteorological variables.

**Parameters:**
- `columns`: List of columns to compute rates for
- `min_gap_hours`: Minimum time gap to consider
- `max_gap_hours`: Maximum time gap to consider

**Example:**
```python
transformer = HourlyRates(
    columns=['TMP_air_temperature', 'DEW_dew_point'],
    min_gap_hours=1,
    max_gap_hours=2
)
X_transformed = transformer.fit_transform(X)
```

### `DatetimeSinCosConverter`

Create cyclic temporal features from datetime.

**Parameters:**
- `column`: Datetime column name
- `monthofyear`: Create month features
- `dayofyear`: Create day-of-year features
- `hourofday`: Create hour features

### `DewTempSpread`

Calculate temperature - dewpoint spread (atmospheric stability indicator).

### Other Transformers

See docstrings in `transformers.py` for:
- `ReplaceValuesWithNaN`
- `CalmWindFixer`
- `DropNaNRows`
- `NaNReplacement`
- `DropColumns`
- `DropDuplicates`

All transformers are sklearn-compatible with `.fit()` and `.transform()` methods.