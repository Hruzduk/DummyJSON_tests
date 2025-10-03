import pytest
import requests


class APIClient:
    def __init__(self, base_url="https://dummyjson.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        if self.token and not headers:
            headers = {"Authorization": f"Bearer {self.token}"}
        elif self.token and headers:
            headers["Authorization"] = f"Bearer {self.token}"

        response = self.session.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        if self.token and not headers:
            headers = {"Authorization": f"Bearer {self.token}"}
        elif self.token and headers:
            headers["Authorization"] = f"Bearer {self.token}"

        response = self.session.post(url, data=data, json=json, headers=headers)
        return response

    def set_token(self, token):
        self.token = token


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def test_user_credentials():
    return {
        "username": "emilys",
        "password": "emilyspass"
    }


@pytest.fixture(scope="session")
def authenticated_client(api_client, test_user_credentials):
    response = api_client.post(
        "/auth/login",
        json=test_user_credentials
    )

    if response.status_code == 200:
        token = response.json().get("accessToken")
        api_client.set_token(token)
        return api_client
    else:
        pytest.fail(f"Failed to authenticate: {response.status_code} - {response.text}")


@pytest.fixture(scope="session")
def products_data(api_client):
    response = api_client.get("/products")
    if response.status_code == 200:
        return response.json().get("products", [])
    return []