from typing import Any, Dict, Optional, Tuple
from api_test_example.library.resource_agnt.base import AgentBase, QueryParams, ResourceInfoBase
from api_test_example.library.resource_agnt.rest_response import EmptyResponse, ResponseInfo
from product_source_code import (Resource1PostRequest, Resource1PostResponse, Resource1GetResponse,
                                 Resource1ListResponse, Resource1PutRequest, Resource1GetSpecialActionResponse)



class Resource1_Info(ResourceInfoBase):
    name: str

    def identifier(self) -> str:
        return self.name


class Resource1Agent(AgentBase[Resource1_Info]):  # pylint: disable=too-many-public-methods
    RESOURCE_NAME = "resource1"
    RESOURCE_TYPE = Resource1_Info

    def create(self, data: Resource1PostRequest) -> Tuple[Resource1_Info, ResponseInfo[Resource1PostResponse]]:

        return self._create(data=data, response_type=Resource1PostResponse)

    def get(self, resource1: Resource1_Info) -> ResponseInfo[Resource1GetResponse]:
        return self._get(resource=resource1, response_type=Resource1GetResponse)

    def list(
        self, query_params: QueryParams = QueryParams()
    ) -> ResponseInfo[Resource1ListResponse]:
        return self._list(response_type=Resource1ListResponse, query_params=query_params)

    def update(
        self, resource1: Resource1_Info, data: Resource1PutRequest
    ) -> Tuple[Resource1_Info, ResponseInfo[EmptyResponse]]:
        return self._update(resource=resource1, data=data, response_type=EmptyResponse)

    def delete(self, hypervisor: Resource1_Info) -> ResponseInfo[EmptyResponse]:
        return self._delete(resource=hypervisor)

    def special_action_on_enpoint(
        self, resource1: Resource1_Info
    ) -> ResponseInfo[Resource1GetSpecialActionResponse]:
        response_data = self.api_client.get(
            path=f"{self.RESOURCE_NAME}/{resource1.id}/special-action-enpoint",
        )
        return self.generate_response(
            response_data=response_data, response_type=Resource1GetSpecialActionResponse
        )

