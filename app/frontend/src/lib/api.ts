const API_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';

export interface User {
  id: number;
  email: string;
  username?: string;
  profile_picture?: string;
  public_key?: string;
}

export interface AuthResponse {
  token: string;
  expires_at: string;
  user: User;
}

export interface ChatRequest {
  id: number;
  from_user_id: number;
  to_user_id: number;
  verification_code: string;
  status: string;
  created_at: string;
  email: string;
  username?: string;
  profile_picture?: string;
}

export interface Chat {
  id: number;
  other_user: User;
  last_verification: string;
  next_verification: string;
  verification_pending: boolean;
  created_at: string;
}

export interface Message {
  id: number;
  chat_id: number;
  sender_id: number;
  encrypted_content: string;
  created_at: string;
  email: string;
  username?: string;
  profile_picture?: string;
  message_type?: string;
}

class ApiClient {
  private token: string | null = null;

  constructor() {
    this.token = localStorage.getItem('token');
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // Auth endpoints
  async register(email: string, password: string, username?: string, profile_picture?: string, public_key?: string): Promise<AuthResponse> {
    const response = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, username, profile_picture, public_key }),
    });
    this.setToken(response.token);
    return response;
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(response.token);
    return response;
  }

  async getMe(): Promise<User> {
    return this.request('/auth/me');
  }

  async updateProfile(username?: string, profile_picture?: string, public_key?: string): Promise<User> {
    return this.request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify({ username, profile_picture, public_key }),
    });
  }

  async logout() {
    await this.request('/auth/logout', { method: 'POST' });
    this.clearToken();
  }

  // Chat endpoints
  async searchUsers(query: string): Promise<{ users: User[] }> {
    return this.request('/chat/search-users', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }

  async sendChatRequest(to_user_id: number, verification_code: string): Promise<{ request_id: number; status: string }> {
    return this.request('/chat/request', {
      method: 'POST',
      body: JSON.stringify({ to_user_id, verification_code }),
    });
  }

  async getPendingRequests(): Promise<{ requests: ChatRequest[] }> {
    return this.request('/chat/requests');
  }

  async acceptChatRequest(request_id: number, verification_code: string): Promise<{ chat_id: number; status: string }> {
    return this.request('/chat/accept', {
      method: 'POST',
      body: JSON.stringify({ request_id, verification_code }),
    });
  }

  async getActiveChats(): Promise<{ chats: Chat[] }> {
    return this.request('/chat/active');
  }

  async getMessages(chat_id: number): Promise<{ messages: Message[] }> {
    return this.request(`/chat/messages/${chat_id}`);
  }

  async verifyChat(chat_id: number, verification_code: string): Promise<{ status: string }> {
    return this.request('/chat/verify', {
      method: 'POST',
      body: JSON.stringify({ chat_id, verification_code }),
    });
  }

  async clearChatMessages(chat_id: number): Promise<{ status: string }> {
    return this.request(`/chat/clear/${chat_id}`, {
      method: 'POST',
    });
  }

  async requestDeleteChat(chat_id: number): Promise<{ status: string; message: string }> {
    return this.request(`/chat/delete/${chat_id}`, {
      method: 'POST',
    });
  }

  // WebSocket
  createWebSocket(): WebSocket {
    if (!this.token) {
      throw new Error('No token available');
    }
    return new WebSocket(`ws://localhost:8000/chat/ws?token=${this.token}`);
  }
}

export const api = new ApiClient();
