import requests  #to put requests to API
from dotenv import load_dotenv
import os
from dataclasses import dataclass

#to get API key from .env directly
load_dotenv()
apikey = os.getenv("API_KEY")

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
    global latitude,longitude
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
    latitude,longitude = getdetails(cityname,statename,countryname,apikey)
    currentweatherdata=currentweather(latitude,longitude,apikey)
    print(currentweatherdata)
    return currentweatherdata





#WEATHER FORECASTING!!!!!!!!

from datetime import datetime, timedelta
import pandas as pd

#fakecall function
main("Kochi","Kerala","India")

end_date=datetime.today().strftime("%Y-%m-%d")  #fetches todays current date-month-year
start_date=(datetime.today()-timedelta(days=30)).strftime("%Y-%m-%d") #calculates the date 30 days before today
print(start_date)
print(end_date)

#fetching updated historical data using Open Meteo
reqparameters={
    "latitude":latitude,
    "longitude":longitude,
    "start_date":start_date,
    "end_date":end_date,
    "hourly": "temperature_2m,precipitation,cloudcover,weathercode",
    "timezone":"auto"}     #we need the data based on these conditions

#fetching data from SOURCE
response=requests.get("https://archive-api.open-meteo.com/v1/archive",params=reqparameters)             
response.raise_for_status()                     #to check if data has been returned, else will raise an exception automatically
data=response.json()                    #setting up return value as data


#Setting up data for each over from data recieved
datahours=[]
for day in data["days"]:
    for hours in data["hours"]:
        hours["datetime"]=f"{day['datetime']} {hours['datetime']}"
        datahours.append(hours)

df=pd.DataFrame(datahours)
print(df)
