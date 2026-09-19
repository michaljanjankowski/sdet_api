from typing import Any

import requests


class ApiClient:
    def __init__(self, url: str, timeout: float = 5.0, session: requests.Session | None = None) -> None:
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self.session.request(
            method, f"{self.url}/{path.lstrip('/')}", timeout=self.timeout, **kwargs
        )

    def login(self, username: str, password: str) -> None:
        response = self.request("POST", "login", json={"username": username, "password": password})
        response.raise_for_status()
        self.set_token(response.json()["access_token"])

    def set_token(self, access_token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {access_token}"

    def logout(self) -> None:
        response = self.request("POST", "logout")
        response.raise_for_status()
        self.session.headers.pop("Authorization", None)

    def get(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        return self.request("GET", path, params=params)

    def post(self, path: str, json_data: dict[str, Any]) -> requests.Response:
        return self.request("POST", path, json=json_data)

    def put(self, path: str, json_data: dict[str, Any]) -> requests.Response:
        return self.request("PUT", path, json=json_data)

    def delete(self, path: str) -> requests.Response:
        return self.request("DELETE", path)

    def close_session(self) -> None:
        self.session.close()
