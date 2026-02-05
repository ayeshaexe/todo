---
id: 1
title: Update Auth Security Constitution
stage: constitution
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-auth-system-foundation
user: NBK COMPUTER
command: sp.constitution
labels: [constitution,security,authentication]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
You are operating under a Spec-Driven Development constitution.

The specifications in /specs are the single source of truth.
Implementation must strictly follow the specs unless a spec is explicitly updated first.

NON-NEGOTIABLE RULES:

1. Authentication & Security
- All API endpoints MUST require a valid JWT token.
- JWT tokens MUST be issued by Better Auth on the frontend.
- FastAPI MUST verify JWT tokens using BETTER_AUTH_SECRET.
- User identity MUST be derived from the JWT, never from client input.
- Every database query MUST be filtered by the authenticated user_id.
- Cross-user data access is strictly forbidden.

2. API Design
- All routes MUST live under /api/.
- REST conventions MUST be followed.
- Endpoints MUST match @specs/api/rest-endpoints.md exactly.
- Requests without valid JWT MUST return 401 Unauthorized.
- Unauthorized resource access MUST return 403 Forbidden.
- Responses MUST be JSON and use proper HTTP status codes.

3. Database & Persistence
- SQLModel MUST be used for all database operations.
- Neon PostgreSQL MUST be the only persistence layer.
- Database schema MUST match @specs/database/schema.md.
- Task ownership MUST be enforced at the database query level.
- No in-memory or mock storage is allowed.

4. Frontend Constraints
- Next.js App Router MUST be used.
- Server Components are default; Client Components only when necessary.
- All backend calls MUST go through a centralized API client.
- JWT tokens MUST be attached to every API request automatically.
- No direct fetch calls scattered across components.

5. Spec Compliance
- Features MUST satisfy all acceptance criteria in @specs/features/.
- Do NOT invent features, endpoints, or fields not defined in specs.
- If ambiguity exists, prefer the more secure and minimal interpretation.
- If a change is required, update the spec BEFORE changing code.

6. Code Quality
- Code MUST be production-ready, not hacky or experimental.
- Clear separation between frontend and backend responsibilities.
- Errors MUST be handled explicitly and safely.
- Logging MUST NOT leak secrets or tokens.

FAILURE CONDITIONS:
- Any endpoint accessible without JWT authentication.
- Any task accessible across users.
- Any deviation from defined specs.
- Any hardcoded secrets or user IDs.

PRIMARY OBJECTIVE:
Deliver a secure, multi-user, full-stack Todo web application that strictly follows the provided specs, enforces user isolation, and demonstrates professional-grade spec-driven development.
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) to reflect the specific non-negotiable rules for the Todo web application. The new constitution includes six core principles covering Authentication & Security, API Design, Database & Persistence, Frontend Constraints, Spec Compliance, and Code Quality. Each principle contains the specific requirements from the user input, ensuring strict adherence to security and spec-driven development practices.

## Outcome

- ✅ Impact: Updated constitution to enforce security and spec compliance requirements
- 🧪 Tests: none
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implementation should now follow these constitution guidelines
- 🧠 Reflection: Constitution now serves as the authoritative source for security and development practices

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution properly updated with all required principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation following the new constitution guidelines