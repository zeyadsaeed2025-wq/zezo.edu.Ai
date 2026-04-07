# EduForge AI - Production Ready

## Quick Start

### Local Development
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open: http://localhost:8000

### Test Account
- Username: testuser
- Password: test123

## Features Working

1. User Registration & Login
2. Curriculum Generation (AI)
3. Multi-Version Content (Standard, Simplified, Accessibility)
4. Smart Assist
5. Smart Alerts
6. Quality Meter

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/auth/register | POST | Register user |
| /api/v1/auth/token | POST | Login |
| /api/v1/auth/me | GET | Get current user |
| /api/v1/projects/generate-curriculum | POST | Generate curriculum |
| /api/v1/ai/smart-assist | POST | AI suggestions |
| /api/v1/ai/evaluate/{id} | POST | Evaluate project |

## Deployment

See DEPLOY.md for full deployment instructions.

## Links

- GitHub: https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai
- Supabase: https://jnzqdznnhcjeovmvznuq.supabase.co
- Railway: https://railway.com/project/3d1fbc84-0967-4b43-8b36-98ad4ff8afd2
