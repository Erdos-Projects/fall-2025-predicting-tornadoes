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



def pre_split_drop(pre_cols_to_drop= None):
    """
    Returns pipeline that drops columns from pre_cols_to_drop
    Args:
        pre_cols_to_drop: columns to drop. Defaults to None, but when 
        this is the case, once the function is called 
        pre_cols_to_drop= [
        'TORNADO_BEGIN_DATE_TIME',
        'TORNADO_END_DATE_TIME',
        'TORNADO_BEGIN_LAT',
        'TORNADO_BEGIN_LON',
        'TORNADO_END_LAT',
        'TORNADO_END_LON',
        'TORNADO_INITIAL_DISTANCE_FROM_STATION',
        'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_50_km',
        ].
    """
    # Definitely needs to be dropped- data leakage
    nec_to_drop =[
        'TORNADO_BEGIN_DATE_TIME',
        'TORNADO_END_DATE_TIME',
        'TORNADO_BEGIN_LAT',
        'TORNADO_BEGIN_LON',
        'TORNADO_END_LAT',
        'TORNADO_END_LON',
        'TORNADO_INITIAL_DISTANCE_FROM_STATION',
        'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_50_km',
        ]
    if pre_cols_to_drop is None:
        pre_cols_to_drop = nec_to_drop
    else:
        pre_cols_to_drop = list(set(nec_to_drop+pre_cols_to_drop))
        
    return  Pipeline([("Pre Train-Test split drops", DropColumns(columns = pre_cols_to_drop))
    
])

# Post Train-Test Split



def post_split_drop(post_cols_to_drop = None):
    # Definitely needs to be dropped because of  type or redundant
    # given other features
    necessary_to_drop = [
        'STATION',
        'WND- Wind Observation- Type Code',
        'STATION_DATE_TIME'
        ]  
    if post_cols_to_drop is None:
        post_cols_to_drop = necessary_to_drop
    
    else:
        # add necessary columns no repeats.
        post_cols_to_drop = list(set(post_cols_to_drop + necessary_to_drop))
    
    return Pipeline([
        ("Post Train-Test split drops", DropColumns(columns = post_cols_to_drop))
        ])

\




