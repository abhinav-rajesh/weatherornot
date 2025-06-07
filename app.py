from flask import Flask, render_template, request
from weather import main as get_weather
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None     # Initialize data to None for the initial GET request
    htmldf = None
    cityname= ""
    statename= ""
    countryname= ""    #it is used to hold the values 
    if request.method == "POST":
        # Get data from the form submission
        cityname = request.form["cityname"]
        statename = request.form["statename"]
        countryname = request.form["countryname"]
        data,df=get_weather(cityname, statename, countryname)
        htmldf=df.to_html()
        print(f"Weather Data Received for {cityname}, {statename}, {countryname}: {data}")
        # Make sure 'temperature' key exists and has a numeric value for display.
    

    # Render the template, passing the weather data if available (with the city, state, and country names so the value will not change) 
    return render_template("index.html", data=data,city=cityname, state=statename, country=countryname,df=htmldf)

if __name__ == "__main__":

    app.run(debug=True)