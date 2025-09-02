from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserResponse, UserUpdate
from services.user_service_supabase import (
    create_user, get_all_users, get_user_by_id, 
    update_user, delete_user
)
from routers.auth_route import get_current_admin_user, get_current_user
from typing import List

router = APIRouter()

@router.get("/users/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_user)):
    """Get all users (requires authentication)"""
    return await get_all_users()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get user by ID"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/users/", response_model=UserResponse)
async def create_new_user(
    user: UserCreate,
    current_user: dict = Depends(get_current_admin_user)
):
    """Create a new user (admin only)"""
    return await create_user(user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_info(
    user_id: int,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user information"""
    # Users can only update their own info unless they're admin
    if not current_user["is_admin"] and current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    user = await update_user(user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/users/{user_id}")
async def delete_user_account(
    user_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
