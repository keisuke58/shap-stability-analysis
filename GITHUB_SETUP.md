# GitHub Repository Setup Guide

## Repository Information

**Repository Name**: `shap-stability-analysis`  
**Description**: Stability and Faithfulness Analysis of SHAP Explanations for Tabular Machine Learning Models

## Steps to Create GitHub Repository

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `shap-stability-analysis`
3. Description: `Stability and Faithfulness Analysis of SHAP Explanations for Tabular Machine Learning Models`
4. Visibility: Public (or Private if preferred)
5. Do NOT initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 2. Initialize Git and Push Code

```bash
cd c:\Users\nishi\Life\iML_Project_Stability_Analysis

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SHAP stability analysis project"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/shap-stability-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Update Links in Documents

After creating the repository, update the GitHub links in:
- `poster.tex` (line with GitHub URL)
- `final_report.tex` (Reproducibility section)

GitHub username is already set to `keisuke58` in the documents.

### 4. Files to Include

The repository should include:
- ✅ All Python source code (`src/`)
- ✅ Jupyter notebooks (`notebooks/`)
- ✅ Configuration files (`config.py`, `requirements.txt`)
- ✅ LaTeX source files (`final_report.tex`, `poster.tex`)
- ✅ README.md
- ✅ Results tables (`results/tables/`)
- ❌ Large files (models, SHAP values) - add to `.gitignore`
- ❌ Generated PDFs (optional - can be added to releases)

### 5. Recommended .gitignore Additions

Add to `.gitignore`:
```
# Large result files
results/models/*.pkl
results/shap_values/*.npz
*.pdf

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Jupyter
.ipynb_checkpoints/

# LaTeX
*.aux
*.log
*.out
*.toc
*.synctex.gz
```

### 6. Create Repository README

The README.md file is already created with project information.

## After Setup

1. Update GitHub links in `poster.tex` and `final_report.tex`
2. Recompile PDFs
3. Optionally create a GitHub Release with the PDFs
