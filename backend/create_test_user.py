import asyncio
from db import get_db
from services.user_service import create_user
from schemas.user import UserCreate

async def create_test_user():
    async for db in get_db():
        try:
            # Create a test user with a simple password
            test_user = UserCreate(
                username="testuser",
                name="Test User",
                email="test@example.com",
                password="password123",
                is_admin=True
            )
            
            user = await create_user(db, test_user)
            print(f"Created test user: {user.username} (ID: {user.id})")
            print("You can now login with username: 'testuser' and password: 'password123'")
                
        except Exception as e:
            print(f"Error creating user: {e}")
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(create_test_user())
