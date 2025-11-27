# Installation Verification Script
# Run this to verify your installation is complete

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Tools - Installation Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([8-9]|\d{2,})") {
        Write-Host "✓ Python installed: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Python version too old: $pythonVersion" -ForegroundColor Red
        Write-Host "  Need Python 3.8 or higher" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "✗ Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check Virtual Environment
Write-Host ""
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found" -ForegroundColor Red
    Write-Host "  Run: .\setup.ps1" -ForegroundColor Yellow
    $allGood = $false
}

# Check Required Files
Write-Host ""
Write-Host "Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "main.py",
    "config.py",
    "requirements.txt",
    ".env.template",
    "backend\__init__.py",
    "backend\organize.py",
    "backend\optimize.py",
    "backend\convert_to_pdf.py",
    "backend\convert_from_pdf.py",
    "backend\edit.py",
    "backend\security.py",
    "frontend\__init__.py",
    "frontend\ui_components.py",
    "frontend\tool_handlers.py",
    "utils\__init__.py",
    "utils\file_utils.py"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file" -ForegroundColor Red
        $missingFiles += $file
        $allGood = $false
    }
}

# Check Directories
Write-Host ""
Write-Host "Checking directories..." -ForegroundColor Yellow

$requiredDirs = @("backend", "frontend", "utils", "temp", "output")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir/" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dir/" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Logo
Write-Host ""
Write-Host "Checking logo..." -ForegroundColor Yellow
if (Test-Path "Logo.jpg") {
    Write-Host "✓ Logo.jpg found" -ForegroundColor Green
} else {
    Write-Host "⚠ Logo.jpg not found (optional)" -ForegroundColor Yellow
    Write-Host "  Add Logo.jpg for branding" -ForegroundColor Gray
}

# Check Dependencies (if venv exists)
if (Test-Path "venv") {
    Write-Host ""
    Write-Host "Checking dependencies..." -ForegroundColor Yellow
    
    & ".\venv\Scripts\Activate.ps1"
    
    $requiredPackages = @(
        "streamlit",
        "PyPDF2",
        "pikepdf",
        "reportlab",
        "Pillow",
        "python-docx",
        "openpyxl",
        "python-pptx"
    )
    
    $missingPackages = @()
    foreach ($package in $requiredPackages) {
        $installed = pip show $package 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $package" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $package" -ForegroundColor Red
            $missingPackages += $package
            $allGood = $false
        }
    }
    
    if ($missingPackages.Count -gt 0) {
        Write-Host ""
        Write-Host "Missing packages. Install with:" -ForegroundColor Yellow
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Cyan
    }
}

# Final Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "  ✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your installation is complete and ready to use!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1" -ForegroundColor Cyan
    Write-Host "  OR" -ForegroundColor Gray
    Write-Host "  streamlit run main.py" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "  ⚠️  SOME ISSUES FOUND" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please fix the issues above and run setup:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1" -ForegroundColor Cyan
    Write-Host ""
    
    if ($missingFiles.Count -gt 0) {
        Write-Host "Missing files:" -ForegroundColor Red
        foreach ($file in $missingFiles) {
            Write-Host "  - $file" -ForegroundColor Red
        }
        Write-Host ""
    }
}

Write-Host ""
