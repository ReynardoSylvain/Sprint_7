import requests
import json

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _send_request(self, method, endpoint, data=None, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, json=data, params=params, headers=headers)
            if response.text:
                try:
                    response_json = response.json()
                except json.JSONDecodeError:
                    return response.status_code, response.text
                return response.status_code, response_json
            else:
               return response.status_code, None
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None, None

    def post(self, endpoint, data=None, params=None, headers=None):
        return self._send_request("POST", endpoint, data, params, headers)

    def get(self, endpoint, params=None, headers=None):
        return self._send_request("GET", endpoint, params=params, headers=headers)

    def put(self, endpoint, data=None, params=None, headers=None):
        return self._send_request("PUT", endpoint, data, params, headers)

    def delete(self, endpoint, params=None, headers=None):
         return self._send_request("DELETE", endpoint, params=params, headers=headers)