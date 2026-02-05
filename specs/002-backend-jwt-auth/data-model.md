# Data Model for Todo App Backend

## Task Entity

### Attributes
- **id**: integer (Primary Key, Auto-generated)
- **user_id**: string (Indexed, Foreign Key reference conceptually to user from JWT)
- **title**: string (Required, 1-200 characters)
- **description**: text (Optional, max 1000 characters)
- **completed**: boolean (Default: false)
- **created_at**: datetime (Auto-generated on creation)
- **updated_at**: datetime (Auto-generated on update)

### Relationships
- Conceptually belongs to a User (identified by user_id from JWT token)
- Each task is owned by exactly one authenticated user
- Users can own multiple tasks

### Validation Rules
- title must be 1-200 characters
- description, if provided, must be ≤ 1000 characters
- completed defaults to false if not provided
- created_at and updated_at are automatically managed

## User Identity (External to Database)

### Attributes
- **user_id**: string (Extracted from JWT payload)
- **email**: string (Extracted from JWT payload, optional)

### Relationships
- Implicitly owns multiple Task entities
- Identified through JWT token verification

### Notes
- User data is managed externally by Better Auth
- Only user_id is used for database filtering
- No direct User table is created as users are managed by Better Auth

## State Transitions

### Task Completion
- **Initial State**: completed = false
- **Transition**: PATCH /api/tasks/{id}/complete with {completed: true}
- **Resulting State**: completed = true

### Task Updates
- **Operation**: PUT /api/tasks/{id} with updated attributes
- **Effect**: updated_at timestamp is refreshed
- **Constraint**: Only owner can modify task