import pandas as pd
import numpy as np
import os

# What this does: Counts the frequency of non nan's for each feature for each station
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
new_df = stations_df.reset_index().drop(['index', 'Unnamed: 0'], axis =1).copy()



new_df['YEAR-MONTH-DAY'] = new_df['DATE'].apply(lambda r: r.split('T')[0])
new_df['TIME'] = new_df['DATE'].apply(lambda r: r.split('T')[1])
new_df.drop(['DATE'],axis=1,inplace=True)

# combined oklahoma tornadoes

path = 'Data/Storm Event Data/Cleaned Data/oklahoma_tornadoes_2000_2021.csv'
df2 = pd.read_csv(path).copy()
# Really will only care about 'BEGIN_DATE_TIME', 'END_DATE_TIME', 'BEGIN_LAT',
# 'END_LAT', 'BEGIN_LON', 'END_LON'

df2 = df2[
        [
        'BEGIN_DATE_TIME', 
        'END_DATE_TIME', 
        'BEGIN_LAT', 
        'END_LAT', 
        'BEGIN_LON', 
        'END_LON'
        ]
        ]

# columns BEGIN-DATE and BEGIN-TIME
new_df2 = df2.copy()
new_df2['BEGIN_DATE'] = df2['BEGIN_DATE_TIME'].apply(lambda r : r.split(' ')[0])
new_df2['BEGIN_TIME'] = df2['BEGIN_DATE_TIME'].apply(lambda r : r.split(' ')[1])
new_df2['END_DATE'] = df2['END_DATE_TIME'].apply(lambda r : r.split(' ')[0])
new_df2['END_TIME'] = df2['END_DATE_TIME'].apply(lambda r : r.split(' ')[1])

new_df2.drop(['BEGIN_DATE_TIME','END_DATE_TIME'],axis=1,inplace=True)

# Change format of 'BEGIN_DATE' and 'END_DATE' to match that of 'YEAR_MONTH_DAY' in station data

month_num = {
            'JAN':'01',
            'FEB':'02',
            'MAR':'03', 
            'APR':'04', 
            'MAY':'05', 
            'JUN':'06', 
            'JUL':'07', 
            'AUG':'08', 
            'SEP':'09', 
            'OCT':'10', 
            'NOV':'11', 
            'DEC':'12'
            }

new_df2['BEGIN_DATE'] = new_df2['BEGIN_DATE'].apply(lambda r: f'{r.split('-')[0]}-{month_num[r.split('-')[1]]}-{r.split('-')[2]}')
new_df2['END_DATE'] = new_df2['END_DATE'].apply(lambda r: f'{r.split('-')[0]}-{month_num[r.split('-')[1]]}-{r.split('-')[2]}')

# Get year to be 20**
new_df2['BEGIN_DATE']=new_df2['BEGIN_DATE'].apply(lambda r: f'20{r.split('-')[2]}-{r.split('-')[1]}-{r.split('-')[0]}')
new_df2['END_DATE']=new_df2['END_DATE'].apply(lambda r: f'20{r.split('-')[2]}-{r.split('-')[1]}-{r.split('-')[0]}')

final_df = pd.merge(left=new_df,right=new_df2,how ='outer',left_on='YEAR-MONTH-DAY',right_on='BEGIN_DATE')

# double check merge went as desired
final_df[final_df['YEAR-MONTH-DAY']==final_df['BEGIN_DATE']]

(final_df[final_df['YEAR-MONTH-DAY']!=final_df['BEGIN_DATE']]['BEGIN_DATE']).unique()