@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo    MSA Scholarship Program
echo ========================================
echo.
echo [1/2] Starting Flask server...
start "Flask Server" .venv\Scripts\python.exe app.py
timeout /t 4 /nobreak > nul

echo [2/2] Starting ngrok tunnel...
echo.
echo *** Copy the https://....ngrok-free.app link below and share it ***
echo.
.\ngrok.exe http 5000
