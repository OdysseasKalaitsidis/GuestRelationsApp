from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import suggest_feedback

router = APIRouter(prefix="/ai", tags=["AI"])

class CaseData(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: str
    action: Optional[str] = None

class FeedbackRequest(BaseModel):
    cases: List[CaseData]

class FeedbackResponse(BaseModel):
    case_id: int
    suggestion_text: str
    confidence: float

@router.post("/feedback", response_model=List[FeedbackResponse])
def generate_feedback(request: FeedbackRequest):
    """Generate AI feedback for uploaded cases"""
    cases = [case.dict() for case in request.cases]
    results = suggest_feedback(cases)
    return results
