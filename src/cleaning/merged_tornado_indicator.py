import pandas as pd
import numpy as np
import datetime
import math
import pathlib
import os
import project_path as ppath
# Create Tornado indicator column
# Things to keep in mind:
# 1. At what time should a tornado be indicated? 
#       eg. during which time periods should we indicate? The same day? within n hours?
# 2. How far from the station should a tornado be in order to count for that station?





# Haversine Formula for computing the number of kilometers between 
# To use this must convert lat lon from degrees to radians.
def lat_lon_metric(lat_1,lon_1,lat_2,lon_2):
    f""" Calculates the great circle distance between two points on Earth given
    their latitude and longitude.

    Args:
        lat1, lon1, lat2, lon2 : float or array-like
        Latitude and longitude in degrees. Can be scalars or pandas Series.

    Returns:
        float or Series : Distance in kilometers
    """
    Rd = 6371 # approx. Earth radius in km
    rlat_1 = (lat_1*(np.pi))/(180) # convert to radians
    rlon_1 = (lon_1*np.pi)/(180) # convert to radians
    rlat_2 = (lat_2*np.pi)/(180) # convert to radians
    rlon_2 = (lon_2*np.pi)/(180) # convert to radians
    Term_1 = (np.sin((rlat_2-rlat_1)/2))**2
    Term_2 = np.cos(rlat_1)*np.cos(rlat_2)*(np.sin((rlon_2-rlon_1)/2))**2
    a = Term_1+Term_2
    c = 2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
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




def tornado_station_matcher(df_station,
                                  df_events,
                                  val_radius,
                                  time_window,
                                  station_datetime_column='DATE',
                                  begin_event_datetime_column='TORNADO_BEGIN_DATE_TIME',
                                  end_event_datetime_column='TORNADO_END_DATE_TIME'
                                  ):
    
    # Ensure datetime columns are proper datetime type
    
    df_station[station_datetime_column] = pd.to_datetime(df_station[station_datetime_column],errors='coerce')
    
    df_events[begin_event_datetime_column] = pd.to_datetime(df_events[begin_event_datetime_column],errors='coerce')

    df_events[end_event_datetime_column] = pd.to_datetime(df_events[end_event_datetime_column],errors='coerce')
    
    # Create 'TORNADO_OCCURRENCE' columns initial values of false
    df_station['TORNADO_OCCURRENCE'] = False
    # Create 'TORNADO_BEGIN_TIME' columns initial values of np.nan
    df_station[begin_event_datetime_column] = pd.NaT
    
    # Important for lat_lon_metric
    df_events = df_events.dropna(subset=['TORNADO_BEGIN_LAT', 'TORNADO_BEGIN_LON'])
    df_station =df_station.dropna(subset=['LATITUDE','LONGITUDE'])
    # For each tornado event and each station observation 
    # determine if station observes tornado.
    # time_window and val_radius
    # Will 'for loop on tornadoes'. Likely a better way to do this- room for improvement.
    for _,row in df_events.iterrows():
        tornado_begin_time = row[begin_event_datetime_column]
        tornado_begin_lat = row['TORNADO_BEGIN_LAT']
        tornado_begin_lon= row['TORNADO_BEGIN_LON']
        
        # time_window mask
        time_diff_hours = (tornado_begin_time - df_station[station_datetime_column]).dt.total_seconds() / 3600  
        time_window_mask = (time_diff_hours >= 0) & (time_diff_hours <= time_window)
        
        
        # distance_mask
        station_tornado_distances = lat_lon_metric(lat_1=df_station['LATITUDE'],
                                                    lon_1=df_station['LONGITUDE'],
                                                    lat_2=tornado_begin_lat,
                                                    lon_2=tornado_begin_lon)
        distance_mask = station_tornado_distances <= val_radius
        
        df_station.loc[(time_window_mask)&(distance_mask),'TORNADO_OCCURRENCE']=True # Inital label is false
        df_station.loc[(time_window_mask)&(distance_mask),begin_event_datetime_column]= tornado_begin_time
    
    # check that time_window is respected
    assert(((df_station[begin_event_datetime_column]-df_station[station_datetime_column]).dt.total_seconds() / 3600).max()<= time_window )
    return df_station

### HYPERPARAMETER time_window in hours
### if a tornado happens at 16:00 and time_window is 1,
### then a tornado is indicated at 15:00,16:00. We don't want to know
### one hour after since this doesn't give us information about
### what factors induce a tornadic episode, rather what happens after.
### Therefore, this would taint the modeling performance.

### HYPERPARAMETER valid_radius in km
### if a tornado occurs within valid_radius km of a station
### a tornado is indicated for that station within the time_window.

### NOTE: If we want improvements, we can draw a "spherical" lin
# between the starting and end lat,lon of a tornado.
### If this line crosses a valid radius of a station, 
### it will be counted. This ASSUMES TORNADO TAKES STRAIGHT LINE.

# Columns from merged station datasets (without tornado indicator)
# to drop. Can be modified if desired. Will be the default value in 
# create_tornado_indicator function below

def create_tornado_indicator(
    processed_event_path:str = 'data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv',
    processed_station_directory:str='data/stations/processed',
    time_window:float = 2,
    val_radius = 75):
    f""" Creates a tornado indicator column in the station-events merged DataFrame.

    Args:
        processed_event_path:str - path to Oklahoma Tornado csv file.
        processed_station_directory:str - path to processed station data directory.
        time_window : float - a positive float.
        val_radius : float - a positive float.

    Returns:
        pd.DataFrame : creates a new pd.dataframe that merges tornado events with station data
        provided tornado begins within {time_window} hours after station observation and 
        tornado begins within {val_radius} kilometers of station.
    """
    
    project_root = ppath.find_project_root()
    pathlib_path_to_folder = pathlib.Path(processed_station_directory)
    local_path_to_folder = project_root / pathlib_path_to_folder
    print(f'Searching for {local_path_to_folder}')
    processed_station_files = os.listdir(local_path_to_folder)
    print(f'Found {local_path_to_folder}')
    
    processed_station_csv_files = [file for file in processed_station_files if file.endswith('.csv')]
    
    # Create output directory if it doesn't exist
    local_event_station_indicator_path = project_root / pathlib.Path('data/event_station_indicator/')
    local_event_station_indicator_path.mkdir(parents=True, exist_ok=True)
    
    
    # read in event data 
    
    events_csv = project_root/pathlib.Path(processed_event_path)
    df_events= pd.read_csv(events_csv)
    
    

    
    for station_csv in processed_station_csv_files:
        
        station_csv_path = local_path_to_folder/pathlib.Path(station_csv)
        df_station = pd.read_csv(station_csv_path)
        df_tornado_indicator= tornado_station_matcher(df_station=df_station,
                                df_events=df_events,
                                time_window=time_window,
                                val_radius=val_radius)
        file_name = station_csv.replace('PROCESSED','TOR_INDICATOR')
            
        # Ensure datetime columns are proper datetime type
        #if not pd.api.types.is_datetime64_any_dtype(df_station['DATE']):
        df_tornado_indicator['DATE'] = pd.to_datetime(df_tornado_indicator['DATE'])
        #if not pd.api.types.is_datetime64_any_dtype(df_events['TORNADO_BEGIN_DATE_TIME']):
        df_tornado_indicator['TORNADO_BEGIN_DATE_TIME'] = pd.to_datetime(df_tornado_indicator['TORNADO_BEGIN_DATE_TIME'])
            
        # Save 
        df_tornado_indicator.to_csv(project_root/local_event_station_indicator_path/pathlib.Path(file_name),index=False)

    return None



create_tornado_indicator(
    processed_event_path= 'data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv',
    processed_station_directory='data/stations/processed',
    time_window = 3,
    val_radius = 75)
