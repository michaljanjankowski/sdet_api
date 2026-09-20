import os
from collections.abc import Iterator

import httpx
import pytest

from mockserver_example.clients.users_client import UsersClient


@pytest.fixture(scope="session")
def mockserver_url() -> str:
    url = os.getenv("MOCKSERVER_URL")
    if not url:
        pytest.skip("Set MOCKSERVER_URL or run docker compose up --build --exit-code-from api-tests")
    return url


@pytest.fixture
def users_client(mockserver_url: str) -> Iterator[UsersClient]:
    client = UsersClient(mockserver_url)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def raw_client(mockserver_url: str) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=mockserver_url, timeout=2.0) as client:
        yield client
