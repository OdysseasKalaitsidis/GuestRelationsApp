#!/usr/bin/env python3
"""
Debug script to check what MySQL environment variables Railway is providing
"""
import os
from dotenv import load_dotenv

def debug_mysql_env():
    """Debug MySQL environment variables"""
    load_dotenv()
    
    print("🔍 Debugging MySQL environment variables...")
    print("=" * 50)
    
    # Check all MySQL-related environment variables
    mysql_vars = {
        'MYSQLUSER': os.getenv('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD'),
        'MYSQLHOST': os.getenv('MYSQLHOST'),
        'MYSQLPORT': os.getenv('MYSQLPORT'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE'),
        'DATABASE_URL': os.getenv('DATABASE_URL')
    }
    
    for var, value in mysql_vars.items():
        if value:
            # Mask password for security
            if var == 'MYSQLPASSWORD':
                masked_value = '*' * len(value) if value else 'None'
                print(f"✅ {var}: {masked_value}")
            elif var == 'DATABASE_URL':
                # Show first 20 chars of DATABASE_URL
                print(f"✅ {var}: {value[:20]}...")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: None")
    
    print("=" * 50)
    
    # Check if we have the required variables
    required_vars = ['MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLHOST', 'MYSQLDATABASE']
    missing_vars = [var for var in required_vars if not mysql_vars[var]]
    
    if missing_vars:
        print(f"❌ Missing required variables: {', '.join(missing_vars)}")
        print("💡 Railway might not be providing these variables.")
        print("💡 Check your Railway dashboard for MySQL service configuration.")
    else:
        print("✅ All required MySQL variables are present!")
        
        # Test the connection string construction
        MYSQLPORT = mysql_vars['MYSQLPORT'] or '3306'
        test_url = (
            f"mysql+pymysql://{mysql_vars['MYSQLUSER']}:{mysql_vars['MYSQLPASSWORD']}"
            f"@{mysql_vars['MYSQLHOST']}:{MYSQLPORT}/{mysql_vars['MYSQLDATABASE']}"
        )
        print(f"✅ Test connection string: {test_url[:30]}...")
    
    # Check if DATABASE_URL is available as alternative
    if mysql_vars['DATABASE_URL']:
        print("💡 DATABASE_URL is also available - you could use this instead!")
    
    print("=" * 50)

if __name__ == "__main__":
    debug_mysql_env()
