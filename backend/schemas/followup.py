from pydantic import BaseModel
from typing import Optional
from enum import Enum

class FollowupStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"

class FollowupBase(BaseModel):
    suggestion_text: str
    status: FollowupStatus = FollowupStatus.pending
    assigned_to: Optional[int] = None  # User ID

class FollowupCreate(FollowupBase):
    case_id: int

class FollowupUpdate(FollowupBase):
    pass

class FollowupOut(FollowupBase):
    id: int
    case_id: int

    class Config:
        from_attributes = True
