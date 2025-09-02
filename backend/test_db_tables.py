import asyncio
from db import get_db
from sqlalchemy import text

async def test_db_tables():
    async for db in get_db():
        try:
            # Test if users table exists
            result = await db.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"Users table exists with {count} users")
            
            # Test if we can query a user
            result = await db.execute(text("SELECT username, name FROM users LIMIT 1"))
            user = result.fetchone()
            if user:
                print(f"Found user: {user}")
            else:
                print("No users found in database")
                
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(test_db_tables())
