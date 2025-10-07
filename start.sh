#!/bin/bash

# Academic Assignment Helper & Plagiarism Detector Startup Script

echo "🚀 Starting Academic Assignment Helper & Plagiarism Detector"
echo "=========================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key before continuing."
    echo "   You can edit it with: nano .env"
    read -p "Press Enter when you've updated the .env file..."
fi

# Start services with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U student -d academic_helper > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check FastAPI backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI backend is ready"
else
    echo "❌ FastAPI backend is not ready"
fi

# Check n8n
if curl -s http://localhost:5678 > /dev/null 2>&1; then
    echo "✅ n8n is ready"
else
    echo "❌ n8n is not ready"
fi

# Initialize database
echo "🗄️  Initializing database..."
docker-compose exec backend python scripts/init_database.py

echo ""
echo "🎉 System is ready!"
echo ""
echo "📋 Access URLs:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • n8n Interface: http://localhost:5678 (admin/admin123)"
echo "   • pgAdmin: http://localhost:5050 (admin@admin.com/admin)"
echo ""
echo "🧪 Test the API:"
echo "   python scripts/test_api.py"
echo ""
echo "📚 Sample credentials:"
echo "   Email: test@student.com"
echo "   Password: password123"
echo ""
echo "🛑 To stop the system:"
echo "   docker-compose down"
