#!/usr/bin/env python3
"""
Debug the get_all_users function
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import get_all_users
from supabase_client import initialize_supabase, get_supabase

async def debug_get_all_users():
    """Debug the get_all_users function"""
    print("🔍 Debugging get_all_users function...")
    print("=" * 50)
    
    # Set environment variables
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    print("✅ Supabase initialized")
    
    # Test 1: Direct Supabase query
    print("\n1. Testing direct Supabase query...")
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").execute()
        
        if response.data is not None:
            print(f"✅ Direct query successful: {len(response.data)} users")
            for user in response.data:
                print(f"   - {user.get('username')} ({user.get('email')})")
        else:
            print("❌ Direct query returned no data")
            if hasattr(response, 'error'):
                print(f"   Error: {response.error}")
    except Exception as e:
        print(f"❌ Direct query error: {e}")
        return
    
    # Test 2: get_all_users function
    print("\n2. Testing get_all_users function...")
    try:
        users = await get_all_users()
        print(f"✅ get_all_users successful: {len(users)} users")
        for user in users:
            print(f"   - {user.get('username')} ({user.get('email')})")
    except Exception as e:
        print(f"❌ get_all_users error: {e}")
        print(f"   Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(debug_get_all_users())
