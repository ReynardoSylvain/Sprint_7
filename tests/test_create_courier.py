import unittest
import requests
import allure
from data.api_client import ApiClient
from data.utils import generate_random_string
from data.urls import BASE_URL


def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


@allure.feature("Курьер")
class CourierTests(unittest.TestCase):

    def setUp(self):
        self.api_client = ApiClient(BASE_URL)

    @allure.title("Создание курьера")
    def test_courier_create_success(self):
        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        status_code, response = self.api_client.post("/api/v1/courier", data=data)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(response)
        self.assertTrue(response["ok"])

    @allure.title("Ошибка создания курьера без логина или пароля")
    def test_courier_create_no_login_or_password(self):
        data = {}
        status_code, response = self.api_client.post("/api/v1/courier", data=data)
        self.assertEqual(status_code, 400)
        self.assertIsNotNone(response)
        self.assertEqual(response["code"], 400)

    @allure.title("Ошибка создания курьера, невозможно создать 2 одинаковых курьера")
    def test_courier_create_duplicate_login(self):
        login_pass = register_new_courier_and_return_login_password()

        data = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        status_code, response = self.api_client.post("/api/v1/courier", data=data)
        self.assertEqual(status_code, 409)
        self.assertIsNotNone(response)
        self.assertEqual(response["code"], 409)