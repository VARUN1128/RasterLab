@echo off
echo ========================================
echo    Starting RasterLab Application
echo ========================================
echo.

echo Starting backend server...
start "RasterLab Backend" cmd /k "python backend/main.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting frontend server...
start "RasterLab Frontend" cmd /k "npm start"

echo.
echo ========================================
echo    Application Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
