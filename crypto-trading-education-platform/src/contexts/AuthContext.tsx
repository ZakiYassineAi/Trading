import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';
import { setTokens, clearTokens, getTokens, isTokenExpired } from '../lib/utils';
import toast from 'react-hot-toast';

interface User {
  id: string;
  username: string;
  role: string;
  email: string;
  fullName: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { username: email, password });
      const { accessToken, refreshToken, user: userData } = response.data;

      setTokens({ accesstoken: accessToken, refreshtoken: refreshToken });
      setUser(userData);

      toast.success(`Welcome ${userData.username}!`);
    } catch (error: any) {
      const message = error.response?.data?.error || 'Login failed';
      toast.error(message);
      throw error;
    }
  }, []);

  const register = async (email: string, password: string, fullName: string) => {
    // This is a placeholder implementation.
    // In a real app, this would call a /register endpoint.
    console.log(email, password, fullName);
    toast.success('Registration successful!');
  };

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
  }, []);

  useEffect(() => {
    const initAuth = async () => {
      const tokens = getTokens();
      if (tokens && isTokenExpired(tokens.accesstoken)) {
        try {
          const { data } = await api.post('/auth/refresh', { refreshtoken: tokens.refreshtoken });
          setTokens(data);
        } catch {
          logout();
        }
      } else if (tokens) {
        // You might want to fetch user data here
      }
      setLoading(false);
    };
    initAuth();
  }, [logout]);

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
