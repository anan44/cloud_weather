"""Contains Observer class and related functionalities"""
import requests
import json

class Observer():
    """Observation point and related limits.
    init arguments:
    name - name of the location
    min_temp = lower temperature limit for alarms
    max_temp = higher temperature limit for alarms
    """
    def __init__(self, name, min_temp, max_temp):
        self.name = name
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.forecasts = None

    def __str__(self):
        return "%s: Min alert: %s, Max alert: %s" % (self.name, self.min_temp,
                                                     self.max_temp)

    def get_forecast(self, api_key):
        """requests for weather data from OpenWeatherMap API
        arguments:
        api_key - api_key for OpenWeatherMap
        """
        baseurl = "http://api.openweathermap.org/data/2.5/forecast/" \
                  "daily?q=%s&cnt=5&units=metric&APPID=%s"
        url = baseurl % (self.name, api_key)

        response = requests.get(url)
        if response.ok:
            data = json.loads(response.content)
            self.forecasts = data["list"]

        return response.status_code
