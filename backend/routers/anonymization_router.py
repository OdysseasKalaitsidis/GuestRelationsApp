# routers/anonymization_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.anonymization_service import anonymization_service
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/anonymization", tags=["Anonymization"])

class AnonymizationRequest(BaseModel):
    preserve_dates: bool = False
    preserve_times: bool = False

class AnonymizationResponse(BaseModel):
    filename: str
    file_type: str
    original_content: List[str]
    anonymized_content: List[str]
    anonymization_summary: Dict[str, Any]
    message: str

class AnonymizationStatsResponse(BaseModel):
    total_potential_pii: int
    breakdown: Dict[str, Any]
    message: str

@router.post("/document", response_model=AnonymizationResponse)
async def anonymize_document(
    file: UploadFile = File(...),
    preserve_dates: bool = Query(False, description="Preserve date information"),
    preserve_times: bool = Query(False, description="Preserve time information")
):
    """
    Anonymize a document (PDF or DOCX) by removing PII while preserving structure
    
    This endpoint will:
    - Extract text from the document
    - Identify and replace PII with anonymized tokens
    - Preserve document structure (paragraphs, tables)
    - Return both original and anonymized versions
    """
    # Check file extension
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400, 
            detail="File must be a PDF (.pdf) or Word document (.docx)"
        )
    
    try:
        result = anonymization_service.anonymize_document(
            file, 
            preserve_dates=preserve_dates, 
            preserve_times=preserve_times
        )
        
        return AnonymizationResponse(
            **result,
            message=f"Successfully anonymized {file.filename}. {result['anonymization_summary']['total_replacements']} PII elements were replaced."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error anonymizing document: {str(e)}"
        )

@router.post("/text", response_model=Dict[str, str])
async def anonymize_text(
    request: AnonymizationRequest,
    text: str = Query(..., description="Text content to anonymize")
):
    """
    Anonymize plain text content
    
    This endpoint will:
    - Identify PII in the provided text
    - Replace PII with anonymized tokens
    - Return the anonymized text
    """
    try:
        anonymized_text = anonymization_service.anonymize_text(
            text,
            preserve_dates=request.preserve_dates,
            preserve_times=request.preserve_times
        )
        
        return {
            "original_text": text,
            "anonymized_text": anonymized_text,
            "message": "Text anonymized successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error anonymizing text: {str(e)}"
        )

@router.post("/stats", response_model=AnonymizationStatsResponse)
async def get_anonymization_stats(text: str = Query(..., description="Text to analyze for PII")):
    """
    Get statistics about potential PII in text without anonymizing
    
    This endpoint will:
    - Analyze the text for potential PII
    - Count different types of PII found
    - Provide examples of what would be anonymized
    - Return statistics without modifying the text
    """
    try:
        stats = anonymization_service.get_anonymization_stats(text)
        
        return AnonymizationStatsResponse(
            **stats,
            message=f"Found {stats['total_potential_pii']} potential PII elements in the text"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )

@router.get("/patterns", response_model=Dict[str, str])
async def get_anonymization_patterns():
    """
    Get information about the anonymization patterns used
    
    This endpoint will:
    - Return the current PII detection patterns
    - Show what types of data are detected
    - Help users understand what will be anonymized
    """
    try:
        patterns_info = {}
        for pattern_name, pattern in anonymization_service.patterns.items():
            patterns_info[pattern_name] = {
                "description": f"Detects {pattern_name.replace('_', ' ')}",
                "example_replacement": anonymization_service.replacements.get(pattern_name, f"[{pattern_name.upper()}]")
            }
        
        return {
            "patterns": patterns_info,
            "message": f"Currently using {len(patterns_info)} PII detection patterns"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving patterns: {str(e)}"
        )
