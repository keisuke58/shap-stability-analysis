"""
CPU環境用の最適化設定ファイル
Student: Keisuke Nishioka (Matrikelnummer: 10081049)

使用方法:
    import config_cpu as config
    または
    from config_cpu import RANDOM_SEEDS, STABILITY_CONFIG, etc.
"""

import numpy as np

# Random Seeds for Reproducibility (CPU環境用：少なめに設定)
RANDOM_SEEDS = [42, 123, 456, 789, 1011]  # 10個 → 5個に削減
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
        'target': None,
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

# Model Configuration (CPU環境用：パラメータを削減)
MODELS = {
    'xgboost': {
        'name': 'XGBoost',
        'shap_method': 'TreeSHAP',
        'params': {
            'n_estimators': 50,  # 100 → 50に削減
            'max_depth': 5,       # 6 → 5に削減
            'learning_rate': 0.1,
            'random_state': None,
            'n_jobs': -1          # 全CPUコアを使用
        }
    },
    'random_forest': {
        'name': 'Random Forest',
        'shap_method': 'TreeSHAP',
        'params': {
            'n_estimators': 50,   # 100 → 50に削減
            'max_depth': 8,       # 10 → 8に削減
            'random_state': None,
            'n_jobs': -1          # 全CPUコアを使用
        }
    },
    'logistic_regression': {
        'name': 'Logistic Regression',
        'shap_method': 'KernelSHAP',
        'params': {
            'max_iter': 1000,
            'random_state': None,
            'n_jobs': -1          # 全CPUコアを使用
        }
    }
}

# SHAP Configuration (CPU環境用：KernelSHAPのサンプル数を削減)
SHAP_CONFIG = {
    'tree_explainer': {
        'check_additivity': False  # Faster computation
    },
    'kernel_explainer': {
        'nsamples': 50,  # 100 → 50に削減（KernelSHAPは時間がかかる）
        'l1_reg': 'auto'
    }
}

# Stability Analysis Configuration (CPU環境用：テストサンプル数を削減)
STABILITY_CONFIG = {
    'top_k_features': [3, 5, 10],
    'n_test_samples': 50,  # 100 → 50に削減（計算時間短縮）
    'correlation_method': 'spearman'
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
