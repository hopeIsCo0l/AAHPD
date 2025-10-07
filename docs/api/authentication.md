## Authentication API

### POST /auth/register
Register a new student account.

- **Request**
```json
{
  "email": "student@university.edu",
  "password": "password123",
  "full_name": "John Doe",
  "student_id": "STU001"
}
```

- **Responses**
  - 201 Created
```json
{
  "id": 1,
  "email": "student@university.edu",
  "full_name": "John Doe",
  "student_id": "STU001",
  "created_at": "2025-01-01T12:00:00Z"
}
```
  - 400 Bad Request — duplicate email or invalid input

- **cURL**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "password123",
    "full_name": "John Doe",
    "student_id": "STU001"
  }'
```

### POST /auth/login
Authenticate and obtain a JWT.

- **Request**
```json
{
  "email": "student@university.edu",
  "password": "password123"
}
```

- **Responses**
  - 200 OK
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 3600
}
```
  - 401 Unauthorized — invalid credentials

- **cURL**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "password123"
  }'
```

### JWT Usage
Include the token in requests:
```http
Authorization: Bearer <jwt>
```

- Tokens are short-lived; refresh by logging in again or using a refresh endpoint if implemented.
