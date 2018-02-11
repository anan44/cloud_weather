"""main functionality of the program"""
import json


def read_config(path):
    """read config file from the given path and returns configs as dict"""
    with open(path) as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    config = read_config("config.json")
    print(config["api_key"])
