import requests

response = requests.get('http://localhost:9200/')
print(response.json())