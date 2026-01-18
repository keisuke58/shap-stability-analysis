"""Check progress of subsampling analysis"""
import os
import pandas as pd

print("Checking analysis progress...\n")

# Check models
if os.path.exists('results/models'):
    model_files = [f for f in os.listdir('results/models') if f.endswith('.pkl')]
    print(f"Models: {len(model_files)} files")
else:
    print("Models: 0 files (not started)")

# Check SHAP values
if os.path.exists('results/shap_values'):
    shap_files = [f for f in os.listdir('results/shap_values') if f.endswith('.npz')]
    print(f"SHAP files: {len(shap_files)} files")
    
    # Count by model type
    xgb_count = len([f for f in shap_files if 'xgboost' in f])
    rf_count = len([f for f in shap_files if 'random_forest' in f])
    lr_count = len([f for f in shap_files if 'logistic_regression' in f])
    print(f"  - XGBoost: {xgb_count}")
    print(f"  - Random Forest: {rf_count}")
    print(f"  - Logistic Regression: {lr_count}")
else:
    print("SHAP files: 0 files (not started)")

# Check results
if os.path.exists('results/tables/subsampling_comparison.csv'):
    df = pd.read_csv('results/tables/subsampling_comparison.csv')
    print(f"\nSubsampling results: {len(df)} rows")
    print("\nResults preview:")
    print(df.head(10).to_string(index=False))
else:
    print("\nSubsampling results: Not yet generated")

# Check figures
if os.path.exists('results/figures'):
    figures = [f for f in os.listdir('results/figures') if f.endswith('.png')]
    print(f"\nFigures: {len(figures)} files")
    if 'subsampling_analysis.png' in figures:
        print("  [OK] Subsampling visualization exists")
    else:
        print("  [PENDING] Subsampling visualization not yet created")

print("\n" + "=" * 60)
print("Progress check complete")
