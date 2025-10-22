"""
Notifications API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..database import db
from ..services.push_notifications import push_service
from .auth import get_current_user

router = APIRouter(prefix='/api/notifications', tags=['notifications'])

class FCMTokenRequest(BaseModel):
    token: str
    device_type: Optional[str] = 'unknown'

class NotificationTestRequest(BaseModel):
    user_id: int
    unread_count: int

@router.post('/register-token')
async def register_fcm_token(
    request: FCMTokenRequest,
    current_user: dict = Depends(get_current_user)
):
    """Register or update FCM token for push notifications"""
    try:
        success = db.save_fcm_token(
            user_id=current_user['id'],
            token=request.token,
            device_type=request.device_type
        )
        
        if success:
            return {'success': True, 'message': 'FCM token registered successfully'}
        else:
            raise HTTPException(status_code=500, detail='Failed to register FCM token')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/unregister-token')
async def unregister_fcm_token(
    request: FCMTokenRequest,
    current_user: dict = Depends(get_current_user)
):
    """Unregister FCM token"""
    try:
        success = db.delete_fcm_token(request.token)
        
        if success:
            return {'success': True, 'message': 'FCM token unregistered successfully'}
        else:
            raise HTTPException(status_code=500, detail='Failed to unregister FCM token')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/unread-count')
async def get_unread_count(
    current_user: dict = Depends(get_current_user)
):
    """Get unread message count for current user"""
    try:
        count = db.get_unread_message_count(current_user['id'])
        return {'unread_count': count}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/test')
async def test_notification(
    request: NotificationTestRequest,
    current_user: dict = Depends(get_current_user)
):
    """Test push notification (for development only)"""
    try:
        # Get user's FCM tokens
        tokens = db.get_user_fcm_tokens(request.user_id)
        
        if not tokens:
            raise HTTPException(status_code=404, detail='No FCM tokens found for user')
        
        # Send notification to first token
        success = await push_service.send_notification(
            token=tokens[0],
            unread_count=request.unread_count
        )
        
        if success:
            return {'success': True, 'message': 'Test notification sent'}
        else:
            raise HTTPException(status_code=500, detail='Failed to send notification')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_new_message_notification(recipient_user_id: int):
    """
    Send push notification when a new message is received
    Called internally when a message is sent
    """
    try:
        # Get recipient's FCM tokens
        tokens = db.get_user_fcm_tokens(recipient_user_id)
        
        if not tokens:
            return False
        
        # Get unread count
        unread_count = db.get_unread_message_count(recipient_user_id)
        
        # Send notification to all user's devices
        result = await push_service.send_batch_notifications(
            tokens=tokens,
            unread_count=unread_count
        )
        
        return result['success'] > 0
    
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False
