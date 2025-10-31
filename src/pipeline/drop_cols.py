from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn import set_config
set_config(transform_output="pandas")
import numpy as np
import pandas as pd

from src.pipeline.transformers import (
    DropColumns
)

# Pre Train-Test Split
# Definitely needs to happen data leakage
pre_cols_to_drop =[
    'TORNADO_BEGIN_DATE_TIME',
    'TORNADO_END_DATE_TIME',
    'TORNADO_BEGIN_LAT',
    'TORNADO_BEGIN_LON',
    'TORNADO_END_LAT',
    'TORNADO_END_LON',
    'TORNADO_INITIAL_DISTANCE_FROM_STATION',
    'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_50_km',
]

pre_split_drop = Pipeline([
    ("Pre Train-Test split drops", DropColumns(columns = pre_cols_to_drop))
])

# Post Train-Test Split

# Definitely needs to happen d object type/ redundant
# given other features/ 
post_cols_to_drop=[
    'STATION_LON',
    'STATION_LAT',
    'WND- Wind Observation- Type Code',
    'SLP- Atmospheric Pressure Observation- Sea Level Pressure',
    'TMP- Air Temperature Observation- Air Temperature' 
]

post_cols_to_drop = Pipeline([
    ("Post Train-Test split drops", DropColumns(columns = post_cols_to_drop))
])

# Optional test after baseline
# Current thoughts on columns to drop that aren't required 
op_post_cols_to_drop = [
    'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate'
    'WND- Wind Observation- Speed Rate'
    'WND- Wind Observation- Direction Angle',
    'VIS- Visibility Observation- Distance Dimension',
    'CIG- Sky Condition Observation- Ceiling Height Dimension',
    'WND- Wind Observation- Speed Rate',
    'WND- Wind Observation- Direction Angle',
    'STATION_DATE_TIME',
]

op_cols_to_drop = Pipeline([
    ("Post Train-Test split optional drops", DropColumns(columns = op_post_cols_to_drop))
])