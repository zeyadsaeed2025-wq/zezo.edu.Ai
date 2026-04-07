"""
EduForge AI - One-Click Deploy
Creates a free deployment on Render.com
"""
import requests
import json
import os
import time

GITHUB_REPO = "https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai"
SUPABASE_URL = "https://jnzqdznnhcjeovmvznuq.supabase.co"

def deploy_to_render():
    print("=" * 50)
    print("EduForge AI - Deploy to Render.com")
    print("=" * 50)
    
    print("\n[1] Create Render Account:")
    print("    1. Go to: https://render.com")
    print("    2. Click 'Get Started'")
    print("    3. Sign up with GitHub")
    print()
    
    print("[2] Create PostgreSQL Database:")
    print("    1. In Render dashboard, click 'New +'")
    print("    2. Select 'PostgreSQL'")
    print("    3. Name it: eduforge-db")
    print("    4. Select Free tier")
    print("    5. Click 'Create Database'")
    print("    6. Copy the 'Internal Database URL'")
    print()
    
    print("[3] Create Web Service:")
    print("    1. Click 'New +' > 'Web Service'")
    print("    2. Connect your GitHub repo")
    print("    3. Set Root Directory: backend")
    print("    4. Set Build Command: pip install -r requirements.txt")
    print("    5. Set Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT")
    print("    6. Add Environment Variables:")
    print("       - DATABASE_URL: (paste PostgreSQL URL from step 2)")
    print("       - OPENAI_API_KEY: (your OpenAI key)")
    print("       - SECRET_KEY: any-random-string")
    print("    7. Click 'Create Web Service'")
    print()
    
    print("[4] Update Frontend API URL:")
    print("    After deployment, copy the Render URL")
    print("    Edit frontend/js/app.js and update:")
    print("    const API_BASE = 'https://your-render-url.onrender.com'")
    print()
    
    print("=" * 50)
    print("FREE ALTERNATIVES:")
    print("=" * 50)
    print()
    print("Option A - PythonAnywhere (Easiest):")
    print("  1. Go to pythonanywhere.com")
    print("  2. Sign up free")
    print("  3. Open Bash console")
    print("  4. Run: git clone https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai")
    print("  5. cd zezo.edu.Ai/backend")
    print("  6. pip install -r requirements.txt")
    print("  7. python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    print()
    
    print("Option B - Railway (Recommended):")
    print("  1. Go to railway.app")
    print("  2. Login with GitHub")
    print("  3. New Project > Deploy from GitHub")
    print("  4. Select zezo.edu.Ai repo")
    print("  5. Set root to 'backend'")
    print("  6. Add env vars and deploy!")
    print()
    
    print("=" * 50)
    print("Your project is ready at:")
    print("https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai")
    print("=" * 50)

if __name__ == "__main__":
    deploy_to_render()
    input("\nPress Enter to exit...")
