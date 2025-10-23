
import pandas as pd
import os

# Step 1: Filter Tornadoes that occurred in Oklahoma for each year
# Put each filtered data frame for each year in the list df_collect

raw_path = 'Data/events/raw'
interim_out_path = 'Data/events/interim/Oklahoma_Tornadoes_2000_2021.csv' # Path to interim CSV (optional)
processed_out_path = 'Data/events/processed/final_Oklahoma_Tornadoes_2000_2021.csv' # Path to processed csv
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
# is in day-month-year format. We split this information into TORNADO_BEGIN_DATE, TORNADO_BEGIN_TIME,
# TORNADO_END_DATE, TORNADO_END_TIME.

combined_df = combined_df.copy()
combined_df['TORNADO_BEGIN_DATE'] = combined_df['BEGIN_DATE_TIME'].apply(lambda r : r.split(' ')[0]) 
combined_df['TORNADO_BEGIN_TIME'] = combined_df['BEGIN_DATE_TIME'].apply(lambda r : r.split(' ')[1])
combined_df['TORNADO_END_DATE'] = combined_df['END_DATE_TIME'].apply(lambda r : r.split(' ')[0])
combined_df['TORNADO_END_TIME'] = combined_df['END_DATE_TIME'].apply(lambda r : r.split(' ')[1])

combined_df.drop(['BEGIN_DATE_TIME','END_DATE_TIME'],axis=1,inplace=True) # drop originals

# Step 4 Change format of 'BEGIN_DATE' and 'END_DATE' to 'year-month-day' format. Here year needs 
# to be a 4 digit number, month a two digit number, and day a two digit number. This is so we can
# merge with station data. 

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

#Replace month name to a two digit number and get into year-month-day order.
combined_df['TORNADO_BEGIN_DATE'] = combined_df['TORNADO_BEGIN_DATE'].apply(lambda r: f'{r.split('-')[0]}-{month_num[r.split('-')[1]]}-{r.split('-')[2]}')
combined_df['TORNADO_END_DATE'] = combined_df['TORNADO_END_DATE'].apply(lambda r: f'{r.split('-')[0]}-{month_num[r.split('-')[1]]}-{r.split('-')[2]}')

# Get year to be 20**
combined_df['TORNADO_BEGIN_DATE']=combined_df['TORNADO_BEGIN_DATE'].apply(lambda r: f'20{r.split('-')[2]}-{r.split('-')[1]}-{r.split('-')[0]}')
combined_df['TORNADO_END_DATE']=combined_df['TORNADO_END_DATE'].apply(lambda r: f'20{r.split('-')[2]}-{r.split('-')[1]}-{r.split('-')[0]}')

# Really only care about the following features, so we will drop the others.
combined_df = combined_df[
        [
        'TORNADO_BEGIN_DATE',
        'TORNADO_BEGIN_TIME',
        'TORNADO_END_DATE',
        'TORNADO_END_TIME',
        'BEGIN_LAT', 
        'BEGIN_LON',
        'END_LAT',  
        'END_LON'
        ]
        ]

# Rename '***_LAT' and '***_LON' 

rename_columns={'BEGIN_LAT':'TORNADO_BEGIN_LAT',
                'END_LAT':'TORNADO_END_LAT',
                'BEGIN_LON':'TORNADO_BEGIN_LON',
                'END_LON':'TORNADO_END_LON',
                }

combined_df.rename(columns=rename_columns, inplace=True)

combined_df.to_csv(processed_out_path,index=False)

# Important Note: Not all tornadoes in this final DataFrame will be used.
# In EDA and Modeling we allow for a hyperparameter that filters the
# occurrence of a tornado based on how far from each station 
# the tornado touched down.