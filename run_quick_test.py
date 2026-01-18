"""
Quick test script for CPU environment
Student: Keisuke Nishioka (Matrikelnummer: 10081049)

This script runs a minimal test to verify everything works:
- Data loading
- Model training (XGBoost only, 3 seeds)
- SHAP computation (TreeSHAP)
- Basic stability analysis
"""

import sys
import os
sys.path.append('src')

import pandas as pd
import numpy as np
from tqdm import tqdm

# Import modules
from data_loader import load_adult_income, prepare_data
from models import train_xgboost, get_task_type, save_model, load_model
from shap_analysis import compute_tree_shap, save_shap_values
from stability_metrics import compute_stability_metrics
import config_cpu as config  # Use CPU optimized config

def main():
    """Quick test execution"""
    
    print("=" * 60)
    print("Quick Test: SHAP Stability Analysis")
    print("Student: Keisuke Nishioka (Matrikelnummer: 10081049)")
    print("=" * 60)
    
    # Step 1: Data Preprocessing
    print("\n[Step 1] Loading and preprocessing data...")
    try:
        X, y = load_adult_income()
        X_train, X_test, y_train, y_test, scaler = prepare_data(
            X, y, test_size=0.2, random_state=42
        )
        print(f"  [OK] Training set: {X_train.shape}")
        print(f"  [OK] Test set: {X_test.shape}")
        
        # Determine task type
        task = get_task_type(y_train)
        print(f"  [OK] Task type: {task}")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return
    
    # Step 2: Model Training (XGBoost only, 3 seeds for quick test)
    print("\n[Step 2] Training XGBoost models...")
    test_seeds = config.RANDOM_SEEDS[:3]  # Use first 3 seeds for quick test
    xgboost_models = {}
    
    try:
        for seed in tqdm(test_seeds, desc="Training"):
            model = train_xgboost(
                X_train, y_train, 
                task=task, 
                random_state=seed,
                n_estimators=50,  # Reduced for quick test
                max_depth=5,
                base_score=0.5  # Explicit base_score for SHAP compatibility
            )
            xgboost_models[seed] = model
            save_model(model, f'results/models/xgboost_seed_{seed}.pkl')
        print(f"  [OK] Trained {len(xgboost_models)} XGBoost models")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return
    
    # Step 3: SHAP Explanation Generation (TreeSHAP)
    print("\n[Step 3] Generating SHAP explanations...")
    n_samples = 30  # Reduced for quick test
    xgboost_shap_results = {}
    
    try:
        for seed in tqdm(test_seeds, desc="Computing SHAP"):
            model = xgboost_models[seed]
            shap_values, X_sample = compute_tree_shap(model, X_test, n_samples=n_samples)
            xgboost_shap_results[seed] = shap_values
            
            # Save SHAP values
            save_shap_values(shap_values, f'results/shap_values/xgboost_seed_{seed}_shap.npz')
        print(f"  [OK] Computed SHAP for {len(xgboost_shap_results)} models")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Stability Analysis
    print("\n[Step 4] Computing stability metrics...")
    try:
        stability_metrics = compute_stability_metrics(xgboost_shap_results)
        
        print("\n  Stability Results:")
        print(f"    Ranking Correlation: {stability_metrics['ranking_correlation']['mean']:.4f}")
        print(f"    SHAP Variance: {stability_metrics['variance']['overall']:.4f}")
        print(f"    Top-5 Consistency: {stability_metrics['consistency']['top_5']['overall']:.4f}")
        print("  [OK] Stability analysis completed!")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("Quick Test Completed Successfully!")
    print("=" * 60)
    print("\nResults:")
    print(f"  Models trained: {len(xgboost_models)}")
    print(f"  SHAP explanations: {len(xgboost_shap_results)}")
    print(f"  Test samples: {n_samples}")
    print("\nOutput files:")
    print("  - Models: results/models/")
    print("  - SHAP values: results/shap_values/")
    print("\nNext steps:")
    print("  1. Run full pipeline with all models")
    print("  2. Generate visualizations")
    print("  3. Run full stability analysis")

if __name__ == "__main__":
    main()
