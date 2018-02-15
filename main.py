"""Main functionality of the program"""
import json
from time import sleep
from datetime import datetime
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from weather.observer import ingestor
from weather.observer import log_forecasts


def read_config(path):
    """Read config file from the given path and returns configs as dict.
    Arguments:
    path - path to config.json file
    """
    with open(path) as config_file:
        # TODO raise error for illegal values
        return json.load(config_file)


if __name__ == "__main__":
    # read configurations from config.json
    config = read_config("config.json")
    api_key = config["api_key"]
    locations = ingestor(config["locations"])
    interval = config["polling_interval_in_minutes"] * 60
    days_checked = config["days_checked"]

    error_msg = ("Unable to connect to OpenWeatherMap API. "
                 "Trying again in 60sec......\n"
                 "Press Ctrl-C if you wish to terminate.")
    valid_key = False
    # check all locations exist and remove ones that don't
    while(True):
        try:
            for i, loc in enumerate(locations):
                if not loc.check_location_exists(api_key):
                    print("%s is not available in OpenWeatherMap and it will "
                          "be removed from polling." % (locations.pop(i).name))
            valid_key = True
            break
        except (ConnectionError, ReadTimeout) as error:
            print(error_msg)
            sleep(60)
        except ValueError:
            print("The API key provided was not accepted by the"
                  "OpenWeatherMap API.\n\n"
                  "In case you just created the key, it might take up to "
                  "10min to activate the new key. In such cases please wait "
                  "patiently and try again in a while.\n\n"
                  "If this is not the case, please double check the API you "
                  "have provided.")
            break

    # run forecer check the weather forecasts and writting them to the log
    while(valid_key):
        try:
            for loc in locations:
                loc.get_forecast(days_checked, api_key)
            log_forecasts(locations, "./logs/weather_log.txt")
            print("Log entry made at %s" %
                  (datetime.now().strftime("%H:%M")))
            sleep(interval)

        except (ConnectionError, ReadTimeout) as error:
            print(error_msg)
            sleep(60)
