import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
