import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, User } from '../lib/api';
import { crypto } from '../lib/crypto/encryption';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, username?: string, profilePicture?: string) => Promise<void>;
  logout: () => void;
  updateProfile: (username?: string, profilePicture?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setLoading(true);
      api.getMe()
        .then(user => {
          setUser(user);
          // Initialize crypto
          if (!crypto.loadKeys()) {
            crypto.generateKeyPair().then(keys => {
              crypto.saveKeys();
              // Update user profile with public key
              api.updateProfile(undefined, undefined, keys.publicKey);
            });
          }
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }

    // Session keep-alive: ping server every 5 minutes to keep session active
    const keepAliveInterval = setInterval(() => {
      if (localStorage.getItem('token')) {
        api.getMe().catch(() => {
          // Session expired, logout
          localStorage.removeItem('token');
          setUser(null);
          window.location.href = '/login';
        });
      }
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(keepAliveInterval);
  }, []);

  const login = async (email: string, password: string) => {
    const response = await api.login(email, password);
    setUser(response.user);
    
    // Initialize crypto
    if (!crypto.loadKeys()) {
      const keys = await crypto.generateKeyPair();
      crypto.saveKeys();
      await api.updateProfile(undefined, undefined, keys.publicKey);
    }
  };

  const register = async (email: string, password: string, username?: string, profilePicture?: string) => {
    // Generate crypto keys
    await crypto.init();
    const keys = await crypto.generateKeyPair();
    
    const response = await api.register(email, password, username, profilePicture, keys.publicKey);
    setUser(response.user);
    crypto.saveKeys();
  };

  const logout = () => {
    api.logout();
    crypto.clearKeys();
    setUser(null);
  };

  const updateProfile = async (username?: string, profilePicture?: string) => {
    const updatedUser = await api.updateProfile(username, profilePicture);
    setUser(updatedUser);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
