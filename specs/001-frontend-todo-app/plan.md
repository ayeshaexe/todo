# Implementation Plan: Frontend Todo Application

**Branch**: `001-frontend-todo-app` | **Date**: 2026-01-31 | **Spec**: [specs/001-frontend-todo-app/spec.md](specs/001-frontend-todo-app/spec.md)
**Input**: Feature specification from `/specs/001-frontend-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure, production-quality frontend for the multi-user Todo web application using Next.js App Router. The implementation will include user authentication via Better Auth with JWT, a centralized API client for backend communication, and a clean, professional UI for task management. The application will enforce user isolation and follow all security requirements from the constitution.

## Technical Context

**Language/Version**: TypeScript with Next.js 16+
**Primary Dependencies**: Next.js App Router, Tailwind CSS, Better Auth, React Server Components
**Storage**: N/A (Client-side only)
**Testing**: Jest and React Testing Library (NEEDS CLARIFICATION)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application
**Performance Goals**: Sub-3s page load times, responsive UI interactions
**Constraints**: Must follow Next.js App Router conventions, JWT authentication required for all API calls, mobile-responsive design
**Scale/Scope**: Individual user sessions, multi-user isolation at backend level

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] All API endpoints require valid JWT token (via centralized API client)
- [x] JWT tokens issued by Better Auth on frontend
- [x] FastAPI verifies JWT tokens using BETTER_AUTH_SECRET
- [x] User identity derived from JWT, never from client input
- [x] Every database query filtered by authenticated user_id (enforced by backend)
- [x] Cross-user data access forbidden (enforced by backend)
- [x] All routes live under /api/ (on backend, frontend routes are /login, /signup, /tasks)
- [x] REST conventions followed for API endpoints
- [x] Endpoints match @specs/api/rest-endpoints.md exactly
- [x] Requests without valid JWT return 401 Unauthorized
- [x] Unauthorized resource access returns 403 Forbidden
- [x] Responses are JSON with proper HTTP status codes
- [x] SQLModel used for database operations (backend responsibility)
- [x] Neon PostgreSQL used (backend responsibility)
- [x] Database schema matches @specs/database/schema.md (backend responsibility)
- [x] Task ownership enforced at database query level (backend responsibility)
- [x] Next.js App Router used as required
- [x] Server Components default; Client Components only when necessary
- [x] All backend calls through centralized API client
- [x] JWT tokens attached to every API request automatically
- [x] No direct fetch calls scattered across components
- [x] Features satisfy all acceptance criteria in @specs/features/
- [x] No features, endpoints, or fields invented not defined in specs
- [x] Code is production-ready, not hacky or experimental
- [x] Clear separation between frontend and backend responsibilities
- [x] Errors handled explicitly and safely
- [x] Logging does not leak secrets or tokens

## Project Structure

### Documentation (this feature)
```text
specs/001-frontend-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
frontend/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   └── tasks/
│       └── page.tsx
├── components/
│   ├── ui/
│   │   ├── AppShell.tsx
│   │   ├── TaskCard.tsx
│   │   ├── TaskList.tsx
│   │   ├── CreateTaskForm.tsx
│   │   ├── EditTaskModal.tsx
│   │   ├── CompletionToggle.tsx
│   │   └── DeleteConfirmation.tsx
│   └── auth/
│       ├── LoginForm.tsx
│       └── SignupForm.tsx
├── lib/
│   ├── auth.ts
│   └── api-client.ts
├── hooks/
│   └── useAuth.ts
├── types/
│   └── index.ts
└── public/
    └── favicon.ico
```

**Structure Decision**: Web application structure selected with frontend directory containing Next.js App Router pages, reusable components, utility functions, and type definitions. The structure separates concerns with dedicated directories for UI components, authentication logic, API client, hooks, and types.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|