import uvicorn
import os
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./eduforge.db'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['SECRET_KEY'] = 'eduforge-secret-2024'
from main import app
print('Server starting on port 8080...')
uvicorn.run(app, host='0.0.0.0', port=8080)
