
#!/usr/bin/env python3
"""
Database setup script for Supabase deployment
"""
import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("Setting up database...")
    
    # Get DATABASE_URL environment variable
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("❌ Missing DATABASE_URL environment variable")
        print("Please set up your Supabase database and ensure DATABASE_URL is configured.")
        sys.exit(1)
    
    print(f"✅ DATABASE_URL found: {DATABASE_URL[:30]}...")
    
    try:
        # Run database migrations
        print("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=".",
            env={**os.environ}
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
