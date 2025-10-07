## Assignments and Analysis API

### POST /upload
Upload an assignment file for processing.

- **Headers**: `Authorization: Bearer <jwt>`
- **Form Data**: `file=@assignment.pdf`

- **Responses**
  - 202 Accepted
```json
{
  "id": 1,
  "filename": "assignment.pdf",
  "uploaded_at": "2025-01-01T12:00:00Z"
}
```
  - 400 Bad Request — invalid file
  - 401 Unauthorized — missing/invalid token

- **cURL**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@assignment.pdf"
```

### GET /analysis/{id}
Fetch analysis results for an uploaded assignment.

- **Headers**: `Authorization: Bearer <jwt>`
- **Path Parameters**:
  - `id` — assignment id

- **Responses**
  - 200 OK
```json
{
  "id": 1,
  "assignment_id": 1,
  "suggested_sources": [
    { "id": 101, "title": "Paper 1", "authors": "A. Author" }
  ],
  "plagiarism_score": 0.12,
  "flagged_sections": [
    { "section": "Introduction", "similarity": 0.85 }
  ],
  "research_suggestions": "Focus on methodology...",
  "citation_recommendations": "Use APA 7th format...",
  "confidence_score": 0.91,
  "analyzed_at": "2025-01-01T12:15:00Z"
}
```
  - 401 Unauthorized
  - 404 Not Found — analysis not available

- **cURL**
```bash
curl -X GET "http://localhost:8000/analysis/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
