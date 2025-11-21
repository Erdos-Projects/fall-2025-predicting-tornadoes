# Executive Summary Document

##A Brief Overview

Oklahoma City (OKC) is in the heart of tornado ally and known for its frequency and strength of tornadoes. This project uses a scikit-learn RandomForestClassifier to predict tornado occurrence in (OKC) given current meteorological conditions with **only** surface data obtained from local weather stations (**no radar data**) . This work demonstrates:

- Rigorous temporal cross-validation to prevent data leakage
- Feature engineering incorporating meteorological domain knowledge
- Handling extreme class imbalance (0.15% tornado rate)


## Data Sources

1) Station Data Sources:
    * NOAA Integrated Surface Database (ISD) was accessed on October 7th, 2025 from https://registry.opendata.aws/noaa-isd. See [Data README.md](data/README.md) for more information.
2) Storm Event Data Source:
    * NOAA National Centers for Environmental Information. Storm Events Database. Accessed on October 6th, 2025 from: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/. See [Data README.md](data/README.md) for more information.

## An Important Assumption

**ASSUMPTION:** All validation and testing thresholds computed for models in this project are chosen as the threshold that yields the best F2 score for the training data. 

## Key Performance Indicators

**Primary Key Performance Indicator**
1. Average Precision (PR-AUC)

**Secondary Key Performance Indicators**
2. F2-Score
3. Recall
4. ROC-AUC
5. Precision


## Chosen Model (Metadata.json)
```json
{
  "model_type": "RandomForestClassifier",
  "training_data": {
    "start_date": "2000-01-01",
    "end_date": "2019-12-31",
    "n_samples": 563033,
    "n_features": 16,
    "tornado_rate": 0.0015469785962812126
  },
  "hyperparameters": {
    "max_depth": 10,
    "max_features": "sqrt",
    "max_samples": 0.3,
    "min_samples_leaf": 20,
    "min_samples_split": 50,
    "n_estimators": 100,
    "class_weight": "balanced",
    "random_state": 42
  },
  "decision_threshold": 0.04591873420428021,
  "threshold_tuning": {
    "tuned_on": "training set (2000-2019)",
    "metric": "Best F2 score",
    "best_train_f2": 0.40956682406076783
  },
  "feature_engineering": [
    "HourlyRates (DEW, TMP, SLP)",
    "DatetimeSinCosConverter (month, hour)",
    "Dropped: [CIG_cavok_code",
    "VIS_variability_code",
    "WND_type_code",
    "WND_direction_angle_variable_wind_direction_flag"
  ],
  "preprocessing": "TC_HR_preprocessor",
  "calibration": {
    "method": "isotonic",
    "cv": "YearlyTemporalWindowSplit(end_year=2019, start_year=2002, val_window_size=2)"
  }
}
```


## Results

| Split | AP | F2 | Recall | Precision | ROC-AUC |
|-------|----|----|--------|-----------|---------|
| **Validation** (2018-2019) |0.07979 |0.091408 | 8.5% |12.6% | .904	 |
| **Test** (2020-2021) | 0.006182	 | 0% | 0%| 0.024558% | 0.918553 |

**Key Finding:** Severe temporal degradation (12.9x AP drop) demonstrates the challenge of distribution shift in meteorological prediction. The 0% recall and 0% precision represents a complete inversion of signal demonstrating that patterns learned from historical data (2000-2019) not only failed to generalize to the model but actively misled the model in testing. 


### Key Learnings/Limitations

1) **Temporal distribution shifts**: Atmospheric patterns shifted between training (2000-2019) and test (2020-2021) periods.
2) **Extreme class imbalance**: 0.15% tornado rate amplifies impact of distribution shifts
3) **Reliance on Seasonality and Time of Day**: Our model rely too heavily on what month it is and time of day. The test set had   more tornadoes in October than in May; moreover, there were 6 tornadoes in both January months for our test sets-- double the total January tornadoes for our training set.
4) **Limited feature set**: Surface weather observations alone provide insufficient signal. Future project may want to utilize radar data too. 






## Future Work

1. **Investigate Temporal Distribution Shift Through Ensemble Methods:**

The significant validation→test performance drop  reveals temporal non-stationarity in tornado formation patterns. Future work should explore ensemble approaches that combine models trained on different **seasonal** periods to create more robust predictions across distributional shifts. In addition, we should also take into account the **time of day** in dealing with temporal distribution-- we saw in our EDA that Tornadoes are more common in early afternoon, but this need not always be the case.

2. **Incorporate Radar and Satellite Data**

Current features are limited to surface weather station measurements (temperature, pressure, dewpoint, ect...). Integrating Doppler radar data—particularly mesocyclone detection, hook echo patterns, and reflectivity values—could dramatically improve tornado prediction accuracy. 
