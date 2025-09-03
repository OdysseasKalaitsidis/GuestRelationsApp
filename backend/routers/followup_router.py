from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.database_service import get_db_service
from services.followup_service_supabase import (
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
async def create_new_followup(followup: FollowupCreate, db_service = Depends(get_db_service)):
    """Create a new followup"""
    try:
        result = await create_followup(followup)
        if result is None:
            raise HTTPException(status_code=500, detail="Failed to create followup")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating followup: {str(e)}")

@router.get("/", response_model=List[FollowupOut])
async def read_followups(db_service = Depends(get_db_service)):
    """Get all followups"""
    return await get_all_followups()

@router.get("/with-case-info")
async def read_followups_with_case_info(db_service = Depends(get_db_service)):
    """Get all followups with case information including room"""
    return await get_followups_with_case_info()

@router.get("/{followup_id}", response_model=FollowupOut)
async def read_followup(followup_id: int, db_service = Depends(get_db_service)):
    """Get a specific followup by ID"""
    followup = await get_followup_by_id(followup_id)
    if followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return followup

@router.put("/{followup_id}", response_model=FollowupOut)
async def update_existing_followup(followup_id: int, followup: FollowupUpdate, db_service = Depends(get_db_service)):
    """Update an existing followup"""
    updated_followup = await update_followup(followup_id, followup)
    if updated_followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return updated_followup

@router.delete("/{followup_id}")
async def remove_followup(followup_id: int, db_service = Depends(get_db_service)):
    """Delete a followup"""
    followup = await delete_followup(followup_id)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return {"status": "success", "id": followup_id}

# New anonymization-related endpoints

@router.get("/anonymized/list", response_model=List[AnonymizedFollowupResponse])
async def read_anonymized_followups(db_service = Depends(get_db_service)):
    """
    Get all followups with anonymized case information
    
    This ensures that any PII in case descriptions is properly anonymized
    before being returned
    """
    return await get_anonymized_followups()

@router.post("/{followup_id}/anonymize", response_model=FollowupOut)
async def anonymize_followup_text(followup_id: int, db_service = Depends(get_db_service)):
    """
    Anonymize the text of an existing followup
    
    This is useful for ensuring that existing followups don't contain PII
    """
    followup = await anonymize_existing_followup_text(followup_id)
    if followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return followup

@router.post("/bulk-anonymize")
async def bulk_anonymize_followups_endpoint(
    request: BulkAnonymizationRequest, 
    db_service = Depends(get_db_service)
):
    """
    Bulk anonymize multiple followups
    
    This endpoint allows you to anonymize multiple followups at once
    """
    anonymized_followups = await bulk_anonymize_followups(request.followup_ids)
    return {
        "message": f"Anonymized {len(anonymized_followups)} followups",
        "anonymized_count": len(anonymized_followups),
        "anonymized_followups": anonymized_followups
    }

@router.get("/anonymization/stats")
async def get_anonymization_statistics(db_service = Depends(get_db_service)):
    """
    Get anonymization statistics for followups
    
    This provides insights into how much data has been anonymized
    """
    stats = await get_followup_anonymization_stats()
    return stats

@router.post("/anonymization/create-from-data")
async def create_followup_from_anonymized_data_endpoint(
    anonymized_data: dict,
    db_service = Depends(get_db_service)
):
    """
    Create a followup from anonymized data
    
    This is useful for creating followups from external sources
    that have already been anonymized
    """
    followup = await create_followup_from_anonymized_data(anonymized_data)
    if followup is None:
        raise HTTPException(status_code=400, detail="Failed to create followup from anonymized data")
    return followup
