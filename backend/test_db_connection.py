# test_db_connection.py
import os
from sqlalchemy import create_engine

# Get the database URL from environment
raw_mysql_url = os.getenv("MYSQL_URL")
if not raw_mysql_url:
    raise RuntimeError("MYSQL_URL not found in environment!")

# Convert to SQLAlchemy format
database_url = raw_mysql_url.replace("mysql://", "mysql+pymysql://")
print("Using DATABASE_URL:", database_url)

# Create engine
engine = create_engine(database_url, echo=False)

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Connection successful! Test query returned:", result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)
