#!/usr/bin/env python3
"""
Seed script to create initial users in the database
Creates 5 users: 2 admins and 3 regular users
"""

import os
import sys
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, User
from services.security import hash_password

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_seed_users():
    """Create initial users"""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Users already exist in database ({existing_users} users found)")
            print("Skipping user creation. Delete existing users first if you want to recreate them.")
            return
        
        # Define users to create
        users_data = [
            # Admin users
            {
                "username": "Diana",
                "name": "Guest Relations Manager - Diana",
                "email": "grm@domesofcorfu.com",
                "password": "dianagrm2025",
                "is_admin": True
            },
            {
                "username": "Aggeliki", 
                "name": "Guest Relations Assistant Manager - Aggeliki",
                "email": "agrm@domesofcorfu.com",
                "password": "aggelikiagrm2025",
                "is_admin": True
            },
            # Regular users
            {
                "username": "Odysseas",
                "name": "Odysseas",
                "email": "odysseas@domesofcorfu.com",
                "password": "odysseasgra2025",
                "is_admin": False
            },
            {
                "username": "Stella",
                "name": "Stella", 
                "email": "stella@domesofcorfu.com",
                "password": "stellagra2025",
                "is_admin": False
            },
            {
                "username": "Maria",
                "name": "Maria",
                "email": "maria@domesofcorfu.com", 
                "password": "mariagra2025",
                "is_admin": False
            },
            {
                "username": "Eleutherios",
                "name": "Eleutherios",
                "email": "eleutherios@domesofcorfu.com", 
                "password": "freedomgra2025",
                "is_admin": False
            }

        ]
        
        print("Creating seed users...")
        
        for user_data in users_data:
            # Hash the password
            hashed_password = hash_password(user_data["password"])
            
            # Create user
            user = User(
                username=user_data["username"],
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=hashed_password,
                is_admin=user_data["is_admin"]
            )
            
            db.add(user)
            print(f"✅ Created user: {user_data['username']} ({'Admin' if user_data['is_admin'] else 'User'})")
        
        # Commit all users
        db.commit()
        print(f"\n🎉 Successfully created {len(users_data)} users!")
        print("\nLogin credentials:")
        print("=" * 50)
        for user_data in users_data:
            role = "Admin" if user_data["is_admin"] else "User"
            print(f"{role}: {user_data['username']} / {user_data['password']}")
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def delete_all_users():
    """Delete all users (for testing)"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            db.delete(user)
        db.commit()
        print(f"🗑️ Deleted {len(users)} users")
    except Exception as e:
        print(f"❌ Error deleting users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--delete":
        delete_all_users()
    else:
        create_seed_users()
