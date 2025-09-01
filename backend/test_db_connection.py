# test_db_connection.py
import os
from sqlalchemy import create_engine

# Get MySQL environment variables with defaults
MYSQLUSER = os.getenv('MYSQLUSER')
MYSQLPASSWORD = os.getenv('MYSQLPASSWORD')
MYSQLHOST = os.getenv('MYSQLHOST')
MYSQLPORT = os.getenv('MYSQLPORT', '3306')  # Default to 3306 if not set
MYSQLDATABASE = os.getenv('MYSQLDATABASE')

# Check if all required environment variables are set
if not all([MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE]):
    raise RuntimeError("Missing required MySQL environment variables: MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE")

# Construct DATABASE_URL
DATABASE_URL = (
    f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}"
    f"@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"
)

print("Using MySQL URL:", DATABASE_URL)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ MySQL connection successful! Test query returned:", result.fetchone())
except Exception as e:
    print("❌ MySQL connection failed:", e)
