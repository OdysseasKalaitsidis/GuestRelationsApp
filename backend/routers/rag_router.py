# backend/routers/rag_router.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import logging
from services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG"])

# Pydantic models for request/response
class EmailProcessRequest(BaseModel):
    input_text: str
    context: Optional[str] = None

class EmailProcessResponse(BaseModel):
    success: bool
    email: Optional[dict] = None
    context_used: Optional[List[dict]] = None
    input_text: str
    processing_info: Optional[dict] = None
    error: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    uploaded_files: List[dict]
    processed_chunks: int
    errors: List[str]

class CollectionStatsResponse(BaseModel):
    total_chunks: int
    status: str
    persist_folder: Optional[str] = None
    error: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[dict]

class ChatResponse(BaseModel):
    reply: str

class ShiftSummaryRequest(BaseModel):
    notes: str

class ShiftSummaryResponse(BaseModel):
    date: Optional[str] = None
    highlights: List[str] = []
    error: Optional[str] = None

@router.post("/upload-documents", response_model=DocumentUploadResponse)
async def upload_training_documents(
    files: List[UploadFile] = File(...)
):
    """
    Upload training documents for the RAG system.
    These documents will be processed and stored in the vector database.
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        logger.info(f"Uploading {len(files)} documents for RAG training")
        
        # Process files through RAG service
        result = rag_service.upload_training_documents(files)
        
        logger.info(f"Successfully processed {result['processed_chunks']} chunks from {len(result['uploaded_files'])} files")
        
        return DocumentUploadResponse(**result)
        
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading documents: {str(e)}")

@router.post("/process-email", response_model=EmailProcessResponse)
async def process_email(request: EmailProcessRequest):
    """
    Process an email using RAG to generate a standardized response.
    Takes input email text and returns a formatted email based on training documents.
    """
    try:
        if not request.input_text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty")
        
        logger.info("Processing email with RAG")
        
        # Process email through RAG service
        result = rag_service.process_email_with_rag(
            input_text=request.input_text,
            context=request.context
        )
        
        if result["success"]:
            logger.info("Email processed successfully")
            return EmailProcessResponse(**result)
        else:
            logger.error(f"Email processing failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Email processing failed"))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")

@router.get("/stats", response_model=CollectionStatsResponse)
async def get_collection_stats():
    """
    Get statistics about the document collection in the vector database.
    """
    try:
        stats = rag_service.get_collection_stats()
        return CollectionStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error getting collection stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting collection stats: {str(e)}")

@router.delete("/clear-collection")
async def clear_collection():
    """
    Clear all documents from the vector database collection.
    This will remove all training data.
    """
    try:
        result = rag_service.clear_collection()
        
        if result["success"]:
            logger.info("Collection cleared successfully")
            return {"success": True, "message": "Collection cleared successfully"}
        else:
            logger.error(f"Error clearing collection: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to clear collection"))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing collection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing collection: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat with the AI assistant using RAG context.
    """
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
        logger.info("Processing chat request")
        
        # Get AI reply with RAG context
        reply = rag_service.get_openai_reply(request.messages)
        
        return ChatResponse(reply=reply)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.post("/extract-shift-summary", response_model=ShiftSummaryResponse)
async def extract_shift_summary(request: ShiftSummaryRequest):
    """
    Extract structured summary from shift notes.
    """
    try:
        if not request.notes.strip():
            raise HTTPException(status_code=400, detail="Notes cannot be empty")
        
        logger.info("Extracting shift summary")
        
        # Extract shift summary
        result = rag_service.extract_shift_summary(request.notes)
        
        if "error" in result:
            return ShiftSummaryResponse(error=result["error"])
        
        return ShiftSummaryResponse(
            date=result.get("date"),
            highlights=result.get("highlights", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting shift summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting shift summary: {str(e)}")

@router.post("/rebuild-from-data")
async def rebuild_from_data_folder():
    """
    Rebuild vectorstore from documents in the data folder.
    This is an admin-only operation.
    """
    try:
        logger.info("Rebuilding vectorstore from data folder")
        
        result = rag_service.rebuild_from_data_folder()
        
        if result["success"]:
            logger.info(f"Vectorstore rebuilt successfully: {result['message']}")
            return result
        else:
            logger.error(f"Vectorstore rebuild failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to rebuild vectorstore"))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rebuilding vectorstore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error rebuilding vectorstore: {str(e)}")

@router.post("/test-rag")
async def test_rag_system():
    """
    Test endpoint to verify the RAG system is working correctly.
    """
    try:
        # Test with a simple query
        test_text = "Hello, I need help with my reservation."
        
        result = rag_service.process_email_with_rag(test_text)
        
        if result["success"]:
            return {
                "success": True,
                "message": "RAG system is working correctly",
                "test_result": result
            }
        else:
            return {
                "success": False,
                "message": "RAG system test failed",
                "error": result.get("error", "Unknown error")
            }
        
    except Exception as e:
        logger.error(f"Error testing RAG system: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error testing RAG system: {str(e)}")
