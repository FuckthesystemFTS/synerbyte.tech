# Firebase Push Notifications Setup

## Prerequisites

1. Create a Firebase project at https://console.firebase.google.com/
2. Add your Android and iOS apps to the Firebase project

## Android Setup

1. Download `google-services.json` from Firebase Console
2. Place it in `android/app/google-services.json`
3. The app is already configured to use it

## iOS Setup

1. Download `GoogleService-Info.plist` from Firebase Console
2. Place it in `ios/App/App/GoogleService-Info.plist`
3. The app is already configured to use it

## Backend Setup

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download the JSON file
4. Set the environment variable:
   ```
   FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
   ```

## Testing

1. Build and run the app on a physical device (notifications don't work on emulators)
2. Login to the app
3. The app will automatically register for push notifications
4. Send a test message from another account
5. You should receive a notification even when the app is closed

## Notification Format

Notifications will show:
- Title: "New Messages"
- Body: "You have X unread message(s)"
- Badge: Number of unread messages
- NO sender name or message content (privacy)

## Troubleshooting

- Make sure you're testing on a physical device
- Check that notifications are enabled in device settings
- Verify Firebase credentials are correctly configured
- Check backend logs for FCM errors
