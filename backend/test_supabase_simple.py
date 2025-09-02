#!/usr/bin/env python3
"""
Simple test script to verify Supabase connection with your environment variables
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_client import initialize_supabase, test_supabase_connection
from services.database_service import get_db_service

async def test_supabase_connection_simple():
    """Simple test of Supabase connection"""
    print("🔍 Testing Supabase connection with your environment variables...")
    
    # Test 1: Initialize Supabase client
    print("\n1. Testing Supabase client initialization...")
    if initialize_supabase():
        print("✅ Supabase client initialized successfully")
    else:
        print("❌ Failed to initialize Supabase client")
        return False
    
    # Test 2: Test database connection
    print("\n2. Testing database connection...")
    if await test_supabase_connection():
        print("✅ Database connection test passed")
    else:
        print("❌ Database connection test failed")
        return False
    
    # Test 3: Test basic database operations
    print("\n3. Testing basic database operations...")
    try:
        db_service = await get_db_service()
        
        # Test getting users
        users = await db_service.get_all("users")
        print(f"✅ Retrieved {len(users)} users from database")
        
        # Test getting cases
        cases = await db_service.get_all("cases")
        print(f"✅ Retrieved {len(cases)} cases from database")
        
        # Test getting followups
        followups = await db_service.get_all("followups")
        print(f"✅ Retrieved {len(followups)} followups from database")
        
        print("✅ All basic database operations successful")
        return True
        
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Supabase connection with your variables...")
    print("=" * 60)
    
    # Set your environment variables directly
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    os.environ["SUPABASE_ANON_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    # Check environment variables
    print("📋 Environment variables set:")
    print(f"✅ SUPABASE_URL: {os.environ.get('SUPABASE_URL')}")
    print(f"✅ SUPABASE_SERVICE_ROLE_KEY: {os.environ.get('SUPABASE_SERVICE_ROLE_KEY')[:20]}...")
    print(f"✅ SUPABASE_ANON_KEY: {os.environ.get('SUPABASE_ANON_KEY')[:20]}...")
    
    # Run async tests
    success = asyncio.run(test_supabase_connection_simple())
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS! Your Supabase connection is working correctly.")
        print("\n💡 This means:")
        print("   ✅ Your environment variables are correct")
        print("   ✅ Supabase client can connect to your database")
        print("   ✅ Your backend can perform database operations")
        print("   ✅ The network connectivity fix is working")
        print("\n🚀 Your backend should now work on Render without network issues!")
    else:
        print("❌ Connection failed. Please check your Supabase configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
