from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str  # amenity_list, emails, courtesy_calls
    assigned_to: Optional[int] = None
    due_date: str  # YYYY-MM-DD format

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[str] = None
    assigned_to: Optional[int] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    task_type: str
    assigned_to: Optional[int] = None
    assigned_by: int
    due_date: str
    status: str
    created_at: str
    completed_at: Optional[str] = None

    class Config:
        from_attributes = True

class TaskWithUser(TaskResponse):
    assigned_user_name: Optional[str] = None
    assigner_name: str
