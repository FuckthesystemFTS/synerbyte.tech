import os
from datetime import timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from .routers import auth, keys, payments, ws


JWT_TTL_SECONDS = int(os.getenv("JWT_TTL_SECONDS", "600"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Synerchat Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(keys.router, prefix="/keys", tags=["keys"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(ws.router, tags=["ws"])  # includes /ws/{conversationId}

@app.get("/healthz")
async def healthz():
    return {"ok": True, "ttl": JWT_TTL_SECONDS}