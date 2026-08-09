import requests 

url = "http://192.168.0.140/measures/current"

response =requests.get(url)

data = response.json()

print (data)