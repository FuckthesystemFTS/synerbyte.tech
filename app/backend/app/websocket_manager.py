from fastapi import WebSocket
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime, timedelta
from .database import db

class ConnectionManager:
    def __init__(self):
        # user_id -> list of websocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # chat_id -> set of user_ids
        self.chat_participants: Dict[int, Set[int]] = {}
        # Background task for verification checks
        self.verification_task = None
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        # Start verification checker if not running
        if self.verification_task is None:
            self.verification_task = asyncio.create_task(self.check_verifications())
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to all connections of a specific user"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def send_to_chat(self, message: dict, chat_id: int, exclude_user_id: int = None):
        """Send message to all participants in a chat"""
        chat = db.get_chat(chat_id)
        if not chat:
            return
        
        user_ids = [chat['user1_id'], chat['user2_id']]
        if exclude_user_id:
            user_ids = [uid for uid in user_ids if uid != exclude_user_id]
        
        for user_id in user_ids:
            await self.send_personal_message(message, user_id)
    
    async def broadcast_to_user(self, user_id: int, message_type: str, data: dict):
        """Broadcast a typed message to user"""
        message = {
            "type": message_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_personal_message(message, user_id)
    
    async def check_verifications(self):
        """Background task to check for required verifications"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Get all active chats
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM active_chats 
                    WHERE verification_pending = 0
                ''')
                chats = [dict(row) for row in cursor.fetchall()]
                
                now = datetime.now()
                
                for chat in chats:
                    next_verification = datetime.fromisoformat(chat['next_verification'])
                    
                    # If we're past the 30-minute mark, start 5-minute verification window
                    if now >= next_verification and not chat['verification_pending']:
                        db.set_verification_pending(chat['id'])
                        
                        # Notify both users
                        message = {
                            "type": "verification_required",
                            "data": {
                                "chat_id": chat['id'],
                                "deadline": (now + timedelta(minutes=5)).isoformat()
                            }
                        }
                        
                        await self.send_personal_message(message, chat['user1_id'])
                        await self.send_personal_message(message, chat['user2_id'])
                    
                    # Check if verification window expired
                    elif chat['verification_pending']:
                        verification_deadline = next_verification + timedelta(minutes=5)
                        if now >= verification_deadline:
                            # Destroy chat
                            db.delete_chat(chat['id'])
                            
                            # Notify both users
                            message = {
                                "type": "chat_destroyed",
                                "data": {
                                    "chat_id": chat['id'],
                                    "reason": "Verification timeout"
                                }
                            }
                            
                            await self.send_personal_message(message, chat['user1_id'])
                            await self.send_personal_message(message, chat['user2_id'])
            
            except Exception as e:
                print(f"Error in verification checker: {e}")
                await asyncio.sleep(60)

manager = ConnectionManager()
