import pandas as pd
import numpy as np
import os
import sys
import project_path as ppath
import pathlib 

# Dictionary mapping compound field names to their component column names
# Order matches ISD documentation exactly
isd_field_parsing_map = {
    # WIND-OBSERVATION (5 components)
    'WND': [
        'WND_direction_angle',
        'WND_direction_quality_code',
        'WND_type_code',
        'WND_speed_rate',
        'WND_speed_quality_code'
    ],
    
    # SKY-CONDITION-OBSERVATION ceiling (4 components)
    'CIG': [
        'CIG_ceiling_height',
        'CIG_ceiling_quality_code',
        'CIG_ceiling_determination_code',
        'CIG_cavok_code'
    ],
    
    # VISIBILITY-OBSERVATION (4 components)
    'VIS': [
        'VIS_distance',
        'VIS_distance_quality_code',
        'VIS_variability_code',
        'VIS_variability_quality_code'
    ],
    
    # AIR-TEMPERATURE-OBSERVATION air temperature (2 components)
    'TMP': [
        'TMP_air_temperature',
        'TMP_air_temperature_quality_code'
    ],
    
    # AIR-TEMPERATURE-OBSERVATION dew point (2 components)
    'DEW': [
        'DEW_dew_point',
        'DEW_dew_point_quality_code'
    ],
    
    # ATMOSPHERIC-PRESSURE-OBSERVATION sea level pressure (2 components)
    'SLP': [
        'SLP_sea_level_pressure',
        'SLP_sea_level_pressure_quality_code'
    ]
}


def parse_isd_compound_fields(df, field_parsing_map):
    """
    Parse compound ISD fields into separate columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing ISD data with compound fields
    field_parsing_map : dict
        Dictionary mapping compound field names to list of new column names
    
    Returns:
    --------
    pd.DataFrame : DataFrame with compound fields parsed into separate columns
    """
    import pandas as pd
    import numpy as np
    
    df_parsed = df.copy()
    
    for field_name, new_column_names in field_parsing_map.items():
        if field_name in df_parsed.columns:
            # Convert to string type first, handling NaN/None values
            field_data = df_parsed[field_name].astype(str)
            
            # Replace 'nan' and 'None' strings with empty string
            field_data = field_data.replace(['nan', 'None'], '')
            
            # Split the compound field by comma
            split_data = field_data.str.split(',', expand=True)
            
            # Assign to new columns
            for i, col_name in enumerate(new_column_names):
                if i < split_data.shape[1]:
                    df_parsed[col_name] = split_data[i]
                    # Replace empty strings with NaN for proper missing value handling
                    df_parsed[col_name] = df_parsed[col_name].replace('', np.nan)
                else:
                    df_parsed[col_name] = np.nan
            
            # Drop the original compound field
            df_parsed = df_parsed.drop(columns=[field_name])
            
            print(f"Parsed {field_name} into {len(new_column_names)} columns")
        else:
            print(f"Warning: {field_name} not found in DataFrame")
    
    return df_parsed


# Usage:
# station_data_parsed = parse_isd_compound_fields(station_data, isd_field_parsing_map)
def process_station_data(path_to_interim_folder, field_parsing_map=isd_field_parsing_map):
    """
    Process interim station CSV files by parsing compound ISD fields.
    
    Parameters:
    -----------
    path_to_interim_folder : str
        Relative path to folder containing interim station CSV files
    field_parsing_map : dict
        Mapping of compound field names to component column lists
        
    Returns:
    --------
    float : Total size of processed files in MB
    """
    project_root = ppath.find_project_root()
    pathlib_path_to_folder = pathlib.Path(path_to_interim_folder)
    local_path_to_folder = project_root / pathlib_path_to_folder
    print(f'Searching for {local_path_to_folder}')
    
    interim_station_files = os.listdir(local_path_to_folder)
    print(f'Found {local_path_to_folder}')
    
    interim_station_csv_files = [file for file in interim_station_files if file.endswith('.csv')]
    local_processed_station_path = project_root / pathlib.Path('Data/stations/processed')
    
    # Create output directory if it doesn't exist
    local_processed_station_path.mkdir(parents=True, exist_ok=True)
    
    total_size_mb = 0
    
    for station_csv in interim_station_csv_files:
        print(f'Reading in {station_csv} as dataframe')
        station_csv_pathlib_path = local_path_to_folder / pathlib.Path(station_csv)
        
        station_df = pd.read_csv(station_csv_pathlib_path)
        parsed_station_df = parse_isd_compound_fields(station_df, field_parsing_map=field_parsing_map)
        
        processed_csv_file = pathlib.Path(station_csv.replace('INTERIM', 'PROCESSED'))
        processed_csv_path = local_processed_station_path / processed_csv_file
        
        print(f'Creating file: {processed_csv_file}')
        parsed_station_df.to_csv(processed_csv_path, index=False)  # index=False to avoid extra column
        print(f'Finished')
        
        file_size_bytes = processed_csv_path.stat().st_size
        total_size_mb += file_size_bytes / (1024**2)
    
    print(f'Total processed data size: {total_size_mb:.2f} MB')
    return None


process_station_data('Data/stations/interim')