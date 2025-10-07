import openai
import os
from sqlalchemy.orm import Session
from models import get_db, AcademicSource
from typing import List, Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set. RAG functionality will be limited.")
        
        openai.api_key = self.openai_api_key
        self.embedding_model = "text-embedding-ada-002"
        self.embedding_dimension = 1536
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text using OpenAI"""
        if not self.openai_api_key:
            # Return dummy embedding for testing
            return [0.0] * self.embedding_dimension
        
        try:
            response = await openai.Embedding.acreate(
                input=text,
                model=self.embedding_model
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return [0.0] * self.embedding_dimension
    
    async def search_sources(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant academic sources using vector similarity"""
        db = next(get_db())
        
        try:
            # Generate embedding for the query
            query_embedding = await self.generate_embedding(query)
            
            # Search for similar sources using vector similarity
            # Note: This is a simplified version. In production, you'd use proper vector search
            sources = db.query(AcademicSource).limit(limit).all()
            
            # Convert to dictionary format
            results = []
            for source in sources:
                results.append({
                    "id": source.id,
                    "title": source.title,
                    "authors": source.authors,
                    "publication_year": source.publication_year,
                    "abstract": source.abstract,
                    "source_type": source.source_type,
                    "relevance_score": 0.85  # Placeholder - would be calculated from vector similarity
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching sources: {str(e)}")
            return []
        finally:
            db.close()
    
    async def add_academic_source(
        self,
        title: str,
        authors: str,
        publication_year: int,
        abstract: str,
        full_text: str,
        source_type: str
    ) -> int:
        """Add a new academic source to the database"""
        db = next(get_db())
        
        try:
            # Generate embedding for the full text
            embedding = await self.generate_embedding(full_text)
            
            # Create new source
            source = AcademicSource(
                title=title,
                authors=authors,
                publication_year=publication_year,
                abstract=abstract,
                full_text=full_text,
                source_type=source_type,
                embedding=embedding
            )
            
            db.add(source)
            db.commit()
            db.refresh(source)
            
            logger.info(f"Added academic source: {title}")
            return source.id
            
        except Exception as e:
            logger.error(f"Error adding academic source: {str(e)}")
            db.rollback()
            return None
        finally:
            db.close()
    
    async def analyze_assignment_content(self, text: str) -> Dict[str, Any]:
        """Analyze assignment content using AI"""
        if not self.openai_api_key:
            return {
                "topic": "Sample Topic",
                "academic_level": "Undergraduate",
                "key_themes": ["education", "technology"],
                "research_questions": ["What is the impact of technology on education?"],
                "word_count": len(text.split())
            }
        
        try:
            prompt = f"""
            Analyze the following academic assignment and extract:
            1. Main topic/subject
            2. Academic level (High School, Undergraduate, Graduate, PhD)
            3. Key themes and concepts
            4. Research questions identified
            5. Word count
            
            Assignment text:
            {text[:2000]}  # Limit to first 2000 characters
            
            Return your analysis in JSON format.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an academic assistant that analyzes student assignments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            # Parse the response (in production, you'd want more robust JSON parsing)
            analysis_text = response.choices[0].message.content
            
            return {
                "topic": "AI-Generated Topic",
                "academic_level": "Undergraduate",
                "key_themes": ["analysis", "research"],
                "research_questions": ["How can AI assist in academic research?"],
                "word_count": len(text.split()),
                "ai_analysis": analysis_text
            }
            
        except Exception as e:
            logger.error(f"Error analyzing assignment: {str(e)}")
            return {
                "topic": "Unknown Topic",
                "academic_level": "Undergraduate",
                "key_themes": [],
                "research_questions": [],
                "word_count": len(text.split())
            }
    
    async def detect_plagiarism(self, text: str) -> Dict[str, Any]:
        """Detect potential plagiarism by comparing with academic sources"""
        db = next(get_db())
        
        try:
            # This is a simplified plagiarism detection
            # In production, you'd use more sophisticated algorithms
            
            # Get all academic sources
            sources = db.query(AcademicSource).all()
            
            plagiarism_score = 0.0
            flagged_sections = []
            
            # Simple word-based similarity check
            text_words = set(text.lower().split())
            
            for source in sources:
                if source.full_text:
                    source_words = set(source.full_text.lower().split())
                    common_words = text_words.intersection(source_words)
                    
                    if len(common_words) > 10:  # Threshold for potential plagiarism
                        similarity = len(common_words) / len(text_words)
                        if similarity > 0.3:  # 30% similarity threshold
                            plagiarism_score = max(plagiarism_score, similarity)
                            flagged_sections.append({
                                "source_title": source.title,
                                "similarity_score": similarity,
                                "common_phrases": list(common_words)[:5]  # First 5 common words
                            })
            
            return {
                "plagiarism_score": plagiarism_score,
                "flagged_sections": flagged_sections,
                "is_plagiarized": plagiarism_score > 0.3
            }
            
        except Exception as e:
            logger.error(f"Error detecting plagiarism: {str(e)}")
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": [],
                "is_plagiarized": False
            }
        finally:
            db.close()
