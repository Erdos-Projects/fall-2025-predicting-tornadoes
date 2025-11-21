
import pandas as pd
import os

# Step 1: Filter Tornadoes that occurred in Oklahoma for each year
# Put each filtered data frame for each year in the list df_collect

raw_path = 'data/events/raw'
interim_out_path = 'data/events/interim/Oklahoma_Tornadoes_2000_2021.csv' # Path to interim CSV (optional)
processed_out_path = 'data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv' # Path to processed csv
df_collect = [] # collect DataFrames here

for year in range(2000, 2022):
    print(f"Processing {year}...")
    
    input_path = os.path.join(raw_path, f'{year}_storm_events.csv')
    df = pd.read_csv(input_path).copy()
    
    # Filter for Oklahoma tornado events
    df_ok_tornado = df[
        (df['STATE'] == 'OKLAHOMA') &
        # Don't use this (df['CZ_NAME'] == 'OKLAHOMA') &
        (df['EVENT_TYPE'] == 'Tornado')
    ]
    
    df_collect.append(df_ok_tornado)
    
    print(f"Saved {len(df_ok_tornado)} rows for {year}.")
    

# Step 2: Combine the contents df_collect. This yields the DataFrame 
# consisting of all tornadoes in Oklahoma from 2000-2021
combined_df = pd.concat(df_collect,axis =0)
combined_df.to_csv(interim_out_path,index=False)

# Step 3: Split Date and Time in 'BEGIN_DATE_TIME' and  'END_DATE_TIME' in combined_df. 
# The entries of these two features are of the form '25-MAY-00 23:55:00' where the date 
# is in day-month-year format. But format of 'BEGIN_DATE_TIME' and 'END_DATE_TIME' to 
# 'year-month-day' format. Here year needs to be a 4 digit number, month a two digit number,
# and day a two digit number. This is for us to be able to put them into datetime64[ns] data types
combined_df = combined_df.copy()

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

# Replace month name to a two digit number and get into year-month-day order.
# The following function helps with this
def event_date_time(pd_row):
    date_time_str = pd_row
    date_str = date_time_str.split(' ')[0]
    time_str = date_time_str.split(' ')[1]
    date_str_split = date_str.split('-')
    new_date_str = f"20{date_str_split[2]}-{month_num[date_str_split[1]]}-{date_str_split[0]}" # Need to get into 20** year/ correct order/ month number
    new_date_time_str = f"{new_date_str} {time_str}"
    return new_date_time_str


combined_df['BEGIN_DATE_TIME'] = combined_df['BEGIN_DATE_TIME'].apply(lambda r : event_date_time(r))
combined_df['END_DATE_TIME'] = combined_df['END_DATE_TIME'].apply(lambda r : event_date_time(r))

# Convert to datetime64[ns] 

combined_df['BEGIN_DATE_TIME'] = pd.to_datetime(combined_df['BEGIN_DATE_TIME'],errors='coerce')
combined_df['END_DATE_TIME'] = pd.to_datetime(combined_df['END_DATE_TIME'],errors='coerce')
# Rename columns

rename_columns={'BEGIN_DATE_TIME': 'TORNADO_BEGIN_DATE_TIME',
                'END_DATE_TIME': 'TORNADO_END_DATE_TIME',
                'BEGIN_LAT':'TORNADO_BEGIN_LAT',
                'END_LAT':'TORNADO_END_LAT',
                'BEGIN_LON':'TORNADO_BEGIN_LON',
                'END_LON':'TORNADO_END_LON',
                }
combined_df.rename(columns=rename_columns, inplace=True)
# Really only care about the following features, so we will drop the others.
combined_df = combined_df[
        [
        'TORNADO_BEGIN_DATE_TIME',
        'TORNADO_END_DATE_TIME',
        'TORNADO_BEGIN_LAT', 
        'TORNADO_BEGIN_LON',
        'TORNADO_END_LAT',  
        'TORNADO_END_LON'
        ]
        ]



combined_df.to_csv(processed_out_path,index=False)

# Important Note: Not all tornadoes in this final DataFrame will be used.
# In EDA and Modeling we allow for a hyperparameter that filters the
# occurrence of a tornado based on how far from each station 
# the tornado touched down.