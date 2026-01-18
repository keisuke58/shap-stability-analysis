@echo off
echo ========================================
echo GitHub Repository Push Script
echo ========================================
echo.

cd /d "%~dp0"

echo [Step 1] Checking git status...
git status --short
echo.

echo [Step 2] Adding all files...
git add .
echo.

echo [Step 3] Creating commit...
git commit -m "Initial commit: SHAP stability analysis project - Final report and poster"
echo.

echo [Step 4] Adding remote repository...
git remote add origin https://github.com/keisuke58/shap-stability-analysis.git
if errorlevel 1 (
    echo Remote already exists, removing and re-adding...
    git remote remove origin
    git remote add origin https://github.com/keisuke58/shap-stability-analysis.git
)
echo.

echo [Step 5] Setting main branch...
git branch -M main
echo.

echo [Step 6] Pushing to GitHub...
echo.
echo NOTE: If you see "Repository not found" error, please:
echo 1. Go to https://github.com/new
echo 2. Create repository named: shap-stability-analysis
echo 3. Do NOT initialize with README, .gitignore, or license
echo 4. Then run this script again
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Repository not created on GitHub yet
    echo    - Go to: https://github.com/new
    echo    - Create: shap-stability-analysis
    echo.
    echo 2. Authentication required
    echo    - Use Personal Access Token
    echo    - Or: gh auth login (if GitHub CLI installed)
    echo.
) else (
    echo.
    echo ========================================
    echo SUCCESS! Repository pushed to GitHub
    echo ========================================
    echo.
    echo Repository URL:
    echo https://github.com/keisuke58/shap-stability-analysis
    echo.
)

pause
