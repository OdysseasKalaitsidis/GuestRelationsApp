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

def test_supabase_connectivity():
    """Test Supabase network connectivity"""
    try:
        from supabase_client import test_network_connectivity
        if test_network_connectivity():
            print("✅ Supabase network connectivity test passed")
            return True
        else:
            print("❌ Supabase network connectivity test failed")
            return False
    except Exception as e:
        print(f"⚠️ Warning: Could not test Supabase connectivity: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Guest Relations API...")
    
    # Install spaCy model if needed
    if not install_spacy_model():
        print("⚠️ Warning: spaCy model installation failed. Some AI features may not work.")
    
    # Test Supabase connectivity
    if not test_supabase_connectivity():
        print("⚠️ Warning: Supabase connectivity test failed. Database operations may not work.")
    
    # Start the application
    print("🎯 Starting uvicorn server...")
    os.execv(sys.executable, [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", os.getenv("PORT", "8000")])

if __name__ == "__main__":
    main()
