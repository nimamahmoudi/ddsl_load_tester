import requests

response = requests.get('http://localhost:8089/stats/requests')
print(response)
print(response.json())
