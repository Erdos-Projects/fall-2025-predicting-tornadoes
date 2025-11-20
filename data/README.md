
# Data Documentation

## Data Sources

1) Station Data Sources:
    * NOAA Integrated Surface Database (ISD). Accessed on October 7th, 2025 from https://registry.opendata.aws/noaa-isd.
    * Used data from stations: 99999903954, 72357099999, 72357003948, 99999903948, 72354013919, 72354403954, 72354499999, 72353013967, 72354099999.
2) Storm Event Data Source:
    * NOAA National Centers for Environmental Information. Storm Events Database. Accessed on October 6th, 2025 from: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/. Downloaded the following files.

        - StormEvents_details-ftp_v1.0_d{year}_c########.csv.gz	for year =2000,...,2021.
    	


## (OPTIONAL) Download Instructions for Station Data Sources

The Raw ISD Station downloaded from the NOAA ISD had to be split into separate csv files (see [data/stations/raw](data/stations/raw))in order to be placed into the repository. To perform this splitting see [src/data/acquisition/split_data.py](../src/data/acquisition/split_data.py). While this data is in the repository, if you would like to download this data on your own:

1) Travel to https://www.ncei.noaa.gov/access/search/data-search/global-hourly.

2) Request all data from Oklahoma City from January 1st, 2000 to December 31st, 2021.

3) Follow directions on webpage.

4) You should receive an email shortly containing a download lnk for the data.


## Folder Tree (Level 2)
```
.
├── __init__.py
├── __pycache__
│   └── __init__.cpython-312.pyc
├── event_station_indicator
│   ├── TOR_INDICATOR_Station_72353013967_Part_1.csv 
│   ├ ...
├── events
│   ├── interim     
│   ├── processed
│   ├── raw
│   ├── storm_events_scraping.bash
│   └── Storm-Data-Bulk-csv-Format.pdf
├── final_cleaned
│   └── final.csv
├── metadata
│   ├── __init__.py
│   ├── __pycache__
│   └── cleaned_feature_info.py
├── README.md
├── stations
│   ├── __pycache__
│   ├── CSV_HELP.pdf
│   ├── interim
│   ├── isd-format-document.pdf
│   ├── processed
│   ├── raw
│   └── README_station_data.md
└── train_val_test_splits
    ├── test_data
    ├── train_data
    └── val_data
```

## Data Transformations

In the above tree there are a lot of datasets floating around. Here is a brief overview of them. The csv file [final.csv](final_cleaned/final.csv) is all that is needed to run the modeling notebooks (except for the eda notebook- these require the csv files in the event_station_indicator folder).



### Events

* raw = raw storm event data per year scraped with `storm_events_scraping.bash`.
* interim + processsed = run [src/cleaning/clean_events.py](../src/cleaning/clean_events.py)
    - filters oklahoma tornadoes  

### Stations

* raw = raw station events from ISD.
* processed = run [src/cleaning/interim_station_data.py](../src/cleaning/interim_station_data.py)
    - Removes a number of features from station data (see py script for more details.)
* cleaned = run [src/cleaning/processed_station_data.py](../src/cleaning/processed_station_data.py)
    - Parses ISD columns; these are strings of comma seperated values that need to be cleaned for modeling and eda.

### Event Station Indicator

* Glues together cleaned event data and cleaned station data using [src/cleaning/merged_tornado_indicator.py](../src/cleaning/merged_tornado_indicator.py)
    - This data is read into eda notebook.

### Final Data
* Event Station Indicator data is read into eda and cleaned in this notebook. The final result is saved to [final.csv](final_cleaned/final.csv).

### Train_Val_Test Splits

* These are the trian-validation-test splits done in the beginning of [notebooks/baseline_modeling.ipynb](../notebooks/baseline_modeling.ipynb).

## Final Data Schema

### Processed Data (`final.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `STATION` | str | Weather station ID |
|`LATITUDE`|float| Latitude of weather station|
|`LONGITUDE`|float| Longitude of weather station|
|`ELEVATION`|float| Elevation of weather station|
| `DATE` | datetime | Observation timestamp |
| `TMP_air_temperature` | float | Air temperature (°C) scaled by 10|
| `DEW_dew_point` | float | Dew point temperature (°C) scaled by 10 |
| `SLP_sea_level_pressure` | float | Sea level pressure (hPa)scaled by 10 |
| `WND_speed_rate` | float | Wind speed (m/s) scaled by 10 |
| `WND_direction_angle` | float | Wind direction (degrees) |
| `WND_type_code` | str | Wind observation type |
| `CIG_ceiling_height` | float | Cloud ceiling (m) |
|`CIG_cavok_code`|str| CAVOK Code|
|`VIS_variability_code`|str| Visibility variability code|
| `VIS_distance` | float | Visibility (m) |
|`WND_direction_angle_variable_wind_direction_flag`| bool| Indicates variable wind direction|
| `TORNADO_OCCURRENCE` | bool | Target: tornado within 1 hour |



## Final Data Characteristics

- **Total samples:** 454,050 observations
- **Temporal coverage:** 2000-2021 (22 years)
- **Spatial coverage:** Oklahoma City and surrounding area.

## Tornado Labels

Tornado occurrence labels derived from:
- **NOAA Storm Event Data**
- Matched to weather station observations via:
  - Spatial proximity (within 75km)
  - Temporal window (+/-3 hour)

## Data Quality Notes

1. **Missing values:** Handled via median imputation for numeric features
2. **Calm winds:** NaN wind direction set to 'C' when speed = 0
3. **Outliers:** Retained (legitimate extreme weather events)
4. **Temporal gaps:** Some stations have irregular reporting intervals