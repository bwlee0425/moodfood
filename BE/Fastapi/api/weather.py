import requests
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, lat: float, lon: float) -> str:
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["weather"][0]["main"]  # 예: "Rain", "Clear"
        return "Unknown"