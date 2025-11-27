# PDF Tools - Run Script
# Quick script to run the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Tools - Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Please run setup.ps1 first" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1" -ForegroundColor Cyan
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Run the application
Write-Host "Starting Streamlit application..." -ForegroundColor Green
Write-Host ""
Write-Host "The application will open in your default browser" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run main.py
