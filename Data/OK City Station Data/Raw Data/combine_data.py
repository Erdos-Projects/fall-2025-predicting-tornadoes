import pandas as pd
import numpy as np
import os

# What this does: combines the dataframes from individual stations in Data/OK City Station Data/Raw Data into 
# a single dataframe


dirc = 'Data/OK City Station Data/Raw Data'
raw_station_data = os.listdir('Data/OK City Station Data/Raw Data') # list files in directory

station_csv_files = [file for file in raw_station_data if ('.csv' in file) and ('Station' in file)] # get csv files

station_list = [] # to hold station numbers as keys and number of csv files as entries

for file in station_csv_files:
    underscore_split = file.split('_')
    station_num = underscore_split[1].replace('.csv','')  
    station_list.append(int(station_num)) # station_num is a string
    


# Read in CSV's as pd.DataFrame's concat along axis = 0 

station_pd_dfs=[pd.read_csv(f"{dirc}/{file}").copy() for file in station_csv_files]
stations_df = pd.concat(station_pd_dfs, axis = 0)
df = stations_df.reset_index().drop(['index', 'Unnamed: 0'], axis =1)