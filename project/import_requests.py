import requests

url = 'http://127.0.0.1:8000/api/token/'
data = {'username': 'siwar', 'password': 'adminpassword123'}
response = requests.post(url, data=data)

print(response.json())
