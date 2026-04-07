from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import init_db
from app.api import auth, projects, ai, websocket

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Educational Content Platform with Multi-Version Support",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(websocket.router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def root():
    return FileResponse("templates/index.html")

@app.get("/app.js")
async def serve_js():
    return FileResponse("static/js/app.js", media_type="application/javascript")

@app.get("/app.css")
async def serve_css():
    return FileResponse("static/css/styles.css", media_type="text/css")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EduForge AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
