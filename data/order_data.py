import pytest
from data.utils import generate_random_string

@pytest.fixture(params=[
    (["BLACK"], "Создание заказа с цветом BLACK"),
    (["GREY"], "Создание заказа с цветом GREY"),
    (["BLACK", "GREY"], "Создание заказа с цветом BLACK и GREY"),
    ([], "Создание заказа без цвета")
])
def order_data(request):
   color, title = request.param
   data =  {
       "firstName": generate_random_string(10),
       "lastName": generate_random_string(10),
       "address": generate_random_string(15),
       "metroStation": generate_random_string(2),
       "phone": "+7" + generate_random_string(10),
       "rentTime": 5,
       "deliveryDate": "2024-06-06",
       "comment": "Test order",
        "color": color
    }
   return data, title