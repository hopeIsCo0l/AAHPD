#!/bin/bash

# Start the FastAPI application
echo "Starting Academic Assignment Helper API..."
echo "Port: ${PORT:-8000}"
echo "Database URL: ${DATABASE_URL}"

# Run the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}