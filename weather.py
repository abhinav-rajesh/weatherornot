import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

#fetches API KEY previously stored in the .env file
load_dotenv()
apikey=os.getenv("API_KEY")

@dataclass
class Weatherdata:
    main: str
    description: str
    icon: str
    temperature: int


#Function to get Latitude and Longitude to calculate Weather Data
def getdetails(city_name,state_code,country_code,API_key):
    response=requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}").json()
    data=response[0]
    #print(response)
    #get the lat and lon from the list of details provided by API
    latitude=data.get("lat")
    longitude=data.get("lon")
    return latitude,longitude

#function to get current weather using latitude and longitude
def currentweather(latitude,longitude,API_key):
    response=requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={API_key}").json()
    data=Weatherdata(
        main=response.get("weather")[0].get("main"),
        description=response.get("weather")[0].get("description"),
        icon=response.get("weather")[0].get("icon"),
        temperature=int(response.get("main").get("temp")))
    return data

def main(cityname,statename,countryname):
    latitude,longitude = getdetails(cityname,statename,countryname,apikey)
    currentweatherdata=currentweather(latitude,longitude,apikey)
    return currentweatherdata

if __name__ == "__main__":
    print(main(cityname,statename,countryname))

