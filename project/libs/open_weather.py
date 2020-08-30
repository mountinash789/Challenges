from datetime import datetime

import requests
from django.conf import settings

from backend.models import Weather


class OpenWeather:
    longitude = None
    latitude = None

    def __init__(self, lon, lat):
        self.longitude = lon
        self.latitude = lat

    def hourly_weather(self):
        params = {
            'appid': settings.OPENWEATHER_KEY,
            'exclude': 'minutely,current,daily',
            'lat': self.latitude,
            'lon': self.longitude,
            'units': 'metric',
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params)
        return response.json().get('hourly', [])

    def save_hourly_weather(self):
        results = self.hourly_weather()
        for result in results:
            obj, created = Weather.objects.get_or_create(
                timestamp=datetime.fromtimestamp(result['dt']),
                longitude=self.longitude,
                latitude=self.latitude,
                temperature=result['temp'],
                feels_like=result['feels_like'],
                pressure=result['pressure'],
                humidity=result['humidity'],
                dew_point=result['dew_point'],
                clouds=result['clouds'],
                visibility=result['visibility'],
                wind_speed=result['wind_speed'],
                wind_deg=result['wind_deg'],
            )
