#!/usr/bin/env python3
"""
Test PDF service directly
"""

from services.pdf_service import process_pdf
from fastapi import UploadFile
from io import BytesIO

def test_pdf_service():
    """Test the PDF service directly"""
    
    # Create a mock PDF file
    pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
    
    # Create a mock UploadFile
    mock_file = UploadFile(
        filename="test.pdf",
        file=BytesIO(pdf_content)
    )
    
    try:
        print("Testing PDF service...")
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
    test_pdf_service() 