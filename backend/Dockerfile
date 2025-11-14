FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
# Increase timeout and add retries for network issues
RUN pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt || \
    pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Create web_interface directory (will be mounted via volume in docker-compose)
RUN mkdir -p web_interface

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
