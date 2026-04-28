import requests

# 1. Configuration
API_KEY = "YOUR_API_KEY_HERE"  # Paste your key inside these quotes
CITY = "Singapore"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather():
    try:
        # 2. Make the request
        response = requests.get(URL)
        
        # 3. Convert response to a Python Dictionary (JSON)
        data = response.json()

        # 4. Extract the 'First' forecast entry
        # OpenWeather returns a list of 40 entries (5 days, every 3 hours)
        current_forecast = data['list'][0]
        
        temp = current_forecast['main']['temp']
        description = current_forecast['weather'][0]['description']

        print(f"--- {CITY} Weather Dashboard ---")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {description.capitalize()}")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_weather()
