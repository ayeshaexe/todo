export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Session {
  jwtToken: string;
  user: User;
  expiresAt: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  status: number;
  message?: string;
  error?: string | Record<string, unknown>;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
  name?: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  completed: boolean;
}