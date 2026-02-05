'use client';

import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User, Session, ApiResponse } from '../types';
import { isTokenExpired } from '../lib/auth';
import { apiClient } from '../lib/api-client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<boolean>;
  signup: (userData: { email: string; password: string; name?: string }) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Check for stored session on mount
  useEffect(() => {
    const storedSession = localStorage.getItem('session');
    if (storedSession) {
      try {
        const session = JSON.parse(storedSession);

        if (!isTokenExpired(session.expiresAt)) {
          // Map stored user data to frontend User interface (handle both old and new formats)
          const storedUser = session.user;
          const mappedUser = {
            id: storedUser.id,
            email: storedUser.email,
            name: storedUser.name,
            createdAt: storedUser.createdAt || storedUser.created_at || new Date().toISOString(), // Handle both formats
            updatedAt: storedUser.updatedAt || storedUser.updated_at || storedUser.last_login || new Date().toISOString()
          };

          setUser(mappedUser);
          setToken(session.jwtToken);
          apiClient.setToken(session.jwtToken); // Set token in API client
        } else {
          // Token expired, remove it
          localStorage.removeItem('session');
        }
      } catch (error) {
        console.error('Failed to parse stored session', error);
        localStorage.removeItem('session');
      }
    }
    setLoading(false);
  }, []);

  const login = async (credentials: { email: string; password: string }): Promise<boolean> => {
    try {
      const response: ApiResponse = await apiClient.login(credentials.email, credentials.password);

      if (response.data && response.data.success) {
        const { user: userData, jwt_token: jwtToken } = response.data.data;

        // Map backend user data to frontend User interface
        const mappedUser = {
          id: userData.id,
          email: userData.email,
          name: userData.name,
          createdAt: userData.created_at || userData.createdAt, // Handle both formats
          updatedAt: userData.updated_at || userData.updatedAt || userData.last_login || new Date().toISOString()
        };

        // Calculate expiration (assuming token is valid for 1 hour)
        const expiresAt = new Date(Date.now() + 60 * 60 * 1000).toISOString();

        const session: Session = {
          jwtToken,
          user: mappedUser,
          expiresAt,
        };

        localStorage.setItem('session', JSON.stringify(session));
        setUser(mappedUser);
        setToken(jwtToken);
        apiClient.setToken(jwtToken); // Set token in API client
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const signup = async (userData: { email: string; password: string; name?: string }): Promise<boolean> => {
    try {
      const response: ApiResponse = await apiClient.signup(userData.email, userData.password, userData.name);

      if (response.data && response.data.success) {
        const { user: backendUser, jwt_token: jwtToken } = response.data.data;

        // Map backend user data to frontend User interface
        const mappedUser = {
          id: backendUser.id,
          email: backendUser.email,
          name: backendUser.name,
          createdAt: backendUser.created_at || backendUser.createdAt, // Handle both formats
          updatedAt: backendUser.updated_at || backendUser.updatedAt || new Date().toISOString()
        };

        // Calculate expiration (assuming token is valid for 1 hour)
        const expiresAt = new Date(Date.now() + 60 * 60 * 1000).toISOString();

        const session: Session = {
          jwtToken,
          user: mappedUser,
          expiresAt,
        };

        localStorage.setItem('session', JSON.stringify(session));
        setUser(mappedUser);
        setToken(jwtToken);
        apiClient.setToken(jwtToken); // Set token in API client
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Signup error:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('session');
    setUser(null);
    setToken(null);
    apiClient.setToken(null); // Clear token in API client
  };

  const isAuthenticated = (): boolean => {
    return !!user && !!token;
  };

  // Create the value object separately to avoid JSX parsing issues
  const authValue = {
    user: user,
    token: token,
    loading: loading,
    login: login,
    signup: signup,
    logout: logout,
    isAuthenticated: isAuthenticated
  };

  return React.createElement(
    AuthContext.Provider,
    { value: authValue },
    children
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};