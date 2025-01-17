import allure
import pytest
from data.api_client import ApiClient
from data.utils import generate_random_string
from data.urls import BASE_URL, COURIER_CREATE
from data.helper import register_new_courier


@allure.feature("Курьер")
class TestCourierCreate:

    @pytest.fixture(scope="function")
    def api_client(self):
        return ApiClient(BASE_URL)

    @allure.title("Создание курьера")
    def test_courier_create_success(self, api_client):
        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        status_code, response = api_client.post(COURIER_CREATE, data=data)
        assert status_code == 201
        assert response is not None
        assert response["ok"] is True

    @allure.title("Ошибка создания курьера без логина или пароля")
    def test_courier_create_no_login_or_password(self, api_client):
        data = {}
        status_code, response = api_client.post(COURIER_CREATE, data=data)
        assert status_code == 400
        assert response is not None
        assert response["code"] == 400

    @allure.title("Ошибка создания курьера, невозможно создать 2 одинаковых курьера")
    def test_courier_create_duplicate_login(self, api_client, register_new_courier):
        login, password, _ = register_new_courier
        if login is None:
            pytest.fail("Не удалось создать курьера для проверки дубликата")
        data = {
            "login": login,
            "password": password,
            "firstName": generate_random_string(10)
        }
        status_code, response = api_client.post(COURIER_CREATE, data=data)
        assert status_code == 409
        assert response is not None
        assert response["code"] == 409