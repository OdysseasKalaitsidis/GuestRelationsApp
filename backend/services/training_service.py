import os
import PyPDF2
from typing import List, Dict
import io
from pathlib import Path

def get_training_documents_folder() -> str:
    """Get the path to the training documents folder"""
    current_dir = Path(__file__).parent.parent
    return os.path.join(current_dir, "training_documents")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading text file {file_path}: {str(e)}")
            return ""

def load_training_documents() -> List[Dict[str, str]]:
    """Load all training documents from the training_documents folder"""
    documents = []
    training_folder = get_training_documents_folder()
    
    if not os.path.exists(training_folder):
        print(f"Training documents folder not found: {training_folder}")
        return documents
    
    for filename in os.listdir(training_folder):
        file_path = os.path.join(training_folder, filename)
        
        if os.path.isfile(file_path):
            file_extension = filename.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                content = extract_text_from_pdf(file_path)
            elif file_extension == 'txt':
                content = extract_text_from_txt(file_path)
            else:
                continue  # Skip unsupported file types
            
            if content.strip():  # Only add documents with content
                documents.append({
                    'filename': filename,
                    'file_type': file_extension,
                    'content': content
                })
    
    return documents

def get_training_documents_info() -> List[Dict[str, str]]:
    """Get information about training documents without loading full content"""
    documents_info = []
    training_folder = get_training_documents_folder()
    
    if not os.path.exists(training_folder):
        return documents_info
    
    for filename in os.listdir(training_folder):
        file_path = os.path.join(training_folder, filename)
        
        if os.path.isfile(file_path):
            file_extension = filename.split('.')[-1].lower()
            
            if file_extension in ['pdf', 'txt']:
                file_size = os.path.getsize(file_path)
                documents_info.append({
                    'filename': filename,
                    'file_type': file_extension,
                    'file_size': file_size,
                    'file_path': file_path
                })
    
    return documents_info
