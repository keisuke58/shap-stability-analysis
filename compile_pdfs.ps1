# Compile LaTeX documents to PDF
Write-Host "Compiling LaTeX documents..."

# Refresh PATH to include MiKTeX
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Try to find pdflatex
$pdflatexPaths = @(
    "C:\Users\$env:USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
    "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
    "C:\Program Files (x86)\MiKTeX\miktex\bin\x64\pdflatex.exe"
)

$pdflatex = $null
foreach ($path in $pdflatexPaths) {
    if (Test-Path $path) {
        $pdflatex = $path
        Write-Host "Found pdflatex at: $path"
        break
    }
}

if (-not $pdflatex) {
    # Try to find in PATH
    try {
        $pdflatexCmd = Get-Command pdflatex -ErrorAction Stop
        $pdflatex = $pdflatexCmd.Source
        Write-Host "Found pdflatex in PATH: $pdflatex"
    } catch {
        Write-Host "ERROR: pdflatex not found!"
        Write-Host "Please ensure MiKTeX is installed and restart your terminal."
        Write-Host "Or run: wait_and_compile.ps1"
        exit 1
    }
}

# Compile final_report.tex
Write-Host "`n[1/2] Compiling final_report.tex (first pass)..."
& $pdflatex -interaction=nonstopmode final_report.tex | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: First compilation had errors. Continuing..."
}

Write-Host "[1/2] Compiling final_report.tex (second pass)..."
& $pdflatex -interaction=nonstopmode final_report.tex | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ final_report.pdf created successfully!"
} else {
    Write-Host "✗ Error compiling final_report.tex"
}

# Compile poster.tex
Write-Host "`n[2/2] Compiling poster.tex (first pass)..."
& $pdflatex -interaction=nonstopmode poster.tex | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: First compilation had errors. Continuing..."
}

Write-Host "[2/2] Compiling poster.tex (second pass)..."
& $pdflatex -interaction=nonstopmode poster.tex | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ poster.pdf created successfully!"
} else {
    Write-Host "✗ Error compiling poster.tex"
}

# Clean up auxiliary files
Write-Host "`nCleaning up auxiliary files..."
Remove-Item *.aux, *.log, *.out -ErrorAction SilentlyContinue

Write-Host "`nDone! Check for final_report.pdf and poster.pdf in the current directory."
