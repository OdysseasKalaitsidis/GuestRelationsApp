# backend/routers/case_router.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from services.database_service import get_db_service
from services.case_service_supabase import create_case, bulk_create_cases, get_cases, get_case_by_id, get_cases_with_followups, update_case
from services.daily_service_supabase import reset_daily_cases
from services.anonymization_service import anonymization_service
from schemas.case import CaseCreate, CaseResponse, CaseUpdate
from routers.auth_route import get_current_admin_user, get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/cases", tags=["Cases"])

class ManualCaseInput(BaseModel):
    room: Optional[str] = None
    status: str = "Open"
    importance: str = "Medium"
    case_type: str = "General"
    title: str
    action: Optional[str] = None
    guest_name: Optional[str] = None
    description: Optional[str] = None

class CaseInputResponse(BaseModel):
    message: str
    case_data: dict
    anonymized: bool
    anonymization_summary: Optional[dict] = None

@router.post("/", response_model=CaseResponse)
async def create_single_case(case: CaseCreate, db_service = Depends(get_db_service)):
    """Create a single case"""
    return await create_case(case)

@router.post("/bulk", response_model=List[CaseResponse])
async def create_multiple_cases(cases: List[CaseCreate], db_service = Depends(get_db_service)):
    """Create multiple cases at once"""
    return await bulk_create_cases(cases)

@router.post("/manual", response_model=CaseInputResponse)
async def create_manual_case(
    case_input: ManualCaseInput,
    anonymize: bool = True,
    db_service = Depends(get_db_service)
):
    """
    Manually input case information when documents don't contain sufficient data
    
    This endpoint allows you to:
    - Input case details manually
    - Optionally anonymize the input
    - Create cases from scratch
    """
    try:
        # Validate input
        if not case_input.title or case_input.title.strip() == "":
            raise HTTPException(status_code=400, detail="Case title is required")
        
        # Prepare case data
        case_data = {
            "room": case_input.room,
            "status": case_input.status,
            "importance": case_input.importance,
            "type": case_input.case_type,
            "title": case_input.title,
            "action": case_input.action,
            "guest_name": case_input.guest_name,
            "description": case_input.description
        }
        
        # Anonymize if requested
        anonymization_summary = None
        if anonymize:
            # Anonymize text fields
            if case_data["title"]:
                case_data["title"] = anonymization_service.anonymize_text(case_data["title"])
            
            if case_data["action"]:
                case_data["action"] = anonymization_service.anonymize_text(case_data["action"])
            
            if case_data["description"]:
                case_data["description"] = anonymization_service.anonymize_text(case_data["description"])
            
            if case_data["guest_name"]:
                case_data["guest_name"] = anonymization_service.anonymize_text(case_data["guest_name"])
            
            # Get anonymization summary
            all_text = " ".join([str(v) for v in case_data.values() if v])
            anonymization_summary = anonymization_service.get_anonymization_stats(all_text)
        
        return CaseInputResponse(
            message=f"Case '{case_input.title}' created successfully",
            case_data=case_data,
            anonymized=anonymize,
            anonymization_summary=anonymization_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating manual case: {str(e)}")

@router.post("/template/{template_name}")
async def create_case_from_template(template_name: str = "default"):
    """
    Create a case from predefined templates
    
    Available templates:
    - default: Basic case template
    - complaint: Guest complaint template
    - maintenance: Maintenance request template
    - service: Service request template
    """
    
    templates = {
        "default": {
            "room": None,
            "status": "Open",
            "importance": "Medium",
            "case_type": "General",
            "title": "New Case - Please Update",
            "action": "Review and assign",
            "guest_name": None,
            "description": "Case created from template - please add details"
        },
        "complaint": {
            "room": None,
            "status": "Open",
            "importance": "High",
            "case_type": "Complaint",
            "title": "Guest Complaint - Requires Attention",
            "action": "Investigate and resolve",
            "guest_name": None,
            "description": "Guest complaint received - please investigate"
        },
        "maintenance": {
            "room": None,
            "status": "Open",
            "importance": "Medium",
            "case_type": "Maintenance",
            "title": "Maintenance Request",
            "action": "Schedule maintenance",
            "guest_name": None,
            "description": "Maintenance request - please schedule"
        },
        "service": {
            "room": None,
            "status": "Open",
            "importance": "Low",
            "case_type": "Service",
            "title": "Service Request",
            "action": "Provide service",
            "guest_name": None,
            "description": "Service request - please fulfill"
        }
    }
    
    if template_name not in templates:
        raise HTTPException(
            status_code=400, 
            detail=f"Template '{template_name}' not found. Available: {list(templates.keys())}"
        )
    
    template = templates[template_name]
    
    return {
        "message": f"Template '{template_name}' loaded successfully",
        "template": template,
        "customizable_fields": [
            "room", "title", "action", "guest_name", "description"
        ]
    }

@router.get("/", response_model=List[CaseResponse])
async def read_cases(db_service = Depends(get_db_service)):
    """Get all cases"""
    return await get_cases()

@router.get("/with-followups")
async def read_cases_with_followups(db_service = Depends(get_db_service)):
    """Get all cases with their associated followups"""
    return await get_cases_with_followups()

@router.post("/reset-daily")
async def reset_daily_cases_endpoint(
    db_service = Depends(get_db_service),
    current_user = Depends(get_current_admin_user)
):
    """Reset all cases, followups, and tasks for a new day (admin only)"""
    result = await reset_daily_cases()
    return result

# Parameterized routes must come LAST
@router.get("/{case_id}", response_model=CaseResponse)
async def read_case(case_id: int, db_service = Depends(get_db_service)):
    """Get a specific case by ID"""
    case = await get_case_by_id(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=CaseResponse)
async def update_case_endpoint(
    case_id: int, 
    case_update: CaseUpdate, 
    db_service = Depends(get_db_service),
    current_user = Depends(get_current_user)
):
    """Update a case (requires authentication)"""
    case = await update_case(case_id, case_update)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
