#!/usr/bin/env python3
"""
Check environment variables without exposing full API keys
"""
import os
from dotenv import load_dotenv

def check_env_vars():
    """Check environment variables safely"""
    print("🔍 Checking environment variables...")
    print("=" * 50)
    
    # Load from .env file if it exists
    load_dotenv()
    
    # Get environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"📋 SUPABASE_URL: {supabase_url}")
    print(f"📋 SUPABASE_SERVICE_ROLE_KEY: {service_role_key[:20] if service_role_key else 'None'}...")
    print(f"📋 SUPABASE_ANON_KEY: {anon_key[:20] if anon_key else 'None'}...")
    
    # Check if keys are different
    if service_role_key and anon_key:
        print(f"📋 Keys are identical: {service_role_key == anon_key}")
        print(f"📋 Service role key length: {len(service_role_key)}")
        print(f"📋 Anon key length: {len(anon_key)}")
        
        # Check if keys start with expected pattern
        print(f"📋 Service role key starts with 'eyJ': {service_role_key.startswith('eyJ') if service_role_key else False}")
        print(f"📋 Anon key starts with 'eyJ': {anon_key.startswith('eyJ') if anon_key else False}")
    
    # Check if any are missing
    missing = []
    if not supabase_url:
        missing.append("SUPABASE_URL")
    if not service_role_key:
        missing.append("SUPABASE_SERVICE_ROLE_KEY")
    if not anon_key:
        missing.append("SUPABASE_ANON_KEY")
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
    else:
        print("✅ All required environment variables are present")
    
    return bool(supabase_url and service_role_key and anon_key)

if __name__ == "__main__":
    check_env_vars()
