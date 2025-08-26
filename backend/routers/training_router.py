from fastapi import APIRouter, Depends, HTTPException
from models import User
from routers.auth_route import get_current_user
from services.training_service import get_training_documents_info
from typing import List

router = APIRouter(prefix="/training", tags=["Training"])

@router.get("/documents")
def get_training_documents(
    current_user: User = Depends(get_current_user)
):
    """Get information about training documents in the local folder"""
    try:
        documents_info = get_training_documents_info()
        return {
            "documents": documents_info,
            "total_count": len(documents_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading training documents: {str(e)}")
