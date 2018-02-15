"""Contains Observer class and related functionalities"""
import requests
import json
import time
from datetime import datetime


class Observer():
    """Observation point and related limits.
    Init arguments:
    name - name of the location
    min_temp - lower temperature limit for alarms
    max_temp - higher temperature limit for alarms
    """
    def __init__(self, name, min_temp, max_temp):
        self.name = name
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.forecasts = None

    def __str__(self):
        return "%s: Min alert: %s, Max alert: %s" % (self.name, self.min_temp,
                                                     self.max_temp)

    def get_forecast(self, days, api_key):
        """Requests for weather data from OpenWeatherMap API.
        Arguments:
        days - number of days to be polled per location
        api_key - api_key for OpenWeatherMap
        """
        baseurl = "http://api.openweathermap.org/data/2.5/forecast/" \
                  "daily?q=%s&cnt=%s&units=metric&APPID=%s"
        url = baseurl % (self.name, days, api_key)

        response = requests.get(url)
        if response.ok:
            data = json.loads(response.content)
            self.forecasts = data["list"]
        elif response.status_code == 401:
            raise ValueError("Invalid API key.")
        return response.status_code

    def get_alerts(self, day):
        """Gets a string of alarms specifying all possible alarms for the given
        day index.
        Arguments:
        day - index of the day from forecasts
        """
        alarm = ""
        temp = self.forecasts[day]["temp"]
        if temp["min"] <= self.min_temp:
            alarm += "Low limit %s reached;" % (self.min_temp)

        if temp["max"] >= self.max_temp:
            alarm += "High limit %s reached;" % (self.max_temp)

        if not alarm:
            return "n/a"
        else:
            return alarm

    def check_location_exists(self, api_key):
        """Checks if a location exists in OpenWeatherMap.
        Arguments:
        api_key - api_key for OpenWeatherMap
        """
        baseurl = "http://api.openweathermap.org/data/2.5/forecast/" \
                  "daily?q=%s&cnt=5&units=metric&APPID=%s"
        url = baseurl % (self.name, api_key)

        response = requests.get(url)
        if response.status_code == 404:
            return False
        elif response.status_code == 401:
            raise ValueError("Invalid API key.")
        else:
            return True

    def get_log_data(self):
        """Gets loggable string from forecast data.
        No arguments.
        """
        log_entry = self.name + "\n"
        for i in range(len(self.forecasts)):
            timestamp = self.forecasts[i]["dt"]
            temp = self.forecasts[i]["temp"]
            date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
            weather = "\t\tday: %s; min: %s; max: %s;\n" % (temp["day"],
                                                            temp["min"],
                                                            temp["max"])
            alert = "Alert: " + self.get_alerts(i)
            log_entry += "\t%s\n%s\t\t%s\n" % (date, weather, alert)
        return log_entry


def ingestor(locations):
    """Turns a list of locations and limit temperaturs to a list of Observers
    required list format is as follows: name, min_temp, max_temp.
    arguments:
    locations - list of observer objects
    """
    observers = [Observer(loc["name"], loc["low_limit"], loc["high_limit"])
                 for loc in locations]

    return observers


def log_forecasts(locations, log_path):
    """Takes a list of locations and appends their forecasts to log file.
    arguments:
    locations - list of observer objects
    log_path - path to the logfile
    """
    time_now = datetime.fromtimestamp(time.time())
    time_str = time_now.strftime("%d.%m.%Y %H:%M:%S")
    line = "-" * 45 + "\n"
    locs = ""
    for loc in locations:
        locs += loc.get_log_data()

    entry = ("Polled at: {time_str}\n{locs}"
             "{line}".format(time_str=time_str, locs=locs, line=line))

    with open(log_path, "a") as output:
        output.write(entry)
