import requests

# py users/tests/register.py
url = "http://localhost:8000/api/auth/register"
data = {
        "username": "test",
        "email": "test@email.com",
        "password": "test123",
        "role": "Adotante"
    }
response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Resposta:", response.json())
