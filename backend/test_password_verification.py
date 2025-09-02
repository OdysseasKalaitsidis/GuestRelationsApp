#!/usr/bin/env python3
"""
Test password verification
"""
from services.security import verify_password, hash_password

def test_password():
    """Test password hashing and verification"""
    password = "test123"
    
    print("🔍 Testing password functionality...")
    print(f"Password: {password}")
    
    # Hash the password
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    
    # Verify the password
    is_valid = verify_password(password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Test with wrong password
    is_wrong_valid = verify_password("wrongpassword", hashed)
    print(f"Wrong password verification: {is_wrong_valid}")
    
    # Test with empty password
    try:
        empty_valid = verify_password("", hashed)
        print(f"Empty password verification: {empty_valid}")
    except Exception as e:
        print(f"Empty password error: {e}")
    
    # Test with None password
    try:
        none_valid = verify_password(None, hashed)
        print(f"None password verification: {none_valid}")
    except Exception as e:
        print(f"None password error: {e}")

if __name__ == "__main__":
    test_password()
