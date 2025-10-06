@echo off
echo ========================================
echo   CodeSonor - GitHub Analyzer Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing/updating dependencies...
pip install -q -r requirements.txt
echo.

REM Start the Flask application
echo Starting CodeSonor server...
echo Navigate to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
