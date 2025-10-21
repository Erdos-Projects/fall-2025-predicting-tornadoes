import pandas as pd
import numpy as np
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
    # Note that time_window and val_radius are in hours and km respectively.

    data = merge_station_events(event_file_path,
                        station_raw_dir,
                        drop_cols,
                        split_tuples,
                        mapping,
                        drop_originals,
                        tuple_sep)
    data['TORNADO_INITIAL_DISTANCE_FROM_STATION'] = data.apply(lambda r : initial_tornado_to_station_distance(r),axis =1)
    data[f'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_{val_radius}_km'] = data.apply(lambda r: apply_valid_radius(r,val_radius),axis =1)
    # Used for enforcing time window 
    def apply_time_window(pd_row, time_window,valid_radius):
        tornado_begin_time = pd_row['TORNADO_BEGIN_TIME']
        station_time = pd_row['STATION_TIME']
        within_radius_boolean = pd_row[f'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_{valid_radius}_km']
        # type check below because np.nan is a float in this column
        if type(tornado_begin_time) is float and np.isnan(tornado_begin_time):
            return np.nan
        if not within_radius_boolean:
            return False
        # All times are in HOUR:MIN:SECONDS 
        # Capture HOURs
        tornado_hour = int(tornado_begin_time.split(":")[0])
        station_hour = int(station_time.split(":")[0])
        if np.abs(station_hour - tornado_hour)<= time_window:
            return True
        else:
            return False
    
    
    
    data['TORNADO_OCCURRENCE'] = data.apply(lambda r : apply_time_window(r, time_window,val_radius), axis = 1)
    return data