# Academic Assignment Helper & Plagiarism Detector (RAG-Powered)

A comprehensive backend system that helps students with academic assignments through AI-powered analysis, RAG-based research suggestions, and plagiarism detection.

## 🚀 Features

- **JWT-based Authentication** - Secure API endpoints with role-based access
- **File Upload & Processing** - Support for PDF and Word documents
- **RAG-Powered Research** - AI-powered academic source suggestions
- **Plagiarism Detection** - Automated similarity analysis against academic databases
- **n8n Automation** - Workflow orchestration for complex processing
- **Vector Database** - PostgreSQL with pgvector for semantic search
- **Dockerized Setup** - Easy deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │      n8n        │    │   PostgreSQL    │
│   Backend       │◄──►│   Workflows     │◄──►│   + pgvector    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Upload   │    │  AI Analysis    │    │  Academic       │
│   & Storage     │    │  & Processing   │    │  Sources DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API Key (for AI analysis)
- Python 3.11+ (for local development)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/hopeIsCo0l/AAHPD.git
   cd academic-assignment-helper
   ```

2. **Environment Configuration**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize Database**
   ```bash
   docker-compose exec backend python scripts/init_database.py
   ```

5. **Access Services**
   - **API Documentation**: http://localhost:8000/docs
   - **n8n Interface**: http://localhost:5678 (admin/admin123)
   - **pgAdmin**: http://localhost:5050 (admin@admin.com/admin)

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - Register new student
- `POST /auth/login` - Login and get JWT token

### Assignment Management
- `POST /upload` - Upload assignment file (requires JWT)
- `GET /analysis/{id}` - Get analysis results (requires JWT)
- `GET /sources` - Search academic sources (requires JWT)

### Health Check
- `GET /health` - Service health status

## 📊 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Assignments Table
```sql
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
```

### Analysis Results Table
```sql
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
```

### Academic Sources Table
```sql
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

## 🔄 n8n Workflow

The n8n workflow handles:
1. **File Processing** - Text extraction from PDF/Word documents
2. **AI Analysis** - Content analysis using OpenAI GPT
3. **RAG Search** - Vector similarity search for relevant sources
4. **Plagiarism Detection** - AI-powered similarity analysis
5. **Database Storage** - Structured storage of analysis results

## 🛠️ Development

### Local Development Setup

1. **Backend Development**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Database Setup**
   ```bash
   # Start PostgreSQL with pgvector
   docker run --name postgres-pgvector -e POSTGRES_PASSWORD=password -p 5432:5432 -d pgvector/pgvector:pg15
   
   # Run database initialization
   python scripts/init_database.py
   ```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Database
POSTGRES_DB=academic_helper
POSTGRES_USER=student
POSTGRES_PASSWORD=secure_password

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key

# n8n
N8N_WEBHOOK_URL=http://n8n:5678/webhook/assignment
```

## 📝 Usage Examples

### 1. Register and Login
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "password123",
    "full_name": "John Doe",
    "student_id": "STU001"
  }'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "password123"
  }'
```

### 2. Upload Assignment
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@assignment.pdf"
```

### 3. Get Analysis Results
```bash
curl -X GET "http://localhost:8000/analysis/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Search Academic Sources
```bash
curl -X GET "http://localhost:8000/sources?query=machine learning education" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- File type validation
- Input sanitization
- Secure password handling (in production)

## 🚀 Production Deployment

1. **Update Environment Variables**
   - Use strong, unique passwords
   - Set secure JWT secret key
   - Configure proper database credentials

2. **Security Hardening**
   - Enable HTTPS
   - Configure firewall rules
   - Regular security updates
   - Monitor logs and access

3. **Scaling Considerations**
   - Use managed database services
   - Implement caching (Redis)
   - Load balancing for API
   - CDN for file storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## 🔮 Future Enhancements

- [ ] Real-time collaboration features
- [ ] Advanced plagiarism detection algorithms
- [ ] Integration with learning management systems
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Citation formatting tools
- [ ] Peer review system
# AAHPD
