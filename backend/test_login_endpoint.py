#!/usr/bin/env python3
"""
Test actual login endpoint for all seed users
"""
import asyncio
import os
import sys
import requests
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_login_endpoint():
    """Test login endpoint for all seed users"""
    print("🌐 Testing login endpoint for seed users...")
    print("=" * 50)
    
    # Define users to test
    users_to_test = [
        {
            "username": "diana",
            "password": "dianadoc",
            "expected_admin": True
        },
        {
            "username": "aggeliki", 
            "password": "aggelikidoc",
            "expected_admin": True
        },
        {
            "username": "odysseas",
            "password": "odyssseas", 
            "expected_admin": False
        }
    ]
    
    # Base URL for the API
    base_url = "http://localhost:8000"
    
    all_tests_passed = True
    
    for user_data in users_to_test:
        username = user_data["username"]
        password = user_data["password"]
        expected_admin = user_data["expected_admin"]
        
        print(f"\n🔍 Testing login for: {username}")
        print("-" * 30)
        
        # Prepare login data as form data
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            # Make login request with form data
            response = requests.post(f"{base_url}/auth/login", data=login_data)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Login successful!")
                print(f"📧 User: {data.get('user', {}).get('name', 'N/A')}")
                print(f"👑 Admin: {data.get('user', {}).get('is_admin', 'N/A')}")
                print(f"🎫 Token: {data.get('access_token', 'N/A')[:20]}...")
                
                # Check admin status
                actual_admin = data.get('user', {}).get('is_admin', False)
                if actual_admin == expected_admin:
                    print(f"✅ Admin status correct: {actual_admin}")
                else:
                    print(f"❌ Admin status incorrect: expected {expected_admin}, got {actual_admin}")
                    all_tests_passed = False
                    
            else:
                print(f"❌ Login failed with status {response.status_code}")
                print(f"Response: {response.text}")
                all_tests_passed = False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Could not connect to server at {base_url}")
            print("Make sure the backend server is running!")
            all_tests_passed = False
        except Exception as e:
            print(f"❌ Error during login test: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All login endpoint tests passed!")
    else:
        print("❌ Some login tests failed!")
    
    return all_tests_passed

if __name__ == "__main__":
    asyncio.run(test_login_endpoint())
