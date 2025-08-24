import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_service import process_pdf
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/pdf", tags=["PDF"])

class CaseData(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: str
    action: Optional[str] = None

class PDFUploadResponse(BaseModel):
    cases: List[CaseData]
    message: str

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, process it, and return structured cases as JSON.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        cases = process_pdf(file)
        return PDFUploadResponse(
            cases=cases,
            message=f"Successfully processed {len(cases)} cases from PDF"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
