
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.metrics import (classification_report, 
                            roc_auc_score,
                            confusion_matrix,
                            average_precision_score,
                            precision_recall_curve,
                            fbeta_score,
                            recall_score,
                            precision_score,
                            brier_score_loss,
                            ConfusionMatrixDisplay)


# A model (or really model collection) utility class. Used for
# collecting information from and initializing scikit learn estimators.
# Made to easily fit multiple pipelines, store metrics, and information for figures.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.metrics import (classification_report, 
                            roc_auc_score,
                            confusion_matrix,
                            average_precision_score,
                            precision_recall_curve,
                            fbeta_score,
                            recall_score,
                            precision_score,
                            brier_score_loss,
                            ConfusionMatrixDisplay)


class ModelingUtilities():
    """
    Utility class for managing multiple scikit-learn models with method chaining.
    
    Provides streamlined methods for fitting multiple models, computing metrics,
    tuning thresholds, and generating visualizations. Designed for binary
    classification tasks with probability predictions.
    
    Parameters
    ----------
    dict_of_models : dict
        Dictionary mapping model names (str) to unfitted scikit-learn pipelines
        or estimators.
    
    Attributes
    ----------
    names_of_models : list
        List of model names from dict_of_models keys.
    models : list
        List of model objects from dict_of_models values.
    dict_of_fitted_models : dict
        Dictionary of fitted models after calling fit_models().
    test_probabilities : dict
        Dictionary of predicted probabilities on test data.
    training_probabilities : dict
        Dictionary of predicted probabilities on training data.
    testing_type : str
        Label for current evaluation ('validation', 'test', etc.).
    precs_recs_thresholds : dict
        Precision-recall curves data for each model.
    """

    def __init__(self, dict_of_models: dict):
        self.dict_of_models = dict_of_models
        self.names_of_models = list(dict_of_models.keys())
        self.models = list(dict_of_models.values())
        
        
    def fit_models(self, X_train, y_train):
        """
        Fit all models in dict_of_models on training data.
        
        Parameters
        ----------
        X_train : array-like of shape (n_samples, n_features)
            Training features.
        y_train : array-like of shape (n_samples,)
            Training target values.
        
        Returns
        -------
        self : ModelingUtilities
            Returns self for method chaining.
        """
        self.dict_of_fitted_models = {}
        for name_of_model, model in self.dict_of_models.items():
            fitted_model = model.fit(X_train, y_train)
            print(f"Fitting model {name_of_model}")
            self.dict_of_fitted_models[name_of_model] = fitted_model
        return self
    
    def save_test_probabilities(self, X_val, testing_type='Validation'): 
        """
        Generate and store test probability predictions for all fitted models.
        
        Parameters
        ----------
        X_val : array-like of shape (n_samples, n_features)
            Validation/test features.
        testing_type : str, default='Validation'
            Label for this evaluation set (e.g., 'validation', 'test').
        
        Returns
        -------
        self : ModelingUtilities
            Returns self for method chaining.
        """
        self.testing_type = testing_type
        self.test_probabilities = {}
        for name_of_model, fitted_models in self.dict_of_fitted_models.items():
            self.test_probabilities[name_of_model] = fitted_models.predict_proba(X_val)[:, 1]
        return self
    
    def save_training_probabilities(self, X_train): 
        """
        Generate and store training probability predictions for all fitted models.
        
        Parameters
        ----------
        X_train : array-like of shape (n_samples, n_features)
            Training features.
        
        Returns
        -------
        self : ModelingUtilities
            Returns self for method chaining.
        """
        self.training_probabilities = {}
        for name_of_model, fitted_models in self.dict_of_fitted_models.items():
            self.training_probabilities[name_of_model] = fitted_models.predict_proba(X_train)[:, 1]
        return self
            
            
    def get_predicts(self, threshold_dict=None, use_test_probs=True):
        """
        Convert probability predictions to binary predictions using thresholds.
        
        Parameters
        ----------
        threshold_dict : dict, optional
            Dictionary mapping model names to classification thresholds.
            If None, uses 0.5 for all models.
        use_test_probs : bool, default=True
            If True, use test_probabilities. If False, use training_probabilities.
        
        Returns
        -------
        dict_of_predictions : dict
            Dictionary mapping model names to binary predictions (0/1).
        """
        dict_of_predictions = {}
        if threshold_dict is None:
            threshold_dict = {model_name: .5 for model_name in self.dict_of_models.keys()}
        
        probs_to_use = self.test_probabilities if use_test_probs else self.training_probabilities
        
        for name_of_model, probs in probs_to_use.items():
            dict_of_predictions[name_of_model] = (probs >= threshold_dict[name_of_model]).astype(int)
        return dict_of_predictions

    
    def get_threshold_metrics(self, y_val, beta, threshold_dict=None, return_dataframe=False):
        """
        Compute classification metrics at specified thresholds.
        
        Parameters
        ----------
        y_val : array-like of shape (n_samples,)
            True target values.
        beta : float
            Beta parameter for F-beta score calculation.
        threshold_dict : dict, optional
            Dictionary mapping model names to thresholds. If None, uses 0.5.
        return_dataframe : bool, default=False
            If True, return pandas DataFrame; otherwise return dict.
        
        Returns
        -------
        dict or pd.DataFrame
            Classification metrics for each model including average precision,
            F-beta score, recall, precision, ROC-AUC, and Brier score.
        """
        dict_of_metrics = {}
        testing_type = self.testing_type
        if threshold_dict is None:
            threshold_dict = {}
            for model_name, fitted_model in self.dict_of_fitted_models.items():
                threshold_dict[model_name] = 0.5
                
        dict_of_predictions = self.get_predicts(threshold_dict, use_test_probs=True)
    
        for model_name, fitted_model in self.dict_of_fitted_models.items():
            params = fitted_model.get_params()
            probs = self.test_probabilities[model_name]
            preds = dict_of_predictions[model_name]
        
            metrics = {
                "Model": model_name,
                "Parameters": params,
                f"{testing_type}_Threshold": threshold_dict[model_name],
                f"{testing_type}_avg_precision": average_precision_score(y_val, probs),
                f"{testing_type}_F{beta}": fbeta_score(y_val, preds, beta=beta, zero_division=0),
                f"{testing_type}_Recall": recall_score(y_val, preds),
                f"{testing_type}_Precision": precision_score(y_val, preds, zero_division=0),
                f"{testing_type}_roc_auc": roc_auc_score(y_val, probs),
                f"{testing_type}_brier_score": brier_score_loss(y_val, probs)
            }
                
            dict_of_metrics[model_name] = metrics
            
        if not return_dataframe:
            result = dict_of_metrics
        else:
            final_df = pd.DataFrame()
            for model_name, model_metrics in dict_of_metrics.items():
                model_metrics_df = pd.DataFrame([model_metrics])
                final_df = pd.concat([final_df, model_metrics_df], ignore_index=True)
            result = final_df
                
        return result
    
    
    def get_test_best_fbeta_thresholds(self, y_val, beta=2):
        """
        Find optimal classification thresholds that maximize F-beta score using test data.
        
        Parameters
        ----------
        y_val : array-like of shape (n_samples,)
            True target values.
        beta : float, default=2
            Beta parameter for F-beta score.
        
        Returns
        -------
        dict_of_best_thresholds : dict
            Dictionary mapping model names to optimal thresholds.
        """
        dict_of_best_thresholds = {}
        self.precs_recs_thresholds = {}
        
        for model_name, fitted_model in self.dict_of_fitted_models.items():
            val_probs = self.test_probabilities[model_name]
            precs, recalls, thresholds = precision_recall_curve(y_val, val_probs)
            self.precs_recs_thresholds[model_name] = (precs, recalls, thresholds)
            f_scores = []
            for i in range(len(thresholds)):
                prec = precs[i]
                rec = recalls[i]
                if prec + rec > 0:
                    f = (1 + beta**2) * (prec * rec) / (beta**2 * prec + rec)
                else:
                    f = 0
                f_scores.append(f)
    
            best_idx = np.argmax(f_scores)
            best_threshold = thresholds[best_idx]
            dict_of_best_thresholds[model_name] = best_threshold
        
        return dict_of_best_thresholds
    
    
    def get_train_best_fbeta_thresholds(self, y_train, beta=2):
        """
        Find optimal classification thresholds that maximize F-beta score using training data.
        
        Parameters
        ----------
        y_train : array-like of shape (n_samples,)
            True target values for training data.
        beta : float, default=2
            Beta parameter for F-beta score.
        
        Returns
        -------
        dict_of_best_thresholds : dict
            Dictionary mapping model names to optimal thresholds.
        
        Saves the dictionary of best fbeta thresholds for training data
        as self.train_best_thresholds
        """
        dict_of_best_thresholds = {}
        precs_recs_thresholds = {}
        
        for model_name, fitted_model in self.dict_of_fitted_models.items():
            train_probs = self.training_probabilities[model_name]
            precs, recalls, thresholds = precision_recall_curve(y_train, train_probs)
            precs_recs_thresholds[model_name] = (precs, recalls, thresholds)
            f_scores = []
            for i in range(len(thresholds)):
                prec = precs[i]
                rec = recalls[i]
                if prec + rec > 0:
                    f = (1 + beta**2) * (prec * rec) / (beta**2 * prec + rec)
                else:
                    f = 0
                f_scores.append(f)
    
            best_idx = np.argmax(f_scores)
            best_threshold = thresholds[best_idx]
            dict_of_best_thresholds[model_name] = best_threshold
        self.train_best_thresholds = dict_of_best_thresholds
        return dict_of_best_thresholds
    
    
    def get_metrics(self, y_data, beta=2, use_train_threshold=True, return_dataframe=False):
        """
        Compute metrics using thresholds optimized for F-beta score.
        
        Parameters
        ----------
        y_data : array-like of shape (n_samples,)
            True target values (matches whichever probability set is being used for threshold).
        beta : float, default=2
            Beta parameter for F-beta score calculation.
        use_train_threshold : bool, default=True
            If True, use training probabilities to find threshold.
            If False, use test probabilities to find threshold.
        return_dataframe : bool, default=False
            If True, return pandas DataFrame; otherwise return dict.
        
        Returns
        -------
        dict or pd.DataFrame
            Classification metrics at F-beta-optimal thresholds for each model.
        """
        if use_train_threshold:
            thresholds = self.train_best_thresholds 
        else:
            thresholds = self.get_test_best_fbeta_thresholds(y_data, beta=beta)
        
        # Always evaluate on test data using the selected threshold
        final_df = self.get_threshold_metrics(y_data, threshold_dict=thresholds, 
                                              beta=beta, return_dataframe=return_dataframe)
        return final_df
    
    
    def plt_precision_recall_curve(self, y_val, use_train_threshold=True, beta=2, save_to=None):
        """
        Plot precision-recall curves with F-beta points marked.
        
        Parameters
        ----------
        y_val : array-like of shape (n_samples,)
            True target values.
        beta : float, default=2
            Beta parameter for F-beta score.
        save_to : str or pathlib.Path, optional
            File path to save the figure. If None, figure is not saved.
        
        Returns
        -------
        None
        """
        # Use test probabilities for PR curve
        metrics_dict = self.get_metrics(y_data=y_val, beta=beta, use_train_threshold=use_train_threshold, return_dataframe=False)
        testing_type = self.testing_type
        save_to = pathlib.Path(save_to)
        
        plt.figure(figsize=(10, 10))
        f_points = {}
        
        for model_name,  model in self.dict_of_fitted_models.items():
            thresh_recall = metrics_dict[model_name][f'{testing_type}_Recall']
            thresh_prec = metrics_dict[model_name][f'{testing_type}_Precision']
            f_score = metrics_dict[model_name][f"{testing_type}_F{beta}"]
            val_probs = self.test_probabilities[model_name]
            precs, recalls, thresholds = precision_recall_curve(y_val, val_probs)
            plt.plot(recalls, precs, label=model_name)
            f_points[model_name] = f_score
            plt.scatter(thresh_recall, thresh_prec, edgecolor='black', s=70)
            plt.text(thresh_recall + 0.01, thresh_prec + 0.01, 
                    f"F{beta}={f_score:.2f}", fontsize=8)
    
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision–Recall Curves with Best F2 Points')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(save_to)
        plt.show()
        
        return None

    def create_confusion_matrix(self, y_val, beta=2, use_train_threshold=True, save_to_dir=None):
        """
        Create and save confusion matrices at F-beta-optimal thresholds.
        
        Parameters
        ----------
        y_val : array-like of shape (n_samples,)
            True target values.
        beta : float, default=2
            Beta parameter for F-beta score.
        use_train_threshold : bool, default=False
            If True, use training data to find threshold. If False, use test data.
        save_to_dir : str or pathlib.Path, optional
            Directory to save confusion matrix plots.
        
        Returns
        -------
        None
        """
        if use_train_threshold:
            thresholds = self.train_best_thresholds
        else:
            thresholds = self.get_test_best_fbeta_thresholds(y_val, beta=beta)
            
        predictions = self.get_predicts(threshold_dict=thresholds, use_test_probs=True)
        
        save_to_dir = pathlib.Path(save_to_dir)
        
        for model_name, fitted_model in self.dict_of_fitted_models.items():
            best_threshold_cm = confusion_matrix(y_val, predictions[model_name], 
                                                 labels=[False, True])
            best_threshold_cmd = ConfusionMatrixDisplay(best_threshold_cm,
                                                        display_labels=['No Tornado', 'Tornado'])
            best_threshold_cmd.plot()
            plt.title(f'{model_name} - Threshold: {thresholds[model_name]:.4f}')
            plt.savefig(save_to_dir / pathlib.Path(f"{model_name}_confusion_matrix.png"))
            plt.show()
        return None

def train_val_model_metrics_df(models_dict: dict, data_dict=None):
    """
    Train models and compute metrics on both training and validation data.
    
    Parameters
    ----------
    models_dict : dict
        Dictionary mapping model names to unfitted scikit-learn models/pipelines.
    data_dict : dict, optional
        Nested dictionary with structure:
        {
            'train': {'X': X_train, 'y': y_train},
            'validation': {'X': X_val, 'y': y_val}
        }
    
    Returns
    -------
    final_df : pd.DataFrame
        DataFrame with interleaved train/validation metrics for each model.
    """
    final_df_list = []
    models = ModelingUtilities(dict_of_models=models_dict)
    
    X_train = data_dict['train']['X']
    y_train = data_dict['train']['y']
    models.fit_models(X_train=X_train, y_train=y_train)
    
    # Compute training thresholds once upfront
    models.save_training_probabilities(X_train)
    models.get_train_best_fbeta_thresholds(y_train, beta=2)
    
    print("=" * 80)
    
    for data_type, X_or_y in data_dict.items():
        X_data = X_or_y['X']
        y_data = X_or_y['y']
        models.save_test_probabilities(X_val=X_data, testing_type=data_type)
        metrics_df = models.get_metrics(y_data=y_data,
                                        beta=2,
                                        use_train_threshold=True,
                                        return_dataframe=True)
        parameter_col = metrics_df['Parameters']
        metrics_df = metrics_df.drop(columns=['Parameters'], inplace=False) 
        final_df_list.append(metrics_df)

    final_df = final_df_list[0]
    
    for df in final_df_list[1:]:
        final_df = pd.merge(left=final_df, right=df, on=['Model'])
        
    num_cols = len(final_df.columns)
    shift = 7
    
    new_col_indices = [0]
    
    num_splits = len(list(data_dict.keys()))
    for i in range(2, shift + 1):
        shifted_indices = [i + shift * k for k in range(0, num_splits)]
        new_col_indices = new_col_indices + shifted_indices
    
    final_df = final_df.iloc[:, new_col_indices]
    final_df['Parameters'] = parameter_col
    
    return final_df


