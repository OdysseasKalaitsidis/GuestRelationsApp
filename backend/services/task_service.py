from sqlalchemy.orm import Session
from models import Task, User
from schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from datetime import datetime, date

def create_task(db: Session, task: TaskCreate, assigned_by: int) -> Task:
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
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Get task by ID"""
    return db.query(Task).filter(Task.id == task_id).first()

def get_all_tasks(db: Session) -> List[Task]:
    """Get all tasks"""
    return db.query(Task).all()

def get_tasks_by_user(db: Session, user_id: int) -> List[Task]:
    """Get tasks assigned to a specific user"""
    return db.query(Task).filter(Task.assigned_to == user_id).all()

def get_tasks_by_date(db: Session, task_date: str) -> List[Task]:
    """Get tasks for a specific date"""
    return db.query(Task).filter(Task.due_date == task_date).all()

def get_tasks_by_type(db: Session, task_type: str) -> List[Task]:
    """Get tasks by type"""
    return db.query(Task).filter(Task.task_type == task_type).all()

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update task information"""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    
    # If status is being updated to completed, set completed_at
    if "status" in update_data and update_data["status"] == "completed":
        update_data["completed_at"] = date.today().strftime("%Y-%m-%d")
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task"""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

def create_daily_tasks(db: Session, assigned_by: int, task_date: str) -> List[Task]:
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
        created_task = create_task(db, task, assigned_by)
        created_tasks.append(created_task)
    
    return created_tasks

def get_tasks_with_user_info(db: Session) -> List[dict]:
    """Get tasks with user information"""
    tasks = db.query(Task).all()
    result = []
    
    for task in tasks:
        assigned_user = db.query(User).filter(User.id == task.assigned_to).first() if task.assigned_to else None
        assigner = db.query(User).filter(User.id == task.assigned_by).first()
        
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
        result.append(task_dict)
    
    return result
