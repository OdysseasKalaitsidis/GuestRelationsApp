from services.security import verify_password

# Test password verification
hash_value = "$2b$12$ZfzDBt80.j5pdbOjTX2qg.hwVC3Ic8VoE48OIIDUQr4asJ3X2qxd6"
test_passwords = ["test123", "password", "diana", "Diana", "123456", "admin"]

for password in test_passwords:
    result = verify_password(password, hash_value)
    print(f"Password '{password}': {result}")
