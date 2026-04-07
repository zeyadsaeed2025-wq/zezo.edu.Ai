@echo off
chcp 65001 >nul
title EduForge AI Server
echo.
echo  ================================================
echo     EduForge AI - Starting Server
echo  ================================================
echo.

cd /d "%~dp0backend"

echo [*] Installing dependencies if needed...
pip install -r requirements.txt -q 2>nul

echo.
echo [*] Starting server...
echo.
echo    Website:    http://localhost:8000
echo    API Docs:   http://localhost:8000/docs
echo.
echo    Press Ctrl+C to stop
echo.
echo ================================================
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
