#!/usr/bin/env python3
"""
Test script to check if the clear-all-data endpoint works correctly
"""

import asyncio
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

# Load environment variables
load_dotenv()

async def test_clear_all_data_endpoint():
    """Test the clear-all-data endpoint"""
    try:
        print("🔍 Testing clear-all-data endpoint...")
        
        # Create test client
        client = TestClient(app)
        
        # Test the endpoint
        response = client.post("/api/documents/clear-all-data")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Clear-all-data endpoint successful")
            return True
        else:
            print(f"❌ Clear-all-data endpoint failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing clear-all-data endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cases_endpoint():
    """Test the cases endpoint"""
    try:
        print("\n🔍 Testing cases endpoint...")
        
        # Create test client
        client = TestClient(app)
        
        # Test the endpoint
        response = client.get("/api/cases/")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            cases = response.json()
            print(f"✅ Cases endpoint successful: {len(cases)} cases found")
            return True
        else:
            print(f"❌ Cases endpoint failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing cases endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🧪 Running endpoint tests...")
    
    # Test cases endpoint
    await test_cases_endpoint()
    
    # Test clear-all-data endpoint
    await test_clear_all_data_endpoint()
    
    print("\n🏁 Tests completed")

if __name__ == "__main__":
    asyncio.run(main())
