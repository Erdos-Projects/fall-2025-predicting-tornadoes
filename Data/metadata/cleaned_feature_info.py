




# Importable dictionaries based on datatype consisting of information about the numerical isd features 
# use in data after the NaN value cleanup in EDA. 

isd_int_columns_station = {
    'STATION': {
        'units': 'identifier code',
        'description': 'Unique numeric identifier for the station (WMO, WBAN, or USAF code).',
        'notes': 'Acts as primary key when merging with station metadata or other ISD files.'
    }
}

isd_float_columns_station = {
    # --- Station metadata ---
    'LATITUDE': {
        'units': 'decimal degrees (°N)',
        'range': '-90 to +90',
        'description': 'Latitude of station location.'
    },
    'LONGITUDE': {
        'units': 'decimal degrees (°E)',
        'range': '-180 to +180',
        'description': 'Longitude of station location.'
    },
    'ELEVATION': {
        'units': 'meters above mean sea level (m)',
        'range': '-400 to ~6000 typical',
        'description': 'Elevation of the station above mean sea level.'
    }
}

isd_float_meteor_columns = {
    # --- Sky condition ---
    'CIG_ceiling_height': {
        'units': 'meters',
        'scale': 1,
        'range': '0–22000 (22000 = unlimited ceiling)',
        'description': 'Height of lowest cloud layer reported as ceiling.',
        'missing_value': 99999,
        'notes': 'Value of 99999 may indicate unlimited ceiling if CIG_cavok_code is N or Y.'
    },
    
    # --- Temperature and Dew Point ---
    'DEW_dew_point': {
        'units': 'degrees Celsius',
        'scale': 10,
        'range': '-93.2 to +61.8°C typical',
        'description': 'Dew point temperature (scaled by 10).',
        'missing_value': 9999,
        'notes': 'Divide by 10 to get actual temperature in °C. Value 9999 indicates missing.'
    },
    'TMP_air_temperature': {
        'units': 'degrees Celsius',
        'scale': 10,
        'range': '-93.2 to +61.8°C typical',
        'description': 'Ambient (dry-bulb) temperature (scaled by 10).',
        'missing_value': 9999,
        'notes': 'Divide by 10 to get actual temperature in °C. Value 9999 indicates missing.'
    },
    
    # --- Pressure ---
    'SLP_sea_level_pressure': {
        'units': 'hectopascals (hPa)',
        'scale': 10,
        'description': 'Pressure reduced to mean sea level (scaled by 10).',
        'missing_value': 99999,
        'notes': 'Divide by 10 to get actual pressure in hPa. Value 99999 indicates missing.'
    },
    
    # --- Visibility ---
    'VIS_distance': {
        'units': 'meters',
        'scale': 1,
        'description': 'Horizontal visibility distance (in meters).',
        'missing_value': 999999,
        'notes': 'Value of 999999 may indicate unlimited visibility if CIG_cavok_code is Y or N.'
    },
    
    # --- Wind ---
    'WND_direction_angle': {
        'units': 'degrees true (0–360)',
        'scale': 1,
        'description': 'Direction from which wind is blowing.',
        'missing_value': 999,
        'notes': 'Value 999 may indicate variable wind (if WND_type_code is V) or calm wind (if WND_type_code is C).'
    },
    'WND_speed_rate': {
        'units': 'meters per second (m/s)',
        'scale': 10,
        'description': 'Wind speed (scaled by 10).',
        'missing_value': 9999,
        'notes': 'Divide by 10 to get actual speed in m/s. Value 9999 indicates missing. Value 0 with WND_type_code=9 indicates calm.'
    },
}

isd_station_datetime_columns = {
    'DATE': {
        'units': 'UTC datetime',
        'description': 'Timestamp of station observation (UTC).',
        'format': 'ISO 8601 datetime string or pandas datetime object'
    }
}

derived_tornado_datetime_columns = {
    'TORNADO_BEGIN_DATE_TIME': {
        'units': 'UTC datetime',
        'description': 'Tornado event start time.',
        'format': 'ISO 8601 datetime string or pandas datetime object'
    }
}

isd_categorical_meteor_columns = {
    # --- Wind type ---
    'WND_type_code': {
        'units': 'categorical',
        'description': 'Wind observation type code.',
        'values': {
            'A': 'Abridged Beaufort',
            'B': 'Beaufort',
            'C': 'Calm',
            'H': 'Estimated (5-minute average)',
            'N': 'Normal',
            'R': 'Estimated (1-minute rapid)',
            'Q': 'Squall',
            'T': 'Estimated (180-second)',
            'V': 'Variable',
            '9': 'Missing'
        },
        'notes': 'C = calm wind, V = variable direction, 9 = missing. If type_code=9 and speed=0, infer calm wind.'
    },
    'WND_direction_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for wind direction measurement.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    'WND_speed_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for wind speed measurement.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    
    # --- Ceiling ---
    'CIG_ceiling_quality_code': {
        'units': 'categorical (numeric)',
        'description': 'Quality code for ceiling height measurement.',
        'values': {
            0: 'Passed gross limits check',
            1: 'Passed all quality control checks',
            2: 'Suspect',
            3: 'Erroneous',
            4: 'Passed gross limits check, data originate from NCEI',
            5: 'Passed all quality control checks, data originate from non-NCEI source',
            6: 'Suspect, data originate from non-NCEI source',
            7: 'Erroneous, data originate from non-NCEI source',
            9: 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data. Stored as integer.'
    },
    'CIG_ceiling_determination_code': {
        'units': 'categorical',
        'description': 'Method used to determine ceiling.',
        'values': {
            'A': 'Aircraft',
            'B': 'Balloon',
            'C': 'Statistically derived',
            'D': 'Persistent cirriform ceiling (pre-1950)',
            'E': 'Estimated',
            'M': 'Measured',
            'P': 'Precipitation ceiling (pre-1950)',
            'R': 'Radar',
            'S': 'ASOS augmented',
            'U': 'Unknown',
            'V': 'Variable',
            'W': 'Obscured',
            '9': 'Missing'
        },
        'notes': 'W with ceiling=99999 indicates clear below 12,000 feet.'
    },
    'CIG_cavok_code': {
        'units': 'categorical',
        'description': 'CAVOK (Ceiling And Visibility OK) indicator.',
        'values': {
            'N': 'No',
            'Y': 'Yes',
            '9': 'Missing'
        },
        'notes': 'Y or N with ceiling=99999 indicates unlimited ceiling. Y with visibility=999999 indicates unlimited visibility.'
    },
    
    # --- Visibility ---
    'VIS_distance_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for visibility measurement.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    'VIS_variability_code': {
        'units': 'categorical',
        'description': 'Visibility variability code.',
        'values': {
            'N': 'Not variable',
            'V': 'Variable',
            '9': 'Missing'
        }
    },
    'VIS_variability_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for visibility variability.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    
    # --- Temperature ---
    'TMP_air_temperature_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for air temperature measurement.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    'DEW_dew_point_quality_code': {
        'units': 'categorical',
        'description': 'Quality code for dew point measurement.',
        'values': {
            '0': 'Passed gross limits check',
            '1': 'Passed all quality control checks',
            '2': 'Suspect',
            '3': 'Erroneous',
            '4': 'Passed gross limits check, data originate from NCEI',
            '5': 'Passed all quality control checks, data originate from non-NCEI source',
            '6': 'Suspect, data originate from non-NCEI source',
            '7': 'Erroneous, data originate from non-NCEI source',
            '9': 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data.'
    },
    
    # --- Pressure ---
    'SLP_sea_level_pressure_quality_code': {
        'units': 'categorical (numeric)',
        'description': 'Quality code for sea level pressure measurement.',
        'values': {
            0: 'Passed gross limits check',
            1: 'Passed all quality control checks',
            2: 'Suspect',
            3: 'Erroneous',
            4: 'Passed gross limits check, data originate from NCEI',
            5: 'Passed all quality control checks, data originate from non-NCEI source',
            6: 'Suspect, data originate from non-NCEI source',
            7: 'Erroneous, data originate from non-NCEI source',
            9: 'Missing'
        },
        'notes': 'Codes 3, 6, 9 indicate poor quality or missing data. Stored as integer.'
    },
}

derived_tornado_bool_columns = {
    'TORNADO_OCCURRENCE': {
        'units': 'boolean',
        'description': 'True if a tornado occurred within the valid radius and time window for the station record.',
        'notes': 'Created by spatial-temporal matching between station observations and tornado event records.'
    }
}

###########

# Complete dictionary of conditional rules where "missing" codes have special meanings
# Structure: {feature: {condition_column_name: {condition_value: rule_details}}}
isd_conditional_meanings = {
    # ========================================
    # WIND-OBSERVATION
    # ========================================
    'WND_direction_angle': {
        'WND_type_code': {
            'V': {
                'interpretation': 'variable_wind_direction',
                'value_to_check': 999,
                'meaning': 'Variable wind direction',
                'action': 'create_flag'
            },
            'C': {
                'interpretation': 'calm_wind',
                'value_to_check': 999,
                'meaning': 'Calm wind (wind speed near zero)',
                'action': 'set_to_zero'
            }
        }
    },
    
    'WND_type_code': {
        'WND_speed_rate': {
            0: {
                'interpretation': 'calm_inferred',
                'value_to_check': '9',
                'meaning': 'Calm wind inferred from zero speed',
                'action': 'set_to_calm'
            }
        }
    },
    
    # ========================================
    # CEILING HEIGHT
    # ========================================
    'CIG_ceiling_height': {
        'CIG_ceiling_determination_code': {
            'W': {
                'interpretation': 'Obscured',
                'value_to_check': 99999,
                'meaning': 'Obscured',
                'action': 'create_flag'
            }
        }
    }
}
###########


# Combined dictionary: Missing values AND poor quality codes
# These values should be replaced with NaN
isd_missing_and_poor_quality_codes = {
    # WIND-OBSERVATION
    'WND_direction_angle': [999],  # 999 = Missing
    'WND_direction_quality_code': ['3', '6', '9'],  # Suspect or missing
    'WND_type_code': ['9'],  # 9 = Missing
    'WND_speed_rate': [9999],  # 9999 = Missing
    'WND_speed_quality_code': ['3', '6', '9'],  # Suspect or missing
    
    # SKY-CONDITION-OBSERVATION (Ceiling)
    'CIG_ceiling_height': [99999],  # 99999 = Missing
    'CIG_ceiling_quality_code': [3, 6, 9],  # Suspect or missing (stored as int)
    'CIG_ceiling_determination_code': ['9'],  # 9 = Missing
    'CIG_cavok_code': ['9'],  # 9 = Missing
    
    # VISIBILITY-OBSERVATION
    'VIS_distance': [999999],  # 999999 = Missing
    'VIS_distance_quality_code': ['3', '6', '9'],  # Suspect or missing
    'VIS_variability_code': ['9'],  # 9 = Missing
    'VIS_variability_quality_code': ['3', '6', '9'],  # Suspect or missing
    
    # AIR-TEMPERATURE-OBSERVATION
    'TMP_air_temperature': [9999],  # +9999 = Missing (scaled)
    'TMP_air_temperature_quality_code': ['3', '6', '9'],  # Suspect or missing
    'DEW_dew_point': [9999],  # +9999 = Missing (scaled)
    'DEW_dew_point_quality_code': ['3', '6', '9'],  # Suspect or missing
    
    # ATMOSPHERIC-PRESSURE-OBSERVATION
    'SLP_sea_level_pressure': [99999],  # 99999 = Missing
    'SLP_sea_level_pressure_quality_code': [3, 6, 9],  # Suspect or missing (stored as int)
}
###########

# Lists of each of the dictionaries keys

# isd_int_columns_station keys
int_station_features = list(isd_int_columns_station.keys())

# isd_float_columns_station keys
float_station_features = list(isd_float_columns_station.keys())

# isd_float_meteor_columns keys
float_meteor_features = list(isd_float_meteor_columns.keys())

# derived_tornado_float_columns keys
float_tornado_features = list(derived_tornado_bool_columns.keys())

# isd_station_datetime_columns keys
datetime_station_features =list(isd_station_datetime_columns.keys())

# derived_tornado_datetime_columns
datetime_tornado_features = list(derived_tornado_datetime_columns.keys())

# isd_categorical_meteor_columns
categorical_meteor_features = list(isd_categorical_meteor_columns.keys())

# derived_tornado_bool_columns
bool_tornado_features = list(derived_tornado_bool_columns.keys())

###########

# Lists of the features based on datatypes

# numeric features
numeric_features = int_station_features+float_meteor_features+float_station_features+float_tornado_features

# datetime features
datetime_features = datetime_station_features+datetime_tornado_features

# categorical features
categorical_features = categorical_meteor_features

# boolean features

boolean_features = bool_tornado_features

###########

