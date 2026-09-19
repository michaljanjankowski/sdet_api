from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from requests import Response

from api_test_example.library.resource_agnt.rest_response import EmptyResponse, ErrorResponse, ResponseInfo
from api_test_example.utils.api_client import ApiClient

ResourceT = TypeVar("ResourceT", bound=BaseModel)
ResponseT = TypeVar("ResponseT", bound=BaseModel)


class QueryParams(BaseModel):
    field1: str | None = None
    page: int = 1
    page_size: int = 10

    def generate_params(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)


class AgentBase(Generic[ResourceT]):
    RESOURCE_NAME: str
    RESOURCE_TYPE: type[ResourceT]

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client
        self.resources: dict[int, ResourceT] = {}

    @staticmethod
    def generate_response(response: Response, response_type: type[ResponseT]) -> ResponseInfo[ResponseT]:
        payload = response.json() if response.content else {}
        parsed = response_type.model_validate(payload) if response.ok else ErrorResponse.model_validate(payload)
        return ResponseInfo[ResponseT](response=parsed, response_status=response.status_code)

    def _list(self, response_type: type[ResponseT], query_params: QueryParams | None = None) -> ResponseInfo[ResponseT]:
        response = self.api_client.get(self.RESOURCE_NAME, params=(query_params or QueryParams()).generate_params())
        return self.generate_response(response, response_type)

    def _get(self, resource: ResourceT, response_type: type[ResponseT]) -> ResponseInfo[ResponseT]:
        response = self.api_client.get(f"{self.RESOURCE_NAME}/{resource.id}")
        return self.generate_response(response, response_type)

    def _create(self, data: BaseModel, response_type: type[ResponseT]) -> ResponseInfo[ResponseT]:
        response = self.api_client.post(self.RESOURCE_NAME, data.model_dump())
        result = self.generate_response(response, response_type)
        if response.ok:
            resource = self.RESOURCE_TYPE.model_validate(result.response.model_dump())
            self.resources[resource.id] = resource
        return result

    def _update(self, resource: ResourceT, data: BaseModel, response_type: type[ResponseT]) -> ResponseInfo[ResponseT]:
        response = self.api_client.put(f"{self.RESOURCE_NAME}/{resource.id}", data.model_dump())
        result = self.generate_response(response, response_type)
        if response.ok:
            self.resources[resource.id] = self.RESOURCE_TYPE.model_validate(result.response.model_dump())
        return result

    def _delete(self, resource: ResourceT) -> ResponseInfo[EmptyResponse]:
        response = self.api_client.delete(f"{self.RESOURCE_NAME}/{resource.id}")
        result = self.generate_response(response, EmptyResponse)
        if response.ok:
            self.resources.pop(resource.id, None)
        return result

    def delete_all(self) -> None:
        for resource in list(self.resources.values()):
            self._delete(resource).check_status(204)
