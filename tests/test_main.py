import unittest
import main


class TestMain(unittest.TestCase):
    """tests for the main.py functions"""
    def test_read_config(self):
        """tests reading config json file"""
        config = main.read_config("config_template.json")

        self.assertEqual(config["api_key"], "qwerty123")
        self.assertEqual(config["polling_interval_in_minutes"], 5)
        self.assertEqual(config["locations"][0]["name"], "Vantaa")
