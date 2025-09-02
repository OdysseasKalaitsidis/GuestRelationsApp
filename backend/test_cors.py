#!/usr/bin/env python3
"""
Test CORS with frontend domain
"""
import requests
import json

def test_cors():
    """Test CORS with frontend domain"""
    base_url = "https://guestrelationsapp.onrender.com/api"
    
    print("🔍 Testing CORS with frontend domain...")
    print("=" * 50)
    
    # Test 1: OPTIONS request (preflight)
    print("\n1. Testing OPTIONS request (preflight)...")
    try:
        headers = {
            "Origin": "https://guestreationadomes.netlify.app",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type"
        }
        response = requests.options(f"{base_url}/users/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ OPTIONS request successful")
        else:
            print(f"❌ OPTIONS request failed: {response.text}")
    except Exception as e:
        print(f"❌ OPTIONS request error: {e}")
    
    # Test 2: GET request with Origin header
    print("\n2. Testing GET request with Origin header...")
    try:
        headers = {
            "Origin": "https://guestreationadomes.netlify.app",
            "Authorization": "Bearer test_token"
        }
        response = requests.get(f"{base_url}/users/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if "Access-Control-Allow-Origin" in response.headers:
            print(f"✅ CORS headers present: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print("❌ CORS headers missing")
            
        if response.status_code == 401:
            print("✅ GET request successful (401 expected without valid token)")
        else:
            print(f"⚠️ GET request: {response.text}")
    except Exception as e:
        print(f"❌ GET request error: {e}")

if __name__ == "__main__":
    test_cors()
