#!/bin/bash

# EduForge AI - One-Click Deployment Script

echo "🎓 EduForge AI Deployment Script"
echo "================================"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Installing GitHub CLI..."
    # Windows
    if command -v choco &> /dev/null; then
        choco install gh
    fi
fi

echo ""
echo "📋 Deployment Steps:"
echo "-------------------"
echo ""
echo "1. SUPABASE SETUP:"
echo "   - Go to https://supabase.com"
echo "   - Create a new project"
echo "   - Go to Settings > Database"
echo "   - Copy the Connection string (URI)"
echo "   - Add it to Railway environment variables"
echo ""
echo "2. RAILWAY BACKEND DEPLOYMENT:"
echo "   - Go to https://railway.app"
echo "   - Login with GitHub"
echo "   - Click 'New Project' > 'Deploy from GitHub'"
echo "   - Select this repository"
echo "   - Set Root Directory to 'backend'"
echo "   - Add Environment Variables:"
echo "     * DATABASE_URL = your Supabase connection string"
echo "     * OPENAI_API_KEY = your OpenAI key"
echo "     * SECRET_KEY = any random string"
echo ""
echo "3. FRONTEND DEPLOYMENT:"
echo "   - Go to https://vercel.com"
echo "   - Import this GitHub repository"
echo "   - Set Root Directory to 'frontend'"
echo "   - Deploy!"
echo ""
echo "4. UPDATE FRONTEND API URL:"
echo "   - After Railway deploys, copy your backend URL"
echo "   - Edit frontend/js/app.js and update:"
echo "     const API_BASE = 'https://your-railway-url.up.railway.app';"
echo ""

# Quick deploy commands
echo ""
echo "🚀 QUICK DEPLOY COMMANDS:"
echo "-------------------------"
echo ""
echo "# Deploy frontend to Vercel (run in frontend directory)"
echo "cd frontend"
echo "vercel"
echo ""
echo "# Or deploy to Vercel with project linking"
echo "vercel --prod"
