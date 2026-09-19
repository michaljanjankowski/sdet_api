"""Example of injecting an HTTP session so requests can be tested without network access."""

import requests


class StatusClient:
    def __init__(self, base_url: str, session: requests.Session | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def get_status(self) -> str:
        response = self.session.get(f"{self.base_url}/status", timeout=5)
        response.raise_for_status()
        return response.json()["status"]
