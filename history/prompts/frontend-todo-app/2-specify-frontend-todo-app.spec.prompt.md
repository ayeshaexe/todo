---
id: 2
title: Specify Frontend Todo App
stage: spec
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-todo-app
branch: 001-frontend-todo-app
user: NBK COMPUTER
command: sp.specify
labels: [specification,todo-app,frontend,authentication]
links:
  spec: specs/001-frontend-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-todo-app/spec.md
  - specs/001-frontend-todo-app/checklists/requirements.md
tests:
  - none
---

## Prompt

```text
You are specifying the FRONTEND implementation for Phase II of the Todo Full-Stack Web Application.

This specification is governed by the active sp.constitution.
All rules defined there are mandatory and override convenience or shortcuts.

SCOPE:
Frontend only.
Backend is assumed to exist and conform to specs.

TECH STACK (MANDATORY):
- Next.js 16+ using App Router
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Spec-driven implementation

PRIMARY OBJECTIVES:
1. Build a secure, production-quality frontend for a multi-user Todo app
2. Enforce JWT-based authentication on all API interactions
3. Deliver a clean, modern, professional UI suitable for real-world SaaS products

---

## AUTHENTICATION REQUIREMENTS

- Use Better Auth for signup, signin, and session management
- JWT plugin MUST be enabled
- JWT token MUST be attached automatically to every backend API request
- Authentication state MUST be globally accessible
- Unauthenticated users MUST be redirected to the login page
- Logout MUST fully clear session state

NO hardcoded user IDs.
NO API calls without JWT.

---

## APPLICATION PAGES (REQUIRED)

1. Authentication Pages
- /login
- /signup

Requirements:
- Minimal, clean layout
- Clear validation feedback
- Accessible and responsive
- Professional typography and spacing
- Error states must be human-readable

2. Main App Page
- /tasks (authenticated only)

Layout:
- Centered content with max-width (no full-width chaos)
- Clear page hierarchy
- Subtle shadows, rounded corners, consistent spacing
- Neutral, modern color palette (no flashy gradients)

---

## UI COMPONENTS (REQUIRED)

- App Shell (layout with header)
- Task List
- Task Card
- Create Task Form
- Edit Task Modal or Inline Edit
- Completion Toggle
- Delete Confirmation
- Loading States (skeletons preferred)
- Empty State (professional, calm messaging)
- Error State

UI must feel:
- Calm
- Trustworthy
- Productivity-focused
- Not playful, not cheap, not over-designed

---

## TASK FUNCTIONALITY

- Create task
- View all tasks
- Edit task
- Delete task
- Toggle completion

Rules:
- UI must optimistically update but recover on failure
- All actions must show loading or disabled states
- Errors must be surfaced clearly without breaking layout

---

## API INTEGRATION

- All backend calls MUST go through a centralized API client
- API client MUST:
  - Attach JWT token automatically
  - Handle 401 and force logout
  - Normalize error responses
- No direct fetch calls inside components

Endpoints used MUST match @specs/api/rest-endpoints.md exactly.

---

## STATE MANAGEMENT

- Prefer server components for data fetching
- Use client components only for interactivity
- Avoid unnecessary global state
- Authentication state must persist across refreshes

---

## UX & DESIGN STANDARDS

- Mobile-first responsive design
- Keyboard accessible
- Proper focus management
- Consistent spacing and typography
- No inline styles
- No component duplication

UI should resemble:
- A small internal company tool
- A minimal SaaS dashboard
- Something a hiring manager would respect

---

## NON-GOALS (EXPLICITLY FORBIDDEN)

- No mock data
- No placeholder UI
- No console-based UX
- No direct DOM manipulation
- No undocumented components

---

## ACCEPTANCE CRITERIA

- User can sign up and sign in successfully
- JWT token is attached to every API request
- Authenticated users see ONLY their own tasks
- UI is responsive, polished, and stable
- App works without backend code changes
- Frontend fully complies with sp.constitution

---

DELIVERABLE:
A production-ready frontend implementation that strictly follows the specs, enforces security boundaries, and presents a clean, professional user experience.
```

## Response snapshot

Created a comprehensive specification for the frontend todo application. The spec includes three user stories prioritized by importance: (1) User Registration and Login (P1), (2) Task Management (P2), and (3) Session Management and Security (P3). Each user story has clear acceptance scenarios, priorities, and independent test criteria. The specification also includes functional requirements, key entities, success criteria, and edge cases. A quality checklist was created to validate the specification completeness.

## Outcome

- ✅ Impact: Created complete feature specification for frontend todo app
- 🧪 Tests: none
- 📁 Files: 2 files created (spec.md, requirements checklist)
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification follows constitution requirements with proper authentication and user isolation

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Specification complete and validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase