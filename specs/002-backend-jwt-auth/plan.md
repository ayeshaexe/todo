# Todo App Backend API Implementation Plan

## Technical Context

**Feature**: Backend API with JWT authentication for Todo application
**Architecture**: FastAPI backend with SQLModel ORM, Neon PostgreSQL, Better Auth JWT integration
**Integration**: Must be fully compatible with existing Next.js frontend
**Environment**: NEON_DB_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL environment variables

**Key Requirements**:
- JWT token verification using BETTER_AUTH_SECRET
- User isolation - users can only access their own tasks
- REST API under /api/ endpoints
- All endpoints require authentication except public routes
- Proper error handling with consistent response format

## Constitution Check

**Authentication & Security**: All API endpoints will require valid JWT token verification using BETTER_AUTH_SECRET. User identity will be derived from JWT payload, never from client input. Every database query will be filtered by authenticated user_id.

**API Design**: All routes will be under /api/ with proper REST conventions. Requests without valid JWT will return 401 Unauthorized. Unauthorized resource access will return 403 Forbidden. Responses will be JSON with proper HTTP status codes.

**Database & Persistence**: SQLModel will be used for all database operations with Neon PostgreSQL as the persistence layer. Task ownership will be enforced at the database query level.

**Spec Compliance**: Implementation will follow the exact specifications defined in the feature spec without adding unrequested functionality.

**Code Quality**: Production-ready code with proper error handling and security considerations.

**Post-Design Evaluation**: All constitutional requirements have been incorporated into the data model and API contracts. JWT-based authentication is central to the design, user isolation is enforced at the database query level, and API design follows REST conventions with proper error handling.

## Gates

✅ **Authentication Gate**: JWT token verification will be implemented using BETTER_AUTH_SECRET
✅ **Security Gate**: User isolation will be enforced at both API and database levels
✅ **Integration Gate**: API will be compatible with existing Next.js frontend
✅ **Quality Gate**: Proper error handling and logging without leaking sensitive information

## Phase 0: Research

### 0.1 JWT Token Verification with Better Auth
- Researched how Better Auth structures JWT tokens
- Confirmed payload structure contains user_id and email
- Determined HS256 algorithm for verification using BETTER_AUTH_SECRET

### 0.2 FastAPI Security Implementation
- Researched best practices for JWT middleware in FastAPI
- Confirmed dependency injection approach for current user
- Verified proper exception handling patterns for authentication failures

### 0.3 SQLModel User Isolation Patterns
- Researched query filtering patterns for user-specific data
- Confirmed relationship definitions between users and tasks
- Identified indexing strategies for performance

## Phase 1: Data Model & API Contracts

### 1.1 Data Model Design
**Task Entity**:
- id: integer (primary key)
- user_id: string (indexed, foreign key to user)
- title: string (1-200 chars, required)
- description: text (optional, max 1000 chars)
- completed: boolean (default false)
- created_at: datetime
- updated_at: datetime

**User Entity** (externally managed by Better Auth):
- user_id: string (extracted from JWT)
- email: string (extracted from JWT)

### 1.2 API Contract Definition

#### Authentication Endpoints (to be implemented separately)
- POST /api/auth/login (handled by Better Auth)
- POST /api/auth/register (handled by Better Auth)
- POST /api/auth/logout (handled by Better Auth)

#### Task Management Endpoints
- GET /api/tasks
  - Headers: Authorization: Bearer <token>
  - Query params: status (all|pending|completed)
  - Response: 200 with array of tasks for authenticated user

- POST /api/tasks
  - Headers: Authorization: Bearer <token>
  - Body: {title: string, description?: string}
  - Response: 201 with created task object

- GET /api/tasks/{id}
  - Headers: Authorization: Bearer <token>
  - Response: 200 with task object or 404/403

- PUT /api/tasks/{id}
  - Headers: Authorization: Bearer <token>
  - Body: {title: string, description?: string}
  - Response: 200 with updated task object

- DELETE /api/tasks/{id}
  - Headers: Authorization: Bearer <token>
  - Response: 204 or appropriate status

- PATCH /api/tasks/{id}/complete
  - Headers: Authorization: Bearer <token>
  - Body: {completed: boolean}
  - Response: 200 with updated task object

## Phase 2: Implementation Plan

### 2.1 Project Setup
- Initialize FastAPI project
- Configure environment variables (NEON_DB_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL)
- Set up SQLModel with Neon PostgreSQL connection
- Configure CORS for frontend integration

### 2.2 Authentication Layer
- Implement JWT verification utility
- Create authentication dependency
- Set up user extraction from token
- Create authentication middleware

### 2.3 Database Models
- Define Task model with SQLModel
- Set up database engine and session management
- Create database initialization

### 2.4 Task Service Layer
- Implement task CRUD operations with user isolation
- Create service functions for all task operations
- Ensure all queries filter by user_id from JWT

### 2.5 API Routes
- Create task router with all required endpoints
- Apply authentication dependency to all routes
- Implement request/response validation
- Handle errors appropriately

### 2.6 Testing & Validation
- Unit tests for service layer
- Integration tests for API endpoints
- Verify user isolation works correctly
- Test error scenarios

## Phase 3: Implementation Steps

### Week 1: Infrastructure
1. Set up FastAPI project with dependencies
2. Configure database connection with SQLModel
3. Implement JWT verification utilities
4. Set up authentication dependency

### Week 2: Core Logic
1. Create Task model and database operations
2. Implement task service layer with user isolation
3. Add request/response validation
4. Create API routes for task management

### Week 3: Integration & Testing
1. Integrate all components
2. Implement comprehensive error handling
3. Add logging and monitoring
4. Conduct security and integration testing

## Success Criteria Validation

- ✅ All API endpoints properly authenticate and authorize requests
- ✅ Authenticated users can only access their own tasks
- ✅ Frontend application can successfully integrate with all API endpoints
- ✅ All API operations complete with response times under 2 seconds
- ✅ Error handling provides meaningful responses without exposing system details
- ✅ JWT token validation works with Better Auth issued tokens
- ✅ Database persists task data correctly with proper user associations