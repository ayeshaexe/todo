# Todo App Backend Implementation Tasks

## Feature: Backend API with JWT authentication for Todo application

## Phase 1: Setup
Goal: Initialize project with required dependencies and configuration

- [X] T001 Create project directory structure for FastAPI backend
- [X] T002 Initialize Python project with requirements.txt containing FastAPI, SQLModel, psycopg2-binary, python-jose, python-multipart
- [X] T003 Create .env file template with NEON_DB_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [X] T004 Set up main.py with basic FastAPI app configuration
- [X] T005 Configure CORS middleware for frontend integration
- [X] T006 [P] Create settings.py for environment variable management

## Phase 2: Foundational
Goal: Establish core infrastructure for database, authentication, and security

- [X] T007 Set up SQLModel database engine and session management in db.py
- [X] T008 Create JWT utility functions for token verification in utils/jwt.py
- [X] T009 Implement authentication middleware with user extraction from JWT
- [X] T010 Create base response utility functions in utils/response.py
- [X] T011 Define Zod-style validation schemas for auth and tasks in validators/
- [X] T012 Create error middleware for consistent error handling

## Phase 3: [US1] Authenticated User Task Management - Create Tasks
Goal: Enable authenticated users to create new tasks associated with their account

- [X] T013 [US1] Define Task model with SQLModel in models/task.py
- [X] T014 [US1] Create task service functions for creation in services/task_service.py
- [X] T015 [US1] Implement POST /api/tasks endpoint with authentication
- [X] T016 [US1] Add request validation for task creation in validators/task_schema.py
- [ ] T017 [US1] Test task creation with valid JWT authentication
- [ ] T018 [US1] Verify task is associated with authenticated user_id

## Phase 4: [US2] Authenticated User Task Management - View Tasks
Goal: Enable authenticated users to view only their own tasks

- [X] T019 [US2] Extend task service with retrieval functions in services/task_service.py
- [X] T020 [US2] Implement GET /api/tasks endpoint with authentication and user filtering
- [X] T021 [US2] Add support for status query parameter (all|pending|completed)
- [ ] T022 [US2] Test task retrieval with valid JWT authentication
- [ ] T023 [US2] Verify user isolation - users can only see their own tasks
- [ ] T024 [US2] Add pagination support for task listings

## Phase 5: [US3] Authenticated User Task Management - Update Tasks
Goal: Enable authenticated users to update their own tasks

- [X] T025 [US3] Add task update functions to service layer in services/task_service.py
- [X] T026 [US3] Implement PUT /api/tasks/{id} endpoint with authentication
- [X] T027 [US3] Add request validation for task updates in validators/task_schema.py
- [ ] T028 [US3] Test task update with valid JWT authentication
- [ ] T029 [US3] Verify user isolation - users can only update their own tasks
- [X] T030 [US3] Ensure updated_at timestamp is refreshed on updates

## Phase 6: [US4] Authenticated User Task Management - Delete Tasks
Goal: Enable authenticated users to delete their own tasks

- [X] T031 [US4] Add task deletion functions to service layer in services/task_service.py
- [X] T032 [US4] Implement DELETE /api/tasks/{id} endpoint with authentication
- [ ] T033 [US4] Test task deletion with valid JWT authentication
- [ ] T034 [US4] Verify user isolation - users can only delete their own tasks
- [X] T035 [US4] Ensure proper response codes for deletion operations

## Phase 7: [US5] Authenticated User Task Management - Toggle Completion
Goal: Enable authenticated users to toggle completion status of their tasks

- [X] T036 [US5] Add task completion toggle function to service layer in services/task_service.py
- [X] T037 [US5] Implement PATCH /api/tasks/{id}/complete endpoint with authentication
- [X] T038 [US5] Add request validation for completion toggle in validators/task_schema.py
- [ ] T039 [US5] Test completion toggle with valid JWT authentication
- [ ] T040 [US5] Verify user isolation - users can only toggle their own tasks
- [X] T041 [US5] Ensure updated_at timestamp is refreshed on completion changes

## Phase 8: [US6] Authentication Enforcement
Goal: Ensure system rejects API requests without valid JWT tokens and prevents cross-user access

- [ ] T042 [US6] Test all endpoints return 401 without valid JWT
- [ ] T043 [US6] Test users cannot access other users' tasks (403 forbidden)
- [X] T044 [US6] Verify JWT token validation against Better Auth secret
- [X] T045 [US6] Add comprehensive error handling for authentication failures
- [X] T046 [US6] Ensure user identity is never accepted from request body or URL parameters

## Phase 9: Polish & Cross-Cutting Concerns
Goal: Complete the implementation with proper error handling, logging, and performance optimizations

- [X] T047 Add proper logging throughout the application
- [ ] T048 Optimize database queries with proper indexing
- [X] T049 Add health check endpoint
- [ ] T050 Create comprehensive API documentation
- [ ] T051 Add unit tests for all service functions
- [ ] T052 Add integration tests for all API endpoints
- [ ] T053 Performance test to ensure response times under 2 seconds
- [ ] T054 Final integration test with existing frontend
- [ ] T055 Deploy to staging environment for validation

## Dependencies

1. Phase 1 (Setup) must complete before any other phases
2. Phase 2 (Foundational) must complete before user story phases
3. Each user story phase builds upon the previous foundational work
4. Phase 9 (Polish) can begin after all user story phases are functionally complete

## Parallel Execution Examples

- T006 (Settings) can run in parallel with other setup tasks
- Validators (T011) can be developed in parallel with service functions
- All user story phases could theoretically run in parallel after Phase 2, but should be sequential for proper foundation building

## Implementation Strategy

- MVP: Complete Phase 1, 2, and US1 (task creation) for basic functionality
- Incremental delivery: Each user story phase delivers a complete, testable feature
- Security-first: Authentication and user isolation implemented before business logic
- Test-driven: Validate each phase before moving to the next