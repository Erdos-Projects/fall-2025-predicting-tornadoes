from src.cleaning.clean_stations import clean_station_data
import pandas as pd
import numpy as np

def merge_station_events(
    event_file_path:str = 'Data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv',
    station_raw_dir:str='Data/stations/raw',
    drop_cols:list[str] = None,
    split_tuples:bool = False,
    mapping: dict = None,
    drop_originals:bool =False,
    tuple_sep:str =None):
    
    # read in station data
    station_df= clean_station_data(station_raw_dir, 
                                drop_cols,
                                split_tuples,
                                mapping,
                                drop_originals,
                                tuple_sep)
    
    # read in event data

    event_df = pd.read_csv(event_file_path)
    
    # Merge Event and Station Data
    data = pd.merge(left=station_df,right=event_df,how ='outer',left_on='YEAR-MONTH-DAY',right_on='TORNADO_BEGIN_DATE')
    
    # Convert to floats when possible
    for col in data.columns:
        try:
            data[col] = pd.to_numeric(data[col],errors ='raise')
        except:
            pass
    
    return data