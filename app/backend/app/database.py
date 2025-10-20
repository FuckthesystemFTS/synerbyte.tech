import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List, Dict

# Get DATABASE_URL from environment (Heroku sets this automatically)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///synerchat.db')

# Fix for Heroku postgres:// -> postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    username = Column(String)
    profile_picture = Column(String)
    public_key = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatRequest(Base):
    __tablename__ = 'chat_requests'
    
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default='pending')  # pending, accepted, rejected
    verification_code = Column(String)
    code_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Chat(Base):
    __tablename__ = 'chats'
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shared_secret = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    encrypted_content = Column(Text, nullable=False)
    message_type = Column(String, default='text')
    created_at = Column(DateTime, default=datetime.utcnow)

class AuthToken(Base):
    __tablename__ = 'auth_tokens'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database wrapper class
class Database:
    def __init__(self):
        Base.metadata.create_all(bind=engine)
    
    def get_session(self):
        return SessionLocal()
    
    def init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(bind=engine)
    
    # User methods
    def create_user(self, email: str, password_hash: str, username: Optional[str] = None, 
                   profile_picture: Optional[str] = None, public_key: Optional[str] = None) -> Optional[int]:
        session = self.get_session()
        try:
            user = User(
                email=email,
                password_hash=password_hash,
                username=username,
                profile_picture=profile_picture,
                public_key=public_key
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user.id
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            session.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.email == email).first()
            if user:
                return {
                    'id': user.id,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'username': user.username,
                    'profile_picture': user.profile_picture,
                    'public_key': user.public_key,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            return None
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'profile_picture': user.profile_picture,
                    'public_key': user.public_key,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            return None
        finally:
            session.close()
    
    def update_user(self, user_id: int, username: Optional[str] = None,
                   profile_picture: Optional[str] = None, public_key: Optional[str] = None) -> bool:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            if username is not None:
                user.username = username
            if profile_picture is not None:
                user.profile_picture = profile_picture
            if public_key is not None:
                user.public_key = public_key
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {e}")
            return False
        finally:
            session.close()
    
    # Auth token methods
    def create_token(self, user_id: int, token: str, expires_at: datetime) -> bool:
        session = self.get_session()
        try:
            auth_token = AuthToken(user_id=user_id, token=token, expires_at=expires_at)
            session.add(auth_token)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error creating token: {e}")
            return False
        finally:
            session.close()
    
    def get_token(self, token: str) -> Optional[Dict]:
        session = self.get_session()
        try:
            auth_token = session.query(AuthToken).filter(AuthToken.token == token).first()
            if auth_token:
                return {
                    'user_id': auth_token.user_id,
                    'token': auth_token.token,
                    'expires_at': auth_token.expires_at.isoformat()
                }
            return None
        finally:
            session.close()
    
    def delete_token(self, token: str) -> bool:
        session = self.get_session()
        try:
            session.query(AuthToken).filter(AuthToken.token == token).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting token: {e}")
            return False
        finally:
            session.close()
    
    # Chat request methods
    def create_chat_request(self, from_user_id: int, to_user_id: int, 
                           verification_code: str, code_expires_at: datetime) -> Optional[int]:
        session = self.get_session()
        try:
            chat_request = ChatRequest(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                verification_code=verification_code,
                code_expires_at=code_expires_at
            )
            session.add(chat_request)
            session.commit()
            session.refresh(chat_request)
            return chat_request.id
        except Exception as e:
            session.rollback()
            print(f"Error creating chat request: {e}")
            return None
        finally:
            session.close()
    
    def get_chat_requests(self, user_id: int) -> List[Dict]:
        session = self.get_session()
        try:
            requests = session.query(ChatRequest).filter(
                ChatRequest.to_user_id == user_id,
                ChatRequest.status == 'pending'
            ).all()
            
            result = []
            for req in requests:
                from_user = session.query(User).filter(User.id == req.from_user_id).first()
                result.append({
                    'id': req.id,
                    'from_user_id': req.from_user_id,
                    'to_user_id': req.to_user_id,
                    'status': req.status,
                    'verification_code': req.verification_code,
                    'code_expires_at': req.code_expires_at.isoformat() if req.code_expires_at else None,
                    'created_at': req.created_at.isoformat() if req.created_at else None,
                    'from_user_email': from_user.email if from_user else None,
                    'from_user_username': from_user.username if from_user else None
                })
            return result
        finally:
            session.close()
    
    def update_chat_request_status(self, request_id: int, status: str) -> bool:
        session = self.get_session()
        try:
            chat_request = session.query(ChatRequest).filter(ChatRequest.id == request_id).first()
            if not chat_request:
                return False
            chat_request.status = status
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error updating chat request: {e}")
            return False
        finally:
            session.close()
    
    def get_chat_request_by_id(self, request_id: int) -> Optional[Dict]:
        session = self.get_session()
        try:
            req = session.query(ChatRequest).filter(ChatRequest.id == request_id).first()
            if req:
                return {
                    'id': req.id,
                    'from_user_id': req.from_user_id,
                    'to_user_id': req.to_user_id,
                    'status': req.status,
                    'verification_code': req.verification_code,
                    'code_expires_at': req.code_expires_at.isoformat() if req.code_expires_at else None,
                    'created_at': req.created_at.isoformat() if req.created_at else None
                }
            return None
        finally:
            session.close()
    
    # Chat methods
    def create_chat(self, user1_id: int, user2_id: int, shared_secret: str) -> Optional[int]:
        session = self.get_session()
        try:
            chat = Chat(user1_id=user1_id, user2_id=user2_id, shared_secret=shared_secret)
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return chat.id
        except Exception as e:
            session.rollback()
            print(f"Error creating chat: {e}")
            return None
        finally:
            session.close()
    
    def get_user_chats(self, user_id: int) -> List[Dict]:
        session = self.get_session()
        try:
            chats = session.query(Chat).filter(
                (Chat.user1_id == user_id) | (Chat.user2_id == user_id)
            ).all()
            
            result = []
            for chat in chats:
                other_user_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id
                other_user = session.query(User).filter(User.id == other_user_id).first()
                
                result.append({
                    'id': chat.id,
                    'user1_id': chat.user1_id,
                    'user2_id': chat.user2_id,
                    'created_at': chat.created_at.isoformat() if chat.created_at else None,
                    'other_user_id': other_user_id,
                    'other_user_email': other_user.email if other_user else None,
                    'other_user_username': other_user.username if other_user else None,
                    'other_user_profile_picture': other_user.profile_picture if other_user else None
                })
            return result
        finally:
            session.close()
    
    def get_chat_by_id(self, chat_id: int) -> Optional[Dict]:
        session = self.get_session()
        try:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                return {
                    'id': chat.id,
                    'user1_id': chat.user1_id,
                    'user2_id': chat.user2_id,
                    'shared_secret': chat.shared_secret,
                    'created_at': chat.created_at.isoformat() if chat.created_at else None
                }
            return None
        finally:
            session.close()
    
    # Message methods
    def create_message(self, chat_id: int, sender_id: int, encrypted_content: str, 
                      message_type: str = 'text') -> Optional[int]:
        session = self.get_session()
        try:
            message = Message(
                chat_id=chat_id,
                sender_id=sender_id,
                encrypted_content=encrypted_content,
                message_type=message_type
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message.id
        except Exception as e:
            session.rollback()
            print(f"Error creating message: {e}")
            return None
        finally:
            session.close()
    
    def get_chat_messages(self, chat_id: int, limit: int = 100) -> List[Dict]:
        session = self.get_session()
        try:
            messages = session.query(Message).filter(
                Message.chat_id == chat_id
            ).order_by(Message.created_at.desc()).limit(limit).all()
            
            result = []
            for msg in messages:
                sender = session.query(User).filter(User.id == msg.sender_id).first()
                result.append({
                    'id': msg.id,
                    'chat_id': msg.chat_id,
                    'sender_id': msg.sender_id,
                    'encrypted_content': msg.encrypted_content,
                    'message_type': msg.message_type,
                    'created_at': msg.created_at.isoformat() if msg.created_at else None,
                    'email': sender.email if sender else None,
                    'username': sender.username if sender else None,
                    'profile_picture': sender.profile_picture if sender else None
                })
            return list(reversed(result))
        finally:
            session.close()
    
    # Search methods
    def search_users(self, query: str, exclude_user_id: Optional[int] = None) -> List[Dict]:
        session = self.get_session()
        try:
            search_query = session.query(User).filter(
                (User.email.ilike(f'%{query}%')) | (User.username.ilike(f'%{query}%'))
            )
            if exclude_user_id:
                search_query = search_query.filter(User.id != exclude_user_id)
            
            users = search_query.limit(10).all()
            result = []
            for user in users:
                result.append({
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'profile_picture': user.profile_picture
                })
            return result
        finally:
            session.close()
    
    def get_active_chats(self, user_id: int) -> List[Dict]:
        """Alias for get_user_chats"""
        return self.get_user_chats(user_id)
    
    def get_pending_requests(self, user_id: int) -> List[Dict]:
        """Alias for get_chat_requests"""
        return self.get_chat_requests(user_id)

# Global instance
db = Database()
