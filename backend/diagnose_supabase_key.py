#!/usr/bin/env python3
"""
Diagnostic test for Supabase API key issues
"""
import os
import sys
from supabase import create_client

def test_api_key_diagnostic():
    """Test API key with detailed error reporting"""
    print("🔍 Diagnosing Supabase API key issue...")
    print("=" * 60)
    
    # Your environment variables
    supabase_url = "https://sjjuaesddqzfcdahutfl.supabase.co"
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqanVhZXNkZHF6ZmNkYWh1dGZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njc5ODcwOCwiZXhwIjoyMDcyMzc0NzA4fQ.wz_qjM4NPeatEir712ug6tHikb4oM8-Mlaie8ezxSjs"
    
    print(f"📋 URL: {supabase_url}")
    print(f"📋 Service Role Key length: {len(service_role_key)} characters")
    print(f"📋 Anon Key length: {len(anon_key)} characters")
    print(f"📋 Keys are identical: {service_role_key == anon_key}")
    
    # Test with service role key
    print("\n1. Testing with Service Role Key...")
    try:
        supabase = create_client(supabase_url, service_role_key)
        response = supabase.table("users").select("id").limit(1).execute()
        print("✅ Service Role Key works!")
        return True
    except Exception as e:
        print(f"❌ Service Role Key failed: {e}")
    
    # Test with anon key
    print("\n2. Testing with Anon Key...")
    try:
        supabase = create_client(supabase_url, anon_key)
        response = supabase.table("users").select("id").limit(1).execute()
        print("✅ Anon Key works!")
        return True
    except Exception as e:
        print(f"❌ Anon Key failed: {e}")
    
    print("\n🔍 Analysis:")
    print("The issue might be:")
    print("1. The API key is truncated or corrupted")
    print("2. The key doesn't have the right permissions")
    print("3. The Supabase project is paused or deleted")
    print("4. The key format is incorrect")
    
    print("\n💡 Please check:")
    print("1. Go to your Supabase dashboard")
    print("2. Navigate to Settings > API")
    print("3. Copy the 'service_role' key (not anon key)")
    print("4. Make sure the key starts with 'eyJ' and is very long")
    print("5. Ensure your project is active (not paused)")
    
    return False

if __name__ == "__main__":
    test_api_key_diagnostic()
