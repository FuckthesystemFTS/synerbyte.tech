import json
import time
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from ..utils.jwt import verify_jwt

router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, set[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.rooms.setdefault(room, set()).add(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: bytes) -> None:
        if room not in self.rooms:
            return
        for ws in list(self.rooms[room]):
            if ws.application_state == WebSocketState.CONNECTED:
                await ws.send_bytes(message)


manager = ConnectionManager()


@router.websocket("/ws/{conversationId}")
async def ws_endpoint(websocket: WebSocket, conversationId: str, token: str):
    try:
        claims = verify_jwt(token)
        if int(claims.get("exp", 0)) <= int(time.time()):
            await websocket.close(code=4403)
            return
    except Exception:
        await websocket.close(code=4403)
        return

    await manager.connect(conversationId, websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            await manager.broadcast(conversationId, data)
    except WebSocketDisconnect:
        manager.disconnect(conversationId, websocket)