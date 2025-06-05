from flask import Flask, render_template, request
# Assuming 'weather.py' contains a function 'main' to get weather data
from weather import main as get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None # Initialize data to None for the initial GET request

    if request.method == "POST":
        # Get data from the form submission
        cityname = request.form["cityname"]
        statename = request.form["statename"]
        countryname = request.form["countryname"]

        # Call your weather fetching function
        data = get_weather(cityname, statename, countryname)

        # --- IMPORTANT DEBUGGING STEP ---
        # Add this print statement to see what 'data' contains.
        # Check your Flask terminal after submitting a city.
        print(f"Weather Data Received for {cityname}, {statename}, {countryname}: {data}")
        # Make sure 'temperature' key exists and has a numeric value for display.

    # Render the template, passing the weather data if available
    return render_template("index.html", data=data)

if __name__ == "__main__":
    # Run the Flask app in debug mode (auto-reloads on code changes, shows errors)
    app.run(debug=True)