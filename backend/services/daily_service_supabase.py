from supabase_client import get_supabase
from typing import List
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

async def clear_all_data() -> dict:
    """Clear all data from the Supabase database - cases, followups, tasks, and documents"""
    try:
        supabase = get_supabase()
        
        # Delete in the correct order to respect foreign key constraints
        
        # First, delete followups (they reference cases)
        followups_result = supabase.table("followups").delete().neq("id", 0).execute()
        followups_deleted = len(followups_result.data) if followups_result.data else 0
        
        # Then delete tasks (they reference users)
        tasks_result = supabase.table("tasks").delete().neq("id", 0).execute()
        tasks_deleted = len(tasks_result.data) if tasks_result.data else 0
        
        # Delete documents (they reference users)
        documents_result = supabase.table("documents").delete().neq("id", 0).execute()
        documents_deleted = len(documents_result.data) if documents_result.data else 0
        
        # Finally delete cases (they reference users)
        cases_result = supabase.table("cases").delete().neq("id", 0).execute()
        cases_deleted = len(cases_result.data) if cases_result.data else 0
        
        return {
            "cases_deleted": cases_deleted,
            "followups_deleted": followups_deleted,
            "tasks_deleted": tasks_deleted,
            "documents_deleted": documents_deleted,
            "message": f"Cleared {cases_deleted} cases, {followups_deleted} followups, {tasks_deleted} tasks, and {documents_deleted} documents"
        }
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        raise Exception(f"Error clearing data: {str(e)}")

async def verify_data_cleared() -> dict:
    """Verify that all data has been cleared from the Supabase database"""
    try:
        supabase = get_supabase()
        
        # Check remaining records in each table
        cases_result = supabase.table("cases").select("id").execute()
        cases_count = len(cases_result.data) if cases_result.data else 0
        
        followups_result = supabase.table("followups").select("id").execute()
        followups_count = len(followups_result.data) if followups_result.data else 0
        
        tasks_result = supabase.table("tasks").select("id").execute()
        tasks_count = len(tasks_result.data) if tasks_result.data else 0
        
        documents_result = supabase.table("documents").select("id").execute()
        documents_count = len(documents_result.data) if documents_result.data else 0
        
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
        logger.error(f"Error verifying data clearance: {e}")
        return {
            "error": str(e),
            "is_cleared": False,
            "message": f"Error verifying data clearance: {str(e)}"
        }

async def reset_daily_cases() -> dict:
    """Reset cases for a new day - archive current cases and create fresh ones"""
    try:
        supabase = get_supabase()
        today = date.today().strftime("%Y-%m-%d")
        
        # Get all current cases
        cases_result = supabase.table("cases").select("*").execute()
        current_cases = cases_result.data if cases_result.data else []
        
        # Archive current cases by updating their status
        archived_count = 0
        for case in current_cases:
            supabase.table("cases").update({"status": "archived"}).eq("id", case["id"]).execute()
            archived_count += 1
        
        # Get all current followups
        followups_result = supabase.table("followups").select("*").execute()
        current_followups = followups_result.data if followups_result.data else []
        completed_followups = len(current_followups)
        
        # Get all current tasks and mark as completed
        tasks_result = supabase.table("tasks").select("*").execute()
        current_tasks = tasks_result.data if tasks_result.data else []
        completed_tasks = 0
        
        for task in current_tasks:
            supabase.table("tasks").update({"status": "completed"}).eq("id", task["id"]).execute()
            completed_tasks += 1
        
        return {
            "date": today,
            "cases_archived": archived_count,
            "followups_completed": completed_followups,
            "tasks_completed": completed_tasks,
            "message": f"Daily reset completed: {archived_count} cases archived, {completed_followups} followups completed, {completed_tasks} tasks completed"
        }
    except Exception as e:
        logger.error(f"Error resetting daily cases: {e}")
        raise Exception(f"Error resetting daily cases: {str(e)}")
