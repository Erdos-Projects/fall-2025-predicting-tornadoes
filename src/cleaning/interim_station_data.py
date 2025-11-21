import pandas as pd
import numpy as np
import os
import sys
import project_path as ppath
import pathlib 



# Features to DROP before EDA - Based on station column names
features_to_drop_before_eda = [
    # ========================================
    # IDENTIFIERS & METADATA (not predictive)
    # ========================================
    'NAME',  # Station name
    'CALL_SIGN',  # Call sign identifier
    'CALL_SIGN.1',  # Duplicate call sign
    'SOURCE',  # Data source flag
    'SOURCE.1',  # Duplicate source
    'REPORT_TYPE',  # Report type code
    'REPORT_TYPE.1',  # Duplicate report type
    'QUALITY_CONTROL',  # QC process name
    'QUALITY_CONTROL.1',  # Duplicate QC
    'REM',  # Remarks section
    # ========================================
    # PRECIPITATION (not super predictive)
    # OTHER FEATURES LIKE SLP and DEW are more 
    # informative.
    # ========================================
    'AA1','AA2','AA3','AA4',
    # ========================================
    # POTENTIAL DATA LEAKAGE WEATHER OBSERVATIONS
    # ========================================
    'AT1', 'AT2', 'AT3', 'AT4', 'AT5', 'AT6','AT7', 'AT8',
    'AU1', 'AU2', 'AU3', 'AU4', 'AU5', 
    'AW1', 'AW2', 'AW3', 'AW4', 'AW5', 'AW6','AW7',
    # ========================================
    # MONTHLY/LONG-PERIOD SUMMARIES (not relevant for hourly forecasting)
    # ========================================
    'AB1',  # Liquid precipitation monthly total
    'AD1',  # Greatest liquid precip in 24 hours for month
    'AE1',  # Number of days with specific precip amounts for month
    'AH1', 'AH2', 'AH3', 'AH4', 'AH5', 'AH6',  # Max short duration precip for month (5-45 min)
    'AI1', 'AI2', 'AI3', 'AI4', 'AI5', 'AI6',  # Max short duration precip for month (60-180 min)
    'AK1',  # Greatest snow depth on ground for month
    'AM1',  # Greatest snow accumulation in 24 hours for month
    'AN1',  # Snow accumulation for day/month
    
    # ========================================
    # SNOW/ICE DATA (Oklahoma tornado season = spring/summer, no snow)
    # ========================================
    'AJ1',  # Snow depth
    'AL1',  # Snow accumulation
    
    # ========================================
    # PAST WEATHER (less predictive than current conditions)
    # ========================================
    'AX1', 'AX2', 'AX3', 'AX4', 'AX5', 'AX6',  # Past weather summary
    
    # ========================================
    # OBSCURE/RARELY REPORTED VARIABLES
    # ========================================
    'AG1',  # Estimated precipitation (from AFCCC)
    'ED1',  # Runway visual range (aviation-specific, rare)
    'EQD',  # Element quality data section
    'GA1', 'GA2', 'GA3', 'GA4', 'GA5', 'GA6',  # Sky cover summation (duplicative with CIG)
    'GD1', 'GD2', 'GD3', 'GD4',  # Sky cover layer (detailed cloud layers - keep if you want detail)
    'GE1',  # Sky condition/cloud genus
    'GF1',  # Sky cover layer base height
    'GJ1',  # Sunshine observation
    'GK1',  # Sunshine percent possible
    'GP1',  # Sky cover time period
    'GQ1',  # Sky condition method
    'GR1',  # Below station cloud layer
    'HL1',  # Hail size
    'IA1',  # Ground surface observation (soil temp, ground state)
    'KA1', 'KA2', 'KA3', 'KA4',  # Extreme air temperature (daily max/min - not hourly)
    'KB1', 'KB2', 'KB3',  # Average air temperature
    'KC1', 'KC2',  # Extreme temperature (manual observation)
    'KD1', 'KD2',  # Heating/cooling degree days
    'KE1',  # Extreme temperature (automated)
    'KG1', 'KG2',  # Average temperature (period)
    'MA1',  # Atmospheric pressure change
    'MD1',  # Atmospheric pressure tendency
    'MF1',  # Atmospheric pressure observation (geopotential height)
    'MG1',  # Atmospheric pressure observation (station pressure at observation level)
    'MH1',  # Atmospheric pressure observation (altimeter setting)
    'MK1',  # Atmospheric pressure observation (station pressure)
    'MV1',  # Present weather in vicinity
    'MW1', 'MW2', 'MW3', 'MW4', 'MW5',  # Manual atmospheric conditions (past weather)
    'OC1',  # Wind gust observation
    'OD1',  # Supplemental wind data
    'OE1', 'OE2', 'OE3',  # Wind summary observations
    'RH1', 'RH2', 'RH3',  # Relative humidity (can be derived from TMP and DEW)
    'SA1',  # Sea surface temperature (not relevant for Oklahoma)
    'UA1',  # Wave measurement (ocean, not relevant)
    'UG1',  # Wave direction (ocean, not relevant)
    'WA1',  # Platform ice accretion

]

# Drop columns for each station.
# Put each data/interim/stations/interim if they are not too large

def interim_station_data(path_to_raw_folder, features_to_drop_before_eda = features_to_drop_before_eda):
    project_root = ppath.find_project_root()
    pathlib_path_to_folder = pathlib.Path(path_to_raw_folder)
    local_path_to_folder = project_root/pathlib_path_to_folder
    
    print(f'Searching for {local_path_to_folder}')
    raw_station_files = os.listdir(local_path_to_folder)
    print(f'Found {local_path_to_folder}')
    
    raw_station_csv_files = [file for file in raw_station_files if ('.csv' in file)]
    total_size_mb = 0
    for station_csv in raw_station_csv_files:
        print(f'Reading in {station_csv} as dataframe')
        station_csv_pathlib_path = local_path_to_folder/pathlib.Path(station_csv)
        station_df = pd.read_csv(station_csv_pathlib_path).copy()
        station_df.index
        station_df_cols = station_df.columns
        station_cols_to_drop = [col for col in features_to_drop_before_eda if (col in station_df_cols)]
        new_station_df=station_df.drop(columns=station_cols_to_drop)
        new_station_file = pathlib.Path(f'data/stations/interim/INTERIM_{station_csv}')
        path_to_new_file = project_root/new_station_file
        new_station_df.to_csv(path_to_new_file, index=False)
        file_size_bytes = path_to_new_file.stat().st_size
        print(f'Creating file: {new_station_file}')
        total_size_mb = total_size_mb+ file_size_bytes/(1024)**2
        print(f" File size of {new_station_file}: ",file_size_bytes/(1024)**2, "MB")
    return print(total_size_mb)

# Run interim_station_data
interim_station_data('data/stations/raw')

