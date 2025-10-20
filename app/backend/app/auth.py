import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Header
from .database import db

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash

def generate_token() -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(32)

def create_session(user_id: int) -> tuple[str, str]:
    """Create session and return token and expiry"""
    token = generate_token()
    expires_at = datetime.now() + timedelta(days=7)
    db.create_session(user_id, token, expires_at.isoformat())
    return token, expires_at.isoformat()

def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    """Verify authorization token and return user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    session = db.get_session(token)
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check expiry
    expires_at = datetime.fromisoformat(session['expires_at'])
    if datetime.now() > expires_at:
        db.delete_session(token)
        raise HTTPException(status_code=401, detail="Token expired")
    
    user = db.get_user_by_id(session['user_id'])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def encrypt_data(data: str, key: str) -> str:
    """Simple XOR encryption for database (not for messages)"""
    key_bytes = key.encode()
    data_bytes = data.encode()
    encrypted = bytearray()
    for i, byte in enumerate(data_bytes):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    return encrypted.hex()

def decrypt_data(encrypted_hex: str, key: str) -> str:
    """Simple XOR decryption for database"""
    key_bytes = key.encode()
    encrypted = bytearray.fromhex(encrypted_hex)
    decrypted = bytearray()
    for i, byte in enumerate(encrypted):
        decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    return decrypted.decode()
