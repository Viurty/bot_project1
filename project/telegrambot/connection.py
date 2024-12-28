import requests
import asyncio
async def get_data(cities,day):
    url="http://127.0.0.1:5000/api/weather"
    r = requests.post(url,json={'cities': cities ,'day' : day})
    return await r.json()
