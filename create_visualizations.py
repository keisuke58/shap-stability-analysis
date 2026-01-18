"""Create visualizations for SHAP stability analysis"""
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

print("Creating visualizations...")

# Load data (reload if not saved)
try:
    X_test = pd.read_csv('data/processed/X_test.csv')
except FileNotFoundError:
    from data_loader import load_adult_income, prepare_data
    X, y = load_adult_income()
    _, X_test, _, _, _ = prepare_data(X, y, test_size=0.2, random_state=42)

feature_names = X_test.columns.tolist()

# Load SHAP values
shap_dict = {}
seeds = [42, 123, 456]
for seed in seeds:
    filepath = f'results/shap_values/xgboost_seed_{seed}_shap.npz'
    if os.path.exists(filepath):
        shap_dict[seed] = load_shap_values(filepath)

print(f"Loaded {len(shap_dict)} SHAP files")

# Compute stability metrics
metrics = compute_stability_metrics(shap_dict)

# Create visualizations
print("\nCreating SHAP summary plot...")
# Check SHAP shape and handle if needed
shap_vals = shap_dict[42]
if len(shap_vals.shape) == 3:
    # If 3D (n_samples, n_features, n_classes), take positive class (index 1)
    shap_vals = shap_vals[:, :, 1] if shap_vals.shape[2] > 1 else shap_vals[:, :, 0]

X_sample = X_test.iloc[:shap_vals.shape[0]]
plot_shap_summary(
    shap_vals, 
    X_sample, 
    feature_names=feature_names, 
    save_path='results/figures/xgboost_shap_summary.png'
)

print("Creating ranking correlation plot...")
plot_ranking_correlation(
    metrics, 
    save_path='results/figures/xgboost_ranking_correlation.png'
)

print("Creating SHAP variance plot...")
plot_shap_variance(
    metrics, 
    feature_names=feature_names, 
    save_path='results/figures/xgboost_shap_variance.png'
)

print("Creating consistency comparison plot...")
plot_consistency_comparison(
    metrics, 
    save_path='results/figures/xgboost_consistency.png'
)

print("\n[OK] All visualizations created!")
print("Files saved to results/figures/")
