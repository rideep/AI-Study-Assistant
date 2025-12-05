import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
import os

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_path: str, clean_text: bool = False) -> Dict[str, Any]:
        """
        Extract text from PDF with metadata.
        Only extracts text from PDFs with text layers (not image-based PDFs).
        
        Args:
            pdf_path: Path to PDF file
            clean_text: If True, apply text cleaning preprocessing
            
        Returns:
            Dictionary with text, metadata, and page information
        """
        # Validate file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not os.path.isfile(pdf_path):
            raise ValueError(f"Path is not a file: {pdf_path}")
        
        try:
            with fitz.open(pdf_path) as doc:
                # Extract metadata
                metadata = {
                    'filename': os.path.basename(pdf_path),
                    'num_pages': len(doc),
                    'title': doc.metadata.get('title', '')
                }
                
                # Extract text page by page
                pages = []
                full_text = []
                
                for page_num, page in enumerate(doc, start=1):
                    # Try direct text extraction
                    text = page.get_text("text")
                    
                    # Fallback to block extraction if no text found
                    if not text or not text.strip():
                        blocks = page.get_text("blocks")
                        if blocks:
                            text = "\n".join([block[4] for block in blocks if block[4].strip()])
                    
                    # Clean text if requested
                    if clean_text and text:
                        text = self._clean_text(text)
                    
                    # Only add non-empty pages
                    if text and text.strip():
                        pages.append({
                            'page_number': page_num,
                            'text': text,
                            'char_count': len(text)
                        })
                        full_text.append(text)
                
                return {
                    'metadata': metadata,
                    'pages': pages,
                    'full_text': '\n\n'.join(full_text),
                    'total_chars': sum(p['char_count'] for p in pages)
                }
            
        except FileNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers (simple pattern)
        text = re.sub(r'\b\d+\b\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common header/footer patterns
        text = re.sub(r'^Page \d+.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Fix common issues
        text = text.replace('�', '')  # Remove replacement characters
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
        
        return text.strip()
    
    def extract_text_by_sections(self, pdf_path: str) -> List[Dict]:
        """
        Attempt to extract text organized by sections/headings
        (More advanced - optional for MVP)
        """
        result = self.extract_text_from_pdf(pdf_path)
        
        # Simple section detection based on formatting cues
        sections = []
        current_section = {'title': 'Introduction', 'content': []}
        
        for page in result['pages']:
            lines = page['text'].split('\n')
            
            for line in lines:
                # Heuristic: Lines that are short and title-cased might be headings
                if self._is_likely_heading(line):
                    # Save previous section
                    if current_section['content']:
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'title': line.strip(),
                        'content': []
                    }
                else:
                    current_section['content'].append(line)
        
        # Add last section
        if current_section['content']:
            sections.append(current_section)
        
        # Convert sections to text
        for section in sections:
            section['text'] = '\n'.join(section['content'])
            del section['content']
        
        return sections
    
    def _is_likely_heading(self, line: str) -> bool:
        """
        Simple heuristic to detect if a line is likely a heading
        """
        line = line.strip()
        
        if not line:
            return False
        
        # Check conditions that suggest heading
        is_short = len(line) < 100
        is_title_case = line[0].isupper() if line else False
        has_few_words = len(line.split()) < 10
        ends_without_period = not line.endswith('.')
        
        return is_short and is_title_case and has_few_words and ends_without_period
    
    def get_pdf_stats(self, pdf_path: str) -> Dict:
        """
        Get quick statistics about a PDF without full processing
        """
        try:
            doc = fitz.open(pdf_path)
            stats = {
                'num_pages': len(doc),
                'file_size_mb': os.path.getsize(pdf_path) / (1024 * 1024),
                'title': doc.metadata.get('title', 'Untitled'),
            }
            doc.close()
            return stats
        except Exception as e:
            return {'error': str(e)}

    def batch_process_pdfs(self, pdf_paths: List[str]) -> List[Dict]:
        """
        Process multiple PDFs
        """
        results = []
        
        for pdf_path in pdf_paths:
            try:
                result = self.extract_text_from_pdf(pdf_path)
                result['status'] = 'success'
                results.append(result)
            except Exception as e:
                results.append({
                    'metadata': {'filename': os.path.basename(pdf_path)},
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results