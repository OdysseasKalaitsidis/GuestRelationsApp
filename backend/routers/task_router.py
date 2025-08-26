from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithUser
from services.task_service import (
    create_task, get_all_tasks, get_task_by_id, 
    update_task, delete_task, create_daily_tasks, get_tasks_with_user_info
)
from routers.auth_route import get_current_admin_user, get_current_user
from typing import List

router = APIRouter()

@router.get("/tasks/", response_model=List[TaskWithUser])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks (requires authentication)"""
    tasks_with_info = get_tasks_with_user_info(db)
    return tasks_with_info

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task by ID"""
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.post("/tasks/", response_model=TaskResponse)
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new task (admin only)"""
    return create_task(db, task, current_user.id)

@router.post("/tasks/daily", response_model=List[TaskResponse])
def create_daily_tasks_endpoint(
    task_date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create daily tasks for a specific date (admin only)"""
    try:
        # Validate date format (YYYY-MM-DD)
        from datetime import datetime
        datetime.strptime(task_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    return create_daily_tasks(db, current_user.id, task_date)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_info(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task information"""
    task = update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/tasks/{task_id}")
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a task (admin only)"""
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

@router.get("/tasks/user/{user_id}", response_model=List[TaskResponse])
def get_user_tasks(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks assigned to a specific user"""
    # Users can only see their own tasks unless they're admin
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own tasks"
        )
    
    from services.task_service import get_tasks_by_user
    return get_tasks_by_user(db, user_id)
