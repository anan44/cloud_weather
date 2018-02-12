"""Contains tests for observer package"""
import unittest
import re
from os import remove

from weather.observer import Observer
from weather.observer import ingestor
from weather.observer import log_forecasts


class TestObserver(unittest.TestCase):
    """Tests observer class."""
    def test_instance_creation(self):
        """Tests the creation of an Observer."""
        point = Observer(name="Espoo", min_temp=-20, max_temp=30)
        self.assertEqual(point.name, "Espoo")
        self.assertEqual(point.max_temp, 30)
        self.assertEqual(point.min_temp, -20)

    def test_creation_without_name_or_limits(self):
        """Tests the creation of an Observer without name or limits."""
        with self.assertRaises(TypeError):
            Observer()

    def test_creation_without_limits(self):
        """Tests the creation of an Observer without limits."""
        with self.assertRaises(TypeError):
            Observer("Berlin")

    def test_creation_without_name(self):
        """Tests the creation of an Observer without name."""
        with self.assertRaises(TypeError):
            Observer(max_temp=30, min_temp=-30)

    def test_to_string(self):
        """Tests the __str__ method."""
        point = Observer("Lodz", max_temp=15, min_temp=-22)
        self.assertEqual(str(point), "Lodz: Min alert: -22, Max alert: 15")

    def test_create_with_empty_forecasts(self):
        """Tests that each instance is created with self.forecasts = None"""
        point = Observer("new york", -5, 5)
        self.assertIsNone(point.forecasts)

    def test_get_forecast_with_wrong_api_key(self):
        """Tests that status code 401 is returned when polling API with
        incorrect apikey
        """
        point = Observer("Stockholm", -10, 22)
        self.assertEqual(point.get_forecast("qwerty"), 401)

    def test_get_forecast(self):
        """This is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("Tallin", -5, 12)
        # self.assertEqual(point.get_forecast("api key goes here", 200))

    def test_check_location_exists_true(self):
        """This is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("Paris", -2, 11)
        # self.assertTrue(point.check_location_exists("api key here"))

    def test_check_location_exists_false(self):
        """This is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("qwert123", -2, 11)
        # self.assertFalse(point.check_location_exists("api key here"))

    def test_get_log_data_format(self):
        """Tests the form of get_log_data string."""
        point = Observer("Vantaa", 0, 25)
        point.forecasts = [{'dt': 1518429600,
                            'temp': {'day': -2, 'min': -2.35, 'max': -2,
                                     'night': -2.35, 'eve': -2, 'morn': -2}},
                           {'dt': 1518516000,
                            'temp': {'day': -1.3, 'min': -2.13, 'max': -0.5,
                                     'night': -1.48, 'eve': -0.86,
                                     'morn': -2.02}}]

        self.assertTrue("Vantaa" in point.get_log_data())
        self.assertTrue("12.02.2018" in point.get_log_data())
        self.assertTrue("13.02.2018" in point.get_log_data())
        self.assertTrue("day: -2; min: -2.35; max: -2" in point.get_log_data())


class TestObserverUtils(unittest.TestCase):
    """Tests for the utility functions in observer package."""
    def test_ingestor_singe_location(self):
        """Tests the successful use of ingestor."""
        json_dict = [{"name": "Copenhagen",
                      "low_limit": -2,
                      "high_limit": 4}]
        locations = ingestor(json_dict)
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].name, "Copenhagen")
        self.assertEqual(locations[0].min_temp, -2)
        self.assertEqual(locations[0].max_temp, 4)

    def test_ingestor_multiple_locations(self):
        """Tests the successful use of ingestor with multiple inputs."""
        json_dict = [{"name": "Copenhagen",
                      "low_limit": -2,
                      "high_limit": 4},
                     {"name": "Helsinki",
                      "low_limit": -5,
                      "high_limit": 12},
                     {"name": "Hong Kong",
                      "low_limit": 4,
                      "high_limit": 22}]
        locations = ingestor(json_dict)
        self.assertEqual(len(locations), 3)
        self.assertEqual(locations[0].name, "Copenhagen")
        self.assertEqual(locations[1].name, "Helsinki")
        self.assertEqual(locations[2].name, "Hong Kong")
        self.assertEqual(locations[1].min_temp, -5)
        self.assertEqual(locations[2].max_temp, 22)

    def test_ingestor_corrupted_input(self):
        """Tests the failed use of ingestor with corrupted input data."""
        json_dict = [{"value": "Tallin",
                      "low_limit": 5,
                      "high_limit": 11}]
        with self.assertRaises(KeyError):
            ingestor(json_dict)

    def test_log_forecasts_no_alerts(self):
        """Tests that log_forecasts is able to append log as intended"""
        point1 = Observer("Tokyo", -19, 10)
        point1.forecasts = [{'dt': 1518429600,
                            'temp': {'day': -2, 'min': -2.35, 'max': -2,
                                     'night': -2.35, 'eve': -2, 'morn': -2}},
                            {'dt': 1518516000,
                             'temp': {'day': -1.3, 'min': -2.13, 'max': -0.5,
                                      'night': -1.48, 'eve': -0.86,
                                      'morn': -2.02}}]
        point2 = Observer("Warsaw", -22, 16)
        point2.forecasts = [{'dt': 1518429600,
                            'temp': {'day': 4, 'min': 2.55, 'max': 5,
                                     'night': 2.35, 'eve': 3, 'morn': 2}},
                            {'dt': 1518516000,
                             'temp': {'day': 0.3, 'min': 2.13, 'max': 0.8,
                                      'night': 4, 'eve': 0.86, 'morn': 2.02}}]
        locations = [point1, point2]
        log_forecasts(locations, "./logs/test_log.txt")
        with open("./logs/test_log.txt", "r") as log_file:
            log_lines = log_file.readlines()
        result = re.search(r"(Polled at: \d\d\.\d\d\.\d{4} \d\d:\d\d:\d\d)",
                           log_lines[0])
        self.assertTrue(bool(result))
        self.assertEqual("Tokyo\n", log_lines[1])
        self.assertEqual("Warsaw\n", log_lines[6])
        self.assertEqual("\t12.02.2018\n", log_lines[2])
        self.assertEqual("\t13.02.2018\n", log_lines[4])
        self.assertEqual("\t\tday: -2; min: -2.35; max: -2;\n", log_lines[3])
        self.assertEqual("\t\tday: -1.3; min: -2.13; max: -0.5;\n",
                         log_lines[5])
        remove("./logs/test_log.txt")
