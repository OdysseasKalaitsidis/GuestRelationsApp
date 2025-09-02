import asyncio
from db import get_db
from services.user_service import authenticate_user

async def test_authentication():
    async for db in get_db():
        try:
            # Test authentication with known user
            user = await authenticate_user(db, "Diana", "test123")
            if user:
                print(f"Authentication successful for user: {user.username}")
                print(f"User ID: {user.id}")
                print(f"Is Admin: {user.is_admin}")
            else:
                print("Authentication failed")
                
        except Exception as e:
            print(f"Authentication error: {e}")
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(test_authentication())
