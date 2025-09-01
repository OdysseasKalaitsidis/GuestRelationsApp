#!/usr/bin/env python3
"""
Test script to verify CORS configuration
"""

import requests
import sys

def test_cors_configuration():
    """Test CORS configuration with different origins"""
    
    base_url = "https://guestrelationsapp-production.up.railway.app"
    
    # Test origins
    test_origins = [
        "https://guestreationadomes.netlify.app",
        "https://guestrelationsapp-production.up.railway.app",
        "http://localhost:5173",
        "https://malicious-site.com"  # Should be blocked
    ]
    
    print("🔍 Testing CORS configuration...")
    
    for origin in test_origins:
        print(f"\nTesting origin: {origin}")
        
        try:
            # Test OPTIONS request (preflight)
            headers = {
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
            
            response = requests.options(f"{base_url}/api/health", headers=headers)
            
            print(f"  OPTIONS /api/health: {response.status_code}")
            print(f"  Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            
            # Test actual GET request
            headers = {"Origin": origin}
            response = requests.get(f"{base_url}/api/health", headers=headers)
            
            print(f"  GET /api/health: {response.status_code}")
            print(f"  Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n✅ CORS test completed!")

if __name__ == "__main__":
    test_cors_configuration()
