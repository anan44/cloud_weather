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
        point = Observer("Lodz", max_temp=15, min_temp=-22)
        self.assertEqual(str(point), "Lodz: Min alert: -22, Max alert: 15")

    def test_create_with_empty_forecasts(self):
        point = Observer("new york", -5, 5)
        self.assertIsNone(point.forecasts)
