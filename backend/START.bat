@echo off
chcp 65001 >nul
echo ============================================
echo    EduForge AI - التثبيت الكامل
echo ============================================
echo.

echo [1/5] جاري تثبيت Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ فشل تثبيت المكتبات!
    pause
    exit /b 1
)
echo ✅ تم!

echo.
echo [2/5] جاري إنشاء قاعدة البيانات...
python setup-database.py
echo.

echo [3/5] جاري نسخ ملف البيئة...
copy .env.example .env
echo ✅ تم!

echo.
echo [4/5] جاري تشغيل السيرفر...
echo.
echo ============================================
echo    افتح المتصفح على: http://localhost:8000
echo ============================================
echo.
echo اضغط Ctrl+C للإيقاف
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
