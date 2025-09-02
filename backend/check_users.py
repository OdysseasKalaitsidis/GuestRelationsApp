#!/usr/bin/env python3
"""
Check what users exist in the database
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_client import initialize_supabase, get_supabase

def check_users():
    """Check what users exist in the database"""
    print("🔍 Checking users in database...")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    print("✅ Supabase initialized")
    
    # Check all users in database
    try:
        supabase = get_supabase()
        
        response = supabase.table("users").select("id, username, email, is_admin").execute()
        
        if response.data:
            print(f"✅ Found {len(response.data)} users:")
            for user in response.data:
                print(f"   - ID: {user.get('id')}, Username: '{user.get('username')}', Email: '{user.get('email')}', Admin: {user.get('is_admin')}")
        else:
            print("❌ No users found in database")
    except Exception as e:
        print(f"❌ Error querying users: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Check completed!")

if __name__ == "__main__":
    check_users()
