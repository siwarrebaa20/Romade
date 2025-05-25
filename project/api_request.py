import requests

# Exemple d'appel API
url = 'https://jsonplaceholder.typicode.com/todos/1'
response = requests.get(url)

# Vérifiez si la requête a réussi
if response.status_code == 200:
    print(response.json())
else:
    print(f"Erreur : {response.status_code}")

