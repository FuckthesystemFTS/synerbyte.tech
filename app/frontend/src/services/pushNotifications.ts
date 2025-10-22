/**
 * Push Notifications Service
 * Handles FCM token registration and notification handling
 */
import { PushNotifications, Token, ActionPerformed, PushNotificationSchema } from '@capacitor/push-notifications';
import { Capacitor } from '@capacitor/core';

class PushNotificationService {
  private initialized = false;
  private currentToken: string | null = null;

  /**
   * Initialize push notifications
   */
  async initialize(): Promise<void> {
    // Only initialize on native platforms
    if (!Capacitor.isNativePlatform()) {
      console.log('Push notifications not available on web');
      return;
    }

    if (this.initialized) {
      return;
    }

    try {
      // Request permission
      let permStatus = await PushNotifications.checkPermissions();

      if (permStatus.receive === 'prompt') {
        permStatus = await PushNotifications.requestPermissions();
      }

      if (permStatus.receive !== 'granted') {
        console.warn('Push notification permission not granted');
        return;
      }

      // Register with FCM
      await PushNotifications.register();

      // Listen for registration success
      await PushNotifications.addListener('registration', async (token: Token) => {
        console.log('Push registration success, token:', token.value);
        this.currentToken = token.value;
        await this.registerTokenWithBackend(token.value);
      });

      // Listen for registration errors
      await PushNotifications.addListener('registrationError', (error: any) => {
        console.error('Error on registration:', error);
      });

      // Listen for push notifications received
      await PushNotifications.addListener(
        'pushNotificationReceived',
        (notification: PushNotificationSchema) => {
          console.log('Push notification received:', notification);
          // Notification is automatically displayed by the system
        }
      );

      // Listen for notification actions (when user taps notification)
      await PushNotifications.addListener(
        'pushNotificationActionPerformed',
        (notification: ActionPerformed) => {
          console.log('Push notification action performed:', notification);
          // Navigate to chat or show unread messages
          this.handleNotificationTap(notification);
        }
      );

      this.initialized = true;
      console.log('Push notifications initialized');
    } catch (error) {
      console.error('Failed to initialize push notifications:', error);
    }
  }

  /**
   * Register FCM token with backend
   */
  private async registerTokenWithBackend(token: string): Promise<void> {
    try {
      const deviceType = Capacitor.getPlatform(); // 'ios' or 'android'
      const authToken = localStorage.getItem('token');
      
      const response = await fetch('/api/notifications/register-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
          token,
          device_type: deviceType
        })
      });

      if (response.ok) {
        console.log('Token registered with backend');
      } else {
        console.error('Failed to register token:', response.statusText);
      }
    } catch (error) {
      console.error('Failed to register token with backend:', error);
    }
  }

  /**
   * Unregister FCM token
   */
  async unregister(): Promise<void> {
    if (!this.currentToken) {
      return;
    }

    try {
      const authToken = localStorage.getItem('token');
      
      await fetch('/api/notifications/unregister-token', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({ token: this.currentToken })
      });

      await PushNotifications.removeAllListeners();
      this.initialized = false;
      this.currentToken = null;

      console.log('Push notifications unregistered');
    } catch (error) {
      console.error('Failed to unregister push notifications:', error);
    }
  }

  /**
   * Handle notification tap
   */
  private handleNotificationTap(notification: ActionPerformed): void {
    // Navigate to chat page
    const chatId = notification.notification.data?.chat_id;
    
    if (chatId) {
      // Navigate to specific chat
      window.location.href = `/chat?id=${chatId}`;
    } else {
      // Navigate to chat list
      window.location.href = '/chat';
    }
  }

  /**
   * Get current FCM token
   */
  getCurrentToken(): string | null {
    return this.currentToken;
  }

  /**
   * Check if notifications are enabled
   */
  async areNotificationsEnabled(): Promise<boolean> {
    if (!Capacitor.isNativePlatform()) {
      return false;
    }

    const permStatus = await PushNotifications.checkPermissions();
    return permStatus.receive === 'granted';
  }

  /**
   * Get unread message count
   */
  async getUnreadCount(): Promise<number> {
    try {
      const authToken = localStorage.getItem('token');
      
      const response = await fetch('/api/notifications/unread-count', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        return data.unread_count || 0;
      }
      return 0;
    } catch (error) {
      console.error('Failed to get unread count:', error);
      return 0;
    }
  }
}

// Export singleton instance
export const pushNotificationService = new PushNotificationService();
