"""
Main pipeline script for SHAP Stability Analysis
Student: Keisuke Nishioka (Matrikelnummer: 10081049)

This script runs the complete pipeline:
1. Data preprocessing
2. Model training
3. SHAP explanation generation
4. Stability analysis
5. Visualization

Usage:
    python run_full_pipeline.py
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
    get_task_type, save_model
)
from shap_analysis import (
    compute_shap_for_model, compute_shap_multiple_seeds,
    save_shap_values
)
from stability_metrics import compute_stability_metrics, compare_models_stability
from visualization import (
    plot_shap_summary, plot_ranking_correlation,
    plot_shap_variance, plot_consistency_comparison, plot_model_comparison
)
import config


def main():
    """Main pipeline execution"""
    
    print("=" * 60)
    print("SHAP Stability Analysis Pipeline")
    print("Student: Keisuke Nishioka (Matrikelnummer: 10081049)")
    print("=" * 60)
    
    # Step 1: Data Preprocessing
    print("\n[Step 1] Loading and preprocessing data...")
    X, y = load_adult_income()
    X_train, X_test, y_train, y_test, scaler = prepare_data(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  Training set: {X_train.shape}")
    print(f"  Test set: {X_test.shape}")
    
    # Determine task type
    task = get_task_type(y_train)
    print(f"  Task type: {task}")
    
    # Step 2: Model Training
    print("\n[Step 2] Training models...")
    n_seeds = len(config.RANDOM_SEEDS)
    
    # Train XGBoost
    print(f"  Training {n_seeds} XGBoost models...")
    xgboost_models = {}
    for seed in tqdm(config.RANDOM_SEEDS, desc="XGBoost"):
        model = train_xgboost(X_train, y_train, task=task, random_state=seed)
        xgboost_models[seed] = model
        save_model(model, f'results/models/xgboost_seed_{seed}.pkl')
    
    # Train Random Forest
    print(f"  Training {n_seeds} Random Forest models...")
    rf_models = {}
    for seed in tqdm(config.RANDOM_SEEDS, desc="Random Forest"):
        model = train_random_forest(X_train, y_train, task=task, random_state=seed)
        rf_models[seed] = model
        save_model(model, f'results/models/random_forest_seed_{seed}.pkl')
    
    # Train Logistic Regression
    print(f"  Training {n_seeds} Logistic Regression models...")
    lr_models = {}
    for seed in tqdm(config.RANDOM_SEEDS, desc="Logistic Regression"):
        model = train_logistic_regression(X_train, y_train, random_state=seed)
        lr_models[seed] = model
        save_model(model, f'results/models/logistic_regression_seed_{seed}.pkl')
    
    print("  Model training completed!")
    
    # Step 3: SHAP Explanation Generation
    print("\n[Step 3] Generating SHAP explanations...")
    n_samples = config.STABILITY_CONFIG['n_test_samples']
    
    # XGBoost (TreeSHAP)
    print("  Computing TreeSHAP for XGBoost...")
    xgboost_shap_results = compute_shap_multiple_seeds(
        xgboost_models, X_train, X_test,
        model_type='xgboost',
        random_seeds=config.RANDOM_SEEDS,
        n_samples=n_samples,
        save_dir='results/shap_values'
    )
    
    # Random Forest (TreeSHAP)
    print("  Computing TreeSHAP for Random Forest...")
    rf_shap_results = compute_shap_multiple_seeds(
        rf_models, X_train, X_test,
        model_type='random_forest',
        random_seeds=config.RANDOM_SEEDS,
        n_samples=n_samples,
        save_dir='results/shap_values'
    )
    
    # Logistic Regression (KernelSHAP) - Use fewer seeds (slower)
    print("  Computing KernelSHAP for Logistic Regression...")
    lr_seeds = config.RANDOM_SEEDS[:5]  # Use first 5 seeds
    lr_models_subset = {seed: lr_models[seed] for seed in lr_seeds}
    lr_shap_results = compute_shap_multiple_seeds(
        lr_models_subset, X_train, X_test,
        model_type='logistic_regression',
        random_seeds=lr_seeds,
        n_samples=n_samples,
        save_dir='results/shap_values'
    )
    
    print("  SHAP computation completed!")
    
    # Step 4: Stability Analysis
    print("\n[Step 4] Computing stability metrics...")
    
    # Extract SHAP values
    xgboost_shap_dict = {seed: shap_vals for seed, (shap_vals, _) in xgboost_shap_results.items()}
    rf_shap_dict = {seed: shap_vals for seed, (shap_vals, _) in rf_shap_results.items()}
    lr_shap_dict = {seed: shap_vals for seed, (shap_vals, _) in lr_shap_results.items()}
    
    # Compute stability metrics
    xgboost_stability = compute_stability_metrics(xgboost_shap_dict)
    rf_stability = compute_stability_metrics(rf_shap_dict)
    lr_stability = compute_stability_metrics(lr_shap_dict)
    
    # Compare models
    stability_results = {
        'XGBoost': xgboost_stability,
        'Random Forest': rf_stability,
        'Logistic Regression': lr_stability
    }
    comparison_df = compare_models_stability(stability_results)
    
    # Save results
    comparison_df.to_csv('results/tables/model_stability_comparison.csv', index=False)
    print("  Stability analysis completed!")
    
    # Step 5: Visualization
    print("\n[Step 5] Generating visualizations...")
    
    # Get sample data for visualization
    seed = config.RANDOM_SEEDS[0]
    xgboost_shap_sample = xgboost_shap_dict[seed]
    X_sample = X_test.iloc[:len(xgboost_shap_sample)]
    feature_names = X_test.columns.tolist()
    
    # Create visualizations
    plot_shap_summary(
        xgboost_shap_sample, X_sample, feature_names=feature_names,
        save_path='results/figures/xgboost_shap_summary.png'
    )
    
    plot_ranking_correlation(
        xgboost_stability,
        save_path='results/figures/xgboost_ranking_correlation.png'
    )
    
    plot_shap_variance(
        xgboost_stability, feature_names=feature_names,
        save_path='results/figures/xgboost_shap_variance.png'
    )
    
    plot_consistency_comparison(
        xgboost_stability,
        save_path='results/figures/xgboost_consistency.png'
    )
    
    plot_model_comparison(
        comparison_df,
        save_path='results/figures/model_comparison.png'
    )
    
    print("  Visualizations completed!")
    
    # Summary
    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)
    print("\nResults:")
    print(f"  Models trained: {n_seeds * 3}")
    print(f"  SHAP explanations generated: {len(xgboost_shap_results) + len(rf_shap_results) + len(lr_shap_results)}")
    print(f"  Stability metrics computed for: 3 models")
    print(f"  Visualizations created: 5 figures")
    print("\nOutput files:")
    print("  - Models: results/models/")
    print("  - SHAP values: results/shap_values/")
    print("  - Tables: results/tables/")
    print("  - Figures: results/figures/")


if __name__ == "__main__":
    main()
