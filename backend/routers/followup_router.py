from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db import get_db
from services.followup_service import (
    get_all_followups, delete_followup, create_followup, update_followup, 
    get_followup_by_id, get_followups_with_case_info, get_anonymized_followups,
    anonymize_existing_followup_text, bulk_anonymize_followups, 
    get_followup_anonymization_stats, create_followup_from_anonymized_data
)
from schemas.followup import FollowupCreate, FollowupUpdate, FollowupOut
from pydantic import BaseModel

router = APIRouter(prefix="/followups", tags=["Followups"])

class BulkAnonymizationRequest(BaseModel):
    followup_ids: List[int]

class AnonymizedFollowupResponse(BaseModel):
    id: int
    case_id: int
    room: str = None
    suggestion_text: str
    assigned_to: int = None
    anonymized_case_title: str = None
    anonymized_case_description: str = None

@router.post("/", response_model=FollowupOut)
async def create_new_followup(followup: FollowupCreate, db: AsyncSession = Depends(get_db)):
    """Create a new followup"""
    return await create_followup(db, followup)

@router.get("/", response_model=List[FollowupOut])
async def read_followups(db: AsyncSession = Depends(get_db)):
    """Get all followups"""
    return await get_all_followups(db)

@router.get("/with-case-info")
async def read_followups_with_case_info(db: AsyncSession = Depends(get_db)):
    """Get all followups with case information including room"""
    return await get_followups_with_case_info(db)

@router.get("/{followup_id}", response_model=FollowupOut)
async def read_followup(followup_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific followup by ID"""
    followup = await get_followup_by_id(db, followup_id)
    if followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return followup

@router.put("/{followup_id}", response_model=FollowupOut)
async def update_existing_followup(followup_id: int, followup: FollowupUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing followup"""
    updated_followup = await update_followup(db, followup_id, followup)
    if updated_followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return updated_followup

@router.delete("/{followup_id}")
async def remove_followup(followup_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a followup"""
    followup = await delete_followup(followup_id, db)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return {"status": "success", "id": followup_id}

# New anonymization-related endpoints

@router.get("/anonymized/list", response_model=List[AnonymizedFollowupResponse])
async def read_anonymized_followups(db: AsyncSession = Depends(get_db)):
    """
    Get all followups with anonymized case information
    
    This ensures that any PII in case descriptions is properly anonymized
    before being returned
    """
    return await get_anonymized_followups(db)

@router.post("/{followup_id}/anonymize", response_model=FollowupOut)
async def anonymize_followup_text(followup_id: int, db: AsyncSession = Depends(get_db)):
    """
    Anonymize the text of an existing followup
    
    This is useful for ensuring that existing followups don't contain PII
    """
    followup = await anonymize_existing_followup_text(db, followup_id)
    if followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return followup

@router.post("/bulk-anonymize")
async def bulk_anonymize_followups_endpoint(
    request: BulkAnonymizationRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Bulk anonymize multiple followups
    
    This endpoint allows you to anonymize multiple followups at once
    """
    if not request.followup_ids:
        raise HTTPException(status_code=400, detail="No followup IDs provided")
    
    results = await bulk_anonymize_followups(db, request.followup_ids)
    return {
        "message": f"Processed {results['total_processed']} followups",
        "results": results
    }

@router.get("/anonymization/stats")
async def get_anonymization_statistics(db: AsyncSession = Depends(get_db)):
    """
    Get statistics about anonymization in followups
    
    This helps identify which followups might need anonymization
    """
    return await get_followup_anonymization_stats(db)

@router.post("/from-anonymized-data", response_model=FollowupOut)
async def create_followup_from_anonymized(
    case_id: int,
    anonymized_text: str,
    assigned_to: int = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a followup from anonymized data
    
    This function ensures that the followup text is properly anonymized
    and doesn't contain any PII that might have been missed
    """
    return await create_followup_from_anonymized_data(db, case_id, anonymized_text, assigned_to)
