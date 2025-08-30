from pydantic import BaseModel
from typing import Optional

class CaseCreate(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: str
    action: Optional[str] = None
    owner_id: Optional[int] = None
    # New fields for AI parsing
    guest: Optional[str] = None
    created: Optional[str] = None
    created_by: Optional[str] = None
    modified: Optional[str] = None
    modified_by: Optional[str] = None
    source: Optional[str] = None
    membership: Optional[str] = None
    case_description: Optional[str] = None
    in_out: Optional[str] = None

class CaseUpdate(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    action: Optional[str] = None
    owner_id: Optional[int] = None
    # New fields for AI parsing
    guest: Optional[str] = None
    created: Optional[str] = None
    created_by: Optional[str] = None
    modified: Optional[str] = None
    modified_by: Optional[str] = None
    source: Optional[str] = None
    membership: Optional[str] = None
    case_description: Optional[str] = None
    in_out: Optional[str] = None

class CaseResponse(CaseCreate):
    id: int

    class Config:
        from_attributes = True
