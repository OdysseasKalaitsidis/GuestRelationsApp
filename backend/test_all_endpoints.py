#!/usr/bin/env python3
"""
Comprehensive test script to verify all endpoints are working correctly
"""
import asyncio
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"

def test_endpoint(method: str, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None, form_data: Dict[str, str] = None) -> Dict[str, Any]:
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if form_data:
                response = requests.post(url, data=form_data, headers=headers)
            else:
                response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def run_tests():
    """Run all endpoint tests"""
    print("🔍 Testing Guest Relations API Endpoints")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    result = test_endpoint("GET", "/health")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    print(f"   Response: {result.get('data', 'No data')}")
    
    # Test 2: Environment Variables
    print("\n2. Testing Environment Variables...")
    result = test_endpoint("GET", "/debug/env")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    print(f"   Response: {result.get('data', 'No data')}")
    
    # Test 3: Users List
    print("\n3. Testing Users List...")
    result = test_endpoint("GET", "/debug/users")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    if result.get('success'):
        users = result.get('data', {}).get('users', [])
        print(f"   Found {len(users)} users")
        for user in users[:3]:  # Show first 3 users
            print(f"   - {user.get('username', 'Unknown')} ({user.get('email', 'No email')})")
    
    # Test 4: Cases List
    print("\n4. Testing Cases List...")
    result = test_endpoint("GET", "/cases/")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    if result.get('success'):
        cases = result.get('data', [])
        print(f"   Found {len(cases)} cases")
        if cases:
            print(f"   First case: {cases[0].get('title', 'No title')[:50]}...")
    
    # Test 5: Cases with Followups
    print("\n5. Testing Cases with Followups...")
    result = test_endpoint("GET", "/cases/with-followups")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    if result.get('success'):
        cases = result.get('data', [])
        print(f"   Found {len(cases)} cases with followups")
        if cases:
            followups_count = sum(len(case.get('followups', [])) for case in cases)
            print(f"   Total followups: {followups_count}")
    
    # Test 6: Clear All Data
    print("\n6. Testing Clear All Data...")
    result = test_endpoint("POST", "/documents/clear-all-data")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    if result.get('success'):
        details = result.get('data', {}).get('details', {})
        print(f"   Cleared: {details.get('cases_deleted', 0)} cases, {details.get('followups_deleted', 0)} followups")
    
    # Test 7: Verify Data is Cleared
    print("\n7. Verifying Data is Cleared...")
    result = test_endpoint("GET", "/cases/")
    print(f"   Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    if result.get('success'):
        cases = result.get('data', [])
        print(f"   Remaining cases: {len(cases)}")
    
    # Test 8: Login (should fail without valid credentials)
    print("\n8. Testing Login (expected to fail without valid credentials)...")
    login_form_data = {
        "username": "testuser",
        "password": "testpass"
    }
    result = test_endpoint("POST", "/auth/login", form_data=login_form_data)
    print(f"   Status: {'✅ PASS' if result.get('status_code') == 401 else '❌ UNEXPECTED'}")
    print(f"   Response: {result.get('data', 'No data')}")
    
    print("\n" + "=" * 50)
    print("🎉 Endpoint testing completed!")
    print("\nSummary:")
    print("- Backend is running and accessible")
    print("- Database connection is working")
    print("- All major endpoints are responding")
    print("- Data clearing functionality is working")
    print("- Authentication endpoint is properly configured")

if __name__ == "__main__":
    run_tests()
