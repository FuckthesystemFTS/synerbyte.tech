# Push Notifications Implementation

## Overview

The app now supports push notifications that work even when the app is closed. Notifications show only the count of unread messages without revealing sender names or message content for privacy.

## Features

✅ **Privacy-First**: Notifications show only message count, no content
✅ **Works when app is closed**: Uses Firebase Cloud Messaging (FCM)
✅ **Cross-platform**: Works on both Android and iOS
✅ **Automatic registration**: Registers on login, unregisters on logout
✅ **Badge count**: Shows unread message count on app icon

## Architecture

### Backend
- **Firebase Admin SDK**: Sends push notifications via FCM
- **Database**: Stores FCM tokens for each user/device
- **API Endpoints**:
  - `POST /api/notifications/register-token`: Register device token
  - `DELETE /api/notifications/unregister-token`: Unregister token
  - `GET /api/notifications/unread-count`: Get unread message count

### Frontend
- **Push Notification Service**: Handles FCM token registration
- **Capacitor Push Notifications**: Native plugin for notifications
- **Auto-initialization**: Starts on login, stops on logout

## Setup Required

### 1. Firebase Project
Create a Firebase project and add your apps:
- Android app with package name
- iOS app with bundle ID

### 2. Download Configuration Files
- **Android**: `google-services.json` → `android/app/`
- **iOS**: `GoogleService-Info.plist` → `ios/App/App/`

### 3. Backend Configuration
Set environment variable with Firebase credentials:
```bash
export FIREBASE_CREDENTIALS_PATH=/path/to/firebase-admin-credentials.json
```

### 4. Build and Deploy
```bash
# Frontend
cd app/frontend
npm run build
npx cap sync

# Backend
cd app/backend
pip install -r requirements.txt
```

## Notification Flow

1. **User logs in** → App requests notification permission
2. **Permission granted** → FCM token generated
3. **Token registered** → Saved to backend database
4. **Message sent** → Backend sends push notification to recipient
5. **Notification received** → Shows "You have X unread messages"
6. **User taps notification** → Opens app to chat

## Privacy & Security

- ❌ **No message content** in notifications
- ❌ **No sender information** in notifications
- ✅ **Only unread count** displayed
- ✅ **End-to-end encryption** still active
- ✅ **Tokens stored securely** in database

## Testing

1. Install app on **physical device** (not emulator)
2. Login with account A
3. Send message from account B
4. **Close app completely**
5. Notification should appear on device

## Troubleshooting

### No notifications received
- Check device notification settings
- Verify Firebase configuration files are present
- Check backend logs for FCM errors
- Ensure testing on physical device

### Token registration fails
- Check network connection
- Verify backend is running
- Check authentication token is valid

### Notifications work but don't open app
- Check deep link configuration
- Verify app is properly installed

## Future Enhancements

- [ ] Notification channels for Android
- [ ] Custom notification sounds
- [ ] Notification grouping
- [ ] Rich notifications with actions
- [ ] Silent notifications for sync

## Files Modified/Created

### Backend
- `app/services/push_notifications.py` - FCM service
- `app/routers/notifications.py` - API endpoints
- `app/database.py` - FCM token model
- `requirements.txt` - Added firebase-admin

### Frontend
- `src/services/pushNotifications.ts` - Push notification service
- `src/contexts/AuthContext.tsx` - Initialize on login
- `package.json` - Added @capacitor/push-notifications

### Configuration
- `FIREBASE_SETUP.md` - Setup instructions
- `NOTIFICATIONS_README.md` - This file
