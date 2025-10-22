"""
Push Notifications Service using Firebase Cloud Messaging
"""
import os
from typing import List, Optional
from firebase_admin import credentials, messaging, initialize_app
import logging

logger = logging.getLogger(__name__)

class PushNotificationService:
    def __init__(self):
        self.initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase credentials are available
            firebase_cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
            
            if firebase_cred_path and os.path.exists(firebase_cred_path):
                cred = credentials.Certificate(firebase_cred_path)
                initialize_app(cred)
                self.initialized = True
                logger.info("Firebase initialized successfully")
            else:
                logger.warning("Firebase credentials not found. Push notifications disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            self.initialized = False
    
    async def send_notification(
        self,
        token: str,
        unread_count: int,
        data: Optional[dict] = None
    ) -> bool:
        """
        Send push notification to a device
        
        Args:
            token: FCM device token
            unread_count: Number of unread messages
            data: Additional data to send with notification
        
        Returns:
            True if notification sent successfully, False otherwise
        """
        if not self.initialized:
            logger.warning("Firebase not initialized. Cannot send notification.")
            return False
        
        try:
            # Create notification message
            message = messaging.Message(
                notification=messaging.Notification(
                    title='New Messages',
                    body=f'You have {unread_count} unread message{"s" if unread_count > 1 else ""}',
                ),
                data=data or {},
                token=token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default',
                        badge=unread_count,
                        channel_id='messages',
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            badge=unread_count,
                            sound='default',
                            content_available=True,
                        )
                    )
                )
            )
            
            # Send the message
            response = messaging.send(message)
            logger.info(f"Successfully sent notification: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    async def send_batch_notifications(
        self,
        tokens: List[str],
        unread_count: int,
        data: Optional[dict] = None
    ) -> dict:
        """
        Send notifications to multiple devices
        
        Args:
            tokens: List of FCM device tokens
            unread_count: Number of unread messages
            data: Additional data to send with notification
        
        Returns:
            Dictionary with success and failure counts
        """
        if not self.initialized:
            logger.warning("Firebase not initialized. Cannot send notifications.")
            return {"success": 0, "failure": len(tokens)}
        
        try:
            # Create multicast message
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title='New Messages',
                    body=f'You have {unread_count} unread message{"s" if unread_count > 1 else ""}',
                ),
                data=data or {},
                tokens=tokens,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default',
                        badge=unread_count,
                        channel_id='messages',
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            badge=unread_count,
                            sound='default',
                            content_available=True,
                        )
                    )
                )
            )
            
            # Send the messages
            response = messaging.send_multicast(message)
            logger.info(f"Sent {response.success_count} notifications successfully")
            
            return {
                "success": response.success_count,
                "failure": response.failure_count
            }
            
        except Exception as e:
            logger.error(f"Failed to send batch notifications: {e}")
            return {"success": 0, "failure": len(tokens)}

# Global instance
push_service = PushNotificationService()
