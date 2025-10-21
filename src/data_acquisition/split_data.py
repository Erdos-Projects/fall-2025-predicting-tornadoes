import pandas as pd
import numpy as np
import os 

# The raw data from Oklahoma stations is too large to be pushed to GitHub
# The purpose of the following code is to split the raw data up to bite-
# sized chunks. 

# File path to original raw data. See Data/README_data.md for more information.
filepath = "Enter path here" 

os.path.getsize(filepath) # outputs 788589632 bytes so around 788.06 MB


df = pd.read_csv(filepath) # Read in as pd.DataFrame
df = df.copy() # Create copy to avoid modification of original

stations = df['STATION'].unique() # List of unique entries of 'STATION' column

##
# Create a new pd.DataFrame for each 'STATION' value
# For each new dataframe write to the csv:
# Station_[insert station value].cvs and split into sub csv's
# of the form Station_[insert station value]_Part_[insert value].cvs.
##


for station in stations:
    station_df = df[df['STATION'] == station]
    station_df.reset_index(inplace=True) # get rid of index values from df
    station_df.drop(['index'], inplace = True,axis=1) #drop 'index' column from .reset_index method
    station_path = f'Station_{station}.csv'
    station_csv = station_df.to_csv(station_path)
    memory_bytes = os.path.getsize(station_path) 
    memory_mb = memory_bytes/(10**6)
    if memory_mb >=100:
        print(f"{station_path} file is too large\n")
        n_splits = memory_mb//100 + 3 # extra wiggle room
        print(f"Splitting {station_path} into {n_splits} parts:\n")
        splits = np.array_split(station_df,n_splits)
        i=1 # Counter
        for split in splits:
            split_path = f'Station_{station}_Part_{i}.csv'
            split_df = pd.DataFrame(split) # Write into pd.DataFrame 
            print(f"Creating {split_path}...")
            split_df.to_csv(split_path)
            print(f"{split_path} created, {len(splits)-(i)} remaining...\n")
            # makes sure file is small enough
            assert(os.path.getsize(split_path)/(10**6)<100)
            i=i+1
        print(f"Finished splitting {station_path}")
        print(f"Removing file {station_path}\n\n")
        os.remove(f'{station_path}')
    else:
        print(f"{station} csv file is fine, no splitting necessary.\n\n")