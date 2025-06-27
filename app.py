from flask import Flask, render_template, request
from weather import main as get_weather
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None     # Initialize data to None for the initial GET request
    plot_file=None
    forecast_data = []
    cityname= ""
    statename= ""
    countryname= ""    #it is used to hold the values 
    if request.method == "POST":
        # Get data from the form submission
        cityname = request.form.get("cityname", "")
        statename = request.form.get("statename", "")
        countryname = request.form.get("countryname", "")
        data,df,plot_file=get_weather(cityname, statename, countryname)
        if df is not None:
            forecast_data = df.to_dict(orient='records')
        
        # Make sure 'temperature' key exists and has a numeric value for display.
    

    # Render the template, passing the weather data if available (with the city, state, and country names so the value will not change) 
    return render_template("index.html", data=data,city=cityname, forecast_data=forecast_data, state=statename, country=countryname,plot_img=plot_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


'''if __name__ == "__main__":
    app.run(debug=True)'''