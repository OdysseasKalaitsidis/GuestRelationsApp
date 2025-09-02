from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from models import Case, Followup, Task
from typing import List
from datetime import date, datetime

async def clear_all_data(db: AsyncSession) -> dict:
    """Clear all data from the database - cases, followups, tasks, and documents"""
    try:
        # For PostgreSQL, we need to handle foreign key constraints differently
        # Delete in the correct order to respect foreign key constraints
        
        # First, delete followups (they reference cases)
        followups_result = await db.execute(text("DELETE FROM followups"))
        followups_deleted = followups_result.rowcount
        
        # Then delete tasks (they reference users)
        tasks_result = await db.execute(text("DELETE FROM tasks"))
        tasks_deleted = tasks_result.rowcount
        
        # Delete documents (they reference users)
        documents_result = await db.execute(text("DELETE FROM documents"))
        documents_deleted = documents_result.rowcount
        
        # Finally delete cases (they reference users)
        cases_result = await db.execute(text("DELETE FROM cases"))
        cases_deleted = cases_result.rowcount
        
        # Single commit for all operations
        await db.commit()
        
        return {
            "cases_deleted": cases_deleted,
            "followups_deleted": followups_deleted,
            "tasks_deleted": tasks_deleted,
            "documents_deleted": documents_deleted,
            "message": f"Cleared {cases_deleted} cases, {followups_deleted} followups, {tasks_deleted} tasks, and {documents_deleted} documents"
        }
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error clearing data: {str(e)}")

async def verify_data_cleared(db: AsyncSession) -> dict:
    """Verify that all data has been cleared from the database"""
    try:
        # Check remaining records in each table
        cases_result = await db.execute(text("SELECT COUNT(*) FROM cases"))
        cases_count = cases_result.scalar()
        
        followups_result = await db.execute(text("SELECT COUNT(*) FROM followups"))
        followups_count = followups_result.scalar()
        
        tasks_result = await db.execute(text("SELECT COUNT(*) FROM tasks"))
        tasks_count = tasks_result.scalar()
        
        documents_result = await db.execute(text("SELECT COUNT(*) FROM documents"))
        documents_count = documents_result.scalar()
        
        total_remaining = cases_count + followups_count + tasks_count + documents_count
        
        return {
            "cases_remaining": cases_count,
            "followups_remaining": followups_count,
            "tasks_remaining": tasks_count,
            "documents_remaining": documents_count,
            "total_remaining": total_remaining,
            "is_cleared": total_remaining == 0,
            "message": f"Verification complete: {total_remaining} records remaining in database"
        }
    except Exception as e:
        return {
            "error": str(e),
            "is_cleared": False,
            "message": f"Error verifying data clearance: {str(e)}"
        }

async def reset_daily_cases(db: AsyncSession) -> dict:
    """Reset cases for a new day - archive current cases and create fresh ones"""
    today = date.today().strftime("%Y-%m-%d")
    
    # Get all current cases
    result = await db.execute(select(Case))
    current_cases = result.scalars().all()
    
    # Archive current cases by updating their status
    archived_count = 0
    for case in current_cases:
        case.status = "archived"
        archived_count += 1
    
    # Get all current followups (no status changes needed)
    followups_result = await db.execute(select(Followup))
    current_followups = followups_result.scalars().all()
    completed_followups = len(current_followups)
    
    # Get all current tasks and mark as completed
    tasks_result = await db.execute(select(Task))
    current_tasks = tasks_result.scalars().all()
    completed_tasks = 0
    for task in current_tasks:
        if task.status != "completed":
            task.status = "completed"
            task.completed_at = today
            completed_tasks += 1
    
    await db.commit()
    
    return {
        "archived_cases": archived_count,
        "completed_followups": completed_followups,
        "completed_tasks": completed_tasks,
        "reset_date": today
    }


