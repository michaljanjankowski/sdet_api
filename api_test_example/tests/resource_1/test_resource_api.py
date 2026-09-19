from http import HTTPStatus

from api_test_example.library.data_gens.base import DataGen
from api_test_example.library.resource_agnt.base import QueryParams
from api_test_example.library.resource_agnt.resource_agnt import ResourceAgent
from api_test_example.library.resource_agnt.rest_response import ErrorResponse
from api_test_example.models import Resource1PutRequest, Resource1Response
from api_test_example.utils.api_client import ApiClient


def test_resource_crud(resource_agent: ResourceAgent, data_gen: DataGen) -> None:
    agent = resource_agent.resource_1
    created = agent.create(data_gen.resource1gen.create_data("first", "value"))
    created.check_status(HTTPStatus.CREATED)
    assert isinstance(created.response, Resource1Response)
    resource = created.response

    fetched = agent.get(resource)
    fetched.check_status(HTTPStatus.OK)
    assert fetched.response == resource

    updated = agent.update(resource, Resource1PutRequest(field1="changed", field2="new"))
    updated.check_status(HTTPStatus.OK)
    assert isinstance(updated.response, Resource1Response)
    assert updated.response.field1 == "changed"

    action = agent.special_action(updated.response)
    action.check_status(HTTPStatus.OK)
    assert action.response.result == "CHANGED"

    agent.delete(updated.response).check_status(HTTPStatus.NO_CONTENT)
    missing = agent.get(updated.response)
    missing.check_status(HTTPStatus.NOT_FOUND)
    assert isinstance(missing.response, ErrorResponse)


def test_filter_and_pagination(resource_agent: ResourceAgent, data_gen: DataGen) -> None:
    agent = resource_agent.resource_1
    for field1 in ("same", "other", "same"):
        agent.create(data_gen.resource1gen.create_data(field1, "value")).check_status(HTTPStatus.CREATED)

    page = agent.list(QueryParams(field1="same", page=2, page_size=1))
    page.check_status(HTTPStatus.OK)
    assert page.response.total == 2
    assert len(page.response.items) == 1
    assert page.response.items[0].field1 == "same"


def test_invalid_payload_returns_400(api_client: ApiClient) -> None:
    response = api_client.post("resource1", {"field1": "", "field2": "value"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["error"] == "Invalid resource data"


def test_unauthorized_request_returns_401(api_url: str) -> None:
    client = ApiClient(api_url)
    try:
        response = client.get("resource1")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["error"] == "Authentication required"
    finally:
        client.close_session()


def test_read_only_user_cannot_create_resource(api_url: str) -> None:
    client = ApiClient(api_url)
    client.login("reader", "pass1")
    try:
        response = client.post("resource1", {"field1": "first", "field2": "value"})
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["error"] == "Write access required"
        assert client.get("resource1").status_code == HTTPStatus.OK
    finally:
        client.close_session()
