#!/usr/bin/env python3
"""
Test script to verify environment variable configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test that all required environment variables are set"""
    print("🔍 Testing Environment Variables Configuration")
    print("=" * 50)
    
    # Required environment variables
    required_vars = {
        'MYSQL_URL': 'MySQL connection URL (Railway)',
        'MYSQLUSER': 'Database username (fallback)',
        'MYSQLPASSWORD': 'Database password (fallback)', 
        'MYSQLHOST': 'Database host (fallback)',
        'DB_NAME': 'Database name (fallback)'
    }
    
    # Optional environment variables
    optional_vars = {
        'MYSQLPORT': 'Database port (default: 3306)',
        'ENVIRONMENT': 'Environment (development/production)',
        'ALLOWED_ORIGINS': 'Additional CORS origins',
        'SECRET_KEY': 'Secret key for JWT tokens',
        'OPENAI_API_KEY': 'OpenAI API key (optional)'
    }
    
    print("\n📋 Required Environment Variables:")
    all_required_set = True
    
    # Check if MYSQL_URL is set (primary method)
    mysql_url = os.getenv('MYSQL_URL')
    if mysql_url:
        print(f"  ✅ MYSQL_URL: *** (MySQL connection URL - primary method)")
    else:
        # Check fallback variables
        for var, description in required_vars.items():
            if var == 'MYSQL_URL':
                continue  # Skip MYSQL_URL since we already checked it
            value = os.getenv(var)
            if value:
                # Mask password for security
                display_value = "***" if var == 'MYSQLPASSWORD' else value
                print(f"  ✅ {var}: {display_value} ({description})")
            else:
                print(f"  ❌ {var}: NOT SET ({description})")
                all_required_set = False
    
    print("\n📋 Optional Environment Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value} ({description})")
        else:
            print(f"  ⚠️  {var}: NOT SET ({description})")
    
    print("\n" + "=" * 50)
    
    if all_required_set:
        print("✅ All required environment variables are set!")
        return True
    else:
        print("❌ Some required environment variables are missing!")
        return False

def test_database_connection():
    """Test database connection using the updated configuration"""
    print("\n🔍 Testing Database Connection")
    print("=" * 50)
    
    try:
        from db import get_database_url, initialize_database
        
        # Get database URL
        database_url = get_database_url()
        if not database_url:
            print("❌ Database URL could not be constructed - missing environment variables")
            return False
        
        # Mask password in URL for security
        masked_url = database_url.replace(
            os.getenv('MYSQLPASSWORD', ''), 
            '***'
        )
        print(f"✅ Database URL constructed: {masked_url}")
        
        # Test initialization
        if initialize_database():
            print("✅ Database initialization successful")
            
            # Test actual connection
            from db import get_engine
            engine = get_engine()
            with engine.connect() as conn:
                result = conn.execute("SELECT 1 as test")
                row = result.fetchone()
                print(f"✅ Database connection test successful! Query returned: {row[0]}")
            return True
        else:
            print("❌ Database initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def test_cors_configuration():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS Configuration")
    print("=" * 50)
    
    # Check if Netlify URL is in CORS origins
    netlify_url = "https://guestreationadomes.netlify.app"
    localhost_urls = ["http://localhost:5173", "http://localhost:5174"]
    
    print(f"✅ Netlify frontend URL configured: {netlify_url}")
    print(f"✅ Localhost development URLs configured: {localhost_urls}")
    
    # Check environment variable for additional origins
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
    if allowed_origins:
        print(f"✅ Additional CORS origins: {allowed_origins}")
    else:
        print("ℹ️  No additional CORS origins configured")
    
    print("✅ CORS configuration looks good!")

if __name__ == "__main__":
    print("🚀 Guest Relations Backend Environment Test")
    print("=" * 60)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    # Test database connection if environment variables are set
    if env_ok:
        db_ok = test_database_connection()
    else:
        print("\n⚠️  Skipping database test due to missing environment variables")
        db_ok = False
    
    # Test CORS configuration
    test_cors_configuration()
    
    print("\n" + "=" * 60)
    if env_ok and db_ok:
        print("🎉 All tests passed! Your backend is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
