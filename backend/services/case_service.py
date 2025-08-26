from sqlalchemy.orm import Session
from models import Case
from schemas.case import CaseCreate, CaseUpdate
from typing import List, Dict, Any, Optional

# Create a single case
def create_case(db: Session, case: CaseCreate) -> Case:
    db_case = Case(**case.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

# Bulk create multiple cases
def bulk_create_cases(db: Session, cases: List[CaseCreate]) -> List[Case]:
    db_cases = [Case(**c.model_dump()) for c in cases]  # Use .model_dump() for Pydantic V2
    db.add_all(db_cases)
    db.commit()
    for c in db_cases:
        db.refresh(c)
    return db_cases

# Retrieve all cases
def get_cases(db: Session) -> List[Case]:
    return db.query(Case).all()

# Retrieve a single case by ID
def get_case_by_id(db: Session, case_id: int) -> Case:
    return db.query(Case).filter(Case.id == case_id).first()

# Update a case
def update_case(db: Session, case_id: int, case_update: CaseUpdate) -> Optional[Case]:
    """Update a case by ID"""
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if not db_case:
        return None
    
    update_data = case_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_case, field, value)
    
    db.commit()
    db.refresh(db_case)
    return db_case

# Retrieve cases with their followups
def get_cases_with_followups(db: Session) -> List[Dict[str, Any]]:
    """Get all cases with their associated followups"""
    cases = db.query(Case).all()
    result = []
    
    for case in cases:
        case_data = {
            "id": case.id,
            "room": case.room,
            "status": case.status,
            "importance": case.importance,
            "type": case.type,
            "title": case.title,
            "action": case.action,
            "owner_id": case.owner_id,
            "followups": []
        }
        
        for followup in case.followups:
            case_data["followups"].append({
                "id": followup.id,
                "suggestion_text": followup.suggestion_text,
                "assigned_to": followup.assigned_to
            })
        
        result.append(case_data)
    
    return result
