"""
Model training utilities
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from xgboost import XGBClassifier, XGBRegressor
import joblib
import os


def train_xgboost(X_train, y_train, task='classification', random_state=42, **kwargs):
    """
    Train XGBoost model
    
    Args:
        X_train: Training features
        y_train: Training target
        task: 'classification' or 'regression'
        random_state: Random seed
        **kwargs: Additional XGBoost parameters
    
    Returns:
        Trained model
    """
    default_params = {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': random_state,
        'n_jobs': -1,
        'base_score': 0.5  # Explicit base_score for SHAP compatibility
    }
    default_params.update(kwargs)
    
    if task == 'classification':
        model = XGBClassifier(**default_params)
    else:
        model = XGBRegressor(**default_params)
    
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train, task='classification', random_state=42, **kwargs):
    """
    Train Random Forest model
    
    Args:
        X_train: Training features
        y_train: Training target
        task: 'classification' or 'regression'
        random_state: Random seed
        **kwargs: Additional Random Forest parameters
    
    Returns:
        Trained model
    """
    default_params = {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': random_state,
        'n_jobs': -1  # Use all CPU cores
    }
    default_params.update(kwargs)
    
    if task == 'classification':
        model = RandomForestClassifier(**default_params)
    else:
        model = RandomForestRegressor(**default_params)
    
    model.fit(X_train, y_train)
    return model


def train_logistic_regression(X_train, y_train, random_state=42, **kwargs):
    """
    Train Logistic Regression model
    
    Args:
        X_train: Training features
        y_train: Training target
        random_state: Random seed
        **kwargs: Additional Logistic Regression parameters
    
    Returns:
        Trained model
    """
    default_params = {
        'max_iter': 1000,
        'random_state': random_state,
        'n_jobs': -1
    }
    default_params.update(kwargs)
    
    model = LogisticRegression(**default_params)
    model.fit(X_train, y_train)
    return model


def train_ridge_regression(X_train, y_train, random_state=42, **kwargs):
    """
    Train Ridge Regression model (for regression tasks)
    
    Args:
        X_train: Training features
        y_train: Training target
        random_state: Random seed
        **kwargs: Additional Ridge parameters
    
    Returns:
        Trained model
    """
    default_params = {
        'alpha': 1.0,
        'random_state': random_state
    }
    default_params.update(kwargs)
    
    model = Ridge(**default_params)
    model.fit(X_train, y_train)
    return model


def get_task_type(y):
    """
    Determine if task is classification or regression
    
    Args:
        y: Target variable
    
    Returns:
        'classification' or 'regression'
    """
    if y.dtype == 'object' or y.dtype.name == 'category':
        return 'classification'
    elif len(np.unique(y)) < 20 and y.dtype == 'int':
        return 'classification'
    else:
        return 'regression'


def save_model(model, filepath):
    """
    Save trained model
    
    Args:
        model: Trained model
        filepath: Path to save model
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)


def load_model(filepath):
    """
    Load saved model
    
    Args:
        filepath: Path to saved model
    
    Returns:
        Loaded model
    """
    return joblib.load(filepath)
