import { ApiResponse } from '../types';
import { isTokenExpired } from './auth';

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '';
  }

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;

    // Check if online before making the request
    if (!navigator.onLine) {
      return {
        status: 0,
        error: 'No internet connection',
        message: 'Please check your internet connection and try again.',
      };
    }

    // Sanitize the token before adding to headers to prevent header injection
    let sanitizedToken = null;
    if (this.token) {
      // Basic sanitization: remove newlines and other control characters
      sanitizedToken = this.token.replace(/[\r\n\t\v\f\0]/g, '');
    }

    // Build safe headers with security in mind
    // Start with safe defaults, add user options, then enforce security headers
    const safeHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers,  // User options added here
    };

    // Enforce security headers after user options
    safeHeaders['Content-Type'] = 'application/json';
    safeHeaders['Accept'] = 'application/json';

    // Add authorization header if available
    if (sanitizedToken) {
      safeHeaders['Authorization'] = `Bearer ${sanitizedToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers: safeHeaders,
      });

      // Verify the response is from our expected server to prevent certain attacks
      const contentType = response.headers.get('content-type');
      if (contentType && !contentType.includes('application/json')) {
        return {
          status: response.status,
          error: 'Unexpected response format',
          message: 'The server returned an unexpected response format.',
        };
      }

      // Handle cases where response is not JSON (like when server is down)
      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        // If response is not JSON, create a generic error response
        return {
          status: response.status,
          error: `Request failed with status ${response.status}`,
          message: 'The server returned an unexpected response format.',
        };
      }

      if (!response.ok) {
        // Handle 401 Unauthorized - likely means token expired
        if (response.status === 401) {
          // Clear the token as it's no longer valid
          this.token = null;
          // Optionally trigger a logout or token refresh mechanism
        }

        return {
          status: response.status,
          error: data.message || 'Request failed',
          message: data.message,
        };
      }

      return {
        data,
        status: response.status,
        message: data.message,
      };
    } catch (error: any) {
      // Handle network errors specifically
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return {
          status: 0,
          error: 'Network request failed',
          message: 'Unable to connect to the server. Please check your connection and try again.',
        };
      }

      return {
        status: 0,
        error: error.message || 'Network error',
        message: 'Network error occurred',
      };
    }
  }

  // Authentication methods
  async login(email: string, password: string): Promise<ApiResponse> {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signup(email: string, password: string, name?: string): Promise<ApiResponse> {
    return this.request('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async logout(): Promise<ApiResponse> {
    // Clear the token locally first
    this.token = null;

    // Then make the API call to invalidate the server-side session
    const response = await this.request('/api/auth/logout', {
      method: 'POST',
    });

    return response;
  }

  // Task methods
  async getTasks(): Promise<ApiResponse> {
    return this.request('/api/tasks');
  }

  async createTask(title: string, description?: string, completed: boolean = false): Promise<ApiResponse> {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description, completed }),
    });
  }

  async updateTask(taskId: string, title: string, description?: string, completed?: boolean): Promise<ApiResponse> {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify({ title, description, completed }),
    });
  }

  async deleteTask(taskId: string): Promise<ApiResponse> {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();