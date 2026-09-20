from http import HTTPStatus

import httpx
import pytest

from mockserver_example.clients.users_client import UserCreate, UsersClient


def test_list_users_is_parsed(users_client: UsersClient) -> None:
    users = users_client.list_users()
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].email == "ada@example.test"


def test_get_and_create_user(users_client: UsersClient) -> None:
    assert users_client.get_user(1).name == "Ada"
    created = users_client.create_user(UserCreate(name="Ada", email="ada@example.test"))
    assert created.id == 2
    users_client.delete_user(1)


@pytest.mark.parametrize(
    ("method", "path", "payload", "expected_status", "expected_error"),
    [
        ("GET", "/users/999", None, HTTPStatus.NOT_FOUND, "User not found"),
        ("POST", "/users", {"name": ""}, HTTPStatus.BAD_REQUEST, "Invalid user payload"),
        ("GET", "/error", None, HTTPStatus.INTERNAL_SERVER_ERROR, "Upstream unavailable"),
    ],
)
def test_error_contracts(
    raw_client: httpx.Client,
    method: str,
    path: str,
    payload: dict | None,
    expected_status: HTTPStatus,
    expected_error: str,
) -> None:
    response = raw_client.request(method, path, json=payload)
    assert response.status_code == expected_status
    assert response.json() == {"error": expected_error}


def test_client_raises_for_not_found(users_client: UsersClient) -> None:
    with pytest.raises(httpx.HTTPStatusError) as error:
        users_client.get_user(999)
    assert error.value.response.status_code == HTTPStatus.NOT_FOUND


def test_client_times_out_on_slow_response(mockserver_url: str) -> None:
    client = UsersClient(mockserver_url, timeout=0.1)
    try:
        with pytest.raises(httpx.TimeoutException):
            client.get_slow()
    finally:
        client.close()
