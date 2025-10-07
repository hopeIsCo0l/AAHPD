"""
Real-time text extraction from various file formats
"""

import os
import PyPDF2
import docx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TextExtractor:
    """Extract text from various document formats"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                logger.info(f"Successfully extracted {len(text)} characters from PDF")
                return text.strip()
                
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text from Word document"""
        try:
            doc = docx.Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            logger.info(f"Successfully extracted {len(text)} characters from DOCX")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_file(file_path: str) -> Optional[str]:
        """Extract text from file based on extension"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return TextExtractor.extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return TextExtractor.extract_text_from_docx(file_path)
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            return None
    
    @staticmethod
    def get_word_count(text: str) -> int:
        """Count words in text"""
        if not text:
            return 0
        return len(text.split())
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            cleaned_line = line.strip()
            if cleaned_line:  # Only add non-empty lines
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
