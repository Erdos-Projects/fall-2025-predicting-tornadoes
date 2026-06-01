# Predicting Tornadoes in Oklahoma City

## Table of Contents

1. [A Brief Overview](#a-brief-overview)
2. [An Important Assumption](#an-important-assumption)
3. [Project Results](#project-results)
4. [Project Structure](#project-structure)
5. [Data Sources](#data-sources)
6. [How to Run This Project](#how-to-run-this-project)
7. [Methodology](#methodology)
8. [Notebooks](#notebooks)
9. [Requirements](#requirements)
10. [Future Work](#future-work)
11. [Author](#author)
12. [Acknowledgements](#acknowledgments)

### A Brief Overview

Oklahoma City (OKC) is in the heart of tornado ally and known for its frequency and strength of tornadoes. This project uses a scikit-learn RandomForestClassifier to predict tornado occurrence in (OKC) given current meteorological conditions with **only** surface data obtained from local weather stations (**no radar data**) . This work demonstrates:

- Rigorous temporal cross-validation to prevent data leakage
- Feature engineering incorporating meteorological domain knowledge
- Handling extreme class imbalance (0.15% tornado rate)


### An Important Assumption

**ASSUMPTION:** All validation and testing thresholds computed for models in this project are chosen as the threshold that yields the best F2 score for the training data. 


### Project Results

| Split | AP | F2 | Recall | Precision | ROC-AUC |
|-------|----|----|--------|-----------|---------|
| **Validation** (2018-2019) |0.07979 |0.091408 | 8.5% |12.6% | .904	 |
| **Test** (2020-2021) | 0.006182	 | 0% | 0%| 0.024558% | 0.918553 |

**Key Finding:** Severe temporal degradation (12.9x AP drop) demonstrates the challenge of distribution shift in meteorological prediction. The 0% recall and 0% precision represents a complete inversion of signal demonstrating that patterns learned from historical data (2000-2019) not only failed to generalize to the model but actively misled the model in testing. 


#### Key Learnings

1) **Temporal distribution shifts**: Atmospheric patterns shifted between training (2000-2019) and test (2020-2021) periods.
2) **Extreme class imbalance**: 0.15% tornado rate amplifies impact of distribution shifts
3) **Reliance on Seasonality and Time of Day**: Our model rely too heavily on what month it is and time of day. The test set had   more tornadoes in October than in May; moreover, there were 6 tornadoes in both January months for our test sets-- double the total January tornadoes for our training set.
4) **Limited feature set**: Surface weather observations alone provide insufficient signal. Future project may want to utilize radar data too. 


### Data Sources

1) Station Data Sources:
    * NOAA Integrated Surface Database (ISD) was accessed on October 7th, 2025 from https://registry.opendata.aws/noaa-isd. See [Data README.md](data/README.md) for more information.
2) Storm Event Data Source:
    * NOAA National Centers for Environmental Information. Storm Events Database. Accessed on October 6th, 2025 from: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/. See [Data README.md](data/README.md) for more information.


### How to Run This Project

#### Prerequisites

**Python 3.12** (or 3.10+)

#### Installation

1. **Clone the repository:**
```bash
   git clone <your-repo-url>
   cd <project-directory>
```

2. **Create and activate conda environment:**
```bash
   conda env create -f environment.yml
   conda activate <env-name>
```


#### Quick Start (Skip Data Processing)

The processed data is already included. You can jump straight to modeling:

**Recommended sequence:**
1. `eda.ipynb` - Exploratory data analysis
2. `baseline_modeling.ipynb` - Initial model comparison
3. `modeling_and_feature_eng.ipynb` - Feature engineering experiments
4. `final_results.ipynb` - Hyperparameter tuning and final testing

**Key data files (already included):**
- `data/final_cleaned/final.csv` - Complete processed dataset
- `data/train_val_test_splits/` - Pre-split train/val/test sets

#### Full Pipeline (Including Data Processing)

If you want to reproduce from raw data:

**Note:** Raw weather station and tornado event data are included in:
- `data/stations/raw/` - NOAA ISD weather station data
- `data/events/raw/` - NOAA Storm Events tornado reports

To reprocess from scratch, run the cleaning scripts in `src/cleaning/`:
```bash
# From project root
python src/cleaning/interim_station_data.py
python src/cleaning/processed_station_data.py
python src/cleaning/clean_events.py
python src/cleaning/merged_tornado_indicator.py
```

Then run the notebooks as described above.

#### Using the Trained Model

The final trained model is saved in `models/`:
```python
import joblib
import json

# Load model
model = joblib.load('models/final_model.joblib')

# Load metadata (threshold, hyperparameters)
with open('models/model_metadata.json', 'r') as f:
    metadata = json.load(f)
    threshold = metadata['decision_threshold']

# Make predictions on new data
probabilities = model.predict_proba(X_new)[:, 1]
predictions = (probabilities >= threshold).astype(int)
```

#### Project Structure
```
├── data/                          # All data files
│   ├── final_cleaned/            # ← Start here: final.csv
│   ├── train_val_test_splits/    # Pre-split data
│   ├── stations/                 # Weather station data (raw/interim/processed)
│   └── events/                   # Tornado event data
├── notebooks/                     # Analysis notebooks (run in order)
│   ├── eda.ipynb
│   ├── baseline_modeling.ipynb
│   ├── modeling_and_feature_eng.ipynb
│   └── final_results.ipynb
├── src/                          # Custom modules
│   ├── modeling/                 # Model utilities, CV splitters
│   ├── pipeline/                 # Custom transformers
│   └── cleaning/                 # Data processing scripts
├── models/                       # Trained models
│   ├── final_model.joblib
│   └── model_metadata.json
└── results/                      # Figures and metrics
```

#### Expected Runtime

- **EDA notebook:** ~5 minutes
- **Baseline modeling:** ~10-15 minutes
- **Feature engineering:** ~15-20 minutes
- **Final results (with GridSearchCV):** approximately 10 hours ( I don't reccomend running the second grid search- see [second grid search](results/cv_parameter_search/random_forest/second_grid_search_results.csv) instead)

**Note:** All GridSearchCV's in `final_results.ipynb` are computationally intensive- especially the second. Results are already saved in `results/final_model/`


### Methodology

#### Temporal Validation Strategy

To prevent data leakage in time series prediction:
- **Training:** 2000-2017 (17 years)
- **Validation:** 2018-2019 (2 years)
- **Test:** 2020-2021 (2 years)

Cross-validation used expanding window strategy with temporal folds whose validation sets all have 2 years of data.

#### Feature Engineering

1. **Temporal Cyclic Encoding:** Sin/cos transformation of month and hour
2. **Hourly Rates of Change:** Rate of change for temperature, pressure, dew point. (NOT USED IN FINAL MODEL)
3. **Dew Point Spread:** Temperature minus dew point (atmospheric stability indicator)

#### Model Selection

Random Forest with:
- "max_depth": 10,
- "max_features": "sqrt",
- "max_samples": 0.3,
- "min_samples_leaf": 20,
- "min_samples_split": 50,
- "n_estimators": 100,
- "class_weight": "balanced",
- "random_state": 42
- Isotonic calibration for probability estimates


### Notebooks

1. **`eda.ipynb`** - Raw data processing and cleaning 
2 **`baseline_modeling.ipynb`** - Initial model comparison and validation strategy
3. **`modeling_and_feature_eng.ipynb`** - Feature creation and systematic evaluation
4. **`final_results.ipynb`** - Hyperparameter tuning and final testing


### Future Work

- Incorporate radar-derived features (rotation signatures, hook echoes)
- Explore domain adaptation techniques for temporal distribution shifts that are robust against seasonal patterns.
- Ensemble methods combining models from different time periods.

### Author

**Taylor Murray**


**Context:** Capstone project for Erdős Institute Data Science Boot Camp, Fall 2025


### Acknowledgments

- NOAA for ISD weather data
- Erdős Institute for project guidance
- Storm Prediction Center for tornado reports

 
