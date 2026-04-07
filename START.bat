@echo off
chcp 65001 >nul
echo ============================================
echo    EduForge AI - Setup & Run
echo ============================================
echo.

REM Set database URL
set DATABASE_URL=postgresql://postgres:2%40xAm7eCy%40Tsr9@db.jnzqdznnhcjeovmvznuq.supabase.co:5432/postgres

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
echo.

echo [2/4] Setting up database...
python setup-database.py
echo.

echo [3/4] Creating .env file...
echo DATABASE_URL=%DATABASE_URL% > backend\.env
echo OPENAI_API_KEY=sk-your-key-here >> backend\.env
echo SECRET_KEY=eduforge-secret-2024 >> backend\.env
echo.

echo [4/4] Starting server...
echo.
echo ============================================
echo    Open browser: http://localhost:8000
echo ============================================
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
