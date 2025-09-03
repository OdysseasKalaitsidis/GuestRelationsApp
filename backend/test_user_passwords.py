#!/usr/bin/env python3
"""
Test script to check user passwords
"""

import asyncio
import sys
import os
from datetime import date

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.user_service_supabase import authenticate_user, get_user_by_username
from supabase_client import initialize_supabase

async def test_user_passwords():
    """Test different user passwords"""
    print("Testing User Passwords...")
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return
    
    # Test users and their possible passwords
    test_users = [
        ("admin", ["admin", "admin123", "admin123!", "password"]),
        ("Diana", ["Diana", "Diana123", "Diana123!", "password"]),
        ("Aggeliki", ["Aggeliki", "Aggeliki123", "password"]),
        ("Odysseas", ["Odysseas", "Odysseas123", "password"])
    ]
    
    for username, passwords in test_users:
        print(f"\nTesting user: {username}")
        
        # Check if user exists
        user = await get_user_by_username(username)
        if not user:
            print(f"❌ User {username} not found")
            continue
        
        print(f"✅ User found: {user.get('username')} (admin: {user.get('is_admin')})")
        
        # Test each password
        for password in passwords:
            result = await authenticate_user(username, password)
            if result:
                print(f"✅ Password found: '{password}'")
                break
        else:
            print(f"❌ No working password found for {username}")

if __name__ == "__main__":
    asyncio.run(test_user_passwords())
