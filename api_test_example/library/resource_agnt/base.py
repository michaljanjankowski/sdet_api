
from __future__ import annotations

from json import JSONDecodeError
from typing import Any, Dict, Generic, Optional, Protocol, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from requests import Response

from api_test_example.utils.api_client import ApiClient
from api_test_example.library.resource_agnt.rest_response import EmptyResponse, ErrorResponse, ResponseInfo


class QueryParams(BaseModel):
    filters: Optional[Dict[Any, Any]] = None
    sort_field: Optional[str] = None
    sort_direction: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    page_all: Optional[bool] = False

    def generate_params(self) -> Dict[Any, Any]:
        result_params: Dict[Any, Any] = {}
        if self.filters:
            result_params.update(self.filters)
        if self.sort_field and self.sort_direction:
            result_params.update({"sort": self.sort_field})
            result_params.update({"sort_direction": self.sort_direction})
        if self.page and self.page_size:
            result_params.update({"page": self.page, "page_size": self.page_size})
        if self.page_all:
            result_params.update({"page_all": self.page_all})
        return result_params


class ResourceInfoBase(BaseModel):
    id: Union[int, str] = -1

    def __hash__(self) -> int:
        return hash((self.id, self.identifier()))

Resource_T = TypeVar("Resource_T", bound=ResourceInfoBase)
Response_T = TypeVar("Response_T", bound=BaseModel)

class AgentBaseResourceless:
    RESOURCE_NAME: str

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    @staticmethod
    def _decode_response(response: Response) -> Dict[str, Any]:
        if not response.content:
            return {}
        try:
            return dict(response.json())
        except JSONDecodeError:
            return {"content": response.content.decode().strip()}

    def generate_response(
        self, response_data: Response, response_type: Type[Response_T]
    ) -> ResponseInfo[Response_T]:
        payload = self._decode_response(response=response_data)
        return ResponseInfo(
            response=response_type(**payload) if response_data.ok else ErrorResponse(**payload),
            response_status=response_data.status_code,
        )

    def _list(
        self,
        response_type: Type[Response_T],
        query_params: QueryParams = QueryParams(),
    ) -> ResponseInfo[Response_T]:
        params = query_params.generate_params()
        response_data = self.api_client.get(path=self.RESOURCE_NAME, params=params)
        return self.generate_response(response_data=response_data, response_type=response_type)

class ResponseWithID(Protocol):
    id: int

class AgentBase(AgentBaseResourceless, Generic[Resource_T]):
    RESOURCE_TYPE: Type[Resource_T]

    def __init__(self, api_client: ApiClient) -> None:
        AgentBaseResourceless.__init__(self, api_client=api_client)
        self.resources: Dict[str, Resource_T] = {}

    def _get(
        self, resource: Resource_T, response_type: Type[Response_T]
    ) -> ResponseInfo[Response_T]:
        response_data = self.api_client.get(path=f"{self.RESOURCE_NAME}/{resource.id}")
        return self.generate_response(response_data=response_data, response_type=response_type)

    def _create(
        self, data: BaseModel, response_type: Type[Response_T]
    ) -> Tuple[Resource_T, ResponseInfo[Response_T]]:
        response_data = self.api_client.post(path=self.RESOURCE_NAME, json_data=data.json())

        resource_info = self.RESOURCE_TYPE.construct(**data.dict())

        payload = self._decode_response(response=response_data)
        response: Union[Response_T, ErrorResponse]
        if response_data.ok:
            response = response_type(**payload)
            resource_info.id = response.id
            self.resources[resource_info.identifier()] = resource_info
        else:
            response = ErrorResponse(**payload)
        return resource_info, ResponseInfo(
            response=response,
            response_status=response_data.status_code,
        )

    def _update(
        self,
        resource: Resource_T,
        data: BaseModel,
        response_type: Type[Response_T],
    ) -> Tuple[Resource_T, ResponseInfo[Response_T]]:
        response_data = self.api_client.put(
            path=f"{self.RESOURCE_NAME}/{resource.id}", json_data=data.json()
        )
        if response_data.ok and resource.identifier() in self.resources:
            old_resource = self.resources.pop(resource.identifier())
            resource = old_resource.copy(update=data.dict())
            self.resources[resource.identifier()] = resource
        return resource, self.generate_response(
            response_data=response_data, response_type=response_type
        )

    def _delete(self, resource: Resource_T) -> ResponseInfo[EmptyResponse]:
        response_data = self.api_client.delete(path=f"{self.RESOURCE_NAME}/{resource.id}")
        return self.generate_response(response_data=response_data, response_type=EmptyResponse)
