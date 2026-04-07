@echo off
chcp 65001 >nul
echo ============================================
echo    EduForge AI - Fast Deploy
echo ============================================
echo.

REM Check if git is available
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git not found! Please install Git first.
    pause
    exit /b 1
)

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [1/4] Checking Python packages...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install fastapi uvicorn sqlalchemy pydantic-settings asyncpg python-jose passlib bcrypt python-multipart python-dotenv websockets openai aiosqlite -q
)

echo [2/4] Testing app...
cd backend
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from main import app; print('[OK] App loads!')"

echo.
echo [3/4] Starting server...
echo.
echo ============================================
echo    Server starting on: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Press Ctrl+C to stop the server.
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
