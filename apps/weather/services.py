import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

def _demo_weather(location):
    return {'location': location or 'Your farm location', 'temperature': 28, 'humidity': 62, 'rainfall': 15, 'condition': 'Partly cloudy', 'wind_speed': 10, 'source': 'demo', 'alerts': ['Demo forecast: add OPENWEATHER_API_KEY to .env for live weather data.']}

def get_weather(location):
    """Returns a normalised weather record; API failures always fall back explicitly."""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key or not location:
        return _demo_weather(location)
    query = urlencode({'q': location, 'appid': api_key, 'units': 'metric'})
    try:
        with urlopen(f'https://api.openweathermap.org/data/2.5/weather?{query}', timeout=5) as response:
            payload = json.load(response)
        rain = float(payload.get('rain', {}).get('1h', 0))
        result = {'location': payload['name'], 'temperature': round(payload['main']['temp']), 'humidity': payload['main']['humidity'], 'rainfall': rain, 'condition': payload['weather'][0]['description'].title(), 'wind_speed': round(payload.get('wind', {}).get('speed', 0) * 3.6), 'source': 'live', 'alerts': []}
        if rain > 10: result['alerts'].append('Rainfall is high. Check field drainage before irrigation.')
        if result['temperature'] > 35: result['alerts'].append('High temperature: consider irrigation timing and crop heat protection.')
        return result
    except Exception:
        demo = _demo_weather(location); demo['alerts'] = ['Live weather could not be reached. Showing a clearly marked demo forecast.']; return demo
