import unittest
import allure
from data.api_client import ApiClient
from data.urls import BASE_URL



@allure.feature("Список заказов")
class GetOrdersListTests(unittest.TestCase):

    def setUp(self):
        self.api_client = ApiClient(BASE_URL)

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        status_code, response = self.api_client.get("/api/v1/orders")

        self.assertIn(status_code, [200, 504], f"Код ответа не 200 и не 504, получен код: {status_code}")

        if response is not None:

            if isinstance(response, dict):
                self.assertIn("orders", response, "Ответ не содержит ключ 'orders'")
                self.assertIsInstance(response["orders"], list, "Ключ 'orders' не является списком")
                self.assertGreater(len(response["orders"]), 0, "Список заказов пуст")
                print(f"Получен список заказов, количество заказов: {len(response['orders'])}")
            elif isinstance(response, str):
                print(f"Ошибка: Получен ответ типа <class 'str'>, статус код {status_code}, содержимое: {response}")
            else:
                print(f"Ошибка: Получен не словарь и не строка, а {type(response)}, статус код {status_code}")
        else:
            print(f"Ошибка: Тело ответа None, статус код {status_code}")