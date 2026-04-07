# EduForge AI - One-Click Deploy

## Deploy to Vercel (Frontend)

1. Go to: https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repo: `zezo.edu.Ai`
4. Set Root Directory: `frontend`
5. Click "Deploy"

## Deploy to Railway (Backend)

1. Go to: https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select repo: `zezo.edu.Ai`
4. Set Root Directory: `backend`
5. Add Environment Variables:
   - `DATABASE_URL` = your Supabase connection string
   - `OPENAI_API_KEY` = your OpenAI key
   - `SECRET_KEY` = any random string
6. Click "Deploy"

## Update Frontend API URL

After Railway deploys:
1. Copy your Railway URL (e.g., `https://zezo-edu-ai-backend.up.railway.app`)
2. Edit `frontend/js/app.js` line 5:
```javascript
const API_BASE = 'https://your-railway-url.up.railway.app';
```
3. Commit and push to redeploy

## Supabase Setup

1. Go to https://supabase.com
2. Create new project
3. Run `supabase/schema.sql` in SQL Editor
4. Copy Connection string from Settings → Database
5. Use as `DATABASE_URL` in Railway
