"""Create all visualizations for all models"""
import sys
sys.path.append('src')

from visualization import (
    plot_shap_summary, plot_ranking_correlation,
    plot_shap_variance, plot_consistency_comparison
)
from shap_analysis import load_shap_values
from stability_metrics import compute_stability_metrics
import pandas as pd
import os

print("Creating visualizations for all models...")

# Load data
try:
    X_test = pd.read_csv('data/processed/X_test.csv')
except FileNotFoundError:
    from data_loader import load_adult_income, prepare_data
    X, y = load_adult_income()
    _, X_test, _, _, _ = prepare_data(X, y, test_size=0.2, random_state=42)

feature_names = X_test.columns.tolist()
seeds = [42, 123, 456, 789, 1011]

# Process each model
models = ['xgboost', 'random_forest', 'logistic_regression']

for model_name in models:
    print(f"\n=== Processing {model_name} ===")
    
    # Load SHAP values
    shap_dict = {}
    for seed in seeds:
        filepath = f'results/shap_values/{model_name}_seed_{seed}_shap.npz'
        if os.path.exists(filepath):
            shap_vals = load_shap_values(filepath)
            # Handle 3D shape
            if len(shap_vals.shape) == 3:
                shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]
            shap_dict[seed] = shap_vals
    
    if len(shap_dict) == 0:
        print(f"  [SKIP] No SHAP files found for {model_name}")
        continue
    
    print(f"  Loaded {len(shap_dict)} SHAP files")
    
    # Compute stability metrics
    metrics = compute_stability_metrics(shap_dict)
    
    # Create visualizations
    print(f"  Creating visualizations...")
    
    # SHAP summary plot
    shap_vals = shap_dict[seeds[0]]
    X_sample = X_test.iloc[:shap_vals.shape[0]]
    plot_shap_summary(
        shap_vals, 
        X_sample, 
        feature_names=feature_names, 
        save_path=f'results/figures/{model_name}_shap_summary.png'
    )
    
    # Ranking correlation
    plot_ranking_correlation(
        metrics, 
        save_path=f'results/figures/{model_name}_ranking_correlation.png'
    )
    
    # SHAP variance
    plot_shap_variance(
        metrics, 
        feature_names=feature_names, 
        save_path=f'results/figures/{model_name}_shap_variance.png'
    )
    
    # Consistency comparison
    plot_consistency_comparison(
        metrics, 
        save_path=f'results/figures/{model_name}_consistency.png'
    )
    
    print(f"  [OK] {model_name} visualizations created!")

print("\n" + "=" * 60)
print("[OK] All visualizations created!")
print("=" * 60)
print("\nGenerated figures:")
for model_name in models:
    print(f"  {model_name}:")
    print(f"    - {model_name}_shap_summary.png")
    print(f"    - {model_name}_ranking_correlation.png")
    print(f"    - {model_name}_shap_variance.png")
    print(f"    - {model_name}_consistency.png")
print(f"\n  Model comparison:")
print(f"    - model_comparison.png")
