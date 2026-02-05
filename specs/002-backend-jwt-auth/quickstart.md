# Quickstart Guide for Todo App Backend

## Prerequisites
- Python 3.10+
- PostgreSQL database (Neon)
- Better Auth configured for frontend

## Environment Setup
Create a `.env` file with the following variables:
```
NEON_DB_URL=postgresql://username:password@host:port/database
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

## Installation
1. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] python-multipart
```

2. Set up the database:
```bash
# This will be handled by SQLModel migrations
```

## Running the Application
1. Start the development server:
```bash
uvicorn main:app --reload --port 8000
```

2. The API will be available at `http://localhost:8000/api`

## API Usage
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Available Endpoints
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Testing the API
Use a tool like curl or Postman to test the endpoints:
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json"
```