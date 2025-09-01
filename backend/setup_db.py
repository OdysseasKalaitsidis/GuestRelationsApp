
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
    
    # Get MySQL environment variables with defaults
    MYSQLUSER = os.getenv('MYSQLUSER')
    MYSQLPASSWORD = os.getenv('MYSQLPASSWORD')
    MYSQLHOST = os.getenv('MYSQLHOST')
    MYSQLPORT = os.getenv('MYSQLPORT', '3306')  # Default to 3306 if not set
    MYSQLDATABASE = os.getenv('MYSQLDATABASE')
    
    # Check if all required MySQL environment variables are set
    required_vars = ['MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLHOST', 'MYSQLDATABASE']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing MySQL environment variables: {', '.join(missing_vars)}")
        print("Please set up a MySQL database and ensure all MySQL environment variables are configured.")
        sys.exit(1)
    
    # Construct DATABASE_URL from individual variables
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}"
        f"@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"
    )
    
    print(f"✅ MySQL environment variables found: {DATABASE_URL[:20]}...")
    
    try:
        # Run database migrations
        print("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=".",
            env={**os.environ, "DATABASE_URL": DATABASE_URL}
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
