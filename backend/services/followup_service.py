from sqlalchemy.orm import Session, joinedload
from models import Followup, Case
from schemas.followup import FollowupCreate, FollowupUpdate
from typing import List, Optional, Dict, Any
from services.anonymization_service import anonymization_service

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

def create_followup_from_anonymized_data(
    db: Session, 
    case_id: int, 
    anonymized_text: str, 
    assigned_to: Optional[int] = None
) -> Followup:
    """
    Create a followup from anonymized data
    
    This function ensures that the followup text is properly anonymized
    and doesn't contain any PII that might have been missed
    """
    # Double-check anonymization to ensure no PII remains
    final_anonymized_text = anonymization_service.anonymize_text(anonymized_text)
    
    followup_data = FollowupCreate(
        case_id=case_id,
        suggestion_text=final_anonymized_text,
        assigned_to=assigned_to
    )
    
    return create_followup(db, followup_data)

def get_anonymized_followups(db: Session) -> List[Dict[str, Any]]:
    """
    Get all followups with anonymized case information
    
    This ensures that any PII in case descriptions is properly anonymized
    before being returned
    """
    followups = db.query(Followup).join(Case).all()
    result = []
    
    for followup in followups:
        # Anonymize case title and description if they exist
        case_title = followup.case.title if followup.case else None
        case_description = getattr(followup.case, 'description', None) if followup.case else None
        
        anonymized_title = anonymization_service.anonymize_text(case_title) if case_title else None
        anonymized_description = anonymization_service.anonymize_text(case_description) if case_description else None
        
        followup_data = {
            "id": followup.id,
            "case_id": followup.case_id,
            "room": followup.case.room if followup.case else None,
            "suggestion_text": followup.suggestion_text,
            "assigned_to": followup.assigned_to,
            "anonymized_case_title": anonymized_title,
            "anonymized_case_description": anonymized_description
        }
        result.append(followup_data)
    
    return result

def anonymize_existing_followup_text(db: Session, followup_id: int) -> Optional[Followup]:
    """
    Anonymize the text of an existing followup
    
    This is useful for ensuring that existing followups don't contain PII
    """
    followup = get_followup_by_id(db, followup_id)
    if not followup:
        return None
    
    # Anonymize the suggestion text
    anonymized_text = anonymization_service.anonymize_text(followup.suggestion_text)
    
    # Update the followup with anonymized text
    update_data = FollowupUpdate(suggestion_text=anonymized_text)
    return update_followup(db, followup_id, update_data)

def bulk_anonymize_followups(db: Session, followup_ids: List[int]) -> Dict[str, Any]:
    """
    Bulk anonymize multiple followups
    
    Returns a summary of the anonymization process
    """
    results = {
        "successful": [],
        "failed": [],
        "total_processed": 0,
        "total_anonymized": 0
    }
    
    for followup_id in followup_ids:
        try:
            followup = anonymize_existing_followup_text(db, followup_id)
            if followup:
                results["successful"].append(followup_id)
                results["total_anonymized"] += 1
            else:
                results["failed"].append(followup_id)
        except Exception as e:
            results["failed"].append(followup_id)
        
        results["total_processed"] += 1
    
    return results

def get_followup_anonymization_stats(db: Session) -> Dict[str, Any]:
    """
    Get statistics about anonymization in followups
    
    This helps identify which followups might need anonymization
    """
    followups = db.query(Followup).all()
    
    stats = {
        "total_followups": len(followups),
        "potentially_containing_pii": 0,
        "anonymization_breakdown": {}
    }
    
    for followup in followups:
        # Check if the followup text contains potential PII
        pii_stats = anonymization_service.get_anonymization_stats(followup.suggestion_text)
        
        if pii_stats["total_potential_pii"] > 0:
            stats["potentially_containing_pii"] += 1
            
            # Aggregate PII types found
            for pii_type, pii_info in pii_stats["breakdown"].items():
                if pii_type not in stats["anonymization_breakdown"]:
                    stats["anonymization_breakdown"][pii_type] = 0
                stats["anonymization_breakdown"][pii_type] += pii_info["count"]
    
    return stats
