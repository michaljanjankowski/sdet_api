from collections.abc import Iterator
from threading import Thread

import pytest

from api_test_example.library.data_gens.base import DataGen
from api_test_example.library.resource_agnt.resource_agnt import ResourceAgent
from api_test_example.sample_api import SampleApiServer
from api_test_example.utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_url() -> Iterator[str]:
    server = SampleApiServer(("127.0.0.1", 0))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/api/v1"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.fixture
def data_gen() -> DataGen:
    return DataGen()


@pytest.fixture
def api_client(api_url: str) -> Iterator[ApiClient]:
    client = ApiClient(api_url)
    client.login("root", "pass1")
    try:
        yield client
    finally:
        client.close_session()


@pytest.fixture
def resource_agent(api_client: ApiClient) -> Iterator[ResourceAgent]:
    agent = ResourceAgent(api_client)
    try:
        yield agent
    finally:
        agent.delete_all()
