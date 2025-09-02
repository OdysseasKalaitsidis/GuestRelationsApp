import asyncio
from db import get_db
from sqlalchemy import text

async def check_user_password():
    async for db in get_db():
        try:
            # Get user details including password hash
            result = await db.execute(text("SELECT username, name, hashed_password FROM users WHERE username = 'Diana'"))
            user = result.fetchone()
            if user:
                print(f"Username: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Password Hash: {user[2]}")
            else:
                print("User not found")
                
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(check_user_password())
