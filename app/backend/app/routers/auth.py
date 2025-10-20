from fastapi import APIRouter, HTTPException, Depends
from ..models import UserRegister, UserLogin, UserProfile, UserUpdate
from ..database import db
from ..auth import hash_password, verify_password, create_session, verify_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user: UserRegister):
    """Register new user"""
    # Check if user exists
    existing = db.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    password_hash = hash_password(user.password)
    
    # Create user
    user_id = db.create_user(
        email=user.email,
        password_hash=password_hash,
        username=user.username,
        profile_picture=user.profile_picture,
        public_key=user.public_key
    )
    
    # Create session
    token, expires_at = create_session(user_id)
    
    # Get user data
    user_data = db.get_user_by_id(user_id)
    
    return {
        "token": token,
        "expires_at": expires_at,
        "user": {
            "id": user_data['id'],
            "email": user_data['email'],
            "username": user_data['username'],
            "profile_picture": user_data['profile_picture'],
            "public_key": user_data['public_key']
        }
    }

@router.post("/login")
async def login(credentials: UserLogin):
    """Login user"""
    # Get user
    user = db.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create session
    token, expires_at = create_session(user['id'])
    
    return {
        "token": token,
        "expires_at": expires_at,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "username": user['username'],
            "profile_picture": user['profile_picture'],
            "public_key": user['public_key']
        }
    }

@router.get("/me")
async def get_current_user(user: dict = Depends(verify_token)):
    """Get current user profile"""
    return {
        "id": user['id'],
        "email": user['email'],
        "username": user['username'],
        "profile_picture": user['profile_picture'],
        "public_key": user['public_key'],
        "created_at": user['created_at']
    }

@router.put("/me")
async def update_profile(update: UserUpdate, user: dict = Depends(verify_token)):
    """Update user profile"""
    db.update_user_profile(
        user_id=user['id'],
        username=update.username,
        profile_picture=update.profile_picture,
        public_key=update.public_key
    )
    
    # Get updated user
    updated_user = db.get_user_by_id(user['id'])
    
    return {
        "id": updated_user['id'],
        "email": updated_user['email'],
        "username": updated_user['username'],
        "profile_picture": updated_user['profile_picture'],
        "public_key": updated_user['public_key']
    }

@router.post("/logout")
async def logout(user: dict = Depends(verify_token)):
    """Logout user (invalidate token)"""
    # Note: In production, you'd want to get the actual token from the request
    # For now, this is a placeholder
    return {"message": "Logged out successfully"}
