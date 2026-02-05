<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: Added 6 specific principles for Todo web application
Added sections: Authentication & Security, API Design, Database & Persistence, Frontend Constraints, Spec Compliance, Code Quality
Removed sections: Template placeholders
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
# Todo Web Application Constitution

## Core Principles

### Authentication & Security
All API endpoints MUST require a valid JWT token. JWT tokens MUST be issued by Better Auth on the frontend. FastAPI MUST verify JWT tokens using BETTER_AUTH_SECRET. User identity MUST be derived from the JWT, never from client input. Every database query MUST be filtered by the authenticated user_id. Cross-user data access is strictly forbidden. This ensures secure multi-user isolation and prevents unauthorized data access.

### API Design
All routes MUST live under /api/. REST conventions MUST be followed. Endpoints MUST match @specs/api/rest-endpoints.md exactly. Requests without valid JWT MUST return 401 Unauthorized. Unauthorized resource access MUST return 403 Forbidden. Responses MUST be JSON and use proper HTTP status codes. This ensures consistent, secure, and well-documented API interactions.

### Database & Persistence
SQLModel MUST be used for all database operations. Neon PostgreSQL MUST be the only persistence layer. Database schema MUST match @specs/database/schema.md. Task ownership MUST be enforced at the database query level. No in-memory or mock storage is allowed. This ensures reliable, consistent, and scalable data persistence with proper user isolation.

### Frontend Constraints
Next.js App Router MUST be used. Server Components are default; Client Components only when necessary. All backend calls MUST go through a centralized API client. JWT tokens MUST be attached to every API request automatically. No direct fetch calls scattered across components. This ensures clean architecture, proper authentication flow, and maintainable frontend code.

### Spec Compliance
Features MUST satisfy all acceptance criteria in @specs/features/. Do NOT invent features, endpoints, or fields not defined in specs. If ambiguity exists, prefer the more secure and minimal interpretation. If a change is required, update the spec BEFORE changing code. This ensures strict adherence to defined requirements and prevents scope creep.

### Code Quality
Code MUST be production-ready, not hacky or experimental. Clear separation between frontend and backend responsibilities. Errors MUST be handled explicitly and safely. Logging MUST NOT leak secrets or tokens. This ensures maintainable, secure, and robust code delivery.

## Additional Constraints

### Security Requirements
- All authentication must use industry-standard JWT tokens
- User data must be isolated at all layers (frontend, API, database)
- Secrets must never be hardcoded or logged
- All API endpoints must validate authentication and authorization

### Technology Stack
- Backend: FastAPI with SQLModel and Neon PostgreSQL
- Frontend: Next.js with App Router
- Authentication: Better Auth
- Specifications: Strict adherence to files in @specs/ directory

## Development Workflow

### Code Review Process
- All changes must comply with the principles outlined in this constitution
- Code reviews must verify authentication and user isolation requirements
- Changes to API endpoints must be verified against spec documentation
- Database queries must be checked for proper user_id filtering

### Quality Gates
- All endpoints must require proper authentication
- Cross-user data access must be prevented
- Spec compliance must be maintained
- Error handling must be comprehensive and safe

## Governance

This constitution is the single source of truth for the Todo web application project. All implementation must strictly follow these principles unless explicitly updated. Any deviation from these principles constitutes a failure condition. Amendment to this constitution requires explicit documentation of changes, approval from project stakeholders, and a migration plan for existing code. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.1.0 | **Ratified**: 2026-01-31 | **Last Amended**: 2026-01-31