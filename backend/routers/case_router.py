# backend/routers/case_router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from services.case_service import create_case, bulk_create_cases, get_cases, get_case_by_id, get_cases_with_followups, update_case
from services.daily_service import reset_daily_cases
from schemas.case import CaseCreate, CaseResponse, CaseUpdate
from routers.auth_route import get_current_admin_user, get_current_user
from models import User
from pydantic import BaseModel

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.post("/", response_model=CaseResponse)
def create_single_case(case: CaseCreate, db: Session = Depends(get_db)):
    """Create a single case"""
    return create_case(db, case)

@router.post("/bulk", response_model=List[CaseResponse])
def create_multiple_cases(cases: List[CaseCreate], db: Session = Depends(get_db)):
    """Create multiple cases at once"""
    return bulk_create_cases(db, cases)

@router.get("/", response_model=List[CaseResponse])
def read_cases(db: Session = Depends(get_db)):
    """Get all cases"""
    return get_cases(db)

@router.get("/with-followups")
def read_cases_with_followups(db: Session = Depends(get_db)):
    """Get all cases with their associated followups"""
    return get_cases_with_followups(db)

@router.post("/reset-daily")
def reset_daily_cases_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Reset all cases, followups, and tasks for a new day (admin only)"""
    result = reset_daily_cases(db)
    return result



@router.get("/{case_id}", response_model=CaseResponse)
def read_case(case_id: int, db: Session = Depends(get_db)):
    """Get a specific case by ID"""
    case = get_case_by_id(db, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=CaseResponse)
def update_case_endpoint(
    case_id: int, 
    case_update: CaseUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a case (requires authentication)"""
    case = update_case(db, case_id, case_update)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
