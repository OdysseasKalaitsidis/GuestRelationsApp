from sqlalchemy.orm import Session
from models import Case, Followup, Task
from typing import List
from datetime import date, datetime

def reset_daily_cases(db: Session) -> dict:
    """Reset cases for a new day - archive current cases and create fresh ones"""
    today = date.today().strftime("%Y-%m-%d")
    
    # Get all current cases
    current_cases = db.query(Case).all()
    
    # Archive current cases by updating their status
    archived_count = 0
    for case in current_cases:
        case.status = "archived"
        archived_count += 1
    
    # Get all current followups (no status changes needed)
    current_followups = db.query(Followup).all()
    completed_followups = len(current_followups)
    
    # Get all current tasks and mark as completed
    current_tasks = db.query(Task).all()
    completed_tasks = 0
    for task in current_tasks:
        if task.status != "completed":
            task.status = "completed"
            task.completed_at = today
            completed_tasks += 1
    
    db.commit()
    
    return {
        "archived_cases": archived_count,
        "completed_followups": completed_followups,
        "completed_tasks": completed_tasks,
        "reset_date": today
    }


