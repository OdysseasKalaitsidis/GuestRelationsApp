#!/usr/bin/env python3
"""
Test script to verify MYSQL_URL parsing
"""
import os
from urllib.parse import urlparse

def test_mysql_url_parsing():
    """Test MYSQL_URL parsing functionality"""
    print("🔍 Testing MYSQL_URL Parsing")
    print("=" * 50)
    
    # Test with a sample MYSQL_URL
    sample_mysql_url = "mysql://user:password@hostname:3306/database_name"
    
    print(f"Sample MYSQL_URL: {sample_mysql_url}")
    
    parsed = urlparse(sample_mysql_url)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    database = parsed.path.lstrip("/")  # VERY IMPORTANT - removes leading slash
    
    print(f"Parsed components:")
    print(f"  User: {user}")
    print(f"  Password: ***")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Database: {database}")
    
    # Reconstruct connection URL
    connection_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    print(f"Reconstructed URL: {connection_url}")
    
    # Test with leading slash in path
    test_paths = ["/database_name", "database_name", "/my_db", "my_db"]
    print(f"\nTesting path.lstrip('/') with different paths:")
    for path in test_paths:
        cleaned = path.lstrip("/")
        print(f"  '{path}' -> '{cleaned}'")
    
    print("✅ MYSQL_URL parsing test completed!")

if __name__ == "__main__":
    test_mysql_url_parsing()
