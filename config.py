"""
Configuration file for SHAP Stability Analysis Project
Student: Keisuke Nishioka (Matrikelnummer: 10081049)
"""

import numpy as np

# Random Seeds for Reproducibility
RANDOM_SEEDS = [42, 123, 456, 789, 1011, 2022, 3033, 4044, 5055, 6066]
N_SEEDS = len(RANDOM_SEEDS)

# Data Subsampling Rates
SUBSAMPLE_RATES = [0.5, 0.75, 1.0]  # 50%, 75%, 100%

# Dataset Configuration
DATASETS = {
    'adult': {
        'name': 'Adult Income',
        'source': 'UCI',
        'task': 'classification',
        'target': 'income',
        'min_samples': 1000
    },
    'boston': {
        'name': 'Boston Housing',
        'source': 'sklearn',
        'task': 'regression',
        'target': None,  # sklearn dataset
        'min_samples': 100
    },
    'wine': {
        'name': 'Wine Quality',
        'source': 'UCI',
        'task': 'classification',
        'target': 'quality',
        'min_samples': 1000
    }
}

# Model Configuration
MODELS = {
    'xgboost': {
        'name': 'XGBoost',
        'shap_method': 'TreeSHAP',
        'params': {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'random_state': None  # Set per seed
        }
    },
    'random_forest': {
        'name': 'Random Forest',
        'shap_method': 'TreeSHAP',
        'params': {
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': None  # Set per seed
        }
    },
    'logistic_regression': {
        'name': 'Logistic Regression',
        'shap_method': 'KernelSHAP',
        'params': {
            'max_iter': 1000,
            'random_state': None  # Set per seed
        }
    }
}

# SHAP Configuration
SHAP_CONFIG = {
    'tree_explainer': {
        'check_additivity': False  # Faster computation
    },
    'kernel_explainer': {
        'nsamples': 100,  # Number of samples for KernelSHAP
        'l1_reg': 'auto'
    }
}

# Stability Analysis Configuration
STABILITY_CONFIG = {
    'top_k_features': [3, 5, 10],  # Top-k features for consistency analysis
    'n_test_samples': 100,  # Number of test instances to analyze
    'correlation_method': 'spearman'  # 'spearman' or 'pearson'
}

# Output Directories
OUTPUT_DIRS = {
    'figures': 'results/figures',
    'tables': 'results/tables',
    'shap_values': 'results/shap_values',
    'models': 'results/models'
}

# Visualization Settings
PLOT_CONFIG = {
    'figsize': (10, 6),
    'dpi': 300,
    'style': 'seaborn-v0_8',
    'fontsize': 12
}
