"""Contains tests for observer package"""
import unittest

from weather.observer import Observer


class TestObserver(unittest.TestCase):
    """tests observer class"""
    def test_instance_creation(self):
        """tests the creation of an Observer"""
        point = Observer(name="Espoo", min_temp=-20, max_temp=30)
        self.assertEqual(point.name, "Espoo")
        self.assertEqual(point.max_temp, 30)
        self.assertEqual(point.min_temp, -20)

    def test_creation_without_name_or_limits(self):
        """tests the creation of an Observer without name or limits"""
        with self.assertRaises(TypeError):
            Observer()

    def test_creation_without_limits(self):
        """tests the creation of an Observer without limits"""
        with self.assertRaises(TypeError):
            Observer("Berlin")

    def test_creation_without_name(self):
        """tests the creation of an Observer without name"""
        with self.assertRaises(TypeError):
            Observer(max_temp=30, min_temp=-30)

    def test_to_string(self):
        """tests the __str__ method"""
        point = Observer("Lodz", max_temp=15, min_temp=-22)
        self.assertEqual(str(point), "Lodz: Min alert: -22, Max alert: 15")

    def test_create_with_empty_forecasts(self):
        """tests that each instance is created with self.forecasts = None"""
        point = Observer("new york", -5, 5)
        self.assertIsNone(point.forecasts)

    def test_get_forecast_with_wrong_api_key(self):
        """tests that status code 401 is returned when polling API with
        incorrect apikey
        """
        point = Observer("Stockholm", -10, 22)
        self.assertEqual(point.get_forecast("qwerty"), 401)

    def test_get_forecast(self):
        """this is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("Tallin", -5, 12)
        # self.assertEqual(point.get_forecast("api key goes here", 200))

    def test_check_location_exists_true(self):
        """this is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("Paris", -2, 11)
        # self.assertTrue(point.check_location_exists("api key here"))

    def test_check_location_exists_false(self):
        """this is a place holder test to be run with real api key.
        I won't write it now to avoid api key ending to Github.
        """
        # point = Observer("qwert123", -2, 11)
        # self.assertFalse(point.check_location_exists("api key here"))
