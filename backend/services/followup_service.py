from sqlalchemy.orm import Session
from models import Followup
from schemas.followup import FollowupCreate, FollowupUpdate
from typing import List, Optional

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
