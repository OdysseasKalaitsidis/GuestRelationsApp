#!/usr/bin/env python3
"""
Test the updated endpoints
"""
import requests
import json

def test_endpoints():
    """Test the updated endpoints"""
    base_url = "https://guestrelationsapp.onrender.com/api"
    
    print("🔍 Testing updated endpoints...")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test 2: Users endpoint (should return 401 without auth)
    print("\n2. Testing users endpoint...")
    try:
        response = requests.get(f"{base_url}/users/")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Users endpoint working (requires auth)")
        else:
            print(f"⚠️ Users endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Users endpoint error: {e}")
    
    # Test 3: Documents workflow endpoint (should return 422 for missing file)
    print("\n3. Testing documents workflow endpoint...")
    try:
        response = requests.post(f"{base_url}/documents/workflow")
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Documents workflow endpoint working (requires file)")
        else:
            print(f"⚠️ Documents workflow endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Documents workflow endpoint error: {e}")

if __name__ == "__main__":
    test_endpoints()
