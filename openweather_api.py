import requests

# === Configuration ===
from config import OPENWEATHER_API_KEY
UNITS = "metric"

# === Shared Weather Parser ===
def parse_weather_data(data):
    return {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather_main": data["weather"][0]["main"],
        "weather_desc": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

# === Get weather by city name ===
def get_weather_by_city(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": UNITS}
    response = requests.get(url, params=params)
    if response.ok:
        return parse_weather_data(response.json())
    print(f"❌ API Error (city): {response.status_code}, {response.text}")
    return None

# === Get weather by lat/lon ===
def get_weather_by_lat_lon(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": UNITS}
    response = requests.get(url, params=params)
    if response.ok:
        return parse_weather_data(response.json())
    print(f"❌ API Error (lat/lon): {response.status_code}, {response.text}")
    return None

# === Get weather using IP geolocation ===
def get_weather_by_ip():
    try:
        loc_response = requests.get("https://ipinfo.io/json")
        loc_response.raise_for_status()
        loc_str = loc_response.json().get("loc")  # e.g., "25.0340,121.5624"
        lat_str, lon_str = loc_str.split(",")
        return get_weather_by_lat_lon(float(lat_str), float(lon_str))
    except Exception as e:
        print(f"❌ Error getting location by IP: {e}")
        return None

# === Test ===
if __name__ == "__main__":
    print("=== Weather by City ===")
    print(get_weather_by_city("Taipei,Taiwan"))

    print("\n=== Weather by IP ===")
    print(get_weather_by_ip())

    print("\n=== Weather by Lat/Lon ===")
    print(get_weather_by_lat_lon(25.0330, 121.5654))
