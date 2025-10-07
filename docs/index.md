## Academic Assignment Helper & Plagiarism Detector – Developer Documentation

Welcome to the developer docs for the RAG-powered Academic Assignment Helper & Plagiarism Detector. This documentation describes the public APIs, data models, system components, and how to use them end-to-end.

- **API base URL**: `http://localhost:8000`
- **OpenAPI UI**: `http://localhost:8000/docs`

### Quick links
- **API Reference**
  - [Authentication](./api/authentication.md)
  - [Assignments & Analysis](./api/assignments.md)
  - [Academic Sources](./api/sources.md)
  - [Health](./api/health.md)
- **Reference**
  - [Data Models](./reference/data-models.md)
  - [Errors](./reference/errors.md)
- **Guides**
  - [Getting Started](./guides/getting-started.md)
  - [End-to-End Workflow](./guides/workflows.md)
- **Architecture**
  - [Overview](./architecture/overview.md)
  - [Components](./architecture/components.md)

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- OpenAI API key set in `.env`

### Conventions
- **Authentication**: Bearer JWT in the `Authorization` header: `Authorization: Bearer <token>`
- **Content Types**: JSON for request/response bodies unless stated otherwise (file uploads use `multipart/form-data`).
- **Timestamps**: ISO 8601 UTC (e.g., `2025-01-30T12:34:56Z`).

> Note: The OpenAPI at `/docs` is the source of truth for parameter and schema details at runtime.
