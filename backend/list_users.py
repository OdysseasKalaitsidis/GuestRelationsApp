import asyncio
from db import get_db
from sqlalchemy import text

async def list_all_users():
    async for db in get_db():
        try:
            # Get all users
            result = await db.execute(text("SELECT username, name, email FROM users"))
            users = result.fetchall()
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"  - {user[0]} ({user[1]}) - {user[2]}")
                
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(list_all_users())
