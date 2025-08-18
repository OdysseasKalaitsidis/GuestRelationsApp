import os
import uuid
from fastapi import APIRouter, UploadFile, File
from services.pdf_service import process_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])



@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, anonymise it, and return structured cases as JSON.
    """

    cases = process_pdf(file)
    return {"cases": cases}
