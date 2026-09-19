from api_test_example.library.resource_agnt.resource_1_agnt import Resource1Agnt
from api_test_example.utils.api_client import ApiClient


class ResourceAgent:
    def __init__(self, api_client: ApiClient) -> None:
        self.resource_1 = Resource1Agnt(api_client)

    def delete_all(self) -> None:
        self.resource_1.delete_all()
