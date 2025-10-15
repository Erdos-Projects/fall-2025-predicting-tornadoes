import pandas as pd
import numpy as np
import os

# What this does: Counts the number of non nan's for each feature for each station
# and organizes this information into Features_No_NAN_Counts.csv.

# Note: In the documentation (isd-format-document.pdf) sometimes a number 
# stands in for a nan value. We will deal with that if we choose such a 
# feature later on.


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
len_record = dict({})
stations = df['STATION'].unique()
for station in stations:
    sub_df = df[df['STATION']== station]
    len_record[station] ={col: len(sub_df[col].dropna()) for col in sub_df.columns}

toconcat = [pd.DataFrame(len_record[station],index = [f'Station {station}']).T for station in stations]
final_df = pd.concat(toconcat, axis = 1)
final_name = 'Features_No_NAN_Counts.csv'
final_path = f'Data/OK City Station Data/Raw Data Observations/{final_name}'
final_df.to_csv(final_path)