# Wait for MiKTeX installation and compile PDFs
Write-Host "Waiting for MiKTeX installation to complete..."
Write-Host "Please complete the MiKTeX installation wizard if it's open."

# Wait for installation process to finish
$maxWait = 300 # 5 minutes
$waited = 0
while ($waited -lt $maxWait) {
    $process = Get-Process | Where-Object {$_.ProcessName -like "*miktex*"}
    if (-not $process) {
        Write-Host "MiKTeX installer process finished."
        break
    }
    Start-Sleep -Seconds 10
    $waited += 10
    Write-Host "Waiting... ($waited seconds)"
}

# Refresh PATH
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
    $pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
    if ($pdflatex) {
        $pdflatex = $pdflatex.Source
        Write-Host "Found pdflatex in PATH: $pdflatex"
    }
}

if (-not $pdflatex) {
    Write-Host "ERROR: pdflatex not found. Please:"
    Write-Host "1. Complete the MiKTeX installation"
    Write-Host "2. Restart PowerShell/terminal"
    Write-Host "3. Run this script again"
    exit 1
}

# Compile documents
Write-Host "`nCompiling final_report.tex..."
& $pdflatex -interaction=nonstopmode final_report.tex
& $pdflatex -interaction=nonstopmode final_report.tex

Write-Host "`nCompiling poster.tex..."
& $pdflatex -interaction=nonstopmode poster.tex
& $pdflatex -interaction=nonstopmode poster.tex

Write-Host "`nCleaning up auxiliary files..."
Remove-Item *.aux, *.log, *.out -ErrorAction SilentlyContinue

Write-Host "`nDone! Check final_report.pdf and poster.pdf"
