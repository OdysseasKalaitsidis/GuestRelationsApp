#!/usr/bin/env python3
"""
Debug script to test login functionality and identify issues
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import authenticate_user, get_user_by_username
from supabase_client import initialize_supabase, get_supabase

async def debug_login():
    """Debug the login functionality"""
    print("🔍 Debugging login functionality...")
    print("=" * 60)
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    print("✅ Supabase initialized")
    
    # Test 1: Check if user exists
    print("\n1. Checking if user 'diana' exists...")
    try:
        user = await get_user_by_username("diana")
        if user:
            print(f"✅ User found: {user}")
            print(f"   Username: {user.get('username')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Hashed password: {user.get('hashed_password', 'None')[:20]}...")
            print(f"   Is admin: {user.get('is_admin')}")
        else:
            print("❌ User 'diana' not found")
            return
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return
    
    # Test 2: Try authentication with correct password
    print("\n2. Testing authentication with password 'test123'...")
    try:
        auth_result = await authenticate_user("diana", "test123")
        if auth_result:
            print("✅ Authentication successful")
            print(f"   Authenticated user: {auth_result}")
        else:
            print("❌ Authentication failed - password might be wrong")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        print(f"   Error type: {type(e).__name__}")
    
    # Test 3: Try authentication with wrong password
    print("\n3. Testing authentication with wrong password...")
    try:
        auth_result = await authenticate_user("diana", "wrongpassword")
        if auth_result:
            print("❌ Authentication succeeded with wrong password (this is bad)")
        else:
            print("✅ Authentication correctly failed with wrong password")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
    
    # Test 4: Check all users in database
    print("\n4. Checking all users in database...")
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").execute()
        
        if response.data:
            print(f"✅ Found {len(response.data)} users:")
            for user in response.data:
                print(f"   - {user.get('username')} ({user.get('email')}) - Admin: {user.get('is_admin')}")
        else:
            print("❌ No users found in database")
    except Exception as e:
        print(f"❌ Error querying users: {e}")

if __name__ == "__main__":
    asyncio.run(debug_login())
