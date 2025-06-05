from flask import Flask, render_template, request
from weather import main as get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None 

    if request.method == "POST":
       
        cityname = request.form["cityname"]
        statename = request.form["statename"]
        countryname = request.form["countryname"]

        data = get_weather(cityname, statename, countryname)

  
        print(f"Weather Data Received for {cityname}, {statename}, {countryname}: {data}")
        

    
    return render_template("index.html", data=data)

if __name__ == "__main__":

    app.run(debug=True)