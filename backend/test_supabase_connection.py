#!/usr/bin/env python3
"""
Test script to verify Supabase connection and basic operations
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_client import initialize_supabase, test_supabase_connection, test_network_connectivity
from services.database_service import get_db_service

async def test_supabase_operations():
    """Test basic Supabase operations"""
    print("🔍 Testing Supabase connection and operations...")
    
    # Test 1: Initialize Supabase client
    print("\n1. Testing Supabase client initialization...")
    if initialize_supabase():
        print("✅ Supabase client initialized successfully")
    else:
        print("❌ Failed to initialize Supabase client")
        return False
    
    # Test 2: Test network connectivity
    print("\n2. Testing network connectivity...")
    if test_network_connectivity():
        print("✅ Network connectivity test passed")
    else:
        print("❌ Network connectivity test failed")
        return False
    
    # Test 3: Test database connection
    print("\n3. Testing database connection...")
    if await test_supabase_connection():
        print("✅ Database connection test passed")
    else:
        print("❌ Database connection test failed")
        return False
    
    # Test 4: Test basic database operations
    print("\n4. Testing basic database operations...")
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
        
        # Test getting tasks
        tasks = await db_service.get_all("tasks")
        print(f"✅ Retrieved {len(tasks)} tasks from database")
        
        # Test getting documents
        documents = await db_service.get_all("documents")
        print(f"✅ Retrieved {len(documents)} documents from database")
        
        print("✅ All basic database operations successful")
        return True
        
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Supabase connection tests...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "SUPABASE_ANON_KEY"
    ]
    
    print("📋 Checking environment variables...")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask the value for security
            masked_value = value[:10] + "..." + value[-10:] if len(value) > 20 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: Not found")
            return False
    
    # Run async tests
    success = asyncio.run(test_supabase_operations())
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Supabase connection is working correctly.")
        print("\n💡 Your backend should now be able to connect to Supabase without network issues.")
        print("   The connection uses HTTPS instead of direct Postgres, which bypasses")
        print("   the port 5432 connectivity problems on Render.")
    else:
        print("❌ Some tests failed. Please check your configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
