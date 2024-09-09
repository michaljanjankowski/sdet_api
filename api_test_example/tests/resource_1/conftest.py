
from typing import Iterator

import pytest

from api_test_example.lib.resource_agnt.resource_1_agnt import Resource1Agent
from api_test_example.lib.resource_agnt.resource_agnt import ResourceAgent


@pytest.fixture(name="resource_agent", scope="function")
def fixture_resource_agent(resource_agent_ssn: ResourceAgent) -> Iterator[ResourceAgent]:
    yield resource_agent_ssn
    resource_agent_ssn.resource_1.delete_all()