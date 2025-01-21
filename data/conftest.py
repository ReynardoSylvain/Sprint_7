import pytest
import requests
from data.utils import generate_random_string
from data.urls import BASE_URL, COURIER_CREATE
from data.api_client import ApiClient

@pytest.fixture(scope="function")
def api_client():
    return ApiClient(BASE_URL)

@pytest.fixture
def register_new_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    api_client = ApiClient(BASE_URL)
    response = requests.post(BASE_URL + COURIER_CREATE, json=payload)
    if response.status_code == 201:
        yield login, password, first_name
    else:
        yield None, None, None

    login_data = {"login": login, "password": password}
    status_code, login_response = api_client.post("/api/v1/courier/login", data=login_data)
    if login_response and "id" in login_response:
        courier_id = login_response["id"]
        api_client.delete(f"/api/v1/courier/{courier_id}")

