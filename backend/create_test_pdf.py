#!/usr/bin/env python3
"""
Create a test PDF with case data
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def create_test_pdf():
    """Create a test PDF with case data"""
    
    # Create a PDF with case data
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add some case data
    p.drawString(100, 750, "Guest Relations Cases")
    p.drawString(100, 720, "[NAME]: John Smith")
    p.drawString(100, 700, "Room: 101")
    p.drawString(100, 680, "Status: pending")
    p.drawString(100, 660, "Importance: high")
    p.drawString(100, 640, "Type: complaint")
    p.drawString(100, 620, "Case: Guest reported noisy neighbors")
    p.drawString(100, 600, "Action: Security team notified")
    
    p.drawString(100, 550, "[NAME]: Sarah Johnson")
    p.drawString(100, 530, "Room: 205")
    p.drawString(100, 510, "Status: in_progress")
    p.drawString(100, 490, "Importance: medium")
    p.drawString(100, 470, "Type: maintenance")
    p.drawString(100, 450, "Case: Air conditioning not working")
    p.drawString(100, 430, "Action: Maintenance team dispatched")
    
    p.save()
    buffer.seek(0)
    return buffer

def test_with_real_pdf():
    """Test the workflow with a realistic PDF"""
    
    # Create test PDF
    pdf_buffer = create_test_pdf()
    
    # Test PDF service
    from services.pdf_service import process_pdf
    from fastapi import UploadFile
    
    mock_file = UploadFile(
        filename="test_cases.pdf",
        file=pdf_buffer
    )
    
    try:
        print("Testing PDF service with realistic data...")
        cases = process_pdf(mock_file)
        print(f"Cases extracted: {len(cases)}")
        print(f"Cases data: {cases}")
        
        # Test CaseCreate validation
        from schemas.case import CaseCreate
        for case_data in cases:
            try:
                case_obj = CaseCreate(**case_data)
                print(f"✅ CaseCreate validation passed: {case_obj}")
            except Exception as e:
                print(f"❌ CaseCreate validation failed: {e}")
                print(f"   Case data: {case_data}")
                
    except Exception as e:
        print(f"Error in PDF service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_real_pdf() 