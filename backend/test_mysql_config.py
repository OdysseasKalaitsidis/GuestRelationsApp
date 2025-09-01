#!/usr/bin/env python3
"""
Test script to verify the new MySQL environment variables configuration
"""
import os
from dotenv import load_dotenv

def test_mysql_config():
    """Test that all required MySQL environment variables are available"""
    load_dotenv()
    
    print("Testing MySQL environment variables configuration...")
    
    # Check all required variables
    required_vars = {
        'MYSQLUSER': os.getenv('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD'),
        'MYSQLHOST': os.getenv('MYSQLHOST'),
        'MYSQLPORT': os.getenv('MYSQLPORT'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE')
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    # Construct DATABASE_URL
    DATABASE_URL = (
        f"mysql+pymysql://{os.getenv('MYSQLUSER')}:{os.getenv('MYSQLPASSWORD')}"
        f"@{os.getenv('MYSQLHOST')}:{os.getenv('MYSQLPORT')}/{os.getenv('MYSQLDATABASE')}"
    )
    
    print(f"✅ All MySQL environment variables found!")
    print(f"✅ Constructed DATABASE_URL: {DATABASE_URL[:20]}...")
    
    return True

if __name__ == "__main__":
    success = test_mysql_config()
    if success:
        print("\n🎉 MySQL configuration test passed!")
    else:
        print("\n❌ MySQL configuration test failed!")
        print("Please ensure all required MySQL environment variables are set.")
