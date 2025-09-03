#!/usr/bin/env python3
"""
Test script to verify that document upload automatically clears all previous data
and creates new cases and followups with proper case IDs.
"""

import asyncio
import os
import tempfile
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
import json

# Load environment variables
load_dotenv()

def create_test_pdf():
    """Create a simple test PDF with case data"""
    # This is a minimal PDF content that should trigger case creation
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Room 101 - Guest Complaint) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000180 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
242
%%EOF"""
    
    return pdf_content

async def test_document_upload_with_clear():
    """Test that document upload clears all previous data and creates new cases/followups"""
    try:
        print("🧪 Testing document upload with automatic data clearing...")
        
        # Create test client
        client = TestClient(app)
        
        # Step 1: First, let's check if there's any existing data
        print("\n📊 Step 1: Checking initial data state...")
        
        # Check cases
        cases_response = client.get("/api/cases/")
        initial_cases = cases_response.json() if cases_response.status_code == 200 else []
        print(f"   Initial cases: {len(initial_cases)}")
        
        # Check followups
        followups_response = client.get("/api/followups/with-case-info")
        initial_followups = followups_response.json() if followups_response.status_code == 200 else []
        print(f"   Initial followups: {len(initial_followups)}")
        
        # Step 2: Create test PDF file
        print("\n📄 Step 2: Creating test PDF...")
        test_pdf_content = create_test_pdf()
        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(test_pdf_content)
            temp_file_path = temp_file.name
        
        try:
            # Step 3: Upload document using the workflow endpoint
            print("\n📤 Step 3: Uploading document with workflow...")
            
            with open(temp_file_path, "rb") as pdf_file:
                files = {"file": ("test_cases.pdf", pdf_file, "application/pdf")}
                response = client.post("/api/documents/workflow", files=files)
            
            print(f"   Upload response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Upload successful!")
                print(f"   Cases created: {result.get('cases_created', 0)}")
                print(f"   Followups created: {result.get('followups_created', 0)}")
                print(f"   Steps: {len(result.get('steps', []))}")
                
                # Print workflow steps for debugging
                for i, step in enumerate(result.get('steps', [])):
                    print(f"     Step {i+1}: {step['step']} - {step['status']} - {step['message']}")
                
            else:
                print(f"   ❌ Upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
            # Step 4: Verify that new data was created
            print("\n📊 Step 4: Verifying new data creation...")
            
            # Check cases again
            cases_response = client.get("/api/cases/")
            new_cases = cases_response.json() if cases_response.status_code == 200 else []
            print(f"   New cases: {len(new_cases)}")
            
            # Check followups again
            followups_response = client.get("/api/followups/with-case-info")
            new_followups = followups_response.json() if followups_response.status_code == 200 else []
            print(f"   New followups: {len(new_followups)}")
            
            # Step 5: Verify that followups have proper case IDs
            print("\n🔍 Step 5: Verifying followup case IDs...")
            
            if new_followups:
                for i, followup in enumerate(new_followups[:3]):  # Check first 3 followups
                    case_id = followup.get('case_id')
                    room_info = followup.get('room') or (followup.get('cases', {}).get('room') if followup.get('cases') else None)
                    case_title = followup.get('cases', {}).get('title') if followup.get('cases') else 'No title'
                    
                    print(f"   Followup {i+1}:")
                    print(f"     Case ID: {case_id}")
                    print(f"     Room: {room_info}")
                    print(f"     Case Title: {case_title}")
                    print(f"     Suggestion: {followup.get('suggestion_text', 'No suggestion')[:50]}...")
                    
                    # Verify that case_id exists
                    if not case_id:
                        print(f"     ❌ ERROR: Followup missing case_id!")
                        return False
                    else:
                        print(f"     ✅ Case ID present: {case_id}")
            else:
                print("   ⚠️ No followups created - this might be expected if no cases were created")
            
            # Step 6: Test second upload to verify clearing works
            print("\n🔄 Step 6: Testing second upload to verify data clearing...")
            
            # Create a different test PDF
            test_pdf_content_2 = create_test_pdf()  # Same content for simplicity
            
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file_2:
                temp_file_2.write(test_pdf_content_2)
                temp_file_path_2 = temp_file_2.name
            
            try:
                with open(temp_file_path_2, "rb") as pdf_file_2:
                    files_2 = {"file": ("test_cases_2.pdf", pdf_file_2, "application/pdf")}
                    response_2 = client.post("/api/documents/workflow", files=files_2)
                
                print(f"   Second upload response status: {response_2.status_code}")
                
                if response_2.status_code == 200:
                    result_2 = response_2.json()
                    print(f"   ✅ Second upload successful!")
                    print(f"   Cases created: {result_2.get('cases_created', 0)}")
                    print(f"   Followups created: {result_2.get('followups_created', 0)}")
                    
                    # Check final data state
                    final_cases_response = client.get("/api/cases/")
                    final_cases = final_cases_response.json() if final_cases_response.status_code == 200 else []
                    
                    final_followups_response = client.get("/api/followups/with-case-info")
                    final_followups = final_followups_response.json() if final_followups_response.status_code == 200 else []
                    
                    print(f"   Final cases: {len(final_cases)}")
                    print(f"   Final followups: {len(final_followups)}")
                    
                    # Verify that data was cleared and recreated
                    if len(final_cases) == result_2.get('cases_created', 0) and len(final_followups) == result_2.get('followups_created', 0):
                        print("   ✅ Data clearing and recreation verified!")
                        return True
                    else:
                        print("   ❌ Data clearing verification failed!")
                        return False
                else:
                    print(f"   ❌ Second upload failed: {response_2.status_code}")
                    return False
                    
            finally:
                # Clean up second temp file
                if os.path.exists(temp_file_path_2):
                    os.unlink(temp_file_path_2)
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Error testing document upload: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_followup_case_id_display():
    """Test that followups display case IDs correctly in the frontend"""
    try:
        print("\n🧪 Testing followup case ID display...")
        
        # Create test client
        client = TestClient(app)
        
        # Get followups with case info
        response = client.get("/api/followups/with-case-info")
        
        if response.status_code == 200:
            followups = response.json()
            print(f"   Found {len(followups)} followups")
            
            if followups:
                print("   Sample followup data structure:")
                sample_followup = followups[0]
                print(f"     Followup ID: {sample_followup.get('id')}")
                print(f"     Case ID: {sample_followup.get('case_id')}")
                print(f"     Room: {sample_followup.get('room')}")
                print(f"     Cases object: {sample_followup.get('cases')}")
                
                # Verify the data structure is correct for frontend
                has_case_id = 'case_id' in sample_followup
                has_cases_object = 'cases' in sample_followup
                
                print(f"     Has case_id: {has_case_id}")
                print(f"     Has cases object: {has_cases_object}")
                
                if has_case_id and has_cases_object:
                    print("   ✅ Followup data structure is correct for frontend display")
                    return True
                else:
                    print("   ❌ Followup data structure is missing required fields")
                    return False
            else:
                print("   ⚠️ No followups found to test")
                return True
        else:
            print(f"   ❌ Failed to get followups: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing followup case ID display: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Running document upload and followup tests...")
    
    # Test document upload with automatic clearing
    upload_test_passed = await test_document_upload_with_clear()
    
    # Test followup case ID display
    display_test_passed = await test_followup_case_id_display()
    
    print("\n🏁 Test Results:")
    print(f"   Document upload with clearing: {'✅ PASSED' if upload_test_passed else '❌ FAILED'}")
    print(f"   Followup case ID display: {'✅ PASSED' if display_test_passed else '❌ FAILED'}")
    
    if upload_test_passed and display_test_passed:
        print("\n🎉 All tests passed! The system is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
