import requests

url = "http://api.weatherapi.com/v1/forecast.json"
params = {
    "key": "YOUR_API_KEY",
    "q": "Chennai",
    "days": "1",
    "aqi": "no",
    "alerts": "yes"
}

response = requests.get(url, params=params)
weather_data = {}
if response.status_code == 200:
    data = response.json()
    
    location = data.get("location", {})
    weather_data["city_name"] = location.get("name", "N/A")
    weather_data["region"] = location.get("region", "N/A")
    weather_data["country"] = location.get("country", "N/A")
    weather_data["localtime"] = location.get("localtime", "N/A")
    
    current = data.get("current", {})
    weather_data["temp_c"] = current.get("temp_c", "N/A")
    weather_data["condition_text"] = current.get("condition", {}).get("text", "N/A")
    weather_data["wind_speed_kph"] = current.get("wind_kph", "N/A")
    weather_data["humidity"] = current.get("humidity", "N/A")
    
    forecast_day = data.get("forecast", {}).get("forecastday", [{}])[0]
    weather_data["max_temp"] = forecast_day.get("day", {}).get("maxtemp_c", "N/A")
    weather_data["min_temp"] = forecast_day.get("day", {}).get("mintemp_c", "N/A")
    weather_data["chance_of_rain"] = forecast_day.get("day", {}).get("daily_chance_of_rain", "N/A")
    weather_data["sunrise"] = forecast_day.get("astro", {}).get("sunrise", "N/A")
    weather_data["sunset"] = forecast_day.get("astro", {}).get("sunset", "N/A")

else:
    weather_data["error"] = f"Failed to retrieve weather data. Status code: {response.status_code}"

import json
with open("weather_data.json", "w") as file:
    json.dump(weather_data, file)