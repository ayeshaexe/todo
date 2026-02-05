---
id: 3
title: Plan Frontend Todo App
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-todo-app
branch: 001-frontend-todo-app
user: NBK COMPUTER
command: sp.plan
labels: [planning,todo-app,frontend,architecture]
links:
  spec: specs/001-frontend-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-todo-app/plan.md
  - specs/001-frontend-todo-app/research.md
  - specs/001-frontend-todo-app/data-model.md
  - specs/001-frontend-todo-app/quickstart.md
  - specs/001-frontend-todo-app/contracts/api-contract.md
tests:
  - none
---

## Prompt

```text
You are planning the FRONTEND implementation for Phase II of the Todo Full-Stack Web Application.

This plan is governed by the active sp.constitution and the approved sp.specify.
No step may violate security, spec compliance, or architectural boundaries.

SCOPE:
Frontend only (Next.js).
Backend is assumed to exist and conform to specs.

---

## STEP 0: ENVIRONMENT SETUP (MANDATORY – FIRST)

Create frontend environment file:

File: frontend/.env.local

Add the following variables exactly:

BETTER_AUTH_SECRET=8ApAiAkyiQZg3XVId7GKjNyYXoFUw9vz
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

Rules:
- Do NOT hardcode these values in code
- Use process.env for access
- .env.local MUST be gitignored
- BETTER_AUTH_SECRET must match backend secret

Implementation must assume these variables already exist.

---

## STEP 1: PROJECT STRUCTURE & BASE SETUP

- Verify Next.js App Router structure
- Configure Tailwind CSS with clean, neutral defaults
- Establish base layout and typography
- Set max-width container and spacing rules
- Create App Shell layout (header + content)

No UI logic yet.

---

## STEP 2: AUTHENTICATION INTEGRATION (BETTER AUTH)

- Install and configure Better Auth
- Enable JWT plugin
- Configure providers for signup and login
- Ensure JWT is issued on successful authentication
- Expose authentication state globally
- Implement protected route logic
- Redirect unauthenticated users to /login
- Ensure logout fully clears session

No backend calls without valid auth state.

---

## STEP 3: CENTRALIZED API CLIENT

Create a single API client module that:

- Uses NEXT_PUBLIC_API_BASE_URL
- Automatically attaches JWT token to every request
- Handles 401 Unauthorized by forcing logout
- Normalizes error responses
- Exposes typed methods for task operations

Strict rule:
NO fetch calls inside components.

---

## STEP 4: AUTHENTICATION PAGES

Implement:
- /login
- /signup

Requirements:
- Clean, minimal layout
- Proper form validation
- Clear error feedback
- Disabled states during submission
- Responsive and accessible

Must feel professional and production-ready.

---

## STEP 5: TASK PAGE & CORE UI

Implement authenticated page:
- /tasks

Include:
- Task list view
- Create task form
- Task card component
- Completion toggle
- Edit task (modal or inline)
- Delete confirmation

Layout rules:
- Centered container
- Clear hierarchy
- Subtle shadows and spacing
- Calm, neutral design

---

## STEP 6: DATA FLOW & INTERACTIONS

- Fetch tasks using API client
- Optimistic UI updates for create/update/delete
- Graceful rollback on failure
- Loading states (skeletons preferred)
- Empty state messaging
- Error states without layout breakage

All data must come from backend APIs.

---

## STEP 7: STATE & PERFORMANCE REFINEMENT

- Server Components by default
- Client Components only where interaction is required
- Persist auth state across refresh
- Avoid unnecessary re-renders
- Remove unused state and props

---

## STEP 8: FINAL VALIDATION

Verify:
- JWT is attached to every API request
- Unauthenticated access is impossible
- UI is responsive and accessible
- No hardcoded secrets or user IDs
- No deviation from specs
- Frontend complies fully with sp.constitution

---

OUTPUT:
A stable, secure, production-quality frontend implementation ready for backend integration and evaluation.
```

## Response snapshot

Completed the implementation planning for the frontend todo application. Created the following artifacts:
1. Implementation plan (plan.md) outlining the architecture and structure
2. Research document (research.md) with technical decisions
3. Data model (data-model.md) defining entities and validation rules
4. API contracts (contracts/api-contract.md) specifying backend integration
5. Quickstart guide (quickstart.md) for development setup

The plan follows all security and architectural requirements from the constitution, including JWT authentication, user isolation, centralized API client, and proper frontend/backend separation.

## Outcome

- ✅ Impact: Complete architecture plan for frontend todo app implementation
- 🧪 Tests: none
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, quickstart.md, api-contract.md)
- 🔁 Next prompts: Ready for task generation (/sp.tasks)
- 🧠 Reflection: Plan comprehensively covers all requirements from spec and constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All planning artifacts created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from this plan