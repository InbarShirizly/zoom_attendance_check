import requests

auth = {
    "username": 'a',
    "password": 'TEST1234',
    "email": "abc@gmail.com"
}

BASE_URL = "http://127.0.0.1:5000/api/"

print(requests.post(BASE_URL + 'register', auth).json())
print(requests.get(BASE_URL + 'classrooms', auth=(auth['username'], auth['password'])).json())
print(requests.get(BASE_URL + 'classrooms'))
print(requests.get(BASE_URL + 'classrooms/1', auth=(auth['username'], auth['password'])).json())
