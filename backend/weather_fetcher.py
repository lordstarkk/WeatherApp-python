import os
from dotenv import load_dotenv  # Load environment variables from a .env file
from datetime import datetime, timezone, timedelta  # For handling time conversions
import requests  # To fetch weather data from an API
import logging

# Configure logging: Save logs to 'weather_app.log' and show messages on console
logging.basicConfig(
    filename="weather_app.log",  # Log file name
    level=logging.INFO,  # Log only INFO and above (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format for logs
)

class WeatherDataFetcher:
    def __init__(self):
        load_dotenv()  # Load API key from .env file
        self.weather_data = False  # Initialize weather data storage
        self.API_KEY = os.getenv("API_KEY")  # Get API key from environment variable
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # API endpoint

    def get_weather(self, city_name):
        """Fetches weather data for a given city."""
        self.city_name = city_name
        self.params = {
            "q": city_name,
            "appid": self.API_KEY,
            "units": "metric",  # Fetch data in Celsius
        }
        try:
            # Sending GET request to OpenWeather API
            response = requests.get(self.BASE_URL, self.params)
            if response.status_code == 200:
                self.weather_data = response.json()  # Store response data
                return response.status_code
            elif response.status_code == 401:
                logging.debug("Invalid API Key")
                return {"status": response.status_code, "message": "Invalid API Key"}

            elif response.status_code == 404:
                logging.error("City not found")
                return {"status": response.status_code, "message": "City not found"}

            else:
                logging.error(f"Response Status Code: {response.status_code}")  # Print error code if request fails
        except requests.ConnectionError:
            logging.error("No internet Connection")
            return {"status": "No internet Connection",
                    }
        except requests.exceptions.Timeout:
            logging.error("Request timed out.")
            return {"status: Reuest timed out. Try again"}
        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e}")


    def temprature(self):
        """Extracts temperature-related data from the response."""
        if self.weather_data:
            return {
                "temprature": self.weather_data["main"]["temp"],
                "feels_like": self.weather_data["main"]["feels_like"],
                "temp_min": self.weather_data["main"]["temp_min"],
                "temp_max": self.weather_data["main"]["temp_max"],
            }
        return {"status": "error",
            "data": None,
            "message": "Temprature data not available"}

    def wind_speed(self):
        """Extracts wind speed data."""
        if self.weather_data:
            return {"wind_speed": self.weather_data["wind"]["speed"]}
        return{"status": "error",
            "data": None,
            "message": "Wind speed data is not available"}

    def humidity(self): 
        """Extracts humidity data."""
        if self.weather_data:
            return {"humidity": self.weather_data["main"]["humidity"]}
        return{"status": "error",
            "data": None,
            "message": "Humidity data is not available"}

    def weather_description(self):
        """Extracts a short description of the weather."""
        if self.weather_data:
            return {
                "main": self.weather_data["weather"][0]["main"],
                "weather_description": self.weather_data["weather"][0]["description"]
            }
        return {"status": "error",
            "data": None,
            "message": "Weather decription is not available"}
        
    def sunrise_sunset(self):
        """Extracts sunrise and sunset times in human-readable format."""
        if self.weather_data:
            sunrise = self.weather_data["sys"]["sunrise"]
            sunset = self.weather_data["sys"]["sunset"]
            offset_seconds = self.weather_data['timezone']

            # Define the timezone using the offset
            self.local_tz = timezone(timedelta(seconds=offset_seconds))
            sunrise_time = datetime.fromtimestamp(sunrise, timezone.utc).astimezone(self.local_tz).strftime("%Y-%m-%d %I:%M:%S")
            sunset_time = datetime.fromtimestamp(sunset, timezone.utc).astimezone(self.local_tz).strftime("%Y-%m-%d %I:%M:%S")
            return {"sunrise_time": sunrise_time, "sunset_time": sunset_time}
        return {"status": "error",
            "data": None,
            "message": "Data is not available"}
    def visibility(self): 
        """Extracts visibility km/h returns a dictionary."""
        if self.weather_data:
            return {"visibility": self.weather_data["visibility"] / 1000}  # Convert meters to kilometers
        return {"status": "error",
            "data": None,
            "message": "Data is not available"}

    def pressure(self):
        """Extracts atmospheric pressure data."""
        if self.weather_data:
            return {"pressure": self.weather_data["main"]["pressure"]}
        return {"status": "error",
            "data": None,
            "message": "Data is not available"}

    def location_info(self):
        """Return a dictionary with city name and country code."""
        if self.weather_data:
            return {"name" : self.weather_data["name"],
                    "country" : self.weather_data["sys"]["country"]}
        return{"status": "error",
            "data": None,
            "message": "Data is not available"}

if __name__ == "__main__":
# Prompt user for city name
    city = input("Enter city name: ")

    # Initialize weather data fetcher
    weather_fetcher = WeatherDataFetcher()

    # Fetch weather data
    status_code = weather_fetcher.get_weather(city)
    
    print(f"Weather data for {city}:")
    
    # Print the results
    print("Temperature:", weather_fetcher.temprature())
    print("Wind Speed:", weather_fetcher.wind_speed())
    print("Humidity:", weather_fetcher.humidity())
    print("Weather Description:", weather_fetcher.weather_description())
    print("Sunrise & Sunset:", weather_fetcher.sunrise_sunset())
    print("Visibility:", weather_fetcher.visibility())
    print("Pressure:", weather_fetcher.pressure())
    print("Location Info:", weather_fetcher.location_info())