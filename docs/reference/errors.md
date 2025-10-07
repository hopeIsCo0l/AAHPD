## Errors

The API uses standard HTTP status codes and returns structured error responses.

### Error Response Format
```json
{
  "error": {
    "code": "string",
    "message": "Human-readable message",
    "details": { "field": "reason" }
  }
}
```

### Common Errors
- **400 Bad Request**: Malformed payload or missing required fields
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **413 Payload Too Large**: File upload exceeds allowed size
- **415 Unsupported Media Type**: Invalid content type for upload
- **429 Too Many Requests**: Rate-limited
- **500 Internal Server Error**: Unexpected server error

### Examples
- Validation error (400):
```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid email format",
    "details": { "email": "must be a valid email" }
  }
}
```

- Unauthorized (401):
```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid token"
  }
}
```
