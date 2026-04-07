# EduForge AI - Deployment Script for Windows

Write-Host "🎓 EduForge AI Deployment Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if Vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host ""
Write-Host "📋 Deployment Steps:" -ForegroundColor Green
Write-Host "-------------------"
Write-Host ""
Write-Host "1. SUPABASE SETUP:" -ForegroundColor Cyan
Write-Host "   - Go to https://supabase.com"
Write-Host "   - Create a new project"
Write-Host "   - Go to Settings > Database"
Write-Host "   - Copy the Connection string (URI)"
Write-Host "   - Add it to Railway environment variables"
Write-Host ""
Write-Host "2. RAILWAY BACKEND DEPLOYMENT:" -ForegroundColor Cyan
Write-Host "   - Go to https://railway.app"
Write-Host "   - Login with GitHub"
Write-Host "   - Click 'New Project' > 'Deploy from GitHub'"
Write-Host "   - Select this repository"
Write-Host "   - Set Root Directory to 'backend'"
Write-Host "   - Add Environment Variables:"
Write-Host "     * DATABASE_URL = your Supabase connection string"
Write-Host "     * OPENAI_API_KEY = your OpenAI key"
Write-Host "     * SECRET_KEY = any random string"
Write-Host ""
Write-Host "3. FRONTEND DEPLOYMENT:" -ForegroundColor Cyan
Write-Host "   - Go to https://vercel.com"
Write-Host "   - Import this GitHub repository"
Write-Host "   - Set Root Directory to 'frontend'"
Write-Host "   - Deploy!"
Write-Host ""
Write-Host "4. UPDATE FRONTEND API URL:" -ForegroundColor Cyan
Write-Host "   - After Railway deploys, copy your backend URL"
Write-Host "   - Edit frontend/js/app.js and update:"
Write-Host "     const API_BASE = 'https://your-railway-url.up.railway.app';"
Write-Host ""

# Deploy to Vercel
Write-Host ""
Write-Host "🚀 Deploying Frontend to Vercel..." -ForegroundColor Green
Set-Location "frontend"
vercel --yes
Set-Location ".."

Write-Host ""
Write-Host "✅ Deployment initiated!" -ForegroundColor Green
Write-Host "Check Vercel dashboard for deployment status" -ForegroundColor Yellow
