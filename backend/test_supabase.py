#!/usr/bin/env python3
"""
Test script for Supabase client setup
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_supabase_setup():
    """Test the Supabase client setup"""
    print("🧪 Testing Supabase Client Setup")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    print(f"SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
    print(f"SUPABASE_KEY: {'✅ Set' if supabase_key else '❌ Missing'}")
    
    if not supabase_url or not supabase_key:
        print("\n❌ Missing required environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_KEY in your environment.")
        return False
    
    try:
        # Test network connectivity
        from supabase_client import test_network_connectivity
        print("\n🌐 Testing network connectivity...")
        if test_network_connectivity():
            print("✅ Network connectivity test passed!")
        else:
            print("❌ Network connectivity test failed!")
            return False
        
        # Test Supabase connection
        from supabase_client import test_supabase_connection
        print("\n🔌 Testing Supabase connection...")
        if await test_supabase_connection():
            print("✅ Supabase connection test passed!")
        else:
            print("❌ Supabase connection test failed!")
            return False
        
        # Test basic operations
        print("\n📊 Testing basic operations...")
        from supabase_client import get_supabase
        
        supabase = get_supabase()
        
        # Test fetching users
        response = supabase.table("users").select("id").limit(1).execute()
        print(f"✅ Users table accessible: {len(response.data)} records found")
        
        # Test fetching cases
        response = supabase.table("cases").select("id").limit(1).execute()
        print(f"✅ Cases table accessible: {len(response.data)} records found")
        
        print("\n🎉 All tests passed! Supabase client is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_supabase_setup())
