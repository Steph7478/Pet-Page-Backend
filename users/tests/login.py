import requests

# py users/tests/login.py
url = "http://localhost:8000/api/auth/login"
data = {
    "email": "test@email.com",
    "password": "test123"
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Resposta:", response.json())
