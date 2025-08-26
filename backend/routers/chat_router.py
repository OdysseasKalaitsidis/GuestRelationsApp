from fastapi import APIRouter, Depends, HTTPException
from models import User
from routers.auth_route import get_current_user
from services.rag_service import process_email_with_rag
from schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/email-assistant", response_model=ChatResponse)
def chat_with_email_assistant(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Process email content and generate AI response using RAG"""
    
    if not chat_request.email_content.strip():
        raise HTTPException(status_code=400, detail="Email content cannot be empty")
    
    try:
        # Process email with RAG
        result = process_email_with_rag(chat_request.email_content)
        
        return ChatResponse(
            response=result["response"],
            relevant_documents=result.get("relevant_documents", 0)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")
