from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    public_key: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    email: str
    username: Optional[str]
    profile_picture: Optional[str]
    public_key: Optional[str]
    created_at: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    public_key: Optional[str] = None

class ChatRequest(BaseModel):
    to_user_id: int
    verification_code: str

class ChatRequestResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    verification_code: str
    status: str
    created_at: str
    email: str
    username: Optional[str]
    profile_picture: Optional[str]

class AcceptChatRequest(BaseModel):
    request_id: int
    verification_code: str

class ChatInfo(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    user1_code: str
    user2_code: str
    last_verification: str
    next_verification: str
    verification_pending: bool
    created_at: str
    other_user: dict

class Message(BaseModel):
    chat_id: int
    content: str
    message_type: Optional[str] = 'text'

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    encrypted_content: str
    created_at: str
    email: str
    username: Optional[str]
    profile_picture: Optional[str]

class VerifyChat(BaseModel):
    chat_id: int
    verification_code: str

class SearchUsers(BaseModel):
    query: str

class WSMessage(BaseModel):
    type: str  # 'message', 'verification_required', 'chat_destroyed', etc.
    data: dict
