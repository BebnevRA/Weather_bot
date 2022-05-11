from src.app import app
from src.open_weather.api import OpenWeather


@app.route('/')
@app.route('/index')
def index():
    weather = OpenWeather('Saint Petersburg')

    return weather.weather_str()
