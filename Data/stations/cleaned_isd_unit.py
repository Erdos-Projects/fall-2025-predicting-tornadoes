
# Importable dictionaries based on datatype consisting of information about the numerical isd features 
# use in data after the NaN value cleanup in EDA. 



isd_int_columns_station = {
    'STATION': {
        'units': 'identifier code',
        'description': 'Unique numeric identifier for the station (WMO, WBAN, or USAF code).',
        'notes': 'Acts as primary key when merging with station metadata or other ISD files.'
    }
}

isd_float_columns_station ={
        # --- Station metadata ---
    'STATION_LAT': {
        'units': 'decimal degrees (°N)',
        'range': '-90 to +90',
        'description': 'Latitude of station location.'
    },
    'STATION_LON': {
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
    'CIG- Sky Condition Observation- Ceiling Height Dimension': {
        'units': 'meters',
        'scale': 1,
        'range': '0–22000 (22000 = unlimited ceiling)',
        'description': 'Height of lowest cloud layer reported as ceiling.'
    },

    # --- Temperature and Dew Point ---
    'DEW- Air Temperature Observation- Dew Point Temperature': {
        'units': 'degrees Celsius',
        'scale': 10,
        'range': '-93.2 to +61.8°C typical',
        'description': 'Dew point temperature (10s of °C).'
    },
    'TMP- Air Temperature Observation- Air Temperature': {
        'units': 'degrees Celsius',
        'scale': 10,
        'range': '-93.2 to +61.8°C typical',
        'description': 'Ambient (dry-bulb) temperature (10s of °C).'
    },

    # --- Pressure ---
    'MA1- Atmospheric Pressure Observation- Altimeter Setting Rate': {
        'units': 'hectopascals per hour (hPa/hr)',
        'scale': 10,
        'description': 'Rate of change in altimeter setting (10s of hPa per hour).'
    },
    'MA1- Atmospheric Pressure Observation- Station Pressure Rate': {
        'units': 'hectopascals per hour (hPa/hr)',
        'scale': 10,
        'description': 'Rate of change of station pressure (10s of hPa per hour).'
    },
    'SLP- Atmospheric Pressure Observation- Sea Level Pressure': {
        'units': 'hectopascals (hPa)',
        'scale': 10,
        'description': 'Pressure reduced to mean sea level (10s of hPa).'
    },

    # --- Visibility ---
    'VIS- Visibility Observation- Distance Dimension': {
        'units': 'meters',
        'scale': 1,
        'description': 'Horizontal visibility distance (in meters).'
    },

    # --- Wind ---
    'WND- Wind Observation- Direction Angle': {
        'units': 'degrees true (0–360)',
        'scale': 1,
        'description': 'Direction from which wind is blowing; -2 for calm.'
    },
    'WND- Wind Observation- Speed Rate': {
        'units': 'meters per second (m/s)',
        'scale': 10,
        'description': 'Wind speed (10s of m/s).'
    },
}

derived_tornado_float_columns = {    # --- Tornado features (derived) ---
    'TORNADO_BEGIN_LAT': {
        'units': 'decimal degrees (°N)',
        'description': 'Latitude of tornado beginning point.'
    },
    'TORNADO_BEGIN_LON': {
        'units': 'decimal degrees (°E)',
        'description': 'Longitude of tornado beginning point.'
    },
    'TORNADO_END_LAT': {
        'units': 'decimal degrees (°N)',
        'description': 'Latitude of tornado ending point.'
    },
    'TORNADO_END_LON': {
        'units': 'decimal degrees (°E)',
        'description': 'Longitude of tornado ending point.'
    },
    'TORNADO_INITIAL_DISTANCE_FROM_STATION': {
        'units': 'kilometers (km)',
        'description': 'Geodesic distance between station and tornado initial location.'
    }
    }


isd_station_datetime_columns = {
    'STATION_DATE_TIME': {
        'units': 'UTC datetime',
        'description': 'Timestamp of station observation (UTC).'
    }
}

derived_tornado_datetime_columns ={
        'TORNADO_BEGIN_DATE_TIME': {
        'units': 'UTC datetime',
        'description': 'Tornado event start time.'
    },
    'TORNADO_END_DATE_TIME': {
        'units': 'UTC datetime',
        'description': 'Tornado event end time.'
    }
}

isd_categorical_meteor_columns ={
    'WND- Wind Observation- Type Code': {
        'units': 'categorical',
        'description': 'Wind observation type code (A, I, P, Q, C).'
    }
}
derived_tornado_bool_columns = {
    'TORNADO_INITIAL_DISTANCE_FROM_STATION_WITHIN_50_km': {
        'units': 'categorical / boolean-like',
        'description': 'Indicator ("True"/"False") of whether tornado began within 50 km of station.'
    },
    'TORNADO_OCCURRENCE': {
        'units': 'boolean',
        'description': 'True if a tornado occurred within the valid radius and time window for the station record.'
    }
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
float_tornado_features = list(derived_tornado_float_columns.keys())

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

