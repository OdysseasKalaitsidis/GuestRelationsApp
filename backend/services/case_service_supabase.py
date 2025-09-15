# Case Service using Supabase Database Service
from typing import List, Optional, Dict, Any
from schemas.case import CaseCreate, CaseUpdate, CaseResponse
from services.database_service import get_db_service
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def create_case(case: CaseCreate) -> Optional[Dict[str, Any]]:
    """Create a new case using Supabase"""
    try:
        db_service = await get_db_service()
        
        # Prepare case data
        case_data = {
            "room": case.room,
            "status": case.status,
            "importance": case.importance,
            "type": case.type,
            "title": case.title,
            "action": case.action,
            "owner_id": case.owner_id,
            "created": case.created,
            "created_by": case.created_by,
            "modified": case.modified,
            "modified_by": case.modified_by,
            "source": case.source,
            "membership": case.membership,
            "case_description": case.case_description,
            "in_out": case.in_out,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Create case in database
        result = await db_service.create("cases", case_data)
        
        if result:
            logger.info(f"Case created successfully: {result['id']}")
            return result
        else:
            logger.error("Failed to create case: No data returned")
            raise Exception("Failed to create case: No data returned")
            
    except Exception as e:
        logger.error(f"Error creating case: {e}", exc_info=True)
        raise Exception(f"Case creation failed: {str(e)}")

async def bulk_create_cases(cases: List[CaseCreate]) -> List[Dict[str, Any]]:
    """Create multiple cases at once"""
    try:
        db_service = await get_db_service()
        created_cases = []
        
        logger.info(f"Starting bulk creation of {len(cases)} cases")
        
        for i, case in enumerate(cases):
            case_data = {
                "room": case.room,
                "status": case.status,
                "importance": case.importance,
                "type": case.type,
                "title": case.title,
                "action": case.action,
                "owner_id": case.owner_id,
                "created": case.created,
                "created_by": case.created_by,
                "modified": case.modified,
                "modified_by": case.modified_by,
                "source": case.source,
                "membership": case.membership,
                "case_description": case.case_description,
                "in_out": case.in_out,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            logger.debug(f"Creating case {i+1}/{len(cases)}: {case.title}")
            result = await db_service.create("cases", case_data)
            if result:
                created_cases.append(result)
                logger.info(f"Successfully created case {i+1}/{len(cases)}: {case.title} (ID: {result.get('id', 'unknown')})")
            else:
                logger.error(f"Failed to create case {i+1}/{len(cases)}: {case.title}")
                logger.error(f"Case data that failed: {case_data}")
                # Continue with other cases instead of failing completely
        
        logger.info(f"Bulk creation completed: {len(created_cases)}/{len(cases)} cases created successfully")
        if len(created_cases) < len(cases):
            logger.warning(f"Some cases failed to create: {len(cases) - len(created_cases)} failures")
        return created_cases
        
    except Exception as e:
        logger.error(f"Error bulk creating cases: {e}", exc_info=True)
        raise Exception(f"Bulk case creation failed: {str(e)}")

async def get_cases() -> List[Dict[str, Any]]:
    """Get all cases"""
    try:
        db_service = await get_db_service()
        cases = await db_service.get_all("cases")
        return cases
    except Exception as e:
        logger.error(f"Error getting cases: {e}")
        return []

async def get_case_by_id(case_id: int) -> Optional[Dict[str, Any]]:
    """Get case by ID"""
    try:
        db_service = await get_db_service()
        case = await db_service.get_by_id("cases", case_id)
        return case
    except Exception as e:
        logger.error(f"Error getting case by ID: {e}")
        return None

async def get_cases_with_followups() -> List[Dict[str, Any]]:
    """Get all cases with their associated followups and user information"""
    try:
        db_service = await get_db_service()
        cases_with_followups = await db_service.get_cases_with_followups()
        return cases_with_followups
    except Exception as e:
        logger.error(f"Error getting cases with followups: {e}")
        return []

async def update_case(case_id: int, case_update: CaseUpdate) -> Optional[Dict[str, Any]]:
    """Update case information"""
    try:
        db_service = await get_db_service()
        
        # Get current case
        current_case = await get_case_by_id(case_id)
        if not current_case:
            return None
        
        # Prepare update data
        update_data = case_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update case in database
        result = await db_service.update("cases", case_id, update_data)
        
        if result:
            logger.info(f"Case updated successfully: {case_id}")
            return result
        return None
        
    except Exception as e:
        logger.error(f"Error updating case: {e}")
        return None

async def delete_case(case_id: int) -> bool:
    """Delete a case"""
    try:
        db_service = await get_db_service()
        
        # Check if case exists
        current_case = await get_case_by_id(case_id)
        if not current_case:
            return False
        
        # Delete case from database
        result = await db_service.delete("cases", case_id)
        
        if result:
            logger.info(f"Case deleted successfully: {case_id}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error deleting case: {e}")
        return False
