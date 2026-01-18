"""
Full analysis with all 3 models
Student: Keisuke Nishioka (Matrikelnummer: 10081049)

This script runs complete analysis for:
- XGBoost (already done, will load)
- Random Forest (new)
- Logistic Regression (new)
"""

import sys
import os
sys.path.append('src')

import pandas as pd
import numpy as np
from tqdm import tqdm

# Import modules
from data_loader import load_adult_income, prepare_data
from models import (
    train_xgboost, train_random_forest, train_logistic_regression,
    get_task_type, save_model, load_model
)
from shap_analysis import (
    compute_tree_shap, compute_kernel_shap, save_shap_values, load_shap_values
)
from stability_metrics import compute_stability_metrics, compare_models_stability
from visualization import plot_model_comparison
import config_cpu as config

def main():
    """Full analysis execution"""
    
    print("=" * 60)
    print("Full Analysis: All 3 Models")
    print("Student: Keisuke Nishioka (Matrikelnummer: 10081049)")
    print("=" * 60)
    
    # Step 1: Data Preprocessing
    print("\n[Step 1] Loading and preprocessing data...")
    X, y = load_adult_income()
    X_train, X_test, y_train, y_test, scaler = prepare_data(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  [OK] Training set: {X_train.shape}")
    print(f"  [OK] Test set: {X_test.shape}")
    
    task = get_task_type(y_train)
    print(f"  [OK] Task type: {task}")
    
    # Step 2: Model Training
    print("\n[Step 2] Training models...")
    test_seeds = config.RANDOM_SEEDS[:5]  # Use 5 seeds for better analysis
    n_samples = 30  # Reduced for CPU efficiency
    
    # XGBoost (load if exists, otherwise train)
    print("  Training XGBoost models...")
    xgboost_models = {}
    for seed in tqdm(test_seeds, desc="XGBoost"):
        model_path = f'results/models/xgboost_seed_{seed}.pkl'
        if os.path.exists(model_path):
            xgboost_models[seed] = load_model(model_path)
        else:
            model = train_xgboost(
                X_train, y_train, task=task, random_state=seed,
                n_estimators=50, max_depth=5, base_score=0.5
            )
            xgboost_models[seed] = model
            save_model(model, model_path)
    
    # Random Forest
    print("  Training Random Forest models...")
    rf_models = {}
    for seed in tqdm(test_seeds, desc="Random Forest"):
        model = train_random_forest(
            X_train, y_train, task=task, random_state=seed,
            n_estimators=50, max_depth=8
        )
        rf_models[seed] = model
        save_model(model, f'results/models/random_forest_seed_{seed}.pkl')
    
    # Logistic Regression
    print("  Training Logistic Regression models...")
    lr_models = {}
    for seed in tqdm(test_seeds, desc="Logistic Regression"):
        model = train_logistic_regression(
            X_train, y_train, random_state=seed
        )
        lr_models[seed] = model
        save_model(model, f'results/models/logistic_regression_seed_{seed}.pkl')
    
    print(f"  [OK] All models trained!")
    
    # Step 3: SHAP Explanation Generation
    print("\n[Step 3] Generating SHAP explanations...")
    
    # XGBoost (load if exists, otherwise compute)
    print("  Computing SHAP for XGBoost...")
    xgboost_shap_dict = {}
    for seed in tqdm(test_seeds, desc="XGBoost SHAP"):
        shap_path = f'results/shap_values/xgboost_seed_{seed}_shap.npz'
        if os.path.exists(shap_path):
            shap_vals = load_shap_values(shap_path)
            # Handle 3D shape
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            xgboost_shap_dict[seed] = shap_vals
        else:
            shap_vals, _ = compute_tree_shap(xgboost_models[seed], X_test, n_samples=n_samples)
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            xgboost_shap_dict[seed] = shap_vals
            save_shap_values(shap_vals, shap_path)
    
    # Random Forest (TreeSHAP)
    print("  Computing SHAP for Random Forest...")
    rf_shap_dict = {}
    for seed in tqdm(test_seeds, desc="Random Forest SHAP"):
        shap_vals, _ = compute_tree_shap(rf_models[seed], X_test, n_samples=n_samples)
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
        rf_shap_dict[seed] = shap_vals
        save_shap_values(shap_vals, f'results/shap_values/random_forest_seed_{seed}_shap.npz')
    
    # Logistic Regression (KernelSHAP - slower)
    print("  Computing SHAP for Logistic Regression (KernelSHAP - this will take time)...")
    lr_shap_dict = {}
    for seed in tqdm(test_seeds, desc="Logistic Regression SHAP"):
        shap_vals, _ = compute_kernel_shap(
            lr_models[seed], X_train, X_test, 
            n_samples=n_samples, nsamples_shap=50  # Reduced for speed
        )
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
        lr_shap_dict[seed] = shap_vals
        save_shap_values(shap_vals, f'results/shap_values/logistic_regression_seed_{seed}_shap.npz')
    
    print("  [OK] All SHAP values computed!")
    
    # Step 4: Stability Analysis
    print("\n[Step 4] Computing stability metrics...")
    
    xgboost_stability = compute_stability_metrics(xgboost_shap_dict)
    rf_stability = compute_stability_metrics(rf_shap_dict)
    lr_stability = compute_stability_metrics(lr_shap_dict)
    
    stability_results = {
        'XGBoost': xgboost_stability,
        'Random Forest': rf_stability,
        'Logistic Regression': lr_stability
    }
    
    comparison_df = compare_models_stability(stability_results)
    comparison_df.to_csv('results/tables/model_stability_comparison.csv', index=False)
    
    print("\n  Stability Results:")
    print(comparison_df.to_string(index=False))
    print("  [OK] Stability analysis completed!")
    
    # Step 5: Model Comparison Visualization
    print("\n[Step 5] Creating model comparison visualization...")
    plot_model_comparison(
        comparison_df,
        save_path='results/figures/model_comparison.png'
    )
    print("  [OK] Model comparison plot created!")
    
    # Summary
    print("\n" + "=" * 60)
    print("Full Analysis Completed Successfully!")
    print("=" * 60)
    print("\nResults:")
    print(f"  Models trained: {len(test_seeds) * 3}")
    print(f"  SHAP explanations: {len(test_seeds) * 3}")
    print(f"  Stability metrics computed for: 3 models")
    print("\nOutput files:")
    print("  - Models: results/models/")
    print("  - SHAP values: results/shap_values/")
    print("  - Tables: results/tables/model_stability_comparison.csv")
    print("  - Figures: results/figures/model_comparison.png")

if __name__ == "__main__":
    main()
