from sqlalchemy.orm import Session
from models import Followup
from db import SessionLocal

def get_all_followups(db: Session = None):
    if db is None:
        db = SessionLocal()
    followups = db.query(Followup).all()
    return [{"id": f.id, "suggestion_text": f.suggestion_text} for f in followups]

def delete_followup(followup_id: int, db: Session = None):
    if db is None:
        db = SessionLocal()
    followup = db.query(Followup).filter(Followup.id == followup_id).first()
    if not followup:
        return None
    db.delete(followup)
    db.commit()
    return followup
