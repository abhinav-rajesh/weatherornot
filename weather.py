import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
apikey = os.getenv("API_KEY")

@dataclass
class Weatherdata:
    main: str
    description: str
    icon: str
    temperature: int

def getdetails(city_name, state_code, country_code, API_key):
    response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}"
    ).json()
    data = response[0]
    return data.get("lat"), data.get("lon")

def currentweather(latitude, longitude, API_key):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={API_key}"
    ).json()
    return Weatherdata(
        main=response.get("weather")[0].get("main"),
        description=response.get("weather")[0].get("description"),
        icon=response.get("weather")[0].get("icon"),
        temperature=int(response.get("main").get("temp"))
    )

def main(cityname, statename, countryname):
    lat, lon = getdetails(cityname, statename, countryname, apikey)
    return currentweather(lat, lon, apikey)
