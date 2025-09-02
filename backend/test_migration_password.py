#!/usr/bin/env python3
"""
Test the specific password hash from the migration
"""
from services.security import verify_password

def test_migration_password():
    """Test the password hash from the migration data"""
    password = "test123"
    migration_hash = "$2b$12$ZfzDBt80.j5pdbOjTX2qg.hwVC3Ic8VoE48OIIDUQr4asJ3X2qxd6"
    
    print("🔍 Testing migration password hash...")
    print(f"Password: {password}")
    print(f"Migration hash: {migration_hash}")
    
    # Test the migration hash
    is_valid = verify_password(password, migration_hash)
    print(f"Password verification: {is_valid}")
    
    # Test with wrong password
    is_wrong_valid = verify_password("wrongpassword", migration_hash)
    print(f"Wrong password verification: {is_wrong_valid}")

if __name__ == "__main__":
    test_migration_password()
