import pandas as pd

import data.metadata.cleaned_feature_info as metadata

isd_conditional_meanings = metadata.isd_conditional_meanings

def handle_conditional_meanings(df, conditional_dict=isd_conditional_meanings):
    """
    Handle special cases where "missing" codes have conditional meanings.
    Uses the conditional_dict to dynamically apply rules.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with ISD parsed columns
    conditional_dict : dict
        Dictionary of conditional rules with structure:
        {feature: {condition_column: {condition_value: rule_details}}}
        
    Returns:
    --------
    pd.DataFrame : DataFrame with conditional meanings properly handled
    """
    import numpy as np
    
    df_clean = df.copy()
    
    # Iterate through each feature that has conditional rules
    for feature, condition_columns_dict in conditional_dict.items():
        
        # Skip if feature not in dataframe
        if feature not in df_clean.columns:
            continue
        
        # Iterate through each condition column for this feature
        for condition_column, rules in condition_columns_dict.items():
            
            # Skip if condition column not in dataframe
            if condition_column not in df_clean.columns:
                continue
            
            # Apply each conditional rule
            for condition_value, rule_details in rules.items():
                value_to_check = rule_details['value_to_check']
                interpretation = rule_details['interpretation']
                action = rule_details['action']
                meaning = rule_details['meaning']
                
            
    

                condition_mask = (
                    (df_clean[condition_column] == condition_value) & 
                    (df_clean[feature] == value_to_check)
                )
                
                num_matches = condition_mask.sum()
                
                if num_matches > 0:
                    print(f"  {feature}: Found {num_matches} '{interpretation}' cases ({meaning})")
                    
                    
                    
                    # Perform action based on rule
                    if action == 'create_flag':
                        # Create flag column
                        flag_column = f"{feature}_{interpretation}_flag"
                        if flag_column not in df_clean.columns:
                            df_clean[flag_column] = False
                            df_clean.loc[condition_mask, flag_column] = True
                        else: print("flag naming error")
                    
                    elif action == 'set_to_zero':
                        # Set the value to 0
                        df_clean.loc[condition_mask, feature] = 0
                    
                    elif action == 'set_to_calm':
                        # Set wind type to 'C' (calm)
                        df_clean.loc[condition_mask, feature] = 'C'
                    
                    elif action == 'set_to_max':
                        # Set to maximum reasonable value
                        if 'ceiling' in feature.lower():
                            df_clean.loc[condition_mask, feature] = 22000  # 30km ceiling
                        elif 'vis' in feature.lower():
                            df_clean.loc[condition_mask, feature] = 160000  # 160km visibility
                    
                    elif action == 'set_to_trace':
                        # Set to trace amount (0.5mm = 5 in tenths)
                        df_clean.loc[condition_mask, feature] = 5
    
    return df_clean