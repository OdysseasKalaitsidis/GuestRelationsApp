from pydantic import BaseModel
from typing import Optional

class FollowupBase(BaseModel):
    suggestion_text: str
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
