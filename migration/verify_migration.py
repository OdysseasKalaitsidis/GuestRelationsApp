#!/usr/bin/env python3
"""
Migration Verification Script
Tests the Supabase connection and data integrity
"""

import psycopg2
import os

# Supabase Configuration
SUPABASE_CONFIG = {
    'host': 'db.sjjuaesddqzfcdahutfl.supabase.co',
    'user': 'postgres',
    'password': 'Odysseaskal',
    'database': 'postgres',
    'port': 5432,
    'sslmode': 'require'
}

def test_connection():
    """Test Supabase connection"""
    try:
        connection = psycopg2.connect(**SUPABASE_CONFIG)
        cursor = connection.cursor()
        
        # Test basic connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]
        print(f"✅ Connection test: {result}")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"✅ Tables found: {', '.join(tables)}")
        
        # Check row counts
        for table in ['users', 'cases', 'followups']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"✅ {table}: {count} rows")
        
        # Test a sample query
        cursor.execute("SELECT username, name FROM users LIMIT 3")
        users = cursor.fetchall()
        print(f"✅ Sample users: {[f'{u[0]} ({u[1]})' for u in users]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Verifying Supabase Migration")
    print("=" * 40)
    
    if test_connection():
        print("\n🎉 Migration verification successful!")
        print("✅ Supabase is ready for your application")
        print("\nNext steps:")
        print("1. Update your environment variables:")
        print("   DATABASE_URL=postgresql+asyncpg://postgres:Odysseaskal@db.sjjuaesddqzfcdahutfl.supabase.co:5432/postgres?sslmode=require")
        print("2. Test your FastAPI application locally")
        print("3. Deploy to Railway with the new configuration")
    else:
        print("\n❌ Migration verification failed")
        print("Please check the Supabase configuration")

if __name__ == "__main__":
    main()
