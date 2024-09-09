
from typing import Dict, List, Union
from api_test_example.utils.api_client import ApiClient
from api_test_example.library.resource_agnt.resource_1_agnt import Resource1Agnt
from api_test_example.library.resource_agnt.resource_2_agnt import Resource2Agnt
from api_test_example.library.resource_agnt.users_agnt import UsersAgnt


class ResourceAgent:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client
        self.users = UsersAgnt(api_client=api_client)
        self.resource_1 = Resource1Agnt(api_client=api_client)
        self.resource_2 = Resource2Agnt(api_client=api_client)

    def delete_all(self) -> None:
        self.resource_1.delete_all()

    def operate_on_combination_of_resources(self):
        resource_id = self.resource_1.resources[0]
        self.resource_2.create(resource_id)
