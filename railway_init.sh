#!/bin/bash

echo "🚀 Initializing Railway Database..."

# Install required packages
pip install sqlalchemy psycopg2-binary pgvector

# Run database initialization
python railway_init_db.py

echo "✅ Database initialization complete!"
