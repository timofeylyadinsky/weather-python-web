from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv
import aiohttp
import asyncio

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

countries = {}

def load_countries(filename):
    global countries
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            countries[row["country"]] = {
                "capital": row["capital"],
                "lat": row["latitude"],
                "lon": row["longitude"],
                }

load_countries('europe.csv')

@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/update')
async def fetch_weather():
    global countries
    async def fetch_city_weather(name):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={countries[name]['lat']}&longitude={countries[name]['lon']}&current_weather=true"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    weather_data = await response.json()
                    countries[name]["temperature"] = weather_data["current_weather"]["temperature"]
    
    tasks = [fetch_city_weather(country) for country in countries]
    await asyncio.gather(*tasks)
    return JSONResponse(content=countries)