from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import suggest_feedback

router = APIRouter(prefix="/ai", tags=["AI"])



@router.post("/feedback")
def generate_feedback(payload: dict):
    cases = payload.get("cases", [])
    results = suggest_feedback(cases)  # each case is already a dict
    return {"results": results}
