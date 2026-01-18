"""Check execution results"""
import sys
sys.path.append('src')

from shap_analysis import load_shap_values
from stability_metrics import compute_stability_metrics
import os

# Load SHAP values
shap_dict = {}
seeds = [42, 123, 456]
for seed in seeds:
    filepath = f'results/shap_values/xgboost_seed_{seed}_shap.npz'
    if os.path.exists(filepath):
        shap_dict[seed] = load_shap_values(filepath)

print(f'Loaded {len(shap_dict)} SHAP files')

# Compute stability metrics
if len(shap_dict) > 0:
    metrics = compute_stability_metrics(shap_dict)
    print('\n=== Stability Results ===')
    print(f'Ranking Correlation: {metrics["ranking_correlation"]["mean"]:.4f}')
    print(f'SHAP Variance: {metrics["variance"]["overall"]:.4f}')
    print(f'Top-5 Consistency: {metrics["consistency"]["top_5"]["overall"]:.4f}')
    print('\n[OK] All calculations completed successfully!')
else:
    print('[ERROR] No SHAP files found')
