"""
Subsampling Analysis with Extended Runs
Student: Keisuke Nishioka (Matrikelnummer: 10081049)

This script runs extended analysis with:
- Data subsampling (50%, 75%, 100%)
- More random seeds (10 seeds)
- All 3 models
- Extended analysis for better accuracy
"""

import sys
import os
sys.path.append('src')

import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# Import modules
from data_loader import load_adult_income, prepare_data, subsample_data
from models import (
    train_xgboost, train_random_forest, train_logistic_regression,
    get_task_type, save_model, load_model
)
from shap_analysis import (
    compute_tree_shap, compute_kernel_shap, save_shap_values, load_shap_values
)
from stability_metrics import compute_stability_metrics, compare_models_stability
from visualization import plot_model_comparison
import config

def main():
    """Extended subsampling analysis"""
    
    print("=" * 60)
    print("Extended Subsampling Analysis")
    print("Student: Keisuke Nishioka (Matrikelnummer: 10081049)")
    print("=" * 60)
    
    # Step 1: Data Preprocessing
    print("\n[Step 1] Loading and preprocessing data...")
    X, y = load_adult_income()
    X_train_full, X_test, y_train_full, y_test, scaler = prepare_data(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  [OK] Full training set: {X_train_full.shape}")
    print(f"  [OK] Test set: {X_test.shape}")
    
    task = get_task_type(y_train_full)
    print(f"  [OK] Task type: {task}")
    print(f"  [OK] Dataset: Adult Income")
    
    # Step 2: Extended Configuration
    print("\n[Step 2] Extended configuration...")
    # Use all 10 seeds for better accuracy
    all_seeds = config.RANDOM_SEEDS  # 10 seeds
    subsample_rates = config.SUBSAMPLE_RATES  # [0.5, 0.75, 1.0]
    n_samples = 50  # Increased from 30 to 50 for better analysis
    
    print(f"  Random seeds: {len(all_seeds)} seeds")
    print(f"  Subsampling rates: {subsample_rates}")
    print(f"  Test samples: {n_samples}")
    
    # Step 3: Subsampling Analysis
    print("\n[Step 3] Running subsampling analysis...")
    
    all_results = {}
    
    for subsample_rate in subsample_rates:
        print(f"\n  === Subsampling Rate: {subsample_rate*100:.0f}% ===")
        
        # Subsample training data
        X_train_sub, y_train_sub = subsample_data(
            X_train_full, y_train_full, 
            rate=subsample_rate, 
            random_state=42
        )
        print(f"  Training set size: {X_train_sub.shape[0]} samples")
        
        # Train models for each subsample rate
        print(f"  Training models...")
        
        # XGBoost
        xgboost_models = {}
        for seed in tqdm(all_seeds, desc=f"XGBoost ({subsample_rate*100:.0f}%)"):
            model = train_xgboost(
                X_train_sub, y_train_sub, task=task, random_state=seed,
                n_estimators=100,  # Increased for better accuracy
                max_depth=6,  # Increased
                base_score=0.5
            )
            xgboost_models[seed] = model
        
        # Random Forest
        rf_models = {}
        for seed in tqdm(all_seeds, desc=f"Random Forest ({subsample_rate*100:.0f}%)"):
            model = train_random_forest(
                X_train_sub, y_train_sub, task=task, random_state=seed,
                n_estimators=100,  # Increased for better accuracy
                max_depth=10  # Increased
            )
            rf_models[seed] = model
        
        # Logistic Regression
        lr_models = {}
        for seed in tqdm(all_seeds, desc=f"Logistic Regression ({subsample_rate*100:.0f}%)"):
            model = train_logistic_regression(
                X_train_sub, y_train_sub, random_state=seed
            )
            lr_models[seed] = model
        
        print(f"  [OK] All models trained for {subsample_rate*100:.0f}% subsample")
        
        # Step 4: SHAP Explanation Generation
        print(f"  Computing SHAP explanations...")
        
        # XGBoost (TreeSHAP)
        xgboost_shap_dict = {}
        for seed in tqdm(all_seeds, desc=f"XGBoost SHAP ({subsample_rate*100:.0f}%)"):
            shap_vals, _ = compute_tree_shap(xgboost_models[seed], X_test, n_samples=n_samples)
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            xgboost_shap_dict[seed] = shap_vals
        
        # Random Forest (TreeSHAP)
        rf_shap_dict = {}
        for seed in tqdm(all_seeds, desc=f"Random Forest SHAP ({subsample_rate*100:.0f}%)"):
            shap_vals, _ = compute_tree_shap(rf_models[seed], X_test, n_samples=n_samples)
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            rf_shap_dict[seed] = shap_vals
        
        # Logistic Regression (KernelSHAP - slower)
        lr_shap_dict = {}
        for seed in tqdm(all_seeds, desc=f"Logistic Regression SHAP ({subsample_rate*100:.0f}%)"):
            shap_vals, _ = compute_kernel_shap(
                lr_models[seed], X_train_sub, X_test,
                n_samples=n_samples, nsamples_shap=100  # Increased for better accuracy
            )
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            lr_shap_dict[seed] = shap_vals
        
        print(f"  [OK] All SHAP values computed for {subsample_rate*100:.0f}% subsample")
        
        # Step 5: Stability Analysis
        print(f"  Computing stability metrics...")
        
        xgboost_stability = compute_stability_metrics(xgboost_shap_dict)
        rf_stability = compute_stability_metrics(rf_shap_dict)
        lr_stability = compute_stability_metrics(lr_shap_dict)
        
        stability_results = {
            'XGBoost': xgboost_stability,
            'Random Forest': rf_stability,
            'Logistic Regression': lr_stability
        }
        
        # Store results
        all_results[f'subsample_{subsample_rate}'] = {
            'rate': subsample_rate,
            'training_size': X_train_sub.shape[0],
            'stability_results': stability_results
        }
        
        print(f"  [OK] Stability analysis completed for {subsample_rate*100:.0f}% subsample")
    
    # Step 6: Compare across subsample rates
    print("\n[Step 6] Comparing across subsample rates...")
    
    comparison_data = []
    for rate_key, result in all_results.items():
        rate = result['rate']
        training_size = result['training_size']
        stability = result['stability_results']
        
        for model_name, metrics in stability.items():
            comparison_data.append({
                'Subsample Rate': f'{rate*100:.0f}%',
                'Training Size': training_size,
                'Model': model_name,
                'Ranking Correlation': metrics['ranking_correlation']['mean'],
                'SHAP Variance': metrics['variance']['overall'],
                'Top-5 Consistency': metrics['consistency']['top_5']['overall']
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv('results/tables/subsampling_comparison.csv', index=False)
    
    print("\n  Subsampling Comparison Results:")
    print(comparison_df.to_string(index=False))
    
    # Step 7: Visualize subsampling effects
    print("\n[Step 7] Creating subsampling visualization...")
    create_subsampling_visualization(comparison_df)
    
    # Summary
    print("\n" + "=" * 60)
    print("Extended Subsampling Analysis Completed!")
    print("=" * 60)
    print("\nResults:")
    print(f"  Subsampling rates analyzed: {len(subsample_rates)}")
    print(f"  Random seeds per rate: {len(all_seeds)}")
    print(f"  Total models trained: {len(subsample_rates) * len(all_seeds) * 3}")
    print(f"  Total SHAP computations: {len(subsample_rates) * len(all_seeds) * 3}")
    print("\nOutput files:")
    print("  - Tables: results/tables/subsampling_comparison.csv")
    print("  - Figures: results/figures/subsampling_analysis.png")

def create_subsampling_visualization(comparison_df):
    """Create visualization for subsampling analysis"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Pivot data for easier plotting
    pivot_rc = comparison_df.pivot(index='Model', columns='Subsample Rate', values='Ranking Correlation')
    pivot_var = comparison_df.pivot(index='Model', columns='Subsample Rate', values='SHAP Variance')
    pivot_cons = comparison_df.pivot(index='Model', columns='Subsample Rate', values='Top-5 Consistency')
    
    # Ranking Correlation
    pivot_rc.plot(kind='bar', ax=axes[0, 0], width=0.8)
    axes[0, 0].set_ylabel('Ranking Correlation')
    axes[0, 0].set_title('Ranking Correlation by Subsample Rate')
    axes[0, 0].legend(title='Subsample Rate')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # SHAP Variance
    pivot_var.plot(kind='bar', ax=axes[0, 1], width=0.8, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[0, 1].set_ylabel('SHAP Variance')
    axes[0, 1].set_title('SHAP Variance by Subsample Rate')
    axes[0, 1].legend(title='Subsample Rate')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Top-5 Consistency
    pivot_cons.plot(kind='bar', ax=axes[1, 0], width=0.8, color=['#96CEB4', '#FFEAA7', '#DDA0DD'])
    axes[1, 0].set_ylabel('Top-5 Consistency')
    axes[1, 0].set_title('Top-5 Consistency by Subsample Rate')
    axes[1, 0].legend(title='Subsample Rate')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Training size effect
    for model in comparison_df['Model'].unique():
        model_data = comparison_df[comparison_df['Model'] == model]
        axes[1, 1].plot(
            model_data['Training Size'], 
            model_data['Ranking Correlation'],
            marker='o', label=model, linewidth=2, markersize=8
        )
    axes[1, 1].set_xlabel('Training Size')
    axes[1, 1].set_ylabel('Ranking Correlation')
    axes[1, 1].set_title('Stability vs Training Size')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs('results/figures', exist_ok=True)
    plt.savefig('results/figures/subsampling_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  [OK] Subsampling visualization created!")

if __name__ == "__main__":
    main()
