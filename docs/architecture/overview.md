## Architecture Overview

The system consists of a FastAPI backend, an n8n workflow engine, and a PostgreSQL database with pgvector for semantic search. Files are uploaded to the backend, processed via n8n, analyzed using LLMs, and results are stored and served via API.

### Components
- FastAPI backend — authentication, API endpoints, orchestration
- n8n — file processing, analysis pipeline, RAG orchestration
- PostgreSQL + pgvector — structured data and vector embeddings

### Data Flow
1. User uploads assignment via `/upload`
2. Backend stores file and triggers n8n webhook
3. n8n extracts text, performs analysis, queries vector DB
4. Results are persisted and available at `/analysis/{id}`

### Security
- JWT-based authentication
- Role-based access (future extension)
- Input validation and sanitization
