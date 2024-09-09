
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from .cons import PROXY_URL, SERVER_PORT, SERVER_URL

import requests

class ApiClient:
    def __init__(
        self,
        url: str = f"http://{SERVER_URL}:{SERVER_PORT}/api/v1",
    ) -> None:
        self.url = url
        self.session = requests.Session()

    def login(self, username: str, password: str) -> None:
        payload = {"username": f"{username}", "password": f"{password}"}

        resp = self.session.post(url=f"{self.url}/auth/login", data=json.dumps(payload))
        if resp.status_code != 201:
            raise ValueError(f"Failed to login to {self.url} using {username} and {password}")
        access_token = resp.json()["access_token"]
        if not access_token:
            raise KeyError(f"Access token was not returned in resp {resp}")

        self.set_token(access_token=access_token)

    def logout(self) -> None:
        resp = self.session.post(url=f"{self.url}/auth/logout")
        if resp.status_code != 204:
            raise ValueError("Failed to logout")