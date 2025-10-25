import pandas as pd
import numpy as np
import datetime
import math
from src.cleaning.merge_station_events import merge_station_events
# Create Tornado indicator column
# Things to keep in mind:
# 1. At what time should a tornado be indicated? 
#       eg. during which time periods should we indicate? The same day? within n hours?
# 2. How far from the station should a tornado be in order to count for that station?





# Haversine Formula for computing the number of kilometers between 
# To use this must convert lat lon from degrees to radians.
def lat_lon_metric(lat_lon_1:tuple[float,float],lat_lon_2:tuple[float,float]):
    f""" Calculates the great circle distance between two points on Earth given
    their latitude and longitude.

    Args:
        lat_lon_1 : tuple[float,float] - a latitude,longitude coordinate. Both entries
        are in degrees.
        lat_lon_2 : tuple[float,float] - a latitude,longitude coordinate. Both entries
        are in degrees.

    Returns:
        float -  the great circle distance between {lat_lon_1} and {lat_lon_2} in kilometers.
    """
    Rd = 6371 # approx. Earth radius in km
    lat_1,lon_1 = lat_lon_1[0],lat_lon_1[1] # in deg
    lat_2,lon_2 = lat_lon_2[0],lat_lon_2[1] # in deg
    rlat_1 = (lat_1*(math.pi))/(180) # convert to radians
    rlon_1 = (lon_1*math.pi)/(180) # convert to radians
    rlat_2 = (lat_2*math.pi)/(180) # convert to radians
    rlon_2 = (lon_2*math.pi)/(180) # convert to radians
    Term_1 = (math.sin((rlat_2-rlat_1)/2))**2
    Term_2 = math.cos(rlat_1)*math.cos(rlat_2)*(math.sin((rlon_2-rlon_1)/2))**2
    a = Term_1+Term_2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    D=Rd*c
    return D

def within_radius(lat_lon_1:tuple[float,float],lat_lon_2:tuple[float,float], valid_radius :float):
    f""" Determines if the great circle distance between two points on Earth, given 
    their latitude and longitude, are within a set distance from each other.

    Args:
        lat_lon_1 : tuple[float,float]- a latitude,longitude coordinate. Both entries
        are in degrees.
        lat_lon_2 : tuple[float,float]- a latitude,longitude coordinate. Both entries
        are in degrees.
        valid_radius : float - a positive float.

    Returns:
        boolean - True if {lat_lon_1} and {lat_lon_2} are withing f{valid_radius} kilometers
        from each other, false otherwise.
    """
    if np.isnan(lat_lon_1[0]):
        return np.nan
    elif np.isnan(lat_lon_1[1]):
        return np.nan
    elif np.isnan(lat_lon_2[0]):
        return np.nan
    elif np.isnan(lat_lon_2[1]):
        return np.nan
    else:
        great_circle_distance = lat_lon_metric(lat_lon_1,lat_lon_2)
    
        if great_circle_distance <= valid_radius:
            return True
        else:
            return False
    

### HYPERPARAMETER time_window in hours
### if a tornado happens at 16:00 and time_window is 1,
### then a tornado is indicated at 15:00,16:00,17:00

### HYPERPARAMETER valid_radius in km
### if a tornado occurs within valid_radius km of a station
### a tornado is indicated for that station within the time_window.

### NOTE: If we want improvements, we can draw a "spherical" lin
# between the starting and end lat,lon of a tornado.
### If this line crosses a valid radius of a station, 
### it will be counted. This ASSUMES TORNADO TAKES STRAIGHT LINE.

def create_tornado_indicator(
    event_file_path:str = 'Data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv',
    station_raw_dir:str='Data/stations/raw',
    drop_cols:list[str] = None,
    split_tuples:bool = False,
    mapping: dict = None,
    drop_originals:bool =False,
    tuple_sep:str =None,
    time_window:float = 1,
    val_radius = 50):
    f""" Creates a tornado indicator column in the station-events merged DataFrame.

    Args:
        event_file_path: str - local GitHub path to the processed Oklahoma Tornadoes.
        station_raw_dir : str - local GitHub directory containing the raw station data.
        drop_cols: list[str] or None - list of columns to be dropped in the merged DataFrame.
        mapping : dict — key = column name, value = list of new sub‐column names. This dictionary
        represents the columns in the merged data frame that are to be split into new sub-columns
        as dictated in the associated dictionary value.
        drop_original : bool — if True, drop the original columns given by the keys of {mapping} 
        after performing the splitting of the column.
        tuple_sep : str or None — if the tuple is stored as a string with a separator, 
        provide the separator (e.g., ",").
        time_window : float - a positive float
        val_radius : float - a positive float.

    Returns:
        pd.DataFrame : creates a station-events 
        merged DataFrame, where columns from {drop_cols} are dropped, if {split_tuples} is True
        columns are split into sub-columns as dictated by {mapping} and {tuple_sep}, and creates a
        new column new column 'TORNADO_OCCURRENCE' consisting of boolean values. A sample has an entry
        of True in 'TORNADO_OCCURRENCE' if the station in the sample observes a Tornado within 
        {time_window} hours of the tornado's beginning time and the station is within {val_radius}
        kilometers of the tornado's STARTING position.
    """
    # Note that time_window and val_radius are in hours and km respectively.

    data = merge_station_events(event_file_path,
                        station_raw_dir,
                        drop_cols,
                        split_tuples,
                        mapping,
                        drop_originals,
                        tuple_sep)
    
    # Tornado starting distance from station
    def initial_tornado_to_station_distance(pd_row):
        station_lat_lon = pd_row['STATION_LAT'],pd_row['STATION_LON']
        initial_tornado_lat_lon = pd_row['TORNADO_BEGIN_LAT'],pd_row['TORNADO_BEGIN_LON']
        return lat_lon_metric(station_lat_lon,initial_tornado_lat_lon)
    
# Checks if lat,lon of station and beginning position of tornado are within valid radius
    def apply_valid_radius(pd_row,valid_radius : float):
        station_lat_lon = pd_row['STATION_LAT'],pd_row['STATION_LON']
        initial_tornado_lat_lon = pd_row['TORNADO_BEGIN_LAT'],pd_row['TORNADO_BEGIN_LON']
        return within_radius(station_lat_lon, initial_tornado_lat_lon,valid_radius) 
    
    data['TORNADO_INITIAL_DISTANCE_FROM_STATION'] = data.apply(lambda r : initial_tornado_to_station_distance(r),axis =1)
    data[f'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_{val_radius}_km'] = data.apply(lambda r: apply_valid_radius(r,val_radius),axis =1)

# Ensures  datetime64[ns] type
    data['TORNADO_BEGIN_DATE_TIME'] = pd.to_datetime(
        data['TORNADO_BEGIN_DATE_TIME'], errors="coerce"
    )
    data['STATION_DATE_TIME'] = pd.to_datetime(
        data['STATION_DATE_TIME'], errors="coerce"
    )
    data['TORNADO_END_DATE_TIME'] = pd.to_datetime(
        data['TORNADO_END_DATE_TIME'], errors="coerce"
    )
# Mask for identifying tornado occurrence per station and station datetime
    mask = (
    (data[f'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_{val_radius}_km']) &
    (data['TORNADO_BEGIN_DATE_TIME'].notna()) &
    (data['STATION_DATE_TIME'].notna())
    )   

    time_diff = data['TORNADO_BEGIN_DATE_TIME'] - data.loc[mask, 'STATION_DATE_TIME']
    # ensure result is actually a timedelta series
    if not np.issubdtype(time_diff.dtype, np.timedelta64):
        raise TypeError(f"time_diff dtype is {time_diff.dtype}, expected timedelta64[ns]")
    
    
    data.loc[mask, 'TORNADO_OCCURRENCE'] = ((time_diff.abs().dt.total_seconds()) <= (3600*time_window))
    
    
    data["TORNADO_OCCURRENCE"].fillna(False, inplace = True)


    return data


# ensure result is actually a timedelta series
    if not np.issubdtype(time_diff.dtype, np.timedelta64):
        raise TypeError(f"time_diff dtype is {time_diff.dtype}, expected timedelta64[ns]")
    
    
    data.loc[mask, 'TORNADO_OCCURRENCE'] = ((time_diff.abs().dt.total_seconds()) <= (3600*time_window))
    
    
    data["TORNADO_OCCURRENCE"].fillna(False, inplace = True)