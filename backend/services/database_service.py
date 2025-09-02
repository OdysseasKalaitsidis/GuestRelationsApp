# Database Service using Supabase Client
from typing import List, Optional, Dict, Any, Union
from supabase_client import get_supabase
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseService:
    """Database service using Supabase client instead of SQLAlchemy"""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    def _handle_response(self, response, operation: str):
        """Handle Supabase response and log results"""
        if response.data is not None:
            logger.info(f"{operation} successful")
            return response.data
        else:
            logger.error(f"{operation} failed: {response.error if hasattr(response, 'error') else 'Unknown error'}")
            return None
    
    # Generic CRUD operations
    async def create(self, table: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new record"""
        try:
            response = self.supabase.table(table).insert(data).execute()
            result = self._handle_response(response, f"Create in {table}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error creating record in {table}: {e}")
            return None
    
    async def get_by_id(self, table: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Get record by ID"""
        try:
            response = self.supabase.table(table).select("*").eq("id", record_id).execute()
            result = self._handle_response(response, f"Get by ID from {table}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting record from {table}: {e}")
            return None
    
    async def get_all(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all records with optional filters"""
        try:
            query = self.supabase.table(table).select("*")
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.execute()
            result = self._handle_response(response, f"Get all from {table}")
            return result or []
        except Exception as e:
            logger.error(f"Error getting records from {table}: {e}")
            return []
    
    async def update(self, table: str, record_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record"""
        try:
            response = self.supabase.table(table).update(data).eq("id", record_id).execute()
            result = self._handle_response(response, f"Update in {table}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error updating record in {table}: {e}")
            return None
    
    async def delete(self, table: str, record_id: int) -> bool:
        """Delete a record"""
        try:
            response = self.supabase.table(table).delete().eq("id", record_id).execute()
            result = self._handle_response(response, f"Delete from {table}")
            return result is not None
        except Exception as e:
            logger.error(f"Error deleting record from {table}: {e}")
            return False
    
    # Specific table operations
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            response = self.supabase.table("users").select("*").eq("username", username).execute()
            result = self._handle_response(response, "Get user by username")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            response = self.supabase.table("users").select("*").eq("email", email).execute()
            result = self._handle_response(response, "Get user by email")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_cases_with_followups(self) -> List[Dict[str, Any]]:
        """Get cases with their followups"""
        try:
            # First get all cases
            cases_response = self.supabase.table("cases").select("*").execute()
            cases = self._handle_response(cases_response, "Get cases")
            
            if not cases:
                return []
            
            # Get followups for all cases
            followups_response = self.supabase.table("followups").select("*").execute()
            followups = self._handle_response(followups_response, "Get followups") or []
            
            # Group followups by case_id
            followups_by_case = {}
            for followup in followups:
                case_id = followup.get("case_id")
                if case_id not in followups_by_case:
                    followups_by_case[case_id] = []
                followups_by_case[case_id].append(followup)
            
            # Add followups to cases
            for case in cases:
                case["followups"] = followups_by_case.get(case.get("id"), [])
            
            return cases
        except Exception as e:
            logger.error(f"Error getting cases with followups: {e}")
            return []
    
    async def get_followups_with_case_info(self) -> List[Dict[str, Any]]:
        """Get followups with case information"""
        try:
            # Get followups with case info using join-like query
            response = self.supabase.table("followups").select("*, cases(*)").execute()
            result = self._handle_response(response, "Get followups with case info")
            return result or []
        except Exception as e:
            logger.error(f"Error getting followups with case info: {e}")
            return []
    
    async def get_tasks_with_case_info(self) -> List[Dict[str, Any]]:
        """Get tasks with case information"""
        try:
            response = self.supabase.table("tasks").select("*, cases(*)").execute()
            result = self._handle_response(response, "Get tasks with case info")
            return result or []
        except Exception as e:
            logger.error(f"Error getting tasks with case info: {e}")
            return []
    
    async def get_documents_with_case_info(self) -> List[Dict[str, Any]]:
        """Get documents with case information"""
        try:
            response = self.supabase.table("documents").select("*, cases(*)").execute()
            result = self._handle_response(response, "Get documents with case info")
            return result or []
        except Exception as e:
            logger.error(f"Error getting documents with case info: {e}")
            return []

# Global database service instance
db_service = DatabaseService()

# Dependency function for FastAPI
async def get_db_service():
    """Get database service instance for dependency injection"""
    return db_service
