
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

Response_T = TypeVar("Response_T")


class ErrorResponse(BaseModel):
    error: Any


class EmptyResponse(BaseModel):
    ...


class ResponseInfo(BaseModel, Generic[Response_T]):
    response: Union[Response_T, ErrorResponse, EmptyResponse]
    response_status: int