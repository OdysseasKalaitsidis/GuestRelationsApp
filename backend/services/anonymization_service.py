# services/anonymization_service.py
import re
import spacy
from typing import Dict, List, Any, Optional
from fastapi import UploadFile
from io import BytesIO
from docx import Document
import pdfplumber

# Load spaCy model for named entity recognition
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model not available
    nlp = None

class AnonymizationService:
    """Enhanced anonymization service for documents"""
    
    def __init__(self):
        # Common patterns for PII detection
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\+?[\d\s\-\(\)]{7,}',
            'booking_ref': r'\b(?:REF|#|Booking|Reservation)[\s\-]?\d+[A-Za-z0-9]*\b',
            'credit_card': r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
            'passport': r'\b[A-Z]{1,2}\d{6,9}\b',
            'ssn': r'\b\d{3}[\-]?\d{2}[\-]?\d{4}\b',
            'date': r'\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b',
            'time': r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b',
            'address': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
            'postal_code': r'\b[A-Z]{1,2}\d[A-Z]\s?\d[A-Z]\d\b',  # UK format
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
        }
        
        # Custom replacement tokens
        self.replacements = {
            'email': '[EMAIL]',
            'phone': '[PHONE]',
            'booking_ref': '[BOOKING_REF]',
            'credit_card': '[CREDIT_CARD]',
            'passport': '[PASSPORT]',
            'ssn': '[SSN]',
            'date': '[DATE]',
            'time': '[TIME]',
            'address': '[ADDRESS]',
            'postal_code': '[POSTAL_CODE]',
            'ip_address': '[IP_ADDRESS]',
            'url': '[URL]',
            'name': '[NAME]',
            'company': '[COMPANY]',
            'location': '[LOCATION]'
        }
    
    def anonymize_text(self, text: str, preserve_dates: bool = False, preserve_times: bool = False) -> str:
        """
        Anonymize text content with configurable options
        
        Args:
            text: Input text to anonymize
            preserve_dates: Whether to preserve date information
            preserve_times: Whether to preserve time information
        
        Returns:
            Anonymized text
        """
        if not text:
            return text
            
        anonymized_text = text
        
        # Apply pattern-based anonymization
        for pattern_name, pattern in self.patterns.items():
            if pattern_name == 'date' and preserve_dates:
                continue
            if pattern_name == 'time' and preserve_times:
                continue
                
            replacement = self.replacements.get(pattern_name, f'[{pattern_name.upper()}]')
            anonymized_text = re.sub(pattern, replacement, anonymized_text, flags=re.IGNORECASE)
        
        # Use spaCy for named entity recognition if available
        if nlp:
            doc = nlp(anonymized_text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    anonymized_text = anonymized_text.replace(ent.text, self.replacements['name'])
                elif ent.label_ == "ORG":
                    anonymized_text = anonymized_text.replace(ent.text, self.replacements['company'])
                elif ent.label_ in ["GPE", "LOC"]:
                    anonymized_text = anonymized_text.replace(ent.text, self.replacements['location'])
        
        # Additional custom patterns for hotel-specific data
        hotel_patterns = {
            'room_number': r'\b(?:Room|Rm)\s*[#]?\s*(\d+)\b',
            'guest_id': r'\b(?:Guest|Customer)\s*ID\s*[#]?\s*(\d+)\b',
            'reservation_id': r'\b(?:Reservation|Booking)\s*ID\s*[#]?\s*(\d+)\b',
            'check_in': r'\b(?:Check[-\s]?in|Arrival)\s*:\s*([^\n]+)\b',
            'check_out': r'\b(?:Check[-\s]?out|Departure)\s*:\s*([^\n]+)\b',
        }
        
        for pattern_name, pattern in hotel_patterns.items():
            replacement = f'[{pattern_name.upper().replace("_", " ")}]'
            anonymized_text = re.sub(pattern, replacement, anonymized_text, flags=re.IGNORECASE)
        
        return anonymized_text
    
    def anonymize_document(self, file: UploadFile, preserve_dates: bool = False, preserve_times: bool = False) -> Dict[str, Any]:
        """
        Anonymize an entire document (PDF or DOCX)
        
        Args:
            file: Uploaded file to anonymize
            preserve_dates: Whether to preserve date information
            preserve_times: Whether to preserve time information
        
        Returns:
            Dictionary containing original and anonymized content
        """
        try:
            if file.filename.lower().endswith('.docx'):
                return self._anonymize_docx(file, preserve_dates, preserve_times)
            elif file.filename.lower().endswith('.pdf'):
                return self._anonymize_pdf(file, preserve_dates, preserve_times)
            else:
                raise ValueError(f"Unsupported file type: {file.filename}")
        except Exception as e:
            raise Exception(f"Error anonymizing document: {str(e)}")
    
    def _anonymize_docx(self, file: UploadFile, preserve_dates: bool, preserve_times: bool) -> Dict[str, Any]:
        """Anonymize DOCX document"""
        docx_bytes = BytesIO(file.file.read())
        doc = Document(docx_bytes)
        
        original_content = []
        anonymized_content = []
        
        # Process paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                original_content.append(paragraph.text)
                anonymized_text = self.anonymize_text(paragraph.text, preserve_dates, preserve_times)
                anonymized_content.append(anonymized_text)
        
        # Process tables
        for table in doc.tables:
            table_data = []
            anonymized_table_data = []
            
            for row in table.rows:
                row_data = []
                anonymized_row_data = []
                
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                    anonymized_cell_text = self.anonymize_text(cell_text, preserve_dates, preserve_times)
                    anonymized_row_data.append(anonymized_cell_text)
                
                table_data.append(row_data)
                anonymized_table_data.append(anonymized_row_data)
            
            original_content.append(f"TABLE: {table_data}")
            anonymized_content.append(f"TABLE: {anonymized_table_data}")
        
        return {
            "filename": file.filename,
            "file_type": "docx",
            "original_content": original_content,
            "anonymized_content": anonymized_content,
            "anonymization_summary": self._generate_summary(original_content, anonymized_content)
        }
    
    def _anonymize_pdf(self, file: UploadFile, preserve_dates: bool, preserve_times: bool) -> Dict[str, Any]:
        """Anonymize PDF document"""
        pdf_bytes = BytesIO(file.file.read())
        
        original_content = []
        anonymized_content = []
        
        with pdfplumber.open(pdf_bytes) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    original_content.append(f"Page {page_num + 1}: {page_text}")
                    anonymized_text = self.anonymize_text(page_text, preserve_dates, preserve_times)
                    anonymized_content.append(f"Page {page_num + 1}: {anonymized_text}")
        
        return {
            "filename": file.filename,
            "file_type": "pdf",
            "original_content": original_content,
            "anonymized_content": anonymized_content,
            "anonymization_summary": self._generate_summary(original_content, anonymized_content)
        }
    
    def _generate_summary(self, original_content: List[str], anonymized_content: List[str]) -> Dict[str, Any]:
        """Generate anonymization summary"""
        original_text = " ".join(original_content)
        anonymized_text = " ".join(anonymized_content)
        
        # Count replacements
        replacements = {}
        for pattern_name, replacement in self.replacements.items():
            count = anonymized_text.count(replacement)
            if count > 0:
                replacements[pattern_name] = count
        
        return {
            "total_replacements": sum(replacements.values()),
            "replacement_breakdown": replacements,
            "anonymization_ratio": len([c for c in anonymized_text if c == '[']) / len(anonymized_text) if anonymized_text else 0
        }
    
    def get_anonymization_stats(self, text: str) -> Dict[str, Any]:
        """Get statistics about what would be anonymized in a text"""
        if not text:
            return {"total_potential_pii": 0, "breakdown": {}}
        
        stats = {}
        total_count = 0
        
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            count = len(matches)
            if count > 0:
                stats[pattern_name] = {
                    "count": count,
                    "examples": matches[:3]  # Show first 3 examples
                }
                total_count += count
        
        return {
            "total_potential_pii": total_count,
            "breakdown": stats
        }

# Create a global instance
anonymization_service = AnonymizationService()
