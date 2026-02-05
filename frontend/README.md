# Todo App Frontend

A secure, production-quality frontend for the multi-user Todo web application built with Next.js.

## Features

- User authentication with Better Auth and JWT
- Task management (create, read, update, delete)
- Optimistic UI updates with error recovery
- Responsive design for all device sizes
- Clean, professional UI focused on productivity
- Session persistence across browser refreshes
- 401 error handling with automatic logout
- Network failure handling and offline detection

## Tech Stack

- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- Better Auth for authentication
- React Server Components

## Architecture

The application follows a component-based architecture with:

- **Pages**: App, login/signup, tasks
- **Components**: Authentication forms, task UI components
- **Hooks**: Authentication context provider
- **Libraries**: Centralized API client
- **Types**: TypeScript interfaces for data structures

## Setup

1. Copy the environment variables to `.env.local`:
   ```
   BETTER_AUTH_SECRET=8ApAiAkyiQZg3XVId7GKjNyYXoFUw9vz
   BETTER_AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for signing JWT tokens
- `BETTER_AUTH_URL`: Base URL for the auth service
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Security Features

- All API requests include JWT tokens automatically
- User isolation enforced (users only see their own tasks)
- Secure authentication flow
- Proper error handling without information leakage
- Automatic logout on token expiration or 401 errors
- Token sanitization to prevent header injection
- Secure API client with validation and proper headers
- Protected routes to prevent unauthorized access

## Performance Features

- Optimized API client with proper error handling
- Optimistic UI updates for responsive user experience
- Loading states and skeleton screens for perceived performance
- Efficient state management to prevent unnecessary re-renders
- Proper caching and request optimization
- Bundle optimization through Next.js

## UI/UX Design

- Clean, professional, productivity-focused interface
- Responsive design for all device sizes
- Consistent spacing, typography, and visual hierarchy
- Calm, trustworthy aesthetic without playful elements
- Accessible form controls and navigation
- Loading states (skeletons) and empty states
- Error states that don't break the layout