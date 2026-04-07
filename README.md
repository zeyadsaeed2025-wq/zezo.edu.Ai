# 🎓 EduForge AI

AI-Powered Educational Content Platform with Multi-Version Support

![EduForge AI](https://img.shields.io/badge/Status-Production-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Smart Curriculum Generation**: Create complete lessons, units, and full curriculum plans
- **Multi-Version Content**: Automatically generate Standard, Simplified, and Accessibility versions
- **Smart Assist**: Real-time AI suggestions for content improvement
- **Smart Alerts**: AI Quality Guardian detects issues in real-time
- **Fix with AI**: One-click auto-fix for detected issues
- **Live Quality Meter**: Track Interactivity, Multimedia, Assessment, and Inclusiveness
- **Inclusive Education**: Built-in support for students with special needs

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai.git
cd zezo.edu.Ai

# 2. Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# 4. Run backend
uvicorn main:app --reload

# 5. Open browser
# Navigate to http://localhost:8000
```

## 🌐 Deploy to Production

### Step 1: Set up Supabase Database

1. Go to [supabase.com](https://supabase.com) and create an account
2. Create a new project
3. Go to **SQL Editor** and run the schema from `supabase/schema.sql`
4. Go to **Settings > Database** and copy the **Connection string**

### Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click **New Project > Deploy from GitHub**
3. Select the `zezo.edu.Ai` repository
4. Set **Root Directory** to `backend`
5. Add Environment Variables:
   - `DATABASE_URL` = Your Supabase connection string
   - `OPENAI_API_KEY` = Your OpenAI API key
   - `SECRET_KEY` = Any random string (e.g., `openssl rand -base64 32`)
6. Click **Deploy**

Wait for deployment and copy your **Railway URL** (e.g., `https://zezo-edu-ai-backend.up.railway.app`)

### Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up
2. Click **Import Project**
3. Import from GitHub (`zezo.edu.Ai`)
4. Set **Root Directory** to `frontend`
5. Click **Deploy**

### Step 4: Configure Frontend

After Vercel deploys:
1. Copy your **Railway backend URL**
2. Edit `frontend/js/app.js`:
   ```javascript
   const API_BASE = 'https://your-railway-url.up.railway.app';
   ```
3. Commit and push changes
4. Vercel will auto-redeploy

## 📁 Project Structure

```
zezo.edu.Ai/
├── backend/              # FastAPI Backend
│   ├── app/              # Application code
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # AI & WebSocket services
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   └── main.py           # Entry point
├── frontend/             # Static Frontend
│   ├── css/             # Styles
│   ├── js/              # JavaScript
│   └── index.html       # Main HTML
├── supabase/            # Database schema
├── deploy.sh            # Linux/Mac deployment script
├── deploy.ps1           # Windows deployment script
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Login
- `GET /api/v1/auth/me` - Get current user

### Projects
- `POST /api/v1/projects/` - Create project
- `GET /api/v1/projects/` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/generate-curriculum` - Generate full curriculum

### AI Features
- `POST /api/v1/ai/smart-assist` - Analyze and improve content
- `POST /api/v1/ai/generate-content` - Generate lesson content
- `POST /api/v1/ai/evaluate/{project_id}` - Evaluate project quality
- `POST /api/v1/ai/analyze/{project_id}` - Detect issues
- `POST /api/v1/ai/fix-alert/{alert_id}` - Fix detected issue
- `GET /api/v1/ai/quality-metrics/{project_id}` - Get quality scores

## 🧠 Multi-Version Content

The system automatically generates three versions of content:

1. **Standard Version**: Regular educational content with full vocabulary
2. **Simplified Version**: 
   - Short sentences (max 15 words)
   - Grade 6-8 vocabulary level
   - Clear bullet points
3. **Accessibility Version**:
   - Screen reader optimized
   - Alt text for images
   - High contrast structure
   - Descriptive headings

## 🛠️ Technology Stack

- **Backend**: Python FastAPI
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **AI**: OpenAI API (GPT-4)
- **Deployment**: Vercel (Frontend) + Railway (Backend)

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | Supabase PostgreSQL connection string | Yes |
| OPENAI_API_KEY | OpenAI API key for AI features | Yes |
| SECRET_KEY | JWT signing secret | Yes |
| OPENAI_MODEL | OpenAI model (default: gpt-4-turbo-preview) | No |

## 🐳 Docker Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

Built with ❤️ for educators and students everywhere.
