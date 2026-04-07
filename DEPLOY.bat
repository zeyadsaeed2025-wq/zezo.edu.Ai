@echo off
echo ====================================
echo   EduForge AI - Auto Deploy
echo ====================================
echo.

echo [1/4] Checking dependencies...
npm list vercel >nul 2>&1
if %errorlevel% neq 0 npm install -g vercel

echo [2/4] Committing changes...
git add .
git commit -m "Deploy update" >nul 2>&1
git push

echo [3/4] Deploying frontend to Vercel...
cd frontend
echo Set your API_BASE in js/app.js first!
echo Example: const API_BASE = 'https://your-backend-url.onrender.com';
echo.
echo Commands to run manually:
echo   vercel login
echo   vercel --prod
cd ..

echo [4/4] Deploying backend to Render...
echo.
echo Go to: https://render.com
echo 1. Login with GitHub
echo 2. Click "New" -^> "Blueprint"
echo 3. Connect this repo
echo 4. Select backend/render.yaml
echo 5. Add OPENAI_API_KEY env var
echo 6. Click "Apply"
echo.
echo ====================================
echo   After deployment:
echo   1. Copy your Render URL
echo   2. Update frontend/js/app.js
echo   3. Push to redeploy
echo ====================================

pause
