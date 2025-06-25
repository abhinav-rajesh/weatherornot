import requests  #to put requests to API
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import matplotlib.pyplot as plt

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


#WEATHER FORECASTING!!!!!!!!

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,accuracy_score,classification_report
import joblib


def modeltraining():
    end_date=(datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")  #fetches todays current date-month-year
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


    #Setting up data recieved as DataFrames
    df=pd.DataFrame({"datetime":data["hourly"]["time"],
                    "temp":data["hourly"]["temperature_2m"],
                    "precip":data["hourly"]["precipitation"],
                    "cloudcover":data["hourly"]["cloudcover"],
                    "weathercode":data["hourly"]["weathercode"]})

    # to converts the string of datetime that is fetched to actual datetime64 bits for computation
    df["datetime"]=pd.to_datetime(df["datetime"]) 
    #remove null values
    df=df.dropna(subset=["temp","precip","cloudcover","weathercode"])

    #to map the weathercode to weathercondition- human values
    snow_mask = df["weathercode"].isin([71, 73, 75, 77])
    fog_mask = df["weathercode"].isin([45, 48])
    thunderstorm_mask = df["weathercode"].isin([95, 96, 99])
    rain_mask = df["precip"] > 0.2
    cloudy_mask = df["cloudcover"] > 70
    clear_mask = df["cloudcover"] < 30

    # Use np.select with conditions and corresponding labels
    conditions = [snow_mask, fog_mask, thunderstorm_mask, rain_mask, cloudy_mask, clear_mask]
    choices = ["Snow", "Fog", "Thunderstorm", "Rainy", "Cloudy", "Clear"]

    #will compare and find suitable weather condition
    df["condition"] = np.select(conditions, choices, default="Partly Cloudy")
    '''print(df.head(10))'''

    #MACHNINE LEARNING
    
    y_temperature=df["temp"]                #target to find using regression
    y_condition=df["condition"]             #target to find using classification
    X=df[["precip","cloudcover","weathercode"]]     #analysis dataframe
    '''print(X.head())'''

    #splitting up data to train and test section - 80% to train and 20% to test
    X_train,X_test,y_temperature_train,y_temperature_test,y_condition_train,y_condition_test=train_test_split(X,y_temperature,y_condition,test_size=0.2,random_state=42)

    #setting up regression model:
    #in RandomForest it uses n number of Decision Trees which is used to train Model
    regression=RandomForestRegressor(n_estimators=100,random_state=42) #estimators refers to number of different decision trees used to train Model
    regression.fit(X_train, y_temperature_train) #because we use Regression to train temperature data

    classifier=RandomForestClassifier(n_estimators=100,random_state=42)
    classifier.fit(X_train,y_condition_train)

    #Testing Model Accuracy:
    regressionprediction=regression.predict(X_test)
    rerror1=mean_absolute_error(y_temperature_test,regressionprediction)
    rerror2=mean_squared_error(y_temperature_test,regressionprediction)
    '''print("---------REGRESSION MODEL---------")
    print("Absolute Error: ",rerror1)
    print("Squared Error: ",rerror2)'''

    
    classifierpredition=classifier.predict(X_test)
    accuracy=accuracy_score(y_condition_test,classifierpredition)
    report=classification_report(y_condition_test,classifierpredition)
    '''
    print("---------CLASSIFIER MODEL---------")
    print("Accuracy: ",accuracy)
    print("Report: ",report)'''

    #save model
    joblib.dump(regression, "temperature_model.pkl")
    joblib.dump(classifier, "condition_model.pkl")

def weatherforecast():
    regression=joblib.load("temperature_model.pkl")
    classifier=joblib.load("condition_model.pkl")

    #switch start and end data from prev function - as for future start is today and end is day+1
    start_date=datetime.today().strftime("%Y-%m-%d")  
    end_date=(datetime.today()+timedelta(days=1)).strftime("%Y-%m-%d")

    reqparameters={
        "latitude":latitude,
        "longitude":longitude,
        "start_date":start_date,
        "end_date":end_date,
        "hourly": "precipitation,cloudcover,weathercode",
        "timezone":"auto"}     #we need the data based on these conditions
    
    response=requests.get("https://api.open-meteo.com/v1/forecast",params=reqparameters)             
    response.raise_for_status()                     #to check if data has been returned, else will raise an exception automatically
    data=response.json()                    #setting up return value as data

    #Setting up data recieved as DataFrames
    forecastdf=pd.DataFrame({"datetime":data["hourly"]["time"],
                    "precip":data["hourly"]["precipitation"],
                    "cloudcover":data["hourly"]["cloudcover"],
                    "weathercode":data["hourly"]["weathercode"]})

    # to converts the string of datetime that is fetched to actual datetime64 bits for computation
    forecastdf["datetime"]=pd.to_datetime(forecastdf["datetime"]) 
    #remove null values
    forecastdf=forecastdf.dropna(subset=["precip","cloudcover","weathercode"])

    currentime=datetime.now()
    forecastdf=forecastdf[forecastdf["datetime"]>=currentime]
    forecastX=forecastdf[["precip","cloudcover","weathercode"]]

    temperatureprediction=regression.predict(forecastX)
    conditionprediction=classifier.predict(forecastX)
    forecastdf["predictedtemperature"]=temperatureprediction
    forecastdf["predictedcondition"]=conditionprediction
    '''print("---------------PREDICTIONS---------------")'''
    '''print(forecastdf[["datetime","predictedtemperature","predictedcondition"]].head(5))'''

    # Predictions
    forecastdf["predictedtemperature"] = regression.predict(forecastX)
    forecastdf["predictedcondition"] = classifier.predict(forecastX)

    # Plot forecasted temperature
    plt.figure(figsize=(10, 5))
    plt.plot(forecastdf["datetime"], forecastdf["predictedtemperature"],
             marker='o', linestyle='-', color='tab:blue')
    plt.title("Forecasted Temperature for Next 24 Hours")
    plt.xlabel("Datetime")
    plt.ylabel("Predicted Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save to static folder
    plot_path = os.path.join("static", "forecast_temp.png")
    plt.savefig(plot_path)
    plt.close()

    return forecastdf[["datetime","predictedtemperature","predictedcondition"]].head(5),"forecast_temp.png"


def main(cityname, statename, countryname):
    latitude,longitude = getdetails(cityname,statename,countryname,apikey)
    currentweatherdata=currentweather(latitude,longitude,apikey)
    modeltraining()
    df,plot_file=weatherforecast()
    print(currentweatherdata)
    print(df)
    return currentweatherdata,df,plot_file

'''#fakecall function
main("Kochi","Kerala","India")'''