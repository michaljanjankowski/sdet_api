from unittest.mock import Mock

from mocking_example.mocking_example import StatusClient


def test_status_client_sends_expected_request() -> None:
    session = Mock()
    session.get.return_value.json.return_value = {"status": "ok"}

    result = StatusClient("https://example.test/api/", session=session).get_status()

    assert result == "ok"
    session.get.assert_called_once_with("https://example.test/api/status", timeout=5)
    session.get.return_value.raise_for_status.assert_called_once_with()
