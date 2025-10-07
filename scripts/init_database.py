#!/usr/bin/env python3
"""
Database initialization script for Academic Assignment Helper
This script creates the database tables and populates them with sample data.
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from models import create_tables, init_db, get_db, AcademicSource
from rag_service import RAGService
from sqlalchemy.orm import Session

async def populate_academic_sources():
    """Populate the database with sample academic sources"""
    print("Loading sample academic sources...")
    
    # Load sample data
    sample_data_path = Path(__file__).parent.parent / "data" / "sample_academic_sources.json"
    
    with open(sample_data_path, 'r', encoding='utf-8') as f:
        sample_sources = json.load(f)
    
    # Initialize RAG service
    rag_service = RAGService()
    
    # Add each source to the database
    db = next(get_db())
    try:
        for source_data in sample_sources:
            print(f"Adding source: {source_data['title']}")
            
            # Generate embedding for the full text
            embedding = await rag_service.generate_embedding(source_data['full_text'])
            
            # Create source record
            source = AcademicSource(
                title=source_data['title'],
                authors=source_data['authors'],
                publication_year=source_data['publication_year'],
                abstract=source_data['abstract'],
                full_text=source_data['full_text'],
                source_type=source_data['source_type'],
                embedding=embedding
            )
            
            db.add(source)
        
        db.commit()
        print(f"Successfully added {len(sample_sources)} academic sources to the database.")
        
    except Exception as e:
        print(f"Error populating academic sources: {str(e)}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("Initializing Academic Assignment Helper database...")
    
    # Create tables
    print("Creating database tables...")
    create_tables()
    
    # Initialize with sample data
    print("Initializing with sample data...")
    init_db()
    
    # Populate academic sources
    print("Populating academic sources...")
    asyncio.run(populate_academic_sources())
    
    print("Database initialization completed successfully!")
    print("\nSample student credentials:")
    print("Email: test@student.com")
    print("Password: password123")

if __name__ == "__main__":
    main()
