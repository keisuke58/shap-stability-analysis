@echo off
echo Compiling LaTeX documents...
echo.

cd /d "%~dp0"

REM Refresh PATH
set "PATH=%PATH%;C:\Users\nishi\AppData\Local\Programs\MiKTeX\miktex\bin\x64"

echo [1/2] Compiling final_report.tex (first pass)...
pdflatex -interaction=nonstopmode final_report.tex

echo.
echo [1/2] Compiling final_report.tex (second pass)...
pdflatex -interaction=nonstopmode final_report.tex

echo.
echo [2/2] Compiling poster.tex (first pass)...
pdflatex -interaction=nonstopmode poster.tex

echo.
echo [2/2] Compiling poster.tex (second pass)...
pdflatex -interaction=nonstopmode poster.tex

echo.
echo Cleaning up auxiliary files...
del *.aux *.log *.out 2>nul

echo.
if exist final_report.pdf (
    echo SUCCESS: final_report.pdf created!
) else (
    echo ERROR: final_report.pdf not found
)

if exist poster.pdf (
    echo SUCCESS: poster.pdf created!
) else (
    echo ERROR: poster.pdf not found
)

echo.
pause
