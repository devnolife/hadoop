@echo off
REM Quick Start Script - Windows
REM Author: devnolife

echo ========================================
echo Hadoop Web Interface - Quick Start
echo Created by devnolife
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo [2/5] Setting up virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements-web.txt
echo.

REM Start application
echo [5/5] Starting web application...
echo.
echo ========================================
echo Web interface will open at:
echo http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
