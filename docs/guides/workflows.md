## End-to-End Workflow

This guide demonstrates a typical student flow from registration through analysis.

### 1. Register
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

### 2. Login
```bash
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "password123"
  }' | jq -r .access_token)
```

### 3. Upload Assignment
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@assignment.pdf"
```

### 4. Get Analysis Results
```bash
curl -X GET "http://localhost:8000/analysis/1" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Search Academic Sources
```bash
curl -X GET "http://localhost:8000/sources?query=machine%20learning%20education" \
  -H "Authorization: Bearer $TOKEN"
```

### Notes
- Replace ids with those returned by your environment.
- Ensure your `.env` contains a valid OpenAI API key.
