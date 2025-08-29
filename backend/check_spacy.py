#!/usr/bin/env python3
"""
Script to check and download required spaCy models
"""

import subprocess
import sys
import os

def check_spacy_model():
    """Check if en_core_web_sm model is installed"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model 'en_core_web_sm' is properly installed")
        print(f"Model version: {nlp.meta['version']}")
        return True
    except OSError:
        print("❌ spaCy model 'en_core_web_sm' is missing")
        return False
    except Exception as e:
        print(f"❌ Error checking spaCy model: {e}")
        return False

def download_spacy_model():
    """Download the required spaCy model"""
    try:
        print("📥 Downloading spaCy model 'en_core_web_sm'...")
        result = subprocess.run([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ], capture_output=True, text=True, check=True)
        print("✅ spaCy model downloaded successfully")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download spaCy model: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Checking spaCy model installation...")
    
    if check_spacy_model():
        print("🎉 Everything is working correctly!")
        return 0
    
    print("\n📥 Model not found, attempting to download...")
    if download_spacy_model():
        print("\n🔍 Verifying installation...")
        if check_spacy_model():
            print("🎉 Model installed and verified successfully!")
            return 0
        else:
            print("❌ Model installation verification failed")
            return 1
    else:
        print("❌ Failed to install spaCy model")
        return 1

if __name__ == "__main__":
    sys.exit(main())
