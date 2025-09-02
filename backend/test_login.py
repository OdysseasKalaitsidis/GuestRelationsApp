import requests
import json

# Test the login endpoint
url = "http://localhost:8000/api/auth/login"
data = {
    "username": "Diana",
    "password": "test123"
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
