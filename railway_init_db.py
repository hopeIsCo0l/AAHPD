#!/usr/bin/env python3
"""
Railway Database Initialization Script
This script initializes the database with tables and sample data for Railway deployment.
"""

import os
import sys
import json
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from datetime import datetime
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from Railway environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set")
    sys.exit(1)

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    logger.info("Creating database tables...")
    
    # Enable pgvector extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    
    # Create tables using SQL
    create_tables_sql = """
    -- Create students table
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL,
        password_hash VARCHAR NOT NULL,
        full_name VARCHAR NOT NULL,
        student_id VARCHAR UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create assignments table
    CREATE TABLE IF NOT EXISTS assignments (
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(id) NOT NULL,
        filename VARCHAR NOT NULL,
        original_text TEXT,
        topic VARCHAR,
        academic_level VARCHAR,
        word_count INTEGER DEFAULT 0,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create analysis_results table
    CREATE TABLE IF NOT EXISTS analysis_results (
        id SERIAL PRIMARY KEY,
        assignment_id INTEGER REFERENCES assignments(id) NOT NULL,
        suggested_sources JSONB,
        plagiarism_score FLOAT,
        flagged_sections JSONB,
        research_suggestions TEXT,
        citation_recommendations TEXT,
        confidence_score FLOAT,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create academic_sources table
    CREATE TABLE IF NOT EXISTS academic_sources (
        id SERIAL PRIMARY KEY,
        title VARCHAR NOT NULL,
        authors VARCHAR NOT NULL,
        publication_year INTEGER,
        abstract TEXT,
        full_text TEXT,
        source_type VARCHAR NOT NULL,
        embedding VECTOR(1536),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
    CREATE INDEX IF NOT EXISTS idx_assignments_student_id ON assignments(student_id);
    CREATE INDEX IF NOT EXISTS idx_analysis_results_assignment_id ON analysis_results(assignment_id);
    CREATE INDEX IF NOT EXISTS idx_academic_sources_source_type ON academic_sources(source_type);
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_tables_sql))
        conn.commit()
    
    logger.info("Database tables created successfully!")

def add_sample_data():
    """Add sample data to the database"""
    logger.info("Adding sample data...")
    
    db = SessionLocal()
    try:
        # Add sample student
        sample_student_sql = """
        INSERT INTO students (email, password_hash, full_name, student_id)
        VALUES ('test@student.com', 'password123', 'Test Student', 'STU001')
        ON CONFLICT (email) DO NOTHING;
        """
        
        with engine.connect() as conn:
            conn.execute(text(sample_student_sql))
            conn.commit()
        
        logger.info("Sample student added: test@student.com / password123")
        
        # Add sample academic sources
        sample_sources = [
            {
                "title": "The Impact of Artificial Intelligence on Education: A Comprehensive Review",
                "authors": "Dr. Sarah Johnson, Prof. Michael Chen, Dr. Emily Rodriguez",
                "publication_year": 2023,
                "abstract": "This comprehensive review examines the transformative effects of artificial intelligence on educational systems worldwide. We analyze current implementations, challenges, and future prospects of AI in learning environments.",
                "full_text": "Artificial Intelligence (AI) has emerged as a revolutionary force in education, transforming traditional learning paradigms and creating new opportunities for personalized, adaptive learning experiences. This paper presents a comprehensive analysis of AI's impact on educational systems, examining both the benefits and challenges associated with its implementation. Our research covers various AI applications including intelligent tutoring systems, automated assessment tools, and personalized learning platforms. We also discuss the ethical considerations and potential risks of AI in education, providing recommendations for responsible implementation. The findings suggest that while AI offers significant potential for improving educational outcomes, careful consideration must be given to issues of equity, privacy, and the role of human educators in an AI-enhanced learning environment.",
                "source_type": "paper"
            },
            {
                "title": "Machine Learning Applications in Academic Research: A Survey",
                "authors": "Dr. Robert Kim, Prof. Lisa Wang",
                "publication_year": 2022,
                "abstract": "This survey paper explores the diverse applications of machine learning techniques in academic research across various disciplines, highlighting successful implementations and emerging trends.",
                "full_text": "Machine learning has become an indispensable tool in academic research, enabling researchers to analyze complex datasets, identify patterns, and make predictions across a wide range of disciplines. This comprehensive survey examines the applications of machine learning in academic research, covering areas such as natural language processing, computer vision, data mining, and predictive analytics. We present case studies from various fields including medicine, social sciences, engineering, and humanities, demonstrating the versatility and effectiveness of machine learning approaches. The paper also discusses challenges such as data quality, model interpretability, and computational requirements, providing practical guidance for researchers considering machine learning applications in their work.",
                "source_type": "paper"
            },
            {
                "title": "Digital Literacy in Higher Education: Challenges and Opportunities",
                "authors": "Dr. Amanda Thompson, Prof. David Lee",
                "publication_year": 2023,
                "abstract": "This study investigates the current state of digital literacy among university students and faculty, identifying key challenges and proposing strategies for improvement.",
                "full_text": "Digital literacy has become a critical skill in higher education, yet many institutions struggle to adequately prepare students and faculty for the digital demands of modern academia. This research examines the current state of digital literacy in higher education institutions, identifying gaps in knowledge and skills among both students and faculty members. Through surveys and interviews conducted across multiple universities, we found that while most students are comfortable with basic digital tools, many lack advanced skills in areas such as data analysis, online collaboration, and digital research methods. The study proposes a comprehensive framework for improving digital literacy that includes curriculum integration, faculty development programs, and student support services. Our recommendations focus on practical, implementable strategies that can be adapted to different institutional contexts.",
                "source_type": "paper"
            },
            {
                "title": "Introduction to Academic Writing and Research Methods",
                "authors": "Dr. Jennifer Martinez, Prof. Thomas Brown",
                "publication_year": 2022,
                "abstract": "A comprehensive textbook covering fundamental principles of academic writing, research methodology, and scholarly communication for undergraduate students.",
                "full_text": "Academic writing and research methods form the foundation of scholarly communication and critical thinking in higher education. This comprehensive textbook provides students with essential skills for conducting research, analyzing sources, and presenting findings in a clear, persuasive manner. The book covers topics including research design, literature review techniques, data collection methods, citation styles, and ethical considerations in research. Each chapter includes practical exercises, examples from various disciplines, and guidance for avoiding common pitfalls in academic writing. The text emphasizes the importance of critical thinking, evidence-based argumentation, and proper attribution of sources. This resource is designed for undergraduate students across all disciplines who are beginning their academic research journey.",
                "source_type": "textbook"
            },
            {
                "title": "Plagiarism Detection and Prevention in Academic Settings",
                "authors": "Dr. Patricia Wilson, Prof. James Taylor",
                "publication_year": 2023,
                "abstract": "This study examines current methods for detecting and preventing plagiarism in academic institutions, evaluating the effectiveness of various tools and strategies.",
                "full_text": "Plagiarism remains a significant concern in academic institutions, threatening the integrity of scholarly work and student learning outcomes. This comprehensive study examines current methods for detecting and preventing plagiarism, evaluating the effectiveness of both technological tools and educational strategies. We analyze various plagiarism detection software, including text-matching algorithms, citation analysis tools, and AI-powered detection systems. The research also investigates the root causes of plagiarism, including lack of understanding of proper citation practices, time pressure, and inadequate academic support. Our findings suggest that a multi-faceted approach combining technological tools with educational interventions is most effective. We provide recommendations for institutions seeking to improve their plagiarism prevention strategies, including faculty training, student education programs, and policy development.",
                "source_type": "paper"
            }
        ]
        
        for source in sample_sources:
            insert_sql = """
            INSERT INTO academic_sources (title, authors, publication_year, abstract, full_text, source_type)
            VALUES (:title, :authors, :publication_year, :abstract, :full_text, :source_type)
            ON CONFLICT DO NOTHING;
            """
            
            with engine.connect() as conn:
                conn.execute(text(insert_sql), source)
                conn.commit()
        
        logger.info(f"Added {len(sample_sources)} sample academic sources")
        
    except Exception as e:
        logger.error(f"Error adding sample data: {e}")
        raise
    finally:
        db.close()

def main():
    """Main initialization function"""
    logger.info("Starting Railway database initialization...")
    
    try:
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
        
        # Create tables
        create_tables()
        
        # Add sample data
        add_sample_data()
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
