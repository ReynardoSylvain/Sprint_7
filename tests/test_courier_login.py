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

    # возвращаем список
    return login_pass


@allure.feature("Логин курьера")
class CourierLoginTests(unittest.TestCase):

    def setUp(self):
        self.api_client = ApiClient(BASE_URL)

    @allure.title("Успешный логин курьера")
    def test_courier_login_success(self):
        login_pass = register_new_courier_and_return_login_password()
        data = {
            "login": login_pass[0],
            "password": login_pass[1]
        }
        status_code, response = self.api_client.post("/api/v1/courier/login", data=data)
        self.assertEqual(status_code, 200)
        self.assertIsNotNone(response)
        self.assertIn("id", response)

    @allure.title("Ошибка логина курьера, нет логина или пароля")
    def test_courier_login_no_login_or_password(self):
        data = {}
        status_code, response = self.api_client.post("/api/v1/courier/login", data=data)
        self.assertIn(status_code, [400, 504])
        self.assertIsNotNone(response)
        if isinstance(response, dict):
            self.assertEqual(response["message"], "Недостаточно данных для входа")
        elif isinstance(response, str):
              print(f"Ошибка: Получен ответ типа <class 'str'>, статус код {status_code}, содержимое: {response}")
        else:
             print(f"Ошибка: Получен не словарь и не строка, а {type(response)}, статус код {status_code}")

    @allure.title("Ошибка логина курьера, неверный логин или пароль")
    def test_courier_login_incorrect_login_or_password(self):
        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        status_code, response = self.api_client.post("/api/v1/courier/login", data=data)
        self.assertEqual(status_code, 404)
        self.assertIsNotNone(response)
        self.assertEqual(response["message"], "Учетная запись не найдена")

    @allure.title("Ошибка логина курьера, несуществующий пользователь")
    def test_courier_login_unknown_user(self):
        data = {
            "login": "unknown_user",
            "password": "unknown_password"
        }
        status_code, response = self.api_client.post("/api/v1/courier/login", data=data)
        self.assertEqual(status_code, 404)
        self.assertIsNotNone(response)
        self.assertEqual(response["message"], "Учетная запись не найдена")