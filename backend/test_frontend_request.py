#!/usr/bin/env python3
"""
Test frontend-like request
"""
import requests
import json

def test_frontend_request():
    """Test request like the frontend would make"""
    base_url = "https://guestrelationsapp.onrender.com/api"
    
    print("🔍 Testing frontend-like request...")
    print("=" * 50)
    
    # First, login to get a token
    print("\n1. Logging in to get token...")
    login_data = {
        "username": "admin",
        "password": "123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", data=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get("access_token")
            print("✅ Login successful")
            
            # Test users endpoint with token (like frontend would)
            print("\n2. Testing users endpoint with token...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Simulate browser request with Origin header
            browser_headers = {
                **headers,
                "Origin": "https://guestreationadomes.netlify.app",
                "Referer": "https://guestreationadomes.netlify.app/"
            }
            
            response = requests.get(f"{base_url}/users/", headers=browser_headers)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                users_data = response.json()
                print(f"✅ Users endpoint working! Found {len(users_data)} users")
                for user in users_data:
                    print(f"   - {user.get('username')} ({user.get('email')})")
            else:
                print(f"❌ Users endpoint failed: {response.text}")
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_frontend_request()
