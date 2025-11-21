import pandas as pd
from sklearn.model_selection import TimeSeriesSplit


def temporal_train_test_split(df, date_column='DATE', test_years=1, verbose = True):
    """
    Split data by time - train on early years, test on recent years.
    
    Parameters:
    -----------
    df : pd.DataFrame
    date_column : str
        Name of datetime column
    test_years : int
        Number of years to reserve for testing
    
    Returns:
    --------
    train_df, test_df
    """
    # Ensure datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Get the cutoff date
    max_date = df[date_column].max()
    cutoff_date = max_date - pd.DateOffset(years=test_years)
    
    # Split
    train_df = df[df[date_column] < cutoff_date].copy()
    test_df = df[df[date_column] >= cutoff_date].copy()
    
    if verbose:
        print(f"Train period: {train_df[date_column].min()} to {train_df[date_column].max()}")
        print(f"Test period: {test_df[date_column].min()} to {test_df[date_column].max()}")
        print(f"Train size: {len(train_df):,} ({len(train_df)/len(df)*100:.1f}%)")
        print(f"Test size: {len(test_df):,} ({len(test_df)/len(df)*100:.1f}%)")
        print(f"Train tornado rate: {train_df['TORNADO_OCCURRENCE'].mean():.4%}")
        print(f"Test tornado rate: {test_df['TORNADO_OCCURRENCE'].mean():.4%}")
    
    return train_df, test_df







import numpy as np
from sklearn.model_selection import BaseCrossValidator

class YearlyTemporalWindowSplit(BaseCrossValidator):
    def __init__(self, start_year=None, end_year=None, val_window_size=2):
        self.start_year = start_year
        self.end_year = end_year
        self.val_window_size = val_window_size
    
    def get_n_splits(self, X=None, y=None, groups=None):
        if self.start_year and self.end_year:
        # Number of non-overlapping windows that fit
            total_years = self.end_year - self.start_year + 1
            n_folds = total_years // self.val_window_size
            return n_folds
        return None
    
    def split(self, X, y=None, groups=None):
        years = X['DATE'].dt.year.values
        unique_years = np.sort(np.unique(years))
        
        start = self.start_year if self.start_year else unique_years[self.val_window_size]
        end = self.end_year if self.end_year else unique_years[-1]
        
        val_start_year = start
        
        while val_start_year + self.val_window_size - 1 <= end:
            val_end_year = val_start_year + self.val_window_size - 1
            
            # Train: all years before validation window
            train_idx = np.where(years < val_start_year)[0]
            
            # Validation: val_window_size consecutive years
            val_idx = np.where((years >= val_start_year) & (years <= val_end_year))[0]
            
            if len(train_idx) > 0 and len(val_idx) > 0:
                yield train_idx, val_idx
            
            # IMPORTANT: Jump by val_window_size (no overlap)
            val_start_year += self.val_window_size  




def print_cv_split_check(cv_splitter, data, date_column='DATE', target_column='TORNADO_OCCURRENCE'):
    """
    Print detailed information about cross-validation splits.
    
    Parameters
    ----------
    cv_splitter : cross-validator
        The CV splitter to check (e.g., YearlyTemporalWindowSplit)
    data : pd.DataFrame
        The full dataset with date and target columns
    date_column : str
        Name of the date column
    target_column : str
        Name of the target column
    """
    print("=" * 80)
    print("CROSS-VALIDATION SPLIT VERIFICATION")
    print("=" * 80)
    
    n_splits = cv_splitter.get_n_splits(data)
    print(f"\nTotal number of folds: {n_splits}")
    print(f"Dataset size: {len(data):,} samples")
    print(f"Overall tornado rate: {data[target_column].mean():.4%}")
    print("\n" + "-" * 80)
    
    fold_stats = []
    
    for fold_idx, (train_idx, val_idx) in enumerate(cv_splitter.split(data), 1):
        # Get train and val data
        train_data = data.iloc[train_idx]
        val_data = data.iloc[val_idx]
        
        # Date ranges
        train_start = train_data[date_column].min()
        train_end = train_data[date_column].max()
        val_start = val_data[date_column].min()
        val_end = val_data[date_column].max()
        
        # Check for temporal leakage
        leakage = train_end >= val_start
        
        # Tornado statistics
        train_tornadoes = train_data[target_column].sum()
        val_tornadoes = val_data[target_column].sum()
        train_rate = train_data[target_column].mean()
        val_rate = val_data[target_column].mean()
        
        # Store for summary
        fold_stats.append({
            'fold': fold_idx,
            'train_size': len(train_data),
            'val_size': len(val_data),
            'train_rate': train_rate,
            'val_rate': val_rate,
            'train_tornadoes': train_tornadoes,
            'val_tornadoes': val_tornadoes
        })
        
        # Print fold details
        print(f"\nFold {fold_idx}:")
        print(f"  Train: {train_start.date()} to {train_end.date()}")
        print(f"         {len(train_data):,} samples, {train_tornadoes:,} tornadoes ({train_rate:.4%})")
        print(f"  Val:   {val_start.date()} to {val_end.date()}")
        print(f"         {len(val_data):,} samples, {val_tornadoes:,} tornadoes ({val_rate:.4%})")
        
        # Warn about issues
        if leakage:
            print(f" WARNING: Temporal leakage detected! Train ends after val starts.")
        if val_tornadoes < 5:
            print(f" WARNING: Very few tornadoes in validation set ({val_tornadoes})")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    fold_stats_df = pd.DataFrame(fold_stats)
    
    print(f"\nTrain set sizes:")
    print(f"  Min: {fold_stats_df['train_size'].min():,}")
    print(f"  Max: {fold_stats_df['train_size'].max():,}")
    print(f"  Mean: {fold_stats_df['train_size'].mean():,.0f}")
    
    print(f"\nValidation set sizes:")
    print(f"  Min: {fold_stats_df['val_size'].min():,}")
    print(f"  Max: {fold_stats_df['val_size'].max():,}")
    print(f"  Mean: {fold_stats_df['val_size'].mean():,.0f}")
    
    print(f"\nTrain tornado rates:")
    print(f"  Min: {fold_stats_df['train_rate'].min():.4%}")
    print(f"  Max: {fold_stats_df['train_rate'].max():.4%}")
    print(f"  Mean: {fold_stats_df['train_rate'].mean():.4%}")
    print(f"  Std: {fold_stats_df['train_rate'].std():.4%}")
    
    print(f"\nValidation tornado rates:")
    print(f"  Min: {fold_stats_df['val_rate'].min():.4%}")
    print(f"  Max: {fold_stats_df['val_rate'].max():.4%}")
    print(f"  Mean: {fold_stats_df['val_rate'].mean():.4%}")
    print(f"  Std: {fold_stats_df['val_rate'].std():.4%}")
    
    print(f"\nValidation tornado counts:")
    print(f"  Min: {fold_stats_df['val_tornadoes'].min():.0f}")
    print(f"  Max: {fold_stats_df['val_tornadoes'].max():.0f}")
    print(f"  Mean: {fold_stats_df['val_tornadoes'].mean():.1f}")
    
    # Check for overlaps between consecutive folds
    print("\n" + "=" * 80)
    print("TEMPORAL ORDERING CHECK")
    print("=" * 80)
    
    all_clear = True
    for fold_idx, (train_idx, val_idx) in enumerate(cv_splitter.split(data), 1):
        train_data = data.iloc[train_idx]
        val_data = data.iloc[val_idx]
        
        if train_data[date_column].max() >= val_data[date_column].min():
            print(f" Fold {fold_idx}: Train ends AFTER val starts (LEAKAGE!)")
            all_clear = False
    
    if all_clear:
        print("All folds maintain proper temporal ordering (no leakage)")
    
    print("\n" + "=" * 80)
    
    return fold_stats_df


