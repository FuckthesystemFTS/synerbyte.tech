import os
import time
from typing import Optional
from jose import jwt


JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ISSUER = os.getenv("JWT_ISSUER", "synerchat")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "synerchat-clients")
ALG = "HS256"


def issue_jwt(subject: str, device_id: str, expires_at: int) -> str:
    now = int(time.time())
    payload = {
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "sub": subject,
        "deviceId": device_id,
        "iat": now,
        "exp": expires_at,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALG)


def verify_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[ALG], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)