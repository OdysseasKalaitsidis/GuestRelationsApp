#!/usr/bin/env python3
"""
Simple test to check login functionality
"""
import requests
import json

def test_login():
    """Test login with the deployed API"""
    url = "https://guestrelationsapp.onrender.com/api/auth/login"
    
    # Test data
    data = {
        "username": "diana",
        "password": "test123"
    }
    
    print("🔍 Testing login with deployed API...")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            response_data = response.json()
            print(f"User: {response_data.get('user', {}).get('username')}")
            print(f"Token: {response_data.get('access_token', '')[:20]}...")
        else:
            print("❌ Login failed")
            try:
                error_data = response.json()
                print(f"Error detail: {error_data.get('detail', 'Unknown error')}")
            except:
                print("Could not parse error response")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_login()
