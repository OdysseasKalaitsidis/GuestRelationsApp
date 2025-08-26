from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from services.followup_service import get_all_followups, delete_followup, create_followup, update_followup, get_followup_by_id, get_followups_with_case_info
from schemas.followup import FollowupCreate, FollowupUpdate, FollowupOut

router = APIRouter(prefix="/followups", tags=["Followups"])

@router.post("/", response_model=FollowupOut)
def create_new_followup(followup: FollowupCreate, db: Session = Depends(get_db)):
    """Create a new followup"""
    return create_followup(db, followup)

@router.get("/", response_model=List[FollowupOut])
def read_followups(db: Session = Depends(get_db)):
    """Get all followups"""
    return get_all_followups(db)

@router.get("/with-case-info")
def read_followups_with_case_info(db: Session = Depends(get_db)):
    """Get all followups with case information including room"""
    return get_followups_with_case_info(db)

@router.get("/{followup_id}", response_model=FollowupOut)
def read_followup(followup_id: int, db: Session = Depends(get_db)):
    """Get a specific followup by ID"""
    followup = get_followup_by_id(db, followup_id)
    if followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return followup

@router.put("/{followup_id}", response_model=FollowupOut)
def update_existing_followup(followup_id: int, followup: FollowupUpdate, db: Session = Depends(get_db)):
    """Update an existing followup"""
    updated_followup = update_followup(db, followup_id, followup)
    if updated_followup is None:
        raise HTTPException(status_code=404, detail="Followup not found")
    return updated_followup

@router.delete("/{followup_id}")
def remove_followup(followup_id: int, db: Session = Depends(get_db)):
    """Delete a followup"""
    followup = delete_followup(followup_id, db)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return {"status": "success", "id": followup_id}
