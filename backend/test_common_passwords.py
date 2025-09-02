#!/usr/bin/env python3
"""
Test common passwords for admin user
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import authenticate_user, get_user_by_username
from supabase_client import initialize_supabase

async def test_common_passwords():
    """Test common passwords for admin user"""
    print("🔍 Testing common passwords for admin user...")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    print("✅ Supabase initialized")
    
    # Test with admin user
    test_username = "admin"
    common_passwords = ["admin", "123", "password", "admin123", "123456", "qwerty", "letmein"]
    
    print(f"\n🔍 Testing login for user: '{test_username}'")
    
    # Step 1: Check if user exists
    print("\n1. Checking if user exists...")
    try:
        user = await get_user_by_username(test_username)
        if user:
            print(f"✅ User found: {user.get('username')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Is admin: {user.get('is_admin')}")
        else:
            print("❌ User not found")
            return
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return
    
    # Step 2: Try authentication with common passwords
    print("\n2. Testing authentication with common passwords...")
    for password in common_passwords:
        try:
            auth_result = await authenticate_user(test_username, password)
            if auth_result:
                print(f"✅ Authentication successful with password: '{password}'")
                print(f"   Authenticated user: {auth_result.get('username')}")
                return
            else:
                print(f"❌ Password '{password}' failed")
        except Exception as e:
            print(f"❌ Authentication error with '{password}': {e}")
    
    print("\n❌ None of the common passwords worked")
    print("💡 You may need to reset the password or check what the actual password is")
    
    print("\n" + "=" * 60)
    print("🎉 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_common_passwords())
