#!/usr/bin/env python3
"""
Test script to verify frontend followup functionality
"""

import asyncio
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
import json

# Load environment variables
load_dotenv()

async def test_frontend_followup_api():
    """Test the API endpoints that the frontend uses for followups"""
    try:
        print("🧪 Testing frontend followup API endpoints...")
        
        # Create test client
        client = TestClient(app)
        
        # Test 1: Get followups with case info (used by frontend)
        print("\n📊 Test 1: Testing /api/followups/with-case-info endpoint...")
        
        response = client.get("/api/followups/with-case-info")
        
        if response.status_code == 200:
            followups = response.json()
            print(f"   ✅ Successfully retrieved {len(followups)} followups")
            
            if followups:
                # Check the structure of the first followup
                sample_followup = followups[0]
                print("   Sample followup structure:")
                print(f"     id: {sample_followup.get('id')}")
                print(f"     case_id: {sample_followup.get('case_id')}")
                print(f"     room: {sample_followup.get('room')}")
                print(f"     suggestion_text: {sample_followup.get('suggestion_text', '')[:50]}...")
                print(f"     assigned_to: {sample_followup.get('assigned_to')}")
                print(f"     cases: {sample_followup.get('cases') is not None}")
                
                # Verify required fields for frontend
                required_fields = ['id', 'case_id', 'suggestion_text', 'cases']
                missing_fields = [field for field in required_fields if field not in sample_followup]
                
                if missing_fields:
                    print(f"   ❌ Missing required fields: {missing_fields}")
                    return False
                else:
                    print("   ✅ All required fields present")
            else:
                print("   ⚠️ No followups found (this might be expected)")
        else:
            print(f"   ❌ Failed to get followups: {response.status_code}")
            return False
        
        # Test 2: Test followup update endpoint
        print("\n✏️ Test 2: Testing followup update endpoint...")
        
        if followups:
            # Get the first followup to update
            followup_id = followups[0]['id']
            update_data = {
                "suggestion_text": "Updated suggestion for testing",
                "assigned_to": 1
            }
            
            response = client.put(f"/api/followups/{followup_id}", json=update_data)
            
            if response.status_code == 200:
                updated_followup = response.json()
                print(f"   ✅ Successfully updated followup {followup_id}")
                print(f"   Updated suggestion: {updated_followup.get('suggestion_text')}")
                print(f"   Updated assigned_to: {updated_followup.get('assigned_to')}")
            else:
                print(f"   ❌ Failed to update followup: {response.status_code}")
                return False
        else:
            print("   ⚠️ No followups available for update test")
        
        # Test 3: Test followup delete endpoint
        print("\n🗑️ Test 3: Testing followup delete endpoint...")
        
        if followups:
            # Get the first followup to delete
            followup_id = followups[0]['id']
            
            response = client.delete(f"/api/followups/{followup_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Successfully deleted followup {followup_id}")
                print(f"   Delete result: {result}")
            else:
                print(f"   ❌ Failed to delete followup: {response.status_code}")
                return False
        else:
            print("   ⚠️ No followups available for delete test")
        
        print("\n✅ All frontend followup API tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing frontend followup API: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_document_upload_clears_data():
    """Test that document upload properly clears all data"""
    try:
        print("\n🧪 Testing document upload data clearing...")
        
        # Create test client
        client = TestClient(app)
        
        # Check initial data
        print("\n📊 Checking initial data...")
        
        cases_response = client.get("/api/cases/")
        initial_cases = cases_response.json() if cases_response.status_code == 200 else []
        
        followups_response = client.get("/api/followups/with-case-info")
        initial_followups = followups_response.json() if followups_response.status_code == 200 else []
        
        print(f"   Initial cases: {len(initial_cases)}")
        print(f"   Initial followups: {len(initial_followups)}")
        
        # Test clear all data endpoint
        print("\n🗑️ Testing clear all data endpoint...")
        
        clear_response = client.post("/api/documents/clear-all-data")
        
        if clear_response.status_code == 200:
            clear_result = clear_response.json()
            print(f"   ✅ Data cleared successfully")
            print(f"   Clear result: {clear_result}")
        else:
            print(f"   ❌ Failed to clear data: {clear_response.status_code}")
            return False
        
        # Verify data is cleared
        print("\n📊 Verifying data is cleared...")
        
        cases_response = client.get("/api/cases/")
        final_cases = cases_response.json() if cases_response.status_code == 200 else []
        
        followups_response = client.get("/api/followups/with-case-info")
        final_followups = followups_response.json() if followups_response.status_code == 200 else []
        
        print(f"   Final cases: {len(final_cases)}")
        print(f"   Final followups: {len(final_followups)}")
        
        if len(final_cases) == 0 and len(final_followups) == 0:
            print("   ✅ All data successfully cleared!")
            return True
        else:
            print("   ❌ Data not fully cleared!")
            return False
        
    except Exception as e:
        print(f"❌ Error testing document upload data clearing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🧪 Running frontend followup functionality tests...")
    
    # Test frontend followup API
    api_test_passed = await test_frontend_followup_api()
    
    # Test document upload data clearing
    clear_test_passed = await test_document_upload_clears_data()
    
    print("\n🏁 Test Results:")
    print(f"   Frontend followup API: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    print(f"   Document upload data clearing: {'✅ PASSED' if clear_test_passed else '❌ FAILED'}")
    
    if api_test_passed and clear_test_passed:
        print("\n🎉 All frontend functionality tests passed!")
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
