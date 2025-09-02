#!/usr/bin/env python3
"""
Test login functionality with detailed error reporting
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import authenticate_user
from supabase_client import initialize_supabase

async def test_login_functionality():
    """Test the login functionality with detailed error reporting"""
    print("🔍 Testing login functionality...")
    print("=" * 60)
    
    # Set environment variables
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    os.environ["SUPABASE_ANON_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    print("📋 Environment variables set")
    
    # Test 1: Initialize Supabase
    print("\n1. Testing Supabase initialization...")
    try:
        if initialize_supabase():
            print("✅ Supabase initialized successfully")
        else:
            print("❌ Supabase initialization failed")
            return False
    except Exception as e:
        print(f"❌ Supabase initialization error: {e}")
        return False
    
    # Test 2: Test authentication
    print("\n2. Testing authentication...")
    try:
        # Try to authenticate with a test user
        user = await authenticate_user("admin", "password")
        if user:
            print("✅ Authentication successful")
            print(f"   User: {user.get('username', 'Unknown')}")
            print(f"   Admin: {user.get('is_admin', False)}")
        else:
            print("❌ Authentication failed - user not found or invalid credentials")
            print("   This might be expected if the user doesn't exist")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    # Test 3: Test database connection directly
    print("\n3. Testing direct database connection...")
    try:
        from supabase_client import get_supabase
        supabase = get_supabase()
        
        # Try to query users table
        response = supabase.table("users").select("id, username").limit(1).execute()
        
        if response.data is not None:
            print(f"✅ Database query successful")
            print(f"   Found {len(response.data)} users")
            if response.data:
                print(f"   Sample user: {response.data[0]}")
        else:
            print("❌ Database query returned no data")
            if hasattr(response, 'error'):
                print(f"   Error: {response.error}")
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Login functionality test completed!")
    print("\n💡 If you see authentication errors, it might be because:")
    print("   1. The test user doesn't exist in your database")
    print("   2. The API keys need to be updated")
    print("   3. The Supabase project is paused")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_login_functionality())
