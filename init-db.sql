-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the academic_helper database (if not exists)
-- This is handled by the POSTGRES_DB environment variable

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE academic_helper TO student;
