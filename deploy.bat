@echo off
REM Academic Assignment Helper - Windows Deployment Script

echo 🚀 Academic Assignment Helper - Deployment Script
echo =================================================

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found. Creating from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo [WARNING] Please edit .env file with your actual values before deploying!
        pause
        exit /b 1
    ) else (
        echo [ERROR] .env.example file not found!
        pause
        exit /b 1
    )
)

if "%1"=="railway" goto :railway
if "%1"=="vps" goto :vps
if "%1"=="render" goto :render
if "%1"=="local" goto :local
goto :help

:railway
echo [INFO] Deploying to Railway...
echo Please install Railway CLI first: npm install -g @railway/cli
echo Then run: railway login
echo Then run: railway link
echo Then run: railway up
pause
exit /b 0

:vps
echo [INFO] Deploying to VPS...
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d
echo [SUCCESS] Deployed to VPS!
echo Application should be available at http://localhost
pause
exit /b 0

:render
echo [INFO] Deploying to Render...
echo Please follow these steps manually:
echo 1. Go to https://render.com
echo 2. Create a new Web Service
echo 3. Connect your GitHub repository
echo 4. Use these settings:
echo    - Build Command: docker-compose -f docker-compose.production.yml build
echo    - Start Command: docker-compose -f docker-compose.production.yml up
echo 5. Add environment variables from your .env file
echo 6. Deploy!
pause
exit /b 0

:local
echo [INFO] Testing local deployment...
docker-compose down
docker-compose up -d
echo [INFO] Waiting for services to start...
timeout /t 30 /nobreak > nul
echo [SUCCESS] Local deployment test complete!
echo Frontend: http://localhost:8080
echo Backend API: http://localhost:8000
echo pgAdmin: http://localhost:5050
pause
exit /b 0

:help
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   railway    Deploy to Railway
echo   vps        Deploy to VPS (Docker)
echo   render     Show instructions for Render deployment
echo   local      Test local deployment
echo   help       Show this help message
echo.
echo Examples:
echo   %0 local      # Test locally
echo   %0 railway    # Deploy to Railway
echo   %0 vps        # Deploy to VPS
pause
exit /b 0
