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
        try:
            if response.data is not None:
                logger.info(f"{operation} successful")
                return response.data
            else:
                error_msg = response.error if hasattr(response, 'error') else 'Unknown error'
                logger.error(f"{operation} failed: {error_msg}")
                if hasattr(response, 'error'):
                    logger.error(f"Supabase error details: {response.error}")
                return None
        except Exception as e:
            logger.error(f"Error handling response for {operation}: {e}")
            return None
    
    # Generic CRUD operations
    async def create(self, table: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new record"""
        try:
            # Remove None values to avoid database errors, but keep empty strings and 0 values
            clean_data = {k: v for k, v in data.items() if v is not None}
            
            logger.debug(f"Creating record in {table} with data: {clean_data}")
            response = self.supabase.table(table).insert(clean_data).execute()
            result = self._handle_response(response, f"Create in {table}")
            
            if result and len(result) > 0:
                logger.debug(f"Successfully created record in {table}: {result[0]}")
                return result[0]
            else:
                logger.error(f"Create in {table} failed: No data returned")
                logger.error(f"Original data: {data}")
                logger.error(f"Cleaned data: {clean_data}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating record in {table}: {e}", exc_info=True)
            return None
    
    async def get_by_field(self, table: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Get records by field value"""
        try:
            response = self.supabase.table(table).select("*").eq(field, value).execute()
            result = self._handle_response(response, f"Get by {field} from {table}")
            return result or []
        except Exception as e:
            logger.error(f"Error getting records by {field} from {table}: {e}")
            return []

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
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            response = self.supabase.table("users").select("*").eq("id", user_id).execute()
            result = self._handle_response(response, "Get user by ID")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None

    async def get_cases_with_followups(self) -> List[Dict[str, Any]]:
        """Get cases with their followups and user information"""
        try:
            # Get cases first
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
            
            # Get unique user IDs from cases
            user_ids = set()
            for case in cases:
                if case.get("owner_id"):
                    user_ids.add(case["owner_id"])
            
            # Fetch user data for all assigned users
            users_data = {}
            if user_ids:
                users_response = self.supabase.table("users").select("id, name, username").in_("id", list(user_ids)).execute()
                users = self._handle_response(users_response, "Get users")
                if users:
                    users_data = {user["id"]: user for user in users}
            
            # Add followups and user info to cases
            for case in cases:
                case["followups"] = followups_by_case.get(case.get("id"), [])
                
                # Add user information
                owner_id = case.get("owner_id")
                if owner_id and owner_id in users_data:
                    case["users"] = users_data[owner_id]
                    case["assigned_user_name"] = users_data[owner_id].get("name", "Unknown")
                    logger.debug(f"Case {case.get('id')} assigned to user: {case['assigned_user_name']}")
                elif owner_id:
                    case["assigned_user_name"] = f"User {owner_id}"
                    logger.debug(f"Case {case.get('id')} has owner_id but no user data: {owner_id}")
                else:
                    case["assigned_user_name"] = "Unassigned"
                    logger.debug(f"Case {case.get('id')} is unassigned")
            
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
