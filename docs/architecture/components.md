## Components

### FastAPI Backend
- Exposes REST endpoints for auth, uploads, analysis, and search
- Handles JWT issuance and verification
- Triggers n8n workflows and aggregates results

### n8n Workflows
- Webhook entrypoint invoked after uploads
- Nodes for text extraction (PDF/Word), LLM analysis, plagiarism detection
- Vector search via pgvector

### PostgreSQL + pgvector
- Relational storage for users, assignments, results, sources
- Vector column for embeddings on `academic_sources`

### External Services
- OpenAI API for LLM-based analysis

### Observability (recommended)
- Request logging and tracing
- Metrics for throughput and latency
- Error monitoring and alerts
