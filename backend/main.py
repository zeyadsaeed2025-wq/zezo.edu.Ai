from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import init_db
from app.api import auth, projects, ai, websocket
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Educational Content Platform",
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
    return FileResponse("frontend/index.html")

@app.get("/{path:path}")
async def serve_static(path: str):
    file_path = f"frontend/{path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EduForge AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
