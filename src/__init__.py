from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn import set_config
set_config(transform_output="pandas")
import numpy as np
import pandas as pd

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
        mask_type_nan = X[self.type_col].isna()
        mask_speed_0 = X[self.speed_col] == 0
        calm_winds_index = X[(mask_speed_0)&(mask_type_nan)].index
        X.loc[calm_winds_index, [self.type_col]] = 'C'
        return X
    
    
    
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
        if self.columns is None:
            return X.dropna()
        else:
            return X.dropna(subset=self.columns)
            
            
class DropDuplicates(BaseEstimator,TransformerMixin):
    """
    Drops duplicated rows.
    """
    def __init__(self):
        pass
    def fit(self, X,y=None):
        # nothing to learn
        return self 
    
    def transform(self,X):
        X = X.copy()
        return X.drop_duplicates()
            