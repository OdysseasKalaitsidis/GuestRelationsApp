#!/usr/bin/env python3
"""
Simple database test script
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Case
from schemas.case import CaseCreate

# Set a default password for testing
os.environ["DB_PASSWORD"] = "test123"

def test_db_connection():
    """Test database connection"""
    try:
        from db import engine, SessionLocal
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            
        # Test creating a case
        db = SessionLocal()
        try:
            # Create a test case
            test_case = CaseCreate(
                room="TEST-001",
                status="pending",
                importance="low",
                type="test",
                title="Test Case",
                action="Testing",
                owner_id=None
            )
            
            print(f"✅ CaseCreate validation successful: {test_case}")
            
            # Try to create in database
            db_case = Case(**test_case.model_dump())
            db.add(db_case)
            db.commit()
            db.refresh(db_case)
            
            print(f"✅ Case created in database with ID: {db_case.id}")
            
            # Clean up
            db.delete(db_case)
            db.commit()
            print("✅ Test case cleaned up")
            
        except Exception as e:
            print(f"❌ Error creating case: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection() 