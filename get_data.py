import logging
from typing import List, Dict, Any
import requests

logger = logging.getLogger("WeatherETLPipeline.Extract")

API_KEY = "0ef77af5425ce53ed86091e4e0fcb3d0"
CITY_LIST = ["London", "Paris", "Tokyo"]


def fetch_raw_weather_data(cities: List[str] = CITY_LIST, api_key: str = API_KEY) -> List[Dict[str, Any]]:
    """Fetches raw JSON weather data for target cities from OpenWeatherMap API."""
    logger.info("Extracting raw weather data from OpenWeatherMap API...")
    all_weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                all_weather_data.append(data)
                logger.info(f"Successfully fetched raw data for city: {city}")
            else:
                logger.error(f"Error fetching data for {city}: HTTP {response.status_code}")

        except requests.RequestException as exc:
            logger.error(f"Network error while fetching weather for {city}: {str(exc)}")

    return all_weather_data