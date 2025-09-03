# Task Service using Supabase Database Service
from typing import List, Optional, Dict, Any
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from services.database_service import get_db_service
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

async def create_task(task: TaskCreate, assigned_by: int) -> Optional[Dict[str, Any]]:
    """Create a new task using Supabase"""
    try:
        db_service = await get_db_service()
        
        # Prepare task data
        task_data = {
            "title": task.title,
            "description": task.description,
            "task_type": task.task_type,
            "assigned_to": task.assigned_to,
            "assigned_by": assigned_by,
            "due_date": task.due_date,
            "status": "pending",
            "created_at": date.today().strftime("%Y-%m-%d"),
            "completed_at": None
        }
        
        # Create task in database
        result = await db_service.create("tasks", task_data)
        
        if result:
            logger.info(f"Task created successfully: {result['id']}")
            return result
        else:
            logger.error("Failed to create task: No data returned")
            return None
            
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return None

async def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    """Get task by ID"""
    try:
        db_service = await get_db_service()
        task = await db_service.get_by_id("tasks", task_id)
        return task
    except Exception as e:
        logger.error(f"Error getting task by ID: {e}")
        return None

async def get_all_tasks() -> List[Dict[str, Any]]:
    """Get all tasks"""
    try:
        db_service = await get_db_service()
        tasks = await db_service.get_all("tasks")
        return tasks
    except Exception as e:
        logger.error(f"Error getting all tasks: {e}")
        return []

async def get_tasks_by_user(user_id: int) -> List[Dict[str, Any]]:
    """Get tasks assigned to a specific user"""
    try:
        db_service = await get_db_service()
        tasks = await db_service.get_by_field("tasks", "assigned_to", user_id)
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks by user: {e}")
        return []

async def update_task(task_id: int, task_update: TaskUpdate) -> Optional[Dict[str, Any]]:
    """Update task information"""
    try:
        db_service = await get_db_service()
        
        # Get current task
        current_task = await get_task_by_id(task_id)
        if not current_task:
            return None
        
        # Prepare update data
        update_data = task_update.dict(exclude_unset=True)
        
        # If status is being updated to completed, set completed_at
        if "status" in update_data and update_data["status"] == "completed":
            update_data["completed_at"] = date.today().strftime("%Y-%m-%d")
        
        # Update task in database
        result = await db_service.update("tasks", task_id, update_data)
        
        if result:
            logger.info(f"Task updated successfully: {task_id}")
            return result
        return None
        
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return None

async def delete_task(task_id: int) -> bool:
    """Delete a task"""
    try:
        db_service = await get_db_service()
        
        # Check if task exists
        current_task = await get_task_by_id(task_id)
        if not current_task:
            return False
        
        # Delete task from database
        result = await db_service.delete("tasks", task_id)
        
        if result:
            logger.info(f"Task deleted successfully: {task_id}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return False

async def create_daily_tasks(assigned_by: int, task_date: str) -> List[Dict[str, Any]]:
    """Create the three daily tasks: amenity list, emails, courtesy calls"""
    try:
        daily_tasks = [
            {
                "title": "Amenity List Check",
                "description": "Review and update the amenity list for guest services",
                "task_type": "amenity_list",
                "due_date": task_date
            },
            {
                "title": "Email Management",
                "description": "Check and respond to guest emails",
                "task_type": "emails",
                "due_date": task_date
            },
            {
                "title": "Courtesy Calls",
                "description": "Make courtesy calls to guests for follow-up",
                "task_type": "courtesy_calls",
                "due_date": task_date
            }
        ]
        
        created_tasks = []
        for task_data in daily_tasks:
            task = TaskCreate(
                title=task_data["title"],
                description=task_data["description"],
                task_type=task_data["task_type"],
                due_date=task_data["due_date"]
            )
            created_task = await create_task(task, assigned_by)
            if created_task:
                created_tasks.append(created_task)
        
        logger.info(f"Created {len(created_tasks)} daily tasks")
        return created_tasks
        
    except Exception as e:
        logger.error(f"Error creating daily tasks: {e}")
        return []

async def get_tasks_with_user_info() -> List[Dict[str, Any]]:
    """Get tasks with user information"""
    try:
        db_service = await get_db_service()
        tasks = await db_service.get_all("tasks")
        
        result_list = []
        for task in tasks:
            assigned_user = None
            assigner = None
            
            if task.get("assigned_to"):
                assigned_user = await db_service.get_by_id("users", task["assigned_to"])
            
            if task.get("assigned_by"):
                assigner = await db_service.get_by_id("users", task["assigned_by"])
            
            task_dict = {
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "task_type": task["task_type"],
                "assigned_to": task["assigned_to"],
                "assigned_by": task["assigned_by"],
                "due_date": task["due_date"],
                "status": task["status"],
                "created_at": task["created_at"],
                "completed_at": task["completed_at"],
                "assigned_user_name": assigned_user["name"] if assigned_user else None,
                "assigner_name": assigner["name"] if assigner else "Unknown"
            }
            result_list.append(task_dict)
        
        return result_list
        
    except Exception as e:
        logger.error(f"Error getting tasks with user info: {e}")
        return []
