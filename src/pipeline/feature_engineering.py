from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn import set_config
set_config(transform_output="pandas")
import numpy as np
import pandas as pd

from src.pipeline.transformers import (
    GrabYear,
    DatetimeSinCosConverter,
    SubtractColumns
)

# Pre Train-Test Split

pre_train_test_split_FE = Pipeline(
    [
        ("Make year column", GrabYear(column ='STATION_DATE_TIME', new_col ='year')),
        ("Sine/Cosine columns", DatetimeSinCosConverter(column= 'STATION_DATE_TIME',
                                                        monthofyear=True,
                                                        dayofyear=True,
                                                        hourofday=True)),
        ("TMP-DEW", SubtractColumns(col_1 = 'TMP- Air Temperature Observation- Air Temperature',
                                    col_2 ='DEW- Air Temperature Observation- Dew Point Temperature',
                                    new_col='TMP-DEW'))
    ]
)

