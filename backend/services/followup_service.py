from sqlalchemy.orm import Session, joinedload
from models import Followup, Case
from schemas.followup import FollowupCreate, FollowupUpdate
from typing import List, Optional, Dict, Any

def create_followup(db: Session, followup: FollowupCreate) -> Followup:
    """Create a new followup"""
    db_followup = Followup(**followup.model_dump())
    db.add(db_followup)
    db.commit()
    db.refresh(db_followup)
    return db_followup

def get_all_followups(db: Session) -> List[Followup]:
    """Get all followups"""
    return db.query(Followup).all()

def get_followups_with_case_info(db: Session) -> List[Dict[str, Any]]:
    """Get all followups with case information including room"""
    followups = db.query(Followup).join(Case).all()
    result = []
    
    for followup in followups:
        followup_data = {
            "id": followup.id,
            "case_id": followup.case_id,
            "room": followup.case.room if followup.case else None,
            "suggestion_text": followup.suggestion_text,
            "assigned_to": followup.assigned_to
        }
        result.append(followup_data)
    
    return result

def get_followup_by_id(db: Session, followup_id: int) -> Optional[Followup]:
    """Get a followup by ID"""
    return db.query(Followup).filter(Followup.id == followup_id).first()

def update_followup(db: Session, followup_id: int, followup: FollowupUpdate) -> Optional[Followup]:
    """Update a followup"""
    db_followup = db.query(Followup).filter(Followup.id == followup_id).first()
    if not db_followup:
        return None
    
    update_data = followup.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_followup, field, value)
    
    db.commit()
    db.refresh(db_followup)
    return db_followup

def delete_followup(followup_id: int, db: Session) -> Optional[Followup]:
    """Delete a followup"""
    followup = db.query(Followup).filter(Followup.id == followup_id).first()
    if not followup:
        return None
    db.delete(followup)
    db.commit()
    return followup
