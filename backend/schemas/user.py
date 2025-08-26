from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

# Schema for reading user data (response)
class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True

# Schema for updating user info
class UserUpdate(BaseModel):
    username: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]

# Schema for login
class UserLogin(BaseModel):
    username: str
    password: str
