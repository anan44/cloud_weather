"""Main functionality of the program"""
import json
from time import sleep
from datetime import datetime
from requests.exceptions import ConnectionError
from weather.observer import ingestor
from weather.observer import log_forecasts


def read_config(path):
    """Read config file from the given path and returns configs as dict.
    Arguments:
    path - path to config.json file
    """
    with open(path) as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    # read configurations from config.json
    config = read_config("config.json")
    api_key = config["api_key"]
    locations = ingestor(config["locations"])
    interval = config["polling_interval_in_minutes"] * 60

    error_msg = ("Unable to connect to OpenWeatherMap API. "
                 "Trying again in 60sec......\n"
                 "Press Ctrl-C if you wish to terminate.")

    # check all locations exist and remove ones that don't
    while(True):
        try:
            for i, loc in enumerate(locations):
                if not loc.check_location_exists(api_key):
                    print("%s is not available in OpenWeatherMap and it will "
                          "be removed from polling." % (locations.pop(i).name))
            break
        except ConnectionError:
            print(error_msg)
            sleep(60)

    # run forecer check the weather forecasts and writting them to the log
    while(True):
        try:
            for loc in locations:
                loc.get_forecast(api_key)
            log_forecasts(locations, "./logs/weather_log.txt")
            print("Log entry made at %s" %
                  (datetime.now().strftime("%H:%M")))
            sleep(interval)

        except ConnectionError:
            print(error_msg)
            sleep(60)
