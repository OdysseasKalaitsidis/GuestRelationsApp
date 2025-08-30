from sqlalchemy.orm import Session
from models import Case
from schemas.case import CaseCreate, CaseUpdate
from typing import List, Dict, Any, Optional

# Create a single case
def create_case(db: Session, case: CaseCreate) -> Case:
    try:
        # Filter out fields that might not exist in the database yet
        case_data = case.model_dump()
        safe_fields = ['room', 'status', 'importance', 'type', 'title', 'action', 'owner_id']
        
        # Only include fields that exist in the current database schema
        filtered_data = {k: v for k, v in case_data.items() if k in safe_fields and v is not None}
        
        db_case = Case(**filtered_data)
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        return db_case
    except Exception as e:
        print(f"Error creating case: {e}")
        db.rollback()
        raise

# Bulk create multiple cases
def bulk_create_cases(db: Session, cases: List[CaseCreate]) -> List[Case]:
    try:
        safe_fields = ['room', 'status', 'importance', 'type', 'title', 'action', 'owner_id']
        db_cases = []
        
        for c in cases:
            case_data = c.model_dump()
            # Only include fields that exist in the current database schema
            filtered_data = {k: v for k, v in case_data.items() if k in safe_fields and v is not None}
            db_case = Case(**filtered_data)
            db_cases.append(db_case)
        
        db.add_all(db_cases)
        db.commit()
        for c in db_cases:
            db.refresh(c)
        return db_cases
    except Exception as e:
        print(f"Error bulk creating cases: {e}")
        db.rollback()
        raise

# Retrieve all cases
def get_cases(db: Session) -> List[Case]:
    try:
        cases = db.query(Case).all()
        return cases
    except Exception as e:
        print(f"Error retrieving cases: {e}")
        return []

# Retrieve a single case by ID
def get_case_by_id(db: Session, case_id: int) -> Case:
    try:
        return db.query(Case).filter(Case.id == case_id).first()
    except Exception as e:
        print(f"Error retrieving case {case_id}: {e}")
        return None

# Update a case
def update_case(db: Session, case_id: int, case_update: CaseUpdate) -> Optional[Case]:
    """Update a case by ID"""
    try:
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return None
        
        update_data = case_update.model_dump(exclude_unset=True)
        safe_fields = ['room', 'status', 'importance', 'type', 'title', 'action', 'owner_id']
        
        # Only update fields that exist in the current database schema
        for field, value in update_data.items():
            if field in safe_fields and hasattr(db_case, field):
                setattr(db_case, field, value)
        
        db.commit()
        db.refresh(db_case)
        return db_case
    except Exception as e:
        print(f"Error updating case {case_id}: {e}")
        db.rollback()
        return None

# Retrieve cases with their followups
def get_cases_with_followups(db: Session) -> List[Dict[str, Any]]:
    """Get all cases with their associated followups using eager loading"""
    try:
        # Use eager loading to fetch cases and followups in one query
        from sqlalchemy.orm import joinedload
        cases = db.query(Case).options(joinedload(Case.followups)).all()
        result = []
        
        for case in cases:
            case_data = {
                "id": case.id,
                "room": getattr(case, 'room', None),
                "status": getattr(case, 'status', None),
                "importance": getattr(case, 'importance', None),
                "type": getattr(case, 'type', None),
                "title": getattr(case, 'title', None),
                "action": getattr(case, 'action', None),
                "owner_id": getattr(case, 'owner_id', None),
                # New fields - temporarily commented out until migration is run
                # "guest": getattr(case, 'guest', None),
                # "created": getattr(case, 'created', None),
                # "created_by": getattr(case, 'created_by', None),
                # "modified": getattr(case, 'modified', None),
                # "modified_by": getattr(case, 'modified_by', None),
                # "source": getattr(case, 'source', None),
                # "membership": getattr(case, 'membership', None),
                # "case_description": getattr(case, 'case_description', None),
                # "in_out": getattr(case, 'in_out', None),
                "followups": []
            }
            
            # Safely access followups if the relationship exists
            try:
                if hasattr(case, 'followups') and case.followups:
                    for followup in case.followups:
                        case_data["followups"].append({
                            "id": followup.id,
                            "suggestion_text": followup.suggestion_text,
                            "assigned_to": followup.assigned_to
                        })
            except Exception as e:
                # If followups relationship fails, just continue with empty list
                print(f"Warning: Could not load followups for case {case.id}: {e}")
                case_data["followups"] = []
            
            result.append(case_data)
        
        return result
        
    except Exception as e:
        print(f"Error in get_cases_with_followups: {e}")
        # Return basic case data without followups if there's an error
        try:
            cases = db.query(Case).all()
            return [{
                "id": case.id,
                "room": getattr(case, 'room', None),
                "status": getattr(case, 'status', None),
                "importance": getattr(case, 'importance', None),
                "type": getattr(case, 'type', None),
                "title": getattr(case, 'title', None),
                "action": getattr(case, 'action', None),
                "owner_id": getattr(case, 'owner_id', None),
                "followups": []
            } for case in cases]
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return []
