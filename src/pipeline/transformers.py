
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import datetime as dt

# Values to replace with NaN
class ReplaceValuesWithNaN(BaseEstimator, TransformerMixin):
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
    Replaces NaN wind type codes with 'C' (calm) 
    whenever the wind speed is 0.
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
    replaces NaN values in self.column with self.value
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
    Drops any row with an nan direction angle and any WND Type Code
    that is not 'C'
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
    drops columns
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
    creates a new column that records the year of an 
    observation
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
    given a datatime column creates new columns with cyclic 
    sine,cosine representations of months in year 1--12, 
    days in year 1--365, hours in day 0--23.
    
    """
    def __init__(self, 
                column = 'STATION_DATE_TIME',
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






#============= Feature Engineering (Pre Train-Test Split)======================

class SubtractColumns(BaseEstimator,TransformerMixin):
    """
    creates a new column whose values are from taking the 
    difference between two given columns
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