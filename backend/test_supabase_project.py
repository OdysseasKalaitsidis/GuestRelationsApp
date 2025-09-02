#!/usr/bin/env python3
"""
Test Supabase project status and API key validity
"""
import requests
import os
from dotenv import load_dotenv

def test_supabase_project():
    """Test if the Supabase project is accessible"""
    print("🔍 Testing Supabase project status...")
    print("=" * 50)
    
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"📋 Project URL: {supabase_url}")
    
    # Test 1: Check if the project URL is accessible
    print("\n1. Testing project URL accessibility...")
    try:
        response = requests.get(supabase_url, timeout=10)
        print(f"✅ Project URL accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Project URL not accessible: {e}")
        return False
    
    # Test 2: Test REST API with service role key
    print("\n2. Testing REST API with service role key...")
    try:
        headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}"
        }
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        print(f"✅ REST API response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Service role key is valid!")
        else:
            print(f"❌ Service role key error: {response.text}")
    except Exception as e:
        print(f"❌ REST API test failed: {e}")
    
    # Test 3: Test REST API with anon key
    print("\n3. Testing REST API with anon key...")
    try:
        headers = {
            "apikey": anon_key,
            "Authorization": f"Bearer {anon_key}"
        }
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        print(f"✅ REST API response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Anon key is valid!")
        else:
            print(f"❌ Anon key error: {response.text}")
    except Exception as e:
        print(f"❌ REST API test failed: {e}")
    
    # Test 4: Try to query a table directly
    print("\n4. Testing table query...")
    try:
        headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}"
        }
        response = requests.get(f"{supabase_url}/rest/v1/users?select=id&limit=1", headers=headers, timeout=10)
        print(f"✅ Table query response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Table query successful!")
            data = response.json()
            print(f"   Found {len(data)} users")
        else:
            print(f"❌ Table query error: {response.text}")
    except Exception as e:
        print(f"❌ Table query failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Supabase project test completed!")
    
    return True

if __name__ == "__main__":
    test_supabase_project()
