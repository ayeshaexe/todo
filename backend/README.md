# Todo App Backend API

A secure, production-ready FastAPI backend for the Todo application with JWT authentication and PostgreSQL database.

## Features

- JWT-based authentication using Better Auth
- User isolation - users can only access their own tasks
- REST API with CRUD operations for tasks
- Secure by design with proper authentication and authorization
- Built with FastAPI and SQLModel

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLModel
- **Authentication**: JWT-based with Better Auth compatibility
- **Validation**: Pydantic
- **Environment**: python-dotenv

## Environment Variables

Create a `.env` file with the following variables:

```env
NEON_DB_URL=postgresql://username:password@host:port/database
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

## Installation

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Running the Application

1. Make sure you have set up the environment variables
2. Run the application: `python server.py`
3. The API will be available at `http://localhost:8000`

Alternatively, use Uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Task Management

- `GET /api/tasks` - Get all tasks for authenticated user (supports `status` query param)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

### Authentication

All task endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── server.py               # Server startup script
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (not committed)
├── models/                 # SQLModel database models
│   └── task.py
├── services/               # Business logic layer
│   └── task_service.py
├── routes/                 # API route definitions
│   └── tasks.py
├── middlewares/            # Middleware components
│   ├── auth.py
│   └── error.py
├── utils/                  # Utility functions
│   ├── jwt.py
│   ├── response.py
│   ├── logging.py
│   └── ...
├── validators/             # Request/response validation schemas
│   └── task_schema.py
├── config/                 # Configuration settings
│   └── settings.py
└── db.py                   # Database connection and session management
```

## Health Check

The API includes a health check endpoint:
- `GET /health` - Returns service health status

## Security Features

- All endpoints require valid JWT authentication
- User isolation - users can only access their own data
- Input validation using Pydantic models
- Proper error handling without sensitive information disclosure
- CORS configured for frontend integration