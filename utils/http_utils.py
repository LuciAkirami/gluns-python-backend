import requests

def fetch_contexts():
    response = requests.get("http://localhost:8080/api/v1/chat/contexts")
    return response.json()

def fetch_chat_data():
    response = requests.get("http://localhost:8080/api/v1/chat")
    return response.json()

def login_keycloak(username: str, password: str):
    url = "http://localhost:8083/api/v1/iam/login"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'username': username, 'password': password}
    response = requests.post(url, headers=headers, params=params)
    return response.json()
