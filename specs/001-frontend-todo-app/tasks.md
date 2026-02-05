---
description: "Task list template for feature implementation"
---

# Tasks: Frontend Todo Application

**Input**: Design documents from `/specs/001-frontend-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in frontend/ directory
- [x] T002 Initialize Next.js 16+ project with TypeScript dependencies
- [x] T003 [P] Configure Tailwind CSS with clean, neutral defaults
- [x] T004 Create frontend/.env.local with BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_BASE_URL
- [x] T005 Add frontend/.env.local to .gitignore

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Next.js App Router structure with base layout in frontend/app/layout.tsx
- [x] T007 [P] Configure Better Auth with JWT plugin in frontend/lib/auth.ts
- [x] T008 Create centralized API client in frontend/lib/api-client.ts that attaches JWT automatically
- [x] T009 Implement useAuth hook in frontend/hooks/useAuth.ts for global auth state
- [x] T010 Create types definition file in frontend/types/index.ts with User, Task interfaces
- [x] T011 Implement protected route logic with redirect to /login for unauthenticated users
- [x] T012 Setup base styling with max-width container and spacing rules in frontend/app/globals.css

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP
npm
**Goal**: Enable new users to create accounts and authenticate to access the todo functionality

**Independent Test**: User can successfully register with valid credentials, then log in with those credentials and be redirected to the task dashboard. The authentication flow must work without any backend code changes.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US1] Contract test for auth endpoints in frontend/tests/contract/test_auth.py
- [x] T014 [P] [US1] Integration test for registration and login flow in frontend/tests/integration/test_auth_flow.py

### Implementation for User Story 1

- [x] T015 [P] [US1] Create LoginForm component in frontend/components/auth/LoginForm.tsx
- [x] T016 [P] [US1] Create SignupForm component in frontend/components/auth/SignupForm.tsx
- [x] T017 [US1] Implement login page in frontend/app/login/page.tsx
- [x] T018 [US1] Implement signup page in frontend/app/signup/page.tsx
- [x] T019 [US1] Add form validation to login and signup forms based on data-model.md rules
- [x] T020 [US1] Add clear error feedback for authentication failures
- [x] T021 [US1] Implement redirect to /tasks after successful login/signup
- [x] T022 [US1] Add disabled states during form submission
- [x] T023 [US1] Make auth pages responsive and accessible with clean, minimal layout

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P2)

**Goal**: Allow authenticated users to create, view, edit, and delete their personal tasks

**Independent Test**: User can create a new task, view all their tasks, edit an existing task, mark a task as complete/incomplete, and delete a task. All operations must be secured by JWT authentication and only affect the authenticated user's tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T024 [P] [US2] Contract test for task endpoints in frontend/tests/contract/test_tasks.py
- [x] T025 [P] [US2] Integration test for task management flow in frontend/tests/integration/test_task_flow.py

### Implementation for User Story 2

- [x] T026 [P] [US2] Create TaskCard component in frontend/components/ui/TaskCard.tsx
- [x] T027 [P] [US2] Create TaskList component in frontend/components/ui/TaskList.tsx
- [x] T028 [P] [US2] Create CreateTaskForm component in frontend/components/ui/CreateTaskForm.tsx
- [x] T029 [US2] Create EditTaskModal component in frontend/components/ui/EditTaskModal.tsx
- [x] T030 [US2] Create CompletionToggle component in frontend/components/ui/CompletionToggle.tsx
- [x] T031 [US2] Create DeleteConfirmation component in frontend/components/ui/DeleteConfirmation.tsx
- [x] T032 [US2] Implement tasks page in frontend/app/tasks/page.tsx
- [x] T033 [US2] Implement API calls for CRUD operations using centralized API client
- [x] T034 [US2] Add optimistic UI updates for create/update/delete operations
- [x] T035 [US2] Add graceful rollback on API failures
- [x] T036 [US2] Implement centered container layout with clear hierarchy, subtle shadows and spacing
- [x] T037 [US2] Add proper loading states (skeletons) for task operations
- [x] T038 [US2] Implement empty state messaging for users with no tasks
- [x] T039 [US2] Add error states that don't break the layout

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session Management and Security (Priority: P3)

**Goal**: Ensure authentication state is properly managed across browser sessions and users are protected from unauthorized access

**Independent Test**: User authentication state persists across browser refreshes, JWT tokens are automatically attached to API requests, and unauthenticated access attempts redirect to the login page.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T040 [P] [US3] Contract test for session management endpoints in frontend/tests/contract/test_session.py
- [x] T041 [P] [US3] Integration test for session persistence in frontend/tests/integration/test_session_flow.py

### Implementation for User Story 3

- [x] T042 [P] [US3] Enhance useAuth hook to persist session state across browser refreshes
- [x] T043 [US3] Implement JWT token expiration detection and redirect to login
- [x] T044 [US3] Add 401 error handling in API client to force logout
- [x] T045 [US3] Implement logout functionality that clears all session state
- [x] T046 [US3] Add network failure handling with appropriate error states and retry mechanisms
- [x] T047 [US3] Ensure all API requests automatically include JWT tokens without user intervention
- [x] T048 [US3] Add offline detection with appropriate messaging

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T049 [P] Documentation updates in frontend/docs/
- [x] T050 Code cleanup and refactoring
- [x] T051 Performance optimization across all stories
- [x] T052 [P] Additional unit tests (if requested) in frontend/tests/unit/
- [x] T053 Security hardening
- [x] T054 Run quickstart.md validation
- [x] T055 Ensure all UI follows calm, trustworthy, productivity-focused design without being playful or over-designed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on successful authentication from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on authentication state management

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Components before pages
- Pages before integration
- Core implementation before advanced features
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories must be implemented sequentially (US1 then US2 then US3) since US2 depends on US1
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories cannot be worked on in parallel due to dependencies

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create LoginForm component in frontend/components/auth/LoginForm.tsx"
Task: "Create SignupForm component in frontend/components/auth/SignupForm.tsx"
Task: "Contract test for auth endpoints in frontend/tests/contract/test_auth.py"
Task: "Integration test for registration and login flow in frontend/tests/integration/test_auth_flow.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Sequential Team Strategy
With multiple developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - After US1 complete: Developer A moves to User Story 2
   - After US2 complete: Developer A moves to User Story 3

Note: Due to dependencies between stories, they must be completed sequentially rather than in parallel.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence