# API Contract: Todo Application Backend Endpoints

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Register a new user account
**Authentication**: None required

**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Response**:
- 201 Created: User successfully registered
```json
{
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  },
  "jwt_token": "string"
}
```
- 400 Bad Request: Invalid input
- 409 Conflict: Email already exists

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
**Authentication**: None required

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**:
- 200 OK: Successful authentication
```json
{
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  },
  "jwt_token": "string"
}
```
- 400 Bad Request: Invalid input
- 401 Unauthorized: Invalid credentials

### POST /api/auth/logout
**Description**: Logout user and invalidate session
**Authentication**: JWT required

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response**:
- 200 OK: Successfully logged out
```json
{
  "message": "Successfully logged out"
}
```

## Task Management Endpoints

### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user
**Authentication**: JWT required

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response**:
- 200 OK: Tasks retrieved successfully
```json
{
  "tasks": [
    {
      "id": "string",
      "userId": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "createdAt": "string (ISO date)",
      "updatedAt": "string (ISO date)"
    }
  ]
}
```
- 401 Unauthorized: Invalid or missing JWT

### POST /api/tasks
**Description**: Create a new task for the authenticated user
**Authentication**: JWT required

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Response**:
- 201 Created: Task created successfully
```json
{
  "task": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```
- 400 Bad Request: Invalid input
- 401 Unauthorized: Invalid or missing JWT

### PUT /api/tasks/{taskId}
**Description**: Update an existing task for the authenticated user
**Authentication**: JWT required

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Parameters**:
- taskId: string (task identifier)

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Response**:
- 200 OK: Task updated successfully
```json
{
  "task": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```
- 400 Bad Request: Invalid input
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Task does not exist

### DELETE /api/tasks/{taskId}
**Description**: Delete a task for the authenticated user
**Authentication**: JWT required

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Parameters**:
- taskId: string (task identifier)

**Response**:
- 200 OK: Task deleted successfully
```json
{
  "message": "Task deleted successfully"
}
```
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Task does not exist