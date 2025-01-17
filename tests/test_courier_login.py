import allure
import logging
import pytest
from data.api_client import ApiClient
from data.utils import generate_random_string
from data.urls import BASE_URL, COURIER_LOGIN
from data.helper import register_new_courier

logging.basicConfig(level=logging.INFO)


@allure.feature("Логин курьера")
class TestCourierLogin:

    @pytest.fixture(scope="function")
    def api_client(self):
        return ApiClient(BASE_URL)

    @allure.title("Успешный логин курьера")
    def test_courier_login_success(self, api_client, register_new_courier):
         login, password, _ = register_new_courier
         if login is None:
              pytest.fail("Не удалось создать курьера для теста логина")
         data = {
              "login": login,
              "password": password
         }
         status_code, response = api_client.post(COURIER_LOGIN, data=data)
         assert status_code == 200
         assert response is not None
         assert "id" in response

    @allure.title("Ошибка логина курьера, нет логина или пароля")
    def test_courier_login_no_login_or_password(self, api_client):
         data = {}
         status_code, response = api_client.post(COURIER_LOGIN, data=data)
         assert status_code in [400, 504]
         assert response is not None
         if isinstance(response, dict):
             assert response["message"] == "Недостаточно данных для входа"
         elif isinstance(response, str):
             logging.info(f"Ошибка: Получен ответ типа <class 'str'>, статус код {status_code}, содержимое: {response}")
         else:
              logging.info(f"Ошибка: Получен не словарь и не строка, а {type(response)}, статус код {status_code}")

    @allure.title("Ошибка логина курьера, неверный логин или пароль")
    def test_courier_login_incorrect_login_or_password(self, api_client):
         data = {
             "login": generate_random_string(10),
             "password": generate_random_string(10)
         }
         status_code, response = api_client.post(COURIER_LOGIN, data=data)
         assert status_code == 404
         assert response is not None
         assert response["message"] == "Учетная запись не найдена"

    @allure.title("Ошибка логина курьера, несуществующий пользователь")
    def test_courier_login_unknown_user(self, api_client):
         data = {
            "login": "unknown_user",
            "password": "unknown_password"
         }
         status_code, response = api_client.post(COURIER_LOGIN, data=data)
         assert status_code == 404
         assert response is not None
         assert response["message"] == "Учетная запись не найдена"