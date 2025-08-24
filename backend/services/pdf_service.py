# services/pdf_service.py
import re
import pdfplumber
import spacy
from fastapi import UploadFile
from io import BytesIO

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

def anonymise_text(text: str) -> str:
    """Remove PII (names, emails, phones, booking refs)"""
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    text = re.sub(r'\+?\d[\d\-\s]{7,}\d', '[PHONE]', text)
    text = re.sub(r'\b(?:REF|#)\d+\b', '[BOOKING]', text)

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, "[NAME]")
    return text

def parse_cases(text: str) -> list:
    """Convert anonymised text into structured list of case dicts"""
    cases = []
    # Keep only text starting from the first case
    first_case_index = text.find('[NAME]:')
    if first_case_index == -1:
        return []  # no cases found
    text = text[first_case_index:]
    blocks = re.split(r'\[NAME\]:', text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        room_match = re.search(r'Room:\s*(\d+)', block)
        status_match = re.search(r'Status:\s*(\w+)', block)
        importance_match = re.search(r'Importance:\s*(\w+)', block)
        type_match = re.search(r'Type:\s*(\w+)', block)
        case_match = re.search(r'Case:\s*((?:.|\n)*?)\s*Action:', block, re.DOTALL)
        action_match = re.search(r'Action:\s*((?:.|\n)*)', block, re.DOTALL)

        # Extract title and ensure it's never None
        title = case_match.group(1).strip() if case_match else None
        if not title or title.strip() == "":
            title = "Untitled Case"  # Provide default title
        
        cases.append({
            "room": room_match.group(1) if room_match else None,
            "status": status_match.group(1) if status_match else None,
            "importance": importance_match.group(1) if importance_match else None,
            "type": type_match.group(1) if type_match else None,
            "title": title,  # This will never be None now
            "action": action_match.group(1).strip() if action_match else None
        })

    return cases

def process_pdf(file: UploadFile) -> list:
    """Full pipeline: extract → anonymise → parse cases"""
    raw_text = extract_text_from_pdf(file)
    anonymised_text = anonymise_text(raw_text)
    return parse_cases(anonymised_text)
