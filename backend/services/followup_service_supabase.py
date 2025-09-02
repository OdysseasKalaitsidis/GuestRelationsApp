# Followup Service using Supabase Database Service
from typing import List, Optional, Dict, Any
from schemas.followup import FollowupCreate, FollowupUpdate, FollowupOut
from services.database_service import get_db_service
from services.anonymization_service import anonymization_service
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def create_followup(followup: FollowupCreate) -> Optional[Dict[str, Any]]:
    """Create a new followup using Supabase"""
    try:
        db_service = await get_db_service()
        
        # Prepare followup data
        followup_data = {
            "case_id": followup.case_id,
            "room": followup.room,
            "suggestion_text": followup.suggestion_text,
            "assigned_to": followup.assigned_to,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Create followup in database
        result = await db_service.create("followups", followup_data)
        
        if result:
            logger.info(f"Followup created successfully: {result['id']}")
            return result
        else:
            logger.error("Failed to create followup: No data returned")
            return None
            
    except Exception as e:
        logger.error(f"Error creating followup: {e}")
        return None

async def get_all_followups() -> List[Dict[str, Any]]:
    """Get all followups"""
    try:
        db_service = await get_db_service()
        followups = await db_service.get_all("followups")
        return followups
    except Exception as e:
        logger.error(f"Error getting followups: {e}")
        return []

async def get_followup_by_id(followup_id: int) -> Optional[Dict[str, Any]]:
    """Get followup by ID"""
    try:
        db_service = await get_db_service()
        followup = await db_service.get_by_id("followups", followup_id)
        return followup
    except Exception as e:
        logger.error(f"Error getting followup by ID: {e}")
        return None

async def get_followups_with_case_info() -> List[Dict[str, Any]]:
    """Get all followups with case information"""
    try:
        db_service = await get_db_service()
        followups_with_case_info = await db_service.get_followups_with_case_info()
        return followups_with_case_info
    except Exception as e:
        logger.error(f"Error getting followups with case info: {e}")
        return []

async def update_followup(followup_id: int, followup_update: FollowupUpdate) -> Optional[Dict[str, Any]]:
    """Update followup information"""
    try:
        db_service = await get_db_service()
        
        # Get current followup
        current_followup = await get_followup_by_id(followup_id)
        if not current_followup:
            return None
        
        # Prepare update data
        update_data = followup_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update followup in database
        result = await db_service.update("followups", followup_id, update_data)
        
        if result:
            logger.info(f"Followup updated successfully: {followup_id}")
            return result
        return None
        
    except Exception as e:
        logger.error(f"Error updating followup: {e}")
        return None

async def delete_followup(followup_id: int) -> bool:
    """Delete a followup"""
    try:
        db_service = await get_db_service()
        
        # Check if followup exists
        current_followup = await get_followup_by_id(followup_id)
        if not current_followup:
            return False
        
        # Delete followup from database
        result = await db_service.delete("followups", followup_id)
        
        if result:
            logger.info(f"Followup deleted successfully: {followup_id}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error deleting followup: {e}")
        return False

async def get_anonymized_followups() -> List[Dict[str, Any]]:
    """Get all followups with anonymized case information"""
    try:
        db_service = await get_db_service()
        followups_with_case_info = await db_service.get_followups_with_case_info()
        
        # Anonymize case information
        anonymized_followups = []
        for followup in followups_with_case_info:
            anonymized_followup = followup.copy()
            
            # Anonymize case title and description if they exist
            if "cases" in followup and followup["cases"]:
                case = followup["cases"]
                if case.get("title"):
                    anonymized_followup["anonymized_case_title"] = anonymization_service.anonymize_text(case["title"])
                if case.get("description"):
                    anonymized_followup["anonymized_case_description"] = anonymization_service.anonymize_text(case["description"])
            
            anonymized_followups.append(anonymized_followup)
        
        return anonymized_followups
    except Exception as e:
        logger.error(f"Error getting anonymized followups: {e}")
        return []

async def anonymize_existing_followup_text(followup_id: int) -> Optional[Dict[str, Any]]:
    """Anonymize the text of an existing followup"""
    try:
        db_service = await get_db_service()
        
        # Get current followup
        current_followup = await get_followup_by_id(followup_id)
        if not current_followup:
            return None
        
        # Anonymize suggestion text
        anonymized_text = anonymization_service.anonymize_text(current_followup["suggestion_text"])
        
        # Update followup with anonymized text
        update_data = {
            "suggestion_text": anonymized_text,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = await db_service.update("followups", followup_id, update_data)
        
        if result:
            logger.info(f"Followup text anonymized successfully: {followup_id}")
            return result
        return None
        
    except Exception as e:
        logger.error(f"Error anonymizing followup text: {e}")
        return None

async def bulk_anonymize_followups(followup_ids: List[int]) -> List[Dict[str, Any]]:
    """Bulk anonymize multiple followups"""
    try:
        anonymized_followups = []
        
        for followup_id in followup_ids:
            result = await anonymize_existing_followup_text(followup_id)
            if result:
                anonymized_followups.append(result)
        
        logger.info(f"Bulk anonymized {len(anonymized_followups)} followups")
        return anonymized_followups
        
    except Exception as e:
        logger.error(f"Error bulk anonymizing followups: {e}")
        return []

async def get_followup_anonymization_stats() -> Dict[str, Any]:
    """Get anonymization statistics for followups"""
    try:
        db_service = await get_db_service()
        followups = await db_service.get_all("followups")
        
        total_followups = len(followups)
        anonymized_count = 0
        
        for followup in followups:
            # Check if suggestion text contains anonymized patterns
            text = followup.get("suggestion_text", "")
            if "[PERSON]" in text or "[EMAIL]" in text or "[PHONE]" in text:
                anonymized_count += 1
        
        return {
            "total_followups": total_followups,
            "anonymized_count": anonymized_count,
            "anonymization_percentage": (anonymized_count / total_followups * 100) if total_followups > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting followup anonymization stats: {e}")
        return {"total_followups": 0, "anonymized_count": 0, "anonymization_percentage": 0}

async def create_followup_from_anonymized_data(anonymized_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a followup from anonymized data"""
    try:
        db_service = await get_db_service()
        
        # Prepare followup data from anonymized data
        followup_data = {
            "case_id": anonymized_data.get("case_id"),
            "room": anonymized_data.get("room"),
            "suggestion_text": anonymized_data.get("suggestion_text", ""),
            "assigned_to": anonymized_data.get("assigned_to"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Create followup in database
        result = await db_service.create("followups", followup_data)
        
        if result:
            logger.info(f"Followup created from anonymized data: {result['id']}")
            return result
        else:
            logger.error("Failed to create followup from anonymized data: No data returned")
            return None
            
    except Exception as e:
        logger.error(f"Error creating followup from anonymized data: {e}")
        return None
