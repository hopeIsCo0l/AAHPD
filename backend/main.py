from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional
import uuid
import asyncio
import httpx
from sqlalchemy.orm import Session
from models import get_db, Student, Assignment, AnalysisResult
from auth import verify_token, get_current_student
from rag_service import RAGService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Academic Assignment Helper & Plagiarism Detector", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/assignment")

# Initialize RAG service
rag_service = RAGService()

# Database initialization function
def init_database():
    """Initialize database with tables and sample data"""
    try:
        from models import create_tables, init_db, engine
        from sqlalchemy import text
        
        logger.info("Initializing database...")
        
        # Check if tables exist
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'students'
                );
            """))
            tables_exist = result.scalar()
            
        if not tables_exist:
            logger.info("Creating database tables...")
            create_tables()
            logger.info("Tables created successfully!")
        else:
            logger.info("Tables already exist, skipping creation...")
        
        # Initialize sample data
        init_db()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise e

# Mount static files
app.mount("/static", StaticFiles(directory="web_interface"), name="static")

# Root endpoint - serve the web interface
@app.get("/")
async def read_root():
    """Serve the main web interface"""
    return FileResponse("web_interface/index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Academic Assignment Helper API is running"}

# Database status endpoint
@app.get("/db-status")
async def database_status():
    """Check database status and tables"""
    try:
        from models import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Check if students table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'students'
                );
            """))
            students_exists = result.scalar()
            
            # List all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            return {
                "status": "success",
                "students_table_exists": students_exists,
                "all_tables": tables,
                "database_url": os.getenv("DATABASE_URL", "Not set")
            }
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        return {"status": "error", "message": f"Database status check failed: {str(e)}"}

# Database initialization endpoint
@app.post("/init-db")
async def init_database_endpoint():
    """Initialize database tables and sample data"""
    try:
        init_database()
        return {"status": "success", "message": "Database initialized successfully!"}
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return {"status": "error", "message": f"Database initialization failed: {str(e)}"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()

@app.post("/auth/register")
async def register_student(
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    student_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Register a new student account"""
    # Check if student already exists
    existing_student = db.query(Student).filter(Student.email == email).first()
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new student (in production, hash the password)
    student = Student(
        email=email,
        password_hash=password,  # In production, use proper password hashing
        full_name=full_name,
        student_id=student_id
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return {"message": "Student registered successfully", "student_id": student.id}

@app.post("/auth/login")
async def login_student(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Login student and return JWT token"""
    student = db.query(Student).filter(Student.email == email).first()
    
    if not student or student.password_hash != password:  # In production, verify hashed password
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {
            "sub": str(student.id),
            "email": student.email,
            "exp": datetime.utcnow() + access_token_expires
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": student.id,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/upload")
async def upload_assignment(
    file: UploadFile = File(...),
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Upload assignment file and trigger n8n analysis"""
    
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and Word documents are allowed"
        )
    
    # Create assignment record first
    assignment = Assignment(
        student_id=current_student.id,
        filename=file.filename,
        original_text="",  # Will be filled by processing
        topic="",  # Will be filled by processing
        academic_level="",  # Will be filled by processing
        word_count=0  # Will be filled by processing
    )
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    
    # Save file locally with assignment ID for easier processing
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
    file_path = f"uploads/{assignment.id}.{file_extension}"
    
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Process assignment directly (simplified version)
    try:
        # Run the processing script directly
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "process_assignment.py", str(assignment.id)
        ], capture_output=True, text=True, cwd="/app")
        
        if result.returncode == 0:
            logger.info(f"Successfully processed assignment {assignment.id}")
        else:
            logger.error(f"Failed to process assignment {assignment.id}: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Failed to process assignment: {str(e)}")
        # Don't fail the upload if processing fails, just log the error
    
    return {
        "message": "Assignment uploaded successfully",
        "assignment_id": assignment.id,
        "analysis_job_id": assignment.id  # Using assignment ID as job ID
    }

@app.get("/analysis/{assignment_id}")
async def get_analysis(
    assignment_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve analysis results for an assignment"""
    
    # Verify assignment belongs to current student
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id,
        Assignment.student_id == current_student.id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )
    
    # Get analysis results
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.assignment_id == assignment_id
    ).first()
    
    if not analysis:
        return {
            "assignment_id": assignment_id,
            "status": "processing",
            "message": "Analysis is still in progress"
        }
    
    return {
        "assignment_id": assignment_id,
        "filename": assignment.filename,
        "topic": assignment.topic,
        "academic_level": assignment.academic_level,
        "word_count": assignment.word_count,
        "analysis": {
            "suggested_sources": analysis.suggested_sources,
            "plagiarism_score": analysis.plagiarism_score,
            "flagged_sections": analysis.flagged_sections,
            "research_suggestions": analysis.research_suggestions,
            "citation_recommendations": analysis.citation_recommendations,
            "confidence_score": analysis.confidence_score,
            "analyzed_at": analysis.analyzed_at
        }
    }

@app.get("/sources")
async def search_sources(
    query: str,
    limit: int = 10,
    current_student: Student = Depends(get_current_student)
):
    """Search academic sources using RAG"""
    
    try:
        sources = await rag_service.search_sources(query, limit)
        return {
            "query": query,
            "sources": sources,
            "total_found": len(sources)
        }
    except Exception as e:
        logger.error(f"Error searching sources: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error searching academic sources"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
