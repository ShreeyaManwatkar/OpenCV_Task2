@echo off
echo ============================================================
echo Member 2 - Gaze Tracking System
echo ============================================================
echo.

if not exist venv\ (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting gaze tracking system...
echo.
cd code
python member2_gaze_tracking.py

cd ..
echo.
echo Program ended.
pause
