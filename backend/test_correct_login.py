#!/usr/bin/env python3
"""
Test login with correct username
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import authenticate_user, get_user_by_username
from supabase_client import initialize_supabase

async def test_correct_login():
    """Test login with correct username"""
    print("🔍 Testing login with correct username...")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    print("✅ Supabase initialized")
    
    # Test with correct username (capital D)
    test_username = "Diana"
    test_password = "password"
    
    print(f"\n🔍 Testing login for user: '{test_username}'")
    print(f"🔍 Password: '{test_password}'")
    
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
    
    # Step 2: Try authentication
    print("\n2. Testing authentication...")
    try:
        auth_result = await authenticate_user(test_username, test_password)
        if auth_result:
            print("✅ Authentication successful!")
            print(f"   Authenticated user: {auth_result.get('username')}")
        else:
            print("❌ Authentication failed - password might be wrong")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_correct_login())
