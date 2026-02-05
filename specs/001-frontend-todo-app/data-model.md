# Data Model: Frontend Todo Application

## User Entity
- **Properties**:
  - id: string (unique identifier from authentication system)
  - email: string (user's email address)
  - name: string (optional, user's display name)
  - createdAt: Date (account creation timestamp)
  - updatedAt: Date (last account update timestamp)

- **Validation**:
  - Email must be a valid email format
  - Email must be unique across all users

- **Relationships**:
  - One-to-many with Task entity (user owns multiple tasks)

## Task Entity
- **Properties**:
  - id: string (unique identifier)
  - userId: string (foreign key linking to User)
  - title: string (task title/description)
  - description: string (optional detailed description)
  - completed: boolean (completion status)
  - createdAt: Date (task creation timestamp)
  - updatedAt: Date (last task update timestamp)

- **Validation**:
  - Title must not be empty
  - UserId must correspond to an existing user
  - Completed defaults to false

- **State Transitions**:
  - Pending → Completed (when user marks task as done)
  - Completed → Pending (when user unmarks task)

## Session Entity (Client-side)
- **Properties**:
  - jwtToken: string (JSON Web Token for API authentication)
  - user: User object (authenticated user data)
  - expiresAt: Date (token expiration timestamp)

- **Validation**:
  - JWT token must be valid and not expired
  - User data must be present when authenticated

## API Response Format
- **Success Response**:
  - data: object/array (actual response data)
  - status: number (HTTP status code)
  - message: string (optional success message)

- **Error Response**:
  - error: string/object (error details)
  - status: number (HTTP status code)
  - message: string (human-readable error message)

## Form Validation Rules
- **Login Form**:
  - Email: required, valid email format
  - Password: required, minimum 8 characters

- **Signup Form**:
  - Email: required, valid email format
  - Password: required, minimum 8 characters, contains uppercase, lowercase, and number
  - Name: optional, maximum 50 characters

- **Task Form**:
  - Title: required, maximum 200 characters
  - Description: optional, maximum 1000 characters