from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import datetime as dt

# Values to replace with NaN
class ReplaceValuesWithNaN(BaseEstimator, TransformerMixin):
    """
    Replace specified values with NaN across all columns.
    
    Parameters
    ----------
    values_to_replace : list or array-like, optional
        Values to replace with NaN.
    """
    def __init__(self, values_to_replace=None):
        self.values_to_replace = values_to_replace 

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # If X is a DataFrame
        if isinstance(X, pd.DataFrame):
            return X.replace(self.values_to_replace, np.nan)
        # If X is a numpy array this is what ColumnTransformers expect
        # if not a passthrough
        else:
            X = np.where(np.isin(X, self.values_to_replace), np.nan, X)
            return X
        
# NaN Replacement Calm Winds as per ISD documentation
class CalmWindFixer(BaseEstimator, TransformerMixin):
    """
    Replaces NaN wind type codes with 'C' (calm) whenever the wind speed is 0.
    
    Parameters
    ----------
    type_col : str, default='WND- Wind Observation- Type Code'
        Name of the wind type code column
    speed_col : str, default='WND- Wind Observation- Speed Rate'
        Name of the wind speed column
    """
    def __init__(self,
                type_col='WND- Wind Observation- Type Code',
                speed_col='WND- Wind Observation- Speed Rate'):
        self.type_col = type_col
        self.speed_col = speed_col

    def fit(self, X, y=None):
        # nothing to learn
        return self

    def transform(self, X):
        X = X.copy()
        # Make sure we can use .loc safely
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        # mask conditions
        mask_type_nan = X[self.type_col].isna()
        mask_speed_0 = X[self.speed_col] == 0
        # assign 'C' for calm where both conditions hold
        X.loc[mask_type_nan & mask_speed_0, self.type_col] = 'C'
        return X
    
# Drop Rows if NaN is in some subset of columns

class DropNaNRows(BaseEstimator, TransformerMixin):
    """
    Drops rows containing NaN in specified columns.
    
    Parameters
    ----------
    columns : list of str or int, optional
        Columns to check for NaN values. If None, drops rows with NaN in any column.
    """
    def __init__(self, columns=None):
        self.columns = columns  # list of columns to check for NaN

    def fit(self, X, y=None):
        # nothing to learn
        return self

    def transform(self, X):
        X = X.copy()
        if isinstance(X, np.ndarray):
            # if no columns are provided, drop rows with any NaN
            if self.columns is None:
                mask = ~np.any(np.isnan(X), axis=1)
            else:
                # if column indices are given
                mask = ~np.any(np.isnan(X[:, self.columns]), axis=1)
            return X[mask]
        else:
            # pandas DataFrame case
            if self.columns is None:
                return X.dropna()
            else:
                return X.dropna(subset=self.columns)
            
class NaNReplacement(BaseEstimator,TransformerMixin):
    """
    Replaces NaN values in self.column with self.value.
    
    Parameters
    ----------
    column : str, optional
        Name of the column to fill NaN values in
    value : any, optional
        Value to use for filling NaN entries
    """
    def __init__(self, column =None, value =None):
        self.column= column
        self.value=value
    
    def fit(self, X, y=None):
        # nothing to learn
        return self
    def transform(self,X):
        X = X.copy()
        if self.column is None or self.value is None:
            return X
        
        X[self.column] = X[self.column].fillna(self.value)
        return X
    
class DirectionAngleReplacement(BaseEstimator,TransformerMixin):
    """
    Drops any row with an nan direction angle and any WND Type Code that is not 'C'.
    
    Parameters
    ----------
    direction_col : str, default='WND- Wind Observation- Direction Angle'
        Name of the wind direction column
    type_col : str, default='WND- Wind Observation- Type Code'
        Name of the wind type code column
    """
    def __init__(self, 
                direction_col = 'WND- Wind Observation- Direction Angle',
                type_col = 'WND- Wind Observation- Type Code'
                ):
        self.direction_col = direction_col
        self.type_col = type_col
        
    
    def fit(self, X, y=None):
        # nothing to learn
        return self
    
    def transform(self, X):
        X = X.copy()
        direction_angle_na_mask = X[self.direction_col].isna()
        typecode_C_mask = (X[self.type_col] != 'C')
        neg2_mask = ((direction_angle_na_mask) & (typecode_C_mask))
        neg2_index = X[neg2_mask].index
        return X.drop(index= neg2_index)
        
# Drop Column

class DropColumns(BaseEstimator,TransformerMixin):
    """
    Drops columns.
    
    Parameters
    ----------
    columns : list of str, optional
        Names of columns to drop
    """
    def __init__(self,columns:list[str]=None):
        self.columns = columns
    
    def fit(self,X,y=None):
        # nothing to learn
        return self

    def transform(self,X):
        X = X.copy()
        return X.drop(columns=self.columns)

# Drop Duplicates
class DropDuplicates(BaseEstimator,TransformerMixin):
    """
    Removes duplicate rows from the dataset.
    """
    def __init__(self):
        pass
    def fit(self, X,y=None):
        # nothing to learn
        return self 
    
    def transform(self,X):
        X = X.copy()
        return X.drop_duplicates()
    
    
    
#================== Pre Train-Test Split Feature Engineering===============

class GrabYear(BaseEstimator,TransformerMixin):
    """
    Creates a new column that records the year of an observation.
    
    Parameters
    ----------
    column : str, default='STATION_DATE_TIME'
        Name of the datetime column
    new_col : str, default='year'
        Name for the new year column
    """
    def __init__(self, column = 'STATION_DATE_TIME', new_col ='year'):
        self.column = column
        self.new_col = new_col
    
    def fit(self, X, y=None):
        # nothing to learn
        return self
    def transform(self, X):
        X = X.copy()
        X[self.new_col] = X[self.column].dt.year
        return X

class DatetimeSinCosConverter(BaseEstimator,TransformerMixin):
    """
    Given a datatime column creates new columns with cyclic sine,cosine 
    representations of months in year 1--12, days in year 1--365, hours in day 0--23.
    
    Parameters
    ----------
    column : str, default='DATE'
        Name of the datetime column
    monthofyear : bool, default=True
        Create sin/cos encoding for month (1-12)
    dayofyear : bool, default=True
        Create sin/cos encoding for day of year (1-365)
    hourofday : bool, default=True
        Create sin/cos encoding for hour (0-23)
    """
    def __init__(self, 
                column = 'DATE',
                monthofyear =True,
                dayofyear = True, 
                hourofday =True):
        self.column = column
        self.monthofyear = monthofyear
        self.dayofyear = dayofyear
        self.hourofday = hourofday
        
    def fit(self, X,y=None):
        # nothing to learn
        return self
    
    def transform(self, X):
        X = X.copy()
        
        if self.monthofyear:
            month = X[self.column].dt.month
            X['sin_monthofyear'] = np.sin((month)*2*np.pi/12)
            X['cos_monthofyear'] = np.cos((month)*2*np.pi/12)
        
        if self.dayofyear:
            day = X[self.column].dt.dayofyear
            X['sin_dayofyear'] = np.sin((day)*2*np.pi/365)
            X['cos_dayofyear'] = np.cos((day)*2*np.pi/365)
        if self.hourofday:
            hour = X[self.column].dt.hour
            X['sin_hourofday'] = np.sin((hour)*2*np.pi/24)
            X['cos_hourofday'] = np.cos((hour)*2*np.pi/24)
        
        return X

    def get_feature_names_out(self, input_features=None):
        """Return input features plus the new difference features."""
        if input_features is None:
            input_features = []
        # Add new feature names for each column
        new_features= []
        
        if self.monthofyear:
            new_features.extend(['sin_monthofyear', 'cos_monthofyear'])  
        if self.dayofyear:
            new_features.extend(['sin_dayofyear', 'cos_dayofyear'])
        if self.hourofday:
            new_features.extend(['sin_hourofday', 'cos_hourofday'])
            
        return np.append(input_features, new_features)





#============= Feature Engineering (Pre Train-Test Split)======================

class SubtractColumns(BaseEstimator,TransformerMixin):
    """
    Creates a new column whose values are from taking the difference between two given columns.
    
    Parameters
    ----------
    col_1 : str
        Name of the first column (minuend)
    col_2 : str
        Name of the second column (subtrahend)
    new_col : str
        Name for the new difference column
    """
    def __init__(self, col_1, col_2, new_col):
        self.col_1 = col_1
        self.col_2 = col_2
        self.new_col = new_col

    def fit(self,X,y=None):
        # nothing to learn
        return self
    
    def transform(self,X):
        X = X.copy()
        if self.col_1 is None or self.col_2 is None:
            return X
        else: 
            X[self.new_col] = X[self.col_1] - X[self.col_2]
        return X
    
class DewTempSpread(BaseEstimator,TransformerMixin):
    """
    Creates a new column whose values are from taking the difference between 
    air temperature and dew point (T - Td).
    
    Parameters
    ----------
    new_col : str
        Name for the new dew point spread column
    """
    def __init__(self, new_col):

        self.new_col = new_col

    def fit(self,X,y=None):
        # nothing to learn
        return self
    
    def transform(self,X):
        X = X.copy()
        
        X[self.new_col] = X['TMP_air_temperature'] - X['DEW_dew_point']
        return X
    
    def get_feature_names_out(self, input_features=None):
        """Return input features plus the new dew point spread feature."""
        if input_features is None:
            input_features = []
        return np.append(input_features, [self.new_col])
    
    

    
#================ Features Engineering (Post Train-Test Split) ================
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class HourlyRates(BaseEstimator, TransformerMixin):
    """
    Calculate hourly rate of change for meteorological variables.
    
    Computes the per-hour rate of change between consecutive observations
    at each weather station. Must be fit on training data only to prevent
    data leakage.
    
    Parameters
    ----------
    columns : list of str, optional
        Column names for which to calculate hourly rates
    time_col : str, default='DATE'
        Name of the datetime column
    id_col : str, default='STATION'
        Name of the station ID column for grouping
    min_gap_hours : float, default=0.5
        Minimum time gap (hours) to consider for rate calculation
    max_gap_hours : float, default=3
        Maximum time gap (hours) to consider for rate calculation
    """
    def __init__(self, 
                 columns=None, 
                 time_col='DATE',
                 id_col='STATION',
                 min_gap_hours=0.5,  
                 max_gap_hours=3):
        self.columns = columns
        self.time_col = time_col
        self.id_col = id_col
        self.min_gap_hours = min_gap_hours  
        self.max_gap_hours = max_gap_hours
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X['_orig_pos'] = np.arange(len(X))
        
        # Sort for proper temporal grouping
        X = X.sort_values([self.id_col, self.time_col])
        
        # Compute time deltas per station
        dt_hours = X.groupby(self.id_col)[self.time_col].diff().dt.total_seconds() / 3600.0
        
        # Compute per-hour rates per column
        for col in self.columns:
            col_diff = X.groupby(self.id_col)[col].diff()
            
            # Only compute rate where time delta is valid AND not too small
            valid_mask = (dt_hours >= self.min_gap_hours) & (dt_hours <= self.max_gap_hours)
            rate = np.where(valid_mask, col_diff / dt_hours, np.nan)
            
            X[f"PER_HOUR_{col}"] = rate
        
        # Restore original order
        X = X.sort_values('_orig_pos').drop(columns='_orig_pos')
        
        return X
    
    def get_feature_names_out(self, input_features=None):
        """Return input features plus the new difference features."""
        if input_features is None:
            input_features = []
        # Add new feature names for each column
        new_features = [f"PER_HOUR_{col}" for col in self.columns]
        return np.append(input_features, new_features)
    


class DifferencesByHours(BaseEstimator, TransformerMixin):
    """
    Calculate rolling window differences for meteorological variables.
    
    Computes the change in a variable over a specified time window. Must be 
    fit on training data only to prevent temporal leakage.
    
    Parameters
    ----------
    columns : list of str, optional
        Column names for which to calculate differences
    time_col : str, default='DATE'
        Name of the datetime column
    id_col : str, default='STATION'
        Name of the station ID column for grouping
    num_hours : int, default=2
        Size of the rolling window in hours
    """
    def __init__(self,
                 columns=None,
                 time_col='DATE',
                 id_col='STATION',
                 num_hours=2):
        
        self.columns = columns
        self.time_col = time_col
        self.id_col = id_col
        self.num_hours = num_hours
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        original_order = X.index  # PRESERVES INPUT ORDER important for splitting
        X = X.sort_values([self.id_col, self.time_col])

        results = []  # list to collect per-station computations

        # Group by station and apply rolling logic
        for station, g in X.groupby(self.id_col):
            g = g.set_index(self.time_col)  # use datetime index for rolling
            
            for col in self.columns:
                diff_name = f"{self.num_hours}H_DIFF_{col}"
                g[diff_name] = (
                    g[col]
                    .rolling(f"{self.num_hours}h", closed='left')
                    .apply(lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 1 else np.nan, raw=False)
                )
            results.append(g.reset_index())

        # Combine all station groups
        out = pd.concat(results, axis=0)

        #  PRESERVES INPUT ORDER important for splitting
        out = out.set_index(original_order)
        out = out.loc[original_order]
        return out
    
 