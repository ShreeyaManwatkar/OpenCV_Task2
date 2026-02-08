@echo off
echo ============================================================
echo Member 2 - Gaze Tracking System Setup
echo ============================================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and added to PATH
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo ============================================================
echo Setup Complete! ✓
echo ============================================================
echo.
echo To run the program:
echo   1. Run: run.bat
echo   OR
echo   2. Activate venv: venv\Scripts\activate
echo      Then run: cd code ^&^& python member2_gaze_tracking.py
echo.
echo Press any key to exit...
pause > nul
