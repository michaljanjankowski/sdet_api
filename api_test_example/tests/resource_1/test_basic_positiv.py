from http import HTTPStatus
from api_test_example.library.data_gens.base import DataGen
from api_test_example.library.resource_agnt.resource_agnt import ResourceAgent


def test_resource1_create_one(
    resource_agent: ResourceAgent,
    data_gen: DataGen,
) -> None:
    resource1_info, response = resource_agent.resource_1.create(
        data=data_gen.resource1gen.create_data(
            field1="value1", field2="value2"
        )
    )
    response.check_ok_response(expected_status=HTTPStatus.CREATED)
