

import os
from datetime import datetime
from typing import Iterator

import pytest

from api_test_example.lib.data_gens.base import DataGen
from api_test_example.utils.api_client import ApiClient
from api_test_example.lib.resource_agnt.resource_agnt import ResourceAgent
from api_test_example.utils.cons import (
    ADMIN_USER,
    TEST_USER,
    COMMON_PASSWORD,
    DEFAULT_PASSWORD,
)

@pytest.fixture(name="data_gen", scope="session")
def fixture_data_generator() -> DataGen:
    return DataGen()


@pytest.fixture(name="admin_api_client", scope="session")
def fixture_admin_api_client() -> Iterator[ApiClient]:
    api_client = ApiClient()
    try:
        api_client.login(username=ADMIN_USER, password=COMMON_PASSWORD)
    except ValueError:
        api_client.login(username=ADMIN_USER, password=DEFAULT_PASSWORD)

    yield api_client
    api_client.close_session()


@pytest.fixture(name="admin_resource_agent", scope="session")
def fixture_admin_resource_agent(admin_api_client: ApiClient) -> Iterator[ResourceAgent]:
    yield ResourceAgent(api_client=admin_api_client)



@pytest.fixture(name="admin_resource_agent", scope="session")
def fixture_admin_resource_agent(admin_api_client: ApiClient) -> Iterator[ResourceAgent]:
    yield ResourceAgent(api_client=admin_api_client)


@pytest.fixture(name="api_client", scope="session")
def fixture_api_client(
    admin_resource_agent: ResourceAgent, data_gen: DataGen
) -> Iterator[ApiClient]:
    admin_resource_agent.users.create(
        data=data_gen.users.create_data(username=TEST_USER, password=COMMON_PASSWORD)
    )
    api_client = ApiClient()
    api_client.login(username=TEST_USER, password=COMMON_PASSWORD)
    yield api_client
    api_client.close_session()


@pytest.fixture(name="resource_agent_ssn", scope="session")
def fixture_resource_agent_ssn(api_client: ApiClient) -> ResourceAgent:
    return ResourceAgent(api_client=api_client)