## Data Models

This section documents the primary data models used by the system. Fields marked as optional may be null or omitted in responses.

### Student
```json
{
  "id": 1,
  "email": "student@university.edu",
  "full_name": "John Doe",
  "student_id": "STU001",
  "created_at": "2025-01-01T12:00:00Z"
}
```

### Assignment
```json
{
  "id": 1,
  "student_id": 1,
  "filename": "assignment.pdf",
  "original_text": "...",
  "topic": "Machine Learning",
  "academic_level": "Undergraduate",
  "word_count": 1234,
  "uploaded_at": "2025-01-01T12:00:00Z"
}
```

### AnalysisResult
```json
{
  "id": 1,
  "assignment_id": 1,
  "suggested_sources": [ /* array of Source */ ],
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

### Source
```json
{
  "id": 101,
  "title": "Impact of ML in Education",
  "authors": "A. Author, B. Researcher",
  "publication_year": 2024,
  "abstract": "...",
  "full_text": "...",
  "source_type": "journal",
  "embedding": "VECTOR(1536)",
  "created_at": "2025-01-01T12:00:00Z"
}
```

### Database Schema
The following SQL is a conceptual representation aligned with the implementation:

```sql
-- Students
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assignments
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    filename TEXT NOT NULL,
    original_text TEXT,
    topic TEXT,
    academic_level TEXT,
    word_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis Results
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id),
    suggested_sources JSONB,
    plagiarism_score FLOAT,
    flagged_sections JSONB,
    research_suggestions TEXT,
    citation_recommendations TEXT,
    confidence_score FLOAT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic Sources
CREATE TABLE academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
