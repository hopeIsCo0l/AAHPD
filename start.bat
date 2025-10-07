@echo off
echo 🚀 Starting Academic Assignment Helper ^& Plagiarism Detector
echo ==========================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file and add your OpenAI API key before continuing.
    echo    You can edit it with: notepad .env
    pause
)

REM Start services with Docker Compose
echo 🐳 Starting services with Docker Compose...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service health...

REM Check FastAPI backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FastAPI backend is ready
) else (
    echo ❌ FastAPI backend is not ready
)

REM Check n8n
curl -s http://localhost:5678 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ n8n is ready
) else (
    echo ❌ n8n is not ready
)

REM Initialize database
echo 🗄️  Initializing database...
docker-compose exec backend python scripts/init_database.py

echo.
echo 🎉 System is ready!
echo.
echo 📋 Access URLs:
echo    • API Documentation: http://localhost:8000/docs
echo    • n8n Interface: http://localhost:5678 (admin/admin123)
echo    • pgAdmin: http://localhost:5050 (admin@admin.com/admin)
echo.
echo 🧪 Test the API:
echo    python scripts/test_api.py
echo.
echo 📚 Sample credentials:
echo    Email: test@student.com
echo    Password: password123
echo.
echo 🛑 To stop the system:
echo    docker-compose down
echo.
pause
