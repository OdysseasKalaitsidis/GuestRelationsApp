import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from services.document_service import process_document
from services.ai_service import suggest_feedback
from services.case_service import bulk_create_cases
from services.followup_service import create_followup
from schemas.case import CaseCreate
from schemas.followup import FollowupCreate
from pydantic import BaseModel
from typing import List, Optional
from db import get_db

router = APIRouter(prefix="/documents", tags=["Documents"])

class CaseData(BaseModel):
    room: Optional[str] = None
    status: Optional[str] = None
    importance: Optional[str] = None
    type: Optional[str] = None
    title: str
    action: Optional[str] = None
    guest: Optional[str] = None
    created: Optional[str] = None
    created_by: Optional[str] = None
    modified: Optional[str] = None
    modified_by: Optional[str] = None
    source: Optional[str] = None
    membership: Optional[str] = None
    case_description: Optional[str] = None
    in_out: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    cases: List[CaseData]
    message: str

class WorkflowStep(BaseModel):
    step: str
    status: str
    message: str
    data: dict = {}

class CompleteWorkflowResponse(BaseModel):
    steps: List[WorkflowStep]
    cases_created: int
    followups_created: int
    final_message: str

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF or DOCX file, process it, and return structured cases as JSON.
    """
    # Check file extension
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400, 
            detail="File must be a PDF (.pdf) or Word document (.docx)"
        )
    
    try:
        raw_cases = process_document(file)
        
        # Convert raw cases to API format
        api_cases = []
        for case in raw_cases:
            api_case = CaseData(
                room=case.get('room'),
                status=case.get('status'),
                importance=case.get('importance'),
                type=case.get('type'),
                title=case.get('title', 'Untitled Case'),
                action=case.get('action'),
                guest=case.get('guest'),
                created=case.get('created'),
                created_by=case.get('created_by'),
                modified=case.get('modified'),
                modified_by=case.get('modified_by'),
                source=case.get('source'),
                membership=case.get('membership'),
                case_description=case.get('case_description'),
                in_out=case.get('in_out')
            )
            api_cases.append(api_case)
        
        return DocumentUploadResponse(
            cases=api_cases,
            message=f"Successfully processed {len(api_cases)} cases from {file.filename}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {str(e)}"
        )

@router.post("/workflow", response_model=CompleteWorkflowResponse)
async def complete_workflow(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Complete workflow: Upload PDF → Process → AI Feedback → Create Cases → Create Followups
    """
    steps = []
    
    try:
        # Step 1: Process PDF
        steps.append(WorkflowStep(
            step="PDF Processing",
            status="success",
            message="PDF uploaded and processed successfully",
            data={}
        ))
        
        cases_data = process_document(file)
        
        # Handle case where no cases are found
        if not cases_data:
            steps.append(WorkflowStep(
                step="PDF Parsing",
                status="warning",
                message="No cases found in PDF - document may not contain case data",
                data={"cases_count": 0}
            ))
            
            # Return early with no cases created
            return CompleteWorkflowResponse(
                steps=steps,
                cases_created=0,
                followups_created=0,
                final_message="PDF processed successfully but no cases were found. Please check the document content."
            )
        
        steps.append(WorkflowStep(
            step="PDF Parsing",
            status="success",
            message=f"Extracted {len(cases_data)} cases from PDF",
            data={"cases_count": len(cases_data), "cases": cases_data}
        ))
        
        # Step 2: Generate AI Feedback
        ai_suggestions = suggest_feedback(cases_data)
        steps.append(WorkflowStep(
            step="AI Feedback",
            status="success",
            message=f"Generated AI suggestions for {len(ai_suggestions)} cases",
            data={"suggestions_count": len(ai_suggestions)}
        ))
        
        # Step 3: Create Cases in Database
        case_objects = []
        for case_data in cases_data:
            # Ensure title is never empty
            title = case_data.get("title") or case_data.get("case") or "Untitled Case"
            
            # Map the data properly, handling potential field name mismatches
            case_obj = CaseCreate(
                room=case_data.get("room"),
                status=case_data.get("status") or "pending",
                importance=case_data.get("importance") or "medium",
                type=case_data.get("type") or "other",
                title=title,
                action=case_data.get("action") or case_data.get("action_text"),
                owner_id=None  # Explicitly set to None for now
            )
            
            case_objects.append(case_obj)
        
        created_cases = bulk_create_cases(db, case_objects)
        steps.append(WorkflowStep(
            step="Case Creation",
            status="success",
            message=f"Created {len(created_cases)} cases in database",
            data={"cases_created": len(created_cases), "cases": cases_data}
        ))
        
        # Step 4: Create Followups with AI Suggestions
        followups_created = 0
        for i, case in enumerate(created_cases):
            if i < len(ai_suggestions):
                followup_data = FollowupCreate(
                    case_id=case.id,
                    suggestion_text=ai_suggestions[i].get("suggestion_text", "No AI suggestion available"),
                    status="pending"
                )
                create_followup(db, followup_data)
                followups_created += 1
        
        steps.append(WorkflowStep(
            step="Followup Creation",
            status="success",
            message=f"Created {followups_created} followups with AI suggestions",
            data={"followups_created": followups_created}
        ))
        
        return CompleteWorkflowResponse(
            steps=steps,
            cases_created=len(created_cases),
            followups_created=followups_created,
            final_message="Workflow completed successfully! All cases and followups have been created."
        )
        
    except Exception as e:
        # Add error step
        steps.append(WorkflowStep(
            step="Error",
            status="error",
            message=f"Workflow failed: {str(e)}",
            data={"error": str(e)}
        ))
        
        raise HTTPException(
            status_code=500,
            detail=f"Workflow failed at step: {steps[-1].step}. Error: {str(e)}"
        )

# Legacy endpoint for backward compatibility
@router.post("/pdf/upload", response_model=DocumentUploadResponse)
async def upload_pdf_legacy(file: UploadFile = File(...)):
    """
    Legacy endpoint for PDF uploads - now redirects to document upload.
    """
    return await upload_document(file)
