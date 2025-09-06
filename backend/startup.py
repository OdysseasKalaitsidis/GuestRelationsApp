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

def setup_ai_vectorstore():
    """Setup AI vectorstore if it doesn't exist"""
    try:
        vectorstore_path = "vectorstore"
        data_folder = "data"
        
        # Check if vectorstore already exists
        if os.path.exists(vectorstore_path):
            print("✅ AI vectorstore already exists")
            return True
        
        # Check if data folder exists
        if not os.path.exists(data_folder):
            print("⚠️ No data folder found - AI assistant will start without training documents")
            return True
        
        print("🤖 Setting up AI vectorstore from training documents...")
        
        # Import and run the vectorstore setup
        from setup_ai_production import build_vectorstore_from_data_folder
        
        if build_vectorstore_from_data_folder():
            print("✅ AI vectorstore setup completed successfully")
            return True
        else:
            print("⚠️ AI vectorstore setup failed - AI assistant will start without training documents")
            return True
            
    except Exception as e:
        print(f"⚠️ Warning: AI vectorstore setup failed: {e}")
        print("AI assistant will start without training documents")
        return True

def main():
    """Main startup function"""
    print("🚀 Starting Guest Relations API...")
    
    # Install spaCy model if needed
    if not install_spacy_model():
        print("⚠️ Warning: spaCy model installation failed. Some AI features may not work.")
    
    # Test database connectivity
    if not test_database_connectivity():
        print("⚠️ Warning: Database connectivity test failed. Some features may not work.")
    
    # Setup AI vectorstore
    setup_ai_vectorstore()
    
    # Start the application
    print("🎯 Starting uvicorn server...")
    os.execv(sys.executable, [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", os.getenv("PORT", "8000")])

if __name__ == "__main__":
    main()
