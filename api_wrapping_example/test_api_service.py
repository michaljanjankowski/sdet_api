from unittest.mock import Mock

import pytest
import requests

from api_wrapping_example.api_service import API_Service
from api_wrapping_example.api_wrapper import summarize_animals


def test_get_animal_parses_list_and_keeps_history_per_instance() -> None:
    session = Mock()
    session.get.return_value.json.return_value = [
        {
            "name": "Cat",
            "taxonomy": {"kingdom": "Animalia"},
            "locations": ["Worldwide"],
            "characteristics": {"diet": "Carnivore"},
        }
    ]
    service = API_Service(api_key="example-key", session=session)

    animals = service.get_animal("cat")

    session.get.assert_called_once_with(
        "https://api.api-ninjas.com/v1/animals",
        params={"name": "cat"},
        headers={"X-Api-Key": "example-key"},
        timeout=5,
    )
    assert animals[0].name == "Cat"
    assert summarize_animals(animals) == {"Cat": {"diet": "Carnivore"}}
    assert service.calls_history == [animals]
    assert API_Service(api_key="other-key", session=Mock()).calls_history == []


def test_get_animal_propagates_http_error_without_recording_result() -> None:
    session = Mock()
    session.get.return_value.raise_for_status.side_effect = requests.HTTPError("503")
    service = API_Service(api_key="example-key", session=session)

    with pytest.raises(requests.HTTPError):
        service.get_animal("cat")

    assert service.calls_history == []
