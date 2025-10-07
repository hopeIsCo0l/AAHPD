#!/usr/bin/env python3
"""
Direct assignment processing without n8n
This processes assignments immediately when uploaded
"""

import asyncio
import json
import os
from sqlalchemy.orm import Session
from models import get_db, Assignment, AnalysisResult
from rag_service import RAGService
from text_extractor import TextExtractor
import logging

logger = logging.getLogger(__name__)

async def process_assignment_directly(assignment_id: int):
    """Process assignment directly without n8n workflow"""
    print(f"Processing assignment {assignment_id}...")
    
    db = next(get_db())
    try:
        # Get the assignment
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            print(f"Assignment {assignment_id} not found")
            return
        
        # Initialize RAG service
        rag_service = RAGService()
        
        # Extract real text from the uploaded file
        file_path = f"uploads/{assignment_id}.{assignment.filename.split('.')[-1]}"
        extracted_text = TextExtractor.extract_text_from_file(file_path)
        
        if not extracted_text:
            # Fallback to simulated text if extraction fails
            extracted_text = f"Text extraction failed for assignment: {assignment.filename}. Using simulated analysis."
            logger.warning(f"Text extraction failed for assignment {assignment_id}")
        
        # Clean the extracted text
        cleaned_text = TextExtractor.clean_text(extracted_text)
        
        # Analyze content with real text
        analysis = await rag_service.analyze_assignment_content(cleaned_text)
        
        # Detect plagiarism with real text
        plagiarism = await rag_service.detect_plagiarism(cleaned_text)
        
        # Search for relevant sources based on real content
        search_query = analysis.get("topic", "academic research")
        if not search_query or search_query == "Sample Topic":
            # Extract keywords from the actual text for better search
            words = cleaned_text.split()[:10]  # First 10 words as keywords
            search_query = " ".join(words)
        
        sources = await rag_service.search_sources(search_query, limit=5)
        
        # Update assignment with real analysis results
        assignment.original_text = cleaned_text
        assignment.topic = analysis.get("topic", "General Topic")
        assignment.academic_level = analysis.get("academic_level", "Undergraduate")
        assignment.word_count = TextExtractor.get_word_count(cleaned_text)
        
        # Create analysis result
        analysis_result = AnalysisResult(
            assignment_id=assignment_id,
            suggested_sources=sources,
            plagiarism_score=plagiarism.get("plagiarism_score", 0.0),
            flagged_sections=plagiarism.get("flagged_sections", []),
            research_suggestions=f"Based on the content analysis, consider exploring related academic literature on '{analysis.get('topic', 'General Topic')}'. The assignment contains {assignment.word_count} words and covers key themes that would benefit from additional scholarly sources.",
            citation_recommendations="Use APA format for citations. Ensure all sources are properly cited and referenced.",
            confidence_score=0.85
        )
        
        db.add(analysis_result)
        db.commit()
        
        print(f"✅ Analysis completed for assignment {assignment_id}")
        print(f"   File: {assignment.filename}")
        print(f"   Text Length: {len(cleaned_text)} characters")
        print(f"   Word Count: {assignment.word_count}")
        print(f"   Topic: {assignment.topic}")
        print(f"   Academic Level: {assignment.academic_level}")
        print(f"   Plagiarism Score: {analysis_result.plagiarism_score}")
        print(f"   Sources Found: {len(sources)}")
        
    except Exception as e:
        logger.error(f"Error processing assignment {assignment_id}: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        assignment_id = int(sys.argv[1])
        asyncio.run(process_assignment_directly(assignment_id))
    else:
        print("Usage: python process_assignment.py <assignment_id>")
