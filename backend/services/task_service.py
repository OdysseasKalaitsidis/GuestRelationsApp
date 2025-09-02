from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Task, User
from schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from datetime import datetime, date

async def create_task(db: AsyncSession, task: TaskCreate, assigned_by: int) -> Task:
    """Create a new task"""
    today = date.today().strftime("%Y-%m-%d")
    
    db_task = Task(
        title=task.title,
        description=task.description,
        task_type=task.task_type,
        assigned_to=task.assigned_to,
        assigned_by=assigned_by,
        due_date=task.due_date,
        created_at=today,
        status="pending"
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[Task]:
    """Get task by ID"""
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()

async def get_all_tasks(db: AsyncSession) -> List[Task]:
    """Get all tasks"""
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_tasks_by_user(db: AsyncSession, user_id: int) -> List[Task]:
    """Get tasks assigned to a specific user"""
    result = await db.execute(select(Task).filter(Task.assigned_to == user_id))
    return result.scalars().all()

async def get_tasks_by_date(db: AsyncSession, task_date: str) -> List[Task]:
    """Get tasks for a specific date"""
    result = await db.execute(select(Task).filter(Task.due_date == task_date))
    return result.scalars().all()

async def get_tasks_by_type(db: AsyncSession, task_type: str) -> List[Task]:
    """Get tasks by type"""
    result = await db.execute(select(Task).filter(Task.task_type == task_type))
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update task information"""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    
    # If status is being updated to completed, set completed_at
    if "status" in update_data and update_data["status"] == "completed":
        update_data["completed_at"] = date.today().strftime("%Y-%m-%d")
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Delete a task"""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return False
    
    await db.delete(db_task)
    await db.commit()
    return True

async def create_daily_tasks(db: AsyncSession, assigned_by: int, task_date: str) -> List[Task]:
    """Create the three daily tasks: amenity list, emails, courtesy calls"""
    daily_tasks = [
        {
            "title": "Amenity List Check",
            "description": "Review and update the amenity list for guest services",
            "task_type": "amenity_list"
        },
        {
            "title": "Email Management",
            "description": "Check and respond to guest emails",
            "task_type": "emails"
        },
        {
            "title": "Courtesy Calls",
            "description": "Make courtesy calls to guests for follow-up",
            "task_type": "courtesy_calls"
        }
    ]
    
    created_tasks = []
    for task_data in daily_tasks:
        task = TaskCreate(
            title=task_data["title"],
            description=task_data["description"],
            task_type=task_data["task_type"],
            due_date=task_date
        )
        created_task = await create_task(db, task, assigned_by)
        created_tasks.append(created_task)
    
    return created_tasks

async def get_tasks_with_user_info(db: AsyncSession) -> List[dict]:
    """Get tasks with user information"""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    
    result_list = []
    for task in tasks:
        assigned_user = None
        assigner = None
        
        if task.assigned_to:
            user_result = await db.execute(select(User).filter(User.id == task.assigned_to))
            assigned_user = user_result.scalars().first()
        
        assigner_result = await db.execute(select(User).filter(User.id == task.assigned_by))
        assigner = assigner_result.scalars().first()
        
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "task_type": task.task_type,
            "assigned_to": task.assigned_to,
            "assigned_by": task.assigned_by,
            "due_date": task.due_date,
            "status": task.status,
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "assigned_user_name": assigned_user.name if assigned_user else None,
            "assigner_name": assigner.name if assigner else "Unknown"
        }
        result_list.append(task_dict)
    
    return result_list
