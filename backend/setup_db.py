#!/usr/bin/env python3
"""
Database setup script for Railway deployment
"""
import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("Setting up database...")
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("Please set up a MySQL database in Railway and ensure DATABASE_URL is configured.")
        sys.exit(1)
    
    print(f"✅ DATABASE_URL found: {database_url[:20]}...")
    
    try:
        # Run database migrations
        print("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully!")
        else:
            print(f"❌ Migration failed: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        sys.exit(1)
    
    print("✅ Database setup completed!")

if __name__ == "__main__":
    main()
