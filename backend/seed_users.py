#!/usr/bin/env python3
"""
Seed users with specified credentials:
- diana (admin): password dianadoc
- aggeliki (admin): password aggelikidoc  
- odysseas (user): password odyssseas
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import create_user, get_user_by_username
from schemas.user import UserCreate
from supabase_client import initialize_supabase

async def seed_users():
    """Seed users with specified credentials"""
    print("🌱 Seeding users...")
    print("=" * 50)
    
    # Set environment variables
    os.environ["SUPABASE_URL"] = "https://sjjuaesddqzfcdahutfl.supabase.co"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return False
    
    print("✅ Supabase initialized")
    
    # Define users to create
    users_to_create = [
        {
            "username": "diana",
            "name": "Diana",
            "email": "diana@domesofcorfu.com",
            "password": "dianadoc",
            "is_admin": True
        },
        {
            "username": "aggeliki",
            "name": "Aggeliki", 
            "email": "aggeliki@domesofcorfu.com",
            "password": "aggelikidoc",
            "is_admin": True
        },
        {
            "username": "odysseas",
            "name": "Odysseas",
            "email": "odysseas@domesofcorfu.com", 
            "password": "odyssseas",
            "is_admin": False
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for user_data in users_to_create:
        username = user_data["username"]
        
        # Check if user already exists
        existing_user = await get_user_by_username(username)
        if existing_user:
            print(f"⏭️  User '{username}' already exists, skipping...")
            skipped_count += 1
            continue
        
        # Create new user
        new_user = UserCreate(
            username=user_data["username"],
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=user_data["is_admin"]
        )
        
        print(f"Creating user: {new_user.username}")
        print(f"Email: {new_user.email}")
        print(f"Admin: {new_user.is_admin}")
        
        try:
            result = await create_user(new_user)
            if result:
                print(f"✅ User '{username}' created successfully!")
                print(f"User ID: {result.get('id')}")
                created_count += 1
            else:
                print(f"❌ Failed to create user '{username}'")
        except Exception as e:
            print(f"❌ Error creating user '{username}': {e}")
    
    print("\n" + "=" * 50)
    print("📊 Seeding Summary:")
    print(f"✅ Created: {created_count} users")
    print(f"⏭️  Skipped: {skipped_count} users (already exist)")
    print(f"📝 Total processed: {len(users_to_create)} users")
    
    if created_count > 0:
        print("\n🎉 New users created! You can now login with:")
        for user_data in users_to_create:
            if not await get_user_by_username(user_data["username"]):
                continue
            print(f"Username: {user_data['username']}")
            print(f"Password: {user_data['password']}")
            print(f"Admin: {user_data['is_admin']}")
            print("---")
    
    return True

if __name__ == "__main__":
    asyncio.run(seed_users())

