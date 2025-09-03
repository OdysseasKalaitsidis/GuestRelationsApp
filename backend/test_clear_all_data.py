#!/usr/bin/env python3
"""
Test script to check if clear-all-data function works correctly
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_clear_all_data():
    """Test the clear-all-data function"""
    try:
        print("🔍 Testing clear-all-data function...")
        
        # Test Supabase connection first
        from supabase_client import test_supabase_connection
        if not await test_supabase_connection():
            print("❌ Supabase connection failed")
            return False
        
        print("✅ Supabase connection successful")
        
        # Test clear-all-data function
        from services.daily_service_supabase import clear_all_data
        result = await clear_all_data()
        
        print(f"✅ Clear-all-data successful: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing clear-all-data: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cases_endpoint():
    """Test the cases endpoint"""
    try:
        print("\n🔍 Testing cases endpoint...")
        
        from services.case_service_supabase import get_cases
        cases = await get_cases()
        
        print(f"✅ Cases endpoint successful: {len(cases)} cases found")
        return True
        
    except Exception as e:
        print(f"❌ Error testing cases endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🧪 Running API tests...")
    
    # Test cases endpoint
    await test_cases_endpoint()
    
    # Test clear-all-data function
    await test_clear_all_data()
    
    print("\n🏁 Tests completed")

if __name__ == "__main__":
    asyncio.run(main())
