import requests  #to put requests to API
from dotenv import load_dotenv
import os
from dataclasses import dataclass

#to get API key from .env directly
load_dotenv()
apikey = os.getenv("API_KEY")
apikey2 = os.getenv("API_KEY2")

#to create a structure- like in C
@dataclass
class Weatherdata:
    main: str
    description: str
    icon: str
    temperature: int

#Function to get Latitude and Longitude to calculate Weather Data
def getdetails(city_name, state_code, country_code, API_key):
    response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}"
    ).json()
    data = response[0]
    latitude=data.get("lat")
    longitude=data.get("lon")
    return latitude,longitude

#function to get current weather using latitude and longitude
def currentweather(latitude, longitude, API_key):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={API_key}"
    ).json()
    return Weatherdata(
        main=response.get("weather")[0].get("main"),                    #to get exactly the details we need- refered to previous outputs 
        description=response.get("weather")[0].get("description"),
        icon=response.get("weather")[0].get("icon"),
        temperature=int(response.get("main").get("temp"))
    )

def main(cityname, statename, countryname):
    #making global copies to pass to forecast
    global cityname_copy,statename_copy
    cityname_copy=cityname
    statename_copy=statename

    latitude,longitude = getdetails(cityname,statename,countryname,apikey)
    currentweatherdata=currentweather(latitude,longitude,apikey)
    print(currentweatherdata)
    return currentweatherdata





#WEATHER FORECASTING!!!!!!!!

from datetime import datetime, timedelta

#fakecall function
main("Kochi","Kerala","India")

end_date=datetime.today().strftime("%d-%m-%Y")  #fetches todays current date-month-year
start_sate=(datetime.today()-timedelta(days=30)).strftime("%d-%m-%Y") #calculates the date 30 days before today
location=cityname_copy+","+statename_copy
print(location)
print(start_sate)
print(end_date)

#fetching updated historical data using Visual Crossing
url=f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}"
reqparameters={"unitGroup": "metric","include":"hours"}