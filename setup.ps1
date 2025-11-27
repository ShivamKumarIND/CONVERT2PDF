# PDF Tools - Setup Script
# Run this script to set up the application automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Tools - Automated Setup" -ForegroundColor Cyan
Write-Host "  Shivam IT Solutions" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
Write-Host ""
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
    $createVenv = Read-Host "Do you want to recreate it? (y/N)"
    if ($createVenv -eq "y" -or $createVenv -eq "Y") {
        Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
        Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
        python -m venv venv
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    }
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}
catch {
    Write-Host "⚠ Could not activate virtual environment automatically" -ForegroundColor Yellow
    Write-Host "  You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Some dependencies failed to install" -ForegroundColor Red
    Write-Host "  Please check the error messages above" -ForegroundColor Yellow
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.template" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    Write-Host "  You can customize settings in .env file" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Check for Logo.jpg
Write-Host ""
Write-Host "Checking for logo..." -ForegroundColor Yellow
if (Test-Path "Logo.jpg") {
    Write-Host "✓ Logo.jpg found" -ForegroundColor Green
} else {
    Write-Host "⚠ Logo.jpg not found" -ForegroundColor Yellow
    Write-Host "  Place your logo as 'Logo.jpg' in the project root" -ForegroundColor Yellow
}

# Create directories if they don't exist
Write-Host ""
Write-Host "Checking directories..." -ForegroundColor Yellow
if (-not (Test-Path "temp")) {
    New-Item -ItemType Directory -Path "temp" | Out-Null
    Write-Host "✓ Created temp directory" -ForegroundColor Green
} else {
    Write-Host "✓ temp directory exists" -ForegroundColor Green
}

if (-not (Test-Path "output")) {
    New-Item -ItemType Directory -Path "output" | Out-Null
    Write-Host "✓ Created output directory" -ForegroundColor Green
} else {
    Write-Host "✓ output directory exists" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure Logo.jpg is in the project root" -ForegroundColor White
Write-Host "2. Customize .env file if needed" -ForegroundColor White
Write-Host "3. Run the application with:" -ForegroundColor White
Write-Host "   streamlit run main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "For help, see:" -ForegroundColor Yellow
Write-Host "- README.md (detailed documentation)" -ForegroundColor White
Write-Host "- QUICKSTART.md (quick reference)" -ForegroundColor White
Write-Host ""

# Ask if user wants to run the app now
$runNow = Read-Host "Do you want to run the application now? (Y/n)"
if ($runNow -ne "n" -and $runNow -ne "N") {
    Write-Host ""
    Write-Host "Starting application..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    streamlit run main.py
}
