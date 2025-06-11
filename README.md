# 🌤️ WeatherOrNot - A Smart Weather Forecast Web App

**WeatherOrNot** is a modern web application built with Flask that not only fetches **real-time weather data** for any location using the OpenWeatherMap API but also **predicts the hourly forecast** using a machine learning model trained on historical weather data from Open-Meteo.

> 🧠 “Because 'Maybe' isn't a weather report.”

---

## 🚀 Features

- 🔎 Search weather by **city, state, and country**
- 📍 Fetches **current temperature, weather type, and description**
- 🎥 Dynamic video backgrounds based on live weather
- ⏳ Predicts **hourly weather forecast** using:
  - 💡 Machine Learning (Random Forest Regressor & Classifier)
  - 📈 30-day historical weather data
- 🌐 Real-time API integrations with:
  - OpenWeatherMap for current weather
  - Open-Meteo for historical + hourly forecast data
- 📱 Clean, responsive Bootstrap-based UI with FontAwesome icons

---

## 🛠️ Built With

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, FontAwesome
- **Backend**: Python 3, Flask
- **Machine Learning**: scikit-learn, pandas, NumPy, joblib
- **APIs**: OpenWeatherMap, Open-Meteo
- **Styling**: Custom CSS animations, video backgrounds

---

## 🖼️ Screenshots

> *(Add screenshots here by uploading to your repo and using `![desc](path)` markdown syntax)*

---

## 🧠 How It Works

1. **User Input**: Enter city, state, and country.
2. **Current Weather**: Fetches geolocation using OpenWeatherMap’s geo API, then gets current weather.
3. **Forecast Prediction**:
   - Trains ML model using 30 days of historical weather (Open-Meteo API).
   - Predicts temperature and condition for next 5 upcoming hours.
4. **Frontend Display**:
   - Displays weather cards with icons and background videos that match the weather.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
## 2.Set up Environment
git clone https://github.com/yourusername/weatherornot.git
cd weatherornot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```
```bash
## Add API KEY
API_KEY=your_openweathermap_api_key_here

```
```bash
## RUNNING THE APP
python app.py

```
```bash
## PROJECT STRUCTURE

weatherornot/
│
├── app.py                    # Flask backend
├── weather.py                # API and ML logic
├── templates/
│   └── index.html            # HTML frontend
├── static/
│   ├── style.css             # CSS styles
│   └── video/                # Weather background videos
├── fonts/
│   └── Region.ttf            # Custom font
├── .env                      # API key config
└── requirements.txt          # Python dependencies

```
📈 Machine Learning Details
Trains two models using Random Forest:

RandomForestRegressor for temperature

RandomForestClassifier for weather condition

Data Source: Open-Meteo archive API

Model is retrained for every new location to ensure accuracy

Output: Top 5 hourly forecasts with condition and temperature


## 🙋‍♂️ Author
 Sreeram v g | Abhinav Rajesh

👨‍💻 Full Stack Developer | ML Enthusiast

🔗https://github.com/SR-005 |🔗https://github.com/abhinav-rajesh


## 🙌 Acknowledgements
OpenWeatherMap

Open-Meteo

Bootstrap

FontAwesome

scikit-learn


## 💡 Future Enhancements
🌐 Add geolocation-based automatic weather fetch

🗺️ Add map visualization using Leaflet or Mapbox

📊 Include graphical temperature trend charts

🧠 Improve model efficiency by caching trained models

