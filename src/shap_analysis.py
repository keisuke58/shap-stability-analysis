"""
SHAP explanation generation utilities
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import numpy as np
import pandas as pd
import shap
import joblib
import os
from tqdm import tqdm


def compute_tree_shap(model, X_test, n_samples=100):
    """
    Compute TreeSHAP values for tree-based models
    
    Args:
        model: Trained tree-based model (XGBoost or Random Forest)
        X_test: Test features
        n_samples: Number of samples to explain (None for all)
    
    Returns:
        SHAP values (numpy array)
    """
    # Select samples if needed
    if n_samples is not None and n_samples < len(X_test):
        indices = np.random.choice(len(X_test), size=n_samples, replace=False)
        X_sample = X_test.iloc[indices] if isinstance(X_test, pd.DataFrame) else X_test[indices]
    else:
        X_sample = X_test
    
    # Create TreeExplainer
    # For XGBoost compatibility with newer versions
    if hasattr(model, 'get_booster'):  # XGBoost
        # Use Explainer for XGBoost (more compatible with newer versions)
        try:
            # Try TreeExplainer first (faster)
            explainer = shap.TreeExplainer(model)
        except:
            # Fallback to Explainer with predict function
            explainer = shap.Explainer(
                model.predict_proba if hasattr(model, 'predict_proba') else model.predict,
                X_sample.iloc[:10] if isinstance(X_sample, pd.DataFrame) else X_sample[:10]
            )
    else:  # Random Forest
        explainer = shap.TreeExplainer(model)
    
    # Compute SHAP values
    shap_values = explainer.shap_values(X_sample)
    
    # Handle multi-class case
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # Use positive class for binary classification
    
    return shap_values, X_sample


def compute_kernel_shap(model, X_train, X_test, n_samples=100, nsamples_shap=100):
    """
    Compute KernelSHAP values for non-tree models
    
    Args:
        model: Trained model (Logistic Regression, etc.)
        X_train: Training features (for background)
        X_test: Test features
        n_samples: Number of test samples to explain
        nsamples_shap: Number of samples for KernelSHAP computation
    
    Returns:
        SHAP values (numpy array)
    """
    # Select background samples
    n_background = min(100, len(X_train))
    background_indices = np.random.choice(len(X_train), size=n_background, replace=False)
    X_background = X_train.iloc[background_indices] if isinstance(X_train, pd.DataFrame) else X_train[background_indices]
    
    # Create KernelExplainer
    explainer = shap.KernelExplainer(model.predict_proba if hasattr(model, 'predict_proba') else model.predict, X_background)
    
    # Select test samples
    if n_samples is not None and n_samples < len(X_test):
        indices = np.random.choice(len(X_test), size=n_samples, replace=False)
        X_sample = X_test.iloc[indices] if isinstance(X_test, pd.DataFrame) else X_test[indices]
    else:
        X_sample = X_test
    
    # Compute SHAP values
    shap_values = explainer.shap_values(X_sample, nsamples=nsamples_shap)
    
    # Handle multi-class case
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # Use positive class for binary classification
    
    return shap_values, X_sample


def compute_shap_for_model(model, X_train, X_test, model_type='xgboost', n_samples=100, **kwargs):
    """
    Compute SHAP values for a given model
    
    Args:
        model: Trained model
        X_train: Training features
        X_test: Test features
        model_type: 'xgboost', 'random_forest', or 'logistic_regression'
        n_samples: Number of samples to explain
        **kwargs: Additional parameters for SHAP computation
    
    Returns:
        shap_values, X_sample
    """
    if model_type in ['xgboost', 'random_forest']:
        return compute_tree_shap(model, X_test, n_samples=n_samples)
    elif model_type in ['logistic_regression', 'ridge']:
        return compute_kernel_shap(model, X_train, X_test, n_samples=n_samples, **kwargs)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def save_shap_values(shap_values, filepath):
    """
    Save SHAP values to file
    
    Args:
        shap_values: SHAP values array
        filepath: Path to save file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.savez_compressed(filepath, shap_values=shap_values)


def load_shap_values(filepath):
    """
    Load SHAP values from file
    
    Args:
        filepath: Path to saved file
    
    Returns:
        SHAP values array
    """
    data = np.load(filepath)
    return data['shap_values']


def compute_shap_multiple_seeds(models_dict, X_train, X_test, model_type, 
                                 random_seeds, n_samples=100, save_dir=None):
    """
    Compute SHAP values for multiple random seeds
    
    Args:
        models_dict: Dictionary of models {seed: model}
        X_train: Training features
        X_test: Test features
        model_type: Model type string
        random_seeds: List of random seeds
        n_samples: Number of samples to explain
        save_dir: Directory to save results (optional)
    
    Returns:
        Dictionary {seed: (shap_values, X_sample)}
    """
    results = {}
    
    for seed in tqdm(random_seeds, desc=f"Computing SHAP for {model_type}"):
        model = models_dict[seed]
        shap_values, X_sample = compute_shap_for_model(
            model, X_train, X_test, model_type, n_samples=n_samples
        )
        results[seed] = (shap_values, X_sample)
        
        # Save if directory provided
        if save_dir:
            save_path = os.path.join(save_dir, f"{model_type}_seed_{seed}_shap.npz")
            save_shap_values(shap_values, save_path)
    
    return results
