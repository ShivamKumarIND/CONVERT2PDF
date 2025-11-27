@echo off
REM PDF Tools - Setup Script (Batch version)
REM Run this if PowerShell scripts are blocked

echo ========================================
echo   PDF Tools - Automated Setup
echo   Shivam IT Solutions
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

REM Check if virtual environment exists
echo Checking virtual environment...
if exist venv (
    echo [OK] Virtual environment found
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
    echo Please check the error messages above
) else (
    echo [OK] All dependencies installed successfully
)
echo.

REM Create .env file if it doesn't exist
echo Checking configuration...
if not exist .env (
    copy .env.template .env >nul
    echo [OK] Created .env file from template
    echo You can customize settings in .env file
) else (
    echo [OK] .env file already exists
)
echo.

REM Check for Logo.jpg
echo Checking for logo...
if exist Logo.jpg (
    echo [OK] Logo.jpg found
) else (
    echo [WARNING] Logo.jpg not found
    echo Place your logo as 'Logo.jpg' in the project root
)
echo.

REM Create directories if they don't exist
echo Checking directories...
if not exist temp mkdir temp
echo [OK] temp directory ready
if not exist output mkdir output
echo [OK] output directory ready
echo.

REM Summary
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Ensure Logo.jpg is in the project root
echo 2. Customize .env file if needed
echo 3. Run the application with:
echo    run.bat  OR  streamlit run main.py
echo.
echo For help, see:
echo - README.md (detailed documentation)
echo - QUICKSTART.md (quick reference)
echo.

REM Ask if user wants to run the app now
set /p RUNNOW="Do you want to run the application now? (Y/n): "
if /i "%RUNNOW%"=="n" goto end

echo.
echo Starting application...
echo Press Ctrl+C to stop
echo.
streamlit run main.py

:end
pause
