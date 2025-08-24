from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

# Schema for reading user data (response)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True

# Schema for updating user info
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
