@echo off
echo Compiling LaTeX documents...
echo.

cd /d "%~dp0"

echo [1/2] Compiling final report...
pdflatex -interaction=nonstopmode final_report.tex
pdflatex -interaction=nonstopmode final_report.tex
echo.

echo [2/2] Compiling poster...
pdflatex -interaction=nonstopmode poster.tex
pdflatex -interaction=nonstopmode poster.tex
echo.

echo Cleaning up auxiliary files...
del *.aux *.log *.out 2>nul

echo.
echo Done! Check final_report.pdf and poster.pdf
pause
