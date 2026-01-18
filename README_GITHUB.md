# GitHub Repository Setup

## Repository Information

**Repository Name**: `shap-stability-analysis`  
**Description**: Stability and Faithfulness Analysis of SHAP Explanations for Tabular Machine Learning Models  
**GitHub URL**: `https://github.com/keisuke58/shap-stability-analysis`

## Quick Setup Commands

```bash
# Navigate to project directory
cd c:\Users\nishi\Life\iML_Project_Stability_Analysis

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SHAP stability analysis project - Final report and poster"

# Add remote
git remote add origin https://github.com/keisuke58/shap-stability-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Files Included

- ✅ All Python source code (`src/`)
- ✅ Jupyter notebooks (`notebooks/`)
- ✅ Configuration files (`config.py`, `requirements.txt`)
- ✅ LaTeX source files (`final_report.tex`, `poster.tex`)
- ✅ Results tables (`results/tables/`)
- ✅ README.md and documentation
- ❌ Large files excluded (models, SHAP values) - see `.gitignore`

## After Creating Repository

1. GitHub links are already configured with username: `keisuke58`

2. Recompile PDFs:
   ```bash
   .\compile_simple.bat
   ```

3. Optionally create a GitHub Release with the PDFs

## Repository Structure

```
shap-stability-analysis/
├── README.md
├── requirements.txt
├── config.py
├── src/
│   ├── data_loader.py
│   ├── models.py
│   ├── shap_analysis.py
│   ├── stability_metrics.py
│   └── visualization.py
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_model_training.ipynb
│   ├── 03_shap_explanations.ipynb
│   ├── 04_stability_analysis.ipynb
│   └── 05_visualization.ipynb
├── results/
│   ├── figures/
│   └── tables/
├── final_report.tex
├── poster.tex
└── .gitignore
```

## License

Add a LICENSE file if needed (e.g., MIT, Apache 2.0, or academic use only).
