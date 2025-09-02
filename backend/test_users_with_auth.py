#!/usr/bin/env python3
"""
Test users endpoint with authentication
"""
import requests
import json

def test_users_with_auth():
    """Test the users endpoint with authentication"""
    base_url = "https://guestrelationsapp.onrender.com/api"
    
    print("🔍 Testing users endpoint with authentication...")
    print("=" * 50)
    
    # First, login to get a token
    print("\n1. Logging in...")
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
            
            # Test users endpoint with token
            print("\n2. Testing users endpoint with token...")
            headers = {"Authorization": f"Bearer {token}"}
            users_response = requests.get(f"{base_url}/users/", headers=headers)
            
            print(f"Users endpoint status: {users_response.status_code}")
            if users_response.status_code == 200:
                users_data = users_response.json()
                print(f"✅ Users endpoint working! Found {len(users_data)} users")
                for user in users_data:
                    print(f"   - {user.get('username')} ({user.get('email')}) - Admin: {user.get('is_admin')}")
            else:
                print(f"❌ Users endpoint failed: {users_response.text}")
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_users_with_auth()
