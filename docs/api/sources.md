## Academic Sources API

### GET /sources
Search academic sources by query string. Requires authentication.

- **Headers**: `Authorization: Bearer <jwt>`
- **Query Parameters**:
  - `query` (string, required) — search terms
  - `limit` (int, optional, default 10)
  - `offset` (int, optional, default 0)

- **Responses**
  - 200 OK
```json
{
  "results": [
    {
      "id": 101,
      "title": "Impact of ML in Education",
      "authors": "A. Author, B. Researcher",
      "publication_year": 2024,
      "abstract": "...",
      "source_type": "journal"
    }
  ],
  "total": 123,
  "limit": 10,
  "offset": 0
}
```
  - 401 Unauthorized

- **cURL**
```bash
curl -X GET "http://localhost:8000/sources?query=machine%20learning%20education" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
