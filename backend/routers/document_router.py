import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from services.document_service import process_document
from services.ai_service import suggest_feedback
from services.case_service_supabase import bulk_create_cases
from services.followup_service_supabase import create_followup
from schemas.case import CaseCreate
from schemas.followup import FollowupCreate
from pydantic import BaseModel
from typing import List, Optional

logger = logging.getLogger(__name__)

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

import time

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF or DOCX file, process it, and return structured cases as JSON.
    This endpoint now automatically clears existing data before processing the new document.
    """
    start_time = time.time()
    
    # Check file extension
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400, 
            detail="File must be a PDF (.pdf) or Word document (.docx)"
        )
    
    try:
        # Step 0: Clear all previous data before processing new document
        from services.daily_service_supabase import clear_all_data, verify_data_cleared
        
        try:
            # Clear data and wait for completion
            clear_result = await clear_all_data()
            print(f"✅ Data cleared successfully: {clear_result['message']}")
            
            # Wait a moment for database to settle
            import asyncio
            await asyncio.sleep(1)
            
            # Verify data is actually cleared
            verification = await verify_data_cleared()
            if verification['is_cleared']:
                print(f"✅ Verification passed: Database is empty")
            else:
                print(f"⚠️ Warning: {verification['message']}")
                # If verification fails, try clearing again
                if verification['total_remaining'] > 0:
                    print(f"🔄 Retrying data clearance...")
                    await clear_all_data()
                    await asyncio.sleep(1)
                    verification = await verify_data_cleared()
                    if verification['is_cleared']:
                        print(f"✅ Second clearance attempt successful")
                    else:
                        print(f"❌ Failed to clear data after retry: {verification['message']}")
        except Exception as clear_error:
            print(f"⚠️ Warning: Could not clear existing data: {clear_error}")
            # Continue with upload even if clearing fails
        
        # Step 1: Process the document (optimized)
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
        
        # If no cases found, provide helpful feedback
        if not api_cases:
            return DocumentUploadResponse(
                cases=[],
                message=f"No cases found in {file.filename}. The document may not contain case data in the expected format, or the parsing may have failed. Please check the document content and try again."
            )
        
        processing_time = time.time() - start_time
        return DocumentUploadResponse(
            cases=api_cases,
            message=f"Successfully processed {len(api_cases)} cases from {file.filename} in {processing_time:.2f}s"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {str(e)}"
        )

@router.post("/workflow", response_model=CompleteWorkflowResponse)
async def complete_workflow(
    file: UploadFile = File(...),
    create_cases: bool = True
):
    """
    Complete workflow: Upload PDF → Process → AI Feedback → Create Cases → Create Followups
    """
    steps = []
    
    try:
        # Step 0: Clear all previous data
        from services.daily_service_supabase import clear_all_data, verify_data_cleared
        
        clear_result = await clear_all_data()
        steps.append(WorkflowStep(
            step="Data Clearance",
            status="success",
            message=clear_result["message"],
            data=clear_result
        ))
        
        # Wait a moment for database to settle
        import asyncio
        await asyncio.sleep(1)
        
        # Verify data is actually cleared
        verification = await verify_data_cleared()
        if verification['is_cleared']:
            steps.append(WorkflowStep(
                step="Data Verification",
                status="success",
                message="Database verified empty - ready for new data",
                data=verification
            ))
        else:
            # If verification fails, try clearing again
            if verification['total_remaining'] > 0:
                steps.append(WorkflowStep(
                    step="Data Retry",
                    status="warning",
                    message=f"Retrying data clearance - {verification['message']}",
                    data=verification
                ))
                
                await clear_all_data()
                await asyncio.sleep(1)
                verification = await verify_data_cleared()
                
                if verification['is_cleared']:
                    steps.append(WorkflowStep(
                        step="Data Verification",
                        status="success",
                        message="Database verified empty after retry - ready for new data",
                        data=verification
                    ))
                else:
                    steps.append(WorkflowStep(
                        step="Data Verification",
                        status="error",
                        message=f"Failed to clear data after retry: {verification['message']}",
                        data=verification
                    ))
            else:
                steps.append(WorkflowStep(
                    step="Data Verification",
                    status="warning",
                    message=f"Warning: {verification['message']}",
                    data=verification
                ))
        
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
                message="No cases found in document - document may not contain case data in expected format",
                data={"cases_count": 0}
            ))
            
            # Return early with no cases created but provide helpful message
            return CompleteWorkflowResponse(
                steps=steps,
                cases_created=0,
                followups_created=0,
                final_message="Document processed successfully but no cases were found. This could be because: 1) The document doesn't contain case data in the expected format, 2) The parsing logic couldn't extract the data properly, 3) The document structure is different from what the system expects. Please check the document content and ensure it contains case information with fields like Guest, Room, Status, etc."
            )
        
        steps.append(WorkflowStep(
            step="PDF Parsing",
            status="success",
            message=f"Extracted {len(cases_data)} cases from PDF",
            data={"cases_count": len(cases_data), "cases": cases_data}
        ))
        
        # Step 2: Generate AI Feedback
        try:
            from services.ai_service import suggest_feedback, check_openai_available
            
            # Check if OpenAI is available
            is_available, message = check_openai_available()
            if is_available:
                ai_suggestions = suggest_feedback(cases_data)
                steps.append(WorkflowStep(
                    step="AI Feedback",
                    status="success",
                    message=f"Generated AI suggestions for {len(ai_suggestions)} cases",
                    data={"suggestions_count": len(ai_suggestions), "suggestions": ai_suggestions}
                ))
            else:
                # Create default suggestions when AI is not available
                ai_suggestions = [
                    {
                        "case_id": i,
                        "suggestion_text": "Please review this case and determine appropriate follow-up action.",
                        "confidence": 0.0,
                        "case_data": case
                    }
                    for i, case in enumerate(cases_data)
                ]
                steps.append(WorkflowStep(
                    step="AI Feedback",
                    status="warning",
                    message=f"AI suggestions not available: {message}. Using default suggestions.",
                    data={"suggestions_count": len(ai_suggestions), "suggestions": ai_suggestions}
                ))
        except Exception as e:
            print(f"Error generating AI suggestions: {e}")
            # Create default suggestions on error
            ai_suggestions = [
                {
                    "case_id": i,
                    "suggestion_text": "Please review this case and determine appropriate follow-up action.",
                    "confidence": 0.0,
                    "case_data": case
                }
                for i, case in enumerate(cases_data)
            ]
            steps.append(WorkflowStep(
                step="AI Feedback",
                status="warning",
                message=f"AI suggestions failed: {str(e)}. Using default suggestions.",
                data={"suggestions_count": len(ai_suggestions), "suggestions": ai_suggestions}
            ))
        
        # Step 3: Create Cases in Database (only if create_cases is True)
        created_cases = []
        if create_cases:
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
                    guest=case_data.get("guest"),
                    created=case_data.get("created"),
                    created_by=case_data.get("created_by"),
                    modified=case_data.get("modified"),
                    modified_by=case_data.get("modified_by"),
                    source=case_data.get("source"),
                    membership=case_data.get("membership"),
                    case_description=case_data.get("case_description"),
                    in_out=case_data.get("in_out"),
                    owner_id=None  # Explicitly set to None for now
                )
                
                case_objects.append(case_obj)
            
            created_cases = await bulk_create_cases(case_objects)
        steps.append(WorkflowStep(
            step="Case Creation",
            status="success",
            message=f"Created {len(created_cases)} cases in database",
            data={"cases_created": len(created_cases), "cases": cases_data}
        ))
        
        # Step 4: Create Followups with AI Suggestions (only if create_cases is True)
        followups_created = 0
        if create_cases:
            for i, case in enumerate(created_cases):
                if i < len(ai_suggestions):
                    try:
                        followup_data = FollowupCreate(
                            case_id=case['id'],  # Use dictionary access since case is a dict
                            suggestion_text=ai_suggestions[i].get("suggestion_text", "No AI suggestion available")
                        )
                        result = await create_followup(followup_data)
                        if result:
                            followups_created += 1
                            logger.info(f"Created followup {followups_created} for case {case['id']}")
                        else:
                            logger.error(f"Failed to create followup for case {case['id']}")
                    except Exception as e:
                        logger.error(f"Error creating followup for case {case['id']}: {e}")
                        # Continue with other followups instead of failing completely
        
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

# Clear all data endpoint
@router.post("/clear-all-data")
async def clear_all_data_endpoint():
    """
    Clear all data from the database - cases, followups, and tasks
    """
    try:
        from services.daily_service_supabase import clear_all_data
        result = await clear_all_data()
        return {
            "message": "All data cleared successfully",
            "details": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error clearing data: {str(e)}"
        )

# Debug endpoint to test AI suggestions
@router.post("/debug/test-ai-suggestions")
async def test_ai_suggestions():
    """
    Debug endpoint to test AI suggestion generation
    """
    try:
        from services.ai_service import suggest_feedback
        
        # Sample case data for testing
        test_cases = [
            {
                "room": "101",
                "status": "OPEN",
                "importance": "HIGH",
                "type": "NEGATIVE",
                "title": "Noisy Neighbors Complaint",
                "case_description": "Guest complained about noisy neighbors and requested room change",
                "action": "Contacted front desk to arrange room change"
            },
            {
                "room": "205",
                "status": "PENDING",
                "importance": "MEDIUM",
                "type": "NEUTRAL",
                "title": "Amenity Request",
                "case_description": "Guest requested additional towels and toiletries",
                "action": "Delivered requested items to room"
            }
        ]
        
        suggestions = suggest_feedback(test_cases)
        
        return {
            "message": f"Successfully generated {len(suggestions)} AI suggestions",
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error testing AI suggestions: {str(e)}"
        )

# Debug endpoint to help troubleshoot parsing issues
@router.post("/debug/extract-text")
async def debug_extract_text(file: UploadFile = File(...)):
    """
    Debug endpoint to extract and return raw text from document for troubleshooting
    """
    try:
        from services.document_service import extract_text_from_pdf, extract_text_from_docx
        
        if file.filename.lower().endswith('.pdf'):
            raw_text = extract_text_from_pdf(file)
        elif file.filename.lower().endswith('.docx'):
            raw_text = extract_text_from_docx(file)
        else:
            raise HTTPException(
                status_code=400, 
                detail="File must be a PDF (.pdf) or Word document (.docx)"
            )
        
        return {
            "filename": file.filename,
            "text_length": len(raw_text),
            "text_preview": raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text,
            "message": f"Successfully extracted {len(raw_text)} characters from {file.filename}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error extracting text: {str(e)}"
        )

# Legacy endpoint for backward compatibility
@router.post("/pdf/upload", response_model=DocumentUploadResponse)
async def upload_pdf_legacy(file: UploadFile = File(...)):
    """
    Legacy endpoint for PDF uploads - now redirects to document upload.
    """
    return await upload_document(file)
