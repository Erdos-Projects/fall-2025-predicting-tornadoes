# Load in merged data frame 
# copied and pasted from Data/Data Scripts/merge_station_and_event_data_script.py

import pandas as pd
import numpy as np
import os
import math



# Note: In the documentation (isd-format-document.pdf) sometimes a number 
# stands in for a nan value. We will deal with that if we choose such a 
# feature later on.

def split_tuple_features(df: pd.DataFrame,
                        mapping: dict = None,
                        drop_originals:bool =False,
                        tuple_sep:str =None) -> pd.DataFrame:
    """
    Splits specified tuple‐columns into separate descriptive columns.
    Args:
    df : pandas.DataFrame — your data.
    mapping : dict — key = column name, value = list of new sub‐column names.
    drop_original : bool — if True, drop the original tuple column after splitting.
    tuple_sep : str or None — if the tuple is stored as a string with a separator, provide the separator (e.g., ",").
    
    Returns:
    A new pandas DataFrame with the expanded columns.
    """
    def split_function(val,i:int):
        if mapping is None:
            return df
    
        if pd.isna(val):
            return np.nan
        elif isinstance(val,tuple):
            return val[i]
        elif isinstance (val,str):
            return val.split(tuple_sep)[i]
        else:
            print(f'Problem with {val}')
            return val
        
    for original_col, new_cols in mapping.items():
        for i in range(0,len(new_cols)):
            df[new_cols[i]] = df[original_col].apply(lambda row : split_function(row,i))
        if drop_originals:
            df.drop(columns=[original_col],inplace=True)
        else:
            pass
        
    
    return df



def clean_station_data(
    raw_dir:str='Data/stations/raw',
    drop_cols:list[str] = None,
    split_tuples:bool = False,
    mapping: dict = None,
    drop_originals:bool =False,
    tuple_sep:str =None
):
    # Step 1: Read in each station csv and concatenate all.


    raw_station_data = os.listdir(raw_dir) # list files in directory

    station_csv_files = [file for file in raw_station_data if ('.csv' in file) and ('Station' in file)] # get csv files

    station_dfs=[pd.read_csv(f"{raw_dir}/{file}").copy() for file in station_csv_files]
    stations_df = pd.concat(station_dfs, axis = 0)
    merged = stations_df.reset_index().drop(['index', 'Unnamed: 0'], axis =1).copy() 

    # Step 2: Values in the 'DATE' feature are of the form 2000-01-01T00:00:00. 
    # Split these into 'YEAR-MONTH-DAY' and 'TIME' features for each DataFrame
    # in station_dfs.


    merged['YEAR-MONTH-DAY'] = merged['DATE'].apply(lambda r: r.split('T')[0])
    merged['TIME'] = merged['DATE'].apply(lambda r: r.split('T')[1])
    merged.drop(['DATE'],axis=1,inplace=True)
    
    # Step 3: A column name change
    rename = {
            'LATITUDE' : 'STATION_LAT',
            'LONGITUDE' : 'STATION_LON',
            'TIME': 'STATION_TIME'
        }
    
    merged.rename(columns= rename, inplace= True)
    

    
    # Step 4 Drop unnecessary columns
    
    if drop_cols is None:
        pass
    else:
        merged.drop(columns=drop_cols, inplace = True)
    
    # Step 5 Split Columns
    
    if not split_tuples:
        pass
    
    else: 
        merged = split_tuple_features(merged, mapping, drop_originals, tuple_sep)

    
    
    return merged













