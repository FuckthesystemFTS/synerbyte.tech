import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { api, Chat, Message, ChatRequest } from '../lib/api';
import { useAuth } from './AuthContext';

interface ChatContextType {
  chats: Chat[];
  activeChat: Chat | null;
  messages: Message[];
  requests: ChatRequest[];
  setActiveChat: (chat: Chat | null) => void;
  sendMessage: (message: string, messageType?: string) => void;
  refreshChats: () => Promise<void>;
  refreshRequests: () => Promise<void>;
  sendChatRequest: (userId: number, code: string) => Promise<void>;
  acceptRequest: (requestId: number, code: string) => Promise<void>;
  verifyChat: (chatId: number, code: string) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [chats, setChats] = useState<Chat[]>([]);
  const [requests, setRequests] = useState<any[]>([]);
  const [activeChat, setActiveChat] = useState<Chat | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const activeChatRef = useRef<any>(null);
  const reconnectTimeoutRef = useRef<any>(null);
  const isConnectingRef = useRef<boolean>(false);

  useEffect(() => {
    activeChatRef.current = activeChat;
  }, [activeChat]);

  useEffect(() => {
    if (user) {
      refreshChats();
      refreshRequests();
      connectWebSocket();
    } else {
      disconnectWebSocket();
    }

    return () => {
      disconnectWebSocket();
    };
  }, [user]);

  useEffect(() => {
    if (activeChat) {
      loadMessages(activeChat.id);
    } else {
      setMessages([]);
    }
  }, [activeChat]);

  const connectWebSocket = () => {
    // Prevent multiple simultaneous connection attempts
    if (isConnectingRef.current || (wsRef.current && wsRef.current.readyState === WebSocket.OPEN)) {
      console.log('⚠️ WebSocket already connecting or connected, skipping');
      return;
    }

    try {
      isConnectingRef.current = true;
      console.log('🔌 Attempting WebSocket connection...');
      
      const ws = api.createWebSocket();
      
      ws.onopen = () => {
        console.log('✅ WebSocket connected successfully');
        isConnectingRef.current = false;
        // Clear any pending reconnect attempts
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };

      ws.onmessage = (event) => {
        console.log('📩 Raw WebSocket message:', event.data);
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        isConnectingRef.current = false;
      };

      ws.onclose = (event) => {
        console.log('🔌 WebSocket disconnected, code:', event.code, 'reason:', event.reason);
        isConnectingRef.current = false;
        wsRef.current = null;
        
        // Reconnect after 2 seconds if user is still logged in
        if (user) {
          console.log('🔄 Scheduling reconnect in 2 seconds...');
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log('🔄 Attempting to reconnect...');
            connectWebSocket();
          }, 2000);
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('❌ Failed to connect WebSocket:', error);
      isConnectingRef.current = false;
      
      // Retry connection after 3 seconds on error
      if (user) {
        reconnectTimeoutRef.current = setTimeout(() => {
          connectWebSocket();
        }, 3000);
      }
    }
  };

  const disconnectWebSocket = () => {
    console.log('🔌 Disconnecting WebSocket...');
    
    // Clear any pending reconnect attempts
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    // Close WebSocket connection
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    isConnectingRef.current = false;
  };

  const handleWebSocketMessage = (data: any) => {
    console.log('🔔 WebSocket message received:', data);
    switch (data.type) {
      case 'message':
      case 'new_message':
        console.log('📨 New message event:', data.data);
        console.log('📍 Active chat from ref:', activeChatRef.current);
        console.log('📍 Active chat from state:', activeChat);
        
        // Add message directly to state for instant display
        const currentActiveChat = activeChatRef.current;
        if (currentActiveChat && data.data.chat_id === currentActiveChat.id) {
          console.log('✅ Adding message directly to state');
          const newMessage = {
            id: data.data.id,
            chat_id: data.data.chat_id,
            sender_id: data.data.sender_id,
            encrypted_content: data.data.content,
            message_type: data.data.message_type || 'text',
            created_at: new Date().toISOString(),
            username: data.data.sender_id === user?.id ? (user?.username || '') : currentActiveChat.other_user.username,
            email: data.data.sender_id === user?.id ? (user?.email || '') : currentActiveChat.other_user.email
          };
          
          // Add to messages array if not already present
          setMessages(prev => {
            const exists = prev.some(msg => msg.id === newMessage.id);
            if (exists) {
              console.log('⚠️ Message already in state, skipping');
              return prev;
            }
            console.log('✅ Message added to state!');
            return [...prev, newMessage];
          });
        } else {
          console.log('⚠️ Message not for active chat or no active chat');
        }
        
        // Refresh chats to update last message
        refreshChats();
        break;

      case 'chat_request':
        // Refresh requests
        refreshRequests();
        break;

      case 'chat_accepted':
        // Refresh chats
        refreshChats();
        break;

      case 'verification_required':
        // Show verification prompt
        alert(`Verification required for chat ${data.data.chat_id}! You have 5 minutes.`);
        refreshChats();
        break;

      case 'chat_verified':
        // Refresh chat status
        refreshChats();
        break;

      case 'chat_destroyed':
        // Remove chat
        alert(`Chat ${data.data.chat_id} was destroyed: ${data.data.reason}`);
        if (activeChat && activeChat.id === data.data.chat_id) {
          setActiveChat(null);
        }
        refreshChats();
        break;

      case 'chat_cleared':
        // Clear messages
        if (activeChat && activeChat.id === data.data.chat_id) {
          setMessages([]);
        }
        break;

      case 'chat_deleted':
        // Chat permanently deleted
        alert('Chat has been deleted by mutual consent');
        if (activeChat && activeChat.id === data.data.chat_id) {
          setActiveChat(null);
        }
        refreshChats();
        break;

      case 'delete_requested':
      case 'deletion_request':
        // Other user wants to delete chat
        const username = data.data.requester_username || 'The other user';
        alert(`${username} wants to delete this chat. If you also want to delete it, click "Delete Chat"`);
        break;
    }
  };

  const refreshChats = async () => {
    try {
      const response = await api.getActiveChats();
      setChats(response.chats);
    } catch (error) {
      console.error('Failed to refresh chats:', error);
    }
  };

  const refreshRequests = async () => {
    try {
      const response = await api.getPendingRequests();
      setRequests(response.requests);
    } catch (error) {
      console.error('Failed to refresh requests:', error);
    }
  };

  const loadMessages = async (chatId: number) => {
    try {
      const response = await api.getMessages(chatId);
      setMessages(response.messages);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const sendMessage = async (message: string, messageType: string = 'text') => {
    if (!activeChat) return;

    try {
      await api.sendMessage(activeChat.id, message, messageType);
      // Message will be received via WebSocket
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  };

  const sendChatRequest = async (userId: number, code: string) => {
    await api.sendChatRequest(userId, code);
    // Request sent, no need to refresh here as WebSocket will notify
  };

  const acceptRequest = async (requestId: number, code: string) => {
    await api.acceptChatRequest(requestId, code);
    await refreshRequests();
    await refreshChats();
  };

  const verifyChat = async (chatId: number, code: string) => {
    await api.verifyChat(chatId, code);
    await refreshChats();
  };

  return (
    <ChatContext.Provider value={{
      chats,
      activeChat,
      messages,
      requests,
      setActiveChat,
      sendMessage,
      refreshChats,
      refreshRequests,
      sendChatRequest,
      acceptRequest,
      verifyChat,
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
};
