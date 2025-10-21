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
        print(f"Broadcasting {message_type} to user {user_id}: {data}")
        await self.send_personal_message(message, user_id)
        print(f"Broadcast complete to user {user_id}")
    
    async def check_verifications(self):
        """Background task to check for required verifications - DISABLED for now"""
        while True:
            try:
                await asyncio.sleep(300)  # Sleep 5 minutes
                # Verification system disabled - needs database schema update
                pass
            except Exception as e:
                print(f"Error in verification checker: {e}")
                await asyncio.sleep(300)

manager = ConnectionManager()
