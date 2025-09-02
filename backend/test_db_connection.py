# test_db_connection.py
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Check if DATABASE_URL is set
if not DATABASE_URL:
    raise RuntimeError("Missing required DATABASE_URL environment variable")

print("Using DATABASE_URL:", DATABASE_URL[:30] + "...")

# Create SSL context for Supabase
ssl_context = ssl.create_default_context(cafile=None)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create async engine with SSL configuration
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"ssl": ssl_context}
)

# Test connection
async def test_connection():
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Supabase connection successful! Test query returned:", result.fetchone())
    except Exception as e:
        print("❌ Supabase connection failed:", e)

# Run the async test
asyncio.run(test_connection())
