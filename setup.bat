@echo off
echo ========================================
echo    RasterLab Setup Script (Windows)
echo ========================================
echo.

echo [1/4] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Python and Node.js found
echo.

echo [2/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✓ Python dependencies installed
echo.

echo [3/4] Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo ✓ Node.js dependencies installed
echo.

echo [4/4] Running tests...
echo Running backend tests...
python -m pytest tests/test_api.py -v
if errorlevel 1 (
    echo WARNING: Some backend tests failed
)

echo Running frontend tests...
npm test -- --watchAll=false --passWithNoTests
if errorlevel 1 (
    echo WARNING: Some frontend tests failed
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Open Terminal 1: python backend/main.py
echo   2. Open Terminal 2: npm start
echo   3. Open browser: http://localhost:3000
echo.
echo Or run: start_application.bat
echo.
pause
