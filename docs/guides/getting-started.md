## Getting Started

This guide helps you run the system locally and call the APIs.

### 1. Clone and Setup
```bash
git clone <repository-url>
cd academic-assignment-helper
cp env.example .env
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Initialize Database
```bash
docker-compose exec backend python scripts/init_database.py
```

### 4. Verify
- API docs at `http://localhost:8000/docs`
- Health check at `http://localhost:8000/health`

### 5. Next Steps
- Register and login to obtain JWT
- Upload assignment and fetch analysis
- Search academic sources
