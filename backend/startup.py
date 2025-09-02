#!/usr/bin/env python3
"""
Startup script to ensure all dependencies are properly installed
"""

import subprocess
import sys
import os

def install_spacy_model():
    """Install spaCy model if not already installed"""
    try:
        import spacy
        # Try to load the model
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model 'en_core_web_sm' is already installed")
        return True
    except OSError:
        print("📥 Installing spaCy model 'en_core_web_sm'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], capture_output=True, text=True, check=True)
            print("✅ spaCy model installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install spaCy model: {e}")
            print(f"Error output: {e.stderr}")
            return False

def test_database_connectivity():
    """Test database connectivity using Supabase client"""
    try:
        from supabase_client import test_network_connectivity, test_supabase_connection
        import asyncio
        
        print("\n🔌 Testing database connectivity...")
        
        # Test network connectivity first
        if test_network_connectivity():
            print("✅ Network connectivity test passed")
        else:
            print("❌ Network connectivity test failed")
            return False
        
        # Test Supabase connection
        if asyncio.run(test_supabase_connection()):
            print("✅ Supabase connection test passed")
            return True
        else:
            print("❌ Supabase connection test failed")
            return False
            
    except Exception as e:
        print(f"⚠️ Warning: Could not test database connectivity: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Guest Relations API...")
    
    # Install spaCy model if needed
    if not install_spacy_model():
        print("⚠️ Warning: spaCy model installation failed. Some AI features may not work.")
    
    # Test database connectivity
    if not test_database_connectivity():
        print("⚠️ Warning: Database connectivity test failed. Some features may not work.")
    
    # Start the application
    print("🎯 Starting uvicorn server...")
    os.execv(sys.executable, [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", os.getenv("PORT", "8000")])

if __name__ == "__main__":
    main()
