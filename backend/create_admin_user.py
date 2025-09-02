#!/usr/bin/env python3
"""
Create a new admin user with password "123"
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import create_user
from schemas.user import UserCreate
from supabase_client import initialize_supabase

async def create_admin_user():
    """Create a new admin user"""
    print("🔧 Creating new admin user...")
    print("=" * 50)
    
    # Set environment variables (you'll need to replace these with your actual values)
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return False
    
    print("✅ Supabase initialized")
    
    # Create new admin user
    new_user = UserCreate(
        username="admin",
        name="System Administrator",
        email="admin@domesofcorfu.com",
        password="123",
        is_admin=True
    )
    
    print(f"Creating user: {new_user.username}")
    print(f"Email: {new_user.email}")
    print(f"Admin: {new_user.is_admin}")
    
    try:
        result = await create_user(new_user)
        if result:
            print("✅ Admin user created successfully!")
            print(f"User ID: {result.get('id')}")
            print(f"Username: {result.get('username')}")
            print(f"Email: {result.get('email')}")
            print(f"Admin: {result.get('is_admin')}")
            print("\n🎉 You can now login with:")
            print("Username: admin")
            print("Password: 123")
        else:
            print("❌ Failed to create admin user")
            return False
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(create_admin_user())
