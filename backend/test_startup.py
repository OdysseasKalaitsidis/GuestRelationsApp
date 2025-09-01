#!/usr/bin/env python3
"""
Test script to verify application startup
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported without spacy"""
    print("🔍 Testing module imports...")
    
    try:
        # Test basic imports
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        # Test our modules
        from db import Base, get_database_url
        print("✅ Database module imported successfully")
        
        from models import User, Case, Followup, Task, Document
        print("✅ Models imported successfully")
        
        # Test services (should not fail even without spacy)
        from services.ai_service import get_client
        print("✅ AI service imported successfully")
        
        from services.anonymization_service import AnonymizationService
        print("✅ Anonymization service imported successfully")
        
        from services.document_service import extract_text_from_pdf
        print("✅ Document service imported successfully")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_startup():
    """Test that the FastAPI app can be created"""
    print("\n🔍 Testing app startup...")
    
    try:
        from main import app
        print("✅ FastAPI app created successfully")
        
        # Test that we can get the app info
        print(f"App title: {app.title}")
        print(f"App version: {app.version}")
        
        return True
        
    except Exception as e:
        print(f"❌ App startup failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Guest Relations API startup...")
    
    if test_imports() and test_app_startup():
        print("\n🎉 All tests passed! Application should start successfully.")
        return 0
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
