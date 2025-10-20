from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List
from ..models import ChatRequest, AcceptChatRequest, Message, VerifyChat, SearchUsers
from ..database import db
from ..auth import verify_token
from ..websocket_manager import manager
import json

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/search-users")
async def search_users(search: SearchUsers, user: dict = Depends(verify_token)):
    """Search for users by email or username"""
    users = db.search_users(search.query, exclude_user_id=user['id'])
    return {"users": users}

@router.post("/request")
async def create_chat_request(request: ChatRequest, user: dict = Depends(verify_token)):
    """Send chat request to another user"""
    # Validate verification code (4 characters)
    if len(request.verification_code) != 4:
        raise HTTPException(status_code=400, detail="Verification code must be 4 characters")
    
    # Check if target user exists
    target_user = db.get_user_by_id(request.to_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already have active chat
    active_chats = db.get_active_chats(user['id'])
    for chat in active_chats:
        if chat['user1_id'] == request.to_user_id or chat['user2_id'] == request.to_user_id:
            raise HTTPException(status_code=400, detail="Already have active chat with this user")
    
    # Create request with expiration (24 hours)
    from datetime import datetime, timedelta
    code_expires_at = datetime.now() + timedelta(hours=24)
    request_id = db.create_chat_request(
        from_user_id=user['id'],
        to_user_id=request.to_user_id,
        verification_code=request.verification_code,
        code_expires_at=code_expires_at
    )
    
    # Notify target user via WebSocket
    await manager.broadcast_to_user(
        user_id=request.to_user_id,
        message_type="chat_request",
        data={
            "request_id": request_id,
            "from_user": {
                "id": user['id'],
                "email": user['email'],
                "username": user['username'],
                "profile_picture": user['profile_picture']
            },
            "verification_code": request.verification_code
        }
    )
    
    return {"request_id": request_id, "status": "sent"}

@router.get("/requests")
async def get_pending_requests(user: dict = Depends(verify_token)):
    """Get pending chat requests"""
    requests = db.get_pending_requests(user['id'])
    return {"requests": requests}

@router.post("/accept")
async def accept_request(accept: AcceptChatRequest, user: dict = Depends(verify_token)):
    """Accept chat request"""
    # Validate verification code
    if len(accept.verification_code) != 4:
        raise HTTPException(status_code=400, detail="Verification code must be 4 characters")
    
    # Create active chat
    try:
        chat_id = db.accept_chat_request(accept.request_id, accept.verification_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Get chat details
    chat = db.get_chat(chat_id)
    
    # Notify both users
    for user_id in [chat['user1_id'], chat['user2_id']]:
        await manager.broadcast_to_user(
            user_id=user_id,
            message_type="chat_accepted",
            data={
                "chat_id": chat_id,
                "chat": chat
            }
        )
    
    return {"chat_id": chat_id, "status": "accepted"}

@router.get("/active")
async def get_active_chats(user: dict = Depends(verify_token)):
    """Get all active chats for user"""
    chats = db.get_active_chats(user['id'])
    
    # Format chats with other user info
    formatted_chats = []
    for chat in chats:
        other_user = {
            "id": chat['other_user_id'],
            "email": chat.get('other_user_email'),
            "username": chat.get('other_user_username'),
            "profile_picture": chat.get('other_user_profile_picture')
        }
        
        formatted_chats.append({
            "id": chat['id'],
            "other_user": other_user,
            "created_at": chat.get('created_at')
        })
    
    return {"chats": formatted_chats}

@router.get("/messages/{chat_id}")
async def get_messages(chat_id: int, user: dict = Depends(verify_token)):
    """Get messages for a chat"""
    # Verify user is part of chat
    chat = db.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if chat['user1_id'] != user['id'] and chat['user2_id'] != user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    messages = db.get_messages(chat_id)
    return {"messages": messages}

@router.post("/verify")
async def verify_chat(verify: VerifyChat, user: dict = Depends(verify_token)):
    """Verify chat with code to keep it alive"""
    chat = db.get_chat(verify.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Check if user is part of chat
    if chat['user1_id'] != user['id'] and chat['user2_id'] != user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get the other user's code
    if chat['user1_id'] == user['id']:
        expected_code = chat['user2_code']
    else:
        expected_code = chat['user1_code']
    
    # Verify code
    if verify.verification_code != expected_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    # Update verification
    db.update_chat_verification(verify.chat_id)
    
    # Notify both users
    await manager.send_to_chat(
        message={
            "type": "chat_verified",
            "data": {
                "chat_id": verify.chat_id,
                "verified_by": user['id']
            }
        },
        chat_id=verify.chat_id
    )
    
    return {"status": "verified"}

@router.post("/clear/{chat_id}")
async def clear_chat_messages(chat_id: int, user: dict = Depends(verify_token)):
    """Clear all messages from a chat"""
    chat = db.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Check if user is part of chat
    if chat['user1_id'] != user['id'] and chat['user2_id'] != user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.clear_messages(chat_id)
    
    # Notify both users
    await manager.send_to_chat(
        message={
            "type": "chat_cleared",
            "data": {"chat_id": chat_id}
        },
        chat_id=chat_id
    )
    
    return {"status": "cleared"}

@router.post("/delete/{chat_id}")
async def request_delete_chat(chat_id: int, user: dict = Depends(verify_token)):
    """Request to delete a chat (requires both users' consent)"""
    chat = db.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Check if user is part of chat
    if chat['user1_id'] != user['id'] and chat['user2_id'] != user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Request deletion
    both_agreed = db.request_chat_deletion(chat_id, user['id'])
    
    if both_agreed:
        # Both users agreed, chat is deleted
        await manager.send_to_chat(
            message={
                "type": "chat_deleted",
                "data": {"chat_id": chat_id}
            },
            chat_id=chat_id
        )
        return {"status": "deleted", "message": "Chat deleted"}
    else:
        # Notify other user that this user wants to delete
        await manager.send_to_chat(
            message={
                "type": "delete_requested",
                "data": {
                    "chat_id": chat_id,
                    "requester_id": user['id']
                }
            },
            chat_id=chat_id
        )
        return {"status": "pending", "message": "Waiting for other user's consent"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    # Get token from query params
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    
    # Verify token
    session = db.get_session(token)
    if not session:
        await websocket.close(code=1008)
        return
    
    user = db.get_user_by_id(session['user_id'])
    if not user:
        await websocket.close(code=1008)
        return
    
    # Connect
    await manager.connect(websocket, user['id'])
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data['type'] == 'message':
                # Save message
                chat_id = message_data['chat_id']
                encrypted_content = message_data['encrypted_content']
                message_type = message_data.get('message_type', 'text')
                
                # Verify user is part of chat
                chat = db.get_chat(chat_id)
                if not chat or (chat['user1_id'] != user['id'] and chat['user2_id'] != user['id']):
                    continue
                
                # Save to database
                message_id = db.save_message(chat_id, user['id'], encrypted_content, message_type)
                
                # Broadcast to chat participants
                await manager.send_to_chat(
                    message={
                        "type": "message",
                        "data": {
                            "id": message_id,
                            "chat_id": chat_id,
                            "sender_id": user['id'],
                            "encrypted_content": encrypted_content,
                            "message_type": message_type,
                            "sender": {
                                "id": user['id'],
                                "email": user['email'],
                                "username": user['username'],
                                "profile_picture": user['profile_picture'],
                                "public_key": user['public_key']
                            }
                        }
                    },
                    chat_id=chat_id
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user['id'])
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user['id'])
