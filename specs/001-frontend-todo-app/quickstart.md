# Quickstart Guide: Frontend Todo Application

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Backend service running at http://localhost:8000
- Better Auth configured with JWT support

## Environment Setup
1. Copy the following to a `.env.local` file in the frontend directory:
```
BETTER_AUTH_SECRET=8ApAiAkyiQZg3XVId7GKjNyYXoFUw9vz
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Installation
1. Navigate to the frontend directory
2. Install dependencies: `npm install` or `yarn install`
3. Start the development server: `npm run dev` or `yarn dev`

## Running the Application
1. Ensure the backend API is running at http://localhost:8000
2. Start the frontend: `npm run dev`
3. Open http://localhost:3000 in your browser
4. Access the following routes:
   - `/signup` - Create a new account
   - `/login` - Log into existing account
   - `/tasks` - View and manage your tasks (authenticated users only)

## Key Features
- Secure authentication with Better Auth and JWT
- Protected routes that redirect unauthenticated users
- Task management: create, read, update, delete
- Optimistic UI updates with error recovery
- Responsive design for all device sizes
- Proper loading and error states

## Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter