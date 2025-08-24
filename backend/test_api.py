#!/usr/bin/env python3
"""
Simple test script to verify API endpoints
Run this after starting the server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")

def test_cases_endpoint():
    """Test cases endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/cases/")
        print(f"✅ Cases endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Cases endpoint failed: {e}")

def test_followups_endpoint():
    """Test followups endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/followups/")
        print(f"✅ Followups endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Followups endpoint failed: {e}")

def test_workflow_endpoint():
    """Test workflow endpoint (without file upload)"""
    try:
        # This should fail without a file, but we can test the endpoint exists
        response = requests.post(f"{BASE_URL}/workflow/complete")
        print(f"✅ Workflow endpoint exists: {response.status_code}")
        if response.status_code == 422:  # Validation error (expected without file)
            print("   Expected validation error (no file provided)")
    except Exception as e:
        print(f"❌ Workflow endpoint failed: {e}")

def main():
    print("🧪 Testing Guest Relations API Endpoints")
    print("=" * 50)
    
    test_root()
    print()
    
    test_cases_endpoint()
    print()
    
    test_followups_endpoint()
    print()
    
    test_workflow_endpoint()
    print()
    
    print("🎯 Test completed! Check the results above.")

if __name__ == "__main__":
    main() 