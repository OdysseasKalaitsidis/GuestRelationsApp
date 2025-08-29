# services/document_service.py
import re
import pdfplumber
import spacy
from fastapi import UploadFile
from io import BytesIO
from docx import Document
from typing import List, Dict, Optional
import zipfile
import xml.etree.ElementTree as ET

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text from PDF using pdfplumber without temp files"""
    pdf_bytes = BytesIO(file.file.read())
    text = ""
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    """
    Extract text from DOCX using direct XML parsing to handle complex table structures
    """
    docx_bytes = BytesIO(file.file.read())
    
    try:
        # Method 1: Direct XML parsing with better table handling
        with zipfile.ZipFile(docx_bytes, 'r') as zip_file:
            if 'word/document.xml' in zip_file.namelist():
                doc_xml = zip_file.read('word/document.xml')
                root = ET.fromstring(doc_xml)
                
                # Extract text with better structure preservation
                text_parts = []
                
                # Process paragraphs first
                paragraphs = root.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                for para in paragraphs:
                    para_text = ""
                    text_elements = para.findall('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                    if text_elements:
                        para_text = ' '.join([elem.text for elem in text_elements if elem.text])
                        if para_text.strip():
                            text_parts.append(para_text.strip())
                
                # Process tables with better structure
                tables = root.findall('.//w:tbl', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                for table in tables:
                    table_text = []
                    rows = table.findall('.//w:tr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                    
                    for row in rows:
                        row_text = []
                        cells = row.findall('.//w:tc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                        
                        for cell in cells:
                            cell_text_elements = cell.findall('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                            cell_text = ' '.join([elem.text for elem in cell_text_elements if elem.text])
                            if cell_text.strip():
                                row_text.append(cell_text.strip())
                        
                        if row_text:
                            table_text.append(' | '.join(row_text))
                    
                    if table_text:
                        text_parts.extend(table_text)
                
                # Combine all text with proper spacing
                all_text = '\n'.join(text_parts)
                
                if len(all_text.strip()) > 100:  # If we got substantial text, use it
                    return all_text
        
        # Method 2: Fallback to python-docx
        docx_bytes.seek(0)  # Reset file pointer
        doc = Document(docx_bytes)
        text = ""
        
        # Extract text from paragraphs
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join([cell.text.strip() for cell in row.cells])
                text += row_text + "\n"
        
        return text
        
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        # Method 3: Last resort - try to read as bytes and decode
        try:
            docx_bytes.seek(0)
            content = docx_bytes.read()
            # Look for readable text in the content
            text = ""
            for i in range(0, len(content), 2):
                try:
                    char = content[i:i+2].decode('utf-16-le', errors='ignore')
                    if char.isprintable():
                        text += char
                except:
                    continue
            return text
        except:
            raise ValueError(f"Failed to extract text from DOCX file: {str(e)}")

def anonymise_text(text: str) -> str:
    """Remove PII (names, emails, phones, booking refs) but preserve field labels and important names"""
    # First, let's extract guest names before anonymizing
    guest_names = []
    guest_pattern = r'Guest\s+([^\n\r]+)'
    guest_matches = re.findall(guest_pattern, text)
    guest_names = [name.strip() for name in guest_matches if name.strip()]
    
    # Also preserve staff names (created by, modified by) as they're useful for case management
    staff_names = []
    staff_patterns = [
        r'Created by\s+([^\n\r]+)',
        r'Modified by\s+([^\n\r]+)'
    ]
    for pattern in staff_patterns:
        matches = re.findall(pattern, text)
        staff_names.extend([name.strip() for name in matches if name.strip()])
    
    # Define important values that should NEVER be anonymized
    important_values = [
        'CLOSED', 'OPEN', 'PENDING', 'RESOLVED',
        'NEGATIVE', 'POSITIVE', 'NEUTRAL',
        'LOW', 'MEDIUM', 'HIGH',
        'CASE', 'ACTION', 'IN/OUT'
    ]
    
    # Now anonymize the text more selectively - preserve field labels and important names
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG']:
            # Don't anonymize if it's a guest name, staff name, or important value
            if (ent.text not in guest_names and 
                ent.text not in staff_names and 
                ent.text not in important_values):
                # Also don't anonymize field labels like "Guest", "Status", "Room", etc.
                field_labels = ['Guest', 'Status', 'Room', 'Importance', 'Type', 'Source', 'Membership', 'CASE', 'ACTION', 'IN/OUT', 'Created', 'Modified', 'Created by', 'Modified by']
                if ent.text not in field_labels:
                    text = text.replace(ent.text, "[NAME]")
    
    return text

def parse_cases(text: str, status_type_info: dict = None) -> list:
    """Convert text into structured list of case dicts - updated for table format"""
    cases = []
    
    # Split text into potential case blocks - improved splitting logic
    # Look for multiple patterns that indicate case boundaries
    case_blocks = re.split(r'(?=Created\s+\d{2}/\d{2}/\d{4})', text)
    
    # If we only got one block, try alternative splitting methods
    if len(case_blocks) <= 1:
        print("DEBUG: Single block detected, trying alternative splitting...")
        # Try splitting by other patterns that might indicate case boundaries
        case_blocks = re.split(r'(?=Guest\s+[A-Z][a-z]+)', text)
        
        if len(case_blocks) <= 1:
            # Try splitting by room numbers
            case_blocks = re.split(r'(?=Room\s+\d+)', text)
    
    print(f"DEBUG: Found {len(case_blocks)} potential case blocks")
    
    case_index = 0
    for i, block in enumerate(case_blocks):
        block = block.strip()
        if not block or len(block) < 50:  # Skip very short blocks
            continue
            
        print(f"DEBUG: Processing block {i+1}, length: {len(block)}")
        print(f"DEBUG: Block content: {block[:200]}...")
        
        # Extract case information using improved regex patterns
        # Look for Created date in multiple formats - the issue might be that "Created" is on a separate line
        created_match = re.search(r'Created\s*\n\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', block)
        if not created_match:
            # Try alternative format with dot separator
            created_match = re.search(r'Created\s*\n\s*(\d{2}\.\d{2}\.\d{4})', block)
        if not created_match:
            # Try without newline
            created_match = re.search(r'Created\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', block)
        if not created_match:
            # Try with dot separator without newline
            created_match = re.search(r'Created\s+(\d{2}\.\d{2}\.\d{4})', block)
        
        guest_match = re.search(r'Guest\s*\n\s*([^\n\r]+)', block)
        if not guest_match:
            guest_match = re.search(r'Guest\s+([^\n\r]+)', block)
            
        # Use pre-extracted status and type information
        status_value = None
        type_value = None
        if status_type_info:
            status_key = f'status_{case_index}'
            type_key = f'type_{case_index}'
            if status_key in status_type_info:
                status_value = status_type_info[status_key]
            if type_key in status_type_info:
                type_value = status_type_info[type_key]
        
        # Fallback to regex extraction if pre-extracted info not available
        if not status_value:
            status_match = re.search(r'Status\s*\n\s*(\w+)', block)
            if not status_match:
                status_match = re.search(r'Status\s+(\w+)', block)
            if status_match:
                status_value = status_match.group(1)
        
        if not type_value:
            case_type_match = re.search(r'Type\s*\n\s*(\w+)', block)
            if not case_type_match:
                case_type_match = re.search(r'Type\s+(\w+)', block)
            if case_type_match:
                type_value = case_type_match.group(1)
            
        created_by_match = re.search(r'Created by\s*\n\s*([^\n\r]+)', block)
        if not created_by_match:
            created_by_match = re.search(r'Created by\s+([^\n\r]+)', block)
            
        room_match = re.search(r'Room\s*\n\s*(\d+)', block)
        if not room_match:
            room_match = re.search(r'Room\s+(\d+)', block)
            
        importance_match = re.search(r'Importance\s*\n\s*(\w+)', block)
        if not importance_match:
            importance_match = re.search(r'Importance\s+(\w+)', block)
            
        modified_match = re.search(r'Modified\s*\n\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', block)
        if not modified_match:
            modified_match = re.search(r'Modified\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', block)
            
        modified_by_match = re.search(r'Modified by\s*\n\s*([^\n\r]+)', block)
        if not modified_by_match:
            modified_by_match = re.search(r'Modified by\s+([^\n\r]+)', block)
            
        source_match = re.search(r'Source\s*\n\s*([^\n\r]+)', block)
        if not source_match:
            source_match = re.search(r'Source\s+([^\n\r]+)', block)
            
        membership_match = re.search(r'Membership\s*\n\s*([^\n\r]+)', block)
        if not membership_match:
            membership_match = re.search(r'Membership\s+([^\n\r]+)', block)
        
        # Extract case description and action with better patterns
        # Look for CASE followed by text until ACTION or end
        case_match = re.search(r'CASE\s+([^A-Z]+?)(?=\s+ACTION|$)', block, re.DOTALL | re.IGNORECASE)
        action_match = re.search(r'ACTION\s+(.+?)(?=\s+[A-Z]+|$)', block, re.DOTALL | re.IGNORECASE)
        
        # Also look for IN/OUT dates
        in_out_match = re.search(r'IN/OUT\s*\n\s*([^\n\r]+)', block)
        if not in_out_match:
            in_out_match = re.search(r'IN/OUT\s+([^\n\r]+)', block)
        
        # Create case object with guaranteed title and more fields
        guest_name = guest_match.group(1).strip() if guest_match else None
        room_number = room_match.group(1) if room_match else None
        
        # Clean up guest name - remove pipe-separated values that indicate malformed data
        if guest_name and '|' in guest_name:
            # Take only the first part before the pipe
            guest_name = guest_name.split('|')[0].strip()
        
        # Ensure we have a valid title - use guest name, room, or fallback
        if guest_name and len(guest_name) < 50:  # Avoid very long names that might be malformed
            title = guest_name
        elif room_number:
            title = f"Room {room_number} Case"
        else:
            title = "Untitled Case"
        
        case = {
            "created": created_match.group(1) if created_match else None,
            "guest": guest_name,
            "status": status_value,
            "created_by": created_by_match.group(1).strip() if created_by_match else None,
            "room": room_number,
            "importance": importance_match.group(1) if importance_match else None,
            "modified": modified_match.group(1) if modified_match else None,
            "modified_by": modified_by_match.group(1).strip() if modified_by_match else None,
            "source": source_match.group(1).strip() if source_match else None,
            "membership": membership_match.group(1).strip() if membership_match else None,
            "type": type_value,
            "case_description": case_match.group(1).strip() if case_match else None,
            "action": action_match.group(1).strip() if action_match else None,
            "in_out": in_out_match.group(1).strip() if in_out_match else None,
            "title": title  # Always guaranteed to have a value
        }
        
        print(f"DEBUG: Extracted case: {case}")
        
        # Only add if we have at least some basic case information and the data looks valid
        # Filter out cases with malformed data
        if (case["guest"] and len(case["guest"]) < 50 and '|' not in case["guest"] and 
            case["guest"] != "Services Domes of Corfu" and case["guest"] != "Guest Services Domes of Corfu") or (case["room"] and case["room"].isdigit()):
            cases.append(case)
            case_index += 1  # Increment case index for status/type mapping
            print(f"DEBUG: Added case {len(cases)}")
        else:
            print(f"DEBUG: Skipped case - insufficient information or malformed data")
    
    print(f"DEBUG: Total cases found: {len(cases)}")
    return cases

def process_document(file: UploadFile) -> list:
    """Full pipeline: extract → try AI parsing → fallback to regex parsing"""
    if file.filename.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(file)
    elif file.filename.lower().endswith('.docx'):
        raw_text = extract_text_from_docx(file)
    else:
        raise ValueError(f"Unsupported file type: {file.filename}")
    
    print(f"DEBUG: Extracted text length: {len(raw_text)} characters")
    print(f"DEBUG: First 500 chars: {raw_text[:500]}")
    
    # Try AI parsing first (much more reliable)
    try:
        from services.ai_service import parse_document_with_ai
        print("Attempting AI-powered document parsing...")
        ai_cases = parse_document_with_ai(raw_text)
        
        if ai_cases and len(ai_cases) > 0:
            print(f"AI parsing successful! Found {len(ai_cases)} cases")
            return ai_cases
        else:
            print("AI parsing returned no cases, falling back to regex parsing...")
    except RuntimeError as e:
        if "OPENAI_API_KEY" in str(e):
            print("OpenAI API key not configured, using regex parsing...")
        else:
            print(f"AI parsing failed: {e}, falling back to regex parsing...")
    except Exception as e:
        print(f"AI parsing failed: {e}, falling back to regex parsing...")
    
    # Fallback to regex parsing if AI fails
    print("Using regex-based parsing as fallback...")
    
    # Extract status and type information from original text before anonymization
    status_type_info = extract_status_type_info(raw_text)
    
    anonymised_text = anonymise_text(raw_text)
    cases = parse_cases(anonymised_text, status_type_info)
    return cases

def extract_status_type_info(text: str) -> dict:
    """Extract status and type information from original text before anonymization"""
    info = {}
    
    # Find all Status and Type fields in the text
    status_matches = re.findall(r'Status\s*\n\s*(\w+)', text)
    type_matches = re.findall(r'Type\s*\n\s*(\w+)', text)
    
    # Create a mapping of positions to values
    for i, status in enumerate(status_matches):
        info[f'status_{i}'] = status
    
    for i, type_val in enumerate(type_matches):
        info[f'type_{i}'] = type_val
    
    print(f"DEBUG: Extracted status/type info: {info}")
    return info

# Legacy functions for backward compatibility
def process_pdf(file: UploadFile) -> list:
    """Legacy function - now redirects to process_document"""
    return process_document(file)

def extract_text_from_document(file: UploadFile) -> str:
    """Extract text from either PDF or DOCX file based on file extension"""
    if file.filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.filename.lower().endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        raise ValueError(f"Unsupported file type: {file.filename}")