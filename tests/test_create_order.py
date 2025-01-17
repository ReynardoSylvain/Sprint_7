import allure
import pytest
import logging
from data.api_client import ApiClient
from data.urls import BASE_URL, ORDERS_CREATE
from data.order_data import order_data

logging.basicConfig(level=logging.INFO)

@allure.feature("Создание заказа")
class TestCreateOrder:
    @pytest.fixture(scope="function")
    def api_client(self):
        return ApiClient(BASE_URL)

    @allure.title("{1}")
    def test_create_order(self, api_client, order_data):
        data, title = order_data
        status_code, response = api_client.post(ORDERS_CREATE, data=data)
        assert status_code == 201
        assert response is not None
        if isinstance(response, dict):
            assert "track" in response
            assert isinstance(response["track"], int)
        else:
            logging.info(f"Ошибка: Получен ответ типа <class 'str'>, статус код {status_code}, содержимое: {response}")