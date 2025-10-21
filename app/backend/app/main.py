import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import auth, chat
from .database import db

CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

app = FastAPI(title='Synerchat Backend', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins in development
    allow_credentials=False,  # Must be False when allow_origins is ['*']
    allow_methods=['*'],
    allow_headers=['*']
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)

@app.get('/healthz')
async def healthz():
    return {'ok': True, 'version': '1.0.0'}

# Serve mobile app downloads
downloads_path = os.path.join(os.path.dirname(__file__), '../downloads')
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

@app.get("/downloads/{filename}")
async def download_app(filename: str):
    """Serve mobile app downloads (APK/IPA)"""
    file_path = os.path.join(downloads_path, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Set appropriate content type
        content_type = "application/vnd.android.package-archive" if filename.endswith('.apk') else "application/octet-stream"
        return FileResponse(
            file_path, 
            media_type=content_type,
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache"
            }
        )
    return {"error": "File not found"}

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), '../static')
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_path, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_path, "index.html"))

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    db.init_db()
    print("Database initialized")
    print("Synerchat backend ready!")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    print("Shutting down Synerchat backend")
