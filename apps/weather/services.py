import json
import os
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def _demo_weather(location):
    return {'location': location or 'Your farm location', 'temperature': 28, 'humidity': 62, 'rainfall': 15, 'condition': 'Partly cloudy', 'wind_speed': 10, 'source': 'demo', 'alerts': ['Demo forecast: add OPENWEATHER_API_KEY to .env for live weather data.']}

def get_weather(location):
    """Returns a normalised weather record; API failures always fall back explicitly."""
    api_key = os.getenv('OPENWEATHER_API_KEY', '').strip()
    if not api_key or not location:
        return _demo_weather(location)
    query = urlencode({'q': location, 'appid': api_key, 'units': 'metric'})
    try:
        request = Request(
            f'https://api.openweathermap.org/data/2.5/weather?{query}',
            headers={'Accept': 'application/json', 'User-Agent': 'Agri-Smart/1.0'},
        )
        with urlopen(request, timeout=8) as response:
            payload = json.load(response)
        main = payload['main']
        condition = payload['weather'][0]['description'].title()
        rain = float(payload.get('rain', {}).get('1h', 0))
        result = {'location': payload['name'], 'temperature': round(main['temp']), 'humidity': main['humidity'], 'rainfall': rain, 'condition': condition, 'wind_speed': round(payload.get('wind', {}).get('speed', 0) * 3.6), 'source': 'live', 'alerts': []}
        if rain > 10: result['alerts'].append('Rainfall is high. Check field drainage before irrigation.')
        if result['temperature'] > 35: result['alerts'].append('High temperature: consider irrigation timing and crop heat protection.')
        return result
    except (KeyError, TypeError, ValueError, HTTPError, URLError, TimeoutError, OSError):
        demo = _demo_weather(location)
        demo['alerts'] = ['Live weather could not be reached. Showing a clearly marked demo forecast.']
        return demo
