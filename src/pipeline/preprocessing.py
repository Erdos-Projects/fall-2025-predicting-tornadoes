from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn import set_config
set_config(transform_output="pandas")
import numpy as np
import pandas as pd

from src.pipeline.transformers import (
    ReplaceValuesWithNaN,
    CalmWindFixer,
    DropNaNRows,
    NaNReplacement,
    DirectionAngleReplacement,
    DropColumns,
    DropDuplicates
)


# Replace particular values to NaN (see eda)
isd_col_nan_vals = {
	'CIG- Sky Condition Observation- Ceiling Height Dimension' : [99999],

	'CIG- Sky Condition Observation- Ceiling Quality Code' : [3,7],

	'CIG- Sky Condition Observation- Ceiling Determination Code' : ['9'],

	'CIG- Sky Condition Observation- Cavok Code' : ['9'],

	'DEW- Air Temperature Observation- Dew Point Temperature' : [9999],

	'DEW- Air Temperature Observation- Dew Point Quality Code' : ['3','7'],

	'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate' : [99999],

	'MA1- Atmospheric Pressure Observation- Altimeter Quality Code' : [3,7],

	'MA1- Atmospheric Pressure Observation- Station Pressure Rate' : [99999],

	'MA1- Atmospheric Pressure Observation- Station Pressure Quality Code' : [3,7],

	'SLP- Atmospheric Pressure Observation- Sea Level Pressure' : [99999],

	'SLP- Atmospheric Pressure Observation- Sea Level Pressure Quality Code' : [3,7],

	'TMP- Air Temperature Observation- Air Temperature' : [9999],

	'TMP- Air Temperature Observation- Air Temperature Quality Code' : ['3','7'],

	'VIS- Visibility Observation- Distance Dimension' : [999999],

	'VIS- Visibility Observation- Distance Quality Code' : ['3','7',3,7],

	'VIS- Visibility Observation- Variability Code' : ['9'],

	'VIS- Visibility Observation- Quality Variability Code' : ['3','7',3,7],

	'WND- Wind Observation- Direction Angle' : [999],

	'WND- Wind Observation- Direction Quality Code' : [3,7],

	'WND- Wind Observation- Type Code' : [9],

	'WND- Wind Observation- Speed Rate' : [9999],

	'WND- Wind Observation- Speed Quality Code' : [3,7]

}
to_nan = ColumnTransformer(
    transformers = 
    [
        (f'{col} Replace with NaN', ReplaceValuesWithNaN(val),[col])
        for col,val in isd_col_nan_vals.items()
    ],
    remainder = 'passthrough',
    verbose_feature_names_out=False
)

# features to use in DropNaNRows
dropnacols = [
'DEW- Air Temperature Observation- Dew Point Temperature',
'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate',
'MA1- Atmospheric Pressure Observation- Station Pressure Rate',
'SLP- Atmospheric Pressure Observation- Sea Level Pressure',
'TMP- Air Temperature Observation- Air Temperature',
'VIS- Visibility Observation- Distance Dimension',
'WND- Wind Observation- Speed Rate',
'CIG- Sky Condition Observation- Ceiling Quality Code',
'CIG- Sky Condition Observation- Cavok Code',
'DEW- Air Temperature Observation- Dew Point Quality Code',
'MA1- Atmospheric Pressure Observation- Altimeter Quality Code',
'MA1- Atmospheric Pressure Observation- Station Pressure Quality Code',
'SLP- Atmospheric Pressure Observation- Sea Level Pressure Quality Code',
'TMP- Air Temperature Observation- Air Temperature Quality Code',
'VIS- Visibility Observation- Distance Quality Code',
'VIS- Visibility Observation- Quality Variability Code',
'VIS- Visibility Observation- Variability Code',
'WND- Wind Observation- Direction Quality Code',
'WND- Wind Observation- Speed Quality Code',
]


# 'CIG- Sky Condition Observation- Ceiling Height Dimension' NaN replacement




na_imputer = Pipeline(
    [
        ('Calm Wind NaN Replacement', CalmWindFixer()),
        ('Drop NaN Row', DropNaNRows(columns = dropnacols)),
        ('Ceiling Height Dim Replacement', NaNReplacement(
            column= 'CIG- Sky Condition Observation- Ceiling Height Dimension',
            value= 22000
            )
        ),
        ('Direction Angle Replacement',DirectionAngleReplacement())
    ]
    
)

# Scale numeric features to proper value as per ISD Documentation
numeric_scale =  ColumnTransformer(
    transformers = [
        (
            'Scale by 1/10',
            FunctionTransformer(lambda X: X*(1/10)),
            ['DEW- Air Temperature Observation- Dew Point Temperature',
            'TMP- Air Temperature Observation- Air Temperature',
            'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate',
            'MA1- Atmospheric Pressure Observation- Station Pressure Rate',
            'SLP- Atmospheric Pressure Observation- Sea Level Pressure',
            'WND- Wind Observation- Speed Rate']
        )
            ],
    remainder= 'passthrough',
    verbose_feature_names_out=False
)

# columns to drop (preprocessing)


# preprocessing pipeline

columns_to_drop =[
    'CIG- Sky Condition Observation- Ceiling Quality Code',
    'CIG- Sky Condition Observation- Cavok Code',
    'DEW- Air Temperature Observation- Dew Point Quality Code',
    'MA1- Atmospheric Pressure Observation- Altimeter Quality Code',
    'MA1- Atmospheric Pressure Observation- Station Pressure Quality Code',
    'SLP- Atmospheric Pressure Observation- Sea Level Pressure Quality Code',
    'TMP- Air Temperature Observation- Air Temperature Quality Code',
    'VIS- Visibility Observation- Distance Quality Code',
    'VIS- Visibility Observation- Quality Variability Code',
    'VIS- Visibility Observation- Variability Code',
    'WND- Wind Observation- Direction Quality Code',
    'WND- Wind Observation- Speed Quality Code',
    'CIG- Sky Condition Observation- Ceiling Determination Code'
        ]

preprocessing = Pipeline([
    ('Values to NaN', to_nan),
    ('NaN Imputer', na_imputer),
    ('Drop Columns PreSplit',DropColumns(columns=columns_to_drop)),
    ('Drop Duplicates', DropDuplicates()),
    ('Scale Columns',numeric_scale)
    ])

