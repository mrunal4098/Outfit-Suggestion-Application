# wardrobe/weather_utils.py

import requests

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        weather = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        print(weather)
        return weather
    except requests.RequestException as e:
        # Log the error or print it to console for debugging purposes
        print(f"Error fetching weather data: {e}")
        return None  # Return None if there's an error
