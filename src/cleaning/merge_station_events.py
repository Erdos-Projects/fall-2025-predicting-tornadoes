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
    f"""
    Cleans the raw station Pandas DataFrames and combines them into a new DataFrame.
    Args:
    event_file_path: str - local GitHub path to the processed Oklahoma Tornadoes.
    station_raw_dir : str - local GitHub directory containing the raw station data.
    drop_cols: list[str] or None - list of columns to be dropped in the merged DataFrame.
    mapping : dict — key = column name, value = list of new sub‐column names. This dictionary
    represents the columns in the merged data frame that are to be split into new sub-columns
    as dictated in the associated dictionary value.
    drop_original : bool — if True, drop the original columns given by the keys of {mapping} 
    after performing the splitting of the column.
    tuple_sep : str or None — if the tuple is stored as a string with a separator, provide the separator (e.g., ",").
    Returns:
    A new pandas DataFrame with the expanded columns.
    """
    
    # read in station data
    station_df= clean_station_data(raw_dir=station_raw_dir, 
                                drop_cols=drop_cols,
                                split_tuples=split_tuples,
                                mapping = mapping,
                                drop_originals=drop_originals,
                                tuple_sep= tuple_sep,
                                )
    
    # read in event data

    event_df = pd.read_csv(event_file_path)
    station_df['STATION_DATE_TIME'] = pd.to_datetime(station_df['STATION_DATE_TIME'], errors='coerce')
    event_df['TORNADO_BEGIN_DATE_TIME'] = pd.to_datetime(event_df['TORNADO_BEGIN_DATE_TIME'], errors='coerce')
    
    # DOESN'T ACCOUNT FOR NEXT DAY TORNADOES-- OKAY WITH THIS
    station_df['DATE']= station_df['STATION_DATE_TIME'].dt.date
    event_df['DATE']= event_df['TORNADO_BEGIN_DATE_TIME'].dt.date
    data = pd.merge(left=station_df,right=event_df,how ='outer',left_on='DATE',right_on='DATE')
    
    # Drop 'DATE' col
    
    data.drop(columns=['DATE'],inplace= True)
    # Convert to floats when possible
    for col in data.columns:
        try:
            data[col] = pd.to_numeric(data[col],errors ='raise')
        except:
            pass
    
    return data