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
        config = json.load(config_file)
        if not isinstance(config["days_checked"], int):
            raise ValueError("Illegal days_checked type.")
        if config["days_checked"] < 1 or config["days_checked"] > 15:
            raise ValueError("Illegal days_checked value.")
        return config


def main():
    """Core functionality of the program"""
    # read configurations from config.json
    valid_key = False
    valid_config = False
    try:
        config = read_config("config.json")
        api_key = config["api_key"]
        locations = ingestor(config["locations"])
        interval = config["polling_interval_in_minutes"] * 60
        days_checked = config["days_checked"]

        error_msg = ("Unable to connect to OpenWeatherMap API. "
                     "Trying again in 60sec......\n"
                     "Press Ctrl-C if you wish to terminate.")
        valid_config = True
    except ValueError as error:
        print(error)
        print("\nProcess terminated")

    # check that all locations exist and remove ones that don't
    while(valid_config):
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

    # runs forever logging weather forecasts
    while(valid_key):
        try:
            for loc in locations:
                loc.get_forecast(days_checked, api_key)
            log_forecasts(locations, "./logs/weather_log.txt")
            print("Log entry made at %s" %
                  (datetime.now().strftime("%H:%M")))
            print("If you wish to stop press Ctrl + C")
            sleep(interval)

        except (ConnectionError, ReadTimeout) as error:
            print(error_msg)
            sleep(60)
        except ValueError:
            print("There is something wrong with your API key.\n\n"
                  "Please check the validity of your key from the"
                  "OpenWeatherMap website")
            break
        except KeyboardInterrupt:
            print("\n\nProcess stoped.\n")
            break


if __name__ == "__main__":
    main()
