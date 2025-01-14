import unittest
import allure
from data.api_client import ApiClient
from data.utils import generate_random_string
from data.urls import BASE_URL


@allure.feature("Создание заказа")
class OrderTests(unittest.TestCase):
    def setUp(self):
        self.api_client = ApiClient(BASE_URL)

    @allure.title("Создание заказа с цветом BLACK")
    def test_create_order_with_black_color(self):
        data = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(15),
            "metroStation": generate_random_string(2),
            "phone": "+7" + generate_random_string(10),
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "Test order",
            "color": ["BLACK"]
        }
        status_code, response = self.api_client.post("/api/v1/orders", data=data)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(response)
        if isinstance(response, dict):
            self.assertIn("track", response)
            self.assertIsInstance(response["track"], int)

    @allure.title("Создание заказа с цветом GREY")
    def test_create_order_with_grey_color(self):
        data = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(15),
            "metroStation": generate_random_string(2),
            "phone": "+7" + generate_random_string(10),
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "Test order",
            "color": ["GREY"]
        }
        status_code, response = self.api_client.post("/api/v1/orders", data=data)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(response)
        if isinstance(response, dict):
            self.assertIn("track", response)
            self.assertIsInstance(response["track"], int)

    @allure.title("Создание заказа с цветом BLACK и GREY")
    def test_create_order_with_black_and_grey_color(self):
        data = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(15),
            "metroStation": generate_random_string(2),
            "phone": "+7" + generate_random_string(10),
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "Test order",
            "color": ["BLACK", "GREY"]
        }
        status_code, response = self.api_client.post("/api/v1/orders", data=data)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(response)
        if isinstance(response, dict):
            self.assertIn("track", response)
            self.assertIsInstance(response["track"], int)

    @allure.title("Создание заказа без цвета")
    def test_create_order_without_color(self):
        data = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(15),
            "metroStation": generate_random_string(2),
            "phone": "+7" + generate_random_string(10),
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "Test order",
            "color": []
        }
        status_code, response = self.api_client.post("/api/v1/orders", data=data)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(response)
        if isinstance(response, dict):
            self.assertIn("track", response)
            self.assertIsInstance(response["track"], int)