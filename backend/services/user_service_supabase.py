# User Service using Supabase Client
from typing import List, Optional, Dict, Any
from schemas.user import UserCreate, UserUpdate
from services.security import hash_password, verify_password
from supabase_client import get_supabase
import logging

logger = logging.getLogger(__name__)

async def create_user(user: UserCreate) -> Optional[Dict[str, Any]]:
    """Create a new user using Supabase"""
    try:
        supabase = get_supabase()
        
        # Hash the password
        hashed_password = hash_password(user.password)
        
        # Prepare user data
        user_data = {
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "hashed_password": hashed_password,
            "is_admin": user.is_admin
        }
        
        # Insert user into Supabase
        response = supabase.table("users").insert(user_data).execute()
        
        if response.data:
            logger.info(f"User created successfully: {user.username}")
            return response.data[0]
        else:
            logger.error("Failed to create user: No data returned")
            return None
            
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username using Supabase"""
    try:
        logger.info(f"Looking up user by username: {username}")
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("username", username).execute()
        
        logger.info(f"Supabase response: {response}")
        if response.data:
            logger.info(f"User found: {response.data[0]}")
            return response.data[0]
        logger.warning(f"No user found with username: {username}")
        return None
        
    except Exception as e:
        logger.error(f"Error getting user by username {username}: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error args: {e.args}")
        return None

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email using Supabase"""
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("email", email).execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID using Supabase"""
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

async def get_all_users() -> List[Dict[str, Any]]:
    """Get all users using Supabase"""
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").execute()
        
        return response.data or []
        
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

async def update_user(user_id: int, user_update: UserUpdate) -> Optional[Dict[str, Any]]:
    """Update user information using Supabase"""
    try:
        supabase = get_supabase()
        
        # Get current user
        current_user = await get_user_by_id(user_id)
        if not current_user:
            return None
        
        # Prepare update data
        update_data = user_update.dict(exclude_unset=True)
        
        # Hash password if it's being updated
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        
        # Update user in Supabase
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        if response.data:
            logger.info(f"User updated successfully: {user_id}")
            return response.data[0]
        return None
        
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return None

async def delete_user(user_id: int) -> bool:
    """Delete a user using Supabase"""
    try:
        supabase = get_supabase()
        
        # Check if user exists
        current_user = await get_user_by_id(user_id)
        if not current_user:
            return False
        
        # Delete user from Supabase
        response = supabase.table("users").delete().eq("id", user_id).execute()
        
        if response.data:
            logger.info(f"User deleted successfully: {user_id}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return False

async def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user with username and password using Supabase"""
    try:
        logger.info(f"Attempting to authenticate user: {username}")
        user = await get_user_by_username(username)
        if not user:
            logger.warning(f"User not found: {username}")
            return None
        
        logger.info(f"User found: {username}, checking password...")
        # Verify password
        if not verify_password(password, user["hashed_password"]):
            logger.warning(f"Invalid password for user: {username}")
            return None
        
        logger.info(f"Authentication successful for user: {username}")
        return user
        
    except Exception as e:
        logger.error(f"Error authenticating user {username}: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error args: {e.args}")
        return None
