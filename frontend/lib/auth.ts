// Better Auth Integration
// This file defines constants and utilities for Better Auth integration

// JWT configuration that should match the backend setup
export const JWT_CONFIG = {
  // Token expiry (should match backend)
  TOKEN_EXPIRY_MS: 60 * 60 * 1000, // 1 hour in milliseconds

  // Claims validation
  ISSUER: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  ALGORITHM: 'HS256',
} as const;

// Better Auth endpoints
export const AUTH_ENDPOINTS = {
  LOGIN: '/api/auth/login',
  SIGNUP: '/api/auth/signup',
  LOGOUT: '/api/auth/logout',
  ME: '/api/auth/me',
} as const;

// Token validation helpers
export const validateToken = (token: string): boolean => {
  try {
    // In a real implementation, we would decode and validate the JWT
    // For now, we just check if it's a non-empty string
    return typeof token === 'string' && token.length > 0;
  } catch (error) {
    console.error('Token validation failed:', error);
    return false;
  }
};

// Token expiration check
export const isTokenExpired = (expiresAt: string): boolean => {
  try {
    const expiryDate = new Date(expiresAt);
    return expiryDate < new Date();
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true; // Assume expired if there's an error
  }
};

// Export default configuration
export default {
  JWT_CONFIG,
  AUTH_ENDPOINTS,
  validateToken,
  isTokenExpired,
};