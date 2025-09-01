# test_db_connection.py
import os
from sqlalchemy import create_engine

# Get the database URL from environment
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQLUSER')}:{os.getenv('MYSQLPASSWORD')}"
    f"@{os.getenv('MYSQLHOST')}:{os.getenv('MYSQLPORT')}/{os.getenv('MYSQLDATABASE')}"
)

# Check if all required environment variables are set
if not all([os.getenv('MYSQLUSER'), os.getenv('MYSQLPASSWORD'), 
           os.getenv('MYSQLHOST'), os.getenv('MYSQLPORT'), os.getenv('MYSQLDATABASE')]):
    raise RuntimeError("MySQL environment variables not found!")

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
