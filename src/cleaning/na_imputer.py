import pandas as pd
import os 
import sys
import numpy as np
from src.cleaning.merged_tornado_indicator import create_tornado_indicator


# All of this is code from the eda notebook

def impute_missing_values(time_window =1,val_radius=50):
    """ Reads in the mreged station-event dataset, imputes missing values,
    and returns the cleaned DataFrame."""
    

    data = create_tornado_indicator(
                                    drop_originals=True, 
                                    tuple_sep=',',
                                    time_window =time_window,
                                    val_radius=val_radius)
    
    
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

# Apply ISD conventions
    for col, vals in isd_col_nan_vals.items():
        data[col].replace(to_replace=vals, value= np.nan,inplace = True)
        for val in vals:
            assert((data[col][data[col]==val]).sum()==0) #make sure changes are implemented
    
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
        'WND- Wind Observation- Speed Quality Code'
        ]

    data.dropna(subset=quality_code_feats,inplace=True)

    for col in quality_code_feats:
        assert(data[col].isna().sum() ==0) # make sure there are no nan values in quality_code_feats
        
        
    # Drop Rows with NaN's in the following columns
    drop_nas = ['DEW- Air Temperature Observation- Dew Point Temperature',
            'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate',
            'MA1- Atmospheric Pressure Observation- Station Pressure Rate',
            'SLP- Atmospheric Pressure Observation- Sea Level Pressure',
            'TMP- Air Temperature Observation- Air Temperature',
            'VIS- Visibility Observation- Distance Dimension',
            'WND- Wind Observation- Speed Rate'
            ]
    data.dropna(subset=drop_nas,inplace =True)



    # 'CIG- Sky Condition Observation- Ceiling Height Dimension' NaN replacement

    data['CIG- Sky Condition Observation- Ceiling Height Dimension'] = data['CIG- Sky Condition Observation- Ceiling Height Dimension'].fillna(22000)

    # 'WND- Wind Observation- Direction Angle' NaN replacement

    direction_angle_na_mask = data['WND- Wind Observation- Direction Angle'].isna()
    typecode_C_mask = (data['WND- Wind Observation- Type Code'] != 'C')


    neg2_mask = ((direction_angle_na_mask) & (typecode_C_mask))

    neg2_index = data[neg2_mask].index
    data.drop(index= neg2_index, inplace=True)

    ####### Check 
    direction_angle_na_mask = data['WND- Wind Observation- Direction Angle'].isna()
    typecode_C_mask = (data['WND- Wind Observation- Type Code'] != 'C')



    neg2_mask = ((direction_angle_na_mask) & (typecode_C_mask))
    assert(neg2_mask.sum()==0)

    ####### End Check


    #  Drop 'CIG- Sky Condition Observation- Ceiling Determination Code' as it is metadata
    data.drop(columns=['CIG- Sky Condition Observation- Ceiling Determination Code'], inplace=True)


    
    return data