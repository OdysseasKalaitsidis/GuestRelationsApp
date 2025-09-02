#!/usr/bin/env python3
"""
Test the exact URLs that the frontend should be using
"""
import requests
import json

def test_frontend_urls():
    """Test the exact URLs that the frontend should be using"""
    base_url = "https://guestrelationsapp.onrender.com/api"
    
    print("🔍 Testing frontend URLs...")
    print("=" * 50)
    
    # Test 1: Users endpoint
    print("\n1. Testing users endpoint...")
    try:
        response = requests.get(f"{base_url}/users/")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Users endpoint accessible (requires auth)")
        else:
            print(f"⚠️ Users endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Users endpoint error: {e}")
    
    # Test 2: Documents workflow endpoint
    print("\n2. Testing documents workflow endpoint...")
    try:
        response = requests.post(f"{base_url}/documents/workflow")
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Documents workflow endpoint accessible (requires file)")
        else:
            print(f"⚠️ Documents workflow endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Documents workflow endpoint error: {e}")
    
    # Test 3: Cases endpoint
    print("\n3. Testing cases endpoint...")
    try:
        response = requests.get(f"{base_url}/cases/")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Cases endpoint accessible (requires auth)")
        else:
            print(f"⚠️ Cases endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Cases endpoint error: {e}")
    
    # Test 4: Health endpoint
    print("\n4. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

if __name__ == "__main__":
    test_frontend_urls()
