#!/bin/bash

# Academic Assignment Helper - Deployment Script
# This script helps deploy the application to various platforms

set -e

echo "🚀 Academic Assignment Helper - Deployment Script"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Please edit .env file with your actual values before deploying!"
            return 1
        else
            print_error ".env.example file not found!"
            return 1
        fi
    fi
    return 0
}

# Deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI not found. Please install it first:"
        echo "npm install -g @railway/cli"
        return 1
    fi
    
    railway login
    railway link
    railway up
    print_success "Deployed to Railway!"
}

# Deploy to VPS
deploy_vps() {
    print_status "Deploying to VPS..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker first."
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not found. Please install Docker Compose first."
        return 1
    fi
    
    # Build and start services
    docker-compose -f docker-compose.production.yml down
    docker-compose -f docker-compose.production.yml build
    docker-compose -f docker-compose.production.yml up -d
    
    print_success "Deployed to VPS!"
    print_status "Application should be available at http://localhost"
}

# Deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    print_warning "Please follow these steps manually:"
    echo "1. Go to https://render.com"
    echo "2. Create a new Web Service"
    echo "3. Connect your GitHub repository"
    echo "4. Use these settings:"
    echo "   - Build Command: docker-compose -f docker-compose.production.yml build"
    echo "   - Start Command: docker-compose -f docker-compose.production.yml up"
    echo "5. Add environment variables from your .env file"
    echo "6. Deploy!"
}

# Test local deployment
test_local() {
    print_status "Testing local deployment..."
    
    if ! check_env; then
        return 1
    fi
    
    # Stop any running containers
    docker-compose down 2>/dev/null || true
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 30
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is running!"
    else
        print_error "Backend health check failed!"
        return 1
    fi
    
    if curl -f http://localhost:8080 > /dev/null 2>&1; then
        print_success "Frontend is running!"
    else
        print_error "Frontend is not accessible!"
        return 1
    fi
    
    print_success "Local deployment test successful!"
    print_status "Frontend: http://localhost:8080"
    print_status "Backend API: http://localhost:8000"
    print_status "pgAdmin: http://localhost:5050"
}

# Show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  railway    Deploy to Railway"
    echo "  vps        Deploy to VPS (Docker)"
    echo "  render     Show instructions for Render deployment"
    echo "  local      Test local deployment"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local      # Test locally"
    echo "  $0 railway    # Deploy to Railway"
    echo "  $0 vps        # Deploy to VPS"
}

# Main script
main() {
    case "${1:-help}" in
        "railway")
            check_env && deploy_railway
            ;;
        "vps")
            check_env && deploy_vps
            ;;
        "render")
            deploy_render
            ;;
        "local")
            test_local
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
