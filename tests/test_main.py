import unittest
import main
import json
from os import remove


class TestMain(unittest.TestCase):
    """Tests for the main.py functions"""
    def tearDown(self):
        """Removes config_test.json file"""
        try:
            remove("config_test.json")
        except FileNotFoundError:
            pass

    def test_read_config(self):
        """Tests reading config json file"""
        config = main.read_config("config_template.json")

        self.assertEqual(config["api_key"], "Your API key goes here")
        self.assertEqual(config["polling_interval_in_minutes"], 180)
        self.assertEqual(config["locations"][0]["name"], "Vantaa")
        self.assertEqual(config["days_checked"], 5)

    def test_read_config_illegal_value_zero(self):
        """Tests reading config json file with illegal value 0"""
        test_dict = {"polling_interval_in_minutes": 180,
                     "api_key": "Your API key goes here",
                     "days_checked": 0
                     }
        with open("config_test.json", "w") as test_file:
            json.dump(test_dict, test_file)

        with self.assertRaises(ValueError):
            main.read_config("config_test.json")

    def test_read_config_illegal_value_str(self):
        """Tests reading config json file with illegal value string"""
        test_dict = {"polling_interval_in_minutes": 180,
                     "api_key": "Your API key goes here",
                     "days_checked": "6"
                     }
        with open("config_test.json", "w") as test_file:
            json.dump(test_dict, test_file)

        with self.assertRaises(ValueError):
            main.read_config("config_test.json")

    def test_read_config_illegal_value_high(self):
        """Tests reading config json file with illegal high value"""
        test_dict = {"polling_interval_in_minutes": 180,
                     "api_key": "Your API key goes here",
                     "days_checked": 20
                     }
        with open("config_test.json", "w") as test_file:
            json.dump(test_dict, test_file)

        with self.assertRaises(ValueError):
            main.read_config("config_test.json")
