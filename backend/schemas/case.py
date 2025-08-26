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

class CaseUpdate(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    action: Optional[str] = None
    owner_id: Optional[int] = None

class CaseResponse(CaseCreate):
    id: int

    class Config:
        from_attributes = True
