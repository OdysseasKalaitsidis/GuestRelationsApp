#!/usr/bin/env python3
"""
Create a test user for frontend testing
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import create_user
from schemas.user import UserCreate

async def create_test_user():
    """Create a test user for frontend testing"""
    print("🔧 Creating test user for frontend...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Create test user
        test_user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            is_admin=True
        )
        
        user = await create_user(test_user)
        print("✅ Test user created successfully!")
        print(f"   Username: testuser")
        print(f"   Password: testpass123")
        print(f"   Email: test@example.com")
        print(f"   Admin: {user.get('is_admin', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(create_test_user())
