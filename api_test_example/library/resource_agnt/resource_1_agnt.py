from api_test_example.library.resource_agnt.base import AgentBase, QueryParams
from api_test_example.library.resource_agnt.rest_response import EmptyResponse, ResponseInfo
from api_test_example.models import (
    Resource1GetSpecialActionResponse,
    Resource1ListResponse,
    Resource1PostRequest,
    Resource1PutRequest,
    Resource1Response,
)


class Resource1Agnt(AgentBase[Resource1Response]):
    RESOURCE_NAME = "resource1"
    RESOURCE_TYPE = Resource1Response

    def create(self, data: Resource1PostRequest) -> ResponseInfo[Resource1Response]:
        return self._create(data, Resource1Response)

    def get(self, resource: Resource1Response) -> ResponseInfo[Resource1Response]:
        return self._get(resource, Resource1Response)

    def list(self, query_params: QueryParams | None = None) -> ResponseInfo[Resource1ListResponse]:
        return self._list(Resource1ListResponse, query_params)

    def update(self, resource: Resource1Response, data: Resource1PutRequest) -> ResponseInfo[Resource1Response]:
        return self._update(resource, data, Resource1Response)

    def delete(self, resource: Resource1Response) -> ResponseInfo[EmptyResponse]:
        return self._delete(resource)

    def special_action(self, resource: Resource1Response) -> ResponseInfo[Resource1GetSpecialActionResponse]:
        response = self.api_client.get(f"{self.RESOURCE_NAME}/{resource.id}/special-action")
        return self.generate_response(response, Resource1GetSpecialActionResponse)
