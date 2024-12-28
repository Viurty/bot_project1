import requests
url="http://127.0.0.1:5000/api/weather"
r = requests.post(url,json={'cities':['Moscow','London'],'day' : 2})
print(r.json())
