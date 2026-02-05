# Todo App Backend API Specification

## Feature Overview

**Purpose**: Implement a secure, stateless FastAPI backend for the Todo application that integrates with JWT authentication and manages task data in Neon PostgreSQL database.

**Scope**: Backend API development only. Frontend integration support with existing React application.

## User Scenarios & Testing

### Primary User Flows

1. **Authenticated User Task Management**
   - As an authenticated user, I can create new tasks that are associated with my user account
   - As an authenticated user, I can view only my own tasks
   - As an authenticated user, I can update my own tasks
   - As an authenticated user, I can delete my own tasks
   - As an authenticated user, I can toggle the completion status of my tasks

2. **Authentication Enforcement**
   - As a system, I must reject API requests without valid JWT tokens
   - As a system, I must prevent users from accessing tasks belonging to other users
   - As a system, I must ensure all operations are tied to the authenticated user's identity

### Testing Scenarios

- Unauthenticated users receive 401 errors when accessing protected endpoints
- Authenticated users can only access their own tasks
- Malicious attempts to access other users' data return 403 forbidden errors
- Successful task operations complete with appropriate status codes
- JWT tokens are properly validated against Better Auth secret

## Functional Requirements

### Authentication & Security
- **REQ-AUTH-001**: All API endpoints must require a valid JWT token in the Authorization header (Bearer <token>)
- **REQ-AUTH-002**: JWT tokens must be verified using the BETTER_AUTH_SECRET environment variable
- **REQ-AUTH-003**: User identity must be extracted from JWT payload (user_id, email)
- **REQ-AUTH-004**: User identity must be automatically applied to all database operations
- **REQ-AUTH-005**: Requests without valid JWT must return 401 Unauthorized

### Task Management API
- **REQ-TASK-001**: GET /api/tasks must return all tasks for the authenticated user
- **REQ-TASK-002**: GET /api/tasks must support optional query param 'status' (all|pending|completed)
- **REQ-TASK-003**: POST /api/tasks must create a new task associated with the authenticated user
- **REQ-TASK-004**: POST /api/tasks requires 'title' (string) and optional 'description' (string)
- **REQ-TASK-005**: GET /api/tasks/{id} must return task details if owned by the authenticated user
- **REQ-TASK-006**: PUT /api/tasks/{id} must update task title and description if owned by the authenticated user
- **REQ-TASK-007**: DELETE /api/tasks/{id} must delete task if owned by the authenticated user
- **REQ-TASK-008**: PATCH /api/tasks/{id}/complete must toggle completion status if owned by the authenticated user

### Data Isolation
- **REQ-DATA-001**: Every database query must include user_id filter to enforce user isolation
- **REQ-DATA-002**: Task ownership must be verified before any update/delete operations
- **REQ-DATA-003**: Cross-user data access must be prevented at both API and database levels
- **REQ-DATA-004**: Task listing endpoints must only return tasks belonging to the authenticated user

### Response Format
- **REQ-RESP-001**: All successful responses must return JSON format
- **REQ-RESP-002**: Error responses must follow consistent format with appropriate HTTP status codes
- **REQ-RESP-003**: Task creation must return the complete task object with assigned ID
- **REQ-RESP-004**: Task updates must return the updated task object

## Non-functional Requirements

### Performance
- **REQ-PERF-001**: API endpoints must respond within 2 seconds under normal load
- **REQ-PERF-002**: Database queries must utilize indexes for efficient lookups

### Security
- **REQ-SEC-001**: No sensitive data should be exposed in error messages
- **REQ-SEC-002**: JWT tokens must be statelessly validated without database lookups
- **REQ-SEC-003**: User identity must never be accepted from request body or URL parameters

### Reliability
- **REQ-REL-001**: Database connections must be properly managed with dependency injection
- **REQ-REL-002**: API must handle database connection failures gracefully

## Success Criteria

- **SUCCESS-001**: 100% of API endpoints properly authenticate and authorize requests
- **SUCCESS-002**: Authenticated users can only access their own tasks (data isolation enforced)
- **SUCCESS-003**: Frontend application can successfully integrate with all API endpoints
- **SUCCESS-004**: All API operations complete with response times under 2 seconds
- **SUCCESS-005**: Error handling provides meaningful responses without exposing system details
- **SUCCESS-006**: JWT token validation works with Better Auth issued tokens
- **SUCCESS-007**: Database persists task data correctly with proper user associations

## Key Entities

### Task Entity
- **Identity**: Unique numeric ID, belongs to a specific user
- **Attributes**: Title (required, 1-200 chars), Description (optional, up to 1000 chars), Completed (boolean), Timestamps
- **Relationships**: Owned by single authenticated user

### User Identity
- **Identity**: User ID extracted from JWT token
- **Attributes**: User ID (string), Email (optional)
- **Relationships**: Owns multiple tasks

## Assumptions

- Better Auth provides JWT tokens with user_id and email in the payload
- Frontend will send JWT tokens in Authorization header as "Bearer <token>"
- Neon PostgreSQL connection is stable and properly configured
- Frontend application structure remains unchanged and compatible with new API endpoints
- BETTER_AUTH_SECRET environment variable will be properly configured in deployment

## Dependencies

- Better Auth service for JWT token generation
- Neon PostgreSQL database service
- Environment variables (NEON_DB_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL)
- Frontend application will consume the API as specified