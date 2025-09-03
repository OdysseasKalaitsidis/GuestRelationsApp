#!/usr/bin/env python3
"""
Test login for all seed users to verify they work correctly
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import get_user_by_username
from services.security import verify_password
from supabase_client import initialize_supabase

async def test_seed_users():
    """Test login for all seed users"""
    print("🧪 Testing seed users login...")
    print("=" * 50)
    
    # Set environment variables
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return False
    
    print("✅ Supabase initialized")
    
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
    
    all_tests_passed = True
    
    for user_data in users_to_test:
        username = user_data["username"]
        password = user_data["password"]
        expected_admin = user_data["expected_admin"]
        
        print(f"\n🔍 Testing user: {username}")
        print("-" * 30)
        
        # Get user from database
        user = await get_user_by_username(username)
        if not user:
            print(f"❌ User '{username}' not found in database")
            all_tests_passed = False
            continue
        
        print(f"✅ User found: {user.get('name')}")
        print(f"📧 Email: {user.get('email')}")
        print(f"🆔 User ID: {user.get('id')}")
        print(f"👑 Admin: {user.get('is_admin')}")
        
        # Test password verification
        hashed_password = user.get('hashed_password')
        if not hashed_password:
            print(f"❌ No hashed password found for '{username}'")
            all_tests_passed = False
            continue
        
        password_valid = verify_password(password, hashed_password)
        if password_valid:
            print(f"✅ Password verification successful")
        else:
            print(f"❌ Password verification failed")
            all_tests_passed = False
        
        # Test admin status
        actual_admin = user.get('is_admin', False)
        if actual_admin == expected_admin:
            print(f"✅ Admin status correct: {actual_admin}")
        else:
            print(f"❌ Admin status incorrect: expected {expected_admin}, got {actual_admin}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All seed user tests passed!")
        print("\n📋 Summary of created users:")
        for user_data in users_to_test:
            print(f"• {user_data['username']} (Admin: {user_data['expected_admin']})")
    else:
        print("❌ Some tests failed!")
    
    return all_tests_passed

if __name__ == "__main__":
    asyncio.run(test_seed_users())
