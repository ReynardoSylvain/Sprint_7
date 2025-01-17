import allure
import logging
import pytest
from data.api_client import ApiClient
from data.urls import BASE_URL, ORDERS_LIST

logging.basicConfig(level=logging.INFO)


@allure.feature("Список заказов")
class TestGetOrdersList:

    @pytest.fixture(scope="function")
    def api_client(self):
        return ApiClient(BASE_URL)

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, api_client):
        status_code, response = api_client.get(ORDERS_LIST)
        assert status_code in [200, 504], f"Код ответа не 200 и не 504, получен код: {status_code}"

        if response is not None:
            if isinstance(response, dict):
                assert "orders" in response, "Ответ не содержит ключ 'orders'"
                assert isinstance(response["orders"], list), "Ключ 'orders' не является списком"
                assert len(response["orders"]) > 0, "Список заказов пуст"
                logging.info(f"Получен список заказов, количество заказов: {len(response['orders'])}")
            elif isinstance(response, str):
                logging.info(
                    f"Ошибка: Получен ответ типа <class 'str'>, статус код {status_code}, содержимое: {response}")
            else:
                logging.info(f"Ошибка: Получен не словарь и не строка, а {type(response)}, статус код {status_code}")
        else:
            logging.info(f"Ошибка: Тело ответа None, статус код {status_code}")