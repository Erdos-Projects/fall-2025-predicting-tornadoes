import pandas as pd
import os 
import sys
import numpy as np



quality_code_feats = [
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


def drop_quality_code_features(data:pd.DataFrame,features_to_drop =quality_code_feats):
    data = data.copy().drop(columns=quality_code_feats,inplace=False)
    return data