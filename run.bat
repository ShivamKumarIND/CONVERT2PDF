@echo off
REM PDF Tools - Run Script (Batch version)

echo ========================================
echo   PDF Tools - Starting Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the application
echo Starting Streamlit application...
echo.
echo The application will open in your default browser
echo Press Ctrl+C to stop the server
echo.

streamlit run main.py
