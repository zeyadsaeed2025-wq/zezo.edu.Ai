# EduForge AI - Deployment Guide

## 🚀 Deploy to Vercel + Supabase

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai.git
git push -u origin main
```

### Step 2: Set up Supabase Database

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the database to be provisioned
3. Go to Settings > Database
4. Copy the **Connection string** (URI format: `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres`)
5. Save this connection string

### Step 3: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Add New Project > Deploy from GitHub
4. Select the `backend` folder
5. Add Environment Variables:
   - `DATABASE_URL` = Your Supabase connection string
   - `OPENAI_API_KEY` = Your OpenAI API key
   - `SECRET_KEY` = Generate a random secret
6. Deploy!

Your backend will be live at: `https://zezo-edu-ai-backend.up.railway.app`

### Step 4: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import the GitHub repo
3. Set Root Directory to `frontend`
4. Update `vercel.json` with your backend URL:
   ```json
   {
     "rewrites": [
       { "source": "/api/(.*)", "destination": "https://your-backend-url.railway.app/api/$1" }
     ]
   }
   ```
5. Deploy!

### Step 5: Update Frontend API URL

Edit `frontend/static/js/app.js` and update the API_BASE URL to your backend:
```javascript
const API_BASE = 'https://your-backend-url.railway.app';
```

## 🐳 Alternative: Docker Deployment

```bash
# Start with Docker Compose
docker-compose up -d
```

## 📁 Project Structure

```
zezo.edu.Ai/
├── backend/           # FastAPI Backend
│   ├── app/          # Application code
│   ├── api/          # Serverless functions
│   ├── static/       # Static assets
│   ├── templates/    # HTML templates
│   └── vercel.json   # Vercel config
├── frontend/         # Static Frontend
│   ├── static/       # CSS, JS
│   └── vercel.json   # Vercel config
├── docker-compose.yml
└── README.md
```

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | Supabase PostgreSQL connection string | Yes |
| OPENAI_API_KEY | OpenAI API key for AI features | Yes |
| SECRET_KEY | JWT signing secret | Yes |
| OPENAI_MODEL | OpenAI model (default: gpt-4-turbo-preview) | No |

## 🌐 API Endpoints

Once deployed, your API will be available at:
- `https://your-backend-url.railway.app/api/v1/`
- `https://your-backend-url.railway.app/docs` (Swagger docs)

## ❓ Troubleshooting

### CORS Errors
Make sure CORS is configured to allow your frontend domain in `backend/app/main.py`

### Database Connection Issues
Verify your Supabase connection string is correct and the password is URL-encoded if it contains special characters.

### WebSocket Not Working
Vercel doesn't support WebSockets natively. Consider using a service like Pusher or Ably for real-time features, or deploy to Railway/Render which supports WebSockets.

## 📝 Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your credentials
uvicorn main:app --reload

# Frontend (optional, backend serves static files)
cd frontend
npx serve -s . -l 3000
```
