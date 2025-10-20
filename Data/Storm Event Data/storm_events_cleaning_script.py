# cleaning storm data 
# difference from Cleaning.ipynb is that we don't use df['CZ_NAME'] to filter
# Instead we later use a valid radius technique to indicate the occurrence of a tornado 

import pandas as pd

df_collect = []

for year in range(2000, 2022):
    print(f"Processing {year}...")
    
    # Load each years CSV
    df = pd.read_csv(f'Data/Storm Event Data/Raw Data/{year}_storm_events.csv')
    
    # Filter for Oklahoma tornado events
    df_ok_tornado = df[
        (df['STATE'] == 'OKLAHOMA') &
        # Don't use this (df['CZ_NAME'] == 'OKLAHOMA') &
        (df['EVENT_TYPE'] == 'Tornado')
    ]
    
    df_collect.append(df_ok_tornado)
    
    # Save filtered data for that year
    df_ok_tornado.to_csv(f'Data/Storm Event Data/Cleaned Data/NEW_{year}_oklahoma_tornadoes.csv', index=False)
    
    print(f"Saved {len(df_ok_tornado)} rows for {year}.")