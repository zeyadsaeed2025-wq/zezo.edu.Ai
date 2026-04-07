from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI(
    title="EduForge AI",
    version="1.0.0",
    description="AI-Powered Educational Content Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api import auth, projects, ai, websocket

app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(websocket.router)

@app.on_event("startup")
async def startup():
    from app.core.database import init_db
    await init_db()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EduForge AI"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "service": "EduForge AI"}

@app.get("/")
async def root():
    frontend_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return JSONResponse({
        "message": "EduForge AI API",
        "version": "1.0.0",
        "docs": "/docs"
    })

@app.get("/{path:path}")
async def serve_static(path: str):
    # Don't intercept API routes
    if path.startswith("api/") or path.startswith("docs") or path.startswith("openapi"):
        return JSONResponse({"error": "Not found"}, status_code=404)
    
    # Try to serve from current directory
    if os.path.exists(path):
        return FileResponse(path)
    
    # Try index.html for SPA routing
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return JSONResponse({"error": "Not found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
