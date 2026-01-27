import requests
from app import app
from models import db, WeatherSample

# Example location: Boulder, CO
LAT = 40.0150
LON = -105.2705
LOCATION_NAME = "Boulder, CO"

def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,wind_speed_10m"
    )
    data = requests.get(url, timeout=10).json()

    current = data["current"]
    temp_c = float(current["temperature_2m"])
    wind_kmh = float(current["wind_speed_10m"])
    return temp_c, wind_kmh

if __name__ == "__main__":
    temp_c, wind_kmh = fetch_weather()

    with app.app_context():
        sample = WeatherSample(
            location=LOCATION_NAME,
            temperature_c=temp_c,
            wind_speed_kmh=wind_kmh,
        )
        db.session.add(sample)
        db.session.commit()

    print(f"✅ Stored weather sample: {LOCATION_NAME} temp={temp_c}C wind={wind_kmh}km/h")
