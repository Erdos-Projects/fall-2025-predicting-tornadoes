import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




# Compare feature distributions between tornado and non-tornado cases

def plot_feature_distributions(X, y, features_to_plot, dataset_name='Train'):
    """
    Plot distributions of features split by class
    """
    n_features = len(features_to_plot)
    n_cols = 3
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    axes = axes.flatten() if n_features > 1 else [axes]
    
    for idx, feature in enumerate(features_to_plot):
        ax = axes[idx]
        
        # Get feature values for each class
        tornado_vals = X[y == 1][feature]
        no_tornado_vals = X[y == 0][feature]
        
        # Plot histograms
        ax.hist(no_tornado_vals, bins=50, alpha=0.5, label='No Tornado', density=True)
        ax.hist(tornado_vals, bins=50, alpha=0.5, label='Tornado', density=True)
        
        ax.set_xlabel(feature)
        ax.set_ylabel('Density')
        ax.set_title(f'{feature} Distribution ({dataset_name})')
        ax.legend()
        
        # Print summary stats
        print(f"\n{feature}:")
        print(f"  No Tornado: mean={no_tornado_vals.mean():.3f}, std={no_tornado_vals.std():.3f}")
        print(f"  Tornado: mean={tornado_vals.mean():.3f}, std={tornado_vals.std():.3f}")
    
    # Hide extra subplots
    for idx in range(len(features_to_plot), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.show()




# Analyze prediction errors
def error_analysis(X, y_true, y_pred_proba, threshold=0.5, dataset_name='Validation'):
    """
    Analyze false positives and false negatives
    """
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # Identify different error types
    true_positives = (y_true == 1) & (y_pred == 1)
    false_positives = (y_true == 0) & (y_pred == 1)
    true_negatives = (y_true == 0) & (y_pred == 0)
    false_negatives = (y_true == 1) & (y_pred == 0)
    
    print(f"\n{dataset_name} Set Error Analysis (threshold={threshold}):")
    print(f"True Positives: {true_positives.sum()}")
    print(f"False Positives: {false_positives.sum()}")
    print(f"True Negatives: {true_negatives.sum()}")
    print(f"False Negatives: {false_negatives.sum()}")
    
    # Look at prediction probabilities for each group
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # True Positives
    if true_positives.sum() > 0:
        axes[0,0].hist(y_pred_proba[true_positives], bins=20, edgecolor='black')
        axes[0,0].set_title(f'True Positives (n={true_positives.sum()})')
        axes[0,0].set_xlabel('Predicted Probability')
        axes[0,0].axvline(threshold, color='red', linestyle='--', label='Threshold')
        axes[0,0].legend()
    
    # False Positives
    if false_positives.sum() > 0:
        axes[0,1].hist(y_pred_proba[false_positives], bins=20, edgecolor='black')
        axes[0,1].set_title(f'False Positives (n={false_positives.sum()})')
        axes[0,1].set_xlabel('Predicted Probability')
        axes[0,1].axvline(threshold, color='red', linestyle='--', label='Threshold')
        axes[0,1].legend()
    
    # True Negatives
    if true_negatives.sum() > 0:
        axes[1,0].hist(y_pred_proba[true_negatives], bins=20, edgecolor='black')
        axes[1,0].set_title(f'True Negatives (n={true_negatives.sum()})')
        axes[1,0].set_xlabel('Predicted Probability')
        axes[1,0].axvline(threshold, color='red', linestyle='--', label='Threshold')
        axes[1,0].legend()
    
    # False Negatives 
    if false_negatives.sum() > 0:
        axes[1,1].hist(y_pred_proba[false_negatives], bins=20, edgecolor='black')
        axes[1,1].set_title(f'False Negatives (n={false_negatives.sum()})')
        axes[1,1].set_xlabel('Predicted Probability')
        axes[1,1].axvline(threshold, color='red', linestyle='--', label='Threshold')
        axes[1,1].legend()
    
    plt.tight_layout()
    plt.show()
    
    # Feature analysis for errors
    print("\n--- Feature Analysis for Errors ---")
    
    if false_positives.sum() > 0:
        print("\nFalse Positives (False Alarms) - Top feature values:")
        fp_features = X[false_positives].select_dtypes(include=[np.number]).mean()
        print(fp_features.sort_values(ascending=False).head(10))
    
    if false_negatives.sum() > 0:
        print("\nFalse Negatives (Missed Tornadoes) - Top feature values:")
        fn_features = X[false_negatives].select_dtypes(include=[np.number]).mean()
        print(fn_features.sort_values(ascending=False).head(10))
    
    if true_positives.sum() > 0:
        print("\nTrue Positives (Caught Tornadoes) - Top feature values:")
        tp_features = X[true_positives].select_dtypes(include=[np.number]).mean()
        print(tp_features.sort_values(ascending=False).head(10))



