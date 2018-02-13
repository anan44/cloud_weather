import unittest
import main


class TestMain(unittest.TestCase):
    """tests for the main.py functions"""
    def test_read_config(self):
        """tests reading config json file"""
        config = main.read_config("config_template.json")

        self.assertEqual(config["api_key"], "Your API key goes here")
        self.assertEqual(config["polling_interval_in_minutes"], 180)
        self.assertEqual(config["locations"][0]["name"], "Vantaa")
        self.assertEqual(config["days_checked"], 5)
